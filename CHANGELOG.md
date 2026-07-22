# Changelog

All notable changes to the Loom plugin are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Two version numbers move independently (see `CLAUDE.md` → Releasing):
- **plugin** — the `version` in `.claude-plugin/plugin.json` (the package).
- **scripts** — `scripts_version` in `init-assets/loom.yaml`, bumped only when
  `scripts/loom/*` change; consuming projects re-sync via `/loom:init --refresh`.

## [0.15.0] — 2026-07-22

### Added
- Explicit, mandatory challenge triggers in the review gate: a `loom-challenger`
  pass is now required before approval not only for any one-way ADR, but also for
  an epic with `criticality: must` and a design doc that introduces a new external
  contract — the high-cost-of-being-wrong cases where the author's own context is
  the liability.
- Explicit, mandatory spike triggers in the technology phase: a `/loom:spike` must
  precede a proposed one-way ADR when the fork is one-way between close options
  decided by a measurable difference, when the deciding `QS-*` is one the walking
  skeleton will not exercise, or when the decision rests on a `confidence: guessed`
  driver that would flip the choice.
- `adr_scan.py --framing` now also verifies that an accepted ADR whose
  `verification: SPIKE-<slug>` points at a spike that actually exists and is
  approved — evidence claimed must be evidence that exists.

### Changed
- Updated the `loom-challenger` agent description to state the broadened mandatory
  triggers.
- **scripts** `0.9.1` → `0.9.2` (`adr_scan.py` changed).

## [0.14.0] — 2026-07-22

### Added
- `/loom:intake` — a triage front door for work arriving on an already-initialized
  project. A lightweight router (no gated artifacts of its own) that sizes a bug,
  change, or new capability and points at the smallest phase that honestly handles
  it, instead of forcing every change through a full `/loom:imagine`. When several
  routes fit, it selects the highest authority so a vision-level change is never
  smuggled in as a task.

### Changed
- Promoted `intake` from `phases.planned` to `phases.implemented` in
  `init-assets/loom.yaml`.

## [0.13.0] — 2026-07-22

### Added
- Upstream-defect escalation (code → docs) in the implement phase. When a subagent
  finds that the spec, design, ADR, or contract is itself wrong — not just a
  mis-written test — the orchestrator now STOPs the red/green cycle, raises a
  blocking OQ on the owning document, and routes to the phase that owns it
  (`/loom:design`, a superseding ADR via `/loom:consolidate`, `/loom:audit`, or
  `/loom:review`) instead of building around the defect.

### Changed
- `loom-planner` now emits an `UPSTREAM-DEFECT` finding at plan time; `loom-implementer`
  labels objections as test-wrong (local, handled by the test-change protocol) vs
  document-wrong (escalated). The implement command surfaces the new protocol.

## [0.12.0] — 2026-07-22

### Added
- `/loom:audit` — the backward pass that closes the learning loop. Composes existing
  scripts into a feedback event: `adr_scan.py --revisit` checks each accepted ADR's
  revisit triggers, `link_check.py --refs DRV-<slug>` finds accepted ADRs standing on
  unconfirmed guessed drivers, and `oq_scan.py` surfaces stale open questions. Drift is
  materialized as blocking OQs and handed to the human, ranked by severity; audit never
  resolves anything itself.

### Changed
- Promoted `audit` from `phases.planned` to `phases.implemented`.
- `/loom:status` now nudges toward `/loom:audit` when a project has accepted ADRs.

## [0.11.0] — 2026-07-22

### Added
- ADR framing gate: `adr_scan.py --framing` (opt-in, combine with `--gate` for CI),
  run at `/loom:consolidate`. Enforces that decisions are framed by facts and targets
  before acceptance:
  - an accepted one-way ADR must cite both a driver (`DRV-*`) and a quality scenario
    (`QS-*`) — no untargeted one-way doors;
  - any one-way ADR must declare its `decision_mode` (decided | framed | menu | delegated);
  - every `QS-*` in `solution-strategy.md` must map to an ADR or a convention.

### Changed
- The prior "accepted one-way decision cites no drivers" warning is promoted to an
  error under `--framing` (unchanged as a warning under plain `--gate`).
- Wired the gate into the consolidate skill and command; the technology skill notes
  that one-way ADRs should already satisfy it.
- **scripts** `0.9.0` → `0.9.1` (`adr_scan.py` changed).

### Notes
- Default `adr_scan.py --gate` behavior is unchanged — backward-compatible for
  consuming projects. Template placeholder rows (`QS-{slug}`) are skipped.

## [0.10.0] — 2026-07-22

Reordered the lifecycle so that structure and quality requirements are settled
before any technology commitment, and technology decisions are proposed
hypotheses the walking skeleton verifies.

New route:
`prime → imagine → roadmap → requirements → architecture → technology → skeleton → consolidate → design → implement`

### Added
- `loom-requirements-phase` + `/loom:requirements` — promote proto-QS driver rows
  into testable quality scenarios (stimulus → response → measure) before architecture.
- `loom-architecture-phase` + `/loom:architecture` — building blocks and solution
  strategy as a draft hypothesis; names technology forks but chooses none.

### Changed
- Renamed `loom-technology-method` → `loom-technology-phase`: keeps posture-gathering
  as step 0, but its main job is now proposed ADRs per fork, framed by `DRV-*`/`QS-*`;
  nothing is accepted here.
- Reframed the skeleton phase: it now validates the proposed decisions and records
  evidence, rather than inventing ADRs in the moment.
- Slimmed the consolidate phase: it reconciles as-built vs as-intended and accepts
  ADRs on skeleton evidence; it no longer originates quality scenarios, building
  blocks, or the solution strategy.
- Moved templates to their originating phase (`quality-requirements.md` →
  requirements; `building-blocks.md`, `solution-strategy.md` → architecture); the
  solution-strategy template now maps each QS to a decision-to-be-made rather than an
  already-accepted ADR.
- Dropped stale phase numbering from command/skill descriptions; synced `loom.yaml`
  phases, `CLAUDE.md`, and `README.md`.

## [0.9.1] — 2026-07-20

The pre-existing baseline before the lifecycle rework above. This is the initial
published state of the plugin (early development moved the manifest version
`0.6.0` → `0.9.1` without intermediate releases).

### Added
- Initial Loom plugin: docs-first framework as a Claude Code plugin — slash commands
  (`loom:` namespace), dispatched subagents, phase/gate/method skills, the stdlib-only
  gate/generator scripts in `scripts/loom/`, the PreToolUse file-role guard hook, and
  the `init-assets/` scaffold copied into target projects by `/loom:init`. Ships
  `scripts_version` `0.9.0`.

### Fixed
- Removed the explicit `"hooks"` key from `.claude-plugin/plugin.json`; Claude Code
  auto-discovers `hooks/hooks.json`, and registering it explicitly caused the
  file-role guard hook to misbehave. Documented the auto-discovery in `CLAUDE.md`.

[0.15.0]: https://github.com/shpakv/loom/compare/v0.14.0...v0.15.0
[0.14.0]: https://github.com/shpakv/loom/compare/v0.13.0...v0.14.0
[0.13.0]: https://github.com/shpakv/loom/compare/v0.12.0...v0.13.0
[0.12.0]: https://github.com/shpakv/loom/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/shpakv/loom/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/shpakv/loom/compare/v0.9.1...v0.10.0
[0.9.1]: https://github.com/shpakv/loom/releases/tag/v0.9.1

