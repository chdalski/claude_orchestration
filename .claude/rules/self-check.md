# Self-Check After Blueprint Changes

After modifying blueprint files (CLAUDE.md, agents, rules,
workflows, knowledge, practices, templates), verify the
changes before considering the work complete. Unchecked
changes accumulate contradictions and stale references that
agents silently inherit — the cost compounds because every
future session trusts these files as ground truth.

## What to Check

### 1. Run the tests

Every blueprint has a test suite in its `tests/` directory.
Run `uv run pytest <blueprint>/tests/ -m static -v` after
changes. Tests catch structural regressions (missing files,
broken frontmatter, dynamic content in static files) that
are easy to introduce and hard to spot by reading.

### 2. Cross-file consistency

Read the files that overlap with what you changed and check
for:

- **Contradictions** — two files giving conflicting advice
  on the same topic (e.g., different priority orderings,
  conflicting style recommendations)
- **Redundancy** — the same paragraph or principle copied
  verbatim across multiple files. Duplicated content
  drifts when one copy is updated and others are not.
  State universal principles once and reference them.
- **Stale references** — mentions of files, directories,
  agents, or concepts that no longer exist or have been
  renamed

### 3. Rationale completeness

Per `reasoned-instructions.md`, every directive must include
its rationale. After writing new instructions, re-read each
one and ask: "Would an agent who has never seen this
codebase understand *why* this matters?" If not, add a
brief explanation.

### 4. Documentation alignment

If the change affects blueprint structure (new files, new
directories, renamed concepts):

- Update the root `CLAUDE.md` structure diagram
- Update the blueprint's `README.md`
- Update `blueprint_contracts.py` if required files or
  directories changed

### 5. Caching compliance

Rule files, CLAUDE.md, and agent definitions are cached at
session start (prompt cache level 3). They must not contain
dynamic content — dates, timestamps, counters, or version
numbers that change between sessions. The caching compliance
tests catch this, but awareness prevents the mistake.

## When to Skip

- Typo fixes in a single file with no cross-references
- Changes to `README.md` files (human-facing, no agent
  impact)
- Changes to test files only (they verify, they don't
  instruct)
