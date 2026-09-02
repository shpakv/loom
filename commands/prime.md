---
description: Bootstrap Loom session context (conventions, glossary, active scope)
argument-hint: [epic-<slug>]
---
Use the `loom-prime-method` skill to bootstrap the Loom working context before
any other work:

1. Read `docs/loom.yaml` for paths and phase config.
2. Read the `loom-core` skill conventions.
3. Read `docs/product/GLOSSARY.md` if present — use its terms verbatim everywhere.
4. Read `docs/conventions/*.md` if present.
5. If `$ARGUMENTS` names an epic (`epic-<slug>`): read its `epic.md` and
   `design.md`.
6. Run `python3 scripts/loom/index_gen.py --print` if available.
7. Run `python3 scripts/loom/oq_scan.py docs/` to see where blocking questions
   sit — these are the most likely "where was I" markers.
8. If the configured changes path exists, run
   `python3 scripts/loom/change_scan.py --json` and inspect the nearest
   captured, triaged, accepted or in-progress change.
9. Check for the nearest unresolved work: blocking OQs, unfinished changes, documents left
   `in-review`, stale generated indexes, or an ADR that needs an audit.

Finish with a one-paragraph summary AND a "resume here" line so a returning
session knows where it stopped: the loaded context and document statuses, then
the single most likely next action — the nearest open blocking OQ, a handed-off
the last task left in-review, or the next command the phase sequence implies. If
nothing is in flight, say so. Do not start any work before this.

Loom is a requirements repository: if the user's next step is implementation,
the approved documents are the source of truth, but implementation is outside
this workflow.
