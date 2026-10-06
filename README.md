# Loom

**Shared product knowledge that survives people, AI sessions and technology changes.**

Loom is a plugin for **Claude Code, OpenAI Codex and GitHub Copilot CLI** that
helps you turn a product idea into reviewed requirements, business rules,
architecture decisions, contracts and task specifications. It keeps that
knowledge in version-controlled documents under `docs/`.

This repository contains the plugin: workflows, templates, document reviewers
and Python validation tools. Install it in your agent host, then initialize
Loom in the repository where you want to maintain your project's requirements.
That can be a dedicated requirements repository or the repository containing
your product.

Loom's deliverable is an approved body of project knowledge. Product code,
implementation plans, tests and code review belong to your development process
and happen outside Loom. There is no implementation or export-to-another-tool
step in its lifecycle.

## Why use it?

An AI assistant can write a plausible solution while losing the agreements that
make it the right solution. A new session may use different terminology, invent
a missing business rule or revisit a technology choice without knowing why it
was made.

Loom gives those agreements a durable home:

- **A shared vocabulary:** what domain terms mean, who uses the product and
  which scenarios matter.
- **Explicit scope and correctness:** goals, non-goals, measurable quality
  requirements and business rules with their sources and edge cases.
- **Decision history:** the options considered, the evidence available, who
  authorized the choice and when it should be reconsidered.
- **Connections between documents:** stable IDs link scenarios, rules,
  decisions, epics and tasks so a change can be traced to its consumers.
- **A way to resume work:** session bootstrap, status reports and open
  questions show what is settled and what needs attention next.

It is useful when several people or agents work on a product, work spans many
sessions, or getting a rule or interface wrong would be expensive. It also
requires upkeep: facts, decisions and affected documents need review as the
product changes.

## What does it create?

Initialization creates the document directories, `docs/loom.yaml`, a seed
`ADR-adopt-loom.md` decision and a local copy of `scripts/loom/*.py`. It preserves
existing documents. The product-specific content is written during the later
workflows, through conversation with you and document review.

The default layout grows into:

```text
docs/
├── loom.yaml                         # paths, statuses and decision policy
├── INDEX.md                          # generated document status index
├── product/
│   ├── VISION.md                      # problem, users, goals and non-goals
│   ├── GLOSSARY.md                    # shared domain vocabulary
│   ├── ACTORS.md                      # roles participating in use cases
│   ├── STEPS.md                       # reusable Given/When/Then phrases
│   ├── DRIVERS.md                     # facts and constraints behind decisions
│   ├── ASSUMPTIONS.md                 # unverified beliefs and how to check them
│   ├── RULES.md                       # binding business rules (BR-*)
│   ├── use-cases/UC-*.md              # scenarios, including errors and boundaries
│   └── UC-DIAGRAM.md                  # generated actor/use-case diagram
├── domain/                           # domain models, added when needed
├── architecture/
│   ├── quality-requirements.md        # measurable quality scenarios (QS-*)
│   ├── building-blocks.md             # responsibilities and allowed dependencies
│   └── solution-strategy.md           # how quality targets map to decisions
├── adr/ADR-*.md                       # architecture decision records
├── spikes/SPIKE-*.md                  # research questions and evidence summaries
├── changes/CHG-*.md                   # incoming requests and their disposition
├── conventions/                      # durable product and architecture conventions
└── roadmap/
    ├── ROADMAP.md                    # generated epic index and dependency graph
    └── epics/epic-<slug>/
        ├── epic.md                   # a business capability and its scope
        ├── design.md                 # contracts, data changes and workstreams
        ├── adr/                      # decisions specific to this epic
        ├── contracts/                # OpenAPI, AsyncAPI or protocol definitions
        └── tasks/TASK-*.md            # behavior and acceptance specifications

scripts/loom/                         # portable document checks and generators
```

Paths are configured in `docs/loom.yaml`. Approved project documents are the
source of truth for behavior, constraints and decisions; generated indexes
summarize those documents.

An **epic** groups a business capability. An **ADR** records a decision and its
reasons. A **driver** is a fact or constraint that informs a decision. An **open
question (OQ)** records an unresolved issue; it can block approval.

For example, for a studio booking product, Loom could record:

| Agreement | Where it lives |
|---|---|
| What “session”, “booking” and “cancellation” mean | `GLOSSARY.md` |
| A member books a session; a full session rejects the request | A `UC-*` use case |
| When cancellation is allowed, with the exact cutoff and its source | A `BR-*` row in `RULES.md` |
| The required booking latency at a stated concurrent load | A `QS-*` quality scenario |
| Why a storage technology was chosen and which alternatives lost | An `ADR-*` decision |
| The booking API and how to handle two requests for the last seat | A contract and a `TASK-*` specification |

The actual thresholds and rules come from the project's sources and authorized
decisions. A missing rule becomes a question to resolve.

## Installation

You need one supported agent host with plugin support and Python 3 for the
document checks. The checks use only the Python standard library; there are no
Python packages to install.

### Claude Code

Start Claude Code with `claude`, then enter these commands **inside the session**:

```text
/plugin marketplace add shpakv/loom
/plugin install loom@loom
```

See the [Claude Code plugin installation guide](https://code.claude.com/docs/en/discover-plugins)
for host installation and plugin management details.

### OpenAI Codex

Run in your **terminal**:

```bash
codex plugin marketplace add shpakv/loom
codex plugin add loom@loom
```

See [OpenAI's marketplace documentation](https://developers.openai.com/plugins/build/plugins#add-a-marketplace-from-the-cli)
for marketplace setup; `codex plugin --help` lists the commands in your CLI.

### GitHub Copilot CLI

Run in your **terminal**:

```bash
copilot plugin marketplace add shpakv/loom
copilot plugin install loom@loom
```

See the [GitHub Copilot CLI plugin installation guide](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing)
for host installation and plugin management details.

All three hosts use the same shared skills and document checks. Claude Code's
`/loom:*` commands are aliases for those workflows; in Codex or Copilot, ask for
the corresponding skill by name.

## Start a project

Open your agent in the repository that will hold the project documents.

In **Claude Code**, initialize Loom and describe your idea:

```text
/loom:init
/loom:imagine A booking tool for small studios where members reserve sessions.
```

In **Codex or Copilot**, use an equivalent prompt:

```text
Use the loom-init skill to initialize Loom in this repository.
Then use loom-imagine-phase for this idea: a booking tool for small studios
where members reserve sessions.
```

The imagine workflow interviews you one question at a time, captures your
terminology and writes the initial product documents. Review them as they become
ready. For example, in Claude Code:

```text
/loom:review docs/product/VISION.md
```

In Codex or Copilot, ask to use `loom-review-gate` on the same file. Resolve the
blocking questions before continuing to a phase that consumes that document.

### The lifecycle

Start each returning session with `prime` to restore context. For a new product,
the authoring route begins with `imagine`:

```text
prime → imagine → roadmap → requirements → architecture → technology → consolidate → design
```

| Claude Code command | Shared skill | Purpose and result |
|---|---|---|
| `/loom:prime` | [loom-prime-method](skills/loom-prime-method/SKILL.md) | Load the current agreements, questions and changes; report one next action. |
| `/loom:imagine` | [loom-imagine-phase](skills/loom-imagine-phase/SKILL.md) | Establish the problem, vocabulary, actors, 3–5 core use cases, drivers and assumptions. |
| `/loom:roadmap` | [loom-roadmap-phase](skills/loom-roadmap-phase/SKILL.md) | Identify business epics, their dependencies and the first small vertical slice. |
| `/loom:requirements` | [loom-requirements-phase](skills/loom-requirements-phase/SKILL.md) | Write measurable quality scenarios and sourced business rules before choosing a structure or stack. |
| `/loom:architecture` | [loom-architecture-phase](skills/loom-architecture-phase/SKILL.md) | Define responsibilities, boundaries and allowed/forbidden dependencies; record open technology choices. |
| `/loom:technology` | [loom-technology-phase](skills/loom-technology-phase/SKILL.md) | Propose technology decisions based on drivers, quality targets, team constraints and evidence. |
| `/loom:consolidate` | [loom-consolidate-phase](skills/loom-consolidate-phase/SKILL.md) | Record authorized decision outcomes, reconcile architecture with evidence and revisit assumptions and epic candidates. |
| `/loom:design epic-<slug>` | [loom-design-phase](skills/loom-design-phase/SKILL.md) | Specify one approved epic: contracts first, then workstreams and tasks with checkable acceptance criteria. |

Run each workflow when its inputs are ready, with review between phases. A draft
from an earlier phase cannot serve as an approved input to the next one.
Architecture is initially reviewed as a hypothesis; consolidation reconciles it
with the available evidence and decisions.

The roadmap uses **rolling waves**: detail and approve only the next epic while
later candidates stay cheap drafts. It records sequence, dependencies and the
effort you are willing to spend, without a calendar schedule. Each task describes
observable behavior, acceptance criteria, contracts and scope; implementation
internals and build order are left to the development process.

## Continue work and handle changes

For a returning session in Claude Code:

```text
/loom:prime
/loom:status
```

In Codex or Copilot, use `loom-prime-method` and `loom-status-method`. Prime loads
context and points to the next action; status reports document health, blockers
and unfinished changes.

Send a new request through intake, for example:

```text
/loom:intake Members should be able to join a waiting list for a full session.
```

The equivalent shared skill is [loom-intake-method](skills/loom-intake-method/SKILL.md).
It preserves the input, classifies it, identifies affected documents and proposes
the smallest owning phase. It waits for your acceptance or rejection before the
change proceeds; invoking intake does not start that phase automatically.

Deferred requests, uncertain changes and changes affecting approved knowledge
get a durable `CHG-*` record. An immediate edit confined to one draft may not
need one. The change record follows:

```text
captured → triaged → accepted → in-progress → applied
```

Rejected or superseded changes remain in the history. An applied change records
both the documents revised and the downstream documents revalidated. Only the
affected scope needs revalidation. Intake can also capture an incoming request
immediately after initialization, before a vision exists; triage waits for it.

If implementation contradicts an approved requirement or decision, record a
blocking question and resolve it through the owning phase. This preserves the
reason for changing an agreement.

### Other tools

| Claude Code command | Workflow | When to use it |
|---|---|---|
| `/loom:review <file>` | [loom-review-gate](skills/loom-review-gate/SKILL.md) | Check a document, resolve questions and manage approval or ADR acceptance. |
| `/loom:challenge <file>` | [loom-challenger](agents/loom-challenger.md) agent | Get a fresh-context critique of assumptions, alternatives and the cost of being wrong. |
| `/loom:spike <question>` | [loom-spike-method](skills/loom-spike-method/SKILL.md) | Frame one time-boxed, falsifiable research question and record its results. |
| `/loom:skeleton` | [loom-skeleton-phase](skills/loom-skeleton-phase/SKILL.md) | Specify an optional small exercise to test an architecture or technology hypothesis. |
| `/loom:audit` | [loom-audit-phase](skills/loom-audit-phase/SKILL.md) | Recheck decision triggers, guessed facts, overdue business rules and stale questions. |
| `/loom:status` | [loom-status-method](skills/loom-status-method/SKILL.md) | See document statuses, blocking questions, unfinished changes and index health. |

Spikes, benchmarks, prototypes and skeletons are optional evidence methods.
Choose one when the learning justifies the cost. The exercise may run outside
Loom; retain its question, observations, limitations, provenance and conclusion
in the documents. Evidence supports a recommendation; an ADR separately records
the authorized decision.

## How agreements stay trustworthy

Regular documents follow `draft → in-review → approved`, with `superseded` for
historical versions. ADRs follow `proposed → accepted | rejected`, and accepted
decisions may later be deprecated or superseded.

Documents and important table rows have stable, meaningful IDs such as
`UC-member-books-session` or `ADR-use-postgres-for-bookings`. An unresolved OQ
marked `(blocking)` prevents approval. You resolve blocking product questions;
ADR decision authority and any delegation are recorded according to the policy
in `docs/loom.yaml`.

An accepted ADR preserves the original decision: later changes use append-only
addenda or a new superseding ADR. It records evidence level (`none`, `reasoned`,
`reported`, `observed`, `measured`), confidence, limitations and revisit triggers.
Weak evidence can support a decision when the remaining risk, accepting
authority and conditions for reconsideration are explicit.

The reviewer and challenger agents report findings and have read-only access;
the main session makes document changes. A challenge is required for one-way
ADRs, must-criticality epics and designs introducing a new external contract.

### Run document checks directly

After initialization, run checks from the **project repository root**. These
examples use the default paths; run them once the relevant documents exist:

```bash
python3 scripts/loom/link_check.py
python3 scripts/loom/oq_scan.py --gate docs/
python3 scripts/loom/adr_scan.py --gate
python3 scripts/loom/change_scan.py --gate
python3 scripts/loom/gherkin_lint.py --gate
python3 scripts/loom/roadmap_gen.py --gate
python3 scripts/loom/uc_diagram_gen.py --gate
```

These tools check ID references, task and epic dependencies, blocking questions,
ADR and change-record metadata, reusable scenario phrasing and actor/use-case
links. Consolidation also uses `adr_scan.py --gate --framing` to check decision
framing and quality-scenario mappings. The scripts check document mechanics;
substantive correctness still needs review.

Regenerate the convenience views when their source documents change:

```bash
python3 scripts/loom/index_gen.py
python3 scripts/loom/roadmap_gen.py
python3 scripts/loom/uc_diagram_gen.py
```

`INDEX.md`, `ROADMAP.md` and `UC-DIAGRAM.md` begin with a `GENERATED` marker.
Update their source documents and rerun the generator. For an affected ID,
`impact_scan.py --id <ID>` reports direct and transitive consumers, and
`link_check.py --refs <ID>` lists reference sites. Each documented check supports
`--help`.

### Refresh an initialized project

After updating the plugin, run `/loom:init --refresh` in Claude Code, or ask
Codex/Copilot to use `loom-init` with `--refresh`. It synchronizes shipped scripts,
updates package/script version metadata, ensures the changes directory exists
and reports local scripts no longer shipped. Existing documents are preserved.

`docs/loom.yaml` holds three independent versions: `loom_version` identifies the
plugin package, `version` identifies the framework configuration, and
`scripts_version` identifies the copied validation tools. Status compares the
project's script version with the plugin's shipped scripts to detect a needed
refresh.

## Developing this plugin

| Path | Responsibility |
|---|---|
| `.claude-plugin/`, `.codex-plugin/`, `plugin.json` | Host-specific plugin manifests. |
| `.agents/`, `.github/plugin/` | Marketplace catalogs; `.github/` also contains Copilot instructions and CI. |
| `commands/` | Thin Claude Code command wrappers. |
| `skills/` | Shared workflows, conventions and document templates. |
| `agents/`, `copilot-agents/` | Read-only document reviewer and challenger profiles. |
| `scripts/loom/` | Python standard-library document checks and generators. |
| `init-assets/` | Configuration and seed decision copied into projects. |
| `tests/` | Tests of the plugin's scripts using temporary project fixtures. |

To validate plugin changes:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/loom/*.py
```

Keep commands thin and procedures in shared skills. Check affected host
integrations in a scratch project, and keep the command, skill, templates,
agents and configuration coherent. See [AGENTS.md](AGENTS.md) for development
and versioning rules, [CHANGELOG.md](CHANGELOG.md) for release history, and
[LICENSE](LICENSE) for the MIT license.
