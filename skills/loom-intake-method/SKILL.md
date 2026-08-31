---
name: loom-intake-method
description: Triage incoming work in an existing Loom project and route it to the smallest honest phase: design, roadmap, consolidate, imagine, requirements or spike. Use for bugs, feature requests and newly discovered facts; use imagine for a brand-new product.
---

# Loom: intake (triage router)

Goal: match incoming work to the SMALLEST phase that honestly handles it. Loom's
forward route is built for greenfield — a full socratic /loom:imagine is right for
a new product, but crushing for "fix this bug" or "add one field" on a project
that already has a vision, a roadmap, and accepted decisions. Intake is the cheap
router that keeps the ceremony proportional to the change. It produces NO gated
artifacts of its own — its only output is a routing decision and the first command
to run. Read `loom-core` conventions first.

Use this only on an initialized Loom project (there is a `docs/loom.yaml` and at
least a VISION). For a brand-new product, skip intake and go straight to
/loom:imagine.

**Two callers, one router.** Items arrive either from the human (a bug, a
request, an idea) or from review of an implementation — a fact that turned out
to be bigger than a glossary line. Newly discovered items enter the
same interview and the same routing table, with one difference: the fact already
exists in code, so the question is not "should we?" but "what authority should
have decided this, and does it still hold?". Route them by the same rules; a
change that contradicts an accepted ADR is a decision to revisit, not a
task, no matter that it is already written.

## Triage interview (one question per turn, stop as soon as the route is clear)

Ask only what you need to place the work — most items are obvious after one or two
questions:

1. **What is it** — a defect in something that already exists, a change to how an
   existing capability behaves, or a genuinely new capability?
2. **Does it fit the current vision and glossary?** If it introduces a new domain
   term, a new actor, or contradicts an anti-goal, it is a vision-level change, not
   a task.
3. **Does it cross a decision?** If satisfying it means changing an accepted ADR (a
   datastore, a protocol, a boundary), it is not a task — it is a decision to
   revisit.
4. **Does it fit one existing epic, or does it span several / need a new one?**

## Routing table

| Signal | Route to | Why |
|---|---|---|
| Defect, or a change wholly inside one existing capability, fits current contracts and decisions | `/loom:design` on the owning epic to add a `TASK-<slug>` (or append the task directly if the design doc is still accurate) | the requirements exist; this is just more work under them |
| New capability that fits the vision but no current epic covers it | `/loom:roadmap` to add an epic candidate, then `/loom:design` when it becomes the rolling-wave epic | roadmap owns epic scoping and sequencing |
| Satisfying it requires changing an accepted decision | a superseding ADR via `/loom:consolidate`, or `/loom:audit` first if a revisit trigger fired | accepted ADRs are immutable; the change is a new decision, not a task |
| It changes the problem, the users, an anti-goal, or needs a new glossary term | `/loom:imagine` (targeted — extend VISION/GLOSSARY/use-cases, not a from-scratch interview) | vision is the authority everything else derives from |
| It needs a new quality target or breaks an existing NFR | `/loom:requirements` to add/adjust the `QS-*`, which may cascade to architecture/technology | NFRs gate the structural and tech decisions below them |
| The answer depends on a falsifiable unknown (does X perform? is Y compatible?) | `/loom:spike` first, then re-run intake with the evidence | decide with evidence, not under pressure |

When several rows apply, route to the **highest-authority** one: a change that
touches both the vision and a task is a vision change first — resolving it there
reshapes everything below. Routing a vision-level change as a mere task is the
main failure intake exists to prevent.

## Output

A short verdict: the classification, the single command to run next, and — if the
work needs a paper trail before that command — the one artifact to create first
(an epic candidate, an OQ on the vision, a spike question). Do NOT start the
downstream phase yourself; hand the user the command so they enter it
deliberately. If the item is trivial and unambiguous (a typo, a one-line fix under
an accurate spec), say so plainly rather than inventing process for it.

## Rules

- **Proportional ceremony.** The right route is the smallest one that does not skip
  a real authority. Do not send a bug through /loom:imagine; do not smuggle a
  vision change in as a task.
- **Intake routes, it does not decide.** It never writes a spec, an ADR, or a
  design — it names where the work belongs and what to run. The owning phase does
  the work under its own gates.
- Re-runnable: after a spike or a vision edit resolves the unknown, run intake
  again — the route often changes once the missing fact exists.
