# Loom — plugin

The knowledge layer for AI development: glossary, drivers, domain rules, ADR
lifecycle, contracts, package boundaries and task specs — compiled into whatever
SDD engine writes the code.

**Loom does not implement.** Spec-driven engines (Spec Kit, Kiro, OpenSpec, BMAD,
…) are execution engines for feature scope and each does it better, in its own
style. What none of them do is accumulate knowledge between features: the
glossary, the measured facts, the binding rules and the reasons behind accepted
decisions. That gap is all Loom does. It hands the engine a spec and a
constitution, and pulls back what the engine decided on its own.

## Installation (local)

    claude
    /plugin marketplace add shpakv/loom
    /plugin install loom@loom

## Project initialization

    /loom:init          # scaffolds docs/, loom.yaml, ADR-0, and a copy of scripts/loom for CI
    # fill in the engine: block in docs/loom.yaml (which SDD engine writes the code)
    /loom:prime

Route: prime → imagine → roadmap → requirements → architecture → technology →
skeleton → consolidate → design → **compile** → ((the engine implements)) →
**harvest**. Utilities: spike, challenge, review, status, audit, intake.

Requirements and structure come before technology; technology decisions are
proposed and the skeleton verifies them (Loom writes the skeleton brief, the
engine builds it). `compile` projects the knowledge layer into the engine's own
files; `harvest` reads back the terms, numbers and decisions the engine settled by
itself and files them where they belong. `audit` is the backward pass that
re-checks accepted decisions against their revisit triggers and rules against
their review dates; `intake` routes incoming work — from a human or from harvest —
to the smallest phase that fits. To update the project scripts after a plugin
update: /loom:init --refresh.

## What Loom owns, and what it does not

| Loom | the engine |
|---|---|
| glossary, drivers, `BR-*` rules, quality scenarios | the plan, the step order |
| decisions and their reasons (ADR lifecycle) | tests and code |
| contracts, invariants, package boundaries | diff review, refactoring |
| the task `## Spec` — behavior, acceptance, out of scope | how the behavior is achieved |

The anti-cheating TDD machinery Loom used to run itself — role separation, a red
gate that requires failing *for the right reason*, a file-role hook — is kept as a
portable recipe in `docs/recipes/anti-cheating-tdd.md`, because SDD engines ship
nothing like it and it is orthogonal to whose engine runs the loop.

## Migration from kit (<=v0.8)

docs/ stays as is. Remove: .claude/commands/loom-*.md, .claude/skills/loom-*,
.claude/agents/loom-*, and any Loom hooks fragment in .claude/settings.json (the
plugin ships no hooks since 0.20.0). Update the project's scripts/loom via
/loom:init --refresh. /loom-imagine becomes /loom:imagine.

## Contents

    commands/      18 commands (loom: namespace)
    skills/        loom-core + 10 phases + review-gate + spike/intake/harvest-method
    agents/        reviewer, challenger, harvester
    scripts/loom/  oq_scan, index_gen, link_check, adr_scan, roadmap_gen, compile
    init-assets/   loom.yaml, ADR-adopt-loom — copied by /loom:init
    docs/recipes/  anti-cheating TDD, for whoever runs the implementation loop
