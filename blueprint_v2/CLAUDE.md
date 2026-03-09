# Blueprint v2 — Design Reference

This file describes how the blueprint is designed and why.
It targets sessions working *on* the blueprint (adding
rules, workflows, agents). For user-facing setup and usage, see
`README.md`. For lead behavior during a session, see
`.claude/CLAUDE.md`.

## Philosophy

### Clarify-first

Every session starts with clarification. The lead
understands the task through structured dialogue with the
user, then presents workflow options. The user chooses how
work gets done — Solo for simple tasks, Develop-Review (Supervised or
Autonomous) or TDD for complex ones. Planning via the Architect happens
when the user selects a workflow that needs it, not as a
forced default.

### Workflow-agnostic

The blueprint does not prescribe how code gets written. It
defines a clarification phase and a set of agents, then
defers execution to workflow files. Each workflow defines
its own agents, step order, and completion criteria. Adding
a new workflow requires no changes to CLAUDE.md, agents, or
rules — just a new file in `.claude/workflows/`.

This means the blueprint intentionally excludes:

- **Specific architectures** (hexagonal, clean, etc.) —
  these are project choices, not blueprint concerns
- **Specific testing approaches** (test-list, TDD, etc.) —
  these belong in workflow definitions
- **Specific design philosophies** beyond universal
  principles — SOLID and Kent Beck's rules are included
  because they are broadly accepted; opinionated choices
  belong in the target project's CLAUDE.md

### User-driven workflow choice

The lead always clarifies the task, then presents workflow
options to the user via `AskUserQuestion`. The user decides
how work gets done — not the lead. This replaces auto-triage
(where the lead decided scope and chose the response level),
which was unreliable because the lead's scope assessment
could be wrong, and users had no control over the process
until they explicitly overrode it.

### File-triggered guidance

Language-specific and topic-specific knowledge loads
automatically via Claude Code's conditional rule mechanism.
Agents don't need startup instructions to load knowledge
files — touching a `.py` file loads Python guidance,
touching a `.rs` file loads Rust guidance. This solves
three problems from the v1 approach:

1. Agents can't forget to load relevant guidance
2. Irrelevant guidance stays out of context (saves tokens)
3. Adding a new language is just adding a file

## Component Architecture

```text
blueprint_v2/
├── CLAUDE.md              ← You are here (design reference)
├── README.md              ← Human-facing setup and usage
├── .claude/
│   ├── CLAUDE.md          ← Lead instructions (session behavior)
│   ├── settings.json      ← Agent teams
│   ├── agents/            ← Agent definitions (frontmatter + instructions)
│   │   ├── architect.md   ← Reads codebase, writes plans, feeds tasks
│   │   ├── developer.md   ← Implements all code (source + tests)
│   │   ├── reviewer.md    ← Independent quality gate + commits approved work
│   │   ├── security-engineer.md ← Advisory — security assessment
│   │   └── test-engineer.md     ← Advisory — test design + verification
│   ├── skills/            ← Skill definitions (preloaded into agents)
│   │   ├── ensure-plans-dir/
│   │   │   └── SKILL.md   ← Create .ai/plans/ and format guide if missing
│   │   └── project-init/
│   │       └── SKILL.md   ← Project scanning + context generation
│   ├── rules/             ← Unconditional + conditional rules
│   │   ├── simplicity.md         ← [unconditional] KISS, YAGNI, etc.
│   │   ├── code-principles.md    ← [conditional: source files] SOLID, Kent Beck
│   │   ├── lang-typescript.md    ← [conditional: *.ts, *.tsx]
│   │   ├── lang-python.md        ← [conditional: *.py]
│   │   ├── lang-go.md            ← [conditional: *.go]
│   │   ├── lang-rust.md          ← [conditional: *.rs]
│   │   ├── functional-style.md   ← [conditional: *.ts, *.py, *.rs]
│   │   ├── documentation.md      ← [conditional: README*, docs/**]
│   │   ├── code-mass.md          ← [conditional: source files]
│   ├── templates/         ← Canonical templates copied at runtime
│   │   ├── plan-format.md ← Plan format guide (copied to .ai/plans/ by /ensure-plans-dir)
│   │   └── project-context.md ← Project context template (filled by /project-init)
│   └── workflows/         ← Workflow definitions
│       ├── CLAUDE.md      ← Workflow format guide + session-start agents
│       ├── develop-review-supervised.md ← Dev-team + review (user approves commits)
│       ├── develop-review-autonomous.md ← Dev-team + review (auto-commit after Reviewer)
│       ├── solo.md        ← Lead handles work + Reviewer quality gate
│       └── tdd-user-in-the-loop.md ← Strict Red-Green-Refactor with user approval
└── tests/                 ← Blueprint verification tests
    ├── blueprint_contracts.py  ← Single source of truth for structure
    ├── conftest.py             ← Shared fixtures + helpers
    ├── static/                 ← Structure, caching, agent tests
    ├── behavioral/             ← SDK-based runtime tests
    └── fixtures/
        └── minimal_project/    ← Minimal project for behavioral tests
```

### How Components Relate

**Lead instructions** (`.claude/CLAUDE.md`) define session
behavior — startup sequence, clarification flow, workflow
proposal, agent coordination. The lead is the only agent
with user access.

**Agent definitions** (`.claude/agents/*.md`) specify each
agent's model, tools, and instructions via YAML frontmatter
and markdown body. The frontmatter is machine-parsed by
Claude Code; the body is the agent's instruction set.
All agents are general-purpose building blocks — no agent
runs automatically. Each workflow declares which agents it
needs in its Agents table. For multi-agent workflows, the
lead creates a team via `TeamCreate` with all listed agents.
For Solo, the lead creates a one-agent team with the
Reviewer via `TeamCreate` so it can receive the commit
signal after the user checkpoint.

**Skills** (`.claude/skills/*/SKILL.md`) define reusable
procedures. Agents preload them via the `skills` frontmatter
field; the lead invokes them autonomously when the
conversation context matches. Currently: `ensure-plans-dir`
(preloaded into the Architect — creates `.ai/plans/` and its
format guide on first use) and `project-init` (invoked by
the lead at startup if `CLAUDE.md` is missing, and
user-invocable to regenerate context).

**Rules** (`.claude/rules/*.md`) provide guidance that
Claude Code injects into agent context automatically.
Unconditional rules load at session start; conditional
rules load when agents touch matching files. Rules are
independent of agents and workflows — they apply to any
agent in any workflow that touches a matching file.

**Workflows** (`.claude/workflows/*.md`) define execution
patterns — which agents are needed, what order they work
in, where user checkpoints go. The lead reads these at
runtime and presents options to the user. Workflows
reference agents but do not define them.

**Templates** (`.claude/templates/*.md`) are canonical
source files that get copied to their runtime locations by
skills. Currently: `plan-format.md` (copied to
`.ai/plans/CLAUDE.md` by `/ensure-plans-dir`) and
`project-context.md` (filled by `/project-init` and written
to the project root as `CLAUDE.md`). Templates ship with
the `.claude/` directory so users don't need to remember
to copy additional directories.

**Plans** (`.ai/plans/*.md`) are runtime artifacts written
by the Architect during a session. They capture the goal,
context, steps, task decomposition, and decisions. Plans
are committed to git as decision records — they survive
across sessions and help future sessions resume work.

**Tests** (`tests/`) verify the blueprint's structural
integrity: required files exist, agent frontmatter matches
contracts, static files contain no dynamic content. Tests
run against the blueprint itself, not against target
projects.

## Rule System Design

### Two tiers

**Unconditional** (no `paths:` frontmatter) — loaded at
session start, always in context. Use for principles that
apply to everything agents produce, regardless of file
type. Currently: `simplicity.md`.

**Conditional** (with `paths:` frontmatter) — loaded only
when agents touch matching files. Use for guidance that is
specific to a file type, language, or context. All other
rules.

### What goes where

| Guidance Type | Location | Rationale |
|---|---|---|
| Universal principles (KISS, YAGNI) | Unconditional rule | Applies before any files are touched — during planning, docs, config |
| Code-specific principles (SOLID, testing) | Conditional rule on source files | Only relevant when writing code |
| Language idioms + testing | Conditional rule on language extension | Only relevant for that language |
| Cross-language patterns (FP, code mass) | Conditional rule on applicable extensions | Avoids loading irrelevant guidance |
| Project-specific conventions | `CLAUDE.md` at project root (generated by `/project-init`) | Detected from manifests + user-curated sections |
| Workflow-specific practices | Workflow definition file | Tied to a specific execution pattern |
| Formatting commands, CI config | Target project's CLAUDE.md or pre-commit hooks | Project-specific tooling |

### Avoiding redundancy

Universal principles are stated once in the highest
applicable tier. Language rules reference them by behavior
(e.g., showing language-specific test patterns) but do not
restate the universal principle. This prevents drift when
one copy is updated and others are not.

Example: test independence is stated once in
`code-principles.md`. Language rules show
language-specific test patterns (pytest fixtures,
table-driven tests, `#[cfg(test)]` modules) without
repeating the independence principle.

### Adding a new language

1. Create `.claude/rules/lang-<language>.md`
2. Add `paths:` frontmatter with the language's file
   extensions
3. Include language idioms, type system, error handling,
   testing patterns, tooling, and common pitfalls
4. Add the language's extensions to `functional-style.md`
   paths if the language supports FP well (skip for
   pragmatic languages like Go)
5. Add the language's extensions to `code-mass.md` and
   `code-principles.md` paths
6. Update `README.md` and root `CLAUDE.md` structure
   diagram
7. Run `uv run pytest blueprint_v2/tests/ -m static -v`

No changes to `.claude/CLAUDE.md`, agents, or workflows.

### Adding a new workflow

1. Create `.claude/workflows/<name>.md` following the
   format in `.claude/workflows/CLAUDE.md`
2. Define which agents the workflow needs — reference
   existing agents from `.claude/agents/` (e.g., Architect,
   Developer, Reviewer) and define new agents if needed
3. If new agents are added, update `blueprint_contracts.py`
   with their expected frontmatter
4. Run tests

No changes to `.claude/CLAUDE.md` or existing rules.

See `develop-review-supervised.md` for a concrete example — it uses
five workflow-specific agents (Architect, Developer, Test
Engineer, Security Engineer, Reviewer).

## Prompt Caching Alignment

The blueprint aligns with Claude Code's prompt caching
architecture (see repo-level
`.claude/rules/prompt-caching.md`):

- **Level 3 (CLAUDE.md + rules)** — all files are fully
  static. No dates, counters, or changing data. Enforced
  by caching compliance tests.
- **Tool set stability** — each agent has a fixed tool set
  in its frontmatter. No conditional tool loading.
  `settings.json` has no hooks that alter tools.
- **Model delegation** — agents are subagents (separate
  conversations), not model switches within a conversation.
- **Conditional rules** — loaded by Claude Code at level 3,
  part of the cached prefix. They do not inject dynamic
  content.

## What This Blueprint Does NOT Prescribe

These are intentional omissions, not gaps:

- **Architecture** — hexagonal, clean, layered, etc. are
  project choices. `/project-init` generates a TODO
  placeholder for architecture in the project root
  `CLAUDE.md`; the user fills it in.
- **Security practices** — threat modeling and security
  audits are workflow-specific. A security-focused workflow
  would reference security guidance; the blueprint doesn't
  bake it in.
- **Data modeling** — SSOT, event sourcing, CQRS, etc. are
  architectural decisions for the target project.
- **CI/CD** — pipeline configuration is project-specific
  infrastructure.
- **Formatting enforcement** — "run the formatter" belongs
  in the target project's CLAUDE.md or pre-commit hooks,
  because the exact command varies by project.
- **Specific testing methodology** — test-list, TDD, BDD,
  etc. are workflow choices, not universal requirements.
