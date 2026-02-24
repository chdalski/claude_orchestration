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
│   ├── init-firewall.sh     # Network firewall setup
│   └── allowed-domains.conf # Configurable domain allowlist
├── blueprint_testlist_v1/   # Test-list blueprint (spec-first)
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
```

## Blueprint

**`blueprint_testlist_v1/`** — **Test-list (spec-first).**
The Test Engineer produces a test specification (what to
test), the Developer writes all code (source and tests).
Test Engineer verifies tests match the spec before
implementation starts, then gives a post-implementation
sign-off confirming tests were not altered. Unified file
ownership eliminates coordination overhead.

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

1. Verify `CLAUDE.md` (this file) reflects current structure
2. Verify `README.md` matches current blueprints and workflow
3. Update the project structure diagram if directories changed
