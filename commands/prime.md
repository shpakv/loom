---
description: Bootstrap Loom session context (conventions, glossary, active scope)
argument-hint: [epic-<slug> | package-path]
---
Bootstrap the Loom working context before any other work:

1. Read `docs/loom.yaml` for paths and phase config.
2. Read the `loom-core` skill conventions.
3. Read `docs/product/GLOSSARY.md` if present — use its terms verbatim everywhere.
4. Read `docs/conventions/*.md` if present.
5. If `$ARGUMENTS` names an epic (`epic-<slug>`): read its `epic.md` and
   `design.md`. If it names a package path: read that package's `SKILL.md`.
6. Run `python3 scripts/loom/index_gen.py --print` if available.
7. Run `python3 scripts/loom/oq_scan.py docs/` to see where blocking questions
   sit — these are the most likely "where was I" markers.
8. Check the seam: which tasks carry `handoff:` with `harvested: false` (handed
   to the engine, facts not yet folded back), and whether
   `python3 scripts/loom/compile.py --check` reports the engine's files stale.

Finish with a one-paragraph summary AND a "resume here" line so a returning
session knows where it stopped: the loaded context and document statuses, then
the single most likely next action — the nearest open blocking OQ, a handed-off
task awaiting /loom:harvest, a stale projection awaiting /loom:compile, the last
task left in-review, or the next command the phase sequence implies. If nothing
is in flight, say so. Do not start any work before this.

Loom does not implement: if the user's next step is writing code, the answer is
/loom:compile and then their SDD engine — not this session.
