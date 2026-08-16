---
description: Scaffold Loom project state (docs skeleton, config, gate scripts) into the current repository
argument-hint: [--refresh]
---
Initialize this repository for Loom. The plugin root is available as
$CLAUDE_PLUGIN_ROOT.

If `$ARGUMENTS` contains `--refresh`: ONLY sync `scripts/loom/*.py` from
`${CLAUDE_PLUGIN_ROOT}/scripts/loom/` — overwrite what the plugin ships and
report (offering to delete) any project-local `scripts/loom/*.py` the plugin no
longer ships, since a stale gate script reads config keys that are gone. Then
update `scripts_version` in docs/loom.yaml to the plugin version. Never touch
anything under docs/ content.

Otherwise, full scaffold (skip any file that already exists — never overwrite):
1. Create directories: docs/product/use-cases, docs/domain, docs/adr,
   docs/spikes, docs/architecture, docs/conventions, docs/roadmap/epics,
   changes/, scripts/loom/.
2. Copy `${CLAUDE_PLUGIN_ROOT}/init-assets/loom.yaml` → docs/loom.yaml.
3. Copy `${CLAUDE_PLUGIN_ROOT}/init-assets/adr/ADR-adopt-loom.md` → docs/adr/.
4. Copy `${CLAUDE_PLUGIN_ROOT}/scripts/loom/*.py` → scripts/loom/ (these are
   the project-local copies used by CI gates).
5. If legacy kit files exist (.claude/commands/loom-*.md,
   .claude/skills/loom-*), tell the user the plugin supersedes them and offer
   to delete them (ask before deleting).
6. Finish by reminding: Loom produces documents and task specs, not code — fill
   the `engine:` block in docs/loom.yaml with the SDD engine that will implement
   them (needed by /loom:compile; ask which one if it is not obvious from the
   repo), then start with /loom:prime.
