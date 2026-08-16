---
description: Loom phase — decision event after the skeleton: accept the proposed one-way ADRs, reconcile as-built architecture, extract conventions, re-cut roadmap
---
Use the `loom-consolidate-phase` skill (read `loom-core` first).

Verify the walking skeleton is demoable with green CI before starting. Accept the
proposed ADRs on the skeleton's evidence (one-way first, `verification: skeleton`),
then reconcile against reality: confirm/correct quality scenarios with what the
skeleton measured, update building blocks as-built vs as-intended, close the
solution-strategy QS → ADR matrix, extract conventions, sweep ASSUMPTIONS, re-cut
the roadmap. These docs already exist from /loom:requirements and
/loom:architecture — you are confirming or correcting them, not writing them
fresh. Finish with `adr_scan.py --gate --framing` (every accepted one-way ADR
must cite a DRV-* and a QS-*, declare its decision_mode, and every QS must map to
an ADR or convention), `link_check.py docs packages`, and /loom:compile — the
newly accepted decisions and extracted conventions must reach the engine's
constitution before it writes another line against the old one.
