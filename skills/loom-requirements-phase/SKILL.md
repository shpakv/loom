---
name: loom-requirements-phase
description: Invoked by the /loom:requirements command to turn approved use cases and DRIVERS into testable quality requirements before any architecture or technology thinking — promote the proto-QS driver rows into full quality scenarios (stimulus → response → measure), add the NFRs the vision metrics and first-slice epic demand, trace each scenario to its source. Run /loom:requirements after the vision and use cases are approved and before /loom:architecture.
---

# Loom: requirements phase (quality scenarios)

Goal: make the "how good must it be" concrete and testable BEFORE any structure
or technology is chosen — so architecture and technology decisions have measurable
targets to satisfy instead of vibes. A quality requirement you cannot measure is
a wish; this phase converts wishes into scenarios with numbers.
Read `loom-core` conventions first.

This phase sits between /loom:roadmap and /loom:architecture. It is deliberately
early: choosing a database before you know the peak ingest rate, or a framework
before you know the latency budget, is how one-way doors get walked through blind.

## Inputs (gate)

Approved `VISION.md` and use cases, and a `DRIVERS.md` that exists (its proto-QS
rows are the raw material). If use cases are still draft, route to /loom:review.
If DRIVERS.md has no quality/data rows yet, the facts are missing — go back to
the driver interview in /loom:imagine before guessing NFRs here.

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
   availability, recovery, security posture, operability, cost ceilings. Each must
   still be a scenario, not an adjective: "secure" is not a QS; "an unauthenticated
   request to any /admin route is rejected within 10ms and logged" is.
4. **Trace every scenario** back to its source (`Traces to`): a VISION metric, a
   driver, or an epic. A QS that traces to nothing is either scope creep or a
   hidden assumption — delete it or raise it as a driver first.
5. **Prioritise.** Not every NFR is a must. Mark each scenario's criticality so
   architecture knows which forks are load-bearing. A "could"-level QS must never
   force a one-way technology decision.
6. **Name enforcement intent** per scenario (`Enforced by`): the fitness function,
   CI job, or load test that will later prove it — or `manual (<why>)`. You are not
   building the check now, only committing to how truth will be established.
7. Gates: `oq_scan.py --gate` on the document, then /loom:review it to `approved`.

## Exit criteria (before /loom:architecture)

- Every proto-QS driver row is either promoted to a `QS-<slug>` or explicitly
  dropped with a one-line reason.
- Every QS is a testable scenario (stimulus → response → measure) that traces to
  a real source and names its criticality and enforcement intent.
- No blocking OQs open; the document is `approved`.

## Rules

- **Measures, not adjectives.** "fast", "secure", "scalable" are forbidden as
  acceptance criteria — each must reduce to a number and a unit someone could
  fail. Orders of magnitude are fine (10^3 vs 10^6); false precision is not.
- **This phase decides nothing about HOW.** No components, no technologies — only
  what the system must be able to withstand. The moment you write a product name
  you have skipped ahead to /loom:technology.
- Do not fold epic-specific acceptance criteria in here; those live in the epic's
  design doc. Quality requirements are system-wide.
