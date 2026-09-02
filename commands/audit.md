---
description: Loom phase — the feedback loop: check whether accepted decisions still hold, surface drift as blocking OQs
---
Use the `loom-audit-phase` skill (read `loom-core` first).

Run the backward pass over settled decisions:
1. `python3 scripts/loom/adr_scan.py --revisit` — check each accepted ADR's
   revisit triggers with the human.
2. Sweep `DRIVERS.md` for `confidence: guessed` rows and, for each,
   `python3 scripts/loom/link_check.py --refs DRV-<slug>` to find accepted ADRs
   standing on an unconfirmed guess.
3. `python3 scripts/loom/oq_scan.py docs/` — surface stale, forgotten OQs.
4. If the configured changes path exists, run
   `python3 scripts/loom/change_scan.py --gate` and report captured/triaged
   changes without a route or accepted/in-progress changes without application
   and revalidation evidence.

Materialize every drifted decision as a `(blocking)` OQ on its document; do NOT
resolve them yourself — present a ranked findings list and the next command per
finding (a superseding ADR via /loom:consolidate, a driver update, or a roadmap
re-cut). For decisions the human confirms still hold, bump the ADR `updated:` and
sharpen its `revisit_when:` instead of opening an OQ.
