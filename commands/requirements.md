---
description: Loom phase — turn approved use cases and drivers into testable quality requirements (NFRs) and binding domain rules, before architecture
---
Use the `loom-requirements-phase` skill (read `loom-core` first).

Verify VISION.md and use cases are `approved` and DRIVERS.md exists before
starting; otherwise route to /loom:review or back to /loom:imagine. Promote the
proto-QS driver rows into full quality scenarios (stimulus → response → measure),
add the NFRs the vision metrics and first-slice epic demand, trace and prioritise
each. Then write `docs/product/RULES.md`: every formula, threshold, rounding and
boundary the system is obliged to reproduce, as `BR-*` rows with bounds and a
named source — interview the human for the edge cases, and raise a blocking OQ
rather than assuming any number. Do not name any component or technology — that is
later. Finish by running `python3 scripts/loom/oq_scan.py --gate` on
`docs/architecture/quality-requirements.md` and `docs/product/RULES.md`, and
reviewing both.
