---
name: loom-spike-method
description: Loom utility — run a time-boxed spike (experiment/research) to answer a specific technical question and produce evidence for an ADR. Use whenever the user runs /loom:spike, wants to compare technologies, validate an assumption (AS-*), de-risk a one-way-door decision, or asks "let's try X before deciding".
---

# Loom: spike

A spike answers ONE falsifiable question within a time-box and ends with a
recommendation. It produces EVIDENCE for ADRs; it never makes the decision.
Read `loom-core` conventions first.

## Procedure

1. Sharpen the question until it is falsifiable: "is QuestDB fast enough?" →
   "does QuestDB sustain 50k rows/s ingest on a 4-vCPU node for 30 min?".
2. Agree the time-box and the kill criterion (when to stop even without an answer).
3. Create `docs/spikes/SPIKE-<slug>.md` from `templates/spike.md`, `status: draft`.
4. Run the experiment. Spike code lives in `spikes/<slug>/` or a scratch branch —
   it is throwaway by default and MUST NOT be promoted to production code silently.
5. Record raw results (numbers, logs, links), then the interpretation, then the
   recommendation — in that order, separated.
6. Set `status: approved` via /loom:review (spikes rarely have blocking OQs) and
   cite the spike from the relevant ADR's Options section as
   `evidence: SPIKE-<slug>`.

## Rules

- One question per spike; a second question is a second spike.
- A spike that ran out of time-box without an answer is still a valid artifact —
  record what was learned and what it would take to answer.
- One spike may feed several ADRs and vice versa.
