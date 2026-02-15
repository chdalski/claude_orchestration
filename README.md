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
└── blueprint_v2/          # Current blueprint
    └── .claude/
        ├── CLAUDE.md      # Orchestration instructions
        ├── settings.json  # Agent teams config + hooks
        ├── agents/        # Developer, Reviewer
        ├── knowledge/     # Shared knowledge base
        │   ├── base/      # Language-agnostic principles
        │   ├── languages/ # Language-specific extensions
        │   └── extensions/# Project-specific conventions
        ├── practices/     # TDD, conventional commits
        └── templates/     # Commit message template
```

- **`blueprint/`** — the original v1 orchestration design.
  Archived for reference. Too prescriptive in its workflow —
  enforced a rigid human-like increment cycle that fought
  against how agents naturally work.
- **`blueprint_v2/`** — the current orchestration design.
  Goals over process, fewer agents with more ownership,
  quality through knowledge rather than enforcement.

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
cp -r blueprint_v2/.claude/ /path/to/your/project/.claude/
```

Start Claude Code in your project directory. The CLAUDE.md
loads automatically and configures your session as the team
lead. Describe what you want to build, and it will decompose
the work, spawn Developer agents, and coordinate their
execution.

## What's Included

### Agents

| Agent | Model | Role |
|-------|-------|------|
| **Developer** | opus | Implements features, writes tests, fixes bugs, updates docs |
| **Reviewer** | sonnet | Reviews code for quality, security, and correctness |

The Developer owns work end-to-end. The Reviewer is spawned
by the lead when a second opinion is needed — not mandated
for every change.

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
- **File conflicts** — Two teammates editing the same file
  causes overwrites. Assign file ownership to prevent this.
- **Permissions inherit** — All teammates inherit the lead's
  permission settings.
