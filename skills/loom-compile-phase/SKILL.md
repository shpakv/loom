---
name: loom-compile-phase
description: Compile Loom's glossary, rules, accepted decisions, anti-goals and conventions into the configured external SDD engine, optionally including an epic's approved task specs. Use after design or consolidation and before the engine implements anything; never write product code.
---

# Loom: compile (handoff to the engine)

Goal: put the knowledge layer where the engine will actually read it. Engines
read their own files — a constitution, steering docs, a spec directory — and no
engine reads `docs/`. Compile is the forward half of the seam; `/loom:harvest` is
the backward half. Read `loom-core` conventions first (the handoff seam
especially).

This phase writes NOTHING under `docs/` and decides nothing. It is a projection:
if the projection and the source disagree, the source wins and the projection is
rebuilt.

## Inputs (gate)

`engine:` configured in `docs/loom.yaml` (at minimum `name` and `constitution`).
For a seed spec: one epic whose `design.md` is `approved`, with approved task
specs. Accepted ADRs, conventions, `GLOSSARY.md`, `RULES.md` and `VISION.md`
anti-goals in whatever state they have reached — compile projects what exists.

If `engine.name` is empty, stop and ask which engine this project uses; do not
guess a layout. Common profiles:

| Engine | `constitution` | `spec_dir` |
|---|---|---|
| Spec Kit | `.specify/memory/constitution.md` | `.specify/specs` |
| Kiro | `.kiro/steering/product.md` | `.kiro/specs` |
| OpenSpec | `openspec/project.md` | `openspec/changes` |
| plain agent harness | `AGENTS.md` or `CLAUDE.md` | `specs/` |

## Procedure

1. **Refuse to hand off a spec that is not ready.** Run
   `python3 scripts/loom/oq_scan.py --gate` on the epic's design doc and task
   files. A blocking open question means the engine would have to invent the
   answer — that is the exact failure the seam exists to prevent. Fix upstream
   and re-run; never compile "most of" a spec.
2. Run `python3 scripts/loom/compile.py [--epic epic-<slug>]`. It assembles the
   constitution (vocabulary → anti-goals → binding rules → decisions in force →
   ruled out → conventions → structural boundaries) and, with `--epic`, that
   epic's seed spec from its approved task specs and contracts.
3. **Read the output before shipping it.** The script is mechanical; two things
   need judgment:
   - **the ADR digest** — it lifts the first sentence of Decision, Context and
     Consequences. Where a decision's binding force does not survive that
     compression, sharpen the ADR's Decision sentence in the source document
     (an accepted ADR's body is immutable, so use an `## Addenda` entry or a
     superseding ADR — never edit the compiled file);
   - **conflicts** — a convention and a rule that contradict each other are
     invisible in `docs/` and glaring once side by side in one file. A conflict
     is a blocking OQ on the weaker document, not something to smooth over in
     the projection.
4. Set `handoff: <engine.name>` in the frontmatter of every task whose spec went
   into the seed. That is what makes the round trip auditable: a task with
   `handoff:` set and `harvested: false` is work whose facts have not come back.
5. Tell the human the one command to run in the engine, and what NOT to expect
   from Loom afterwards: no plan, no tests, no diff review. When the engine is
   done, `/loom:harvest`.

## Exit criteria

- `python3 scripts/loom/compile.py --check` passes (nothing stale or missing).
- Every compiled file opens with the GENERATED marker and is committed — the
  projection is reviewable in the diff, which is how drift gets noticed.
- Every handed-off task carries `handoff:`.

## Rules

- **Never hand-edit a compiled file.** The next compile overwrites it, and the
  edit was a fact that now exists in only one place — the one place nobody reads
  when they ask "why do we do it this way?".
- **Compile is not a review gate.** It does not approve documents, resolve OQs or
  accept ADRs; it refuses to run when those are outstanding and sends you back.
- **Re-compile after any decision event.** `/loom:consolidate` and `/loom:audit`
  change the set of accepted ADRs, which changes the constitution. A constitution
  that lags the ADRs is worse than none: the engine obeys a decision that was
  superseded.
- **Digest, not archive.** The constitution carries decisions, reasons and
  consequences — not options, not the debate, not spike results. An engine needs
  the constraint; the history lives in `docs/adr/` for humans and for challenge.
- Keep rejected decisions in the projection. "Do not propose Kafka again, because
  operational cost dominates at our scale" is one of the cheapest and most
  effective constraints you can hand a model.
