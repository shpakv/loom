---
name: loom-status-method
description: Report portable Loom project status from configured document indexes, open questions and gate health.
---

# Loom status method

Read `docs/loom.yaml`, print the configured document index and scan configured
documents for open questions. Check generated indexes and report document
status counts, blocking questions and the most useful next phase. Compare the
project `scripts_version` with the shipped scripts version; do not compare it
with the plugin package version.
