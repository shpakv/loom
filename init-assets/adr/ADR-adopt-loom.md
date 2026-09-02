---
id: ADR-adopt-loom
status: accepted
reversibility: two-way
verification: judgment
enforced: none
revisit_when:
  - the doc-maintenance overhead visibly exceeds its value for the team
supersedes: []
superseded_by: null
aliases: [ADR-0000]
decided: 2026-07-06
updated: 2026-07-06
---
# ADR: Adopt the Loom docs-first workflow

Status: accepted · reversibility: two-way · verification: judgment

## Context
AI-assisted development degrades without persistent, structured context: agents
re-derive intent, drift from decisions, and produce inconsistent terminology.

## Options
### A. Loom (docs-first, slug IDs, gated phases)
(+) every session starts from the same written context; decisions survive people
(−) documentation upkeep becomes part of definition-of-done
### B. Ad-hoc CLAUDE.md + conventions only
(+) zero process overhead  (−) no decision history, no gates, terminology drift

## Decision
Chosen A: the cost of context loss across agent sessions exceeds the upkeep cost.

## Consequences
- (+) /loom:prime gives deterministic context bootstrap.
- (−) Every artifact edit carries frontmatter/status discipline.
- Enforcement: none (process-level decision).

## Addenda
