---
description: Show Loom project status — document statuses and open questions
---
Run and interpret for the user:

1. `python3 scripts/loom/index_gen.py --print`
2. `python3 scripts/loom/oq_scan.py docs/`

Also compare `scripts_version` in docs/loom.yaml with the installed plugin version; on mismatch suggest `/loom:init --refresh`.

Summarize: which documents are draft / in-review / approved, how many blocking
OQs are open and where, and suggest the single most useful next Loom command.
If the project has accepted ADRs and no recent audit, mention that /loom:audit
can re-check whether those decisions still hold against their revisit triggers.
