# Claude Orchestration Kit - Project Instructions

## What This Is

This repository contains a **blueprint** for Claude Code
multi-agent orchestration. It is not a runnable application.
The `blueprint/` directory contains a `.claude/` setup that
gets copied into target projects to enable coordinated
multi-agent workflows.

## Project Structure

```text
claude_orchestration/
├── CLAUDE.md              # This file (project context)
├── README.md              # User-facing documentation
├── blueprint/             # The copyable kit
│   └── .claude/           # Copied into target project
│       ├── CLAUDE.md      # Orchestration instructions
│       ├── agents/        # 7 agent definitions
│       ├── knowledge/
│       │   ├── base/      # Language-agnostic principles
│       │   └── languages/ # Language-specific extensions
│       └── practices/     # TDD, human-in-the-loop
└── starting_rules/        # Legacy source material (archived)
```

## Key Distinction

- **This `CLAUDE.md`** is for working on the blueprint itself.
- **`blueprint/.claude/CLAUDE.md`** is the template that gets
  copied into target projects and loaded by agents there.

## Conventions

### Knowledge files (`blueprint/.claude/knowledge/`)

- `base/` files are **language-agnostic**. No code examples
  in any specific language. Use pseudocode or prose
  descriptions. Agents produce language-specific examples on
  demand based on the target project's languages.
- `languages/` files contain language-specific guidance that
  extends the base principles. Each file references the base
  principles it builds on.

### Agent files (`blueprint/.claude/agents/`)

- Each agent has YAML frontmatter: name, description, model,
  color, tools.
- Agents load knowledge **selectively** based on their role,
  not everything.
- Language detection algorithm is defined once in
  `blueprint/.claude/CLAUDE.md`. Agent files reference it
  rather than duplicating it.
- Polyglot projects load all matching language files.

### Practices

- `practices/` files are language-agnostic workflow guidance.

## Legacy

`starting_rules/` contains the original Rust-specific rules
this project was refactored from. It is kept for reference
but is not part of the blueprint.
