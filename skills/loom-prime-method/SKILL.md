---
name: loom-prime-method
description: Bootstrap a portable Loom session by reading configuration, conventions, current indexes and unresolved questions.
---

# Loom prime method

Read `docs/loom.yaml`, then `loom-core`, the glossary, conventions, and the
relevant approved documents. Run the configured index and open-question gates
when the scripts are available. If `docs/changes/` exists, run the change schema
gate and prioritize the nearest captured, triaged, accepted or in-progress
change, its prerequisites and affected scope. Summarize document statuses,
unresolved blocking questions, unfinished changes, and the single next Loom
action. Do not start work while priming. This method is host-neutral; Claude
commands, Codex and Copilot may all invoke it.
