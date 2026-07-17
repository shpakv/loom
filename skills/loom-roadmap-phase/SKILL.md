---
name: loom-roadmap-phase
description: Loom phase 2 (command /loom:roadmap) — rolling-wave roadmap: pick the FIRST vertical slice for the walking skeleton, keep other epics as cheap draft candidates in a dependency DAG, generate ROADMAP.md. Use whenever the user runs /loom:roadmap, asks to plan epics, sequence work, or asks "what do we build first". Also used to re-cut the roadmap after consolidation or retro.
---

# Loom: roadmap phase (rolling wave)

Goal: choose the first slice and keep the rest deliberately cheap. Detailed
plans made before the skeleton exist are inventory that rots — sequence over
schedule, one wave at a time. Read `loom-core` conventions first.

## Inputs (gate)

Approved `VISION.md` and use cases (minimum form is fine).

## Procedure

1. List epic candidates from use cases. An epic is a **vertical business
   capability** (noun phrase: `epic-billing-analytics`), never a technical
   layer — `epic-backend` is forbidden. For candidates, cheap frontmatter is
   enough: `id`, `goal`, `criticality`; leave the body one paragraph.
2. **Pick the first slice** — the thinnest capability that forces every
   architectural layer to exist: it feeds /loom:skeleton. Selection criteria:
   maximum architectural learning per unit of appetite, not maximum user value.
3. Only the first-slice epic gets full treatment: complete frontmatter
   (`goal, metric, criticality, appetite, depends_on`), scope with anti-scope,
   definition of done — from `templates/epic.md`. Only it goes to /loom:review.
4. Dependencies (`depends_on`) must be real — data, contract, or learning
   dependencies, not preferences. Parallel-capable epics must NOT depend on
   each other.
5. Run `python3 scripts/loom/roadmap_gen.py` — validates the DAG (cycles,
   broken deps) and generates ROADMAP.md. Never edit ROADMAP.md by hand.

## Rolling wave rules

- **At most ONE approved, not-yet-started epic at any time.** The next epic
  is detailed and approved only when the current one finishes (at retro) or
  at consolidation — with the knowledge just gained.
- Re-cutting candidates (merge, split, re-sequence, park as `wont`) is the
  norm, not an exception; drafts are cheap by design.
- No dates, sprints, or quarters. Sequence and appetite only.

## Exit criteria

- First-slice epic approved; DAG valid; every other candidate is draft.
