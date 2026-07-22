---
name: loom-skeleton-phase
description: Invoked by the /loom:skeleton command to build the walking skeleton — the thinnest end-to-end slice through all layers that validates the proposed architecture and technology decisions by building them, generating the material evidence one-way ADRs cite at consolidation and surfacing where the hypothesis was wrong. Run /loom:skeleton after /loom:technology has proposed the one-way ADRs and before /loom:consolidate.
---

# Loom: skeleton phase

Goal: validate the proposed architecture and technology by BUILDING them, not by
planning. Structure (from /loom:architecture) and technology (from
/loom:technology) enter this phase as hypotheses — draft blocks and proposed
ADRs. The skeleton is the material verification those one-way ADRs cite at
consolidation, and the first honest chance to discover the hypothesis was wrong
while only one slice exists to correct.
Read `loom-core` conventions first (ADR lifecycle especially).

## Inputs (gate)

Approved `GLOSSARY.md`, `VISION.md` (minimum form), `DRIVERS.md`,
`quality-requirements.md`, and the architecture hypothesis (`building-blocks.md`,
`solution-strategy.md`) approved as a hypothesis, with its proposed technology ADRs;
plus exactly one approved first-slice epic. If the structure or the technology
forks are not yet settled as proposals, route back to /loom:architecture or
/loom:technology — the skeleton verifies decisions, it does not originate them.

## What a walking skeleton is (and is not)

The thinnest slice that exercises EVERY layer the real system will have:
entry point → domain logic → persistence → response, plus CI and, if relevant,
a deploy path. One use case, degenerate data, ugly UI — but genuinely
end-to-end and genuinely tested. It validates the architecture and technology
HYPOTHESIS, not features; feature completeness belongs to epics. Build the slice
along the building-block boundaries and on the technologies the proposed ADRs
chose — the point is to make those decisions carry real weight. If a piece of
work does not change what you will learn about the architecture or confirm a
proposed ADR, it is gold-plating — cut it.

## Procedure

1. Take the first-slice epic's primary use case and strip it to its thinnest
   honest path through all layers. Write that path down in the epic's
   `## Definition of done` before coding.
2. Build TDD from the first line (red → green → refactor, commit per phase) —
   the skeleton sets the culture every later task inherits.
3. **Build on the proposed decisions and record what the build demonstrates.**
   The one-way ADRs already exist as proposals from /loom:technology — build the
   slice on the technologies and building-block boundaries they chose, and on
   each proposed ADR note (in its Options or an addendum) what the skeleton
   actually exercised of it: the protocol round-tripped, the datastore held the
   write path, the boundary stayed clean. That note is the material evidence
   consolidation needs to move `verification: skeleton` from promise to fact.
   Keep every ADR `proposed`; acceptance is consolidation's job.
4. **A new fork surfacing here means the technology phase missed one** — that is
   expected, not a failure. Follow the technology-fork protocol from loom-core
   (decision mode BEFORE any recommendation), cite the deciding `DRV-*`/`QS-*`,
   and add a NEW proposed ADR: one-way → `verification: skeleton` (or a
   `/loom:spike` if it needs a head-to-head), two-way → `verification: judgment`,
   one paragraph. Do not accept it here.
5. **The hypothesis may be refuted — say so loudly.** If the slice shows a
   proposed ADR is wrong (the datastore can't meet the QS, the boundary leaks),
   do not quietly build around it: record the refutation on the ADR and raise a
   blocking OQ. Discovering this now, with one slice built, is the whole point.
6. **Every package created gets its SKILL.md at birth** from
   `templates/package-skill.md` — purpose, boundaries, API surface, how to
   test. A package without SKILL.md does not pass this phase.
7. Unknowns you consciously defer go to `ASSUMPTIONS.md` or as OQs on the
   relevant ADR — deferring is fine, silence is not.

## Exit criteria (before /loom:consolidate)

- The slice is demoable end-to-end and CI is green.
- Every proposed one-way ADR is either backed by a note of what the skeleton
  demonstrated (ready to accept) or carries a blocking OQ recording its
  refutation; any fork newly surfaced here has its own proposed ADR.
- Every package has a SKILL.md; `link_check.py docs packages` passes.
- The epic's definition of done is met and the epic is marked done.

## Rules

- One use case only. The second use case is scope creep, not thoroughness.
- Prefer boring choices with escape hatches; the skeleton exists to prove or
  cheaply correct the hypothesis at consolidation, not to be perfect.
- The skeleton verifies decisions; it does not originate the architecture. A
  structural or technology choice invented here that /loom:architecture or
  /loom:technology should have made is a signal those phases were rushed —
  record it, but note it back to keep the earlier documents honest.
