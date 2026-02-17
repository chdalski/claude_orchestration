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
├── CLAUDE.md              # This file (project context)
├── README.md              # User-facing documentation
├── blueprint/             # v1 blueprint (archived)
├── blueprint_v2/          # v2 blueprint (archived)
├── blueprint_v3/          # v3 blueprint (archived)
├── blueprint_v4/          # v4 blueprint (archived)
│   └── .claude/
│       ├── ...            # Same structure as v7
├── blueprint_v5/          # v5 blueprint (archived)
│   └── .claude/
│       ├── ...            # Same structure as v7
├── blueprint_v6/          # v6 blueprint (archived)
│   └── .claude/
│       ├── ...            # Same structure as v7
├── blueprint_v7/          # Current blueprint
│   └── .claude/
│       ├── CLAUDE.md      # Orchestration instructions
│       ├── settings.json  # Enables agent teams + hooks
│       ├── config.json    # Documentation files to check
│       ├── agents/        # Developer, Test Engineer,
│       │                  # Security Engineer, Reviewer
│       ├── knowledge/
│       │   ├── base/      # Language-agnostic principles
│       │   ├── languages/ # Language-specific extensions
│       │   └── extensions/# Project-specific conventions
│       ├── practices/     # TDD, conventional commits
│       └── templates/     # Commit message template
```

## Key Directories

- **`blueprint/`** — v1 blueprint, archived for reference.
- **`blueprint_v2/`** — v2 blueprint, archived for reference.
- **`blueprint_v3/`** — v3 blueprint, archived for reference.
- **`blueprint_v4/`** — v4 blueprint, archived for reference.
- **`blueprint_v5/`** — v5 blueprint, archived for reference.
- **`blueprint_v6/`** — v6 blueprint, archived for reference.
- **`blueprint_v7/`** — current orchestration design, in
  active development.

## Conventions

### Knowledge files (`blueprint_v7/.claude/knowledge/`)

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
