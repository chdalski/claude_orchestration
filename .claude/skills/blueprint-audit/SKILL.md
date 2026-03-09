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
   blueprint to audit — list the `blueprint_*` directories
   in the repo root.

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
- `<blueprint>/README.md` (user-facing docs)
- All files in `<blueprint>/.claude/agents/`
- All files in `<blueprint>/.claude/workflows/`
- All files in `<blueprint>/.claude/rules/`
- All files in `<blueprint>/.claude/templates/`
- Root `/CLAUDE.md` (project-level description)

**What to look for:**

### 2a — Contradictions

Two files giving conflicting guidance on the same topic.
Common patterns:
- Agent role described differently in the agent file vs.
  the workflow file vs. the lead instructions
- Communication mechanism described inconsistently (e.g.,
  one file says `SendMessage`, another says `TaskOutput`
  for the same agent type)
- Different agent lists in the lead instructions vs.
  workflow files vs. README
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
  `.claude/workflows/*.md` filenames
- References to removed sections or renamed concepts
- Structure diagrams (code trees) that don't match actual
  directory layout

### 2c — Terminology Drift

Inconsistent terminology across files for the same concept.
Common patterns:
- "spawn" vs. "create" vs. "start" for agent creation —
  pick one per mechanism (`TeamCreate` = "create a team",
  `Agent` tool = "spawn")
- "shared" vs. "session-start" vs. "utility" for
  non-workflow agents
- "workflow-specific" vs. "team" vs. "workflow" for agents
  listed in workflow files
- Agent role labels differing between workflow tables and
  agent definition files

### 2d — Redundancy

The same instruction or principle repeated verbatim across
multiple files. Duplicated content drifts when one copy is
updated and the others are not. Flag instances where the
same paragraph or directive appears in more than one file.
State-once-reference-elsewhere is the correct pattern.

---

## Check 3 — Rationale Completeness

**Reference:** `.claude/rules/reasoned-instructions.md`

For every directive, constraint, or recommendation in the
blueprint's instruction files, check: does it include its
rationale? A directive without a "why" tells agents what to
do but gives no basis for judgment in novel situations.

Focus on recently changed or added directives — these are
most likely to be missing rationale. Skip well-established
sections that clearly include rationale.

Report directives that lack rationale, grouped by file.

---

## Check 4 — Documentation Alignment

Check that the three documentation layers agree:

1. **Root `/CLAUDE.md`** — project-level blueprint
   description (agent list, workflow list, structure
   diagram)
2. **`<blueprint>/CLAUDE.md`** — design reference
   (component architecture, how components relate,
   structure diagram)
3. **`<blueprint>/README.md`** — user-facing docs (agent
   table, workflow descriptions, setup instructions)

For each, verify:
- Agent lists match the actual `.claude/agents/` contents
- Workflow lists match the actual `.claude/workflows/`
  contents (excluding `CLAUDE.md` format guide)
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

**Read:** The lead's `.claude/CLAUDE.md` and all workflow
files in `.claude/workflows/`.

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

For each process gate in the lead instructions (clarification,
workflow selection, planning trigger), check whether it is
stated as a **per-task** requirement or only as a
**startup-sequence** step.

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
[List inconsistent terms with file locations,
 or "None found"]

### Redundancy
[List duplicated content with file locations,
 or "None found"]

## Rationale Completeness
[List directives missing rationale, grouped by file,
 or "All directives include rationale"]

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
