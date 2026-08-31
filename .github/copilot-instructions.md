# Loom plugin repository

Loom is a multi-host agent plugin. It produces project knowledge and task
specifications; it does not implement product code. Claude Code uses
`.claude-plugin/`, `commands/`, `skills/` and `agents/`. Codex uses
`.codex-plugin/plugin.json` and the shared `skills/`. GitHub Copilot uses the
root `plugin.json`, `skills/` and `copilot-agents/`.

Keep the four plugin surfaces coherent when changing a concept. Shared skills
must use the Agent Skills frontmatter (`name` and `description`) and must not
depend on Claude-only environment variables. Claude command wrappers may refer
to `/loom:*`, but the skill body must remain understandable when invoked as a
Codex skill or by Copilot's task matching.

Scripts under `scripts/loom/` are standalone Python 3 standard-library tools.
Do not add third-party dependencies. Generated files must begin with the
required `<!-- GENERATED ... -->` marker. There is no test suite or CI in this
repository; validate edited scripts directly and inspect manifests as JSON.

Loom stops at `## Spec`. The external SDD engine writes plans, tests and code.
