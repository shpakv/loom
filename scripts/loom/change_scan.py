#!/usr/bin/env python3
"""Loom: validate durable CHG-* change records.

Usage:
  change_scan.py                 report change records
  change_scan.py --gate          fail on schema or lifecycle violations
  change_scan.py --json           emit machine-readable records and errors

The validator intentionally uses only the restricted YAML reader already used
by the other Loom gates.  It validates the change-record contract; reference
resolution is handled by link_check.py.
"""
import json
import re
import sys
from pathlib import Path

from config import (
    CHANGE_CLASSIFICATIONS,
    CHANGE_CONFIDENCE,
    CHANGE_SOURCES,
    CHANGE_STATUSES,
    ConfigError,
    project_config,
    require_targets,
    target,
    usage,
)

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID_RE = re.compile(r"^CHG-[a-z0-9][a-z0-9-]*[a-z0-9]$")

REQUIRED = ("id", "status", "source", "received", "confidence", "updated")
TRANSITIONS = {
    "captured": {"captured", "triaged"},
    "triaged": {"triaged", "accepted", "rejected"},
    "accepted": {"accepted", "in-progress", "rejected", "superseded"},
    "in-progress": {"in-progress", "applied", "superseded"},
    "applied": {"applied"},
    "rejected": {"rejected"},
    "superseded": {"superseded"},
}


def scalar(value):
    value = value.strip()
    if not value or value in {"null", "~"}:
        return None
    if value in {"[]", "[ ]"}:
        return []
    if value.startswith("[") and value.endswith("]"):
        return [x.strip().strip("'\"") for x in value[1:-1].split(",") if x.strip()]
    if (value.startswith("\"") and value.endswith("\"")) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def frontmatter(lines):
    if not lines or lines[0].strip() != "---":
        return {}
    fm, key = {}, None
    for line in lines[1:]:
        if line.strip() == "---":
            return fm
        if re.match(r"^\S[^:]*:", line):
            key, _, value = line.partition(":")
            key, value = key.strip(), value.split("#", 1)[0].strip()
            fm[key] = scalar(value)
        elif key and line.strip().startswith("- "):
            if not isinstance(fm.get(key), list):
                fm[key] = []
            fm[key].append(line.strip()[2:].split("#", 1)[0].strip().strip("'\""))
    return fm


def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def nonempty(value):
    return value is not None and str(value).strip() not in {"", "null"}


def validate(path, fm, lines, allowed_statuses):
    errors = []
    expected = path.stem
    record_id = fm.get("id")
    status = fm.get("status")
    if record_id != expected:
        errors.append(f"id '{record_id}' != filename '{expected}'")
    if not isinstance(record_id, str) or not ID_RE.fullmatch(record_id):
        errors.append("id must match CHG-<slug>")
    for field in REQUIRED:
        if not nonempty(fm.get(field)):
            errors.append(f"missing required field '{field}'")
    if status not in allowed_statuses:
        errors.append(f"invalid status '{status}'")
    if fm.get("source") not in CHANGE_SOURCES:
        errors.append(f"invalid source '{fm.get('source')}'")
    if fm.get("confidence") not in CHANGE_CONFIDENCE:
        errors.append(f"invalid confidence '{fm.get('confidence')}'")
    if fm.get("classification") is not None and fm.get("classification") not in CHANGE_CLASSIFICATIONS:
        errors.append(f"invalid classification '{fm.get('classification')}'")
    for field in ("affects", "applied_documents", "revalidated_documents"):
        if field in fm and fm[field] is not None and not isinstance(fm[field], list):
            errors.append(f"{field} must be a list")
    for field in ("received", "updated"):
        if nonempty(fm.get(field)) and not DATE_RE.fullmatch(str(fm[field])):
            errors.append(f"{field} must be YYYY-MM-DD")

    original = False
    for line in lines:
        if line.strip().lower() == "## original input":
            original = True
            break
    if not original:
        errors.append("missing '## Original input' section")

    if status in {"triaged", "accepted", "in-progress", "applied", "superseded"}:
        if fm.get("classification") not in CHANGE_CLASSIFICATIONS:
            errors.append("triaged-or-later status requires classification")
        if not nonempty(fm.get("route")):
            errors.append("triaged-or-later status requires route")
    if status in {"accepted", "rejected"}:
        for field in ("decision", "decided_by", "decided_at"):
            if not nonempty(fm.get(field)):
                errors.append(f"{status} status requires {field}")
        if nonempty(fm.get("decided_at")) and not DATE_RE.fullmatch(str(fm["decided_at"])):
            errors.append("decided_at must be YYYY-MM-DD")
    if status == "applied":
        for field in ("applied_documents", "revalidated_documents"):
            if not as_list(fm.get(field)):
                errors.append(f"applied status requires non-empty {field}")
    if status == "superseded" and not nonempty(fm.get("superseded_by")):
        errors.append("superseded status requires superseded_by")
    return errors


def load_records(changes_dir, allowed_statuses):
    records, errors = [], []
    for path in sorted(changes_dir.glob("CHG-*.md")):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            errors.append(f"{path}: cannot read: {exc}")
            continue
        fm = frontmatter(lines)
        record_errors = validate(path, fm, lines, allowed_statuses)
        records.append({"file": str(path), **fm, "errors": record_errors})
        errors.extend(f"{path}: {error}" for error in record_errors)
    return records, errors


def main(argv):
    if "--help" in argv:
        print(usage("change_scan.py", "[--gate|--json]", "Validate CHG-* change records."))
        return 0
    try:
        config, base = project_config()
        changes_dir = base / target(config, "changes", "docs/changes")
        configured = config.get("statuses", {}).get("changes", CHANGE_STATUSES)
        allowed_statuses = set(configured) if isinstance(configured, list) else CHANGE_STATUSES
    except ConfigError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    for error in require_targets([changes_dir]):
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    records, errors = load_records(changes_dir, allowed_statuses)
    if "--json" in argv:
        print(json.dumps({"records": records, "errors": errors}, ensure_ascii=False, indent=2))
    else:
        for record in records:
            print(f"{record.get('status', '?'):<12} {record.get('id', '?')}  {record['file']}")
            if record.get("route"):
                print(f"  route: {record['route']}")
            if record.get("errors"):
                for error in record["errors"]:
                    print(f"  ERROR: {error}")
        print(f"-- changes: {len(records)}, errors: {len(errors)}")
    if "--gate" in argv and errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
