#!/usr/bin/env python3
"""Loom TDD gate: verify the GREEN step — the whole suite must pass.

Usage: verify_green.py [--cmd "<test command>"]
Reads test_command from docs/loom.yaml unless --cmd is given.
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
    cmd = argv[argv.index("--cmd") + 1] if "--cmd" in argv else test_command()
    if not cmd:
        print("ERROR: no test_command in docs/loom.yaml and no --cmd", file=sys.stderr)
        return 1
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    out = (r.stdout + "\n" + r.stderr).strip()
    tail = "\n".join(out.splitlines()[-15:])
    if r.returncode != 0:
        print("GREEN FAILED: suite not passing.", file=sys.stderr)
        print(tail)
        return 1
    print("GREEN VERIFIED: suite passing.")
    print(tail)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
