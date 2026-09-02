#!/usr/bin/env python3
"""Loom: calculate direct and transitive document consumers of an ID.

Usage:
  impact_scan.py --id ID                 print a human-readable impact report
  impact_scan.py --id ID --json          emit machine-readable output
  impact_scan.py --id ID --gate          fail when an approved/accepted consumer is found

The graph is deliberately based on explicit ID references. Generated projection
files are excluded, as they are derived from source documents and do not add a
dependency edge.
"""
import json
import re
import sys
from collections import defaultdict, deque
from pathlib import Path

from config import ConfigError, project_config, require_targets, target, usage

REF_RE = re.compile(
    r"\b(?:ADR|UC|SPIKE|TASK|OQ|QS|DRV|BR|ACTOR|track|epic|CHG)-"
    r"[a-z0-9][a-z0-9-]*[a-z0-9]\b"
)
QS_DEF_RE = re.compile(
    r"^\|\s*((?:QS|DRV|BR|ACTOR|track)-[a-z0-9][a-z0-9-]*[a-z0-9])\s*\|"
)
OQ_DEF_RE = re.compile(r"^-\s*\[[ xX]\]\s*(OQ-[a-z0-9][a-z0-9-]*)\b")


def generated(path):
    try:
        return path.read_text(encoding="utf-8").splitlines()[0].lstrip().startswith("<!-- GENERATED")
    except (OSError, UnicodeError, IndexError):
        return False


def frontmatter(lines):
    if not lines or lines[0].strip() != "---":
        return {}
    fm = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fm
        if re.match(r"^\S[^:]*:", line):
            key, _, value = line.partition(":")
            value = value.split("#", 1)[0].strip()
            if value in {"", "[]", "null", "~"}:
                fm[key.strip()] = [] if value in {"", "[]"} else None
            else:
                fm[key.strip()] = value.strip("'\"")
    return fm


def collect(docs):
    definitions = {}
    refs = defaultdict(list)
    file_info = {}
    for path in sorted(docs.rglob("*.md")):
        if path.name == "INDEX.md" or generated(path):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError):
            continue
        fm = frontmatter(lines)
        if isinstance(fm.get("id"), str) and fm["id"].startswith("CHG-"):
            continue
        ids = []
        if isinstance(fm.get("id"), str):
            ids.append(fm["id"])
        for line in lines:
            q = OQ_DEF_RE.match(line.strip())
            if q:
                ids.append(q.group(1))
            row = QS_DEF_RE.match(line.strip())
            if row:
                ids.append(row.group(1))
        file_key = str(path)
        file_info[file_key] = {
            "file": file_key,
            "ids": ids,
            "status": fm.get("status"),
        }
        for item in ids:
            definitions.setdefault(item, file_key)
        for number, line in enumerate(lines, 1):
            for ref in REF_RE.findall(line):
                refs[ref].append({"file": file_key, "line": number})
    return definitions, refs, file_info


def state(info):
    status = info.get("status")
    if status in {"approved", "accepted"}:
        return "blocked"
    if status in {"draft", "in-review", "proposed"}:
        return "needs-review"
    return "informational"


def scan(target_id, definitions, refs, file_info):
    direct = []
    target_file = definitions.get(target_id)
    for ref in refs.get(target_id, []):
        if ref["file"] == target_file:
            continue
        info = file_info[ref["file"]]
        direct.append({
            "id": info["ids"][0] if info["ids"] else None,
            "file": info["file"],
            "status": info.get("status"),
            "state": state(info),
            "line": ref["line"],
            "distance": 1,
        })

    seen = {item["file"] for item in direct}
    queue = deque((item["file"], 1) for item in direct)
    transitive = []
    while queue:
        current, distance = queue.popleft()
        current_info = file_info[current]
        for defined_id in current_info["ids"]:
            for ref in refs.get(defined_id, []):
                consumer = ref["file"]
                if consumer in seen or consumer == current:
                    continue
                seen.add(consumer)
                info = file_info[consumer]
                item = {
                    "id": info["ids"][0] if info["ids"] else None,
                    "file": consumer,
                    "status": info.get("status"),
                    "state": state(info),
                    "line": ref["line"],
                    "distance": distance + 1,
                }
                transitive.append(item)
                queue.append((consumer, distance + 1))
    return {
        "target": target_id,
        "defined_at": definitions.get(target_id),
        "direct": direct,
        "transitive": transitive,
        "blocked": sum(item["state"] == "blocked" for item in direct + transitive),
    }


def main(argv):
    if "--help" in argv:
        print(usage("impact_scan.py", "--id ID [--json|--gate]", "Calculate direct and transitive ID consumers."))
        return 0
    if "--id" not in argv:
        print("ERROR: --id requires an ID", file=sys.stderr)
        return 1
    index = argv.index("--id")
    if index + 1 >= len(argv):
        print("ERROR: --id requires an ID", file=sys.stderr)
        return 1
    target_id = argv[index + 1]
    try:
        config, base = project_config()
        docs = base / target(config, "docs", "docs")
    except ConfigError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    for error in require_targets([docs]):
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    definitions, refs, file_info = collect(docs)
    if target_id not in definitions:
        print(f"ERROR: target ID '{target_id}' is not defined", file=sys.stderr)
        return 1
    result = scan(target_id, definitions, refs, file_info)
    if "--json" in argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Impact for {target_id} ({result['defined_at']})")
        for label in ("direct", "transitive"):
            print(f"{label}:")
            items = result[label]
            if not items:
                print("  —")
            for item in items:
                print(f"  [{item['state']}] {item['id'] or '?'}  {item['file']}:{item['line']}")
        print(f"-- direct: {len(result['direct'])}, transitive: {len(result['transitive'])}, blocked: {result['blocked']}")
    if "--gate" in argv and result["blocked"]:
        print(f"GATE FAILED: {result['blocked']} blocked consumer(s)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
