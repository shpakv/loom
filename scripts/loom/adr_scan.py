#!/usr/bin/env python3
"""Loom: ADR lifecycle validator.

Scans docs for files whose frontmatter id starts with 'ADR-'.

Checks:
  - status in {proposed, accepted, rejected, deprecated, superseded}
  - body contains a human-visible `Status: <value>` line matching frontmatter
  - accepted/rejected ADRs have `decided:` filled
  - ADRs use neutral evidence_level and confidence values
  - superseded ADRs have `superseded_by`; supersedes/superseded_by are symmetric
  - warns on accepted ADRs with empty revisit_when (not a gate failure)

Usage:
  adr_scan.py [paths...]          report (default: docs/)
  adr_scan.py --gate [paths...]   exit 1 on violations
  adr_scan.py --revisit           print accepted ADRs' revisit triggers, plus
                                  BR-* rules whose calendar review_by is due (audit)
  adr_scan.py --framing [paths..] add stricter framing checks (opt-in), combine
                                  with --gate for CI. Enforces that decisions are
                                  framed by facts and targets before acceptance:
                                    - accepted one-way ADR cites both DRV-* and QS-*
                                    - any one-way ADR declares decision_mode
                                    - every QS-* in solution-strategy.md maps to an
                                      ADR-* or a convention (no unmapped NFR)
                                    - weak one-way decisions explicitly record
                                      risk acceptance and revisit conditions
                                    - accepted one-way ADR does not stand on a
                                      confidence: guessed driver without a
                                      revisit_when trigger
"""
import re
import sys
from datetime import date
from pathlib import Path
from config import (CONFIDENCE_LEVELS, DECISION_MODES, EVIDENCE_LEVELS,
                     ConfigError, project_config, target, require_targets, usage)

STATUSES = {"proposed", "accepted", "rejected", "deprecated", "superseded"}
QS_RE = re.compile(r"\bQS-[a-z0-9-]+", re.IGNORECASE)
ADR_REF_RE = re.compile(r"\bADR-[a-z0-9-]+", re.IGNORECASE)
DRV_REF_RE = re.compile(r"\bDRV-[a-z0-9-]+", re.IGNORECASE)
# a DRIVERS.md table row: | DRV-slug | fact | confidence | verify by |
DRV_ROW_RE = re.compile(
    r"^\|\s*(DRV-[a-z0-9-]+)\s*\|[^|]*\|\s*([a-z]+)\s*\|", re.IGNORECASE)

BODY_STATUS_RE = re.compile(r"^Status:\s*([a-z]+)\b", re.IGNORECASE)

# a RULES.md row: | BR-slug | rule | bounds | source | review_by |
BR_ROW_RE = re.compile(r"^\|\s*(BR-[a-z0-9-]+)\s*\|(.*)$", re.IGNORECASE)
ISO_DATE_RE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")


def rules_due(targets, today=None):
    """[(BR id, review_by, path)] for rules with a calendar review_by at or past
    due. Rules sourced from a standard rot by revision, not by a condition — so
    unlike ADRs they need a date, and something has to read it."""
    today = today or date.today().isoformat()
    due = []
    for t in targets:
        p = Path(t)
        for f in (sorted(p.rglob("*.md")) if p.is_dir() else [p]):
            try:
                lines = f.read_text(encoding="utf-8").splitlines()
            except (UnicodeDecodeError, OSError):
                continue
            for line in lines:
                m = BR_ROW_RE.match(line.strip())
                if not m or "{" in line:
                    continue
                cells = [c.strip() for c in m.group(2).split("|")]
                # review_by is the last non-empty cell only if it is a bare date
                dates = [c for c in cells if ISO_DATE_RE.fullmatch(c)]
                if dates and dates[-1] <= today:
                    due.append((m.group(1), dates[-1], str(f)))
    return due


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


def has_section(text, heading):
    return bool(re.search(rf"^##\s+{re.escape(heading)}\s*$", text,
                          re.IGNORECASE | re.MULTILINE))


def empty(value):
    return value in (None, "", "null", "[]", [])


def decision_policy(config, reversibility):
    policy = config.get("decisions", {}) if isinstance(config, dict) else {}
    key = "irreversible" if reversibility in ("irreversible", "permanent") else (
        "one_way" if reversibility == "one-way" else "two_way")
    return policy.get(key, "recommend" if key == "one_way" else "delegated")


def policy_is_freer(mode, default):
    # Higher rank means less human authority is required. record-only is a
    # separate audit mode and is never treated as a freer override.
    rank = {"record-only": 0, "confirm": 1, "recommend": 2, "delegated": 3}
    return rank.get(mode, -1) > rank.get(default, -1)


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
    if "--help" in argv:
        print(usage("adr_scan.py", "[--gate] [--framing|--revisit] [paths ...]", "Validate ADR lifecycle and symmetry."))
        return 0
    gate = "--gate" in argv
    revisit_only = "--revisit" in argv
    framing = "--framing" in argv
    targets = [a for a in argv if not a.startswith("--")]
    if not targets:
        try:
            config, base = project_config()
            targets = [str(base / target(config, "docs", "docs"))]
        except ConfigError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
    for error in require_targets(targets):
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    config = {}
    try:
        config, _ = project_config()
        statuses = set(config.get("statuses", {}).get("adr", STATUSES))
    except ConfigError:
        statuses = STATUSES
    adrs = {}
    errors = []
    doc_ids = set()
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
            if isinstance(fid, str) and fid:
                doc_ids.add(fid)
            if isinstance(fid, str) and fid.startswith("ADR-"):
                if fid in adrs:
                    errors.append(f"duplicate ADR id '{fid}' in {adrs[fid][1]} and {f}")
                adrs[fid] = (fm, str(f), body_status(text.splitlines()), text,
                             "DRV-" in text, bool(QS_RE.search(text)),
                             sorted(set(DRV_REF_RE.findall(text))))
            # DRIVERS.md (or any doc carrying DRV rows) → confidence map
            for line in text.splitlines():
                m = DRV_ROW_RE.match(line.strip())
                if m:
                    drv_conf[m.group(1).lower()] = m.group(2).lower()

    warnings = []
    for aid, (fm, path, bstat, text, has_drv, has_qs, drv_refs) in sorted(adrs.items()):
        st = fm.get("status", "?")
        reversibility = fm.get("reversibility", "two-way")
        one_way = reversibility in ("one-way", "irreversible", "permanent")
        if st not in statuses:
            errors.append(f"{aid}: invalid ADR status '{st}' ({path})")
            continue
        if bstat is None:
            errors.append(f"{aid}: missing human-visible 'Status: ...' line "
                          f"in the body ({path})")
        elif bstat != st:
            errors.append(f"{aid}: body status '{bstat}' != frontmatter "
                              f"'{st}' — update both on transition ({path})")
        evidence = fm.get("evidence_level")
        confidence = fm.get("confidence")
        mode = fm.get("decision_mode")
        if evidence not in EVIDENCE_LEVELS:
            errors.append(f"{aid}: invalid evidence_level '{evidence}' — use "
                          f"{', '.join(sorted(EVIDENCE_LEVELS))} ({path})")
        if confidence not in CONFIDENCE_LEVELS:
            errors.append(f"{aid}: invalid confidence '{confidence}' — use low, "
                          f"medium or high ({path})")
        if mode not in DECISION_MODES:
            errors.append(f"{aid}: invalid decision_mode '{mode}' — use "
                          f"{', '.join(sorted(DECISION_MODES))} ({path})")
        refs = fm.get("evidence_refs", [])
        refs = refs if isinstance(refs, list) else [refs]
        for ref in refs:
            if not ref or str(ref).startswith(("http://", "https://")):
                continue
            if ref not in doc_ids:
                errors.append(f"{aid}: evidence_ref '{ref}' does not resolve to "
                              f"an internal document or external URI ({path})")
        if st in ("proposed", "accepted") and not has_section(text, "Recommendation"):
            errors.append(f"{aid}: missing ## Recommendation ({path})")
        if st in ("proposed", "accepted") and not has_section(text, "Evidence"):
            errors.append(f"{aid}: missing ## Evidence ({path})")
        default_mode = decision_policy(config, reversibility)
        if mode in DECISION_MODES and policy_is_freer(mode, default_mode):
            if not fm.get("policy_override") or empty(fm.get("override_reason")):
                errors.append(f"{aid}: decision_mode '{mode}' is freer than project "
                              f"default '{default_mode}'; require policy_override "
                              f"and override_reason ({path})")
        if st == "accepted" and mode != "delegated" and empty(fm.get("authority")):
            errors.append(f"{aid}: accepted decision requires authority ({path})")
        if st in ("accepted", "rejected") and fm.get("decided") in (None, "", "null", []):
            errors.append(f"{aid}: status '{st}' but 'decided:' is empty ({path})")
        if st == "accepted":
            if not fm.get("revisit_when"):
                warnings.append(f"{aid}: accepted with empty revisit_when ({path})")
            if one_way and not has_drv:
                (errors if framing else warnings).append(
                    f"{aid}: accepted one-way decision cites no drivers "
                    f"(DRV-*) in its body ({path})")
        # --framing: stricter, opt-in checks that hard-wire "framed by facts and
        # targets before acceptance" (see the phase-reordering, v0.10.0).
            weak = confidence == "low" or evidence in ("none", "reasoned")
            if one_way and weak:
                required = [("risk_accepted_by", fm.get("risk_accepted_by")),
                            ("revisit_when", fm.get("revisit_when"))]
                for field, value in required:
                    if empty(value):
                        errors.append(f"{aid}: weak evidence on accepted one-way "
                                      f"decision requires {field} ({path})")
                for heading in ("Unknowns", "Residual risk", "Research decision"):
                    if not has_section(text, heading):
                        errors.append(f"{aid}: weak evidence requires ## {heading} "
                                      f"to make risk explicit ({path})")
        if framing:
            if st == "accepted" and one_way and not has_qs:
                errors.append(f"{aid}: accepted one-way decision cites no quality "
                              f"scenario (QS-*) — an untargeted one-way door ({path})")
            # Legacy verification fields are ignored; the neutral evidence model
            # is authoritative for new decisions.
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
        newer = fm.get("superseded_by")
        if newer in adrs:
            forward = adrs[newer][0].get("supersedes", [])
            if aid not in (forward if isinstance(forward, list) else [forward]):
                errors.append(f"{aid} is superseded_by {newer}, but {newer}.supersedes "
                              f"does not include {aid} — links must be symmetric")

    if revisit_only:
        for aid, (fm, _, _, _, _, _, _) in sorted(adrs.items()):
            if fm.get("status") == "accepted":
                trig = fm.get("revisit_when") or ["(none declared)"]
                print(aid)
                for tr in (trig if isinstance(trig, list) else [trig]):
                    print(f"  revisit when: {tr}")
        due = rules_due(targets)
        if due:
            print("\n-- business rules due for review (external source revised?)")
            for rid, when, path in sorted(due):
                print(f"{rid}\n  review_by: {when} ({path})")
        return 0

    if framing:
        spath, unmapped = strategy_unmapped_qs(targets)
        if unmapped:
            errors.append(f"solution-strategy: quality scenario(s) "
                          f"{', '.join(unmapped)} map to neither an ADR nor a "
                          f"convention — a decorative or undecided NFR ({spath})")

    for aid, (fm, _, _, _, _, _, _) in sorted(adrs.items()):
        print(f"{fm.get('status', '?'):<11} {aid}  "
              f"[{fm.get('reversibility', '?')}, evidence: {fm.get('evidence_level', '?')}, "
              f"confidence: {fm.get('confidence', '?')}]" )
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
