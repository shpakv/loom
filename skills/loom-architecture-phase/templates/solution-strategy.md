---
id: solution-strategy
status: draft
owner: pair
updated: {date}
---
# Solution strategy

Half a page maximum. The through-line from each quality scenario to the
decision that will satisfy it. At architecture time these are decisions
still to be MADE, not yet accepted ADRs — name the fork, not the answer.

| Quality scenario | Satisfied by (approach / building block) | Decision still open |
|---|---|---|
| QS-{slug} | {block or tactic that carries this NFR} | {tech fork to resolve in /loom:technology, or "none — structural"} |

Unmapped QS = missing structural approach or decorative NFR — neither may
survive review. A row whose "decision still open" is a technology fork
becomes a proposed ADR in /loom:technology and is filled back in here
(→ ADR-{slug}) at /loom:consolidate.

## Open questions
- [ ] OQ-strategy-{topic}: ...
