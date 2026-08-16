---
name: loom-core
description: The shared substrate every loom-*-phase, -gate, and -method skill reads before doing its work — slug-based naming grammar, document status model, ADR lifecycle, frontmatter schema, open-question lifecycle, file layout. Consult it when authoring or validating any Loom document under docs/ (vision, glossary, ADR, spike, epic, design doc, task); the Loom commands load it by name, so it need not auto-trigger on free-text.
---

# Loom core conventions

Loom is the **knowledge layer** of a docs-first workflow: documents are the
source of truth, and code — written by an external SDD engine — follows them.
Loom itself writes no plan, no test, and no production code; what it produces is
knowledge in checkable form, up to and including the task spec the engine
consumes (see the handoff seam below). Every phase skill (loom-imagine-phase,
loom-skeleton-phase, loom-consolidate-phase, ...) builds on the conventions
defined here.

## The handoff seam (what Loom does not do)

Loom stops at the spec. Knowing exactly where it stops is what keeps it from
competing with the engine over "how we code" — two sources of truth on that
question is strictly worse than either one alone.

| Loom owns | The engine owns |
|---|---|
| glossary, drivers, rules, quality scenarios | the plan, the step order |
| decisions and their reasons (ADR lifecycle) | tests and the code |
| contracts, invariants, package boundaries | diff review, refactoring |
| the task `## Spec` — behavior, acceptance, out of scope | how the behavior is achieved |

Consequences that bind every skill here:

- **Never prescribe internals.** A Loom document names behavior, contracts and
  glossary terms; it does not name source files, functions, or a build order.
  The one exception is a contract file, which IS the interface.
- **`rigor: full | light` is advice, not a mode.** It tells the engine the cost
  of being wrong (public contract / domain invariant / more than one package →
  `full`). Loom no longer runs a ceremony for it; the one it used to run is kept
  as a recipe in `docs/recipes/anti-cheating-tdd.md`.
- **The seam is bidirectional.** `/loom:compile` pushes the knowledge layer into
  the engine's own files; `/loom:harvest` reads back what the engine decided and
  materializes the facts. A task with `handoff:` set and `harvested: false` is
  work whose facts are still missing from the docs — the successor to the old
  "unfinished task" signal.
- **Code is evidence, not authority.** When code and an `approved` document
  disagree, the document is the bug to fix or the decision to supersede — never
  something to quietly work around. Harvest raises it as a blocking OQ; it does
  not edit the document to match the code.

## Identity and naming (slugs, never sequential numbers)

Every artifact has a unique, immutable, meaning-bearing slug ID.
**ID = filename without extension.** kebab-case, 3–6 words, drop stop-words.
Sequential numbers are forbidden: they require a central counter (merge conflicts
between parallel agents) and carry no meaning at the reference site.

Naming grammar by type:

| Type | Grammar | Example |
|---|---|---|
| ADR | decision as a claim (verb phrase) | `ADR-use-questdb-for-timeseries` |
| Epic | business capability (noun phrase) | `epic-billing-analytics` |
| Use case | actor + action | `UC-trainer-logs-workout` |
| Spike | question / comparison | `SPIKE-questdb-vs-timescale-ingest` |
| Track | workstream in a design doc | `track-billing-api` |
| Task | package + change | `TASK-billing-add-vat-rates` |
| OQ | topic slug | `OQ-vision-multi-tenancy` |
| Quality scenario | topic slug | `QS-ingest-sustained-load` |
| Driver (fact) | fact slug | `DRV-peak-ingest-rate` |
| Business rule | rule slug | `BR-tonnage-rounding` |

ADR name test: it must read as an ANSWER, not a topic.
`ADR-database-choice` — wrong (topic). `ADR-use-postgres-for-billing` — right.

Command/skill naming convention (slash-picker collision safety): commands and
skills share the `/` namespace, so they must never share a name. A command is a
verb entry point (`/loom:imagine`); its skill carries the same name plus a role
suffix: `-phase` for lifecycle phases (loom-imagine-phase), `-gate` for gates
(loom-review-gate), `-method` for utilities (loom-spike-method). `loom-core`
has no paired command, so it takes no suffix.

Epic ID exception: an epic is a bundle directory `epics/epic-<slug>/` — the
directory carries the slug; `epic.md` frontmatter `id:` equals the directory
name; `design.md` takes `id: epic-<slug>-design`.

Rules:
- **Immutability**: once an ID is referenced anywhere, it never changes. If the
  name became a lie, that is a superseding document with a new name, not a rename.
- Rare legitimate renames: keep the old ID in frontmatter `aliases: []` — aliases
  stay globally unique and resolvable forever.
- Reference integrity is enforced by `scripts/loom/link_check.py` (uniqueness of
  all IDs + aliases; every `ADR-* / UC-* / SPIKE-* / TASK-* / OQ-* / epic-*`
  mention in docs must resolve; QS-*, track-* and DRV-* table rows count as definitions).

## File layout

```
docs/
├── loom.yaml                 # framework config (paths, phases, status vocabularies)
├── product/                  # VISION.md, GLOSSARY.md, ASSUMPTIONS.md, DRIVERS.md, RULES.md, use-cases/
├── domain/                   # event storming notes, C4 models (.dsl / mermaid)
├── adr/                      # global ADRs: ADR-<slug>.md
├── spikes/                   # SPIKE-<slug>.md
├── architecture/             # quality-requirements, building-blocks, solution-strategy
├── conventions/              # golden-path rules inherited by every package
└── roadmap/
    ├── ROADMAP.md            # generated index + dependency DAG
    └── epics/epic-<slug>/
        ├── epic.md
        ├── design.md         # includes tracks table (track-<slug> rows)
        ├── adr/              # epic-scoped ADR deltas
        ├── contracts/        # OpenAPI/AsyncAPI/proto — source of truth
        └── tasks/TASK-<slug>.md
```

Everything above is authored. Everything the engine reads is **generated** by
`/loom:compile` into the paths named in `loom.yaml` `engine:` — outside `docs/`,
opening with a `<!-- GENERATED ... do not edit -->` marker, and never edited by
hand: a fix belongs in the source document, and the next compile would overwrite
it anyway. The generated tree is not part of the knowledge layer; deleting it and
recompiling must lose nothing.

## Frontmatter schema

```yaml
---
id: epic-billing-analytics   # must equal filename without extension
status: draft                # see status vocabularies below
owner: human                 # human | agent | pair
updated: 2026-07-06
aliases: []                  # former IDs after a legitimate rename
---
```

Optional keys by type: `depends_on: []` (epics, tasks), `packages: []` (tasks),
`criticality: must|should|could|wont` (epics), `appetite: <duration>` (epics).

Handoff keys (tasks only, written at the seam — see above): `handoff: <engine>`
when `/loom:compile` shipped the spec, `landed: <PR|commit>` when the engine
closed it, `harvested: true|false` once `/loom:harvest` folded its facts back.
They track the round trip, not the document's own review status — a task can be
`approved` and unharvested, and that combination is exactly what /loom:status
surfaces.

## Status vocabularies

**Regular documents** (vision, epics, design docs, tasks, spikes):
- `draft` — being written; downstream phases MUST NOT consume it.
- `in-review` — frozen for review; only OQ resolutions may change content.
- `approved` — consumable by the next phase. Requires zero open blocking OQs.
- `superseded` — kept for history; add `superseded_by: <id>`.

**ADRs have their own lifecycle** (see next section):
`proposed → accepted | rejected`, then `accepted → deprecated | superseded`.

A phase may only read `approved` (or `accepted`) documents of the previous phase.

## ADR lifecycle

Template: `templates/adr.md` in this skill. Key rules:

- **Status is visible in the body**: the line right under the H1
  (`Status: <value> · reversibility: ... · verification: ...`) mirrors the
  frontmatter for human readers. Update BOTH on every transition —
  `adr_scan.py` fails on mismatch or a missing body line.

- **Rejected is not trash.** A rejected ADR is kept forever — "why we did NOT
  pick Kafka" is a ready-made negative constraint for future sessions.
- **Accepted is immutable.** After acceptance only metadata (status, links) and
  append-only `## Addenda` entries may change. Changing the decision = a new
  superseding ADR linked both ways (`supersedes` / `superseded_by`).
- **Decisions cite facts**: the Context section names the `DRV-*` drivers the
  decision stands on. Hitting a fork whose deciding fact is missing from
  DRIVERS.md: for a one-way door — STOP, raise a blocking OQ to the human,
  record the answer as a driver, then decide; guessing is forbidden. For a
  two-way door — proceeding is allowed, but the guess is recorded in
  DRIVERS.md as `confidence: guessed` first. `adr_scan.py` warns on accepted
  one-way ADRs citing no drivers.
- **Never open a technology fork with a recommendation.** Protocol:
  (1) check DRIVERS.md `## Tech posture` — the fork may already be constrained
  or decided; (2) if not, ask the human the decision mode in ONE question:
  `decided` (already chosen — record as driver) / `framed` (constraints given,
  options within them) / `menu` (2–3 options with trade-offs against THIS
  project's drivers, recommendation only on explicit request) / `delegated`
  (agent decides — two-way doors only; one-way still requires human accept);
  (3) record the mode in ADR frontmatter `decision_mode:`. A recommendation
  offered before the mode was asked anchors the human — that is the failure
  this protocol exists to prevent.
- **One-way acceptance requires a challenge.** Before accepting any one-way
  ADR, the review gate dispatches the `loom-challenger` agent (fresh context);
  its findings are materialized as OQs and resolved first.
- **Verification is proportional to reversibility** (`reversibility` field):
  - `two-way` (cheap to undo) → `verification: judgment` is acceptable.
  - `one-way` (expensive to undo: language, DB, data schema, inter-package
    protocol) → requires material evidence: the walking skeleton
    (`verification: skeleton` — the primary path), `verification: SPIKE-<slug>`,
    benchmark, prototype, or a justified external reference.
- **Rot by triggers, not by calendar**: `revisit_when:` lists the assumptions
  under which the decision holds; the audit phase scans these. Use a calendar
  `review_by` only for decisions tied to the external world (licenses, vendors).
- **Enforce what is enforceable** (`enforced` field): if a consequence can be
  checked automatically, it MUST become a lint/arch-test rule that references the
  ADR ID in a comment; `code-tag` means the implementing code carries the ADR ID.
- `scripts/loom/adr_scan.py --gate` validates lifecycle invariants in CI.

Spike vs ADR: a spike ends with a **recommendation** (evidence), an ADR fixes a
**decision**. Spikes are cited from the ADR Options section, never merged into it.

## Business rules (BR-*)

`docs/product/RULES.md` holds the rules the system is OBLIGED to reproduce —
formulas, thresholds, rounding, boundaries, tie-breaks, period edges. They are
not choices; they are given. This is the file that closes the third failure mode
Loom exists for: an agent inventing a plausible formula, and nobody noticing at
review because it looks right.

One table row per rule: **ID | rule | bounds | source | review_by**.

```markdown
| BR-tonnage-formula | Tonnage = Σ(weight × reps) over working sets | warm-ups excluded; supersets counted separately | product owner, 2026-03-11 | |
| BR-vat-rate-standard | Standard VAT is 20%, rounded up to the cent | applies to the invoice total, not per line | UK VAT Act §2(1) | 2027-01-01 |
```

- **Bounds are the rule.** Most hallucinated arithmetic hides at the edges, not in
  the main formula: state rounding and where it is applied, inclusive vs exclusive
  on boundaries, tie-break order, behavior at zero / empty / negative, timezone
  and period boundaries, and precedence when two rules collide.
- **`source` is not decoration.** It is the only thing separating a rule from a
  guess. Name who or what says so — a person and a date, a regulation with its
  section and edition, a contract. A rule whose source is "the engine chose it"
  during `/loom:harvest` is recorded as `confidence: guessed` with what would
  confirm it — never presented as settled.
- **`review_by` for rules with an external source.** Standards and regulations get
  revised, and unlike a decision there is no `revisit_when` condition to watch —
  the trigger is a calendar one. `/loom:audit` scans these; a product built "to the
  standard" is compliant only until its next edition, and an undated citation makes
  that invisible.
- **Never infer a missing rule.** A gap here is a blocking OQ to the human, at any
  reversibility — a wrong threshold silently corrupts data and is discovered by a
  user, not by a test. This is stricter than the driver protocol, where a two-way
  door may proceed on a labelled guess.

Where a fact belongs — the boundary these four confuse most often:

| If it is… | it is | test |
|---|---|---|
| a measured fact about the world, input to decisions | `DRV-*` | it describes the territory, not our behavior |
| a measurable demand on quality | `QS-*` | it is about speed / reliability, not about a result |
| our choice, with alternatives and a reversibility | `ADR-*` | it could be re-decided; a BR has no options, only a source |
| a "must never" statement about state | invariant | it forbids, it does not compute |
| how we write code | `conventions/*` | lintable, no domain content |

Deciding question: **could this be re-decided?** Yes → ADR. No, and we measured it
→ DRV. No, and we are obliged to reproduce it → BR.

## Open questions (OQ)

Every document may contain an `## Open questions` section, one checklist line per
question. OQ IDs are slugs too — `OQ-<doc-topic>-<question-topic>`:

```markdown
## Open questions
- [ ] OQ-vision-multi-tenancy (blocking): Do we support multi-tenant from day one?
- [x] OQ-vision-payment-provider: Which PSP? → resolved: ADR-use-stripe-for-payments
```

Rules:
- `(blocking)` marks questions that gate the `approved` transition.
- A resolved OQ is checked `[x]` and MUST name its materialization after
  `→ resolved:` — an ADR id, a section edit, or `wontfix (<reason>)`.
- `scripts/loom/oq_scan.py --gate <file>` exits non-zero while blocking OQs are open.

## Writing rules for all Loom documents

- Use glossary terms verbatim; new domain terms go to GLOSSARY first.
- Anti-goals are first-class: every vision/epic/design states what it will NOT do.
- Prefer short declarative sections over prose walls; documents are prompts.
- Never edit `status` and content in the same commit, except draft-phase work.
- Generated files (ROADMAP.md, docs/INDEX.md) are never edited by hand;
  run `scripts/loom/index_gen.py` and `scripts/loom/roadmap_gen.py` instead.
