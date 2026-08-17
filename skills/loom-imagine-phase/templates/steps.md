---
id: STEPS
status: draft
owner: pair
updated: {date}
---
# Gherkin step catalog

The single source of truth for Given/When/Then phrasing. Before writing a new
step in any `UC-*.md`, check here first — reusing a registered phrase means
the engine writes (or generates) one step definition instead of N near-duplicates
for N slightly different wordings of the same fact. `scripts/loom/gherkin_lint.py`
enforces this: every step in every UC's Gherkin block must resolve to a row
here, exactly or via its `{placeholder}` slots.

`{placeholder}` marks the only part of the phrase allowed to vary — everything
else must match verbatim, glossary terms only.

| ID | Keyword | Phrase |
|---|---|---|
| STEP-{topic} | Given | {actor} is logged in as {role} |
| STEP-{topic} | When | {actor} {does action} with {input} |
| STEP-{topic} | Then | {system} {observable outcome} |

Rules:
- One row per distinct fact/action — do not add a second row that only
  rewords an existing one (e.g. "the user has logged in" vs "the user is
  logged in"); pick one and reuse it everywhere.
- A step that needs a genuinely new fact gets a new row here in the same
  change that introduces it in a UC — never inline a step that isn't
  registered.
- Renaming a phrase is a breaking change to every UC that uses it: update all
  call sites in the same commit, `gherkin_lint.py --gate` catches stragglers.

## Open questions
- [ ] OQ-steps-{topic}: ...
