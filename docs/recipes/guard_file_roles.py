#!/usr/bin/env python3
"""Loom PreToolUse hook: enforce file-role boundaries for implement subagents.

Reads the current role from .loom/role (written by the orchestrator around
each dispatch). No marker file -> allow everything (main session).
Roles:
  test-author  -> may write ONLY files matching test_globs
  implementer  -> may write anything EXCEPT files matching test_globs
Blocking = exit code 2 with a message on stderr (Claude Code convention).
Test globs come from docs/loom.yaml `test_globs:` (inline JSON-ish list).
"""
import fnmatch
import json
import re
import sys
from pathlib import Path

DEFAULT_GLOBS = ["*_test.go", "*.spec.ts", "*.test.ts", "*.test.tsx",
                 "*.spec.js", "*.test.js", "test_*.py", "*_test.py",
                 "tests/**", "**/tests/**", "**/__tests__/**"]


def globs():
    try:
        for line in Path("docs/loom.yaml").read_text(encoding="utf-8").splitlines():
            m = re.match(r"^test_globs:\s*\[(.*)\]\s*$", line)
            if m:
                return [x.strip().strip("'\"") for x in m.group(1).split(",") if x.strip()]
    except OSError:
        pass
    return DEFAULT_GLOBS


def is_test(path, patterns):
    p = path.replace("\\", "/")
    name = p.rsplit("/", 1)[-1]
    return any(fnmatch.fnmatch(p, g) or fnmatch.fnmatch(name, g) for g in patterns)


def main():
    role_file = Path(".loom/role")
    if not role_file.exists():
        return 0
    role = role_file.read_text(encoding="utf-8").strip()
    if role not in ("test-author", "implementer"):
        return 0
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0
    path = (payload.get("tool_input") or {}).get("file_path", "")
    if not path:
        return 0
    test = is_test(path, globs())
    if role == "test-author" and not test:
        print(f"BLOCKED by loom guard: role=test-author may only write test "
              f"files; '{path}' is not one. Report findings to the "
              f"orchestrator instead.", file=sys.stderr)
        return 2
    if role == "implementer" and test:
        print(f"BLOCKED by loom guard: role=implementer may not modify tests; "
              f"'{path}' matches test globs. Return an OBJECTION to the "
              f"orchestrator instead.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
