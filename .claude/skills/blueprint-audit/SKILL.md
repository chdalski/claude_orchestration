---
name: blueprint-audit
description: Audit a blueprint for cross-file consistency, stale references, contradictions, rationale completeness, and documentation alignment. Returns a structured report with specific findings and fixes.
---

# Blueprint Audit Skill

**Trigger:** `/blueprint-audit` or "audit the blueprint" or "check blueprint consistency"

**What it does:** Reads all files in a blueprint directory, cross-references claims across files, runs static tests, and produces a structured report of contradictions, stale references, gaps, and terminology drift.

---

## When Invoked

1. Determine which blueprint to audit. If the user specifies
   one (e.g., "audit v2"), use that. If not, ask which
   blueprint to audit — list the directories under
   `blueprints/`.

2. Run all checks below in order. Read all files before
   reporting — findings often require cross-referencing
   multiple files to confirm.

3. Produce the full report in one pass.

---

## Check 1 — Static Tests

**Run:** `uv run pytest <blueprint>/tests/ -m static -v`

Report the result count (passed/failed/skipped). If any
tests fail, list them with their failure reason. Static
tests catch structural regressions (missing files, broken
frontmatter, dynamic content in cached files) that are
mechanical to detect.

---

## Check 2 — Cross-File Consistency

**Read:** Every file that agents consume as instructions:
- `<blueprint>/.claude/CLAUDE.md` (lead instructions)
- `<blueprint>/CLAUDE.md` (design reference)
- Root `/README.md` (user-facing docs — consolidated for
  all blueprints)
- All files in `<blueprint>/.claude/agents/`
- All files in `<blueprint>/.claude/workflows/` (if present)
- All files in `<blueprint>/.claude/rules/`
- All files in `<blueprint>/.claude/templates/`
- Root `/CLAUDE.md` (project-level description)

**What to look for:**

### 2a — Contradictions

Two files giving conflicting guidance on the same topic.
Common patterns:
- Agent role described differently in the agent file vs.
  the lead instructions (or workflow file, if present)
- Communication mechanism described inconsistently (e.g.,
  one file says `SendMessage`, another says `TaskOutput`
  for the same agent type)
- Different agent lists in the lead instructions vs.
  README (or workflow files, if present)
- Conflicting lifecycle descriptions (who creates whom,
  when agents are created, how they communicate)

### 2b — Stale References

Mentions of files, directories, agents, sections, or
concepts that no longer exist or have been renamed.
Common patterns:
- File paths in prose that don't match the actual
  filesystem (use Glob to verify)
- Agent names that don't match `.claude/agents/*.md`
  filenames
- Workflow names that don't match
  `.claude/workflows/*.md` filenames (if present)
- References to removed sections or renamed concepts
- Structure diagrams (code trees) that don't match actual
  directory layout

### 2c — Terminology Drift

**Reference:** `/.claude/rules/terminology.md`

Read the terminology rule's Quick Reference table. For each
term defined there, search the blueprint's instruction files
for non-canonical synonyms. The rule lists correct terms,
"do not use" alternatives, and which tool/mechanism each
term maps to.

**How to check:**

1. Read `/.claude/rules/terminology.md` to get the current
   glossary (terms, correct usage, and banned synonyms).
2. For each entry's "do not use" list, search the
   blueprint's files for those banned synonyms. Also search
   for common informal alternatives not explicitly listed
   (e.g., "kick off", "fire up", "spin up", "ping",
   "notify", "hand off to [named agent]").
3. Verify that agent files use role-neutral references
   ("the requester", "the implementor") instead of naming
   specific teammates — per both `terminology.md` and
   `agent-design.md`.

**Additional patterns to check:**
- "shared" vs. "session-start" vs. "utility" for
  non-workflow agents
- "workflow-specific" vs. "team" vs. "workflow" for agents
  listed in workflow files (if present)
- Agent role labels differing between workflow tables and
  agent definition files

Report each violation with the file, the term used, and the
correct term from the glossary.

### 2d — Redundancy

The same instruction or principle repeated verbatim across
multiple files. Duplicated content drifts when one copy is
updated and the others are not. Flag instances where the
same paragraph or directive appears in more than one file.
State-once-reference-elsewhere is the correct pattern.

---

## Check 3 — Rationale Completeness

**Reference:** `.claude/rules/reasoned-instructions.md`

Check whether directives that *need* rationale have it.
Not every instruction benefits — rationale matters when it
would change how an agent applies the rule:

- **Non-obvious failure modes** — the instruction exists
  because of a specific incident or edge case not
  predictable from the rule alone
- **Conflicting instructions** — two principles pull in
  opposite directions and the agent needs a priority
  framework
- **Steps that appear skippable** — an instruction looks
  redundant but isn't; without rationale, an agent under
  optimization pressure skips it

Do not flag simple mechanical rules ("use lowercase names"),
well-known practices ("validate external input"), or
unambiguous directives with no edge cases.

Report directives that need rationale but lack it, grouped
by file.

---

## Check 4 — Documentation Alignment

Check that the three documentation layers agree:

1. **Root `/CLAUDE.md`** — project-level blueprint
   description (agent list, workflow list, structure
   diagram)
2. **`<blueprint>/CLAUDE.md`** — design reference
   (component architecture, how components relate,
   structure diagram)
3. **Root `/README.md`** — user-facing docs (blueprint
   summaries, agent tables, setup instructions)

For each, verify:
- Agent lists match the actual `.claude/agents/` contents
- Workflow lists match the actual `.claude/workflows/`
  contents, if present (excluding `CLAUDE.md` format guide)
- Structure diagrams match the actual directory layout
- Agent role descriptions are consistent across all three

---

## Check 5 — Agent Tool Coherence

For each agent in `.claude/agents/`:

1. Read the frontmatter tool list
2. Read the agent's instructions
3. Check: does the agent's instructions reference tools
   it doesn't have? (e.g., instructions say "use Bash"
   but Bash isn't in the tool list)
4. Check: does the agent have tools it never references
   in its instructions? (not necessarily wrong — tools
   may be used implicitly — but worth flagging as an
   observation)

---

## Check 6 — Workflow-Agent Alignment

Skip if the blueprint has no `.claude/workflows/` directory.

For each workflow in `.claude/workflows/`:

1. Read the workflow's Agents table
2. Verify every listed agent has a corresponding file in
   `.claude/agents/`
3. Verify the role description in the workflow table is
   consistent with the agent's own role description
4. Check the Team Lifecycle section: does it list all
   agents from the Agents table?
5. Check the Flow section: does every agent mentioned in
   the flow appear in the Agents table?

---

## Check 7 — Instruction Gap Audit

The previous checks verify what the instructions *say*. This
check looks for what they *don't say* — gaps that let an
agent rationalize skipping a required step by interpreting
ambiguous language in its favor.

**Read:** The lead's `.claude/CLAUDE.md` and workflow
files in `.claude/workflows/` (if present).

### 7a — Judgment-call language

Scan for magnitude qualifiers and category boundary terms
that leave thresholds undefined:

- **Magnitude qualifiers:** `trivial`, `non-trivial`,
  `simple`, `obvious`, `mechanical`, `small`, `basic`,
  `minor`
- **Category boundary terms:** `non-code`, `configuration`,
  `documentation`, `code work`, `directly`

For each instance, check whether the surrounding text
provides a bright-line definition or concrete examples.
Flag any that rely on the agent's judgment to place the
boundary — undefined thresholds become rationalization
paths under pressure.

### 7b — Gate scope

For each process gate in the lead instructions (e.g.
clarification, planning trigger, or any gate the blueprint
defines), check whether it is stated as a **per-task**
requirement or only as a **startup-sequence** step.

A gate described solely in a Startup section, without an
explicit per-task statement elsewhere, is a gap — agents
internalize startup sequences as one-time rituals and do
not re-enter them mid-session when a new task begins.

### 7c — Exception language

Scan for exception clauses: `except for`, `unless`,
`when it's`, `directly`, or any phrasing that carves out
cases from a general rule.

For each exception, verify it is narrowly and concretely
scoped — not a judgment-call qualifier broad enough that
the agent could rationalize the main case into it. If the
exception boundary is fuzzy, flag it.

### 7d — Procedural short-circuit risk

**Read:** All skill files (`<blueprint>/.claude/skills/*/SKILL.md`),
lead instructions (`.claude/CLAUDE.md`), and workflow files
(`.claude/workflows/*.md`, if present).

Scan for multi-step procedures (numbered step lists, phase
sequences, checklists). For each procedure:

1. Identify whether an early step produces observable state
   (directory exists, config key found, file present, build
   passes).
2. Check whether later steps are unconditional — they must
   execute regardless of the early step's outcome.
3. If later steps are unconditional but the language does
   not make this explicit, flag it. An agent under
   optimization pressure will treat the early step's
   success as proof that everything is current and skip
   the rest.

**Vulnerable patterns to flag:**

- A step that reads/checks state followed by a step that
  writes/overwrites, with no explicit "always" or
  "unconditional" marker on the write step.
- Steps using conditional-sounding verbs (`ensure`,
  `verify`, `check if`) for actions that must always
  execute — these verbs imply "skip if already done."
- Procedures missing a preamble that states all steps are
  mandatory — without it, agents treat early steps as
  gates that can short-circuit the rest.

**Not vulnerable (do not flag):**

- Steps that are genuinely conditional (e.g., "if the key
  is absent, create it").
- Procedures where later steps explicitly depend on early
  step outputs (natural data flow, not skippable).

Report each vulnerable procedure with the file, step
numbers, and what an agent could skip.

---

## Check 8 — Configuration Coupling

**Read:** `<blueprint>/.claude/settings.json`

For each key that specifies a path or name (e.g.,
`plansDirectory`), search all agent files, skill files, and
workflow files for hardcoded occurrences of that value
using Grep.

If a hardcoded string matches a configurable value in
`settings.json`, it is a coupling violation — changing the
setting breaks any agent that hardcoded the old value
instead of reading from the config. The agent will silently
use the wrong path.

Report each violation with the file, the hardcoded value,
and which `settings.json` key owns it.

Add to the output report under a **Configuration Coupling**
section:
- List each violation, or "None found"

---

## Check 9 — Rule File Length

**Read:** All `.md` files in `<blueprint>/.claude/rules/`.

For each rule file, count the lines (`wc -l` or equivalent).
The documented recommendation is under 200 lines per file —
beyond that, agent adherence degrades.

**Severity levels:**

- **Over 250 lines** — hard violation. The static tests
  enforce this ceiling. Must be split before merging.
- **201–250 lines** — warning. Acceptable for code-heavy
  files (language idioms with inline examples) but should
  be reviewed for split opportunities.
- **Under 200 lines** — no action needed.

Report each file with its line count, grouped by severity.
If all files are under 200 lines, report "All rule files
within target."

---

## Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  BLUEPRINT AUDIT: <blueprint_name>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Static Tests
[X passed, Y failed, Z skipped]
[List failures if any]

## Cross-File Consistency

### Contradictions
[List each with the two files and what they disagree on,
 or "None found"]

### Stale References
[List each with the file, the reference, and what's
 actually there, or "None found"]

### Terminology Drift
[List each non-canonical term with the file, line, the term
 used, and the correct term from the glossary,
 or "None found"]

### Redundancy
[List duplicated content with file locations,
 or "None found"]

## Rationale Completeness
[List directives that need rationale but lack it, grouped
 by file, or "No gaps found"]

## Documentation Alignment
[List mismatches between the three doc layers,
 or "All documentation layers agree"]

## Agent Tool Coherence
[List mismatches between tool lists and instructions,
 or "All agent tools align with instructions"]

## Workflow-Agent Alignment
[List mismatches between workflow tables and agent files,
 or "All workflows align with agent definitions"]

## Instruction Gap Audit

### Judgment-Call Language
[List each flagged term with file location and whether a
 bright-line definition exists nearby, or "None found"]

### Gate Scope
[List each gate that is only described at startup without
 a per-task statement, or "All gates are per-task"]

### Exception Language
[List each exception clause with file location and whether
 it is narrowly scoped, or "None found"]

### Procedural Short-Circuit Risk
[List each vulnerable procedure with file, step numbers,
 and what an agent could skip, or "None found"]

## Configuration Coupling
[List each hardcoded value that settings.json owns, with
 file location and the key it should read instead,
 or "None found"]

## Rule File Length
[List files over 250 as violations, 201-250 as warnings,
 or "All rule files within target"]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  OBSERVATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Items that aren't wrong but are worth noting — unused
 tools, asymmetric patterns, potential simplifications]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TOP FIXES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Ranked list of the most impactful changes, with specific
 file paths and what to change]
```
