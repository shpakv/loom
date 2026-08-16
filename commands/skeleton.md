---
description: Loom phase — specify the walking skeleton as a falsification brief, then read its result onto the proposed decisions
---
Use the `loom-skeleton-phase` skill (read `loom-core` first).

Verify inputs: approved GLOSSARY, VISION (minimum), quality-requirements, the
architecture hypothesis (building-blocks, solution-strategy) with its proposed
technology ADRs, and exactly one approved first-slice epic.

You do not build the slice. Write the brief — what each proposed ADR must
demonstrate, which layers must be traversed, the `Faked:` list, and the
observation that would refute the hypothesis — give every new package its
SKILL.md before the build, and hand off with /loom:compile. When the slice runs,
harvest it: record on each ADR what was actually exercised (discounting anything
that ran through a fake), and if the build refutes a decision or surfaces a fork
the technology phase missed, say so with a new/updated proposed ADR and a
blocking OQ. Do not accept one-way ADRs — that is /loom:consolidate's job.
