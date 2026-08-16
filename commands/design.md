---
description: Loom design phase — decompose the approved epic into design doc, tracks, and session-sized task specs
argument-hint: [epic-<slug>]
---
Use the `loom-design-phase` skill (read `loom-core` first) on epic: $ARGUMENTS

Contracts first, tracks as conflict-free workstreams, tasks sized to one
session. `## Spec` is the whole task file — never write a plan, a step order, or
internal file names into it; that is the engine's half of the seam. Finish with
review of design.md, then hand the epic off with /loom:compile.
