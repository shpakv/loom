---
description: Loom implement phase — orchestrated TDD of one task via role-separated subagents
argument-hint: <TASK-slug>
---
Use the `loom-implement-phase` skill (read `loom-core` first) for: $ARGUMENTS

You are the orchestrator: dispatch loom-planner first, show the plan to the
human, then run the red/green cycle with loom-test-author and loom-implementer,
verify via scripts, finish with loom-code-reviewer and closure gates. Never
write code or tests yourself. Maintain `.loom/role` around every dispatch.
