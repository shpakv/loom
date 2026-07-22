---
name: loom-imagine-phase
description: Loom phase (command /loom:imagine) — extract the MINIMUM shared understanding before first code: glossary, anti-goals, 3 use cases, assumptions — via socratic interview and throwaway prototypes. Use whenever the user runs /loom:imagine, brings a new project or feature idea, says "I have an idea", or asks to flesh out a raw concept.
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
| `GLOSSARY.md` | from `templates/glossary.yaml` | every term used in UC and VISION |
| `VISION.md` | `templates/vision.md` | problem, for whom, ≥3 anti-goals, ≥1 metric; personas table and full metrics may stay empty |
| `use-cases/UC-*.md` | `templates/use-case.md` | exactly 3–5, glossary terms only |
| `ASSUMPTIONS.md` | `templates/assumptions.md` | every unverified belief, with verify-by |
| `DRIVERS.md` | `templates/drivers.md` | facts in orders of magnitude; unknowns as `guessed` |

Deliberately deferred (do NOT produce here): full personas, complete metric
trees, domain C4 diagrams, any ADRs. They are added when learning demands —
by the skeleton, consolidation, or intake. The only ADR allowed is
ADR-adopt-loom, which ships with the kit.

## Exit criteria (before /loom:roadmap)

- Glossary covers every domain noun in the other artifacts.
- ≥3 anti-goals; 3–5 use cases; ASSUMPTIONS rows all have verify-by.
- DRIVERS.md exists; every `guessed` row has a verify-by.
- Blocking OQs resolved via /loom:review on VISION.md.
