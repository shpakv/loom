#!/usr/bin/env python3
"""Loom: ADR lifecycle validator.

Scans docs for files whose frontmatter id starts with 'ADR-'.

Checks:
  - status in {proposed, accepted, rejected, deprecated, superseded}
  - body contains a human-visible `Status: <value>` line matching frontmatter
  - accepted/rejected ADRs have `decided:` filled
  - accepted one-way ADRs have material verification (not 'judgment')
  - superseded ADRs have `superseded_by`; supersedes/superseded_by are symmetric
  - warns on accepted ADRs with empty revisit_when (not a gate failure)

Usage:
  adr_scan.py [paths...]          report (default: docs/)
  adr_scan.py --gate [paths...]   exit 1 on violations
  adr_scan.py --revisit           print only accepted ADRs' revisit triggers (audit)
"""
import re
import sys
from pathlib import Path

STATUSES = {"proposed", "accepted", "rejected", "deprecated", "superseded"}


BODY_STATUS_RE = re.compile(r"^Status:\s*([a-z]+)\b", re.IGNORECASE)


def body_status(lines):
    """First `Status: ...` line after the frontmatter block, or None."""
    in_fm, fm_done = False, False
    for line in lines:
        st = line.strip()
        if st == "---" and not fm_done:
            if in_fm:
                fm_done = True
            in_fm = True
            continue
        if fm_done:
            m = BODY_STATUS_RE.match(st)
            if m:
                return m.group(1).lower()
    return None


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
    gate = "--gate" in argv
    revisit_only = "--revisit" in argv
    targets = [a for a in argv if not a.startswith("--")] or ["docs"]

    adrs = {}
    for t in targets:
        p = Path(t)
        for f in (sorted(p.rglob("*.md")) if p.is_dir() else [p]):
            try:
                fm = frontmatter(f.read_text(encoding="utf-8").splitlines())
            except (UnicodeDecodeError, OSError):
                continue
            if isinstance(fm.get("id"), str) and fm["id"].startswith("ADR-"):
                text = f.read_text(encoding="utf-8")
                adrs[fm["id"]] = (fm, str(f), body_status(text.splitlines()),
                                  "DRV-" in text)

    errors, warnings = [], []
    for aid, (fm, path, bstat, has_drv) in sorted(adrs.items()):
        st = fm.get("status", "?")
        if st not in STATUSES:
            errors.append(f"{aid}: invalid ADR status '{st}' ({path})")
            continue
        if bstat is None:
            errors.append(f"{aid}: missing human-visible 'Status: ...' line "
                          f"in the body ({path})")
        elif bstat != st:
            errors.append(f"{aid}: body status '{bstat}' != frontmatter "
                          f"'{st}' — update both on transition ({path})")
        if st in ("accepted", "rejected") and fm.get("decided") in (None, "", "null", []):
            errors.append(f"{aid}: status '{st}' but 'decided:' is empty ({path})")
        if st == "accepted":
            if fm.get("reversibility") == "one-way" and fm.get("verification", "judgment") == "judgment":
                errors.append(f"{aid}: one-way decision accepted on 'judgment' — "
                              f"needs SPIKE/benchmark/prototype/reference ({path})")
            if not fm.get("revisit_when"):
                warnings.append(f"{aid}: accepted with empty revisit_when ({path})")
            if fm.get("reversibility") == "one-way" and not has_drv:
                warnings.append(f"{aid}: accepted one-way decision cites no "
                                f"drivers (DRV-*) in its body ({path})")
        if st == "superseded" and fm.get("superseded_by") in (None, "", "null", []):
            errors.append(f"{aid}: superseded without 'superseded_by' ({path})")
        sup = fm.get("supersedes", [])
        for old in (sup if isinstance(sup, list) else [sup]):
            if old in adrs:
                back = adrs[old][0].get("superseded_by")
                if back != aid:
                    errors.append(f"{aid} supersedes {old}, but {old}.superseded_by "
                                  f"is '{back}' — links must be symmetric")

    if revisit_only:
        for aid, (fm, _, _, _) in sorted(adrs.items()):
            if fm.get("status") == "accepted":
                trig = fm.get("revisit_when") or ["(none declared)"]
                print(aid)
                for tr in (trig if isinstance(trig, list) else [trig]):
                    print(f"  revisit when: {tr}")
        return 0

    for aid, (fm, _, _, _) in sorted(adrs.items()):
        print(f"{fm.get('status', '?'):<11} {aid}  "
              f"[{fm.get('reversibility', '?')}, verify: {fm.get('verification', '?')}]")
    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    print(f"-- ADRs: {len(adrs)}, errors: {len(errors)}, warnings: {len(warnings)}")

    if gate and errors:
        print("GATE FAILED", file=sys.stderr)
        return 1
    if gate:
        print("GATE PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
