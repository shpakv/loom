---
description: Loom phase — design the logical structure (building blocks + solution strategy) as a hypothesis, before choosing technologies
---
Use the `loom-architecture-phase` skill (read `loom-core` first).

Verify `quality-requirements.md` is `approved` before starting; otherwise route
to /loom:requirements. Derive building blocks from responsibilities (never
layers), draw the allowed and forbidden dependency graph, and map every quality
scenario to a structural approach and the technology fork it leaves open. Choose
NO technologies — name the forks, not the answers; leave the ADR column empty.
The output is a draft hypothesis the skeleton will test, not accepted
architecture. Finish with `link_check.py docs` and review of both documents.
