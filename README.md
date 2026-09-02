# Loom

Loom is a requirements repository for AI-assisted development: a structured,
docs-first place for product language, requirements, business rules,
architecture, decisions and task specifications.

Loom does not generate code, tests or plans, and it does not prepare files for
another development process. It keeps the project's durable knowledge coherent;
implementation may happen by hand, in an IDE, through an AI assistant or by any
other process.

## Installation

Claude Code:

    claude
    /plugin marketplace add shpakv/loom
    /plugin install loom@loom

Codex:

    codex plugin marketplace add shpakv/loom
    codex plugin add loom@loom

GitHub Copilot:

    copilot plugin marketplace add shpakv/loom
    copilot plugin install loom@loom

## Project initialization

Claude Code:

    /loom:init
    /loom:prime

Codex:

    Use the `loom-init` skill, then invoke `loom-prime-method`.

GitHub Copilot:

    Ask Copilot to initialize Loom, then run the `loom-prime-method` workflow.

All hosts use the same shared skills and `scripts/loom` gates; Claude commands
are thin aliases for those methods.

The lifecycle is:

    prime → imagine → roadmap → requirements → architecture → technology →
    skeleton → consolidate → design

Utilities are `spike`, `challenge`, `review`, `status`, `audit` and `intake`.
The final artifact is an approved set of requirements and decisions under
`docs/`; Loom has no implementation handoff step.

## What Loom stores

- glossary, actors and use cases;
- drivers and quality scenarios;
- binding domain rules (`BR-*`);
- ADRs with alternatives, evidence and revisit triggers;
- architecture hypotheses, boundaries and contracts;
- roadmap epics, designs and task specifications;
- open questions and the reasons behind decisions.

Generated indexes are convenience projections of the documents. The documents
under `docs/` remain the source of truth.

## Contents

    commands/       Claude Code command wrappers
    skills/         shared lifecycle phases, gates and methods
    agents/         read-only challenger and reviewer agents
    copilot-agents/ Copilot read-only agent profiles
    scripts/loom/   stdlib-only document gates and generators
    init-assets/    loom.yaml, seed ADR and initialization assets
