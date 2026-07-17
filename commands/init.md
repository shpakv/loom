---
description: Scaffold Loom project state (docs skeleton, config, gate scripts) into the current repository
argument-hint: [--refresh]
---
Initialize this repository for Loom. The plugin root is available as
$CLAUDE_PLUGIN_ROOT.

If `$ARGUMENTS` contains `--refresh`: ONLY overwrite `scripts/loom/*.py` from
`${CLAUDE_PLUGIN_ROOT}/scripts/loom/` and update `scripts_version` in
docs/loom.yaml to the plugin version. Never touch anything under docs/ content.

Otherwise, full scaffold (skip any file that already exists — never overwrite):
1. Create directories: docs/product/use-cases, docs/domain, docs/adr,
   docs/spikes, docs/architecture, docs/conventions, docs/roadmap/epics,
   changes/, scripts/loom/.
2. Copy `${CLAUDE_PLUGIN_ROOT}/init-assets/loom.yaml` → docs/loom.yaml.
3. Copy `${CLAUDE_PLUGIN_ROOT}/init-assets/adr/ADR-adopt-loom.md` → docs/adr/.
4. Copy `${CLAUDE_PLUGIN_ROOT}/scripts/loom/*.py` → scripts/loom/ (these are
   the project-local copies used by CI gates).
5. Append `.loom/` to .gitignore if missing.
6. If legacy kit files exist (.claude/commands/loom-*.md,
   .claude/skills/loom-*), tell the user the plugin supersedes them and offer
   to delete them (ask before deleting).
7. Finish by reminding: set `test_command` in docs/loom.yaml before
   /loom:implement, then start with /loom:prime.
