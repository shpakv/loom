---
name: loom-review-gate
description: Loom gate utility — review any Loom document, resolve its open questions, check consistency against glossary/ADRs, and manage status transitions (draft → in-review → approved for documents, proposed → accepted/rejected for ADRs). Use whenever the user runs /loom:review, asks to review/approve a doc or ADR, resolve open questions, or asks whether a document is ready for the next phase.
---

# Loom: review gate

Applies to ANY Loom document. Read `loom-core` conventions first.
Prefer running the review in the `loom-reviewer` subagent (fresh context) when
the current session authored the document — the author inherits its blind spots.

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
- **One-way only, mandatory**: dispatch `loom-challenger` BEFORE acceptance;
  materialize its findings as OQs and resolve them first. No challenge pass —
  no accept.
- On acceptance: set `status: accepted` in the frontmatter AND in the body
  `Status:` line, fill `decided:`, then treat the body as immutable (addenda
  only). Run `python3 scripts/loom/adr_scan.py --gate`.

## Rules

- Never resolve a blocking OQ or accept an ADR without an explicit human decision.
- Never edit document substance during review except as OQ materialization.
- Review output ends with a verdict line: `APPROVED` / `ACCEPTED` or
  `BLOCKED (reasons)`.
