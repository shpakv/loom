---
name: loom-imagine-phase
description: Invoked by the /loom:imagine command to extract the minimum shared understanding before first code — glossary, anti-goals, 3–5 use cases, assumptions — via socratic interview and throwaway prototypes. Run /loom:imagine to start a new product or greenfield idea; not meant to auto-trigger on free-text idea prompts (routing existing-project work is /loom:intake's job).
---

# Loom: imagine phase (minimum)

Goal: the smallest set of written agreements that must exist before the first
code — everything else is learned cheaper by building (skeleton, prototypes).
Read `loom-core` conventions first.

## Interview protocol

1. Ask exactly ONE question per turn. Never bundle questions.
2. Question ladder (adapt, don't recite): who has the problem and how do they
   cope today → what changes when this exists → what is explicitly OUT of
   scope (push until you get at least 3 anti-goals) → the 3 scenarios that,
   if they work, the project succeeds.
3. New domain words go to GLOSSARY.md immediately, in the user's own words.
   Before writing a new Given/When/Then, check `STEPS.md` for an existing
   phrase first — reuse it rather than rewording; a genuinely new fact gets a
   new `STEP-<slug>` row in the same turn.
4. **Prototype-as-interview**: when the user struggles to answer in the
   abstract, or after two unproductive rounds on the same question, offer to
   build 1–3 throwaway prototypes and harvest reactions instead — people
   answer "what do you want" poorly and critique "is it this?" excellently.
   Rules: prototype code lives on a scratch branch, is NEVER merged, and its
   only outputs are edits to VISION / GLOSSARY / ASSUMPTIONS / use cases.
5. Every 4–6 answers, reflect a summary back and get confirmation.

## Driver interview (second ladder, after the functional minimum)

Architecture decisions are made from FACTS, not use cases — collect them now,
cheaply, in orders of magnitude. Same one-question-per-turn rule. Ladder:
how much data and how fast it grows → who else reads/writes it → what a loss
of it costs → expected load pattern and peaks → what the system MUST talk to
(protocols mandated?) → what is already imposed (budget, deadline, mandated
tech, compliance, who will operate it) → what will change often vs what is
frozen. Record every answer as a `DRV-<slug>` row in DRIVERS.md
(`templates/drivers.md`), `confidence: known`. What the user cannot answer is
recorded as `guessed` with a verify-by — never silently omitted.

## Artifacts — the minimum (docs/product/)

| Artifact | Template | Scope in this phase |
|---|---|---|
| `GLOSSARY.md` | written directly (no template) | every term used in UC and VISION |
| `VISION.md` | `templates/vision.md` | problem, for whom, ≥3 anti-goals, ≥1 metric; personas table and full metrics may stay empty |
| `ACTORS.md` | `templates/actors.md` | one row per actor a use case names as `primary_actor`/`secondary_actors` |
| `STEPS.md` | `templates/steps.md` | one row per distinct Given/When/Then phrase before it is used in a UC |
| `use-cases/UC-*.md` | `templates/use-case.md` (Cockburn fully-dressed) | exactly 3–5, glossary terms only, actor(s) resolved against `ACTORS.md`, steps resolved against `STEPS.md`, ≥1 `[error]`/`[boundary]` extension each |
| `ASSUMPTIONS.md` | `templates/assumptions.md` | every unverified belief, with verify-by |
| `DRIVERS.md` | `templates/drivers.md` | facts in orders of magnitude; unknowns as `guessed` |

`docs/product/UC-DIAGRAM.md` is **generated**, not authored here: run
`scripts/loom/uc_diagram_gen.py` after ACTORS.md and the UC set stabilize to
render the actor↔UC UML diagram (Mermaid flowchart: actors, use cases as
stadium nodes, `<<include>>`/`<<extend>>` edges between UC). It also validates
that every `primary_actor`/`secondary_actors`/`includes`/`extends` reference
resolves — treat a nonzero exit as a blocking OQ, not a thing to hand-fix in
the generated file.

Deliberately deferred (do NOT produce here): full personas, complete metric
trees, domain C4 diagrams, any ADRs. They are added when learning demands —
by the skeleton, consolidation, or intake. The only ADR allowed is
ADR-adopt-loom, which ships with the kit.

## Exit criteria (before /loom:roadmap)

- Glossary covers every domain noun in the other artifacts.
- ≥3 anti-goals; 3–5 use cases; ASSUMPTIONS rows all have verify-by.
- Every use case names a `primary_actor` that resolves to an ACTORS.md row;
  `uc_diagram_gen.py` exits 0.
- `scripts/loom/gherkin_lint.py --gate` exits 0: every step resolves to
  STEPS.md, no near-duplicate phrasing, ≥1 `[error]`/`[boundary]` extension
  per use case.
- DRIVERS.md exists; every `guessed` row has a verify-by.
- Blocking OQs resolved via /loom:review on VISION.md.
