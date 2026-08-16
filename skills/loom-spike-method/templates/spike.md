---
id: SPIKE-{question-or-comparison}
status: draft
owner: pair
updated: {date}
feeds: []                # ADR ids this spike is expected to inform
---
# SPIKE: {Falsifiable question}

**Time-box:** {e.g. 4h}
**Kill criterion:** {when to stop without an answer}
**Fidelity axis:** {UX | performance | integration | logic} — minimal on all others
**Rung:** {napkin | clickable mock | single-file script | throwaway app} — the
lowest one that can falsify the answer

## Setup
Environment, versions, data set, method — enough to reproduce.

## Faked
What is stubbed, hardcoded or skipped. **The contract of the probe.** Without
this list, "it was slow" cannot be distinguished from an artifact of a fake, and
the results are uninterpretable a week later.

- {…}

## Raw results
Numbers, logs, links. No interpretation here.

## Interpretation
What the results mean, threats to validity.

## Recommendation
{One paragraph. A recommendation, not a decision — the decision is an ADR.}
