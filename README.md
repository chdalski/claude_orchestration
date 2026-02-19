# Claude Orchestration Kit

A drop-in orchestration kit for Claude Code multi-agent
workflows. Copy a blueprint's `.claude/` directory into any
project to get a team of specialized agents coordinated by
your Claude Code session, guided by a shared knowledge base
of software engineering principles.

## Repository Layout

```text
claude_orchestration/
├── blueprint_tdd_v1/        # TDD blueprint (test-first)
│   ├── .claude/             # Orchestration config + agents
│   └── .devcontainer/       # Sandboxed execution environment
└── blueprint_testlist_v1/   # Test-list blueprint (spec-first)
    ├── .claude/             # Orchestration config + agents
    └── .devcontainer/       # Sandboxed execution environment
```

## Choosing a Blueprint

Both blueprints use the same four agents, knowledge base,
and coordination principles. They differ in **who writes
test code**:

| | TDD (test-first) | Test-list (spec-first) |
|---|---|---|
| **Test Engineer** | Writes all test code | Designs test spec, verifies coverage |
| **Developer** | Writes source code only | Writes all code (source + tests) |
| **File ownership** | Split (TE owns tests, Dev owns source) | Unified (Dev owns everything) |
| **Coordination** | Dev waits for "tests ready" | Dev writes tests from spec, TE verifies |
| **Practice** | Red-green-refactor (TDD) | Test-list-driven development |
| **Tradeoff** | Structural enforcement of test-first | Less coordination overhead, faster cycles |

**TDD blueprint** — choose when you want strict enforcement
that tests exist before implementation, and are willing to
accept the coordination overhead of split file ownership.

**Test-list blueprint** — choose when you want faster cycles
with less agent coordination, accepting that test quality is
enforced through verification checkpoints rather than file
ownership boundaries.

## Prerequisites

Agent teams are an experimental Claude Code feature, disabled
by default. The included `settings.json` enables them
automatically when you copy the blueprint. You can also set
the environment variable directly:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

## Quick Start

Copy your chosen blueprint into your project:

```bash
# TDD blueprint
cp -r blueprint_tdd_v1/.claude/ /path/to/your/project/.claude/

# Or test-list blueprint
cp -r blueprint_testlist_v1/.claude/ /path/to/your/project/.claude/
```

Start Claude Code in your project directory. The CLAUDE.md
loads automatically and configures your session as the team
lead. Describe what you want to build, and it will
decompose the work into tasks and feed them to the dev-team.

## Devcontainer (Sandboxed Execution)

Each blueprint includes a `.devcontainer/` directory for
running agents in an isolated container with:

- **Network firewall** — outbound traffic restricted to
  an allowlist of domains (Anthropic API, GitHub, package
  registries, language docs). Edit
  `allowed-domains.conf` to add or remove domains —
  changes take effect on container restart, no rebuild
  needed.
- **UID/GID mapping** — container user matches the host
  user, so bind-mounted files have correct permissions
  regardless of the host's UID.
- **Autopilot permissions** — `bypassPermissions` mode
  is enabled automatically inside the container. The
  container is the security boundary, so per-tool prompts
  are unnecessary.
- **Host Claude config** — `~/.claude` is bind-mounted
  read-only so agents have access to API keys and
  settings without modifying the host config.

To use the devcontainer, copy it alongside `.claude/`:

```bash
cp -r blueprint_tdd_v1/.devcontainer/ /path/to/your/project/.devcontainer/
```

Then open the project in VS Code with the Dev Containers
extension, or use the `devcontainer` CLI.

## Agents

| Agent | Model | Role |
|-------|-------|------|
| **Developer** | opus | Implements code (scope depends on blueprint) |
| **Test Engineer** | opus | Test design and verification |
| **Security Engineer** | opus | Advisory — checks security gaps |
| **Reviewer** | opus | Quality gate — commits when satisfied |

## Workflow

```text
Lead -> Task -> Dev-Team -> Reviewer -> Commit
                  ^            |
                  '------------' (if rejected)
```

1. **Lead** decomposes the user's request into sequential
   tasks.
2. **Dev-team** (Developer, Test Engineer, Security
   Engineer) receives each task, discusses approach, then
   implements. The testing workflow depends on the blueprint
   chosen.
3. **Reviewer** examines the completed work. If satisfied,
   commits with a conventional commit message. If not, sends
   findings back to the full dev-team for fixes.
4. Lead sends the next task after commit.

## Knowledge Base

Engineering principles in `knowledge/` that agents load
during startup:

- **`base/`** — language-agnostic principles: Simple Design,
  KISS, YAGNI, SOLID, FP, SSOT, security (OWASP Top 10),
  code mass, hexagonal architecture, testing pyramid,
  documentation.
- **`languages/`** — language-specific extensions for Rust,
  TypeScript, Python, and Go. Each references the base
  principles it builds on.
- **`extensions/`** — project-specific conventions added
  after copying the blueprint into a target project.

## Adding Languages

Create a file at `knowledge/languages/<language>.md`
following the pattern of existing language files. Include:

1. Language philosophy and idioms
2. How base principles apply in that language
3. Testing frameworks and patterns
4. Common pitfalls
5. Recommended tools and libraries

## Project Extensions

After copying into your project, add project-specific
conventions in `.claude/knowledge/extensions/`. See
`knowledge/extensions/README.md` for format details.

## Known Limitations

Agent teams are experimental. Be aware of:

- **No session resumption** — `/resume` and `/rewind` do not
  restore in-process teammates.
- **One team per session** — Clean up the current team before
  starting another.
- **No nested teams** — Only the lead can manage the team.
- **Lead is fixed** — The session that creates the team stays
  the lead.
- **Task status can lag** — Teammates sometimes fail to mark
  tasks completed. Check and update manually if stuck.
- **Permissions inherit** — All teammates inherit the lead's
  permission settings.
