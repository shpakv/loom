---
name: loom-harvest-method
description: Invoked by the /loom:harvest command to close the seam after an external SDD engine implemented a task or a skeleton — read the diff and the engine's own artifacts with a fresh-context agent, and materialize the facts it decided on its own as glossary terms, rules, drivers, proposed ADRs, package surface updates, or blocking open questions. Run /loom:harvest once the engine's work has landed, before handing it the next task.
---

# Loom: harvest (the backward half of the seam)

Goal: recover the facts the engine decided by itself, before they are forgotten.
`/loom:compile` pushes knowledge out; harvest pulls it back. Skipping it is the
one way to kill Loom while every other mechanism still works: the engine
inevitably settles thresholds, names and boundaries the documents never stated,
and two epics later the knowledge layer describes a project that no longer
exists. Read `loom-core` conventions first (the handoff seam especially).

Harvest does not review code quality. Whether the implementation is elegant,
fast, or well-tested is the engine's business. Harvest asks only what the code
now knows that the documents do not.

## Inputs (gate)

A landed unit of engine work — a task with `handoff:` set (or a skeleton slice)
whose diff is available — plus the documents it was compiled from. If the work
has not landed, harvest is premature. If `handoff:` is empty, this work never
went through the seam: harvest it anyway, then fix why it bypassed /loom:compile.

## Procedure

1. **Establish the diff.** Get the commit range or PR the engine produced, plus
   any artifacts it authored for itself (its spec, plan, or task files) — those
   record its reasoning, which is often where a decision is stated most plainly.
2. **Dispatch `loom-harvester`** (fresh context) with the diff, the task
   `## Spec`, the design doc, GLOSSARY/RULES/DRIVERS, accepted ADRs, conventions,
   and the SKILL.md of touched packages. Do not read the diff yourself first: your
   context is contaminated by having compiled the spec, and you will normalize
   exactly the deviations worth catching.
3. **Route every finding by class.** This is the whole of the phase — findings are
   worthless until they land in the one place their class belongs:

| Class | Materialize as | Where |
|---|---|---|
| term (new) | glossary entry, then the term used verbatim from now on | `GLOSSARY.md` |
| term (existing, new sense) | **blocking OQ** — a word with two meanings is the drift Loom exists to stop | on the glossary + the owning doc |
| rule or number | `BR-<slug>` row: rule + bounds + source. Source is "the engine chose it" → `confidence: guessed` with a verify-by, never presented as settled | `RULES.md` |
| measured fact about the world | `DRV-<slug>` row with its measurement | `DRIVERS.md` |
| decision, two-way | one-paragraph ADR, `status: proposed` | `docs/adr/` or the epic's `adr/` |
| decision, one-way | ADR `proposed` **plus** a blocking OQ: a one-way door was walked through without a human. Challenge before accepting | `docs/adr/` |
| surface | update the package's Public API / Boundaries sections | package `SKILL.md` |
| contradiction | blocking OQ on the **document**, quoting both sides | the owning document |
| scope (extra behavior) | blocking OQ on the task or design doc | owning doc |
| implementation detail | nothing. Discard it | — |

4. **Never resolve a contradiction by editing the document to match the code.**
   The document may be right and the code the defect. Materialize it as a
   blocking OQ, name both sides, and let the human decide; then route the
   resolution through the phase that owns it (`/loom:design` for a spec defect, a
   superseding ADR via `/loom:consolidate`, `/loom:review` for an upstream doc).
   Silently retro-fitting docs to code turns the knowledge layer into a
   changelog — a record of what happened, with no authority over what happens.
5. **Escalate anything bigger than an edit through `/loom:intake`.** A harvested
   finding that reshapes an epic, a quality target, or the vision is routed, not
   absorbed here. Intake takes harvested items as one of its two callers.
6. **Close the loop.** Set `harvested: true` on the task, record `landed:` (PR or
   commit), and re-run `/loom:compile` if the harvest changed anything the
   constitution projects — new rule, new accepted decision, new convention. A
   harvest that changed the docs and did not recompile leaves the engine working
   from the previous truth.
7. Gates: `oq_scan.py --gate` on the documents you touched (blocking OQs raised
   here are expected to be open — the gate tells you what must be resolved before
   the next handoff, not that harvest failed), `link_check.py docs packages`,
   `adr_scan.py --gate` if you added ADRs, and `compile.py --check`.

## Exit criteria

- Every harvester finding is either materialized, routed to intake, or explicitly
  discarded as implementation detail (say which — a silent drop is indistinguishable
  from an oversight).
- The task carries `harvested: true` and `landed:`.
- Every number and term the code relies on now exists in a document, or has a
  blocking OQ against it.

## Rules

- **Harvest is not code review.** Style, structure, performance and test quality
  belong to the engine. The moment you start improving the code you have taken
  back the responsibility Loom just gave away.
- **One task per harvest.** Batching a whole epic's diffs guarantees the small
  findings — the undocumented rounding rule — get lost behind the big ones.
- **Harvest before the next handoff, always.** Compiling task N+1 from a
  knowledge layer that has not absorbed task N ships the engine a spec that
  contradicts the code it is about to touch.
- **A guessed fact is labelled, not laundered.** A number recovered from code has
  the authority of "someone's plausible default" until a human or a measurement
  confirms it: `confidence: guessed`, with what would confirm it.
- **Nothing found is a result worth recording.** Two or three consecutive clean
  harvests on an epic is the signal from `CONCEPT.md` §9 that the documentation is
  complete enough to let that epic run with less supervision.
