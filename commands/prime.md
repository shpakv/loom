---
description: Bootstrap Loom session context (conventions, glossary, active scope)
argument-hint: [E-XXX | package-path]
---
Bootstrap the Loom working context before any other work:

1. Read `docs/loom.yaml` for paths and phase config.
2. Read the `loom-core` skill conventions.
3. Read `docs/product/GLOSSARY.md` if present — use its terms verbatim everywhere.
4. Read `docs/conventions/*.md` if present.
5. If `$ARGUMENTS` names an epic (E-XXX): read its `epic.md` and `design.md`.
   If it names a package path: read that package's `SKILL.md`.
6. Run `python3 scripts/loom/index_gen.py --print` if available.

Finish with a one-paragraph summary: loaded context, document statuses, and what
appears to be the current active work. Do not start any task before this.
