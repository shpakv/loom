---
description: Loom phase — turn approved use cases and drivers into testable quality requirements (NFRs) before architecture
---
Use the `loom-requirements-phase` skill (read `loom-core` first).

Verify VISION.md and use cases are `approved` and DRIVERS.md exists before
starting; otherwise route to /loom:review or back to /loom:imagine. Promote the
proto-QS driver rows into full quality scenarios (stimulus → response → measure),
add the NFRs the vision metrics and first-slice epic demand, trace and prioritise
each. Do not name any component or technology — that is later. Finish by running
`python3 scripts/loom/oq_scan.py --gate docs/architecture/quality-requirements.md`
and reviewing the document.
