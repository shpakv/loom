---
name: loom-init
description: Initialize or refresh Loom project state in the current repository by creating the docs structure, configuration and portable gate scripts. Use when starting Loom in a repository or synchronizing its scripts after a plugin update.
---

# Loom initialization

Initialize the current repository without overwriting existing project
documents. Loom scaffolds knowledge-layer state; it does not create product
code.

## Identify the plugin version

Before creating or refreshing the project configuration, determine the
installed Loom package version from the plugin root that contains
`init-assets/loom.yaml`. Read the `version` field from the first available
manifest in this order:

1. `.codex-plugin/plugin.json`
2. `.claude-plugin/plugin.json`
3. `plugin.json`

Call that value `<loom-version>`. It is the version of the Loom plugin package,
not the framework `version` or the shipped-gates `scripts_version` in
`loom.yaml`. If no manifest is readable, use the template's `loom_version` as
a fallback and report that the package version could not be verified.

## Full initialization

When the request is a normal initialization, create these directories if they
do not exist:

```text
docs/product/use-cases
docs/domain
docs/adr
docs/spikes
docs/changes
docs/architecture
docs/conventions
docs/roadmap/epics
scripts/loom
```

Copy the plugin's `init-assets/loom.yaml` to `docs/loom.yaml`, the seed ADR to
`docs/adr/ADR-adopt-loom.md`, and every `scripts/loom/*.py` file to the
project's `scripts/loom/`. Skip files that already exist; never overwrite
project content during full initialization.

After copying (or when `docs/loom.yaml` already exists), add or update only
its top-level `loom_version` field to `<loom-version>`. Preserve every other
line and project-specific setting in the existing configuration. This records
which Loom package performed the initialization.

Locate those resources relative to the installed Loom plugin. In Claude Code
the plugin root is `${CLAUDE_PLUGIN_ROOT}`. In Codex or Copilot, use the
installed plugin's resource directory or the equivalent local checkout path;
do not hardcode this repository's absolute path.

If legacy `.claude/commands/loom-*.md` or `.claude/skills/loom-*` files exist,
report them and ask before deleting them. Finish by showing the created paths,
then continue with the imagine phase.

## Refresh

When the request contains `--refresh`, copy only the currently shipped
`scripts/loom/*.py` into the project's `scripts/loom/`, report project-local
scripts that are no longer shipped, and update `scripts_version` in
`docs/loom.yaml`. Also add or update only its top-level `loom_version` field to
`<loom-version>`. Ensure the configured changes directory exists, but never
overwrite or rewrite documents under `docs/`.

After either mode, report what was created or synchronized and remind the user
that the phase route starts with imagine unless an existing project is being
triaged through intake. Intake may be used immediately after init in capture-only
mode, even before VISION exists.
