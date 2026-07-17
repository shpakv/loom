#!/usr/bin/env python3
"""Loom: scan documents for open questions (OQ).

Usage:
  oq_scan.py <file-or-dir> [...]      list all OQs with status
  oq_scan.py --gate <file>            exit 1 if the file has open blocking OQs
  oq_scan.py --json <file-or-dir>     machine-readable output
"""
import json
import re
import sys
from pathlib import Path

OQ_RE = re.compile(
    r"^-\s*\[(?P<done>[ xX])\]\s*(?P<id>OQ-[A-Za-z0-9][A-Za-z0-9-]*)\s*"
    r"(?P<blocking>\(blocking\))?\s*:?\s*(?P<text>.*)$"
)


def scan_file(path: Path):
    out = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return out
    for n, line in enumerate(lines, 1):
        m = OQ_RE.match(line.strip())
        if m:
            out.append({
                "file": str(path), "line": n, "id": m["id"],
                "open": m["done"] == " ",
                "blocking": bool(m["blocking"]),
                "text": m["text"].strip(),
            })
    return out


def collect(targets):
    oqs = []
    for t in targets:
        p = Path(t)
        files = sorted(p.rglob("*.md")) if p.is_dir() else [p]
        for f in files:
            oqs.extend(scan_file(f))
    return oqs


def main(argv):
    gate = "--gate" in argv
    as_json = "--json" in argv
    targets = [a for a in argv if not a.startswith("--")] or ["docs"]
    oqs = collect(targets)

    if as_json:
        print(json.dumps(oqs, ensure_ascii=False, indent=2))
    else:
        for q in oqs:
            state = "OPEN " if q["open"] else "done "
            flag = " [BLOCKING]" if q["blocking"] and q["open"] else ""
            print(f"{state}{q['id']}{flag}  {q['text']}  ({q['file']}:{q['line']})")
        open_n = sum(q["open"] for q in oqs)
        blk_n = sum(q["open"] and q["blocking"] for q in oqs)
        print(f"-- total: {len(oqs)}, open: {open_n}, open blocking: {blk_n}")

    if gate:
        blocking_open = [q for q in oqs if q["open"] and q["blocking"]]
        if blocking_open:
            print(f"GATE FAILED: {len(blocking_open)} open blocking OQ(s)",
                  file=sys.stderr)
            return 1
        print("GATE PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
