---
id: CHG-{slug}
status: captured
owner: human
source: unknown
received: {date}
confidence: reported
classification: null
route: null
affects: []
decision: null
decided_by: null
decided_at: null
applied_documents: []
revalidated_documents: []
superseded_by: null
updated: {date}
---
# Change: {short title}

## Original input

Record the incoming message verbatim, including its source and date.

## Classification

- **Type:** pending
- **Proposed route:** pending
- **Confidence:** reported

## Impact

Run `python3 scripts/loom/impact_scan.py --id <affected-id>` after the project
has a VISION. Record direct and transitive consumers in frontmatter `affects:`.

## Decision

Record the human decision, authority and date here. Intake does not decide on
behalf of the human.

## Application

List the owning documents changed by the owning phase and the downstream
documents revalidated. Set `status: applied` only when both lists are complete.

## Open questions

- [ ] OQ-{slug}-decision: What decision is required before this change can proceed?
