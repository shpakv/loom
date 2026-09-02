---
id: building-blocks
status: draft
owner: pair
updated: {date}
---
# Building blocks (C4 L2)

Responsibilities of the system. Every block here is an architectural boundary
documented under `docs/architecture/` — keep names in glossary terms.

```mermaid
graph LR
  %% containers and their allowed dependencies (arrows = "may call/import")
```

Leave the **Key ADRs** column empty in /loom:architecture — no ADRs exist yet;
it is filled in at /loom:consolidate once the technology ADRs are accepted.

| Block | Responsibility (one sentence) | Monorepo path | Key ADRs |
|---|---|---|---|
| {name} | {what it owns, in glossary terms} | {boundary or document} | — (filled at consolidate) |

## Forbidden dependencies
Explicit negative edges (these become arch-test rules referencing ADRs once the
decisions exist — leave the ADR reference off until /loom:consolidate):
- {block} must not import {block}

## Open questions
- [ ] OQ-blocks-{topic}: ...
