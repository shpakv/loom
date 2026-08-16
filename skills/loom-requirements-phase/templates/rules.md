---
id: rules
status: draft
owner: human
updated: {date}
---
# Domain rules

Rules the system is OBLIGED to reproduce: formulas, thresholds, rounding,
boundaries, tie-breaks. These are not decisions — they have a source, not
alternatives. A rule that is missing here is a blocking open question, never a
sensible default: a wrong threshold corrupts data silently and is discovered by a
user, not by a test.

Use glossary terms verbatim. One row per rule; `BR-<slug>` IDs are immutable once
referenced.

| ID | Rule | Bounds | Source | review_by |
|---|---|---|---|---|
| BR-{rule-slug} | {the rule, with its numbers} | {rounding and where applied; inclusive/exclusive edges; zero / empty / negative; tie-break; timezone; precedence} | {person + date, or standard §section, edition} | {YYYY-MM-DD for external sources, else empty} |

## Notes on bounds

Fill the bounds column properly — it is where invented arithmetic hides. For each
rule, the questions worth answering before an agent answers them for you:

- rounding mode, and applied to the total or to each component?
- boundaries inclusive or exclusive?
- what happens at zero, on an empty set, on a negative value?
- how are ties broken?
- which timezone, and where does the period start?
- when two rules could both apply, which wins?

## Provenance

- `source` is what separates a rule from a guess. A person plus a date, or a
  document with its section and edition.
- A rule recovered from code during `/loom:harvest` is marked
  `confidence: guessed` in its source cell, with what would confirm it. It stays
  labelled until a human or a measurement settles it.
- `review_by` is only for rules whose source lives outside the project. Standards
  get revised and no `revisit_when` condition can catch that; `/loom:audit` reads
  this date.

## Open questions
- [ ] OQ-rules-{topic} (blocking): ...
