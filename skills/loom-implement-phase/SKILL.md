---
name: loom-implement-phase
description: Invoked by the /loom:implement command to orchestrate TDD implementation of one task via role-separated subagents (planner, test-author, implementer, code-reviewer) with deterministic red/green verification and a file-role guard. Run /loom:implement TASK-<slug> on a planned task.
---

# Loom: implement phase (per task)

The main session is an ORCHESTRATOR: it dispatches subagents, runs verify
scripts, writes role markers and commits — it never writes production code or
tests itself. Cheating is prevented by information asymmetry and file-role
guards, not by instructions. Read `loom-core` first.

## Inputs (gate)

An approved task file with `## Spec`; approved design.md of its epic;
SKILL.md of every package in `packages:`. `test_command` configured in
`docs/loom.yaml`.

## Role topology

| Role | Sees | Must not | Writes |
|---|---|---|---|
| loom-planner | spec, design.md, SKILL.md, current code | write any code | `## Plan` in task file |
| loom-test-author | spec, plan step, SKILL.md public API, contracts | open implementation internals; touch src | test files only (guard-enforced) |
| loom-implementer | failing test, spec, SKILL.md | modify tests (guard-enforced) | src only |
| loom-code-reviewer | final diff, spec, conventions, SKILL.md | — fresh context by design | `## Review` findings |

Verification is SCRIPTS, not agents: `verify_red.py` / `verify_green.py` —
an agent can be argued with, an exit code cannot.

## Cycle

The cycle has three parts: **Setup** (once) → **Per-step loop** (each plan step)
→ **Closure** (once). Which loop you run depends on the task's `rigor`.

### Setup (once)

0. Write `.loom/role` = `planner`, dispatch loom-planner → it fills `## Plan`
   (steps of behavior → test → minimal change; contracts touched; proposed
   rigor). **Stop and show the plan to the human** — this is the cheap gate.
   The planner may propose changing the task's `rigor`; the human decides.

### Per-step loop — `rigor: full` (role-separated)

Full rigor is the default and the one the anti-cheating machinery protects:
test-author and implementer are different subagents, and the file-role guard
(`.loom/role`) physically stops each from touching the other's files. Run this
for every plan step:

1. `.loom/role` = `test-author`, dispatch loom-test-author with ONLY the spec,
   this step, SKILL.md and contracts → new failing test.
2. `python3 scripts/loom/verify_red.py [--expect <substr>]` — red for the
   RIGHT reason. Commit `RED(TASK-<slug>): <step>`.
3. `.loom/role` = `implementer`, dispatch loom-implementer → minimal code to
   green. If it believes the test is wrong, it returns an OBJECTION to the
   orchestrator instead of editing the test.
4. `python3 scripts/loom/verify_green.py`. Commit `GREEN(TASK-<slug>): <step>`.
5. Optional refactor by implementer under green; verify_green again.
   Commit `REFACTOR(TASK-<slug>): <step>`.

### Per-step loop — `rigor: light` (single agent)

Light rigor is for low-risk tasks only — one package, no public contract, no
domain invariant (the same bar /loom:design uses to assign it). One agent does
classic TDD (write failing test → make it pass → refactor) instead of two.

This deliberately **trades the role guard for the commit trail**: with a single
agent there is no test-author/implementer asymmetry for the guard to enforce, so
`.loom/role` is CLEARED (no marker → the guard allows all edits) and the
integrity of the step rests entirely on the verify scripts and the audit trail
that remain mandatory:

- `verify_red.py` must pass BEFORE any implementation — the test must genuinely
  fail first, and the separate `RED(...)` commit proves it did. A step that goes
  straight to green with no red commit is the exact cheat this preserves against.
- `verify_green.py` must pass after; commit `GREEN(...)` (and `REFACTOR(...)`).
- The fresh-context reviewer in Closure still runs — it is the independent check
  that replaces the second pair of eyes the role split would have given.

If a light task turns out to touch a contract or a domain invariant mid-flight,
stop and escalate it to `full` (re-dispatch with role separation) rather than
finishing single-agent.

### Closure (once)

6. Clear `.loom/role`. Dispatch loom-code-reviewer (fresh context) → numbered
   findings into `## Review`, ending in its `APPROVED` / `BLOCKED (n)` verdict.
   Loop back through the relevant per-step cycle until the verdict is APPROVED.
7. Closure gates: `python3 scripts/loom/verify_green.py`; SKILL.md of touched
   packages updated if their public surface changed; changelog fragment
   `changes/TASK-<slug>.md` written; `python3 scripts/loom/oq_scan.py --gate`
   on the task file; `python3 scripts/loom/link_check.py docs packages`.
   Task → `approved`.

## Test-change protocol

Tests are append-only for the implementer. A test may be modified only by
orchestrator decision (human-visible), and every such change gets a line in
the task's `## Test-change log`: what changed and why. A red test is work for
the code — silence-editing it into green is structurally blocked by
`guard_file_roles.py` — installed automatically as a plugin hook;
`.loom/` is gitignored by /loom:init.

## Upstream-defect escalation (code → docs)

Implementation is the phase where documents meet reality, so it is where a wrong
document is discovered — not where it is quietly worked around. Loom is
docs-first: if the code and an `approved` upstream document disagree, the default
is that the DOCUMENT is the bug to fix, not the thing to route around in code.

Distinguish two kinds of "this is wrong", because they escalate differently:

- **The test contradicts the spec** → local; use the test-change protocol above.
  The spec is still the authority; the test was written wrong.
- **The spec / design.md / an ADR / a contract is itself wrong or incomplete** →
  the authority itself is the defect. STOP the red/green cycle. Do NOT invent a
  spec, widen scope, or build around the gap. Raise a `(blocking)` OQ on the
  OWNING document (not on the task), stating what the code revealed and why the
  document cannot be honestly satisfied, then route to the phase that owns it:
  a task/design defect → /loom:design; a wrong or missing decision → a
  superseding ADR via /loom:consolidate (or /loom:audit if a revisit trigger
  fired); a vision/scope conflict → /loom:review on the upstream doc. Record the
  halt in the task's `## Plan` so the next session sees why it stopped.

The signal from planner or implementer is the same escalation surfacing at
different depths: the planner emits blocking OQs when the spec is ambiguous
before any code; the implementer returns an OBJECTION mid-cycle. When that
objection is "the test is wrong", handle it locally; when it is "the document is
wrong", it becomes an upstream-defect escalation. Discovering a broken document
here — one task in — is a success of docs-first, exactly as the skeleton
refuting an ADR is: cheap correction now beats silent drift compounding across
every later task built on the same wrong document.

## Rules

- One task per /loom:implement invocation; parallel tasks = parallel sessions
  on different tracks.
- Never proceed past a failed verify script; never skip the RED commit.
- An empty or assertion-free test found by verify_red is a test-author defect,
  not a pass.
