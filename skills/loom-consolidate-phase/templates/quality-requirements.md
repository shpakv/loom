---
id: quality-requirements
status: draft
owner: pair
updated: {date}
---
# Quality requirements (scenarios)

Testable NFRs. Each row is a scenario: concrete stimulus, expected response,
hard measure. `Enforced by` names a fitness function or `manual (<why>)`.

| ID | Stimulus | Response | Measure | Traces to | Enforced by |
|---|---|---|---|---|---|
| QS-{slug} | {load/failure/change event} | {expected behavior} | {number + unit} | {VISION metric / epic} | {arch-test, CI job, or manual (<why>)} |

## Open questions
- [ ] OQ-quality-{topic}: ...
