# AGENTS.md — developing the Loom plugin

Loom is a multi-host plugin for Claude Code, OpenAI Codex and GitHub Copilot.
It is a requirements repository: a docs-first workflow for storing and
validating product language, requirements, rules, decisions, architecture and
task specifications. Loom does not generate product code, tests, plans or
files for another development process.

## Route and boundaries

The lifecycle is:

`prime → imagine → roadmap → requirements → architecture → technology → skeleton → consolidate → design`

Utilities are `spike`, `challenge`, `review`, `status`, `audit` and `intake`.
The durable result is the approved knowledge under `docs/`.

Loom owns glossary, drivers, quality scenarios, `BR-*` rules, ADRs, contracts,
architecture boundaries, epics, designs and task specs. Implementation,
testing and code review may happen anywhere, but are outside Loom's workflow.
If implementation contradicts an approved document, record a blocking OQ and
resolve the document through its owning phase; do not silently rewrite it.

## Repository layout

    .claude-plugin/   Claude Code plugin + marketplace manifests
    .codex-plugin/    Codex plugin manifest
    plugin.json       GitHub Copilot plugin manifest
    .agents/          Codex repository marketplace
    .github/           Copilot instructions + marketplace
    commands/         Claude Code slash commands
    agents/           Claude Code read-only challenger and reviewer
    copilot-agents/   Copilot read-only agent profiles
    skills/           shared Agent Skills and phase workflows
    scripts/loom/     stdlib-only document gates and generators
    init-assets/      loom.yaml, seed ADR, copied by /loom:init

## Golden rules

- `scripts/loom/` uses only the Python standard library.
- Never hardcode the plugin path. Claude commands use
  `${CLAUDE_PLUGIN_ROOT}`; other hosts locate bundled resources relative to the
  installed plugin.
- Commands are thin wrappers. Durable procedure belongs in skills.
- `loom.yaml` is the source of truth for paths, statuses, naming and phases.
- Generated indexes are projections and open with the `GENERATED` marker.
- Keep a new concept coherent across its command, skill, templates, agents and
  `init-assets/loom.yaml` when applicable.

## Authoring conventions

Commands use `description:` and optional `argument-hint:` frontmatter, read
arguments through `$ARGUMENTS`, and invoke a named skill. Skills use only
`name:` and `description:` frontmatter. `loom-core` is the shared read-first
substrate. Agents are read-only and report findings; the orchestrating session
materializes document changes.

Documents use immutable slug IDs, explicit statuses and blocking OQs. Accepted
ADRs are changed only through addenda or superseding ADRs. Templates live in a
skill's `templates/` directory.

## Testing plugin changes

There is no consuming-product test suite in this repository. Run edited scripts
directly, compile Python files with `python3 -m py_compile`, and install the
affected host integration in a scratch project initialized with `/loom:init`.

## Releasing

Bump the plugin version in all host manifests for user-visible changes
and update `CHANGELOG.md` in the same commit. The framework `version` and
`scripts_version` in `init-assets/loom.yaml` track the scaffolded document
workflow independently; bump `scripts_version` when `scripts/loom/*` changes.
