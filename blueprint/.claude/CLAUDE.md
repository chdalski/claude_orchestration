# Claude Orchestration Kit

## Overview

This project uses a multi-agent orchestration system with
specialized agent roles and a layered knowledge system for
consistent engineering best practices.

## Agents

The following specialist agents are available in `agents/`:

| Agent | Model | Role |
|-------|-------|------|
| **Orchestrator** | opus | Team lead - coordinates agents, manages tasks |
| **Architect** | opus | Analyzes codebase, designs solutions |
| **Developer** | sonnet | Implements features, fixes bugs |
| **Test Engineer** | sonnet | Writes and runs tests |
| **Code Reviewer** | sonnet | Reviews code for quality and best practices |
| **Security Engineer** | sonnet | Audits code for vulnerabilities |
| **Tech Writer** | sonnet | Writes and maintains documentation |

## Knowledge System

### Base Knowledge (`knowledge/base/`)

Language-agnostic engineering principles. Each agent loads
only the files relevant to its role (see agent definitions):

- **principles.md** - Kent Beck's 4 Rules of Simple Design,
  KISS, YAGNI, SOLID
- **functional.md** - Functional programming principles
- **data.md** - Single Source of Truth (SSOT) guidelines
- **code-mass.md** - Absolute Priority Premise (APP) for
  measuring code complexity
- **testing.md** - TDD principles and best practices

### Language Extensions (`knowledge/languages/`)

Language-specific guidance that extends the base principles.
Agents detect project languages and load **all** matching
files (polyglot projects get multiple):

- **rust.md** - Ownership, type system, error handling,
  iterators, async
- **typescript.md** - Strict types, React patterns, Node.js,
  testing with Vitest/Jest
- **python.md** - Pythonic patterns, type hints, pytest,
  functional tools
- **go.md** - Idioms, error handling, concurrency, table-driven
  tests

### How Language Detection Works

1. Scan the project for code file extensions using Glob
2. Only count code extensions - ignore non-code files:
   - **Count**: `.rs`, `.ts`, `.tsx`, `.js`, `.jsx`, `.py`,
     `.go`, `.rb`, `.java`, `.kt`, `.cs`, `.cpp`, `.c`, `.h`
   - **Ignore**: `.md`, `.json`, `.yaml`, `.yml`, `.toml`,
     `.lock`, `.css`, `.scss`, `.html`, `.svg`, `.txt`
3. Map extensions to language files:
   - `.rs` -> `rust.md`
   - `.ts`, `.tsx`, `.js`, `.jsx` -> `typescript.md`
   - `.py` -> `python.md`
   - `.go` -> `go.md`
4. Load **every** language file that has matching extensions
   in the project (not just the most common one)
5. If no code extensions match any language file, skip
   language-specific loading

## Practices

Workflow practices in `practices/`:

- **tdd.md** - Test-Driven Development process
- **hitl.md** - Human-in-the-loop checkpoints for TDD

## Workflow Patterns

### Feature Implementation

```text
Architect -> Developer + Test Engineer
-> Code Reviewer + Security Engineer -> Tech Writer
```

1. Architect analyzes codebase and creates implementation plan
2. Developer implements following architect's guidance
3. Test Engineer writes and runs tests
4. Code Reviewer and Security Engineer review in parallel
5. Developer addresses findings
6. Tech Writer updates documentation

### Bug Fix

```text
Developer -> Test Engineer
```

1. Developer investigates and fixes the bug
2. Test Engineer writes regression test and verifies

### Security Audit

```text
Security Engineer -> Developer (if fixes needed)
```

1. Security Engineer performs audit and reports findings
2. Developer implements fixes based on findings

### Documentation Update

```text
Tech Writer
```

1. Tech Writer reads code and updates documentation

## Agent Startup Protocol

Every agent follows the startup sequence defined in its own
agent file. The general pattern is:

1. Read `CLAUDE.md` for project-specific instructions
2. Load the knowledge/base files relevant to the agent's role
3. Detect project languages and load all matching
   `knowledge/languages/<lang>.md` files (see detection
   algorithm above)
4. Load practices files as needed for the task

Agents load knowledge selectively to conserve context:

| Agent | Base Knowledge | Practices |
|-------|---------------|-----------|
| Orchestrator | principles | - |
| Architect | principles, functional, data | - |
| Developer | principles, functional, code-mass (when refactoring) | tdd, hitl (on demand) |
| Code Reviewer | principles, functional, code-mass | - |
| Test Engineer | testing, code-mass | tdd, hitl (on demand) |
| Security Engineer | - | - |
| Tech Writer | - | - |

## Rules

- **Orchestrator coordinates, doesn't implement** - It reads
  code and assigns work but never edits files
- **Agents follow knowledge principles** - All agents should
  reference and apply the knowledge base
- **Not every task needs every agent** - The orchestrator
  decides which agents to spawn based on the request
- **Dependencies matter** - Tasks should have proper ordering
  so agents don't work on dependent tasks prematurely
- **Language extensions augment, not replace** - Base knowledge
  always applies; language files add specifics
