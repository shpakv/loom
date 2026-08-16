---
id: TASK-{pkg-change}
status: draft
track: track-{slug}
rigor: full            # full | light — advisory signal to the engine; full if public contracts, invariants, or >1 package
depends_on: []         # TASK ids within the epic
packages: []           # packages touched; their SKILL.md is mandatory context
handoff: ""            # engine this spec was compiled for; empty = not handed off yet
landed: ""             # PR / commit the engine closed it with
harvested: false       # has /loom:harvest folded its facts back into the docs?
updated: {date}
---
# TASK: {package + change, glossary terms}

## Spec
**Behavior:** what becomes true, observable, in glossary terms.
**Acceptance:** checkable criteria with numbers, traced to UC-*/design sections.
**Contracts touched:** {contract files or "none"}.
**Out of scope:** explicit non-goals of this task.

<!--
This is the last artifact Loom writes for this task. The plan, the tests, the
code and the diff review belong to the SDD engine — see CONCEPT.md §5.
Do not name internal files, functions, or a step order here: how to build it is
the engine's choice, and pinning it here is how a spec goes stale.
-->

## Open questions
- [ ] OQ-{task-slug}-{topic}: ...
