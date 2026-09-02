---
description: Loom phase — decision event after evidence: accept proposed ADRs, reconcile architecture, extract conventions, and re-cut the roadmap
---
Use the `loom-consolidate-phase` skill (read `loom-core` first).

Verify the evidence summary or reasoned judgment is recorded before starting.
Accept, reject or defer proposed ADRs according to project policy and authority,
then reconcile against reality: confirm/correct quality scenarios with what the
available evidence observed, update building blocks as-observed vs as-intended, close the
solution-strategy QS → ADR matrix, extract conventions, sweep ASSUMPTIONS, re-cut
the roadmap. These docs already exist from /loom:requirements and
/loom:architecture — you are confirming or correcting them, not writing them
fresh. Finish with `adr_scan.py --gate --framing` (every accepted one-way ADR
must cite a DRV-* and a QS-*, declare its policy decision_mode, and every QS must map to
an ADR or convention), and `link_check.py docs`. The repository's
approved documents are the durable result.
