---
name: loom-design-phase
description: Invoked by the /loom:design command to decompose one approved epic into a design doc, contracts, parallel conflict-free tracks, and session-sized task files with rigor levels. Run /loom:design on an approved epic to prepare its work for /loom:implement.
---

# Loom: design phase (per epic)

Goal: turn one approved epic into tasks so self-sufficient that /loom:implement
needs no clarifying questions. Read `loom-core` conventions first.

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
5. Only the `## Spec` section is written here. `## Plan` is deliberately left
   empty — it is produced just-in-time by the planner inside /loom:implement,
   against the code as it will be then.
6. Assign `rigor` per task: `full` when it touches public contracts, domain
   invariants, or more than one package; `light` otherwise.
7. Task `depends_on` forms a DAG within the epic; cross-track dependencies
   are a design smell — restructure tracks before accepting one.
8. Gates: `oq_scan --gate` on design.md, `link_check.py docs packages`,
   then /loom:review on design.md before any implementation starts.

## Exit criteria

- Contracts reviewed; every task self-contained with acceptance criteria;
  task DAG valid; every task names its packages and rigor.
