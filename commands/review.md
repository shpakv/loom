---
description: Loom gate — review a document, resolve open questions, manage status transition
argument-hint: <path/to/document.md>
---
Use the `loom-review-gate` skill (read `loom-core` first) on: $ARGUMENTS

If this session authored that document, dispatch the `loom-reviewer` subagent
instead of reviewing inline, and relay its findings.
