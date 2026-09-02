---
name: loom-consolidate-phase
description: Consolidate evidence from any source: accept, reject or defer proposed ADRs, reconcile architecture and quality scenarios, extract conventions, sweep assumptions and recut the roadmap.
---

# Loom: consolidation event

Goal: reconcile recommendations, evidence and decisions at the moment the
authority is ready to act. This is an event, not an ongoing phase: enter with
proposed ADRs and an architecture hypothesis, leave with accepted, rejected or
deferred outcomes and a reconciled architecture. Evidence may come from any
source and does not need to be stored as code in Loom.
Read `loom-core` conventions first.

## Inputs (gate)

A recorded evidence summary from any source; proposed ADRs carrying their
recommendations and provenance; the
architecture approved as a hypothesis (`quality-requirements.md`,
`building-blocks.md`, `solution-strategy.md`); and `ASSUMPTIONS.md` in any state.
If required evidence is missing, keep the ADR proposed with an explicit risk or
route to an optional evidence method; do not invent a skeleton requirement.

## Procedure

1. **ADR sweep** — for every proposed ADR, via /loom:review (one-way first):
   - accept, reject or defer according to project `decisions` policy and the
     recorded authority; preserve evidence level, confidence and provenance;
   - reject alternatives that lost — with reasons (rejected ADRs are the
     negative constraints future sessions need);
   - weak evidence is not an automatic failure when residual risk is explicit,
     accepted by `risk_accepted_by` and tied to `revisit_when`.
2. **Guessed-driver sweep** — for every DRIVERS.md row with
   `confidence: guessed` that is cited by an accepted ADR
   (`link_check.py --refs DRV-<slug>`), either confirm it (→ `known`, with a
   note of the evidence) or add a matching `revisit_when` trigger to that ADR.
   An accepted one-way decision standing on an unconfirmed guess without a
   trigger is a hard failure of the `adr_scan.py --framing` gate at step 10 — the
   sweep here is how you clear it before running the gate.
3. **Quality scenarios, reconciled with evidence** — `quality-requirements.md`
   already exists from /loom:requirements. Update each `QS-<slug>` with the
   observations that apply, correct it where evidence disagreed, and add any
   scenario the research revealed was missing. An unobserved QS is a declared
   coverage gap, not an automatic block.
4. **Building blocks, as-observed vs as-intended** — reconcile
   `building-blocks.md` (the hypothesis) with the boundaries observed by the
   external experiment. Where they diverge, record the evidence and update the
   architectural document through review.
5. **Solution strategy, closed** — in `solution-strategy.md`, fill the ADR
   column: each QS now maps to the accepted ADR or convention that satisfies it,
   and each "decision still open" fork is resolved. An unmapped QS means a
   missing decision or a decorative NFR — resolve which.
6. **Conventions** — extract durable product and architecture conventions into
   `conventions/*.md`. Enforceable rules point to their gate; the rest are
   marked `advisory`.
7. **Assumption sweep** — every `AS-*` row: promote to ADR, schedule
   `/loom:spike`, or delete with a one-line reason. The event is not done
   while ASSUMPTIONS.md has unswept rows.
8. **Re-cut the roadmap** — with the new knowledge in hand, revisit draft
   epic candidates: merge, split, re-sequence, adjust appetites. Approve only
   the next one epic (rolling wave). Run `roadmap_gen.py`.
9. Gates: `adr_scan.py --gate --framing`, `link_check.py docs`, and
   `oq_scan.py --gate` on each architecture document, then /loom:review them.
   The `--framing` mode is the point of this event: it fails unless every
   accepted one-way ADR is framed by a driver (DRV-*) AND a quality scenario
   (QS-*), declares its policy mode, every QS in the solution strategy maps to
   an accepted ADR or a convention, and weak evidence has explicit risk
   acceptance and revisit conditions. It validates transparency, not a specific
   experiment.

## Exit criteria

- All proposed ADRs have an accepted, rejected or deferred outcome; deferred
  decisions carry an explicit follow-up or blocking OQ.
- ASSUMPTIONS.md is empty.
- Building blocks match the recorded evidence.
- Exactly one approved not-yet-started epic exists; the rest are draft.

## Rules

- Consolidation may conclude the skeleton chose wrong — that is success, not
  failure: supersede cheaply now, while one slice exists instead of ten epics.
- Do not write epic-specific details into architecture documents — they
  belong to that epic's future design doc.
