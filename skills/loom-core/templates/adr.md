---
id: ADR-{decision-as-verb-phrase}     # must equal filename; reads as an answer, not a topic
status: proposed                      # proposed | accepted | rejected | deprecated | superseded
reversibility: two-way                # one-way | two-way
decision_mode: recommend              # delegated | recommend | confirm | record-only
evidence_level: reasoned              # none | reasoned | reported | observed | measured
confidence: medium                    # low | medium | high
evidence_refs: []                     # IDs or external URIs; details live in ## Evidence
authority: null                       # side authorized to accept/reject this ADR
risk_accepted_by: null                # required when weak evidence is accepted
enforced: none                        # fitness | code-tag | none
revisit_when: []                      # triggers that invalidate this decision, e.g. "sustained load > 5k rps"
supersedes: []
superseded_by: null
aliases: []
decided: null                         # date of accepted/rejected transition
updated: {date}
---
# ADR: {Decision as a claim, e.g. "Use QuestDB for time-series storage"}

Status: proposed · reversibility: two-way · evidence: reasoned · confidence: medium
<!-- This line mirrors the frontmatter for human readers; adr_scan fails on mismatch. Update BOTH on every status transition. -->

## Context
Problem, forces, constraints. MUST cite the drivers this decision stands on
(DRV-*); also link use cases / QS-* / assumptions (AS-*). If the deciding
fact is not in DRIVERS.md yet — ask the human and record it there first.

## Recommendation
{The agent's recommendation, with the reason it is preferred. This is not the
decision; authority may accept, reject or defer it.}

## Evidence
{Question, method, observations, interpretation, limitations and provenance.
External evidence is allowed; do not copy its code or infrastructure into Loom.}

## Options
### A. {option} — honest pros and cons, 2–3 each
### B. {option} — evidence: SPIKE-{slug} showed ...
<!-- at least two REAL options; "do it well vs do it badly" is a strawman -->

## Decision
{Accepted, rejected or deferred outcome, recorded only when authority decides.}

## Consequences
- (+) ...
- (−) ...                             # at least one real minus, or this is an ad
- Enforcement: {lint/arch-test rule referencing this ADR id, or "none, because ..."}

## Addenda
<!-- append-only after acceptance; the body above is immutable once accepted -->
