# Claude Orchestration Kit - Project Instructions

## What This Is

This repository contains a blueprint for Claude Code
multi-agent orchestration. It is not a runnable application.
The `blueprint_v2/` directory contains a `.claude/` setup
that gets copied into target projects to enable coordinated
multi-agent workflows.

## Project Structure

```text
claude_orchestration/
├── CLAUDE.md              # This file (project context)
├── README.md              # User-facing documentation
├── blueprint/             # v1 blueprint (archived)
├── blueprint_v2/          # Current blueprint
│   └── .claude/
│       ├── CLAUDE.md      # Orchestration instructions
│       ├── settings.json  # Enables agent teams + hooks
│       ├── agents/        # Developer, Reviewer
│       ├── knowledge/
│       │   ├── base/      # Language-agnostic principles
│       │   ├── languages/ # Language-specific extensions
│       │   └── extensions/# Project-specific conventions
│       ├── practices/     # TDD, conventional commits
│       └── templates/     # Commit message template
```

## Key Directories

- **`blueprint/`** — v1 blueprint, archived for reference.
- **`blueprint_v2/`** — current orchestration design, in
  active development.

## Conventions

### Knowledge files (`blueprint_v2/.claude/knowledge/`)

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
