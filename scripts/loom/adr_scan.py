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
  adr_scan.py --framing [paths..] add stricter framing checks (opt-in), combine
                                  with --gate for CI. Enforces that decisions are
                                  framed by facts and targets before acceptance:
                                    - accepted one-way ADR cites both DRV-* and QS-*
                                    - any one-way ADR declares decision_mode
                                    - every QS-* in solution-strategy.md maps to an
                                      ADR-* or a convention (no unmapped NFR)
                                    - accepted ADR with verification: SPIKE-<slug>
                                      points at a real, approved spike
                                    - accepted one-way ADR does not stand on a
                                      confidence: guessed driver without a
                                      revisit_when trigger
"""
import re
import sys
from pathlib import Path

STATUSES = {"proposed", "accepted", "rejected", "deprecated", "superseded"}
DECISION_MODES = {"decided", "framed", "menu", "delegated"}

QS_RE = re.compile(r"\bQS-[a-z0-9-]+", re.IGNORECASE)
ADR_REF_RE = re.compile(r"\bADR-[a-z0-9-]+", re.IGNORECASE)
DRV_REF_RE = re.compile(r"\bDRV-[a-z0-9-]+", re.IGNORECASE)
# a DRIVERS.md table row: | DRV-slug | fact | confidence | verify by |
DRV_ROW_RE = re.compile(
    r"^\|\s*(DRV-[a-z0-9-]+)\s*\|[^|]*\|\s*([a-z]+)\s*\|", re.IGNORECASE)

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


def strategy_unmapped_qs(targets):
    """Return (path, [QS ids]) for solution-strategy.md rows whose line names a
    QS but resolves to neither an ADR-* nor a 'convention'. Empty list == clean."""
    for t in targets:
        p = Path(t)
        for f in (sorted(p.rglob("solution-strategy.md")) if p.is_dir()
                  else ([p] if p.name == "solution-strategy.md" else [])):
            try:
                lines = f.read_text(encoding="utf-8").splitlines()
            except (UnicodeDecodeError, OSError):
                continue
            unmapped = []
            for line in lines:
                for qs in QS_RE.findall(line):
                    # a template placeholder row (QS-{slug}) is not a real mapping
                    if "{" in line:
                        continue
                    if not ADR_REF_RE.search(line) and "convention" not in line.lower():
                        unmapped.append(qs)
            if unmapped:
                return str(f), sorted(set(unmapped))
    return None, []


def main(argv):
    gate = "--gate" in argv
    revisit_only = "--revisit" in argv
    framing = "--framing" in argv
    targets = [a for a in argv if not a.startswith("--")] or ["docs"]

    adrs = {}
    spikes = {}          # SPIKE-<slug> -> status (for framing verification checks)
    drv_conf = {}        # DRV-<slug> -> confidence (from DRIVERS.md rows)
    for t in targets:
        p = Path(t)
        for f in (sorted(p.rglob("*.md")) if p.is_dir() else [p]):
            try:
                text = f.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            fm = frontmatter(text.splitlines())
            fid = fm.get("id")
            if isinstance(fid, str) and fid.startswith("ADR-"):
                adrs[fid] = (fm, str(f), body_status(text.splitlines()),
                             "DRV-" in text, bool(QS_RE.search(text)),
                             sorted(set(DRV_REF_RE.findall(text))))
            elif isinstance(fid, str) and fid.startswith("SPIKE-"):
                spikes[fid] = fm.get("status", "?")
            # DRIVERS.md (or any doc carrying DRV rows) → confidence map
            for line in text.splitlines():
                m = DRV_ROW_RE.match(line.strip())
                if m:
                    drv_conf[m.group(1).lower()] = m.group(2).lower()

    errors, warnings = [], []
    for aid, (fm, path, bstat, has_drv, has_qs, drv_refs) in sorted(adrs.items()):
        st = fm.get("status", "?")
        one_way = fm.get("reversibility") == "one-way"
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
            if one_way and fm.get("verification", "judgment") == "judgment":
                errors.append(f"{aid}: one-way decision accepted on 'judgment' — "
                              f"needs SPIKE/benchmark/prototype/reference ({path})")
            if not fm.get("revisit_when"):
                warnings.append(f"{aid}: accepted with empty revisit_when ({path})")
            if one_way and not has_drv:
                (errors if framing else warnings).append(
                    f"{aid}: accepted one-way decision cites no drivers "
                    f"(DRV-*) in its body ({path})")
        # --framing: stricter, opt-in checks that hard-wire "framed by facts and
        # targets before acceptance" (see the phase-reordering, v0.10.0).
        if framing:
            if st == "accepted" and one_way and not has_qs:
                errors.append(f"{aid}: accepted one-way decision cites no quality "
                              f"scenario (QS-*) — an untargeted one-way door ({path})")
            if one_way and fm.get("decision_mode") not in DECISION_MODES:
                errors.append(f"{aid}: one-way decision with no decision_mode "
                              f"(decided|framed|menu|delegated) — a fork opened "
                              f"without agreeing how it was decided ({path})")
            # a verification: SPIKE-<slug> claim must point at a real, approved spike
            verif = fm.get("verification", "")
            if st == "accepted" and isinstance(verif, str) and verif.startswith("SPIKE-"):
                if verif not in spikes:
                    errors.append(f"{aid}: verification cites {verif}, which does "
                                  f"not exist — evidence claimed but missing ({path})")
                elif spikes[verif] not in ("approved", "accepted"):
                    errors.append(f"{aid}: verification cites {verif}, still "
                                  f"'{spikes[verif]}' — evidence not yet approved ({path})")
            # an accepted one-way decision may not rest on an unconfirmed guess
            # unless it declares what would invalidate it (revisit_when)
            if st == "accepted" and one_way and not fm.get("revisit_when"):
                guessed = sorted(d for d in drv_refs
                                  if drv_conf.get(d.lower()) == "guessed")
                if guessed:
                    errors.append(f"{aid}: accepted one-way decision stands on "
                                  f"guessed driver(s) {', '.join(guessed)} with no "
                                  f"revisit_when trigger — confirm the fact or "
                                  f"declare what invalidates the decision ({path})")
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
        for aid, (fm, _, _, _, _, _) in sorted(adrs.items()):
            if fm.get("status") == "accepted":
                trig = fm.get("revisit_when") or ["(none declared)"]
                print(aid)
                for tr in (trig if isinstance(trig, list) else [trig]):
                    print(f"  revisit when: {tr}")
        return 0

    if framing:
        spath, unmapped = strategy_unmapped_qs(targets)
        if unmapped:
            errors.append(f"solution-strategy: quality scenario(s) "
                          f"{', '.join(unmapped)} map to neither an ADR nor a "
                          f"convention — a decorative or undecided NFR ({spath})")

    for aid, (fm, _, _, _, _, _) in sorted(adrs.items()):
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
