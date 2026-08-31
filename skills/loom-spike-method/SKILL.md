---
name: loom-spike-method
description: Frame and record a time-boxed spike that answers one falsifiable question and produces evidence for an ADR. Use when a technology or design fork needs evidence; define the probe, fidelity, kill criterion and fakes before building.
---

# Loom: spike (probes)

A spike answers ONE falsifiable question within a time-box and ends with a
recommendation. It produces EVIDENCE for ADRs; it never makes the decision.
Loom frames it and records it — the throwaway code itself is built by the engine,
a human, or a shell one-liner, whichever is cheapest.
Read `loom-core` conventions first.

Spike, probe, prototype, tracer bullet: one genre — **throwaway code as an
instrument of knowledge**. Treat them identically; the differences that matter
are the fidelity axis and the rung, both recorded in the document.

## Procedure

1. Sharpen the question until it is falsifiable: "is QuestDB fast enough?" →
   "does QuestDB sustain 50k rows/s ingest on a 4-vCPU node for 30 min?".
2. Agree the time-box and the kill criterion (when to stop even without an answer).
3. Create `docs/spikes/SPIKE-<slug>.md` from `templates/spike.md`, `status: draft`,
   and fill everything except results BEFORE anything is built:
   - **fidelity axis** — one of UX / performance / integration / logic, minimal on
     all the others. A probe that is faithful on every axis is a product;
   - **rung** — napkin → clickable mock → single-file script → throwaway app. Take
     the LOWEST rung that can falsify the answer; a napkin that settles the
     question beats a working prototype that settles it a day later;
   - **`Faked:`** — what is stubbed, hardcoded or skipped. This is the contract:
     without it, "it was slow" cannot be told apart from an artifact of a fake.
4. Have it built and run. Probe code lives in `spikes/<slug>/` or a scratch
   branch, is throwaway by default, and MUST NOT be promoted to production code
   silently. It gets **no tests, no review, no conventions and no roles** — its
   cheapness comes from the absence of the quality apparatus, not from being
   small. Paying for the protection of code you are about to delete is a category
   error.
5. Record raw results (numbers, logs, links), then the interpretation, then the
   recommendation — in that order, separated. In the interpretation, state
   explicitly which results ran through something on the `Faked:` list: those
   measure the fake, not the system.
6. Set `status: approved` via /loom:review (spikes rarely have blocking OQs) and
   cite the spike from the relevant ADR's Options section as
   `evidence: SPIKE-<slug>`.

## Rules

- One question per spike; a second question is a second spike.
- A spike that ran out of time-box without an answer is still a valid artifact —
  record what was learned and what it would take to answer.
- One spike may feed several ADRs and vice versa.
- **Quarantine the code.** Separate branch or directory, not deployed by CI, merge
  blocked. "But it works, let's keep it" is how a probe becomes an unowned
  production dependency with no tests.
- **Know what a probe cannot answer.** "Code is cheap" holds for stateless logic
  and UI, weakens on persistence, and dies on live data — a migration is never
  throwaway. And invariants and security do not show up in a reaction to a
  prototype: they have to be stated, not probed.
