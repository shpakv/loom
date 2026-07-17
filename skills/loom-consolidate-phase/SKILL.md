---
name: loom-consolidate-phase
description: Loom phase 4 (command /loom:consolidate) — the decision event after the walking skeleton: accept one-way ADRs using the skeleton as material verification, write quality scenarios, as-built building blocks, solution strategy and golden-path conventions, sweep assumptions, re-cut the roadmap. Use whenever the user runs /loom:consolidate, says the skeleton is done, or asks to lock in the architecture.
---

# Loom: consolidation event

Goal: fix the expensive-to-change decisions NOW — at the moment of maximum
knowledge, with a working skeleton as evidence. This is an event, not an
ongoing phase: enter with proposed ADRs, leave with accepted ones.
Read `loom-core` conventions first.

## Inputs (gate)

A demoable walking skeleton (CI green), its proposed ADRs, and
`ASSUMPTIONS.md` in any state. If the skeleton is not demoable, this event
is premature — go back to /loom:skeleton.

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
   trigger is a gate failure of this event.
3. **Quality scenarios** — `architecture/quality-requirements.md` from
   `templates/quality-requirements.md`. Promote the quality-lite rows of
   DRIVERS.md into full QS (stimulus → response → measure); add what VISION
   metrics, the first epics, and the skeleton's measurements demand. Each `QS-<slug>` is testable
   (stimulus → response → measure) and names its enforcement.
4. **Building blocks, as-built** — `architecture/building-blocks.md` from
   `templates/building-blocks.md`: document the package structure the skeleton
   actually has (not the intended one), C4 L2, forbidden dependencies. Every
   block must already have its package SKILL.md from the skeleton phase.
5. **Solution strategy** — `templates/solution-strategy.md`: QS → ADR matrix.
   An unmapped QS means a missing decision or a decorative NFR — resolve which.
6. **Conventions** — extract the golden path the skeleton converged on
   (error handling, logging, test layout, package structure) into
   `conventions/*.md`. Enforceable rules point to their lint/arch-test;
   the rest are marked `advisory`.
7. **Assumption sweep** — every `AS-*` row: promote to ADR, schedule
   `/loom:spike`, or delete with a one-line reason. The event is not done
   while ASSUMPTIONS.md has unswept rows.
8. **Re-cut the roadmap** — with skeleton knowledge in hand, revisit draft
   epic candidates: merge, split, re-sequence, adjust appetites. Approve only
   the next one epic (rolling wave). Run `roadmap_gen.py`.
9. Gates: `adr_scan.py --gate`, `link_check.py docs packages`,
   `oq_scan.py --gate` on each architecture document, then /loom:review them.

## Exit criteria

- All one-way ADRs are accepted or explicitly parked with a blocking OQ.
- ASSUMPTIONS.md is empty.
- Building blocks match reality (`as-built`), every block has a SKILL.md.
- Exactly one approved not-yet-started epic exists; the rest are draft.

## Rules

- Consolidation may conclude the skeleton chose wrong — that is success, not
  failure: supersede cheaply now, while one slice exists instead of ten epics.
- Do not write epic-specific details into architecture documents — they
  belong to that epic's future design doc.
