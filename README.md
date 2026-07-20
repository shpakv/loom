# Loom — plugin

A docs-first framework for AI development: a knowledge layer (glossary, DRIVERS,
ADR, package SKILL.md) + gated phases + an anti-cheating TDD engine.

## Installation (local)

    claude
    /plugin marketplace add shpakv/loom
    /plugin install loom@loom

## Project initialization

    /loom:init          # scaffolds docs/, loom.yaml, ADR-0, and a copy of scripts/loom for CI
    # fill in test_command in docs/loom.yaml
    /loom:prime

Route: prime → imagine → technology → review → roadmap → skeleton →
consolidate → design → implement. Utilities: spike, challenge, status.
To update the project scripts after a plugin update: /loom:init --refresh.

## Migration from kit (<=v0.8)

docs/ stays as is. Remove: .claude/commands/loom-*.md,
.claude/skills/loom-*, .claude/agents/loom-*, and the hooks fragment from
.claude/settings.json (the plugin installs the guard hook itself). Update the
project's scripts/loom via /loom:init --refresh. /loom-imagine becomes /loom:imagine.

## Contents

    commands/      13 commands (loom: namespace)
    skills/        loom-core + 6 phases + review-gate + spike/technology-method
    agents/        reviewer, planner, test-author, implementer, code-reviewer, challenger
    hooks/         file-role guard (PreToolUse, automatic)
    scripts/loom/  oq_scan, index_gen, link_check, adr_scan, roadmap_gen, verify_red/green, guard
    init-assets/   loom.yaml, ADR-adopt-loom — copied by /loom:init
