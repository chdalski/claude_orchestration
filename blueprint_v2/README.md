# Plan-First Blueprint (v2)

Plan-first, workflow-based blueprint for Claude Code
multi-agent orchestration. The lead clarifies, the
Architect plans, and workflows define how work gets done.

## How It Works

### Planning Approach

The lead starts every session in plan mode. For medium to
large tasks, it clarifies the request with the user, spawns
the Architect to read the codebase and write a plan, then
presents the plan for approval before proposing a workflow.
No code is touched until the user approves. This
front-loads understanding and avoids wasting tokens on
misunderstood requirements.

Not every task needs the full flow. The lead triages each
request by scope:

- **Trivial** (1-2 files, mechanical) — the lead handles
  it directly. No agents, no plan.
- **Small** (2-5 files, clear scope) — a single agent
  executes directly. No Architect or plan needed.
- **Medium to large** (5+ files, design decisions) — full
  planning flow with Architect, plan approval, and
  workflow selection.

The user can exit plan mode at any time. When they do, the
lead assesses scope and responds proportionally. If the
task turns out to be larger than it looks, the lead shares
its findings and recommends creating a plan — but the user
decides whether to follow that recommendation.

### Startup

1. Lead spawns the Auditor in the background to check
   CLAUDE.md integrity.
2. Lead checks for existing plans from previous sessions.
3. Lead begins clarification with the user.
4. Once clarified, lead spawns the Architect with the
   request.
5. Architect writes the plan and reports back.
6. Lead presents the plan to the user for approval.
7. When the Auditor reports discrepancies and the plan
   involves codebase changes, a fix step is prepended.

### Agents

| Agent | Model | Role | Writes Code |
|-------|-------|------|-------------|
| **Architect** | opus | Reads codebase, writes plans, decomposes and feeds tasks | No (plans only) |
| **Auditor** | haiku | Checks CLAUDE.md accuracy | No (read-only) |
| **Committer** | haiku | Stages and commits files | No (git only) |
| **Developer** | sonnet | Implements all code (source + tests) | Yes |
| **Test Engineer** | sonnet | Advisory — designs test specs, verifies coverage | No |
| **Security Engineer** | sonnet | Advisory — checks security gaps | No |
| **Reviewer** | sonnet | Independent quality gate — reviews completed work | No |

The Architect spans both planning (pre-workflow) and
execution (during workflow). It writes the plan, then
feeds tasks to whichever agents the chosen workflow
provides.

The Auditor runs at session start to catch stale
instructions. The Committer is a shared utility — any
workflow can use it to commit work without bundling commit
logic into review or implementation agents.

Developer, Test Engineer, Security Engineer, and Reviewer
are workflow-specific agents used by the Develop-Review
workflow.

### Workflows

Workflows live in `.claude/workflows/` as separate
markdown files. Each workflow defines which agents it
needs, the step-by-step execution flow, and completion
criteria. Adding a new workflow requires no changes to
CLAUDE.md — just add a file.

See `.claude/workflows/CLAUDE.md` for the required format
and the list of shared agents available to all workflows.

#### Develop-Review

The Develop-Review workflow provides a full development
cycle for code tasks. The Architect feeds task slices to a
dev-team (Developer, Test Engineer, Security Engineer) that
uses test-list-driven development. After implementation,
the Reviewer provides an independent quality gate before
each commit.

Flow per task slice:

1. Dev-team discusses → Security Engineer assesses →
   Test Engineer produces test list
2. Developer writes tests → Test Engineer verifies →
   Developer implements
3. Test Engineer and Security Engineer give sign-offs
4. Reviewer evaluates → approves or rejects
5. User confirms commit → Committer commits

See `.claude/workflows/develop-review.md` for the full
step-by-step flow and completion criteria.

### Conditional Rules

Language-specific and topic-specific guidance lives in
`.claude/rules/` as conditional rule files with `paths:`
frontmatter. Claude Code automatically injects these into
context when agents touch matching files — no startup
loading or agent configuration needed.

**Unconditional** (always loaded, no `paths:` frontmatter):

| Rule File | Content |
|-----------|---------|
| `simplicity.md` | KISS, YAGNI, Reveals Intent, Fewest Elements — universal principles for all work |

**Conditional** (loaded when matching files are touched):

| Rule File | Triggers On | Content |
|-----------|------------|---------|
| `code-principles.md` | all source files | SOLID, Kent Beck's Four Rules, type-driven design |
| `lang-typescript.md` | `*.ts`, `*.tsx` | TypeScript idioms, type system, React, testing |
| `lang-python.md` | `*.py` | Pythonic patterns, type hints, pytest |
| `lang-go.md` | `*.go` | Go idioms, error handling, concurrency, testing |
| `lang-rust.md` | `*.rs` | Ownership, type system, async, testing |
| `functional-style.md` | `*.ts`, `*.tsx`, `*.py`, `*.rs` | FP principles (not Go) |
| `documentation.md` | `README*`, `docs/**/*.md` | Documentation principles |
| `code-mass.md` | `*.ts`, `*.tsx`, `*.py`, `*.rs`, `*.go` | APP refactoring metric |
| `cargo-lints.md` | `Cargo.toml` | Required Clippy lints |

Adding a new language is just adding a file — no changes
to CLAUDE.md or agent definitions required.

### Conventional Commits

All commits use conventional prefixes (`feat:`, `fix:`,
`chore:`, etc.) for scannable git history. The Committer
receives the full commit message from its caller — it
does not choose the prefix or message itself.

## Setup

```bash
cp -r .claude/ /path/to/your/project/.claude/
cp -r .ai/ /path/to/your/project/.ai/
```

Optionally, copy the devcontainer for sandboxed execution
with a network firewall and autopilot permissions:

```bash
cp -r .devcontainer/ /path/to/your/project/.devcontainer/
```

See the repository README for prerequisites, devcontainer
details, and configuration options.
