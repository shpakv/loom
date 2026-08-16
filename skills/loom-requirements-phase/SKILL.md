---
name: loom-requirements-phase
description: Invoked by the /loom:requirements command to turn approved use cases and DRIVERS into testable quality requirements and binding domain rules before any architecture or technology thinking — promote the proto-QS driver rows into full quality scenarios (stimulus → response → measure), write the BR-* rules the system is obliged to reproduce, trace each to its source. Run /loom:requirements after the vision and use cases are approved and before /loom:architecture.
---

# Loom: requirements phase (quality scenarios and domain rules)

Goal: make the "how good must it be" concrete and testable BEFORE any structure
or technology is chosen — so architecture and technology decisions have measurable
targets to satisfy instead of vibes. A quality requirement you cannot measure is
a wish; this phase converts wishes into scenarios with numbers.

This phase owns both kinds of number the project must honour: `QS-*` quality
scenarios (how good) and `BR-*` domain rules (what is correct). They sit together
because they are gathered in the same conversation and are equally worthless as
adjectives.
Read `loom-core` conventions first (the BR-* section especially).

This phase sits between /loom:roadmap and /loom:architecture. It is deliberately
early: choosing a database before you know the peak ingest rate, or a framework
before you know the latency budget, is how one-way doors get walked through blind.

## Inputs (gate)

Approved `VISION.md` and use cases, the approved first-slice epic (its definition
of done is a source of quality demands), and a `DRIVERS.md` that exists (its
proto-QS rows are the raw material). If use cases or the first-slice epic are
still draft, route to /loom:review or /loom:roadmap. If DRIVERS.md has no
quality/data rows yet, the facts are missing — go back to the driver interview in
/loom:imagine before guessing NFRs here.

## Procedure

1. **Harvest sources.** Read the `## Quality (proto-QS)` and `## Data profile`
   rows of DRIVERS.md, the VISION metrics, and the first-slice epic's definition
   of done. These three are where real quality demands hide.
2. **Promote each proto-QS into a full scenario** in
   `architecture/quality-requirements.md` (from `templates/quality-requirements.md`):
   a concrete stimulus, an expected response, and a hard measure (number + unit).
   `DRV-peak-ingest-rate: ~10^4 rps` becomes
   `QS-ingest-sustained-load: at 10^4 events/s sustained for 1h, p99 write latency < 50ms, zero loss`.
3. **Add the scenarios the drivers missed** but the vision or first epic demand —
   availability, recovery, security posture, operability, cost ceilings. Each is a
   full scenario, not an adjective (see Rules): "an unauthenticated request to any
   /admin route is rejected within 10ms and logged", not "secure".
4. **Trace every scenario** back to its source (`Traces to`): a VISION metric, a
   driver, or an epic. A QS that traces to nothing is either scope creep or a
   hidden assumption — delete it or raise it as a driver first.
5. **Prioritise.** Not every NFR is a must. Mark each scenario's criticality so
   architecture knows which forks are load-bearing. A "could"-level QS must never
   force a one-way technology decision.
6. **Name enforcement intent** per scenario (`Enforced by`): the fitness function,
   CI job, or load test that will later prove it — or `manual (<why>)`. You are not
   building the check now, only committing to how truth will be established.
7. **Write the binding domain rules** into `docs/product/RULES.md` (from
   `templates/rules.md`): every formula, threshold, rounding, boundary and
   tie-break the system is OBLIGED to reproduce, one `BR-<slug>` row each, with
   bounds and source. Mine the use cases, the vision metrics and the domain
   language for them — a use case that says "the invoice shows VAT" is hiding a
   rate, a rounding mode and a base.
   Interview rather than infer: for each rule, ask the human the number, the edge
   behavior (zero, empty, negative, boundary inclusivity, tie-break, timezone) and
   who says so. A rule you cannot source is a **blocking OQ**, not a default —
   this is the one place where even a two-way door does not license a guess,
   because a wrong threshold corrupts data silently. External sources (a standard,
   a regulation, a contract) get a `review_by` date, cited to the section and
   edition; `/loom:audit` reads it.
8. Gates: `oq_scan.py --gate` on both documents, `link_check.py docs`, then
   /loom:review each to `approved`.

## Exit criteria (before /loom:architecture)

- Every proto-QS driver row is either promoted to a `QS-<slug>` or explicitly
  dropped with a one-line reason.
- Every QS is a testable scenario (stimulus → response → measure) that traces to
  a real source and names its criticality and enforcement intent.
- Every rule the approved use cases imply exists as a `BR-<slug>` with bounds and
  a named source, or as a blocking OQ. No rule is present as prose only.
- No blocking OQs open; both documents are `approved`.

## Rules

- **Measures, not adjectives.** "fast", "secure", "scalable" are forbidden as
  acceptance criteria — each must reduce to a number and a unit someone could
  fail. Orders of magnitude are fine (10^3 vs 10^6); false precision is not.
- **A rule without bounds is half a rule.** Most invented arithmetic hides at the
  edges, not in the formula: rounding and where it applies, inclusive vs exclusive
  boundaries, zero and empty cases, tie-breaks, timezones. State them or expect
  them to be filled in plausibly by a model, once per session, differently.
- **QS is not BR.** "p99 write latency under 50 ms" is a quality scenario; "VAT is
  20%, rounded up to the cent" is a rule. If it could be re-decided, it is an ADR
  and belongs in neither file (see the boundary table in `loom-core`).
- **This phase decides nothing about HOW.** No components, no technologies — only
  what the system must be able to withstand. The moment you write a product name
  you have skipped ahead to /loom:technology.
- Do not fold epic-specific acceptance criteria in here; those live in the epic's
  design doc. Quality requirements are system-wide.
