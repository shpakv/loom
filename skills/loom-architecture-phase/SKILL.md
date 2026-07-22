---
name: loom-architecture-phase
description: Invoked by the /loom:architecture command to design the logical solution structure as a hypothesis before any technology commitment — building blocks (C4 L2 — responsibilities, allowed and forbidden dependencies) and a solution-strategy skeleton mapping each quality scenario to the structural approach and the technology fork that will satisfy it. Produces draft documents the walking skeleton later validates, not accepted architecture; chooses no technologies. Run /loom:architecture after quality requirements are approved and before /loom:technology.
---

# Loom: architecture phase (structure as hypothesis)

Goal: decide the SHAPE of the system — what the parts are, what each owns, and how
they may and may not talk — driven by the quality scenarios, and BEFORE any
technology is picked. Structure is more durable than technology: the same building
blocks can be realised in several stacks, so settling structure first keeps the
technology forks small and local instead of sprawling.
Read `loom-core` conventions first.

This phase sits between /loom:requirements and /loom:technology. Its output is a
HYPOTHESIS: `draft` documents that the walking skeleton will later confirm or
refute. Nothing here is `approved`-as-truth — approving it means "this is a
coherent plan worth testing", not "this is how it is". That distinction is what
keeps this phase from becoming big-design-up-front: you are drawing the map you
will walk, knowing the walk may redraw it.

## Inputs (gate)

Approved `quality-requirements.md` (the QS this structure must satisfy), approved
`VISION.md`, and the first-slice epic. If quality requirements are still draft,
route to /loom:requirements — designing structure without measurable targets is
guessing.

## Procedure

1. **Derive blocks from responsibilities, not layers.** In
   `architecture/building-blocks.md` (from `templates/building-blocks.md`), name
   each building block by what it OWNS in glossary terms — a business capability
   or a bounded responsibility, never a technical tier. `billing`, `ingest`,
   `identity` are blocks; `backend`, `database-layer`, `utils` are not.
2. **Draw the dependency graph.** The mermaid graph and the table's edges say who
   may call/import whom. Then write the **forbidden dependencies** explicitly —
   the negative edges are the ones worth enforcing later as arch-tests. A block
   diagram with no forbidden edges has not made any real decision.
3. **Map every quality scenario to a structural approach** in
   `architecture/solution-strategy.md` (from `templates/solution-strategy.md`):
   which block or tactic carries each QS, and — crucially — which rows still hide
   a **technology fork** to be resolved in /loom:technology. Leave the ADR column
   empty; ADRs do not exist yet. An unmapped QS means either a missing block or a
   decorative NFR — resolve which.
4. **Do NOT choose technologies here.** When a fork surfaces (which datastore,
   which transport, which language), record it as a row in the solution strategy's
   "decision still open" column and move on. Naming a product here anchors the
   later decision and is the exact failure /loom:technology's protocol exists to
   prevent.
5. **Mark structural assumptions.** Anything you are asserting about the structure
   that the skeleton has not yet proven (a boundary will hold, a block can stay
   stateless, an async seam is viable) goes to `ASSUMPTIONS.md` or as an OQ — so
   consolidation knows what to check as-built.
6. Gates: `oq_scan.py --gate` on each document, `link_check.py docs`, then
   /loom:review both to `approved` (meaning: coherent hypothesis, ready to test).

## Exit criteria (before /loom:technology)

- Building blocks named by responsibility, with an explicit allowed/forbidden
  dependency graph; every block will own a package SKILL.md once the skeleton
  creates it.
- Every quality scenario maps to a structural approach; each remaining technology
  fork is captured as an open decision, not resolved.
- Structural assumptions recorded; documents `approved` as a hypothesis.

## Rules

- **Structure before technology, hypothesis before truth.** These documents are
  `draft`/`approved-as-hypothesis`; the skeleton is what turns a hypothesis into a
  verified fact, and /loom:consolidate reconciles this intended structure with the
  as-built one.
- **No product names.** The first datastore, framework, or language name written
  in this phase is a leak from /loom:technology — pull it back into a fork.
- Keep it system-wide and thin. Epic-internal structure belongs to that epic's
  design doc, not here.
