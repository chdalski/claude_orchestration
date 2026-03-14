# Claude Orchestration Kit

Drop-in multi-agent orchestration for Claude Code. Copy a
blueprint's `.claude/` directory into any project to get a
team of specialized agents coordinated by your Claude Code
session.

## Blueprints

### Choosing a Blueprint

| If you want... | Use |
|---|---|
| Full control, spec-first TDD with knowledge base | v1 |
| Workflow options (supervised, autonomous, TDD) | v2 |
| Maximum throughput, minimal interaction | v3 |
| Per-commit user approval | v1 or v2 (Supervised) |
| Full autonomy after plan approval | v3 |
| Fewer agents, simpler coordination | v3 |

### v1 — Test-List (5 agents)

Spec-first development. The Architect decomposes work, the
Test Engineer designs what to test, the Developer writes all
code. Both Test Engineer and Security Engineer give
post-implementation sign-offs before review.

| Agent | Model | Role |
|-------|-------|------|
| Architect | Sonnet | Reads codebase, decomposes tasks, writes plans |
| Developer | Sonnet | Implements all code (source + tests) |
| Test Engineer | Sonnet | Advisory — designs test specs, verifies coverage |
| Security Engineer | Sonnet | Advisory — checks security gaps |
| Reviewer | Opus | Quality gate — commits when satisfied |

```text
User -> Lead -> Architect -> Dev-Team -> Reviewer -> Commit
```

The dev-team (Developer, Test Engineer, Security Engineer)
discusses approach before implementing. The Architect feeds
tasks sequentially; the lead coordinates review handoffs.

Engineering principles live in `knowledge/` — language-agnostic
base principles, language-specific extensions, and
project-specific conventions in `extensions/`.

### v2 — Clarify-First (workflow-based)

The lead clarifies the task, then presents workflow options.
The user chooses how work gets done. Workflows are separate
files in `.claude/workflows/` — adding one requires no
changes to CLAUDE.md.

| Agent | Model | Role |
|-------|-------|------|
| Architect | Opus | Reads codebase, writes plans, feeds tasks |
| Developer | Sonnet | Implements all code (source + tests) |
| Test Engineer | Sonnet | Advisory — designs test specs, verifies coverage |
| Security Engineer | Sonnet | Advisory — checks security gaps |
| Reviewer | Sonnet | Quality gate — reviews and commits |

**Workflows:**

- **Direct-Review** — lead handles work directly, Reviewer
  checks quality. For well-scoped tasks.
- **Develop-Review (Supervised)** — full dev cycle with
  Architect planning, test-list development, and user
  approval per commit.
- **Develop-Review (Autonomous)** — same as Supervised but
  commits automatically after Reviewer approval.
- **TDD User-in-the-Loop** — strict Red-Green-Refactor with
  user approval at every phase transition.

Language-specific guidance loads automatically via
conditional rules when agents touch matching files.
`/project-init` generates project context on first session.

### v3 — Autonomous Lead (3 agents)

The lead handles everything: clarification, planning, and
implementation. Three subagents provide independent code
review, on-demand test design, and on-demand security
assessment. After the user approves the plan, execution is
fully autonomous.

| Agent | Model | Role |
|-------|-------|------|
| Reviewer | Sonnet | Quality gate — reviews and commits |
| Test Engineer | Sonnet | Advisory — test lists on demand |
| Security Engineer | Sonnet | Advisory — security assessments on demand |

```text
User -> Lead -> Plan -> [Assess Risk/Uncertainty]
                  |            |              |
                  |     Test Engineer   Security Engineer
                  |     (if needed)      (if needed)
                  v
              Implement -> Reviewer -> Commit
```

Advisors are consulted based on risk and uncertainty
indicators — not on every task. When consulted, they also
verify the implementation post-implementation (test coverage
conformance, security sign-off). Hub-and-spoke communication
(lead is always one party) eliminates message-loss risk.

## Quick Start

```bash
# Copy a blueprint into your project
cp -r blueprint_v1/.claude/ /path/to/your/project/.claude/
# or
cp -r blueprint_v2/.claude/ /path/to/your/project/.claude/
# or
cp -r blueprint_v3/.claude/ /path/to/your/project/.claude/
```

Start Claude Code in your project directory. The CLAUDE.md
loads automatically and configures your session as the team
lead.

## Prerequisites

Agent teams are an experimental Claude Code feature,
disabled by default. Each blueprint's `settings.json`
enables them automatically. You can also set the environment
variable directly:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

## Devcontainer Template

`devcontainer_template/` provides a devcontainer setup for
sandboxed agent execution. Copy it alongside `.claude/`:

```bash
cp -r devcontainer_template/.devcontainer/ /path/to/your/project/.devcontainer/
```

Features:

- **Dual auth mode** — proxy (default) or OAuth, controlled
  by `CLAUDE_AUTH` in `.devcontainer/.env.local`
- **Project-scoped volume** — Claude config and history
  isolated per project
- **Host config as template** — `~/.claude/` mounted
  read-only, copied into container on startup

See `devcontainer_template/.devcontainer/README.md` for
auth configuration, troubleshooting, and mount details.

## Known Limitations

Agent teams are experimental. Be aware of:

- **No session resumption** — `/resume` and `/rewind` do
  not restore in-process teammates.
- **One team per session** — clean up the current team
  before starting another.
- **No nested teams** — only the lead can manage the team.
- **Lead is fixed** — the session that creates the team
  stays the lead.
- **Permissions inherit** — all teammates inherit the
  lead's permission settings.
