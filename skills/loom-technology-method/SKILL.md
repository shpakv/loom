---
name: loom-technology-method
description: Loom utility (command /loom:technology) — interview the human about tech posture: stack competence, forbidden tech, novelty appetite, ops reality, existing infrastructure; writes DRV rows into DRIVERS.md. Use whenever the user runs /loom:technology, mentions stack preferences or constraints, or before any session expected to hit technology forks.
---

# Loom: technology posture

Technology decisions fail more often from ignoring the TEAM than from ignoring
the workload. This interview collects facts about the humans: what they know,
what they refuse, what they want to learn, and who keeps it alive at 3am.
Read `loom-core` conventions first (technology-fork protocol especially).

## Interview ladder (one question per turn)

1. What stack does the team actually know well? What looks familiar but isn't?
2. What is vetoed or undesired — and why (licensing, past burns, politics)?
3. Novelty appetite: anything you WANT to learn on this project? Anything
   where you explicitly want the most boring option?
4. Ops reality: who deploys, who is on call, what is the deploy target?
5. What already exists and is paid for (infra, licenses, accounts)?

Record every answer as a DRV row in `## Tech posture` of
docs/product/DRIVERS.md (`confidence: known`). "I want to learn X" is a
legitimate driver — record it, don't judge it. Update rows on re-runs
instead of appending duplicates.

## Rules

- Facts only; zero recommendations in this mode. If the human asks "so what
  should I pick?", switch to the technology-fork protocol (loom-core): ask
  the decision mode first.
- This interview is callable at any point in the project, not only at start.
