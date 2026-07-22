---
name: loom-technology-phase
description: Loom phase (command /loom:technology) — choose technologies AFTER the logical architecture and quality requirements exist: for each building block and each unmet quality scenario, open a technology fork (decision mode first — never lead with a recommendation), record a PROPOSED ADR framed by DRIVERS and QS, and schedule a /loom:spike where a comparison needs evidence. Also captures the team's tech posture into DRIVERS.md if it is not there yet. Use whenever the user runs /loom:technology, mentions choosing or comparing a stack, database, framework, language, queue, protocol or cloud, captures stack constraints or vetoes, or asks "what should we build this with".
---

# Loom: technology phase (decisions as hypotheses)

Goal: pick the technologies that realise the building blocks and satisfy the
quality scenarios — as PROPOSED ADRs, framed by facts, to be verified by the
walking skeleton and accepted only at /loom:consolidate. Technology decisions
fail more often from ignoring the TEAM and the measurable targets than from
ignoring the workload, so this phase leans on two things that now already exist:
DRIVERS.md (facts about the team and world) and quality-requirements.md
(measurable targets). Read `loom-core` conventions first — the technology-fork
protocol especially.

This phase sits between /loom:architecture and /loom:skeleton. Structure is
already fixed as a hypothesis; here you decide what each part is built with. You
do NOT accept one-way decisions here — the skeleton has not proven anything yet.

## Step 0 — Tech posture (only if missing or stale)

Technology choices need facts about the humans, not just the workload: what they
know, what they refuse, what they want to learn, who keeps it alive at 3am. If
DRIVERS.md has no `## Tech posture` section, or it is stale, interview first —
one question per turn, zero recommendations:

1. What stack does the team actually know well? What looks familiar but isn't?
2. What is vetoed or undesired — and why (licensing, past burns, politics)?
3. Novelty appetite: anything you WANT to learn here? Anything you explicitly
   want the most boring option for?
4. Ops reality: who deploys, who is on call, what is the deploy target?
5. What already exists and is paid for (infra, licenses, accounts)?

Record each answer as a `DRV-*` row in `## Tech posture` (`confidence: known`);
update rows on re-runs instead of appending duplicates. "I want to learn X" is a
legitimate driver — record it, don't judge it. This interview is callable at any
time, not only here.

## Procedure — the decisions

1. **Enumerate the forks.** Walk `solution-strategy.md`: every row whose
   "decision still open" column names a technology fork is a decision to make
   here. Add any fork implied by the building blocks (transport between blocks,
   persistence per stateful block, language/runtime).
2. **For each fork, run the technology-fork protocol from loom-core** — decision
   mode BEFORE any recommendation. First check `DRIVERS.md ## Tech posture` and
   the constraints: the fork may already be constrained (a veto, a mandated tech)
   or decided. If not, ask the human the decision mode in ONE question:
   `decided` / `framed` / `menu` / `delegated`. Record the mode in the ADR
   `decision_mode:`. Leading with "I'd use Postgres" before asking the mode
   anchors the human — that is the failure this protocol prevents.
3. **Frame every decision by facts and targets.** The ADR Context must cite the
   `DRV-*` drivers and the `QS-*` scenarios the choice stands on. A datastore ADR
   that does not reference the ingest-rate QS and the data-profile driver is
   deciding blind. Missing deciding fact on a one-way door → STOP, raise a
   blocking OQ, record the answer as a driver, then decide; two-way door → record
   the guess as `confidence: guessed` first.
4. **Record a PROPOSED ADR per fork** (`templates/adr.md` in loom-core), name it
   as an answer (`ADR-use-questdb-for-timeseries`, not `ADR-datastore`):
   - one-way door (language, persistence, inter-block protocol, monorepo tooling)
     → `verification: skeleton` (the skeleton will demonstrate it) or a scheduled
     `/loom:spike` where two options need a head-to-head; keep it `proposed`.
   - two-way door → `verification: judgment`, one paragraph, `proposed`.
   Never set a one-way ADR to `accepted` here — acceptance is /loom:consolidate's
   job, after the skeleton has proven it.
5. **Schedule spikes where evidence is required.** A one-way fork between close
   options, or any choice whose deciding QS the skeleton alone will not exercise,
   gets a `/loom:spike` with a falsifiable question and a kill criterion. The
   spike's recommendation is cited from the ADR Options section, never merged in.
6. **Feed the strategy back.** For each fork now covered by a proposed ADR, note
   the ADR id against its QS row in `solution-strategy.md` — closing the loop
   from quality scenario → structure → technology.
7. Gates: `adr_scan.py --gate` (proposed ADRs are valid), `link_check.py docs`,
   `oq_scan.py --gate` on any ADR carrying a blocking OQ. Proposed ADRs are
   reviewed for framing, not accepted — /loom:review may move them `in-review`,
   never `accepted`.

## Exit criteria (before /loom:skeleton)

- Tech posture exists in DRIVERS.md.
- Every open technology fork from the solution strategy has a proposed ADR (or a
  scheduled spike feeding one), framed by the drivers and quality scenarios it
  depends on.
- Every one-way ADR carries `verification: skeleton` or `verification: SPIKE-*`
  and stays `proposed`; none is accepted.

## Rules

- **Facts and targets, never taste.** Every choice is justified by a `DRV-*`
  and/or a `QS-*`. "I like it" is not a driver; "team knows it
  (DRV-stack-competence)" is.
- **Propose, don't accept.** This phase produces hypotheses to be tested. The
  skeleton verifies; consolidation accepts. A technology decision accepted before
  a single line proves it is exactly the risk this ordering removes.
- **Boring by default, novel by budget.** Prefer the option the team can operate
  unless a driver (novelty appetite) or a QS the boring option cannot meet
  justifies the risk — and say which, in the ADR.
