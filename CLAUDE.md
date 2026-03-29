# Claude Orchestration Kit - Project Instructions

## What This Is

This repository contains blueprints for Claude Code
multi-agent orchestration. It is not a runnable application.
Blueprint directories contain a `.claude/` setup that gets
copied into target projects to enable coordinated multi-agent
workflows.

## Project Structure

```text
claude_orchestration/
├── CLAUDE.md                # This file (project context)
├── README.md                # User-facing documentation
├── pyproject.toml           # Test harness dependencies
├── .claude/
│   ├── rules/
│   │   ├── prompt-caching.md        # Caching design constraints
│   │   ├── reasoned-instructions.md # Rationale requirement
│   │   ├── self-check.md            # Post-change verification
│   │   ├── agent-design.md          # Agent vs workflow separation
│   │   ├── claude-code-guide.md     # Delegate Claude Code questions
│   │   ├── terminology.md          # Official Claude Code terms glossary
│   │   ├── simplicity.md            # KISS, YAGNI, Reveals Intent
│   │   ├── code-principles.md       # SOLID, Kent Beck rules
│   │   ├── code-mass.md             # APP refactoring metric
│   │   ├── documentation.md         # Documentation principles
│   │   ├── functional-style.md      # FP principles
│   │   ├── lang-python.md           # Python core idioms
│   │   ├── lang-python-patterns.md # Python types, FP
│   │   └── lang-python-testing.md  # Python testing
│   └── skills/
│       └── blueprint-audit/
│           └── SKILL.md             # Audit blueprint consistency
├── blueprint_v1/            # Test-list blueprint (5 agents)
│   ├── .claude/
│   │   ├── CLAUDE.md        # Orchestration instructions
│   │   ├── settings.json    # Enables agent teams + hooks
│   │   ├── config.json      # Documentation files to check
│   │   ├── agents/          # Architect, Developer, Test Engineer,
│   │   │                    # Security Engineer, Reviewer
│   │   ├── knowledge/
│   │   │   ├── base/        # Language-agnostic principles
│   │   │   ├── languages/   # Language-specific extensions
│   │   │   └── extensions/  # Project-specific conventions
│   │   ├── practices/       # Test-list workflow, conventional
│   │   │                    # commits
│   │   └── templates/       # Commit message template
│   └── tests/               # Blueprint verification tests
│       ├── blueprint_contracts.py  # Single source of truth
│       ├── conftest.py      # Shared fixtures + helpers
│       ├── static/          # Structure, caching, hook tests
│       ├── behavioral/      # SDK-based runtime tests
│       └── fixtures/        # Minimal project for behavioral
│           └── minimal_project/
├── blueprint_v2/            # V2 blueprint (clarify-first, workflow-based)
│   ├── CLAUDE.md            # Design reference
│   ├── .claude/
│   │   ├── CLAUDE.md        # Lead instructions
│   │   ├── settings.json    # Agent teams
│   │   ├── agents/          # Architect, Developer, Reviewer,
│   │   │                    # Security Engineer, Test Engineer
│   │   ├── skills/          # Skill definitions
│   │   │   ├── ensure-plans-dir/
│   │   │   │   └── SKILL.md # Create .ai/plans/ and format guide if missing
│   │   │   ├── project-init/
│   │   │   │   ├── SKILL.md # Project scanning + context generation
│   │   │   │   ├── README.md  # Extension guide
│   │   │   │   └── rust-init.md  # Rust-specific init (Cargo lints)
│   │   │   └── project-sanity/
│   │   │       ├── SKILL.md # Audit repo for common issues
│   │   │       ├── github-sanity.md # GitHub Actions workflow checks
│   │   │       └── codecov-sanity.md # Codecov config + coverage checks
│   │   ├── rules/           # Unconditional + conditional rules
│   │   │   ├── simplicity.md       # KISS, YAGNI, Reveals Intent (unconditional)
│   │   │   ├── risk-assessment.md  # Workflow selection risk check (unconditional)
│   │   │   ├── procedural-fidelity.md # Execute every step (unconditional)
│   │   │   ├── github-workflows.md # GitHub Actions (conditional)
│   │   │   ├── code-principles.md  # SOLID, Kent Beck (source files)
│   │   │   ├── code-mass.md        # APP refactoring metric
│   │   │   ├── documentation.md    # Documentation principles
│   │   │   ├── functional-style.md # FP principles (TS/Py/Rust)
│   │   │   ├── lang-go.md          # Go core idioms
│   │   │   ├── lang-go-concurrency.md # Go concurrency
│   │   │   ├── lang-go-testing.md  # Go testing
│   │   │   ├── lang-python.md      # Python core idioms
│   │   │   ├── lang-python-patterns.md # Python types, FP
│   │   │   ├── lang-python-testing.md  # Python testing
│   │   │   ├── lang-rust.md        # Rust core idioms
│   │   │   ├── lang-rust-patterns.md # Rust FP, DDD, async
│   │   │   ├── lang-rust-testing.md  # Rust testing patterns
│   │   │   ├── benchmark-rust.md  # Rust benchmarking (Criterion)
│   │   │   ├── lang-typescript.md  # TypeScript core idioms
│   │   │   ├── lang-typescript-patterns.md # TypeScript FP, React, Node.js
│   │   │   └── lang-typescript-testing.md  # TypeScript testing
│   │   ├── templates/        # Canonical templates copied at runtime
│   │   │   ├── plan-format.md       # Plan format guide (copied to .ai/plans/)
│   │   │   └── project-context.md   # Project context template (filled by /project-init)
│   │   └── workflows/       # Workflow definitions + format guide
│   │       ├── CLAUDE.md          # Workflow format guide
│   │       ├── develop-review-supervised.md  # Dev-team + review (user approves commits)
│   │       ├── develop-review-autonomous.md # Dev-team + review (auto-commit after Reviewer)
│   │       ├── direct-review.md   # Lead handles work directly
│   │       └── tdd-user-in-the-loop.md  # TDD with user approval at phase transitions
│   └── tests/               # Blueprint verification tests
│       ├── blueprint_contracts.py  # Single source of truth
│       ├── conftest.py      # Shared fixtures + helpers
│       ├── static/          # Structure, caching, agent tests
│       ├── behavioral/      # SDK-based runtime tests
│       └── fixtures/        # Minimal project for behavioral
│           └── minimal_project/
├── blueprint_v3/            # V3 blueprint (plan queue + developer)
│   ├── CLAUDE.md            # Design reference
│   ├── .claude/
│   │   ├── CLAUDE.md        # Lead instructions
│   │   ├── settings.json    # Agent teams
│   │   ├── agents/          # Developer, Reviewer, Test Engineer,
│   │   │                    # Security Engineer
│   │   ├── rules/           # Unconditional + conditional rules
│   │   │                    # (includes risk-assessment.md)
│   │   └── skills/          # Skill definitions (with co-located templates)
│   │       ├── ensure-plans-dir/
│   │       │   ├── SKILL.md # Create .ai/plans/ and format guide
│   │       │   └── plan-format.md  # Plan format template
│   │       ├── project-init/
│   │       │   ├── SKILL.md # Project scanning + context generation
│   │       │   ├── project-context.md  # Project context template
│   │       │   ├── README.md  # Extension guide
│   │       │   └── rust-init.md  # Rust-specific init (Cargo lints)
│   │       └── project-sanity/
│   │           ├── SKILL.md # Audit repo for common issues
│   │           ├── github-sanity.md # GitHub Actions workflow checks
│   │           └── codecov-sanity.md # Codecov config + coverage checks
│   └── tests/               # Blueprint verification tests
│       ├── blueprint_contracts.py  # Single source of truth
│       ├── conftest.py      # Shared fixtures + helpers
│       ├── static/          # Structure, caching, agent tests
│       ├── behavioral/      # SDK-based runtime tests
│       └── fixtures/        # Minimal project for behavioral
│           └── minimal_project/
├── devcontainer_templates/   # Devcontainer templates for sandboxed runs
│   ├── CLAUDE.md              # Keep templates in sync
│   ├── .devcontainer/         # Base template (cross-platform)
│   │   ├── README.md          # Setup and configuration docs
│   │   ├── devcontainer.json  # Container config
│   │   ├── Dockerfile         # Image definition
│   │   ├── init-env           # Cross-platform .env.local bootstrap (Unix)
│   │   ├── init-env.cmd       # Cross-platform .env.local bootstrap (Windows)
│   │   ├── post-create.sh     # One-time setup (pnpm store ownership)
│   │   └── post-start.sh     # Auth-mode config copy on each start
│   └── .devcontainer_audio/   # Audio variant (PulseAudio passthrough)
│       ├── README.md          # Platform support and audio setup
│       └── ...                # Same files as base + audio additions
```

## Blueprint

### blueprint_v1 (5 agents)

**Test-list (spec-first), Architect handles task decomposition.**

The lead focuses on user communication and team
coordination. The Architect reads the codebase, decomposes
work into tasks, writes plans to `.claude/plan.md`, and
feeds tasks to the dev-team sequentially. The Test Engineer
produces test specs, the Developer writes all code (source
and tests). Both Test Engineer and Security Engineer give
post-implementation sign-offs before review.

**Agents:**

- Lead (user communication + team coordination)
- Architect (codebase understanding + task decomposition + planning)
- Developer (implements all code)
- Test Engineer (advisory — designs test specs, verifies coverage)
- Security Engineer (advisory — checks security)
- Reviewer (independent quality gate)

### blueprint_v2 (clarify-first, workflow-based)

**Clarify-first, the lead owns clarification and workflow
proposal. The user chooses how work gets done.**

The lead checks for project context at startup (invokes
`/project-init` if `CLAUDE.md` is missing), clarifies the
task with the user, then presents workflow options. The user
chooses a workflow: Direct-Review for simple tasks (lead
handles directly), or Develop-Review (Supervised or Autonomous) / TDD
for complex tasks (Architect writes a plan, user approves,
then workflow agents execute). Workflows are defined as
separate files in `.claude/workflows/` — adding a new
workflow requires no changes to CLAUDE.md. The Reviewer
handles both quality review and git commits.

**Agents:**

- Lead (clarification + coordination)
- Architect (workflow-specific — codebase analysis + plan
  writing + task decomposition + task feeding)
- Developer (implements all code — source and tests)
- Test Engineer (advisory — designs test specs, verifies
  coverage)
- Security Engineer (advisory — checks security)
- Reviewer (independent quality gate — reviews and commits
  approved work)

**Workflows:**

- Direct-Review — lead handles work directly for simple tasks
- Develop-Review (Supervised) — test-list-driven development
  with security review and independent quality gate; user
  approves each commit
- Develop-Review (Autonomous) — same as Supervised but
  commits automatically after Reviewer approval
- TDD User-in-the-Loop — strict Red-Green-Refactor with
  user approval at every phase transition

### blueprint_v3 (plan queue + developer)

**Autonomous after clarification. The lead coordinates
planning and a plan queue; the developer implements.**

The lead checks for project context at startup, clarifies
the task with the user, writes a plan, and manages a plan
queue. For each task in the plan, the lead assesses risk
and uncertainty at dispatch time and directs the developer
to consult advisors when warranted. The developer
implements, and sends to the reviewer. The reviewer
approves and commits or rejects — it also provides a test
adequacy backstop, rejecting work that lacks tests or
advisor consultation for non-trivial changes. The lead
stays responsive to the user during execution — it can
clarify and plan new work concurrently.

**Agents:**

- Lead (clarification + planning + plan queue management +
  coordination)
- Developer (implements all code — source and tests)
- Reviewer (independent quality gate — reviews and commits)
- Test Engineer (advisory — test design on demand)
- Security Engineer (advisory — security assessment on
  demand)

## Devcontainer Template

`devcontainer_templates/` provides a devcontainer setup for
sandboxed agent execution.

- Project-scoped Docker volume for Claude config and history
- Host `~/.claude/` and `~/.claude.json` mounted read-only as templates
- Dual auth mode (`proxy`/`oauth`) controlled by `CLAUDE_AUTH` env var
- `post-start.sh` copies the appropriate config files into the container
  on each start based on auth mode

## Conventions

### Rule files (`.claude/rules/`)

Rule files are Claude Code's mechanism for modular,
topic-specific instructions that load into every session.

- Stored in `.claude/rules/` (project-level) or
  `~/.claude/rules/` (user-level)
- Plain markdown with optional YAML frontmatter
- **Unconditional** (no `paths` frontmatter): loaded at
  session start, always in context — same priority as
  CLAUDE.md
- **Conditional** (with `paths:` frontmatter): loaded only
  when Claude reads files matching the glob patterns

Use rule files for self-contained constraints that should
always be enforced (like caching rules). Use CLAUDE.md for
project structure, workflow, and session checklists.

This project uses:
- `.claude/rules/prompt-caching.md` — ensures all
  blueprints align with Claude Code's prompt caching
  architecture
- `.claude/rules/reasoned-instructions.md` — requires
  every directive in blueprint files to include its
  rationale so agents understand intent, not just rules
- `.claude/rules/self-check.md` — post-change verification
  checklist for blueprint edits
- `.claude/rules/agent-design.md` — enforces separation
  between agent role definitions and workflow coordination
- `.claude/rules/claude-code-guide.md` — delegates Claude
  Code questions to the built-in guide subagent
- `.claude/rules/terminology.md` — enforces official Claude
  Code terms (launch, spawn, create, message) across
  blueprint files to prevent terminology drift
- `.claude/rules/simplicity.md`, `code-principles.md`,
  `code-mass.md`, `documentation.md`, `functional-style.md`,
  `lang-python.md`, `lang-python-patterns.md`,
  `lang-python-testing.md` — coding and documentation standards
  that apply when editing source files in this repo

### Skills (`.claude/skills/`)

Project-level skills for working *on* blueprints. These are
not part of any blueprint and are not copied to target
projects — they are tooling for maintaining this repository.

- `.claude/skills/blueprint-audit/` — audits a blueprint
  for cross-file consistency, stale references,
  contradictions, rationale completeness, and
  documentation alignment

### Two levels of `.claude/`

This repository has two distinct `.claude/` locations with
different purposes:

- **Project-level** (`/.claude/`) — tooling for working
  *on* this repository: rules and skills that govern how
  blueprints are written and maintained. Never copied to
  target projects.
- **Blueprint-level** (`blueprint_*/. claude/`) — the
  `.claude/` setup that gets copied into target projects.
  These are the agent definitions, workflows, rules, and
  templates that end users receive.

### Knowledge files (`knowledge/`)

- `base/` files are **language-agnostic**. No code examples
  in any specific language. Use pseudocode or prose
  descriptions. Agents produce language-specific examples on
  demand based on the target project's languages.
- `languages/` files contain language-specific guidance that
  extends the base principles. Each file references the base
  principles it builds on.
- `extensions/` is for project-specific conventions added
  after copying the blueprint. Contains a `README.md` with
  format guidance. All agents load all extension files.

### Practices

- `practices/` files are language-agnostic workflow guidance.

### Terminology

- Use **"lead"** — not "orchestrator" — when referring to
  the session that creates and manages the team. "Lead" is
  Claude Code's native term.
- If the user says "orchestrator," gently remind them that
  the correct term is "lead."

## Environment Setup

This project runs in a Docker container. On first use, install `uv` if it
is not already available — it is required to run the test suite:

```bash
which uv || curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Session Checklist

Before ending a session that modified the blueprint:

1. Verify that all changes are safe, sound and concise
2. Verify `CLAUDE.md` (this file) reflects current structure
3. Verify root `README.md` matches current blueprints
4. Update the project structure diagram if directories changed
