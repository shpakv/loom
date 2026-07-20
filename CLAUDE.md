# CLAUDE.md — developing the Loom plugin

This repository **is** a Claude Code plugin. This file guides work on the plugin
itself (its commands, agents, skills, scripts, and manifests) — not on projects
that consume it.

## What Loom is

A docs-first framework for AI development, shipped as a Claude Code plugin:
a knowledge layer (glossary, DRIVERS, ADR, package SKILL.md) + gated lifecycle
phases + an anti-cheating TDD engine. When installed into a target project, its
commands scaffold and drive a `docs/`-centric workflow.

Phase route the plugin exposes to users:
`prime → imagine → technology → review → roadmap → skeleton → consolidate → design → implement`
plus utilities `spike`, `challenge`, `status`.

## Repository layout

    .claude-plugin/   plugin.json + marketplace.json (manifests)
    commands/         13 slash commands (loom: namespace)
    agents/           6 subagents dispatched by commands
    skills/           loom-core + phase/gate/method skills, each with SKILL.md
    hooks/            hooks.json — PreToolUse file-role guard
    scripts/loom/     8 stdlib-only Python gate/generator scripts
    init-assets/       loom.yaml + seed ADR, copied into target projects by /loom:init

## Golden rules

- **Stdlib only in `scripts/loom/`.** Every script is `#!/usr/bin/env python3`
  and imports only the standard library (`re`, `json`, `sys`, `pathlib`,
  `subprocess`, `fnmatch`, `datetime`). There is no dependency manifest and no
  virtualenv. Do not add third-party imports — including PyYAML: `loom.yaml` is
  parsed with deliberate naive regex/line parsing so consuming projects need
  zero setup.
- **Never hardcode the plugin path.** Reference the plugin root as
  `${CLAUDE_PLUGIN_ROOT}` in commands and hooks (e.g.
  `${CLAUDE_PLUGIN_ROOT}/scripts/loom/foo.py`,
  `${CLAUDE_PLUGIN_ROOT}/init-assets/...`).
- **Commands are thin.** A command's job is to invoke a skill by name (and, for
  orchestrators, to dispatch agents) — the actual procedure lives in the skill,
  not the command body.
- **`loom.yaml` is the single source of truth** for paths, statuses, naming,
  phases, `test_command`, and `test_globs`. Scripts read config from it; don't
  duplicate those values elsewhere.
- Keep changes coherent across the four surfaces that describe the same concept:
  a new phase usually touches a **command**, a **skill** (+ templates), possibly
  an **agent**, and the `phases:`/`paths:` blocks in **init-assets/loom.yaml**.

## Authoring conventions

### Commands (`commands/*.md`)
- Frontmatter fields used: `description:` (always) and `argument-hint:` (only for
  commands that take args). No `allowed-tools:` is used anywhere — don't add it
  unless intentionally restricting a command.
- Body: read args via `$ARGUMENTS`. Invoke skills by name, e.g.
  *"Use the `loom-design-phase` skill (read `loom-core` first) on epic:
  $ARGUMENTS"*. Orchestrating commands dispatch named agents.
- Filename = command name; the `loom:` namespace comes from the plugin, so
  `commands/design.md` → `/loom:design`.

### Agents (`agents/*.md`)
- Frontmatter fields (all three required): `name:` (matches filename),
  `description:` (state who dispatches it, e.g. *"Dispatched by /loom:implement
  step 6"*), `tools:` (comma-separated).
- Tool convention: read-only agents (challenger, code-reviewer, planner,
  reviewer) use `Read, Grep, Glob, Bash`; write-capable agents (implementer,
  test-author) use `Read, Grep, Glob, Write, Edit, Bash`. No `model:` field is
  used.
- Body is a plain-prose role and output contract.

### Skills (`skills/<name>/SKILL.md`)
- Frontmatter fields: `name:` (matches directory) and `description:` only. Make
  the description trigger-oriented (*"Use whenever the user runs /loom:..."*) —
  it's how the skill gets surfaced.
- Naming suffixes (defined in `loom-core`): `-phase` for lifecycle phases,
  `-gate` for gates, `-method` for utilities. `loom-core` has no suffix and no
  paired command.
- Document scaffolds live in the skill's `templates/` subdir; the skill
  instructs the agent to instantiate them by relative path (e.g.
  `templates/task.md`). Not every skill has templates.

### Scripts (`scripts/loom/*.py`)
Each is a standalone CLI; most take a `--gate` flag that exits non-zero on
violations for CI use, and several offer `--json`/`--print`.

- `oq_scan.py` — scans docs for open questions (`OQ-`); gates on unresolved
  blocking OQs.
- `index_gen.py` — generates `docs/INDEX.md` from document frontmatter.
- `link_check.py` — slug-ID reference integrity (uniqueness + every mention
  resolves); `--refs <id>` reverse index.
- `adr_scan.py` — ADR lifecycle validator (status vocab, body/frontmatter
  agreement, supersedes symmetry); `--revisit` audits triggers.
- `roadmap_gen.py` — generates `docs/roadmap/ROADMAP.md` from epic frontmatter;
  validates the epic dependency DAG is acyclic.
- `verify_red.py` — TDD red gate: passes only if tests FAIL (optionally for the
  right reason via `--expect`).
- `verify_green.py` — TDD green gate: whole suite must pass.
- `guard_file_roles.py` — the PreToolUse hook (below).

### Hook (`hooks/hooks.json`)
PreToolUse matcher `Edit|Write|MultiEdit` runs `guard_file_roles.py`. It reads
`.loom/role` (written by the implement orchestrator): no marker → allow all;
role `test-author` may write only files matching `test_globs`; role
`implementer` may not touch test-glob files. Blocks with exit code 2 + stderr.

## Testing changes to the plugin

There is **no test suite or CI in this repo** — the TDD gates operate on a
*consuming* project's `test_command`, not on the plugin. To exercise a change:

1. Sanity-run edited scripts directly, e.g.
   `python3 scripts/loom/link_check.py --help` and against a project's `docs/`.
2. Install the plugin locally and drive the affected command end-to-end:
   `/plugin marketplace add /Users/z003pz4w/personal/loom` then
   `/plugin install loom@loom`. Reload Claude Code to re-read the marketplace.
3. For phase/skill changes, run the relevant `/loom:*` command in a scratch
   project scaffolded via `/loom:init`.

## Releasing

- Bump `version` in `.claude-plugin/plugin.json` on any user-visible change.
- **Version skew to be aware of:** `plugin.json` `version` (currently `0.6.0`)
  tracks the *plugin package*, while `init-assets/loom.yaml` carries its own
  `version`/`scripts_version` (currently `0.9`/`0.9.0`) tracking the *scaffolded
  framework/scripts*. These are intentionally independent — bump each for changes
  to its own surface. Bump `scripts_version` in `init-assets/loom.yaml` when
  `scripts/loom/*` change, since consuming projects re-sync via
  `/loom:init --refresh`.
- Install/marketplace names are both `loom`, so the install id is `loom@loom`
  (`<plugin>@<marketplace>`). Keep README install instructions in sync.
