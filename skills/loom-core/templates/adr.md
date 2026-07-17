---
id: ADR-{decision-as-verb-phrase}     # must equal filename; reads as an answer, not a topic
status: proposed                      # proposed | accepted | rejected | deprecated | superseded
reversibility: two-way                # one-way | two-way
verification: judgment                # skeleton | SPIKE-<slug> | benchmark | prototype | reference | judgment
enforced: none                        # fitness | code-tag | none
decision_mode: null                   # decided | framed | menu | delegated — how the human chose to decide
revisit_when: []                      # triggers that invalidate this decision, e.g. "sustained load > 5k rps"
supersedes: []
superseded_by: null
aliases: []
decided: null                         # date of accepted/rejected transition
updated: {date}
---
# ADR: {Decision as a claim, e.g. "Use QuestDB for time-series storage"}

Status: proposed · reversibility: two-way · verification: judgment
<!-- This line mirrors the frontmatter for human readers; adr_scan fails on mismatch. Update BOTH on every status transition. -->

## Context
Problem, forces, constraints. MUST cite the drivers this decision stands on
(DRV-*); also link use cases / QS-* / assumptions (AS-*). If the deciding
fact is not in DRIVERS.md yet — ask the human and record it there first.

## Options
### A. {option} — honest pros and cons, 2–3 each
### B. {option} — evidence: SPIKE-{slug} showed ...
<!-- at least two REAL options; "do it well vs do it badly" is a strawman -->

## Decision
Chosen A, because {the deciding factor — one, not a list}.

## Consequences
- (+) ...
- (−) ...                             # at least one real minus, or this is an ad
- Enforcement: {lint/arch-test rule referencing this ADR id, or "none, because ..."}

## Addenda
<!-- append-only after acceptance; the body above is immutable once accepted -->
