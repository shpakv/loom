---
id: epic-{slug}-design
status: draft
owner: pair
updated: {date}
---
# Design: epic-{slug}

## Scope recap
2–3 sentences + link to epic. What this design does NOT cover.

## Domain changes
New/changed aggregates, events, invariants — glossary terms only.
New terms go to GLOSSARY.md first.

## Contracts
| Contract | File (source of truth) | Consumers |
|---|---|---|
| {api} | contracts/{name}.yaml | track-{a}, track-{b} |

## Data changes
Migrations, new tables/streams, retention. Or "none".

## Test strategy
What is covered at which level (unit/integration/e2e); fixtures approach.

## ADR deltas (epic-local)
Proposed ADRs in ./adr/, listed here with one line each. Or "none".

## Tracks
Parallel workstreams; each row must be executable without conflicts with siblings.
| Track | Owns | Packages | Tasks |
|---|---|---|---|
| track-{slug} | {responsibility} | packages/{x} | TASK-{a}, TASK-{b} |

## Open questions
- [ ] OQ-{epic-slug}-design-{topic} (blocking): ...
