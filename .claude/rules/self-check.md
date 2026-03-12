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

### 5. Procedural redundancy across agents

For each setup or preparation step in an agent's
instructions, ask: is this step already guaranteed to be
done by a preceding agent in the same workflow, or by
Claude Code automatically (e.g., via `settings.json`,
auto-loaded `CLAUDE.md` files)?

If yes, the step is redundant — remove it from the
downstream agent. Redundant setup steps create unclear
ownership: if two agents both "ensure" the same
precondition, neither truly owns it, and future changes to
the setup logic must be made in multiple places.

Common patterns to catch:
- An agent runs a skill that an earlier agent already ran
  in the same workflow
- An agent verifies a precondition (directory exists,
  format guide loaded) that Claude Code handles
  automatically based on `settings.json` or file naming
  conventions (e.g., files named `CLAUDE.md` are loaded
  into context automatically)
- An agent re-reads or re-checks state that was already
  established and hasn't changed since

### 6. Hardcoded configuration values

Any path, directory name, or setting that is owned by
`settings.json` must not be hardcoded in agent or skill
files — if `settings.json` changes, hardcoded copies break
silently and the agent uses a stale value.

After writing or editing agent or skill instructions, check:
does any path or name in the instructions match a key in
`settings.json` (e.g., `plansDirectory`)? If so, the
instruction should tell the agent to read from
`settings.json`, not reproduce the value inline.

### 7. Caching compliance

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
