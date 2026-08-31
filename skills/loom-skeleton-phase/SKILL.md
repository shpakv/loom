---
name: loom-skeleton-phase
description: Specify and interpret the walking skeleton: the thinnest end-to-end slice through all layers, built by the external SDD engine from a Loom brief. Use after technology proposals and before consolidation; the result provides evidence for one-way ADRs.
---

# Loom: skeleton phase

Goal: validate the proposed architecture and technology by BUILDING them, not by
planning. Structure (from /loom:architecture) and technology (from
/loom:technology) enter this phase as hypotheses — draft blocks and proposed
ADRs. The skeleton is the material verification those one-way ADRs cite at
consolidation, and the first honest chance to discover the hypothesis was wrong
while only one slice exists to correct.

**Loom does not build it.** This phase writes the brief that makes the slice a
falsification test rather than a demo, hands it to the SDD engine, and then reads
the result back onto the ADRs. Read `loom-core` conventions first (ADR lifecycle
and the handoff seam especially).

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
HYPOTHESIS, not features; feature completeness belongs to epics. The slice must
run along the building-block boundaries and on the technologies the proposed ADRs
chose — the point is to make those decisions carry real weight. If a piece of
work does not change what you will learn about the architecture or confirm a
proposed ADR, it is gold-plating — cut it from the brief.

## Procedure

### Specify (before the engine starts)

1. Take the first-slice epic's primary use case and strip it to its thinnest
   honest path through all layers. Write that path down in the epic's
   `## Definition of done`.
2. **Write the brief** — `skeleton-brief.md` in the epic directory, from
   `templates/skeleton-brief.md`. Its load-bearing sections are not "what to
   build" but:
   - **the question per proposed ADR** — what this slice must demonstrate for each
     one to be acceptable, phrased so a result could refute it;
   - **layers that must be traversed** — a slice that stops short of persistence
     or deploy proves nothing about the decisions that live there;
   - **`Faked:`** — what may be stubbed, hardcoded or skipped. Without this list,
     "it was slow" is indistinguishable from an artifact of a fake, and every
     later reading of the evidence is contaminated;
   - **falsification criterion** — the observation that would mean a proposed ADR
     is wrong. An unfalsifiable brief produces a demo, not evidence.
3. **Give every package its SKILL.md at birth**, from
   `templates/package-skill.md` — purpose, boundaries, API surface, how to test.
   These are written BEFORE the build, not after it: they are the engine's
   constraint, not a record of what it happened to do. A package without a
   SKILL.md does not pass this phase.
4. Hand off with `/loom:compile` on the first-slice epic. The brief and the
   proposed ADRs travel as part of the projection; the engine owns the plan, the
   tests and the code.

### Interpret (once the slice runs)

5. **Read the result onto each proposed ADR** via `/loom:harvest` on the slice.
   For every proposed ADR, note (in its Options section or an addendum) what the
   skeleton actually exercised of it: the protocol round-tripped, the datastore
   held the write path, the boundary stayed clean. That note is the material
   evidence consolidation needs to move `verification: skeleton` from promise to
   fact. Keep every ADR `proposed` — acceptance is consolidation's job.
6. **A new fork surfacing here means the technology phase missed one** — that is
   expected, not a failure. Follow the technology-fork protocol from loom-core
   (decision mode BEFORE any recommendation), cite the deciding `DRV-*`/`QS-*`,
   and add a NEW proposed ADR: one-way → `verification: skeleton` (or a
   `/loom:spike` if it needs a head-to-head), two-way → `verification: judgment`,
   one paragraph. Do not accept it here.
7. **The hypothesis may be refuted — say so loudly.** If the slice shows a
   proposed ADR is wrong (the datastore can't meet the QS, the boundary leaks),
   do not quietly let the engine build around it: record the refutation on the ADR
   and raise a blocking OQ. Discovering this now, with one slice built, is the
   whole point of the phase.
8. **Check the evidence against `Faked:`** before believing it. A measurement
   taken through a stub measures the stub. Where a fake stands between the slice
   and the question, the ADR is not verified — say so and either extend the brief
   or route the question to `/loom:spike`.
9. Unknowns you consciously defer go to `ASSUMPTIONS.md` or as OQs on the
   relevant ADR — deferring is fine, silence is not.

## Exit criteria (before /loom:consolidate)

- The slice is demoable end-to-end and its CI is green (a fact the engine
  reports; Loom does not run it).
- Every proposed one-way ADR is either backed by a note of what the skeleton
  demonstrated — through no fake — or carries a blocking OQ recording its
  refutation; any fork newly surfaced here has its own proposed ADR.
- Every package has a SKILL.md; `link_check.py docs packages` passes.
- The slice has been harvested: terms, numbers and decisions the engine settled
  on its own are in the documents, not only in the code.
- The epic's definition of done is met and the epic is marked done.

## Rules

- One use case only. The second use case is scope creep, not thoroughness.
- Prefer boring choices with escape hatches; the skeleton exists to prove or
  cheaply correct the hypothesis at consolidation, not to be perfect.
- The skeleton verifies decisions; it does not originate the architecture. A
  structural or technology choice invented here that /loom:architecture or
  /loom:technology should have made is a signal those phases were rushed —
  record it, but note it back to keep the earlier documents honest.
- **The brief is the deliverable, not the code.** If you find yourself writing
  the slice, the brief was too vague to hand over — fix the brief.
