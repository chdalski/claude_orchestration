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
- Update the root `README.md` blueprint section
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

### 7. Procedural short-circuit resistance

When writing multi-step procedures (skills, checklists,
agent workflows), check whether an early step produces
observable state that could make later steps *seem*
redundant — even though later steps are unconditional.

The pattern: step N checks or creates something (a
directory exists, a config key is present, a file is
found). Steps N+1..M act on that state but must always
execute regardless of step N's outcome. An agent under
optimization pressure treats step N's success as proof
that everything is current and skips to "done."

For each multi-step procedure, ask:

- If an agent executes only step 1 and declares success,
  what breaks? If something breaks, the procedure is
  vulnerable.
- Are later steps marked as unconditional with language
  that cannot be read as conditional? Words like "ensure,"
  "verify," and "check" imply conditionality — "always
  write," "execute every time," and "not conditional" are
  harder to skip.
- Does the procedure include a preamble stating that all
  steps are mandatory? Agents pattern-match against
  structure — a bold preamble before the steps list is
  harder to skip than a rationale sentence buried in a
  step description.

This check exists because a production session
short-circuited `/ensure-ai-dirs` by treating "config
key found" (step 1) as sufficient, skipping the format
guide overwrite (step 2), and producing four plans with
a stale template.

### 8. Rule file length

Rule files and CLAUDE.md files should target under 200
lines each. Beyond that threshold, agent adherence
degrades — Claude is less likely to follow every directive
in a long file. The static tests enforce a hard ceiling at
250 lines, but 200 is the target.

**This does not apply to agent files** (`agents/*.md`).
Agent files are procedurally dense — numbered steps,
checklists, handoff protocols — and splitting them would
fragment a single agent's instructions across files,
hurting coherence. The static tests confirm this scope:
`test_rule_file_length.py` only checks `rules/*.md`.

After creating or expanding a rule file, check `wc -l` on
the result. If it exceeds 200 lines, split it into focused
files with appropriate `paths:` frontmatter. Code-heavy
files (language idioms with inline examples) may land
slightly above 200 — that is acceptable if the content is
cohesive and cannot be split without losing context.

### 9. Handoff coverage

If the change affects a multi-agent pipeline (agent
responsibilities, handoff messages, verification steps),
run the analysis described in `handoff-coverage.md`. For
each guarantee the pipeline should provide, verify that
a specific agent owns the check and receives sufficient
input. Gaps in handoff coverage are invisible during
normal operation — they only surface when a real task
hits the uncovered case.

### 10. Caching compliance

Rule files, CLAUDE.md, and agent definitions are cached at
session start (prompt cache level 3). They must not contain
dynamic content — dates, timestamps, counters, or version
numbers that change between sessions. The caching compliance
tests catch this, but awareness prevents the mistake.

## When to Skip

- Typo fixes in a single file with no cross-references
- Changes to the root `README.md` (human-facing, no agent
  impact)
- Changes to test files only (they verify, they don't
  instruct)
