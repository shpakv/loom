---
name: loom-consolidate-phase
description: Consolidate evidence from a skeleton or spike: accept or reject proposed one-way ADRs, reconcile architecture and quality scenarios, extract conventions, sweep assumptions and recut the roadmap.
---

# Loom: consolidation event

Goal: fix expensive-to-change decisions at the moment of maximum knowledge. This
is an event, not an ongoing phase: enter with proposed ADRs and an architecture
hypothesis, leave with accepted ADRs and a reconciled architecture. This phase
does not originate quality scenarios or building blocks; it confirms or
corrects them against recorded evidence.
Read `loom-core` conventions first.

## Inputs (gate)

A recorded skeleton or spike; proposed ADRs carrying its evidence notes; the
architecture approved as a hypothesis (`quality-requirements.md`,
`building-blocks.md`, `solution-strategy.md`); and `ASSUMPTIONS.md` in any state.
If the skeleton is not demoable, this event is premature — go back to
/loom:skeleton.

## Procedure

1. **ADR sweep** — for every proposed ADR, via /loom:review (one-way first):
   - accept with `verification: skeleton` (state in Options what the skeleton
     demonstrated) or `SPIKE-*` where a spike was run;
   - reject alternatives that lost — with reasons (rejected ADRs are the
     negative constraints future sessions need);
   - a one-way ADR the skeleton did NOT actually exercise cannot cite it —
     either run the missing spike or keep it proposed with a blocking OQ.
2. **Guessed-driver sweep** — for every DRIVERS.md row with
   `confidence: guessed` that is cited by an accepted ADR
   (`link_check.py --refs DRV-<slug>`), either confirm it (→ `known`, with a
   note of the evidence) or add a matching `revisit_when` trigger to that ADR.
   An accepted one-way decision standing on an unconfirmed guess without a
   trigger is a hard failure of the `adr_scan.py --framing` gate at step 10 — the
   sweep here is how you clear it before running the gate.
3. **Quality scenarios, confirmed by measurement** — `quality-requirements.md`
   already exists from /loom:requirements. Update each `QS-<slug>` with what the
   skeleton actually measured: confirm the target, correct it where reality
   disagreed, and add any scenario the build revealed was missing. A QS the
   skeleton could not exercise at all is a coverage gap — note how it will be
   proven later.
4. **Building blocks, as-tested vs as-intended** — reconcile
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
8. **Re-cut the roadmap** — with skeleton knowledge in hand, revisit draft
   epic candidates: merge, split, re-sequence, adjust appetites. Approve only
   the next one epic (rolling wave). Run `roadmap_gen.py`.
9. Gates: `adr_scan.py --gate --framing`, `link_check.py docs`, and
   `oq_scan.py --gate` on each architecture document, then /loom:review them.
   The `--framing` mode is the point of this event: it fails unless every
   accepted one-way ADR is framed by a driver (DRV-*) AND a quality scenario
   (QS-*), declares its decision_mode, every QS in the solution strategy maps to
   an accepted ADR or a convention, any `verification: SPIKE-*` claim points at a
   real, approved spike, and no accepted one-way decision rests on a guessed
   driver without a revisit_when trigger. An accepted one-way door with no target,
   no agreed decision mode, missing evidence, or an unconfirmed guess under it
   does not leave this event.

## Exit criteria

- All one-way ADRs are accepted or explicitly parked with a blocking OQ.
- ASSUMPTIONS.md is empty.
- Building blocks match the recorded evidence.
- Exactly one approved not-yet-started epic exists; the rest are draft.

## Rules

- Consolidation may conclude the skeleton chose wrong — that is success, not
  failure: supersede cheaply now, while one slice exists instead of ten epics.
- Do not write epic-specific details into architecture documents — they
  belong to that epic's future design doc.
