---
name: loom-audit-phase
description: Run the backward audit over accepted ADRs, revisit triggers, stale open questions, guessed drivers and due business rules. Use after a release, incident or meaningful change; report drift as blocking questions and never decide on behalf of the human.
---

# Loom: audit phase (close the learning loop)

Goal: catch decisions that have quietly gone stale. Loom's forward phases fix
decisions at the moment of maximum knowledge — but the world moves: load grows,
vendors change, guessed facts get measured, assumptions break. Without a
deliberate backward pass, an `accepted` ADR keeps looking authoritative long
after its deciding facts stopped being true. This phase is that backward pass.
Read `loom-core` conventions first (ADR lifecycle and the OQ lifecycle
especially).

This is an **event**, not an ongoing phase, and it is callable at any time — after
a release, after an incident, on a cadence, or whenever someone suspects a
decision has drifted. It never resolves anything itself: it surfaces drift as
blocking OQs and hands them to the human. Resolution happens through the normal
phases (a superseding ADR, a driver update, a re-cut roadmap).

## Inputs (gate)

An initialized Loom project with accepted ADRs and a `DRIVERS.md`. No status gate
— audit reads everything, including `accepted`/`approved` documents, precisely
because those are the ones assumed settled.

## Procedure

1. **Fire the revisit triggers.** Run `adr_scan.py --revisit` — it prints every
   accepted ADR and its `revisit_when:` triggers. For each trigger, ask the human
   ONE question: has this condition been met since the decision? (A trigger like
   "sustained load > 5k rps" is a fact to check, not an opinion.) An accepted ADR
   with `revisit_when: (none declared)` is itself a finding — a decision no one
   knows how to invalidate.
   The same command also lists `BR-*` rules whose `review_by` date has arrived —
   rules sourced from a standard, regulation or contract rot by revision, so for
   each one ask whether that source has been revised since. "We comply with the
   standard" silently becomes false at its next edition.
2. **Sweep unconfirmed guessed drivers.** For every `DRIVERS.md` row with
   `confidence: guessed`, run `link_check.py --refs DRV-<slug>` to see which
   accepted ADRs stand on it. A guessed fact still carrying a live one-way
   decision is the highest-risk drift there is: flag it.
3. **Surface stale open questions.** Run `oq_scan.py docs/` — OQs that were opened
   long ago and never resolved, especially on `approved` documents, are decisions
   that were deferred and then forgotten. List them.
4. **Materialize drift as blocking OQs.** For each finding above, add a `(blocking)`
   OQ to the affected document (the ADR, the driver's consumer, or the design
   doc), phrased as the question the human must answer — e.g.
   `OQ-<adr>-revisit-load (blocking): peak load now exceeds 5k rps — does
   ADR-use-questdb still hold?`. Do NOT resolve them; that is the human's call and
   the forward phases' job.
5. **Route the confirmed-still-valid ones.** Where the human confirms a decision
   still holds, do not open an OQ — bump the ADR's `updated:` and, if the trigger
   was vague, sharpen its `revisit_when:`. A decision that survived an audit with a
   tightened trigger is stronger than one that was never checked.
6. **Re-cut the roadmap if the audit changed the picture.** A broken load-bearing
   decision often reshuffles priorities — hand off to /loom:roadmap (or
   /loom:consolidate if a one-way ADR must be superseded) rather than editing
   epics here.
7. **Check the projection.** Run `compile.py --check`: a stale constitution means
   the engine is being handed decisions the docs no longer hold, which is drift in
   the other direction. If this audit changed any ADR status, sharpened a rule, or
   deprecated a decision, re-run `/loom:compile` — a deprecated decision still
   sitting in the engine's constitution is worse than an undocumented one, because
   the engine will actively obey it.
8. Report: a short list of findings by severity (broken one-way decision >
   unconfirmed guessed driver under a live decision > deprecated decision still in
   the projection > overdue rule review > stale OQ > missing revisit trigger),
   each pointing at the OQ it became and the command that will resolve it.

## Exit criteria

- Every accepted ADR's revisit triggers have been checked with the human.
- Every drifted decision is now a blocking OQ on its document; every
  confirmed-still-valid decision has a bumped `updated:` and a usable trigger.
- The human has a ranked findings list and a clear next command per finding.

## Rules

- **Audit surfaces, it never decides.** The moment you supersede an ADR or rewrite
  a driver inside this event, you have skipped the human and the forward phase that
  own that change. Produce OQs and hand off.
- **Triggers, not calendars.** Audit is driven by `revisit_when:` conditions, not
  by "it's been six months". A calendar `review_by` is only appropriate for
  decisions tied to the outside world (licenses, vendor EOL) — treat those as one
  more trigger.
- **A clean audit is a real result.** Finding nothing drifted, on a project whose
  triggers are well-declared, is success — record it so the next audit knows the
  baseline.
