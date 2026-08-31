# Claude Code instructions for Loom

The canonical repository instructions are in [AGENTS.MD](../AGENTS.MD).
Read that file first: it covers the shared Loom model, repository layout,
authoring conventions, multi-host packaging, validation and release rules.

Claude Code-specific conventions:

- Commands live in `commands/*.md` and are exposed in the `loom:` namespace.
- Commands are thin wrappers around skills; durable procedure belongs in
  `skills/<name>/SKILL.md`.
- Claude agents live in `agents/*.md`, use `Read, Grep, Glob, Bash`, and are
  read-only. Copilot profiles live separately in `copilot-agents/`.
- `${CLAUDE_PLUGIN_ROOT}` is the only supported way for Claude commands to
  reference plugin resources.
- Validate Claude changes with the relevant `/loom:*` command in a scratch
  project, while keeping shared skills understandable to Codex and Copilot.
