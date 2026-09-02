---
description: Loom utility — capture and triage incoming work, persist durable changes, and route them to the smallest phase that fits
argument-hint: [idea | bug | feature request in a sentence]
---
Use the `loom-intake-method` skill (read `loom-core` first).

Incoming item from the user: $ARGUMENTS

Use the loom-intake-method skill. First preserve the incoming item in the
configured changes path from docs/loom.yaml (normally docs/changes/CHG-<slug>.md)
unless it is an immediate draft-only additive edit.
If VISION.md does not yet exist, stop after capture and report the change ID.
Otherwise run a short triage interview (one question per turn), calculate the
ID-based impact, and route to the smallest honest owning phase. Do not start the
downstream phase or decide accepted/rejected on the human's behalf. Return the
change ID, classification, blast radius, single next command and prerequisites.
