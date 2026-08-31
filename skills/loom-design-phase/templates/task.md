---
id: TASK-{pkg-change}
status: draft
track: track-{slug}
rigor: full            # full | light — advisory signal for review effort; full if public contracts, invariants, or >1 package
depends_on: []         # TASK ids within the epic
packages: []           # packages touched; their SKILL.md is mandatory context
updated: {date}
---
# TASK: {package + change, glossary terms}

## Spec
**Behavior:** what becomes true, observable, in glossary terms.
**Acceptance:** checkable criteria with numbers, traced to UC-*/design sections.
**Contracts touched:** {contract files or "none"}.
**Out of scope:** explicit non-goals of this task.

<!--
This is the requirements artifact for this task. The plan, tests, code and diff
review are outside Loom.
Do not name internal files, functions, or a step order here: how to build it is
an implementation choice, and pinning it here is how a requirement goes stale.
-->

## Open questions
- [ ] OQ-{task-slug}-{topic}: ...
