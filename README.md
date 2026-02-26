# Claude Orchestration Kit

A drop-in orchestration kit for Claude Code multi-agent
workflows. Copy a blueprint's `.claude/` directory into any
project to get a team of specialized agents coordinated by
your Claude Code session, guided by a shared knowledge base
of software engineering principles.

## Repository Layout

```text
claude_orchestration/
├── .devcontainer/           # Sandboxed execution environment
├── blueprint_testlist_v1/   # Test-list blueprint (4 agents)
│   └── .claude/             # Orchestration config + agents
└── blueprint_testlist_v2/   # Test-list blueprint (5 agents + Architect)
    └── .claude/             # Orchestration config + agents
```

## Blueprints

Both blueprints use the **test-list (spec-first)** workflow:

| | Test-list (spec-first) |
|---|---|
| **Test Engineer** | Designs test spec, verifies coverage |
| **Developer** | Writes all code (source + tests) |
| **File ownership** | Unified (Dev owns everything) |
| **Coordination** | Dev writes tests from spec, TE verifies |
| **Practice** | Test-list-driven development |

The Developer owns all code, eliminating file-conflict
coordination. Test quality is enforced through verification
checkpoints: the Test Engineer verifies tests match the spec
before implementation, then confirms tests were not altered
after implementation.

### v1: Lead Decomposes Tasks (4 agents)

The lead handles everything: clarifies requirements with
the user, reads the codebase, decomposes work into tasks,
and sends tasks to the dev-team.

**Agents:** Lead, Developer, Test Engineer, Security Engineer, Reviewer

**Best for:** Smaller projects, or when you want the lead
to understand the codebase directly.

### v2: Architect Decomposes Tasks (5 agents)

The lead focuses purely on user communication and
coordination. The Architect reads the codebase, decomposes
work into tasks, writes plans to `.claude/plan.md`, and
feeds tasks to the dev-team.

**Agents:** Lead, Architect, Developer, Test Engineer, Security Engineer, Reviewer

**Best for:** Larger projects, or when you want clearer
separation between communication (lead) and technical
analysis (architect). The plan file persists across
context compaction.

## Prerequisites

Agent teams are an experimental Claude Code feature, disabled
by default. The included `settings.json` enables them
automatically when you copy the blueprint. You can also set
the environment variable directly:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

## Quick Start

Copy a blueprint into your project:

```bash
# v1 (lead decomposes tasks)
cp -r blueprint_testlist_v1/.claude/ /path/to/your/project/.claude/

# OR v2 (architect decomposes tasks)
cp -r blueprint_testlist_v2/.claude/ /path/to/your/project/.claude/
```

Start Claude Code in your project directory. The CLAUDE.md
loads automatically and configures your session as the team
lead. Describe what you want to build:

- **v1:** Lead decomposes work and sends tasks to dev-team
- **v2:** Lead clarifies requirements, sends story to Architect, who decomposes and manages dev-team

## Devcontainer (Sandboxed Execution)

The root `.devcontainer/` directory provides an isolated
container for running agents with:

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
cp -r .devcontainer/ /path/to/your/project/.devcontainer/
```

Then open the project in VS Code with the Dev Containers
extension, or use the `devcontainer` CLI.

## Agents

### v1 (4 agents)

| Agent | Model | Role |
|-------|-------|------|
| **Developer** | sonnet | Implements all code (source + tests) |
| **Test Engineer** | sonnet | Advisory — designs test specs, verifies coverage |
| **Security Engineer** | sonnet | Advisory — checks security gaps |
| **Reviewer** | opus | Quality gate — commits when satisfied |

### v2 (5 agents)

| Agent | Model | Role |
|-------|-------|------|
| **Architect** | sonnet | Reads codebase, decomposes tasks, writes plans |
| **Developer** | sonnet | Implements all code (source + tests) |
| **Test Engineer** | sonnet | Advisory — designs test specs, verifies coverage |
| **Security Engineer** | sonnet | Advisory — checks security gaps |
| **Reviewer** | opus | Quality gate — commits when satisfied |

## Workflow

### v1 Workflow

```text
User -> Lead -> Task -> Dev-Team -> Reviewer -> Commit
                 ^         |           |
                 |         '-----<-----' (if rejected)
                 '-----<-----' (questions)
```

1. **Lead** clarifies requirements with user, reads codebase,
   decomposes into tasks
2. **Dev-team** receives task, implements
3. **Reviewer** commits or rejects
4. Lead sends next task after commit

### v2 Workflow

```text
User -> Lead -> Story -> Architect -> Task -> Dev-Team -> Reviewer -> Commit
         ^                  |          ^        |            |
         |                  |          |        '------<-----' (if rejected)
         '--------<---------'          '--------<-----' (questions)
```

1. **Lead** clarifies requirements with user using AskUserQuestion
2. **Architect** receives clarified story, reads codebase,
   decomposes into tasks, writes plan to `.claude/plan.md`
3. **Dev-team** receives task from Architect, implements
4. **Reviewer** commits or rejects (coordinated by Lead)
5. Architect sends next task after commit

In both workflows:

- **Dev-team** (Developer, Test Engineer, Security Engineer)
  discusses approach before implementing
- Test Engineer produces test spec, Developer writes tests,
  Test Engineer verifies before implementation starts
- Post-implementation: both Test Engineer and Security
  Engineer give sign-offs before review

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
