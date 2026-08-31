---
name: loom-review-gate
description: Review a Loom-managed document or ADR, resolve or surface open questions, check consistency with the knowledge layer and recommend a valid lifecycle transition. Use for Loom documents only, not source-code diffs or GitHub pull requests.
---

# Loom: review gate

Applies to ANY Loom document. Read `loom-core` conventions first.
Prefer running the review in the `loom-reviewer` subagent (fresh context) when
the current session authored the document — the author inherits its blind spots.

## Pre-flight (before spending any human review time)

Mechanics a script can catch should never consume a review turn. Before reading
the document for substance, run `python3 scripts/loom/link_check.py` on it — if
any slug reference is broken or an ID is duplicated, STOP and report that: the
document is not review-ready, and fixing a dangling `ADR-…`/`QS-…` reference is
authoring work, not a review decision. Return the document to its author with the
failing references rather than reviewing around them. Only once links resolve does
the substantive review below begin.

## Procedure (regular documents)

1. Run `python3 scripts/loom/oq_scan.py <file>` to list open questions.
2. Set the document `status: in-review` (if it was draft).
3. Iterate OQs one at a time, blocking first. For each: present the question,
   the relevant doc excerpt, and 2–3 answer options with trade-offs. The human
   decides; the agent materializes.
4. Materialize every resolution: an ADR (global `docs/adr/` for cross-cutting,
   epic-local `epics/epic-<slug>/adr/` for scoped), a concrete section edit, or
   an explicit `wontfix (<reason>)`. Update the OQ line:
   `- [x] ... → resolved: <ref>`.
5. Consistency pass — check the document against:
   - GLOSSARY.md: every domain term defined; no synonyms for defined terms.
   - Accepted ADRs: no contradiction; an intentional contradiction needs a
     superseding ADR, not silence.
   - Upstream doc of its phase (design vs epic, epic vs vision).
   Report findings as new OQs if non-trivial.
6. Gates: `python3 scripts/loom/oq_scan.py --gate <file>` and
   `python3 scripts/loom/link_check.py`. If clean, set `status: approved`,
   bump `updated`, run `scripts/loom/index_gen.py`.

## Additional checklist for ADRs (proposed → accepted)

- At least two REAL options with honest trade-offs (no strawmen).
- At least one genuine negative consequence of the chosen option.
- Verification matches reversibility: `one-way` decisions require material
  evidence (skeleton, SPIKE-*, benchmark, prototype, justified reference) — `judgment`
  is only acceptable for `two-way`.
- `revisit_when` is non-empty, or its emptiness is explicitly justified.
- Enforceable consequences have an enforcement plan (`enforced: fitness|code-tag`).
- No contradiction with accepted ADRs; if superseding, both link fields are set.
- Name reads as an answer (verb phrase), not a topic.
- `decision_mode` is filled and truthful (see loom-core fork protocol).
- On acceptance: set `status: accepted` in the frontmatter AND in the body
  `Status:` line, fill `decided:`, then treat the body as immutable (addenda
  only). Run `python3 scripts/loom/adr_scan.py --gate`.

## Challenge triggers (when a fresh-context skeptic is mandatory)

A challenge is not optional politeness — it is required BEFORE approval whenever
the cost of being wrong is high and the author's context is the liability. The
`loom-challenger` agent runs in fresh context precisely because the author
inherits their own blind spots. Dispatch it and resolve its findings as OQs first
— no challenge pass, no approval — in these cases:

- **any one-way ADR** (expensive to undo — the original mandatory case);
- **an epic with `criticality: must`** — a load-bearing capability whose framing,
  if wrong, cascades into every task under it;
- **a design doc that introduces a new external contract** (a public API, an
  event schema, a cross-package protocol) — contracts are the hardest thing to
  change once consumers exist.

For everything else the challenger is available on demand via /loom:challenge but
not gated. When in doubt on a two-way decision, prefer shipping and revisiting
over a ceremonial challenge — reserve the mandatory pass for the doors that don't
reopen cheaply.

## Rules

- Never resolve a blocking OQ or accept an ADR without an explicit human decision.
- Never edit document substance during review except as OQ materialization.
- Review output ends with a verdict line: `APPROVED` / `ACCEPTED` or
  `BLOCKED (reasons)`.
