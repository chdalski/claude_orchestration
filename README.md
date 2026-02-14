# Claude Orchestration Kit

A drop-in orchestration kit for Claude Code multi-agent
workflows. Copy the `blueprint/.claude/` directory into any
project to get a team of specialized agents (Architect,
Developer, Test Engineer, Code Reviewer, Security Engineer,
Tech Writer) coordinated by your Claude Code session, guided
by a shared knowledge base of software engineering principles.

## Why This Exists

Claude Code can spawn multiple agents that work together, but
out of the box each agent starts from scratch with no shared
understanding of engineering practices. This kit solves that by
providing:

1. **Pre-defined specialist roles** so the right agent handles
   the right task (architects don't write code, developers
   don't do security audits).
2. **A layered knowledge system** that gives every agent a
   common foundation of design principles (SOLID, TDD, FP,
   SSOT, code mass, hexagonal architecture) while automatically
   loading language-specific guidance (Rust, TypeScript, Python,
   Go) based on the project's file types.
3. **Increment-based workflows** that slice large tasks into
   small, committable units — each going through the full cycle
   of TDD, review, documentation, and conventional commit
   before the next one starts.

The goal is to encode good engineering judgment once and reuse
it across projects, rather than relying on each conversation to
rediscover the same principles.

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
cp -r blueprint/.claude/ /path/to/your/project/.claude/
```

Start Claude Code in your project directory. The CLAUDE.md
loads automatically and configures your session as the team
coordinator. Describe what you want to build, and it will
decompose the work, spawn the right specialist agents as
teammates, and coordinate their execution.

After creating a team, press **Shift+Tab** to enable delegate
mode. This restricts your session to coordination-only tools,
preventing it from implementing work directly.

## What's Included

```text
blueprint/.claude/
├── CLAUDE.md              # Orchestration instructions
├── settings.json          # Enables agent teams + hooks
├── agents/                # 6 agent definitions
│   ├── architect.md       # Solution design (opus)
│   ├── developer.md       # Implementation (opus)
│   ├── code-reviewer.md   # Code quality review (sonnet)
│   ├── test-engineer.md   # Testing (sonnet)
│   ├── security-engineer.md # Security audit (sonnet)
│   └── tech-writer.md     # Documentation (sonnet)
├── knowledge/
│   ├── base/              # Language-agnostic principles
│   │   ├── principles.md  # Simple Design, KISS, YAGNI, SOLID
│   │   ├── functional.md  # FP principles
│   │   ├── data.md        # SSOT guidelines
│   │   ├── code-mass.md   # APP complexity metric
│   │   ├── testing.md     # Testing pyramid, TDD principles
│   │   ├── documentation.md # Documentation principles
│   │   └── architecture.md  # Hexagonal architecture
│   ├── languages/         # Language-specific extensions
│   │   ├── rust.md
│   │   ├── typescript.md
│   │   ├── python.md
│   │   └── go.md
│   └── extensions/        # Project-specific conventions
│       └── README.md      # Guide for adding extensions
└── practices/
    ├── tdd.md             # TDD workflow
    └── hitl.md            # Human-in-the-loop checkpoints
```

## How It Works

Your Claude Code session acts as the team coordinator. It
receives your request, breaks it into tasks, and spawns
specialist agents as teammates. Each agent loads only the
knowledge files relevant to its role. Language-specific
extensions are detected automatically from the project's
code files — polyglot projects load all matching language
files.

### Feature Implementation

Large features are broken into **increments** — each one a
meaningful, encapsulated improvement with a conventional
commit type (e.g., `chore(scaffold)`, `feat(parser)`).

```text
Architect -> [per increment: TDD -> Review -> Docs -> Commit]
```

1. **Architecture**: Architect designs the solution and slices
   it into ordered increments. Each increment gets a file in
   `.claude/temp/increments/` that serves as the working
   contract for that cycle.
2. **Per increment**: Test Engineer writes a test list,
   Developer implements via TDD, Code Reviewer and Security
   Engineer review in parallel, Tech Writer updates docs,
   then a conventional commit is created.
3. **Cleanup**: After all increments are committed, temp files
   are deleted. The git log tells the full story.

### Other Workflows

- **Bug fix**: Test Engineer writes failing test first,
  Developer implements the fix
- **Fix batch**: For well-defined fixes from a review or audit,
  a single Developer subagent implements fixes and tests
- **Security audit**: Security Engineer reviews codebase
- **Documentation**: Tech Writer updates docs

### Hooks

The `settings.json` includes hooks that help agents maintain
context:

- **SessionStart**: Reminds agents to read their role
  definitions before starting work.
- **PreCompact**: Before context compaction, agents write a
  status summary to the increment file and notify the team
  lead, so context can be recovered after compaction.

## Project Extensions

After copying the blueprint, add project-specific conventions
in `knowledge/extensions/`. All agents load all files in this
directory during startup.

Example — create `knowledge/extensions/rust-conventions.md`:

```markdown
# Rust Conventions

**Agents**: Developer, Test Engineer, Code Reviewer

## Module Structure

- Use `module_name.rs` files, not `mod.rs` for modules.

## Test Placement

- Write unit tests as inline `#[cfg(test)]` modules.
- Use `/tests/` only for integration tests.
```

See `knowledge/extensions/README.md` for format details and
guidance on what belongs in extensions vs. in the project's
`CLAUDE.md`.

## Adding Languages

Create a file at `knowledge/languages/<language>.md`
following the pattern of existing language files. Include:

1. Language philosophy and idioms
2. How base principles apply in that language
3. Testing frameworks and patterns
4. Common pitfalls
5. Recommended tools and libraries

## Known Limitations

Agent teams are experimental. Be aware of:

- **No session resumption** — `/resume` and `/rewind` do not
  restore in-process teammates. After resuming, tell the lead
  to spawn new ones. The increment file preserves context so
  fresh agents can pick up where previous ones left off.
- **One team per session** — Clean up the current team before
  starting another.
- **No nested teams** — Only the lead can manage the team.
  Teammates cannot spawn their own teams.
- **Lead is fixed** — The session that creates the team stays
  the lead. Leadership cannot transfer.
- **Task status can lag** — Teammates sometimes fail to mark
  tasks completed, blocking dependent tasks. Check and update
  manually if stuck.
- **Shutdown can be slow** — Teammates finish their current
  tool call before shutting down.
- **File conflicts** — Two teammates editing the same file
  causes overwrites. The coordinator assigns file ownership
  to prevent this.
- **Permissions inherit** — All teammates inherit the lead's
  permission settings. Read-only tools need no approval.
  Edit, Write, and Bash prompts bubble up to the lead where
  the user approves them. Create `.claude/settings.local.json`
  with allow-rules to pre-approve common operations for
  trusted workflows.

## Customization

After copying into your project:

- Add project-specific conventions in
  `.claude/knowledge/extensions/` (preferred)
- Edit your project's root `CLAUDE.md` for build commands,
  repo structure, and setup instructions
- Modify agent definitions in `.claude/agents/` to adjust
  roles, models, or tool access
- Add new knowledge files in `.claude/knowledge/base/` for
  additional principles
- Extend language support in `.claude/knowledge/languages/`
