---
name: loom-skeleton-phase
description: Loom phase 3 (command /loom:skeleton) — build the walking skeleton: the thinnest end-to-end slice through all layers that validates the architecture, accumulating proposed ADRs as a by-product of building. Use whenever the user runs /loom:skeleton, asks to start the walking skeleton, bootstrap the codebase, or build the first end-to-end slice.
---

# Loom: skeleton phase

Goal: validate the architecture by building, not by planning. The skeleton is
the material verification that one-way ADRs will cite at consolidation.
Read `loom-core` conventions first (ADR lifecycle especially).

## Inputs (gate)

Approved `GLOSSARY.md`, `VISION.md` (minimum form), `DRIVERS.md`, and exactly one approved
first-slice epic. If missing, route to /loom:imagine or /loom:roadmap.

## What a walking skeleton is (and is not)

The thinnest slice that exercises EVERY layer the real system will have:
entry point → domain logic → persistence → response, plus CI and, if relevant,
a deploy path. One use case, degenerate data, ugly UI — but genuinely
end-to-end and genuinely tested. It validates architecture, not features;
feature completeness belongs to epics. If a piece of work does not change
what you will learn about the architecture, it is gold-plating — cut it.

## Procedure

1. Take the first-slice epic's primary use case and strip it to its thinnest
   honest path through all layers. Write that path down in the epic's
   `## Definition of done` before coding.
2. Build TDD from the first line (red → green → refactor, commit per phase) —
   the skeleton sets the culture every later task inherits.
3. **Decisions are captured in the moment, not reconstructed later.** Every
   time you hit a fork, follow the technology-fork protocol from loom-core
   (decision mode BEFORE any recommendation) and FIRST consult `DRIVERS.md`
   for the deciding facts —
   the ADR Context must cite them (DRV-*). If the fact is missing: one-way
   door → STOP and ask the human (blocking OQ), record the answer as a driver,
   then decide; two-way door → record your guess as `confidence: guessed`
   first, then proceed. Then:
   - one-way door (language, persistence, protocol, monorepo tooling) →
     create a proposed ADR NOW, with `verification: skeleton` and a note of
     what the skeleton will demonstrate; keep building on the chosen branch;
   - a fork needing comparison → `/loom:spike` (time-boxed), then the ADR;
   - two-way door → proposed ADR with `verification: judgment`, one paragraph,
     move on.
   Never set any one-way ADR to `accepted` during this phase — acceptance is
   consolidation's job, after the skeleton has proven itself.
4. **Every package created gets its SKILL.md at birth** from
   `templates/package-skill.md` — purpose, boundaries, API surface, how to
   test. A package without SKILL.md does not pass this phase.
5. Unknowns you consciously defer go to `ASSUMPTIONS.md` or as OQs on the
   relevant ADR — deferring is fine, silence is not.

## Exit criteria (before /loom:consolidate)

- The slice is demoable end-to-end and CI is green.
- Every one-way question encountered has a proposed ADR or a blocking OQ.
- Every package has a SKILL.md; `link_check.py docs packages` passes.
- The epic's definition of done is met and the epic is marked done.

## Rules

- One use case only. The second use case is scope creep, not thoroughness.
- Prefer boring choices with escape hatches; the skeleton exists to be
  corrected cheaply at consolidation, not to be perfect.
