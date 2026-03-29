# Blueprint v3 — Design Reference

This file describes how the blueprint is designed and why.
It targets sessions working *on* the blueprint (adding
rules, agents, modifying the flow). For user-facing setup
and usage, see the root `README.md`. For lead behavior during a
session, see `.claude/CLAUDE.md`.

## Philosophy

### Autonomous after clarification

Every session starts with clarification and planning. Once
the user approves the plan, execution is fully autonomous —
the lead feeds tasks to the developer, the developer
implements and sends to the reviewer for independent review
and commit. No user checkpoints gate individual task slices.

This trades user control for speed. Users who want
per-commit approval should use blueprint_v2's Supervised
workflow instead. V3 is for users who trust the quality
gates (reviewer + advisors) and want maximum throughput.

### Lead as coordinator

The lead manages clarification, planning, plan queue, and
task feeding — but delegates all implementation to the
developer. This separation exists because a lead that is
blocked writing code cannot respond to the user. With the
developer handling implementation, the lead stays
responsive: the user can describe new work, ask questions,
or adjust priorities while code is being written.

The trade-off is handoff latency — sending a task to the
developer and waiting for the result is slower than
implementing directly. This is accepted because lead
responsiveness during execution is more valuable than
marginal speed: users who can interact with the lead
concurrently produce better plans and catch issues earlier.

### Plan queue

The plan queue model supports multiple concurrent feature
requests. The lead can clarify and plan new work while the
developer executes the current plan. Plans are ordered by
dependency and impact, and the lead checks for supersession
before each task — if a newer plan invalidates the current
one, the current plan is canceled and the lead switches.

This solves two problems: (1) if a session crashes
mid-implementation, all plans are persisted as files and
can be resumed; (2) new feature requests during execution
have a clear mechanism — they become plans in the queue.

### Selective advisor consultation (lead-directed)

Advisors (test-engineer, security-engineer) are consulted
based on risk and uncertainty indicators, not on every task.
This is informed by the retrospective finding that mandatory
security review on low-risk tasks (pure functions, internal
wiring) produces rubber-stamp sign-offs that dilute the
signal when real issues arise.

The framework lives in `.claude/rules/risk-assessment.md`
(an unconditional rule loaded by both lead and developer):
- **High uncertainty → test-engineer** — design trade-offs,
  complex interactions, greenfield code, API surface changes,
  behavioral changes observable by callers, code with no
  existing test coverage, new test files.
  When consulted, the test-engineer also verifies the
  implementation against the test list post-implementation.
- **High risk → security-engineer** — trust boundaries,
  untrusted input, crypto, network-facing code, secrets,
  permissions, data persistence. When consulted, the
  security-engineer also reviews the implementation and
  gives a post-implementation sign-off.
- **Low risk + low uncertainty → skip advisors** — pure
  functions with existing test patterns,
  pattern-following with test coverage, test-only,
  refactoring, docs

**The lead owns the consultation decision.** The lead
assesses each task at dispatch time and includes an explicit
directive ("consult the test advisor" or "no advisors
needed"). The developer treats lead directives as mandatory
and may add — but not remove — consultations based on what
implementation reveals. This shifts the decision to the
agent with full plan context and counterbalances the
developer's natural optimization-speed bias.

**The reviewer provides a backstop.** If the reviewer finds
that non-trivial behavioral changes lack new tests and no
test advisor was consulted, it rejects and directs the
developer to consult the test advisor before resubmission.
This catches cases where the lead misjudged uncertainty.

## Component Architecture

```text
blueprint_v3/
├── CLAUDE.md              ← You are here (design reference)
├── .claude/
│   ├── CLAUDE.md          ← Lead instructions (session behavior)
│   ├── settings.json      ← Agent teams config
│   ├── agents/            ← Agent definitions (4 agents)
│   │   ├── developer.md   ← Implements all code (source + tests)
│   │   ├── reviewer.md    ← Independent quality gate + commits
│   │   ├── test-engineer.md   ← Advisory — test design on demand
│   │   └── security-engineer.md ← Advisory — security assessment on demand
│   ├── rules/             ← Unconditional + conditional rules
│   │   ├── simplicity.md         ← [unconditional] KISS, YAGNI, etc.
│   │   ├── procedural-fidelity.md ← [unconditional] Execute every step
│   │   ├── risk-assessment.md    ← [unconditional] When to consult advisors
│   │   ├── github-workflows.md   ← [conditional: .github/workflows/**]
│   │   ├── code-principles.md    ← [conditional: source files] SOLID, Kent Beck
│   │   ├── lang-typescript.md    ← [conditional: *.ts, *.tsx] Core idioms
│   │   ├── lang-typescript-patterns.md ← [conditional: *.ts, *.tsx] FP, React, Node.js
│   │   ├── lang-typescript-testing.md  ← [conditional: *.ts, *.tsx] Testing
│   │   ├── lang-python.md        ← [conditional: *.py] Core idioms
│   │   ├── lang-python-patterns.md ← [conditional: *.py] Types, FP
│   │   ├── lang-python-testing.md  ← [conditional: *.py] Testing
│   │   ├── lang-go.md            ← [conditional: *.go] Core idioms
│   │   ├── lang-go-concurrency.md ← [conditional: *.go] Concurrency
│   │   ├── lang-go-testing.md   ← [conditional: *.go] Testing
│   │   ├── lang-rust.md          ← [conditional: *.rs] Core idioms
│   │   ├── lang-rust-patterns.md ← [conditional: *.rs] FP, DDD, async
│   │   ├── lang-rust-testing.md  ← [conditional: *.rs] Testing
│   │   ├── benchmark-rust.md     ← [conditional: benches/**/*.rs]
│   │   ├── functional-style.md   ← [conditional: *.ts, *.py, *.rs]
│   │   ├── documentation.md      ← [conditional: README*, docs/**]
│   │   └── code-mass.md          ← [conditional: source files]
│   └── skills/            ← Skill definitions (with co-located templates)
│       ├── ensure-plans-dir/
│       │   ├── SKILL.md   ← Create .ai/plans/ and format guide if missing
│       │   └── plan-format.md  ← Plan format template
│       ├── project-init/
│       │   ├── SKILL.md   ← Project scanning + context generation
│       │   ├── README.md  ← Extension guide (add <language>-init.md)
│       │   ├── rust-init.md ← Rust-specific init (Cargo lints)
│       │   └── project-context.md ← Project context template
│       └── project-sanity/
│           ├── SKILL.md   ← Audit repo for common issues across detected technologies
│           ├── github-sanity.md ← GitHub Actions workflow checks
│           └── codecov-sanity.md ← Codecov configuration + coverage checks
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
behavior — startup, clarification, planning, plan queue
management, and task feeding to the developer. The lead is
the only agent with user access and the coordinator of the
execution pipeline.

**Agent definitions** (`.claude/agents/*.md`) specify each
agent's model, tools, and instructions via YAML frontmatter
and markdown body. All four agents are general-purpose
building blocks — the developer implements code, the
reviewer evaluates and commits, and advisors respond to
consultation requests without knowing which workflow or
blueprint invoked them. The developer-reviewer handoff
includes a working-tree delta: the developer snapshots
`git diff --name-only` before and after implementation,
reports the exact file list (including incidental formatter
changes), and the reviewer commits that scoped set —
not all dirty files in the tree.

#### Agent Design Principle

Agent files define **role, domain expertise, and
capability** — what the agent is and how it does its work.
Agents communicate generically: "the requester" — never
hardcoded teammate names.

What belongs in an agent file:
- The agent's purpose and domain expertise
- How the agent does its work (process, checklist)
- Generic communication: "message the requester," "send
  findings to whoever requested the review"
- Tool usage and constraints

What does NOT belong in an agent file:
- Named teammates
- Coordination sequences
- Workflow-specific conditionals

**Skills** (`.claude/skills/*/SKILL.md`) define reusable
procedures invoked by the lead. Templates consumed by a
skill live in that skill's directory (not a separate
`templates/` directory) — this makes dependencies explicit
and eliminates a top-level directory. Currently:
`ensure-plans-dir` (prepares the plans directory and its
format guide) and `project-init` (scans the project and
generates context).

Skills run at startup — before the team exists — so their
outputs cannot go through the developer-reviewer pipeline.
The lead commits skill outputs directly, scoped by the
**skill-output commit rule** (defined in `.claude/CLAUDE.md`):
only files that a skill's `SKILL.md` explicitly names as
outputs, committed immediately after the skill completes.
This prevents the lead from using the exception to bypass
the reviewer for arbitrary files. The bright-line test: if
the skill invocation were removed, would the file still
need to exist? If yes, it belongs in the pipeline.

**Rules** (`.claude/rules/*.md`) provide guidance that
Claude Code injects into agent context automatically.
Unconditional rules load at session start; conditional
rules load when agents touch matching files. Rules are
independent of agents — they apply to any agent that
touches a matching file. The `risk-assessment.md` rule
is unconditional and loaded by both the lead and developer,
ensuring consistent advisor consultation decisions.

**Plans** (`.ai/plans/*.md`) are runtime artifacts written
by the lead during a session. They capture the goal,
context, steps, task decomposition, and commit SHAs as
tasks complete. Plans are committed to git as decision
records. Multiple plans can coexist in the queue.

**Tests** (`tests/`) verify the blueprint's structural
integrity: required files exist, agent frontmatter matches
contracts, static files contain no dynamic content.

## Rule System Design

Identical to blueprint_v2. See the v2 design reference for
the full rule system design documentation. In summary:

- **Unconditional** (no `paths:` frontmatter): `simplicity.md`,
  `risk-assessment.md`
- **Conditional** (with `paths:` frontmatter): all others
- Universal principles stated once, language rules extend
  without restating

### Adding a new language

1. Create `.claude/rules/lang-<language>.md`
2. Add `paths:` frontmatter with file extensions
3. Include idioms, testing, tooling, pitfalls
4. Update `functional-style.md` paths if applicable
5. Update `code-mass.md` and `code-principles.md` paths
6. Update root `CLAUDE.md` and root `README.md`
7. Run `uv run pytest blueprint_v3/tests/ -m static -v`

No changes to `.claude/CLAUDE.md` or agents.

## Prompt Caching Alignment

The blueprint aligns with Claude Code's prompt caching
architecture (see repo-level
`.claude/rules/prompt-caching.md`):

- **Level 3 (CLAUDE.md + rules)** — all files are fully
  static. No dates, counters, or changing data. Enforced
  by caching compliance tests.
- **Tool set stability** — each agent has a fixed tool set
  in its frontmatter. No conditional tool loading.
- **Model delegation** — agents are subagents (separate
  conversations), not model switches within a conversation.
- **Conditional rules** — loaded by Claude Code at level 3,
  part of the cached prefix.

## What This Blueprint Does NOT Prescribe

These are intentional omissions, not gaps:

- **Architecture** — project choice, not blueprint concern
- **Security practices** — handled on-demand by the
  security-engineer advisor
- **Data modeling** — project-specific decisions
- **CI/CD** — project-specific infrastructure
- **Formatting** — belongs in project CLAUDE.md or
  pre-commit hooks
- **Testing methodology** — the test-engineer advisor
  designs test specifications; the developer implements them
- **User checkpoints** — v3 is fully autonomous after plan
  approval; use v2 for per-commit user control

## Comparison with Blueprint v2

| Aspect | v2 | v3 |
|---|---|---|
| Implementation | Developer agent (Sonnet) | Developer agent (Sonnet) |
| Planning | Architect agent (Opus) | Lead (Opus) |
| User checkpoints | Per-commit (Supervised) or none (Autonomous) | None after plan approval |
| Advisor invocation | Every task (mandatory sign-offs) | Lead-directed, on-demand (risk/uncertainty) |
| Workflows | 4 variants (user chooses) | 1 flow (autonomous) |
| Agents | 5 (Architect, Developer, Reviewer, TE, SE) | 4 (Developer, Reviewer, TE, SE) |
| Agent communication | Peer-to-peer + lead relay | Developer-reviewer direct + lead hub |
| Execution pipeline | Architect → Developer → Reviewer | Lead → Developer → Reviewer → Lead |
| Plan management | Single plan per session | Plan queue (multiple plans, supersession) |
| Lead during execution | Blocked (relaying messages) | Responsive (can clarify new work) |
