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

## Main success scenario
```gherkin
Given ...
When ...
Then ...
```

## Extensions
Numbered against the main scenario step they branch from; each is itself a
Gherkin fragment so it stays executable-adjacent.

- **{step}a.** {condition}
  ```gherkin
  Given ...
  When ...
  Then ...
  ```

## Open questions
- [ ] OQ-{uc-slug}-{topic}: ...
