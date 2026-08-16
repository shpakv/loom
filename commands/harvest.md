---
description: Loom seam — read what the SDD engine built and fold the facts it decided on its own back into the docs
argument-hint: [TASK-<slug> | git range]
---
Use the `loom-harvest-method` skill (read `loom-core` first) on: $ARGUMENTS

Do NOT read the diff yourself first — dispatch the `loom-harvester` subagent with
fresh context, then route each of its findings to the one place its class belongs
(term → GLOSSARY, number → RULES as BR-*, decision → proposed ADR, surface →
package SKILL.md, contradiction → blocking OQ on the document). Never edit a
document to match the code: the document may be right. Finish by setting
`harvested: true` and `landed:` on the task and re-running /loom:compile if the
constitution's sources changed. This is not a code review — quality is the
engine's business.
