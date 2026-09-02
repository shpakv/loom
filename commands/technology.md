---
description: Loom phase — choose technologies as proposed recommendations with evidence provenance after the logical architecture exists
argument-hint: [building block or fork to decide]
---
Use the `loom-technology-phase` skill (read `loom-core` first).

Verify `solution-strategy.md` is `approved` (its open forks are your work list);
if DRIVERS.md has no `## Tech posture`, run that interview first (one question
per turn, zero recommendations). For each open fork run the loom-core
technology-fork protocol — decision mode BEFORE any recommendation — and record
a PROPOSED ADR framed by the `DRV-*` and `QS-*` it stands on. Never accept a
one-way ADR here. Use an optional spike, benchmark, prototype or skeleton where
uncertainty reduction justifies the cost; /loom:consolidate or /loom:review records
the authority's outcome. Finish with `adr_scan.py --gate`
and `link_check.py docs`.

Fork or block to decide (optional): $ARGUMENTS
