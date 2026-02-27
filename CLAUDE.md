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
├── .devcontainer/           # Devcontainer for sandboxed runs
│   ├── devcontainer.json    # Container config
│   ├── Dockerfile           # Image definition
│   └── claude_proxy/        # Prompt caching proxy scripts
├── container_template/      # Standalone proxy container
│   ├── docker-compose.yaml  # Configurable compose file
│   ├── Dockerfile           # Python + mitmproxy image
│   ├── cache-proxy.py       # Proxy with stdout logging
│   └── .env.example         # Environment variable docs
├── blueprint_testlist_v1/   # Test-list blueprint (4 agents)
│   └── .claude/
│       ├── CLAUDE.md        # Orchestration instructions
│       ├── settings.json    # Enables agent teams + hooks
│       ├── config.json      # Documentation files to check
│       ├── agents/          # Developer, Test Engineer,
│       │                    # Security Engineer, Reviewer
│       ├── knowledge/
│       │   ├── base/        # Language-agnostic principles
│       │   ├── languages/   # Language-specific extensions
│       │   └── extensions/  # Project-specific conventions
│       ├── practices/       # Test-list workflow, conventional
│       │                    # commits
│       └── templates/       # Commit message template
├── blueprint_testlist_v2/   # Test-list blueprint (5 agents + Architect)
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
```

## Blueprints

### blueprint_testlist_v1 (4 agents)

**Test-list (spec-first), Lead handles task decomposition.**

The lead clarifies requirements with the user, reads the
codebase, decomposes work into tasks, and sends tasks to
the dev-team. The Test Engineer produces a test
specification (what to test), the Developer writes all
code (source and tests). Test Engineer verifies tests
match the spec before implementation starts, then gives a
post-implementation sign-off confirming tests were not
altered. Unified file ownership eliminates coordination
overhead.

**Agents:**
- Lead (user communication + codebase understanding + task decomposition)
- Developer (implements all code)
- Test Engineer (advisory — designs test specs, verifies coverage)
- Security Engineer (advisory — checks security)
- Reviewer (independent quality gate)

### blueprint_testlist_v2 (5 agents + Architect)

**Test-list (spec-first), Architect handles task decomposition.**

The lead focuses purely on user communication and team
coordination. The Architect reads the codebase, decomposes
work into tasks, writes plans to `.claude/plan.md`, and
feeds tasks to the dev-team sequentially. The dev-team
workflow is the same as v1 — Test Engineer produces test
specs, Developer implements, both engineers give sign-offs.

**Agents:**
- Lead (user communication + team coordination only)
- Architect (codebase understanding + task decomposition + planning)
- Developer (implements all code)
- Test Engineer (advisory — designs test specs, verifies coverage)
- Security Engineer (advisory — checks security)
- Reviewer (independent quality gate)

**Key differences from v1:**
- Lead is simpler — no Read/Glob/Grep, no codebase understanding
- Architect bridges between lead and dev-team
- Plans persist in `.claude/plan.md` for context continuity
- Better separation of concerns: communication vs technical analysis

## Container Template

`container_template/` provides a standalone prompt caching proxy
container. It injects `cache_control` blocks into Claude API
requests to enable prompt caching.

**Environment variables:**
- `PROXY_PORT` — Port to listen on (default: 3000)
- `TARGET_URL` — Upstream API URL (default: https://api.portkey.ai)
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
