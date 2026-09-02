---
name: loom-skeleton-phase
description: Define the smallest architecture-validation slice or falsification exercise for a Loom project. Use after technology proposals and before consolidation when a decision needs evidence; record the brief and results as project knowledge, without prescribing an implementation.
---

# Loom: skeleton phase

Goal: validate an architectural or technology hypothesis with the smallest
honest exercise that can falsify it. Loom records the question, evidence and
conclusion; it does not build production code or prescribe who builds a probe.
Read `loom-core` conventions first.

## Inputs (gate)

Approved `GLOSSARY.md`, `VISION.md`, `quality-requirements.md`, the
architecture hypothesis (`building-blocks.md`, `solution-strategy.md`) and its
proposed technology ADRs. A first-slice epic may be used to choose the domain
scenario, but this phase does not require an implementation project.

## Procedure

1. Choose one falsifiable question per decision. State what observation would
   refute the hypothesis and what evidence would be sufficient to accept it.
2. Create the skeleton brief from `templates/skeleton-brief.md`. Record the
   scenario, layers or boundaries that matter, the fidelity required, what may
   be faked, the time-box and the falsification criterion.
3. Run the cheapest honest exercise available: a paper model, benchmark,
   prototype, integration probe or walking slice. Keep throwaway artifacts
   quarantined and label every fake or shortcut.
4. Record raw observations before interpretation. Update the relevant proposed
   ADR with the evidence, limitations and conclusion; keep the ADR proposed
   until `/loom:consolidate` accepts or rejects it.
5. If the evidence exposes a missing requirement, driver or decision, create a
   blocking OQ and route it to the owning phase. Do not silently adapt the
   architecture to the result.

## Exit criteria

- The question, time-box, fidelity and falsification criterion are explicit.
- Results distinguish observation from interpretation and state the limits of
  the evidence.
- Every affected ADR, quality scenario or assumption links to the result.
- Any unresolved consequence is a blocking OQ.
- `link_check.py docs` and `oq_scan.py --gate` pass on the artifacts.

## Rules

- One question per exercise; a second question is a second spike.
- A demo that cannot fail is not evidence.
- Do not turn a throwaway probe into a product dependency through this phase.
- The deliverable is durable knowledge in `docs/`, not code.
