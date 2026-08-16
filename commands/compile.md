---
description: Loom handoff — compile the knowledge layer into the files the SDD engine reads (constitution + epic seed spec)
argument-hint: [epic-<slug>]
---
Use the `loom-compile-phase` skill (read `loom-core` first) on epic: $ARGUMENTS

Gate first: no blocking open questions in the epic's design doc or task specs —
a spec the engine has to guess at must not be handed off. Then run
`python3 scripts/loom/compile.py [--epic <epic>]`, read the assembled output for
lossy ADR digests and for conventions that contradict rules, mark every handed-off
task with `handoff:`, and end with the single command the human should run in the
engine. Never hand-edit a compiled file; never write anything under docs/ here.
