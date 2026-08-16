#!/usr/bin/env python3
"""Loom TDD gate: verify the RED step — tests must FAIL, for the right reason.

Usage:
  verify_red.py [--expect <substring>] [--cmd "<test command>"]
Reads test_command from docs/loom.yaml unless --cmd is given.
Exit 0: tests failed (and output contains --expect if provided).
Exit 1: tests passed (red step invalid) or expected reason not found.
"""
import re
import subprocess
import sys
from pathlib import Path


def test_command():
    for line in Path("docs/loom.yaml").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^test_command:\s*(.+)$", line)
        if m:
            return m.group(1).strip().strip("'\"")
    return None


def main(argv):
    cmd, expect = None, None
    if "--cmd" in argv:
        cmd = argv[argv.index("--cmd") + 1]
    if "--expect" in argv:
        expect = argv[argv.index("--expect") + 1]
    cmd = cmd or test_command()
    if not cmd:
        print("ERROR: no test_command in docs/loom.yaml and no --cmd", file=sys.stderr)
        return 1

    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    out = (r.stdout + "\n" + r.stderr).strip()
    tail = "\n".join(out.splitlines()[-15:])

    if r.returncode == 0:
        print("RED INVALID: test suite PASSED — the new test does not fail.\n"
              "Either it tests nothing (no real assertions) or the behavior "
              "already exists.", file=sys.stderr)
        print(tail)
        return 1
    if expect and expect not in out:
        print(f"RED SUSPICIOUS: tests failed, but not for the expected reason "
              f"(substring not found: {expect!r}). Inspect before proceeding.",
              file=sys.stderr)
        print(tail)
        return 1
    print("RED VERIFIED: tests fail" + (f" with expected reason {expect!r}" if expect else ""))
    print(tail)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
