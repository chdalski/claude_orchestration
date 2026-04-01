# Contributing

How to develop and extend blueprints in this repository.
For usage instructions (copying a blueprint into a project),
see `README.md`. For deep design rationale, see each
blueprint's `CLAUDE.md` design reference.

## Blueprint Anatomy

A blueprint is a `.claude/` directory that gets copied into
a target project. It contains everything Claude Code needs
to run a coordinated multi-agent session:

```text
blueprints/<name>/
├── CLAUDE.md                ← Design reference (for working on the blueprint)
├── .claude/
│   ├── CLAUDE.md            ← Lead instructions (session behavior)
│   ├── settings.json        ← Agent teams config, plans directory
│   ├── agents/              ← Agent definitions (frontmatter + instructions)
│   ├── rules/               ← Unconditional + conditional rules
│   ├── skills/              ← Reusable procedures (with co-located templates)
│   ├── workflows/           ← Execution patterns (workflow blueprint only)
│   └── templates/           ← Canonical templates (workflow blueprint only)
└── tests/
    ├── blueprint_contracts.py  ← Single source of truth for structure
    ├── conftest.py
    └── static/              ← Structure, caching, agent tests
```

Two levels of `.claude/` exist: project-level (`/.claude/`)
is tooling for this repo and is never copied. Blueprint-level
(`blueprints/*/.claude/`) is what gets copied to target
projects.

## Design Conventions

These conventions are enforced by the rules in
`/.claude/rules/` and by the test suite. Understand them
before making changes.

**Reasoned instructions.** Every directive in a blueprint
markdown file must include its rationale — why the rule
exists or what breaks if it is ignored. Agents that
understand "why" apply rules correctly in novel situations.
See `.claude/rules/reasoned-instructions.md`.

**Agent design.** Agent files define role and capability
only. No named teammates, no workflow-specific coordination,
no sign-off sequences. Agents use "the requester" and "the
implementor" instead of specific names. Agent `name:` fields
use lowercase hyphenated form (`test-engineer`, not
`Test Engineer`). See `.claude/rules/agent-design.md`.

**Terminology.** Use Claude Code's official terms: "launch"
subagents, "create" teams, "spawn" teammates, "message"
within teams. See `.claude/rules/terminology.md`.

**Prompt caching.** All content at cache levels 1-4
(CLAUDE.md, rules, agent files) must be fully static. No
dates, counters, or version numbers. Dynamic content goes
in messages (level 5). See `.claude/rules/prompt-caching.md`.

**File length.** Rule files and CLAUDE.md files target under
200 lines (hard limit: 250). Agent adherence degrades beyond
that. If a file grows too large, split it into focused files
with appropriate `paths:` frontmatter.

**Simplicity.** KISS, YAGNI, fewest elements. Don't build
for hypothetical future requirements. See
`.claude/rules/simplicity.md`.

## Common Development Tasks

Each task below includes the typical set of files to touch.
Cross-reference with the real commits listed — they show
the actual diff patterns.

### Adding a Language Rule

Language rules provide guidance when agents touch files
with matching extensions. They load via Claude Code's
conditional rule mechanism (the `paths:` frontmatter).

**Files to create/modify (per blueprint):**

1. Create `.claude/rules/lang-<language>.md` with `paths:`
   frontmatter matching the language's file extensions
2. Add extensions to `functional-style.md` paths if the
   language supports FP well
3. Add extensions to `code-mass.md` and
   `code-principles.md` paths
4. Update the blueprint's design reference (`CLAUDE.md`)
   structure diagram
5. Run tests

If the rule exceeds 200 lines, split into focused files
(e.g., `lang-python.md`, `lang-python-patterns.md`,
`lang-python-testing.md`).

**Apply to both blueprints** — language rules are shared.

**Real examples:**
- `5da1b8e` — split Go, Python, and TypeScript rule files
  to comply with line limits
- `1cd182d` — split Rust rule and add benchmark-rust rule

### Adding a Workflow (workflow blueprint only)

Workflows are separate files in `.claude/workflows/`. Adding
one requires no changes to `CLAUDE.md` or agents.

**Files to create/modify:**

1. Create `.claude/workflows/<name>.md` following the format
   in `.claude/workflows/CLAUDE.md` (required sections: When
   to Use, Agents, Flow, Completion Criteria)
2. If the workflow needs a new agent, create it in
   `.claude/agents/` (see "Adding an Agent" below)
3. Update `blueprint_contracts.py` if new agents were added
4. Update root `README.md` with the new workflow
5. Run tests

**Real examples:**
- `7f948e5` — add TDD User-in-the-Loop workflow
- `1488da7` — add Develop-Review workflow (also added 4
  agents)

### Adding an Agent

Agents are general-purpose building blocks. They define
role and capability, not workflow coordination.

**Files to create/modify (per blueprint):**

1. Create `.claude/agents/<name>.md` with YAML frontmatter
   (`name`, `description`, `model`, `tools`) and markdown
   instructions
2. Add the agent to `blueprint_contracts.py` (`AGENT_FILES`,
   `AGENT_TOOLS`, `AGENT_MODELS`)
3. Reference the agent in the relevant workflow files
4. Update the blueprint's design reference structure diagram
5. Run tests

**Frontmatter example:**

```yaml
---
name: test-engineer
description: Designs test specifications and verifies coverage
model: sonnet
tools:
  - Read
  - Glob
  - Grep
  - Bash
  - SendMessage
---
```

**Real example:**
- `1488da7` — added developer, reviewer, test-engineer,
  and security-engineer agents together with the
  develop-review workflow

### Adding a Skill

Skills are reusable procedures invoked by the lead. Each
skill lives in its own directory under `.claude/skills/`.

**Files to create/modify (per blueprint):**

1. Create `.claude/skills/<name>/SKILL.md` with YAML
   frontmatter (`name`, `description`) and step-by-step
   instructions
2. Co-locate any templates the skill needs in the same
   directory (not in a separate `templates/` directory)
3. Add the skill directory to `REQUIRED_DIRECTORIES` and
   any required files to `REQUIRED_ROOT_FILES` in
   `blueprint_contracts.py`
4. Update the blueprint's design reference structure diagram
5. If the lead should invoke this skill, update
   `.claude/CLAUDE.md` with when and how to call it
6. Run tests

**Real example:**
- `e5c313c` — added the project-sanity skill with a
  github-sanity check

### Adding a Check to project-sanity

The project-sanity skill audits repos for common issues.
Each check is a co-located markdown file.

**Files to create/modify (per blueprint):**

1. Create `.claude/skills/project-sanity/<check>.md` with
   the check procedure
2. Add a detection trigger to `SKILL.md` (e.g., "if
   `codecov.yml` exists, read `codecov-sanity.md`")
3. Add the file to `REQUIRED_ROOT_FILES` in
   `blueprint_contracts.py`
4. Run tests

**Real example:**
- `3c903c8` — added codecov-sanity check

### Adding a Language-Specific Init

The project-init skill supports language-specific
initialization (e.g., Cargo lint config for Rust, TypeScript
strictness settings).

**Files to create/modify (per blueprint):**

1. Create `.claude/skills/project-init/<language>-init.md`
   with setup instructions
2. Add a corresponding step to `SKILL.md` that reads the
   file when that language is detected
3. Update the blueprint's design reference structure diagram

No other files need to change. See
`blueprints/*/skills/project-init/README.md` for details.

**Real examples:**
- `1ee6bef` — Rust-init: deny `expect_used` and
  `unwrap_used` in Cargo lints
- `2448caf` — TypeScript-init: compiler and lint strictness

### Adding an Unconditional Rule

Unconditional rules (no `paths:` frontmatter) load at
session start and apply to everything agents produce.

**Files to create/modify (per blueprint):**

1. Create `.claude/rules/<name>.md` without `paths:`
   frontmatter
2. Update the blueprint's design reference with the new
   rule in the rule system section
3. Run tests

**Real examples:**
- `c3593fa` — added procedural-fidelity rule (motivated by
  a production failure where a lead short-circuited a skill)
- `553f2d4` — added rule file line limit enforcement

## Cross-Blueprint Changes

Most changes apply to both blueprints (language rules,
skills, agent improvements). The convention is to make the
change in one blueprint and copy it to the other. The commit
messages use the `(v2,v3)` scope prefix to signal this.

Run tests for both blueprints after cross-blueprint changes:

```bash
uv run pytest blueprints/workflow/tests/ -m static -v
uv run pytest blueprints/autonomous/tests/ -m static -v
```

## Testing

Every blueprint has a test suite that verifies structural
integrity. Tests use pytest with the `-m static` marker.

```bash
# Install uv if needed
which uv || curl -LsSf https://astral.sh/uv/install.sh | sh

# Run tests for a specific blueprint
uv run pytest blueprints/workflow/tests/ -m static -v
uv run pytest blueprints/autonomous/tests/ -m static -v
```

### What Tests Verify

- **File structure** — required files and directories exist
- **Agent frontmatter** — names, models, and tool sets
  match contracts in `blueprint_contracts.py`
- **Caching compliance** — no dynamic content (dates,
  timestamps, counters) in static files
- **Settings** — required configuration keys are present
- **Rule file length** — all rule files under the line limit

### blueprint_contracts.py

This is the single source of truth for each blueprint's
expected structure. When you add files, agents, or required
settings, update this file first — the tests follow.

## Self-Check After Changes

After modifying blueprint files, verify (per
`.claude/rules/self-check.md`):

1. **Run the tests**
2. **Cross-file consistency** — no contradictions, no stale
   references, no redundant paragraphs
3. **Rationale completeness** — every directive explains why
4. **Documentation alignment** — root `CLAUDE.md` and
   `README.md` reflect current structure
5. **Rule file length** — target under 200 lines
6. **Caching compliance** — no dynamic content in static
   files
