---
name: loom-implement-phase
description: Loom implement phase (command /loom:implement TASK-<slug>) — orchestrate TDD implementation of one task via role-separated subagents (planner, test-author, implementer, code-reviewer) with deterministic red/green verification. Use whenever the user runs /loom:implement, asks to implement a task, or start coding a planned task.
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

0. Write `.loom/role` = `planner`, dispatch loom-planner → it fills `## Plan`
   (steps of behavior → test → minimal change; contracts touched; proposed
   rigor). **Stop and show the plan to the human** — this is the cheap gate.
   `rigor: light` (from task frontmatter, planner may propose changing it):
   steps 1–5 may run in one agent doing classic TDD, but verify scripts,
   guards and the reviewer remain mandatory.

For each plan step (rigor: full):
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

Then:
6. Clear `.loom/role`. Dispatch loom-code-reviewer (fresh context) → findings
   into `## Review`. Non-trivial fixes go through the cycle again.
7. Closure gates: verify_green; SKILL.md of touched packages updated if their
   public surface changed; changelog fragment `changes/TASK-<slug>.md` written;
   `oq_scan --gate` on the task file; `link_check.py docs packages`.
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
