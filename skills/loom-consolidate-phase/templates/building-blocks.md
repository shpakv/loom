---
id: building-blocks
status: draft
owner: pair
updated: {date}
---
# Building blocks (C4 L2)

Containers/packages of the system. Every block here later owns a package
SKILL.md at the listed path — keep names in glossary terms.

```mermaid
graph LR
  %% containers and their allowed dependencies (arrows = "may call/import")
```

| Block | Responsibility (one sentence) | Monorepo path | Key ADRs |
|---|---|---|---|
| {name} | {what it owns, in glossary terms} | packages/{name} | ADR-{...} |

## Forbidden dependencies
Explicit negative edges (these become arch-test rules referencing ADRs):
- {block} must not import {block} — ADR-{slug}

## Open questions
- [ ] OQ-blocks-{topic}: ...
