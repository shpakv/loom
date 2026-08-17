---
id: ACTORS
status: draft
owner: pair
updated: {date}
---
# Actors

Every role that triggers or participates in a use case, glossary terms only.
One row per actor; `ID` is referenced from `use-cases/UC-*.md` frontmatter
(`primary_actor:`, `secondary_actors:`) and from `docs/product/UC-DIAGRAM.md`
(generated — never edit by hand).

| ID | Name | Kind | Description |
|---|---|---|---|
| ACTOR-{role} | {role, glossary term} | primary \| secondary \| system | {who they are, what they want from the system} |

Kind: `primary` initiates use cases toward a goal; `secondary` is consulted or
notified but does not initiate; `system` is an external system acting as an
actor (an integration, not a person).

## Open questions
- [ ] OQ-actors-{topic}: ...
