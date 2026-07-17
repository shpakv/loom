---
id: DRIVERS
status: draft
owner: pair
updated: {date}
---
# Architecture drivers

FACTS about the world — not choices. Orders of magnitude, not precision:
for a "Postgres vs ClickHouse" fork, knowing 10^2 vs 10^6 rows/s is enough.
Every row has a DRV slug (referenceable from ADR Context) and a confidence:
`known` (stated by the human / measured) or `guessed` (needs verify-by —
a guessed driver is an assumption and follows the same discipline).

## Quality (proto-QS)
| ID | Fact | Confidence | Verify by |
|---|---|---|---|
| DRV-{load-topic} | peak ~{order} rps, {pattern} | guessed | {how} |
| DRV-{latency-topic} | {operation} tolerable at ~{order} | known | — |

## Constraints (mandated facts)
| ID | Fact | Confidence | Verify by |
|---|---|---|---|
| DRV-{constraint} | {budget / deadline / mandated tech / compliance / who operates it} | known | — |

## Integrations
| ID | Fact | Confidence | Verify by |
|---|---|---|---|
| DRV-{system} | {system}, {protocol}, {direction}, {SLA expectations} | known | — |

## Data profile
| ID | Fact | Confidence | Verify by |
|---|---|---|---|
| DRV-{data-topic} | volume ~{order}, growth {rate}, retention {period}, sensitivity {class}, loss tolerance {level} | guessed | {how} |

## Tech posture (about the team, not the system)
| ID | Fact | Confidence | Verify by |
|---|---|---|---|
| DRV-stack-competence | team knows {stack}; unfamiliar: {list} | known | — |
| DRV-tech-vetoes | forbidden/undesired: {list, with reasons} | known | — |
| DRV-novelty-appetite | wants to learn {X} on this project / prefers boring tech | known | — |
| DRV-ops-reality | operated by {who}; on-call {reality}; deploy target {where} | known | — |
| DRV-existing-infra | already paid for / running: {list} | known | — |

## Evolution expectations
| ID | Fact | Confidence | Verify by |
|---|---|---|---|
| DRV-{evolution-topic} | {what will change often} / {what is frozen} | guessed | {how} |

## Open questions
- [ ] OQ-drivers-{topic} (blocking): ...
