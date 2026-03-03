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
├── blueprint_testlist/      # Test-list blueprint (5 agents)
│   ├── README.md            # Blueprint-specific docs
│   └── .claude/
│       ├── CLAUDE.md        # Orchestration instructions
│       ├── settings.json    # Enables agent teams + hooks
│       ├── config.json      # Documentation files to check
│       ├── agents/          # Architect, Developer, Test Engineer,
│       │                    # Security Engineer, Reviewer
│       ├── knowledge/
│       │   ├── base/        # Language-agnostic principles
│       │   ├── languages/   # Language-specific extensions
│       │   └── extensions/  # Project-specific conventions
│       ├── practices/       # Test-list workflow, conventional
│       │                    # commits
│       └── templates/       # Commit message template
├── devcontainer_template/   # Devcontainer for sandboxed runs
│   ├── README.md            # Setup and configuration docs
│   └── .devcontainer/
│       ├── devcontainer.json  # Container config
│       ├── Dockerfile         # Image definition
│       └── init-claude-settings.sh  # Startup script
├── container_template/      # Standalone prompt caching proxy
│   ├── docker-compose.yaml  # Configurable compose file
│   ├── Dockerfile           # Python + mitmproxy image
│   ├── cache-proxy.py       # Proxy with stdout logging
│   └── .env.example         # Environment variable docs
└── docs/                    # Design docs and references
    └── prompt-caching-proxy-solution.md
```

## Blueprint

### blueprint_testlist (5 agents)

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

## Devcontainer Template

`devcontainer_template/` provides a devcontainer setup for
sandboxed agent execution. It uses an external prompt
caching proxy (from `container_template/`) rather than
embedding one.

- Project-scoped Docker volume for Claude config and history
- Host `~/.claude/settings.json` mounted read-only as template
- Startup script copies and modifies settings to point at
  the external proxy

## Container Template

`container_template/` provides a standalone prompt caching proxy
container. It injects `cache_control` blocks into Claude API
requests to enable prompt caching.

**Environment variables:**

- `PROXY_PORT` — Port to listen on (default: 3000)
- `TARGET_URL` — Upstream API URL (default: `https://api.portkey.ai`)
- `MIN_CACHE_CHARS` — Minimum chars for caching (default: 1024)

**Usage:**

```bash
cd container_template
cp .env.example .env  # edit as needed
docker compose up -d
```

Logs go to stdout (viewable via `docker compose logs -f`).

## Conventions

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

## Session Checklist

Before ending a session that modified the blueprint:

1. Verify that all changes are safe, sound and concise
2. Verify `CLAUDE.md` (this file) reflects current structure
3. Verify `README.md` matches current blueprints and workflow
4. Update the project structure diagram if directories changed
