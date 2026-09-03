---
name: loom-status-method
description: Report portable Loom project status from configured document indexes, open questions and gate health.
---

# Loom status method

Read `docs/loom.yaml`, print the configured document index and scan configured
documents for open questions. Check generated indexes and report document
status counts, blocking questions and the most useful next phase. Report the
recorded `loom_version` when present. Compare the project `scripts_version`
with the shipped scripts version; do not compare it with the plugin package
version.

If the configured changes directory exists, also run `change_scan.py --json` and
report unfinished change records, their routes and affected IDs. For accepted
or in-progress changes, use `impact_scan.py` for affected IDs and report
approved/accepted consumers as blocked scope rather than blocking the whole
project.
