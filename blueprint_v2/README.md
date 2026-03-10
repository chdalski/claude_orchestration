# Clarify-First Blueprint (v2)

Clarify-first, workflow-based blueprint for Claude Code
multi-agent orchestration. The lead clarifies, the user
chooses a workflow, and specialized agents execute.

## How It Works

### Approach

The lead starts every session by clarifying the request
with the user through structured dialogue. Once the task is
understood, the lead reads the available workflow files and
presents them as options via `AskUserQuestion`. The user
chooses how work gets done — not the lead.

Available workflows:

- **Direct-Review** — the lead handles work directly, with
  a Reviewer quality check (including CLAUDE.md drift
  detection) before presenting to the user. For tasks
  where the user prefers directness over process and the
  change is well-scoped. Not appropriate for cross-cutting
  design decisions or security-sensitive changes.
  No Architect, no plan, no multi-agent overhead.
- **Develop-Review (Supervised)** — full development cycle
  with Architect planning, test-list-driven development,
  security review, and independent quality gate. The user
  approves each commit before it enters git history.
- **Develop-Review (Autonomous)** — same as Supervised but
  commits automatically after Reviewer approval. The user
  trusts the agent quality gates.
- **TDD User-in-the-Loop** — strict Red-Green-Refactor
  with user approval at every phase transition. Best when
  the user wants maximum visibility and control over
  implementation.

For Direct-Review, the lead implements directly. For the
Develop-Review variants and TDD, the lead creates a team
via `TeamCreate` with all workflow agents (including the
Architect), sends the clarified request to the Architect,
presents the plan for approval, then executes per the
workflow definition.

### Startup

1. Lead checks for project context — if `CLAUDE.md` is
   missing at the project root, it invokes `/project-init`
   to generate it.
2. Lead checks for existing plans from previous sessions.
3. Lead begins clarification with the user.
4. Once clarified, lead presents workflow options.
5. User chooses a workflow.
6. For Direct-Review: lead handles work directly, spawns
   Reviewer via TeamCreate, then presents to user for
   approval before telling the Reviewer to commit.
7. For Develop-Review (Supervised or Autonomous) / TDD: lead creates a team with all
   workflow agents, sends clarified request to the
   Architect, Architect writes the plan, lead presents the
   plan for approval, then executes per workflow.

### Agents

| Agent | Model | Role | Writes Code |
|-------|-------|------|-------------|
| **Architect** | opus | Reads codebase, writes plans, decomposes and feeds tasks | No (plans only) |
| **Developer** | sonnet | Implements all code (source + tests) | Yes |
| **Test Engineer** | sonnet | Advisory — designs test specs, verifies coverage | No |
| **Security Engineer** | sonnet | Advisory — checks security gaps | No |
| **Reviewer** | sonnet | Independent quality gate — reviews completed work and commits approved changes | No (review + git only) |

All agents are general-purpose building blocks — no agent
runs automatically. Each workflow declares which agents it
needs. The lead creates a team via `TeamCreate` with all
listed agents — this applies to all workflows including
Direct-Review, where a one-agent team keeps the Reviewer
alive to receive the commit signal after the user checkpoint.

### Workflows

Workflows live in `.claude/workflows/` as separate
markdown files. Each workflow defines which agents it
needs, the step-by-step execution flow, and completion
criteria. Adding a new workflow requires no changes to
CLAUDE.md — just add a file.

See `.claude/workflows/CLAUDE.md` for the required format.

#### Direct-Review

The Direct-Review workflow is for tasks where the user
prefers directness over process. The lead
handles all work directly — reading files, implementing
changes, running tests — then creates a one-agent team
via TeamCreate with the Reviewer for an independent
quality check (including CLAUDE.md drift detection)
before presenting the result for user approval, then
tells the Reviewer to commit.

See `.claude/workflows/direct-review.md` for the full flow
and completion criteria.

#### Develop-Review (Supervised)

The Develop-Review workflow provides a full development
cycle for code tasks. The Architect feeds task slices to a
dev-team (Developer, Test Engineer, Security Engineer) that
uses test-list-driven development. After implementation,
the Reviewer provides an independent quality gate before
each commit. In the Supervised variant, the user approves
each commit before it enters git history.

Flow per task slice:

1. Dev-team discusses → Security Engineer assesses →
   Test Engineer produces test list
2. Developer writes tests → Test Engineer verifies →
   Developer implements
3. Test Engineer and Security Engineer give sign-offs
4. Reviewer evaluates → approves or rejects
5. User confirms commit → Reviewer commits

See `.claude/workflows/develop-review-supervised.md` for
the full step-by-step flow and completion criteria.

#### Develop-Review (Autonomous)

Same as the Supervised variant, but after Reviewer approval
the lead immediately tells the Reviewer to commit — no user
checkpoint. The user trusts the agent quality gates (Test
Engineer sign-off, Security Engineer sign-off, Reviewer
approval) to ensure correctness.

See `.claude/workflows/develop-review-autonomous.md` for
the full step-by-step flow and completion criteria.

#### TDD User-in-the-Loop

The TDD User-in-the-Loop workflow provides strict
Red-Green-Refactor development with user approval at every
phase transition. The Test Engineer produces the test list
upfront, the user approves it, then the Developer works
through tests one at a time. The user sees and approves each
Red (failing test), Green (minimal implementation), and
Refactor (mandatory improvement) phase before the next
begins.

Flow per task slice:

1. Dev-team discusses → Security Engineer assesses →
   Test Engineer produces test list → **User approves
   test list**
2. Per test: Red (write failing test, **user approves**) →
   Green (minimal implementation, **user approves**) →
   Refactor (mandatory improvement, **user approves**) →
   Test Engineer verifies
3. Test Engineer and Security Engineer give sign-offs
4. Reviewer evaluates → approves or rejects
5. User confirms commit → Reviewer commits

See `.claude/workflows/tdd-user-in-the-loop.md` for the
full step-by-step flow and completion criteria.

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

Adding a new language is just adding a file — no changes
to CLAUDE.md or agent definitions required.

### Project Initialization

After copying `.claude/` to a new project, the lead
auto-generates `CLAUDE.md` at the project root on the
first session by invoking `/project-init`. This scans the project for languages,
frameworks, and structure, then maps findings to the
blueprint's conditional rule files. Auto-detected sections
are filled in; human-curated sections (Overview,
Architecture, Code Exemplars, Anti-Patterns, Trusted
Sources) are left as TODOs for you to complete.

For projects with git-repository subdirectories, the skill
also generates a `CLAUDE.md` in each subdirectory that has
its own `.git/`, scanned independently.

To regenerate after major project changes, run
`/project-init` manually.

### Conventional Commits

All commits use conventional prefixes (`feat:`, `fix:`,
`chore:`, etc.) for scannable git history. The Reviewer
composes the commit message after review — it has the full
context of what changed and why, making it the right agent
to write an accurate, informative message.

## Setup

```bash
cp -r .claude/ /path/to/your/project/.claude/
```

Optionally, copy the devcontainer for sandboxed execution
with a network firewall:

```bash
cp -r .devcontainer/ /path/to/your/project/.devcontainer/
```

### Permissions

The blueprint relies on the clarification-first behavior
defined in `.claude/CLAUDE.md` to ensure requirements are
understood before execution — not on plan mode enforcement.
The lead always clarifies the task and presents workflow
options before any work begins.

On the host, users are prompted for tool permissions — this
is the safe default for unsandboxed environments.

**Devcontainer (sandboxed):** The Dockerfile aliases
`claude` to `claude --dangerously-skip-permissions`, so
all tools are auto-approved without per-tool permission
prompts. The startup script (`init-claude-settings.sh`)
copies host settings into the container volume for
configuration (model preferences, API keys, etc.).

To add project-specific commands to the allow-list, create
`.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(make *)",
      "Bash(docker *)"
    ]
  }
}
```

See the repository README for prerequisites, devcontainer
details, and configuration options.
