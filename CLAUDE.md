# CLAUDE.md — developing the Loom plugin

This repository **is** a Claude Code plugin. This file guides work on the plugin
itself (its commands, agents, skills, scripts, and manifests) — not on projects
that consume it.

## What Loom is

The knowledge layer for AI development, shipped as a Claude Code plugin:
glossary, DRIVERS, `BR-*` rules, ADR lifecycle, contracts, package SKILL.md and
task specs + gated lifecycle phases. When installed into a target project, its
commands scaffold and drive a `docs/`-centric workflow.

**Loom does not implement** (since 0.20.0 — see `CONCEPT.md` §2). It produces
knowledge and stops at the task `## Spec`; an external SDD engine (Spec Kit, Kiro,
OpenSpec, BMAD, a plain agent harness) writes the plan, the tests and the code.
Two commands are the seam: `compile` projects the knowledge layer into the
engine's own files, `harvest` reads back what the engine decided by itself. When
adding a surface, the test is: *does this produce knowledge, or does it produce
code?* The second belongs to the engine — and the old implementation machinery is
kept only as a portable recipe in `docs/recipes/anti-cheating-tdd.md`, which the
plugin never executes.

Phase route the plugin exposes to users (requirements and structure precede
technology; technology decisions are proposed, the skeleton verifies them):
`prime → imagine → roadmap → requirements → architecture → technology → skeleton → consolidate → design → compile → ((engine)) → harvest`
plus utilities `spike`, `challenge`, `review`, `status`, `audit` (the backward
pass that re-checks accepted decisions against their revisit triggers and `BR-*`
rules against their `review_by` dates), and `intake` (triage front door that
routes incoming work — from a human or from `harvest` — to the smallest phase that
fits, instead of a full `imagine`).

## Repository layout

    .claude-plugin/   plugin.json + marketplace.json (manifests)
    commands/         18 slash commands (loom: namespace)
    agents/           3 read-only subagents dispatched by commands
    skills/           loom-core + phase/gate/method skills, each with SKILL.md
    scripts/loom/     6 stdlib-only Python gate/generator scripts
    init-assets/      loom.yaml + seed ADR, copied into target projects by /loom:init
    docs/recipes/     the retired TDD machinery, documentation only — never executed

There is deliberately no `hooks/` directory: the only hook Loom ever shipped
guarded implementation roles, and Loom no longer implements.

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
  phases, and the `engine:` profile (which SDD engine, and where its constitution
  and spec directory live). Scripts read config from it; don't duplicate those
  values elsewhere. Engine-specific knowledge belongs in that profile, never in
  script code — chasing four vendors' file layouts in Python is the fastest-rotting
  thing this repo could own.
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
  `description:` (state who dispatches it, e.g. *"Dispatched by /loom:harvest"*),
  `tools:` (comma-separated).
- Tool convention: **every agent is read-only** — `Read, Grep, Glob, Bash`. All
  three (challenger, reviewer, harvester) analyse and report; the orchestrating
  session materializes their findings into documents. No `model:` field is used,
  and no agent gets `Write`/`Edit`: a write-capable agent here would mean Loom is
  producing something it should have handed to the engine.
- Body is a plain-prose role and output contract.

### Skills (`skills/<name>/SKILL.md`)
- Frontmatter fields: `name:` (matches directory) and `description:` only.
- **Descriptions are command-scoped, not free-text triggers.** Every Loom skill
  is loaded by name from its paired command (`commands/x.md` says *"Use the
  `loom-x-phase` skill"*), so the description does not need to match the phrases
  a user might type — it should open with *"Invoked by the /loom:x command to
  …"*, state what the skill does, and name the phase boundaries (run after X,
  before Y). Do NOT add pushy *"use whenever the user says '…'"* trigger lists:
  they don't help command-driven loading and cause the skill to mis-fire on
  free-text that belongs to a sibling (imagine vs intake) or an unrelated
  installed skill (review-gate vs a generic PR `review`). `loom-core` is the one
  skill with no paired command — its description states its read-first substrate
  role instead.
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
  resolves; `QS/DRV/BR/track` table rows count as definitions); `--refs <id>`
  reverse index. Skips files opening with the `<!-- GENERATED` marker — a
  generated file restates IDs defined elsewhere, so scanning it would report
  every projected ID as a duplicate.
- `adr_scan.py` — ADR lifecycle validator (status vocab, body/frontmatter
  agreement, supersedes symmetry); `--revisit` audits triggers and lists `BR-*`
  rules whose calendar `review_by` is due; `--framing`
  adds opt-in strict checks used at /loom:consolidate (accepted one-way ADR
  must cite DRV-* and QS-* and declare decision_mode; every QS in
  solution-strategy.md maps to an ADR or convention; a `verification: SPIKE-*`
  claim must resolve to a real, approved spike; no accepted one-way ADR rests on
  a `confidence: guessed` driver without a `revisit_when` trigger).
- `roadmap_gen.py` — generates `docs/roadmap/ROADMAP.md` from epic frontmatter;
  validates the epic dependency DAG is acyclic.
- `compile.py` — projects the knowledge layer into the engine's files per the
  `engine:` profile: the constitution (vocabulary, anti-goals, `BR-*` rules,
  accepted-ADR digest, ruled-out decisions, conventions, structural boundaries)
  and, with `--epic`, that epic's seed spec from its approved task specs.
  `--print` shows without writing; `--check` gates on missing/stale output.
  Generated content carries no timestamp **on purpose** — a date in the body would
  make `--check` report every output stale the day after it was written.

### Generated files
Anything a script writes opens with `<!-- GENERATED by scripts/loom/<x>.py — do
not edit ... -->` on line 1 (`INDEX.md`, `ROADMAP.md`, everything `compile.py`
emits). The marker is load-bearing, not decorative: `link_check.py` and
`index_gen.py` skip files that carry it. A new generator must emit it.

## Testing changes to the plugin

There is **no test suite or CI in this repo** — nothing here executes a consuming
project's tests any more. To exercise a change:

1. Sanity-run edited scripts directly, e.g.
   `python3 scripts/loom/link_check.py --help` and against a project's `docs/`.
   For `compile.py`, scaffold a throwaway `docs/` tree with a glossary, an
   accepted and a rejected ADR, a RULES row and one approved task, then check the
   three things a mechanical projection gets wrong: `--print` output, `--check`
   passing immediately after a write (idempotence), and `--check` failing when a
   source document changes.
2. Install the plugin locally and drive the affected command end-to-end:
   `/plugin marketplace add /Users/z003pz4w/personal/loom` then
   `/plugin install loom@loom`. Reload Claude Code to re-read the marketplace.
3. For phase/skill changes, run the relevant `/loom:*` command in a scratch
   project scaffolded via `/loom:init`.

## Releasing

- Bump `version` in `.claude-plugin/plugin.json` on any user-visible change.
- **Always update `CHANGELOG.md` in the same commit as the change** — it is the
  human-facing record of every user-visible change. Follow the existing
  [Keep a Changelog](https://keepachangelog.com) format: add (or append to) an
  entry under a `## [<new-version>]` heading with the release date, grouped into
  Added / Changed / Fixed / Removed. Note a `scripts` bump explicitly when
  `scripts/loom/*` changed. A version bump without a matching changelog entry is
  an incomplete release.
- **Tag each release** once committed: `git tag -a v<version> -m "..."` then
  `git push origin --tags`, so the `CHANGELOG.md` compare links resolve.
- **Version skew to be aware of:** `plugin.json` `version` (currently `0.20.0`)
  tracks the *plugin package*, while `init-assets/loom.yaml` carries its own
  `version`/`scripts_version` (currently `0.10`/`0.10.0`) tracking the *scaffolded
  framework/scripts*. These are intentionally independent — bump each for changes
  to its own surface. Bump `scripts_version` in `init-assets/loom.yaml` when
  `scripts/loom/*` change, since consuming projects re-sync via
  `/loom:init --refresh`.
- Install/marketplace names are both `loom`, so the install id is `loom@loom`
  (`<plugin>@<marketplace>`). Keep README install instructions in sync.
