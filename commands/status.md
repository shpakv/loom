---
description: Show Loom project status — document statuses, open questions, and the state of the handoff seam
---
Run and interpret for the user:

1. `python3 scripts/loom/index_gen.py --print`
2. `python3 scripts/loom/oq_scan.py docs/`
3. `python3 scripts/loom/compile.py --check` (skip if `engine.name` is empty in
   docs/loom.yaml — then the finding IS that no engine is configured)

Also compare `scripts_version` in docs/loom.yaml with the installed plugin version; on mismatch suggest `/loom:init --refresh`.

Summarize: which documents are draft / in-review / approved, how many blocking
OQs are open and where, and the state of the seam — tasks with `handoff:` set and
`harvested: false` (the engine has them, their facts are not back yet) and whether
the compiled projection is stale. Then suggest the single most useful next Loom
command. Unharvested work outranks new work: a growing set of handed-off,
unharvested tasks means the docs are drifting behind the code, which is the one
failure mode that quietly voids the whole knowledge layer.
If the project has accepted ADRs and no recent audit, mention that /loom:audit
can re-check whether those decisions still hold against their revisit triggers.
