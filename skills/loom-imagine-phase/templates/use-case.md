---
id: UC-{actor-action}
status: draft
owner: pair
updated: {date}
primary_actor: ACTOR-{role}
secondary_actors: []
includes: []       # UC-* this one always pulls in (UML <<include>>)
extends: []        # UC-* this one conditionally extends (UML <<extend>>)
---
# UC: {Actor does action, in glossary terms}

Cockburn fully-dressed use case. Actor(s) resolve against `ACTORS.md`
(`templates/actors.md`); `includes`/`extends` resolve against sibling
`UC-*.md` — both are checked by `link_check.py` and drawn in the generated
`docs/product/UC-DIAGRAM.md` (never hand-edited).

**Primary actor:** {ACTOR-role} — {one-line goal from their point of view}
**Secondary actors:** {ACTOR-role, or "none"}
**Trigger:** {what starts this}

**Preconditions:** {what must already be true for the scenario to start}
**Minimal guarantee:** {what holds even if the scenario fails or is aborted}
**Success guarantee:** {observable result worth money/time to the actor, once achieved}

Every Given/When/Then below must match a phrase registered in `STEPS.md`
(`templates/steps.md`), exactly or via its `{placeholder}` slots — do not
reword an existing step; reuse it. `scripts/loom/gherkin_lint.py --gate`
checks this and that at least one extension below is tagged `[error]` or
`[boundary]` — happy-path-only use cases fail the gate.

## Main success scenario
```gherkin
Given ...
When ...
Then ...
```

## Extensions
Numbered against the main scenario step they branch from. Tag each with its
kind — `[alternate]` (a different but still successful path), `[error]` (the
actor or system fails, is denied, times out, ...), `[boundary]` (empty,
zero, max, duplicate, concurrent). At least one `[error]` or `[boundary]`
extension is required; each is itself a Gherkin fragment reusing `STEPS.md`
phrases.

- **{step}a. [alternate]** {condition}
  ```gherkin
  Given ...
  When ...
  Then ...
  ```
- **{step}b. [error]** {condition}
  ```gherkin
  Given ...
  When ...
  Then ...
  ```

## Open questions
- [ ] OQ-{uc-slug}-{topic}: ...
