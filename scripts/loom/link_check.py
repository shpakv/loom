#!/usr/bin/env python3
"""Loom: reference integrity check for slug-based IDs.

Definitions:
  - frontmatter `id:` of every docs/**/*.md (+ its `aliases:`)
  - OQ slugs defined in checklist lines
  - QS/DRV/BR/ACTOR/track table rows (`| <ID> | ... |`)
References:
  - every ADR/UC/SPIKE/TASK/OQ/QS/DRV/BR/ACTOR/track/epic-* mention in scanned files

Usage:
  link_check.py [paths...]        scan (default: docs/); exit 1 on violations
  link_check.py --refs <id>       reverse index: who references <id>
Violations: duplicate IDs/aliases, references that resolve to nothing.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

REF_RE = re.compile(r"\b(?:ADR|UC|SPIKE|TASK|OQ|QS|DRV|BR|ACTOR|track|epic)-[a-z0-9][a-z0-9-]*[a-z0-9]\b")
QS_DEF_RE = re.compile(r"^\|\s*((?:QS|DRV|BR|ACTOR|track)-[a-z0-9][a-z0-9-]*[a-z0-9])\s*\|")
OQ_DEF_RE = re.compile(r"^-\s*\[[ xX]\]\s*(OQ-[a-z0-9][a-z0-9-]*[a-z0-9])\b")


def generated(path: Path) -> bool:
    """Skip files written by a loom generator (ROADMAP.md, compiled engine files):
    they restate IDs defined elsewhere, so scanning them would report every
    projected ID as a duplicate definition."""
    try:
        with path.open(encoding="utf-8") as fh:
            return fh.readline().lstrip().startswith("<!-- GENERATED")
    except (UnicodeDecodeError, OSError):
        return False


def frontmatter(lines):
    if not lines or lines[0].strip() != "---":
        return {}
    fm, key = {}, None
    for line in lines[1:]:
        if line.strip() == "---":
            return fm
        if re.match(r"^\S[^:]*:", line):
            key, _, v = line.partition(":")
            key, v = key.strip(), v.strip()
            fm[key] = [] if v in ("", "[]") else v
            if v.startswith("[") and v.endswith("]") and v != "[]":
                fm[key] = [x.strip().strip("'\"") for x in v[1:-1].split(",")]
        elif key and line.strip().startswith("- "):
            if not isinstance(fm[key], list):
                fm[key] = []
            fm[key].append(line.strip()[2:].strip().strip("'\""))
    return fm


def main(argv):
    want_refs = None
    if "--refs" in argv:
        i = argv.index("--refs")
        want_refs = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    targets = argv or ["docs"]

    files = []
    for t in targets:
        p = Path(t)
        files += sorted(p.rglob("*.md")) if p.is_dir() else [p]
    files = [f for f in files if f.name != "INDEX.md" and not generated(f)]

    defined = {}                      # id -> file where defined
    refs = defaultdict(list)          # id -> [(file, line_no)]
    errors = []

    for f in files:
        try:
            lines = f.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        fm = frontmatter(lines)
        ids = []
        if isinstance(fm.get("id"), str):
            ids.append(fm["id"])
        ids += [a for a in fm.get("aliases", []) if isinstance(fm.get("aliases"), list)]
        for n, line in enumerate(lines, 1):
            m = OQ_DEF_RE.match(line.strip())
            if m:
                ids.append(m.group(1))
            q = QS_DEF_RE.match(line.strip())
            if q:
                ids.append(q.group(1))
            for ref in REF_RE.findall(line):
                refs[ref].append((str(f), n))
        for i in ids:
            if i in defined and defined[i] != str(f):
                errors.append(f"duplicate id '{i}': {defined[i]} and {f}")
            defined.setdefault(i, str(f))

    if want_refs:
        for file, n in refs.get(want_refs, []):
            print(f"{file}:{n}")
        return 0

    for ref, sites in sorted(refs.items()):
        if ref not in defined:
            for file, n in sites:
                errors.append(f"unresolved reference '{ref}' at {file}:{n}")

    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    print(f"-- files: {len(files)}, ids: {len(defined)}, "
          f"distinct refs: {len(refs)}, errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
