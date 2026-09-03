---
description: Show Loom project status — document statuses, open questions, and generated-index health
---
Use the `loom-status-method` skill and interpret for the user:

1. `python3 scripts/loom/index_gen.py --print`
2. `python3 scripts/loom/oq_scan.py docs/`
3. `python3 scripts/loom/change_scan.py --json` when the configured changes
   path exists
4. Check whether `docs/INDEX.md` and `docs/roadmap/ROADMAP.md` are generated
   and current; regenerate them when needed.

Also report `loom_version` when present, and compare `scripts_version` in
docs/loom.yaml with the shipped scripts version; on mismatch suggest
`/loom:init --refresh`. The plugin package version, framework version and
scaffolded scripts version are independent.

Summarize which documents are draft / in-review / approved, how many blocking
OQs are open and where, whether generated indexes are current, and the single
most useful next Loom command. Summarize unfinished change records, their
routes and affected/blocked scope. Unresolved questions, changes waiting for a
human decision and documents waiting for review outrank new work.
If the project has accepted ADRs and no recent audit, mention that /loom:audit
can re-check whether those decisions still hold against their revisit triggers.
