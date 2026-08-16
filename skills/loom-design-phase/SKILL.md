---
name: loom-design-phase
description: Invoked by the /loom:design command to decompose one approved epic into a design doc, contracts, parallel conflict-free tracks, and session-sized task specs ready for handoff. Run /loom:design on an approved epic, before /loom:compile hands its tasks to the SDD engine.
---

# Loom: design phase (per epic)

Goal: turn one approved epic into task specs so self-sufficient that the SDD
engine implementing them needs no clarifying questions. This is the last phase
that produces per-task artifacts — the plan, the tests and the code are the
engine's, and `/loom:compile` is the handoff. Read `loom-core` conventions first
(the handoff seam especially).

## Inputs (gate)

The one approved epic (rolling wave), consolidated architecture (accepted ADRs,
building-blocks, conventions), package SKILL.md of packages likely touched.

## Procedure

1. Create `epics/epic-<slug>/design.md` from `templates/design-doc.md`:
   scope recap, domain changes (glossary deltas go to GLOSSARY first),
   contracts, data changes, test strategy, epic-local ADR deltas.
2. **Contracts before tasks.** API/event contracts (OpenAPI/AsyncAPI YAML,
   .proto) are written and reviewed first — they are the source of truth that
   parallel tracks build against, and the main thing that makes tracks
   conflict-free.
3. **Tracks** — sections of design.md, not separate files. A track
   (`track-<slug>` in the tracks table) is a workstream that can proceed in
   parallel with its siblings: two tracks must be executable by two agents
   without merge conflicts or mid-sprint blocking. Tracks usually align with
   package boundaries. If two tracks keep touching the same files, they are
   one track.
4. **Tasks** — `tasks/TASK-<pkg-change>.md` from `templates/task.md`. Sizing
   rule: one task = one context window = one session = one PR. The spec plus
   the package SKILL.md plus the relevant design.md excerpt must fit in
   context with room to spare. If a task cannot be specified without "and
   then figure out...", it is underdesigned — split or return to the track.
5. **`## Spec` is the whole task file.** Behavior, acceptance with numbers,
   contracts touched, out of scope — and nothing about HOW. No file names, no
   function names, no step order: those are the engine's decisions, made against
   the code as it will be then, and pinning them here is how a spec starts lying
   before it is read. A spec that cannot be written without naming internals is
   usually a missing contract.
6. Assign `rigor` per task: `full` when it touches public contracts, domain
   invariants, or more than one package; `light` otherwise. This is an
   **advisory signal** about the cost of being wrong — the engine decides what
   ceremony it applies to it (see `docs/recipes/anti-cheating-tdd.md` for the
   ceremony Loom used to apply itself).
7. Task `depends_on` forms a DAG within the epic; cross-track dependencies
   are a design smell — restructure tracks before accepting one.
8. Gates: `oq_scan --gate` on design.md, `link_check.py docs packages`,
   then /loom:review on design.md.
9. Hand off with `/loom:compile` on the epic. Do not start work in the engine
   from a `draft` design doc — compile refuses a spec with open blocking OQs,
   which is the point.

## Exit criteria (before /loom:compile)

- Contracts reviewed; task DAG valid; every task names its packages and rigor.
- Every task is **engine-ready**: acceptance criteria are checkable and carry
  numbers where numbers exist, contracts touched are named, out of scope is
  filled, and no internal file or step order is prescribed.
