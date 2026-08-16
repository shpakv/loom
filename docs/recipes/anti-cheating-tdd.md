# Recipe: anti-cheating TDD by information asymmetry

**This is not part of the Loom plugin.** Nothing here is loaded, dispatched, or
executed by any `/loom:*` command. Loom stopped implementing code in 0.20.0 —
it produces the knowledge layer and hands a task `## Spec` to an external SDD
engine (see `CONCEPT.md` §5). This file is the machinery that used to live in
`/loom:implement`, kept because it is **orthogonal to whose engine runs the
loop** and SDD engines generally ship nothing like it: they instruct the model
to be honest rather than removing its ability to cheat.

Take it with you. The three scripts next to this file are the originals, moved
here verbatim — they are stdlib-only Python 3 CLIs with no Loom imports.

## The problem it solves

An agent that can see the implementation while writing the test will write a
test the implementation passes. An agent that can edit the test to reach green
will edit the test. Neither is misconduct — both are the shortest path to the
stated goal. Instructions do not help: the model that is told "do not weaken
assertions" weakens assertions under pressure, and reports success.

The fix is structural. Split the work across agents with **disjoint fields of
view**, enforce the split with a **hook on file paths**, and verify each
transition with an **exit code** rather than an agent's opinion.

## Role topology

One orchestrating session dispatches all four and writes no code itself.

| Role | Sees | Must not | Writes |
|---|---|---|---|
| planner | spec, design doc, package docs, current code | write any code | the plan (just-in-time) |
| test-author | spec, one plan step, public API docs, contracts | open implementation internals | test files only (hook-enforced) |
| implementer | the failing test, spec, package docs | modify tests (hook-enforced) | src only |
| code-reviewer | final diff, spec, conventions | — fresh context by design | review findings |

Two properties carry the whole recipe:

- **the test-author never reads src.** If the public surface is unclear from the
  package documentation, that is a documentation defect to report — not a reason
  to go look. This is what makes the test a statement about the contract.
- **the reviewer never participated.** Fresh context is the value; a reviewer who
  watched the authoring inherits its blind spots.

## The loop

Per plan step:

1. dispatch test-author → one new failing test;
2. `verify_red.py --expect <substring>` → **red for the right reason**;
   commit `RED(<task>): <step>`;
3. dispatch implementer → minimal code to green;
4. `verify_green.py` → whole suite passes; commit `GREEN(<task>): <step>`;
5. optional refactor under green; `verify_green.py` again; commit `REFACTOR(...)`.

Then once: dispatch code-reviewer on the full diff, loop until its verdict is
`APPROVED`.

`--expect` is the load-bearing flag. A test that is red because of a typo, a
missing import, or an empty body is not red for the right reason — without the
expected-failure substring, "the test failed" is indistinguishable from "the test
is broken", and an empty test file passes the red gate trivially.

The three commits per step are not bookkeeping: they are the only durable
evidence the reviewer has that the test genuinely failed before the code existed.
A step that arrives at green with no `RED` commit is the exact cheat this
preserves against.

## Enforcement

`guard_file_roles.py` is a `PreToolUse` hook on `Edit|Write|MultiEdit`. It reads
the current role from `.loom/role` (the orchestrator writes it around each
dispatch, and it is gitignored) and:

- no marker → allow everything;
- `test-author` → may write **only** files matching the test globs;
- `implementer` → may write anything **except** files matching the test globs.

It blocks with exit code 2 and an explanatory message on stderr, which the agent
sees. Wire it up in the harness config, e.g. for Claude Code:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [{ "type": "command", "command": "python3 path/to/guard_file_roles.py" }]
      }
    ]
  }
}
```

Note on config: the scripts read `test_command:` and `test_globs:` from
`docs/loom.yaml` by naive line parsing. **Loom no longer ships either key** —
add them yourself, or edit the two parse functions to read your engine's config
instead. `verify_red.py`/`verify_green.py` also accept `--cmd "<test command>"`,
which sidesteps the config entirely.

## Test-change protocol

Tests are append-only for the implementer. A test may be changed only by an
explicit orchestrator decision, in the open, with a logged line: what changed,
why, who decided. The implementer that believes a test is wrong returns an
`OBJECTION` — quoting the test expectation and the spec line it contradicts —
rather than editing it. Never route around red: no skips, no commented-out
assertions, no widened matchers, no test-environment tricks.

## Rigor as a dial

Full role separation is not always worth its cost. The bar used to be: `full`
when the task touches a public contract, a domain invariant, or more than one
package; `light` otherwise (one package, no contract, no invariant).

`light` runs one agent doing classic TDD, which means **trading the role guard
for the commit trail**: with a single agent there is no asymmetry left for the
hook to enforce (clear `.loom/role`), so the verify scripts, the separate `RED`
commit, and the fresh-context reviewer become the whole of the integrity
guarantee — all three stay mandatory. A `light` task that turns out to touch a
contract mid-flight escalates to `full` rather than finishing as it started.

Loom still emits this signal: every task file carries `rigor: full | light` as
advice about the cost of being wrong. What an engine does with it is its own
business.

## The part that stayed in Loom

The old implement phase also carried **upstream-defect escalation**: when code
and an approved document disagree, the document is the bug — stop, raise a
blocking open question on the owning document, and route to the phase that owns
it, rather than quietly building around it.

That half did not move here. It is the reverse edge of the seam and now lives in
`/loom:harvest` (`CONCEPT.md` §5), which reads what the engine actually did and
folds the facts back into the knowledge layer. If you adopt this recipe, keep
that channel open in whatever form your engine allows — a loop with no way to
say "the spec is wrong" converges on a confidently wrong implementation.
