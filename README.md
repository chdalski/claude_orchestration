# Claude Orchestration Kit

A drop-in orchestration kit for Claude Code multi-agent
workflows. Copy the `blueprint/.claude/` directory into any
project to get a team of specialized agents (Orchestrator,
Architect, Developer, Test Engineer, Code Reviewer, Security
Engineer, Tech Writer) that coordinate automatically, guided
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
   SSOT, code mass) while automatically loading
   language-specific guidance (Rust, TypeScript, Python, Go)
   based on the project's file types.
3. **Standardized workflows** for common tasks (feature
   implementation, bug fixes, security audits, documentation)
   so the Orchestrator knows how to sequence work and set up
   dependencies between agents.

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

Then use the Orchestrator agent to handle complex tasks. It
will automatically spawn the right specialist agents, assign
work, and coordinate execution.

After creating a team, press **Shift+Tab** to enable delegate
mode. This restricts the lead to coordination-only tools,
matching the Orchestrator's design of never editing code
directly.

## What's Included

```text
blueprint/.claude/
├── CLAUDE.md              # Orchestration instructions
├── settings.json          # Enables agent teams + config
├── agents/                # 7 agent definitions
│   ├── orchestrator.md    # Team lead (opus)
│   ├── architect.md       # Solution design (opus)
│   ├── developer.md       # Implementation (sonnet)
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
│   │   └── testing.md     # TDD principles
│   └── languages/         # Language-specific extensions
│       ├── rust.md
│       ├── typescript.md
│       ├── python.md
│       └── go.md
└── practices/
    ├── tdd.md             # TDD workflow
    └── hitl.md            # Human-in-the-loop checkpoints
```

## How It Works

The Orchestrator agent receives a request, breaks it into
tasks, and spawns specialist agents as needed. Each agent
loads only the knowledge files relevant to its role.
Language-specific extensions are detected automatically from
the project's code files - polyglot projects load all
matching language files.

### Workflow Examples

- **New feature**: Architect designs, Developer implements,
  Test Engineer tests, Code Reviewer and Security Engineer
  review in parallel, Tech Writer documents
- **Bug fix**: Test Engineer writes failing test first,
  Developer implements the fix
- **Security audit**: Security Engineer reviews codebase
- **Documentation**: Tech Writer updates docs

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
  to spawn new ones.
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
  causes overwrites. The Orchestrator assigns file ownership
  to prevent this.
- **Permissions inherit** — All teammates inherit the lead's
  permission settings. Read-only tools need no approval.
  Edit, Write, and Bash prompts bubble up to the lead where
  the user approves them. Create `.claude/settings.local.json`
  with allow-rules to pre-approve common operations for
  trusted workflows.

## Customization

After copying into your project:

- Edit `.claude/CLAUDE.md` to add project-specific
  instructions
- Modify agent definitions in `.claude/agents/` to adjust
  roles or tool access
- Add new knowledge files for additional principles
- Extend language support as needed
