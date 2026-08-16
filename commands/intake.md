---
description: Loom utility — triage incoming work on an existing project and route it to the smallest phase that fits
argument-hint: [idea | bug | feature request in a sentence]
---
Use the `loom-intake-method` skill (read `loom-core` first).

Incoming item from the user: $ARGUMENTS

Run a short triage interview (one question per turn, stop as soon as the route is
clear) to size the work and route it to the SMALLEST phase that honestly handles
it — a task under an existing epic (/loom:design → /loom:compile), a new epic
candidate (/loom:roadmap), a revisited decision (superseding ADR via
/loom:consolidate or /loom:audit), a vision change (/loom:imagine), a new quality
target (/loom:requirements), or a spike first (/loom:spike). When several fit,
route to the highest authority. Output a verdict, the single next command, and the
one artifact (if any) to create before it. Do not start the downstream phase
yourself. For a brand-new product with no docs/ yet, send the user to /loom:imagine
instead.
