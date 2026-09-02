---
name: loom-intake-method
description: Capture and triage incoming work in a Loom project, persist changes as CHG records when they affect accepted knowledge or are deferred, and route them to the smallest honest owning phase.
---

# Loom: intake

Intake is the durable front door for incoming requirements, customer changes,
new facts and ideas. Read loom-core first.

Intake has two modes:

- **Capture-only:** immediately after loom:init, before VISION.md exists.
  Preserve the original message and source in the configured changes path
  (normally docs/changes/CHG-<slug>.md) with status: captured; do not classify
  or edit product documents.
- **Capture and triage:** after VISION exists. Classify the item, calculate
  impact, propose one owning phase and stop for the human decision. Do not start
  the downstream phase automatically.

For a trivial, unambiguous change inside one draft document, no CHG-* is
required if it does not affect another scope and is applied immediately. Every
deferred item, hypothesis, change to approved/accepted knowledge or item with
uncertain blast radius gets a change record.

## Capture

1. Record the incoming message verbatim under Original input.
2. Record who or what supplied it in source:
   human, customer, implementation, external or unknown.
3. Record confidence as confirmed, reported or hypothesis.
4. Use skills/loom-intake-method/templates/change-record.md.
5. Keep status: captured until VISION exists and triage is possible.

Do not rewrite the original input into a cleaner requirement. Interpretation
belongs in classification and the owning phase.

## Triage interview

Ask only what is needed to place the work, one question per turn:

1. Is it a defect, a behavior change, a new capability, a new fact, or an idea?
2. Does it fit the current vision, glossary and anti-goals?
3. Does it contradict an approved/accepted document or decision?
4. Does it fit one existing epic, or does it span several / need a new one?
5. Is the claim confirmed, reported or hypothetical?

When VISION is missing, stop after capture. When an unknown is falsifiable,
route to spike rather than guessing.

## Classification

Use one of:

| Classification | Meaning |
|---|---|
| additive | Consistent addition without changing approved authority |
| forgotten-requirement | Requirement that should already have been recorded |
| fact-correction | Previously recorded fact is no longer correct |
| customer-change | Confirmed customer or stakeholder change |
| hypothesis | Unconfirmed signal that needs evidence |
| rule-change | New or changed BR, QS, SLA or numeric constraint |
| decision-conflict | Contradiction with an accepted ADR or architecture |
| roadmap-idea | New capability or priority candidate |

additive is a classification, not a phase. A draft-only additive edit may be
applied without a change record; an additive edit touching approved knowledge
still requires CHG-*.

## Routing table

| Signal | Route to | Why |
|---|---|---|
| Defect or change inside one existing capability, fitting current contracts and decisions | /loom:design on the owning epic | requirements already exist |
| New capability fitting the vision but not covered by an epic | /loom:roadmap, then /loom:design | roadmap owns scope and sequence |
| Change to an accepted decision | /loom:consolidate for a superseding ADR, or /loom:audit when a revisit trigger fired | accepted ADRs are immutable |
| Change to problem, users, anti-goal or glossary | targeted /loom:imagine | vision is the highest authority |
| New quality target or changed NFR/rule | /loom:requirements | requirements own QS/BR |
| Changed boundary or responsibility | /loom:architecture | architecture owns structural boundaries |
| Changed technology decision | /loom:technology plus superseding ADR | technology owns the fork |
| Falsifiable unknown | /loom:spike, then re-run intake | evidence precedes commitment |

When several rows fit, route to the highest-authority row. If prerequisites
are not yet approved, keep the change triaged or accepted and report the
prerequisites; do not restart the whole lifecycle.

## Impact

After the affected IDs are known, run:

    python3 scripts/loom/impact_scan.py --id <affected-id>

Record direct and transitive consumers in affects. Treat approved/accepted
consumers as blocked until their owning phase or review gate revalidates them;
draft consumers are needs-review; generated projections are informational.

## Human decision and handoff

Present:

- classification;
- direct and transitive blast radius;
- proposed owning phase;
- prerequisites and unresolved OQs.

The human, not intake, sets accepted or rejected. On acceptance, hand off
the owning command and leave execution to that command. Intake never edits
approved knowledge and never marks a change applied.

## Output

Return a short verdict containing the change ID, classification, impact summary,
single next command and any prerequisite. For capture-only mode, return the
created change ID and state that triage is waiting for VISION.
