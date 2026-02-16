# Claude Orchestration Kit

A drop-in orchestration kit for Claude Code multi-agent
workflows. Copy the blueprint's `.claude/` directory into any
project to get a team of specialized agents coordinated by
your Claude Code session, guided by a shared knowledge base
of software engineering principles.

## Repository Layout

```text
claude_orchestration/
├── blueprint/             # v1 blueprint (archived)
├── blueprint_v2/          # v2 blueprint (archived)
├── blueprint_v3/          # v3 blueprint (archived)
└── blueprint_v4/          # Current blueprint
    └── .claude/
        ├── CLAUDE.md      # Orchestration instructions
        ├── settings.json  # Agent teams config + hooks
        ├── config.json    # Documentation files to check
        ├── agents/        # Developer, Test Engineer,
        │                  # Security Engineer, Reviewer
        ├── knowledge/     # Shared knowledge base
        │   ├── base/      # Language-agnostic principles
        │   ├── languages/ # Language-specific extensions
        │   └── extensions/# Project-specific conventions
        ├── practices/     # TDD, conventional commits
        └── templates/     # Commit message template
```

- **`blueprint/`** — v1: rigid increment-based workflow with
  6 specialist agents. Too prescriptive.
- **`blueprint_v2/`** — v2: minimal 2-agent design
  (Developer + Reviewer). Too permissive — Developer
  skipped tests and security checks.
- **`blueprint_v3/`** — v3: dev-team model without
  housekeeping checks. Archived as baseline.
- **`blueprint_v4/`** — v4: dev-team model with housekeeping
  checks, pre-commit hooks, and config.json. Current.

## Prerequisites

Agent teams are an experimental Claude Code feature, disabled
by default. The included `settings.json` enables them
automatically when you copy the blueprint. You can also set
the environment variable directly:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

## Quick Start

Copy the blueprint into your project:

```bash
cp -r blueprint_v4/.claude/ /path/to/your/project/.claude/
```

Start Claude Code in your project directory. The CLAUDE.md
loads automatically and configures your session as the team
lead. Describe what you want to build, and it will
decompose the work into tasks and feed them to the dev-team.

## How It Works

### Agents

| Agent | Model | Role |
|-------|-------|------|
| **Developer** | opus | Implements source code |
| **Test Engineer** | opus | Owns all test code |
| **Security Engineer** | opus | Advisory — checks security gaps |
| **Reviewer** | opus | Quality gate — commits when satisfied |

### Workflow

```text
Lead → Task → Dev-Team → Reviewer → Commit
                  ↑          |
                  └──────────┘ (if rejected)
```

1. **Lead** decomposes the user's request into
   sequential tasks.
2. **Dev-team** (Developer, Test Engineer, Security
   Engineer) receives each task, discusses approach, then
   implements. Test Engineer writes tests first. Developer
   makes them pass. Security Engineer advises throughout.
3. **Reviewer** examines the completed work. If satisfied,
   commits with a conventional commit message. If not,
   sends findings back to the full dev-team for fixes.
4. Lead sends the next task after commit.

### Knowledge Base

Engineering principles in `knowledge/` that agents load
during startup:

- **`base/`** — language-agnostic principles: Simple Design,
  KISS, YAGNI, SOLID, FP, SSOT, security (OWASP Top 10),
  code mass, hexagonal architecture, testing pyramid,
  documentation.
- **`languages/`** — language-specific extensions for Rust,
  TypeScript, Python, and Go. Each references the base
  principles it builds on.
- **`extensions/`** — project-specific conventions added
  after copying the blueprint into a target project.

### Practices

- **TDD** — red-green-refactor workflow
- **Conventional Commits** — structured commit messages

### Templates

- **Commit message** — format for consistent, informative
  commit history

## Adding Languages

Create a file at `knowledge/languages/<language>.md`
following the pattern of existing language files. Include:

1. Language philosophy and idioms
2. How base principles apply in that language
3. Testing frameworks and patterns
4. Common pitfalls
5. Recommended tools and libraries

## Project Extensions

After copying into your project, add project-specific
conventions in `.claude/knowledge/extensions/`. See
`knowledge/extensions/README.md` for format details.

## Known Limitations

Agent teams are experimental. Be aware of:

- **No session resumption** — `/resume` and `/rewind` do not
  restore in-process teammates.
- **One team per session** — Clean up the current team before
  starting another.
- **No nested teams** — Only the lead can manage the team.
- **Lead is fixed** — The session that creates the team stays
  the lead.
- **Task status can lag** — Teammates sometimes fail to mark
  tasks completed. Check and update manually if stuck.
- **File conflicts** — Test Engineer goes first, Developer
  follows. Assign clear file ownership.
- **Permissions inherit** — All teammates inherit the lead's
  permission settings.
