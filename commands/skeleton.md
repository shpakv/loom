---
description: Loom phase — build the walking skeleton: thinnest end-to-end slice that validates the proposed architecture and technology decisions
---
Use the `loom-skeleton-phase` skill (read `loom-core` first).

Verify inputs: approved GLOSSARY, VISION (minimum), quality-requirements, the
architecture hypothesis (building-blocks, solution-strategy) with its proposed
technology ADRs, and exactly one approved first-slice epic. Build the slice on
those proposed decisions and record on each ADR what the skeleton demonstrated;
if the build refutes a decision or surfaces a fork the technology phase missed,
say so with a new/updated proposed ADR and a blocking OQ. Give every new package
its SKILL.md at birth. Do not accept one-way ADRs — that is /loom:consolidate's
job.
