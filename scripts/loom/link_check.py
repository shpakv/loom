#!/usr/bin/env python3
"""Loom: check document IDs and local Markdown navigation links.

Definitions:
  - frontmatter `id:` of every docs/**/*.md (+ its `aliases:`)
  - OQ slugs defined in checklist lines
  - QS/DRV/BR/ACTOR/track table rows (`| <ID> | ... |`)
References:
  - every ADR/UC/SPIKE/TASK/OQ/QS/DRV/BR/ACTOR/CHG/track/epic-* mention in scanned files
  - inline local .md links resolve to a file; fragments resolve to an HTML id or heading
  - a Markdown link labelled with a Loom ID points to the file defining that ID

Usage:
  link_check.py [paths...]        scan (default: docs/); exit 1 on violations
  link_check.py --refs <id>       reverse index: who references <id>
Violations: duplicate IDs/aliases, unresolved references, and broken Markdown
document links or fragments.
"""
import html
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit
from config import ConfigError, project_config, target, require_targets, usage

REF_RE = re.compile(r"\b(?:ADR|UC|SPIKE|TASK|OQ|QS|DRV|BR|ACTOR|CHG|track|epic)-[a-z0-9][a-z0-9-]*[a-z0-9]\b")
QS_DEF_RE = re.compile(r"^\|\s*((?:QS|DRV|BR|ACTOR|track)-[a-z0-9][a-z0-9-]*[a-z0-9])\s*\|")
OQ_DEF_RE = re.compile(r"^-\s*\[[ xX]\]\s*(OQ-[a-z0-9][a-z0-9-]*[a-z0-9])\b")
TASK_DEP_RE = re.compile(r"\bTASK-[a-z0-9][a-z0-9-]*[a-z0-9]\b")
MARKDOWN_LINK_RE = re.compile(
    r"(?<!!)\[((?:\\.|[^\]])+)\]\(\s*(?:<([^>\n]+)>|((?:\\.|[^\s)])+))"
)
FENCE_RE = re.compile(r"^\s{0,3}(\x60{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"(\x60+).*?\1")
ATX_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
SETEXT_HEADING_RE = re.compile(r"^\s{0,3}(=+|-+)\s*$")
HTML_ID_RE = re.compile(
    r"(?<![\w:-])id\s*=\s*(?:\"([^\"]+)\"|'([^']+)'|([^\s'\"=<>]+))",
    re.IGNORECASE,
)


def visible_markdown_lines(lines):
    """Return source lines outside fenced code blocks, preserving line numbers."""
    visible = []
    fence_char, fence_size = None, 0
    for number, line in enumerate(lines, 1):
        match = FENCE_RE.match(line)
        if fence_char:
            if match and match.group(1)[0] == fence_char and len(match.group(1)) >= fence_size:
                fence_char, fence_size = None, 0
            visible.append((number, ""))
            continue
        if match:
            fence_char, fence_size = match.group(1)[0], len(match.group(1))
            visible.append((number, ""))
            continue
        visible.append((number, line))
    return visible


def markdown_link_items(lines):
    """Yield (line number, label, destination) for inline Markdown links."""
    for number, line in visible_markdown_lines(lines):
        line = INLINE_CODE_RE.sub("", line)
        for match in MARKDOWN_LINK_RE.finditer(line):
            label = match.group(1)
            destination = match.group(2) or match.group(3)
            destination = re.sub(r"\\([!#$%&'()*+,\-./:;<=>?@\[\]^_\x60{|}~])", r"\1", destination)
            yield number, label, destination


def markdown_links(lines):
    """Yield (line number, destination) for inline Markdown links."""
    for number, _, destination in markdown_link_items(lines):
        yield number, destination


def heading_slug(text):
    """Approximate GitHub-style heading slugs for ordinary Markdown headings."""
    text = html.unescape(text)
    text = re.sub(r"<[^>]*>", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = text.replace("\x60", "")
    text = re.sub(r"[^\w -]", "", text, flags=re.UNICODE).lower().strip()
    return re.sub(r"\s+", "-", text)


def markdown_anchors(path):
    """Collect explicit HTML ids and renderer-style anchors for Markdown headings."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return set()
    visible = visible_markdown_lines(lines)
    anchors, heading_counts = set(), defaultdict(int)
    for index, (number, line) in enumerate(visible):
        markup_free = INLINE_CODE_RE.sub("", line)
        for match in HTML_ID_RE.finditer(markup_free):
            anchors.add(match.group(1) or match.group(2) or match.group(3))

        heading = ATX_HEADING_RE.match(line)
        heading_text = heading.group(1) if heading else None
        if not heading_text and index + 1 < len(visible):
            next_line = visible[index + 1][1]
            if line.strip() and SETEXT_HEADING_RE.match(next_line):
                heading_text = line.strip()
        if heading_text:
            base = heading_slug(heading_text)
            if base:
                suffix = heading_counts[base]
                heading_counts[base] += 1
                anchors.add(base if suffix == 0 else f"{base}-{suffix}")
    return anchors


def markdown_link_errors(path, lines, anchor_cache):
    """Validate local Markdown page destinations and any supplied fragments."""
    errors = []
    for number, destination in markdown_links(lines):
        try:
            parsed = urlsplit(html.unescape(destination))
        except ValueError:
            errors.append(f"invalid Markdown link '{destination}' at {path}:{number}")
            continue
        if parsed.scheme or parsed.netloc:
            continue
        target_path = unquote(parsed.path)
        fragment = unquote(parsed.fragment)
        if target_path and Path(target_path).suffix.lower() != ".md":
            continue
        if target_path:
            target = (path.parent / target_path).resolve()
        elif fragment:
            target = path.resolve()
        else:
            continue
        if not target.is_file():
            errors.append(
                f"unresolved Markdown document link '{destination}' at {path}:{number}"
            )
            continue
        if fragment:
            if target not in anchor_cache:
                anchor_cache[target] = markdown_anchors(target)
            if fragment not in anchor_cache[target]:
                errors.append(
                    f"unresolved Markdown anchor '#{fragment}' in {target} "
                    f"from {path}:{number}"
                )
    return errors


def find_cycle(graph):
    state, stack = {}, []
    def visit(node):
        state[node] = 1
        stack.append(node)
        for dep in graph.get(node, []):
            if dep not in graph:
                continue
            if state.get(dep) == 1:
                return stack[stack.index(dep):] + [dep]
            if not state.get(dep) and (cycle := visit(dep)):
                return cycle
        stack.pop()
        state[node] = 2
        return None
    for node in graph:
        if not state.get(node) and (cycle := visit(node)):
            return cycle
    return None


def generated(path: Path) -> bool:
    """Skip files written by a Loom generator (ROADMAP.md and INDEX.md):
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
    if "--help" in argv:
        print(usage("link_check.py", "[paths ...] | --refs ID", "Validate document IDs, references and local Markdown links."))
        return 0
    want_refs = None
    if "--refs" in argv:
        i = argv.index("--refs")
        if i + 1 >= len(argv):
            print("ERROR: --refs requires an ID", file=sys.stderr)
            return 1
        want_refs = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    targets = argv or []
    if not targets:
        try:
            config, base = project_config()
            docs_target = base / target(config, "docs", "docs")
            targets = [str(docs_target)]
            changes_target = base / target(config, "changes", "docs/changes")
            try:
                changes_target.relative_to(docs_target)
                changes_inside_docs = True
            except ValueError:
                changes_inside_docs = False
            if changes_target != docs_target and not changes_inside_docs:
                targets.append(str(changes_target))
        except ConfigError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
    for error in require_targets(targets):
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    files = []
    for t in targets:
        p = Path(t)
        files += sorted(p.rglob("*.md")) if p.is_dir() else [p]
    files = [f for f in files if f.name != "INDEX.md" and not generated(f)]

    defined = {}                      # id -> file where defined
    refs = defaultdict(list)          # id -> [(file, line_no)]
    linked_ids = []                   # (id, destination, source file, line)
    errors = []
    task_graph = {}
    anchor_cache = {}
    document_statuses = set()
    try:
        config, _ = project_config()
        document_statuses = set(config.get("statuses", {}).get("documents", []))
        change_statuses = set(config.get("statuses", {}).get("changes", []))
    except ConfigError as exc:
        errors.append(str(exc))
        change_statuses = set()

    for f in files:
        try:
            lines = f.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        errors.extend(markdown_link_errors(f, lines, anchor_cache))
        for line_number, label, destination in markdown_link_items(lines):
            linked_ids.extend(
                (ref, destination, str(f), line_number)
                for ref in REF_RE.findall(label)
            )
        fm = frontmatter(lines)
        record_id = str(fm.get("id", ""))
        valid_change_status = record_id.startswith("CHG-") and (not change_statuses or fm.get("status") in change_statuses)
        if fm.get("status") and document_statuses and fm["status"] not in document_statuses and not record_id.startswith("ADR-") and not valid_change_status:
            errors.append(f"invalid document status '{fm['status']}' at {f}")
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
        if isinstance(fm.get("id"), str) and fm["id"].startswith("TASK-"):
            deps = fm.get("depends_on", [])
            task_graph[fm["id"]] = deps if isinstance(deps, list) else ([deps] if deps else [])

    for task, deps in task_graph.items():
        for dep in deps:
            if dep and dep not in task_graph:
                errors.append(f"{task}: depends_on '{dep}' does not resolve to a task")
    if (cycle := find_cycle(task_graph)):
        errors.append("task dependency cycle: " + " -> ".join(cycle))

    if want_refs:
        for file, n in refs.get(want_refs, []):
            print(f"{file}:{n}")
        return 0

    for ref, sites in sorted(refs.items()):
        if ref not in defined:
            for file, n in sites:
                errors.append(f"unresolved reference '{ref}' at {file}:{n}")

    for ref, destination, source_file, line_number in linked_ids:
        if ref not in defined:
            continue
        try:
            parsed = urlsplit(html.unescape(destination))
        except ValueError:
            continue
        if parsed.scheme or parsed.netloc:
            continue
        target_path = unquote(parsed.path)
        if not target_path or Path(target_path).suffix.lower() != ".md":
            continue
        target = (Path(source_file).parent / target_path).resolve()
        defined_at = Path(defined[ref]).resolve()
        if target.is_file() and target != defined_at:
            errors.append(
                f"Markdown link for '{ref}' at {source_file}:{line_number} "
                f"targets {target}, but the ID is defined in {defined_at}"
            )

    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    print(f"-- files: {len(files)}, ids: {len(defined)}, "
          f"distinct refs: {len(refs)}, errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
