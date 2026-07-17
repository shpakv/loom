---
name: {package-name}
description: Working with the {package-name} package — its purpose, boundaries, public API and testing workflow. Consult whenever a task touches packages/{package-name}.
api_hash: null           # refreshed by tooling; drift vs exported surface fails CI
---

# Package: {package-name}

## Purpose
2–3 sentences: what this package owns, in glossary terms, and its place in
building-blocks (C4 L2).

## Boundaries — what this package must NOT do
- Must not import: {packages}  (see ADR-{slug})
- Must not know about: {concerns owned elsewhere}
Negative constraints first — they steer agents better than permissions.

## Public API surface
The exported types/functions consumers may rely on. Everything else is
internal and free to change.

## Domain invariants
Rules that must hold regardless of caller.

## How to test
```
{exact commands: unit, integration, lint}
```

## Common tasks
Typical changes with a pointer to an example commit/file each.

## Relevant ADRs
- ADR-{slug} — {one line why it matters here}
