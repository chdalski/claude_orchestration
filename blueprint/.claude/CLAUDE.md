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
- **testing.md** - Testing principles: test design, structure,
  naming, anti-patterns

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

- **tdd.md** - TDD execution workflow: red-green-refactor
  cycle, guessing game, baby steps
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
Test Engineer -> Developer
```

1. Test Engineer writes a failing test that reproduces the bug
2. Developer implements the minimal fix to make it pass

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

Agents load knowledge selectively to conserve context.
All agents also load language-specific files based on
project detection.

**Base knowledge** (`knowledge/base/`):

| Agent             | Files loaded                          |
|-------------------|---------------------------------------|
| Orchestrator      | principles                            |
| Architect         | principles, functional, data          |
| Developer         | principles, functional                |
| Code Reviewer     | principles, functional, code-mass     |
| Test Engineer     | testing                               |
| Security Engineer | (none)                                |
| Tech Writer       | (none)                                |

Conditional base knowledge:

- **Developer** loads `code-mass` when refactoring
- **Test Engineer** loads `code-mass` during the refactor
  phase of TDD

**Practices** (`practices/`):

| Agent         | Files loaded         |
|---------------|----------------------|
| Developer     | tdd, hitl (on demand)|
| Test Engineer | tdd, hitl (on demand)|

Only Developer and Test Engineer load practice files.
The `hitl` practice is loaded when the user requests
human-in-the-loop checkpoints; otherwise agents use
`tdd` autonomously.

## Agent Teams Setup

Agent teams are experimental and require explicit opt-in.
The `settings.json` in this directory enables them with
`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` and sets
`teammateMode` to `in-process`.

### Delegate Mode

The Orchestrator is designed as a coordination-only lead — it
reads code and manages tasks but never edits files. After
creating a team, press **Shift+Tab** to enable delegate mode.
This restricts the lead to coordination tools only (spawning,
messaging, task management), preventing it from implementing
work itself. This matches the Orchestrator's intended role.

### Permissions

All teammates inherit the lead session's permission settings
at spawn time. Read-only tools (Read, Glob, Grep) require no
approval by default. File modifications (Edit, Write) and
shell commands (Bash) will prompt the user for approval
through the lead's session.

This means the user stays in control: when a Developer or
Test Engineer teammate first tries to edit a file or run a
command, the prompt bubbles up to the lead where the user
approves or denies it.

To reduce friction for trusted workflows, users can create
a `.claude/settings.local.json` (not checked into version
control) with allow-rules:

```json
{
  "permissions": {
    "allow": [
      "Edit",
      "Write",
      "Bash(npm run *)",
      "Bash(cargo *)"
    ]
  }
}
```

Other options:

- Use `--dangerously-skip-permissions` for fully trusted
  local-only workflows. All teammates inherit this setting.
- You cannot set per-teammate permissions at spawn time.
  Adjust individual teammate modes after they are running if
  needed.

### Limitations

Agent teams have known limitations to be aware of:

- **No session resumption** — `/resume` and `/rewind` do not
  restore in-process teammates. After resuming, the lead may
  try to message teammates that no longer exist. Tell it to
  spawn new ones.
- **One team per session** — A lead can only manage one team
  at a time. Clean up the current team before starting
  another.
- **No nested teams** — Teammates cannot spawn their own
  teams. Only the lead manages the team.
- **Lead is fixed** — The session that creates the team stays
  the lead for its lifetime. Leadership cannot transfer.
- **Task status can lag** — Teammates sometimes fail to mark
  tasks completed, blocking dependent tasks. Check manually
  and update if stuck.
- **Shutdown can be slow** — Teammates finish their current
  tool call before shutting down.
- **File conflicts** — Two teammates editing the same file
  causes overwrites. The Orchestrator must ensure each
  teammate owns different files.

## Rules

- **Orchestrator coordinates, doesn't implement** - It reads
  code and assigns work but never edits files. Use delegate
  mode (Shift+Tab) to enforce this.
- **Agents follow knowledge principles** - All agents should
  reference and apply the knowledge base
- **Not every task needs every agent** - The orchestrator
  decides which agents to spawn based on the request
- **Dependencies matter** - Tasks should have proper ordering
  so agents don't work on dependent tasks prematurely
- **Language extensions augment, not replace** - Base knowledge
  always applies; language files add specifics
