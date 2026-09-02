---
id: epic-{slug}-skeleton-brief
status: draft
owner: human
updated: {date}
---
# Skeleton brief: {first-slice epic}

The thinnest end-to-end slice that makes the proposed decisions carry real
weight. Run by any convenient means; specified here. This is a falsification test,
not a demo — a slice that cannot come out wrong has told us nothing.

## The path

One use case across the relevant boundaries: {entry point} → {domain logic} →
{persistence} → {response}, plus the external validation path if relevant.

Use case: `UC-{actor-action}`. Degenerate data and an ugly UI are correct here.

## What each decision must demonstrate

One row per proposed ADR this slice is meant to verify. "Demonstrates" must be an
observation, not a feeling.

| Proposed ADR | Must demonstrate | Refuted if |
|---|---|---|
| `ADR-{slug}` | {the protocol round-trips a real message end to end} | {round-trip needs a translation layer we did not plan} |
| `ADR-{slug}` | {the datastore sustains the write path at QS-{slug}'s rate} | {sustained rate is below target with tuning exhausted} |

## Layers that must be traversed

Anything on this list that the slice stops short of leaves the decisions living
there unverified — name them so the gap is visible rather than assumed.

- [ ] {persistence — the real datastore, not an in-memory double}
- [ ] {boundary as drawn in building-blocks.md}
- [ ] {repeatable observation for the slice}
- [ ] {deploy path, if a decision depends on it}

## Faked

What may be stubbed, hardcoded, or skipped. **This list is the contract.** A
measurement taken through a fake measures the fake, and without this list nobody
can tell afterwards which is which.

- {auth: hardcoded single user}
- {external payment provider: in-process stub returning success}
- {UI: one unstyled page}

## Falsification criterion

The observation that would mean the hypothesis is wrong, stated before the build:
{e.g. "p99 write latency above 50 ms at 10^4 events/s with the datastore tuned"}.

If this is observed, the slice succeeded — record the refutation on the ADR and
raise a blocking OQ. Do not build around it.

## Boundaries

Boundaries exercised by this experiment:

- `{boundary}` — {purpose and evidence needed}

Forbidden dependencies from `building-blocks.md` apply. A forbidden import is a
blocker to report, not an obstacle to work around.

## Out of scope

- A second use case.
- Anything that does not change what we learn about a proposed decision.

## Open questions
- [ ] OQ-{epic-slug}-{topic}: ...
