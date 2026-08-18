# Changelog

All notable changes to the Loom plugin are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Two version numbers move independently (see `CLAUDE.md` → Releasing):
- **plugin** — the `version` in `.claude-plugin/plugin.json` (the package).
- **scripts** — `scripts_version` in `init-assets/loom.yaml`, bumped only when
  `scripts/loom/*` change; consuming projects re-sync via `/loom:init --refresh`.

## [0.22.1] — 2026-08-18

### Removed
- `skills/loom-imagine-phase/templates/glossary.yaml`: an unused template left
  over from an earlier design where a YAML source generated `GLOSSARY.md`. No
  generator script ever existed for it, and the skill's interview protocol
  writes directly to `GLOSSARY.md` — the table row in `SKILL.md` claiming it
  came "from `templates/glossary.yaml`" was stale and now says "written
  directly (no template)".

## [0.22.0] — 2026-08-17

Unifies Gherkin step phrasing across use cases and requires non-happy-path
coverage, so the engine writes one step definition per fact instead of one
per rewording.

### Added
- `docs/product/STEPS.md` (`templates/steps.md` in `loom-imagine-phase`): the
  canonical Given/When/Then phrase catalog, `STEP-*` rows with `{placeholder}`
  slots. Every step in every `UC-*.md` must resolve to a row here.
- `use-case.md` template: each Extension is now tagged `[alternate]` /
  `[error]` / `[boundary]`; at least one `[error]` or `[boundary]` extension
  is required per use case.
- `scripts/loom/gherkin_lint.py --gate` — flags Gherkin steps that don't
  resolve to a STEPS.md phrase, flags near-duplicate rewordings of an
  existing phrase (word-overlap heuristic, no fuzzy-match false negatives on
  differently-sized `{placeholder}` fills), and flags use cases with no
  `[error]`/`[boundary]` extension.

### Changed
- `loom-imagine-phase` and `loom-core` skills document `STEP-*` as a naming
  type and `STEPS.md` as an imagine-phase artifact; exit criteria now include
  `gherkin_lint.py --gate`.

## [0.21.0] — 2026-08-17

The use case template now follows Cockburn's "fully dressed" standard instead
of a homegrown one, and actors become a first-class artifact with UML-style
relationships between use cases.

### Added
- `ACTOR-*` as a first-class ID type: `docs/product/ACTORS.md`
  (`templates/actors.md` in `loom-imagine-phase`), one table row per actor,
  referenced from `UC-*.md` frontmatter (`primary_actor`, `secondary_actors`).
- `use-case.md` template rewritten to Cockburn fully-dressed structure
  (preconditions, trigger, minimal/success guarantees, numbered extensions)
  while keeping the Main success scenario and each extension in Gherkin —
  unchanged from `CONCEPT.md`'s "closes: непонимание сценариев → Gherkin" form.
- `includes`/`extends` frontmatter fields on `UC-*.md` for UML
  `<<include>>`/`<<extend>>` relationships between use cases.
- `scripts/loom/uc_diagram_gen.py` — generates `docs/product/UC-DIAGRAM.md`,
  a Mermaid flowchart rendering of the actor↔use-case UML diagram, and
  validates that every actor/includes/extends reference resolves.

### Changed
- `link_check.py`: `ACTOR-*` mentions now resolve as references, and
  `ACTOR-*` table rows count as definitions (same treatment as `QS-*` /
  `DRV-*` / `track-*`).
- `loom-imagine-phase` and `loom-core` skills document the new artifact and ID
  type (file layout, naming grammar, exit criteria).

## [0.20.0] — 2026-08-16

Loom stops implementing. It is now the knowledge layer only: it produces
documents and task specs, and an external SDD engine (Spec Kit, Kiro, OpenSpec,
BMAD, a plain agent harness) writes the plan, the tests and the code. Two new
commands are the seam — `compile` projects the knowledge layer into the engine's
own files, `harvest` reads back what the engine decided by itself. Rationale in
`CONCEPT.md` (§2 boundaries, §5 the seam, §10 what was dropped).

### Removed
- `/loom:implement` and `loom-implement-phase` — the orchestrated TDD engine.
- Agents `loom-planner`, `loom-test-author`, `loom-implementer`,
  `loom-code-reviewer`. Every remaining agent is read-only; no Loom agent writes
  code or tests.
- `scripts/loom/verify_red.py`, `verify_green.py`, `guard_file_roles.py` and
  `hooks/hooks.json` — the plugin now ships no hooks at all.
- `test_command` and `test_globs` from `init-assets/loom.yaml`; `.loom/` role
  markers and the `changes/` changelog-fragment convention.
- `## Plan`, `## Test-change log` and `## Review` from the task template. The task
  file is its `## Spec` — behavior, acceptance, contracts, out of scope.

### Added
- `/loom:compile` + `loom-compile-phase` + `scripts/loom/compile.py`: assembles
  the engine's constitution (vocabulary → anti-goals → binding rules → decisions
  in force → ruled out → conventions → structural boundaries) and, with `--epic`,
  a seed spec from that epic's approved task specs and contracts. `--print`,
  `--check` (gates on stale or missing output). Refuses to hand off a spec with
  open blocking OQs.
- `engine:` block in `init-assets/loom.yaml` (`name`, `constitution`, `spec_dir`)
  — engine-specific layout is configuration, never script code. Profiles for
  Spec Kit / Kiro / OpenSpec / plain harnesses are listed in the skill.
- `/loom:harvest` + `loom-harvest-method` + the read-only `loom-harvester` agent:
  fresh-context reading of the engine's diff and artifacts, classifying findings
  into term / rule-or-number / decision / surface / contradiction / scope and
  routing each to the one document that owns it. A contradiction becomes a
  blocking OQ on the document — never a document edited to match the code.
- `BR-*` domain rules in `docs/product/RULES.md` (template + `loom-core` section):
  formulas, thresholds, rounding and boundaries the system is obliged to
  reproduce, with bounds, a named source, and `review_by` for external sources.
  Authored in `/loom:requirements`; `link_check.py` resolves `BR-*` references and
  treats table rows as definitions; `adr_scan.py --revisit` lists rules whose
  review date is due; `/loom:audit` asks whether the source was revised.
- Task frontmatter `handoff:` / `landed:` / `harvested:`, surfaced as a `Seam`
  column in `docs/INDEX.md` and by `/loom:status` and `/loom:prime`. A task
  handed off and unharvested is the successor to the old unfinished-task signal.
- `templates/skeleton-brief.md` — what each proposed ADR must demonstrate, layers
  that must be traversed, the `Faked:` contract, and the falsification criterion.
- `docs/recipes/anti-cheating-tdd.md` — the retired role-asymmetry / verify-red /
  file-guard machinery as a portable recipe, with the three original scripts. Not
  executed by the plugin; documented because SDD engines ship nothing like it.

### Changed
- `loom-core` gained a handoff-seam section (what Loom owns vs the engine) and a
  `BR-*` section with the DRV / QS / ADR / invariant / convention boundary table.
  `rigor: full | light` is now an advisory signal about the cost of being wrong,
  not a mode Loom executes.
- `loom-design-phase` ends at an engine-ready spec: acceptance criteria with
  numbers, contracts named, and no internal file names or step order.
- `loom-skeleton-phase` writes a brief and interprets the result; the engine
  builds the slice. Evidence that ran through something on the `Faked:` list does
  not verify an ADR. Package `SKILL.md` files are now written *before* the build,
  as the engine's constraint rather than a record of what it did.
- `loom-spike-method` absorbs the probe genre explicitly: fidelity axis, cheapness
  ladder (napkin → mock → single-file script → throwaway app), a mandatory
  `Faked:` list, and quarantine rules. Probes get no tests, review or conventions
  by design.
- `loom-consolidate-phase` and `loom-audit-phase` re-project into the engine after
  changing decisions — a deprecated decision left in the constitution is worse
  than an undocumented one, because the engine actively obeys it.
- `loom-intake-method` takes harvested findings as a second caller alongside the
  human, and routes tasks to `/loom:compile` instead of `/loom:implement`.
- `loom-requirements-phase` owns both kinds of number: `QS-*` scenarios and `BR-*`
  rules.
- Ships `scripts_version` `0.10.0` (`loom.yaml` `version` `0.10`). `/loom:init
  --refresh` now reports project-local `scripts/loom/*.py` the plugin no longer
  ships, since a stale gate script reads config keys that are gone.

### Fixed
- `link_check.py` and `index_gen.py` skip files opening with the `<!-- GENERATED`
  marker; without this, compiled projections would report every projected ID as a
  duplicate definition.
- `/loom:prime` no longer suggests the pre-slug `E-XXX` epic form.
- `loom-reviewer` pointed at a kit-era path (`.claude/skills/loom:review-gate/`)
  instead of the `loom-review-gate` skill.

## [0.19.0] — 2026-07-22

### Changed
- `loom-technology-phase` gained an explicit `## Inputs (gate)` section (it was
  the only phase skill without one), listing the approved solution-strategy,
  building-blocks, quality-requirements, and DRIVERS it consumes.
- `loom-requirements-phase` gate now lists the approved first-slice epic it
  consumes (its procedure already read the epic's definition of done), closing
  the roadmap → requirements handoff.
- Stopped presenting `approved-as-hypothesis` as if it were a status value —
  loom-core's status vocabulary has no such entry. Architecture/skeleton/
  consolidate now say the documents are `approved` with the "hypothesis worth
  testing" meaning carried as prose.
- `templates/building-blocks.md` and the architecture skill now say the `Key ADRs`
  column and forbidden-dependency ADR refs are left empty until /loom:consolidate
  (no ADRs exist during architecture), resolving a template-vs-skill contradiction.
- Removed the empty `templates/` directory under `loom-consolidate-phase` (cruft).
- Trimmed a duplicated "measures, not adjectives" restatement in requirements.

## [0.18.0] — 2026-07-22

### Changed
- Restructured the implement-phase Cycle into three labelled parts — Setup (once)
  → Per-step loop → Closure (once) — so control flow (which steps run once vs per
  step) is unambiguous.
- **Specified the `rigor: light` path, which was previously ambiguous.** It now
  has its own subsection stating that a single agent does classic TDD, that
  `.loom/role` is cleared (no marker → the file-role guard allows all edits), and
  that this deliberately trades the role guard for the commit trail: the mandatory
  RED-before-green commit sequence, the verify scripts, and the fresh-context
  reviewer carry the integrity the role split would otherwise provide. A light
  task that turns out to touch a contract or domain invariant must escalate to
  `full`. This closes a gap where the anti-cheating machinery silently collapsed
  in light mode without saying what replaced it.
- Surfaced the code-reviewer's `APPROVED` / `BLOCKED (n)` verdict in Closure and
  normalized closure gate commands to the fully-qualified `python3
  scripts/loom/…` form used elsewhere in the skill.

## [0.17.0] — 2026-07-22

### Changed
- Rewrote all 14 skill `description:` fields to be **command-scoped** rather than
  free-text trigger lists. Every Loom skill is loaded by name from its paired
  command, so pushy "use whenever the user says …" phrasing did not help loading
  and caused mis-fires: `loom-imagine-phase` vs `loom-intake-method` both claimed
  free-text idea prompts, and `loom-review-gate`'s "review any document" collided
  with an unrelated installed PR-`review` skill. Descriptions now open with
  "Invoked by the /loom:x command to …" and name the phase boundaries;
  `loom-review-gate` explicitly excludes code diffs and GitHub PRs; `loom-core`
  states its read-first substrate role.
- Documented the command-scoped description rule in CLAUDE.md's skill authoring
  conventions (replacing the earlier "make the description trigger-oriented"
  guidance that produced the collisions).

## [0.16.0] — 2026-07-22

### Added
- `/loom:prime` now ends with a "resume here" line — the single most likely next
  action (a task left in-review or with an empty `## Plan`, the nearest open
  blocking OQ, or the command the phase sequence implies) — so a returning session
  knows where it stopped. It also runs `oq_scan.py` as part of the bootstrap.
- Review-gate pre-flight: before spending any human review time, `link_check.py`
  runs on the document and a broken reference or duplicate ID stops the review as
  not-ready (authoring work), rather than being reviewed around.
- `adr_scan.py --framing` now also fails when an accepted one-way ADR stands on a
  `confidence: guessed` driver with no `revisit_when` trigger — the guessed-driver
  sweep that consolidate always described is now enforced, not just advised.

### Changed
- **scripts** `0.9.2` → `0.9.3` (`adr_scan.py` changed).

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

[0.20.0]: https://github.com/shpakv/loom/compare/v0.19.0...v0.20.0
[0.19.0]: https://github.com/shpakv/loom/compare/v0.18.0...v0.19.0
[0.18.0]: https://github.com/shpakv/loom/compare/v0.17.0...v0.18.0
[0.17.0]: https://github.com/shpakv/loom/compare/v0.16.0...v0.17.0
[0.16.0]: https://github.com/shpakv/loom/compare/v0.15.0...v0.16.0
[0.15.0]: https://github.com/shpakv/loom/compare/v0.14.0...v0.15.0
[0.14.0]: https://github.com/shpakv/loom/compare/v0.13.0...v0.14.0
[0.13.0]: https://github.com/shpakv/loom/compare/v0.12.0...v0.13.0
[0.12.0]: https://github.com/shpakv/loom/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/shpakv/loom/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/shpakv/loom/compare/v0.9.1...v0.10.0
[0.9.1]: https://github.com/shpakv/loom/releases/tag/v0.9.1

