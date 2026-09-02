---
description: Loom phase — specify and record the smallest falsification exercise for proposed architecture or technology decisions
---
Use the `loom-skeleton-phase` skill (read `loom-core` first).

Verify inputs: approved GLOSSARY, VISION (minimum), quality-requirements, the
architecture hypothesis (building-blocks, solution-strategy) with its proposed
technology ADRs, and optionally one approved first-slice epic to provide the
scenario.

Do not prescribe production implementation. Write the brief as a record of an
external experiment — what each proposed ADR must demonstrate, which boundaries
must be traversed, the `Faked:` list, and the observation that would refute the
hypothesis. Label every fake and shortcut, and record the raw result on each
affected ADR. If the evidence refutes a decision or surfaces a
fork the technology phase missed, say so with a new/updated proposed ADR and a
blocking OQ. Do not accept one-way ADRs — that is /loom:consolidate's job.
