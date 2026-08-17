#!/usr/bin/env python3
"""Loom: unified-phrasing + non-happy-path gate for UC Gherkin scenarios.

Reads docs/product/STEPS.md (STEP-* rows: Keyword | Phrase, `{placeholder}`
slots allowed) and every ```gherkin fenced block in docs/product/use-cases/UC-*.md.

Checks:
  - every Given/When/Then/And/But step line resolves to a STEPS.md phrase
    (exact match modulo {placeholder} slots)
  - a step line that is a near-rewording of a registered phrase (not exact,
    but similar) is flagged instead of silently accepted as "new" — the two
    should be one phrase, reused
  - every UC has at least one Extension tagged [error] or [boundary] — a
    use case with only [alternate] (or untagged) extensions is happy-path-only

Usage:
  gherkin_lint.py            report findings
  gherkin_lint.py --gate     exit 1 if any finding
"""
import re
import sys
from pathlib import Path

STEPS = Path("docs/product/STEPS.md")
USE_CASES = Path("docs/product/use-cases")

STEP_ROW_RE = re.compile(
    r"^\|\s*(STEP-[a-z0-9][a-z0-9-]*[a-z0-9])\s*\|\s*(Given|When|Then)\s*\|\s*(.+?)\s*\|$",
    re.IGNORECASE,
)
GHERKIN_LINE_RE = re.compile(r"^(Given|When|Then|And|But)\s+(.+)$", re.IGNORECASE)
EXTENSION_TAG_RE = re.compile(r"^\s*-\s*\*\*.+?\[(alternate|error|boundary)\]\*\*", re.IGNORECASE)

NEAR_DUPLICATE_OVERLAP = 0.6  # share of a phrase's literal (non-{slot}) words found in the step line


def phrase_to_pattern(phrase):
    """Turn a catalog phrase into a regex: literal text escaped, {slot} -> wildcard."""
    parts = re.split(r"(\{[a-zA-Z0-9_]+\})", phrase)
    pattern = "".join(
        r"(.+?)" if p.startswith("{") and p.endswith("}") else re.escape(p)
        for p in parts
    )
    return re.compile("^" + pattern + "$", re.IGNORECASE)


def literal_words(phrase):
    """Words in a catalog phrase outside its {slot}s — the part that must not drift."""
    stripped = re.sub(r"\{[a-zA-Z0-9_]+\}", " ", phrase)
    return set(re.findall(r"[a-z0-9]+", stripped.lower()))


def load_steps():
    steps, errors = [], []
    if not STEPS.exists():
        return steps, [f"{STEPS} does not exist — create it from templates/steps.md"]
    for line in STEPS.read_text(encoding="utf-8").splitlines():
        m = STEP_ROW_RE.match(line.strip())
        if m:
            sid, keyword, phrase = m.groups()
            if "{topic}" in sid or "..." in phrase:
                continue  # template placeholder row, not a real entry
            steps.append({
                "id": sid, "keyword": keyword.title(), "phrase": phrase,
                "pattern": phrase_to_pattern(phrase),
                "literal": literal_words(phrase),
            })
    return steps, errors


def gherkin_blocks(text):
    return re.findall(r"```gherkin\n(.*?)```", text, re.DOTALL)


def check_uc(f, text, steps):
    findings = []
    for block in gherkin_blocks(text):
        for raw_line in block.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            m = GHERKIN_LINE_RE.match(line)
            if not m:
                continue
            _, body = m.groups()
            if any(s["pattern"].match(body) for s in steps):
                continue
            body_words = set(re.findall(r"[a-z0-9]+", body.lower()))

            def overlap(s):
                return len(s["literal"] & body_words) / len(s["literal"]) if s["literal"] else 0

            best = max(steps, key=overlap, default=None)
            ratio = overlap(best) if best else 0
            if best and ratio >= NEAR_DUPLICATE_OVERLAP:
                findings.append(
                    f"{f}: step '{line}' shares {ratio:.0%} of its wording with "
                    f"{best['id']} '{best['phrase']}' but doesn't match it exactly — "
                    f"reuse that phrase instead of rewording"
                )
            else:
                findings.append(
                    f"{f}: step '{line}' does not resolve to any STEPS.md phrase — "
                    f"register it in STEPS.md before use"
                )

    tags = [m.group(1).lower() for m in
            (EXTENSION_TAG_RE.match(l) for l in text.splitlines()) if m]
    if not any(t in ("error", "boundary") for t in tags):
        findings.append(f"{f}: no [error] or [boundary] extension — happy-path-only")
    return findings


def main(argv):
    steps, errors = load_steps()
    for f in sorted(USE_CASES.glob("UC-*.md")):
        text = f.read_text(encoding="utf-8")
        errors += check_uc(f, text, steps)

    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    print(f"-- steps: {len(steps)}, use cases scanned: "
          f"{len(list(USE_CASES.glob('UC-*.md')))}, findings: {len(errors)}")
    return 1 if ("--gate" in argv and errors) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
