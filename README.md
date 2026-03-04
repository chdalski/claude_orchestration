# Claude Orchestration Kit

A drop-in orchestration kit for Claude Code multi-agent
workflows. Copy a blueprint's `.claude/` directory into any
project to get a team of specialized agents coordinated by
your Claude Code session.

## Repository Layout

```text
claude_orchestration/
├── .devcontainer/           # Sandboxed execution environment
├── blueprint_testlist/      # Test-list blueprint (5 agents)
│   └── .claude/             # Orchestration config + agents
└── blueprint_v2/            # Plan-first blueprint (workflow-based)
    ├── .claude/             # Lead instructions, agents, rules, workflows
    └── .ai/                 # Plan documents
```

## Blueprints

### Test-List Blueprint (blueprint_testlist)

**Test-list (spec-first), Architect handles task
decomposition.**

The lead focuses on user communication and team
coordination. The Architect reads the codebase, decomposes
work into tasks, writes plans to `.claude/plan.md`, and
feeds tasks to the dev-team sequentially. The Test Engineer
produces test specs, the Developer writes all code (source
and tests). Both Test Engineer and Security Engineer give
post-implementation sign-offs before review.

**Agents:** Lead, Architect, Developer, Test Engineer,
Security Engineer, Reviewer

| Agent | Model | Role |
|-------|-------|------|
| **Architect** | sonnet | Reads codebase, decomposes tasks, writes plans |
| **Developer** | sonnet | Implements all code (source + tests) |
| **Test Engineer** | sonnet | Advisory — designs test specs, verifies coverage |
| **Security Engineer** | sonnet | Advisory — checks security gaps |
| **Reviewer** | opus | Quality gate — commits when satisfied |

**Workflow:**

```text
User -> Lead -> Story -> Architect -> Task -> Dev-Team -> Reviewer -> Commit
         ^                  |          ^        |            |
         |                  |          |        '------<-----' (if rejected)
         '--------<---------'          '--------<-----' (questions)
```

1. **Lead** clarifies requirements with user
2. **Architect** receives clarified story, reads codebase,
   decomposes into tasks, writes plan to `.claude/plan.md`
3. **Dev-team** receives task from Architect, implements
4. **Reviewer** commits or rejects (coordinated by Lead)
5. Architect sends next task after commit

The dev-team (Developer, Test Engineer, Security Engineer)
discusses approach before implementing. Test Engineer
produces test spec, Developer writes tests, Test Engineer
verifies before implementation starts. Post-implementation:
both Test Engineer and Security Engineer give sign-offs
before review.

**Knowledge base:** Engineering principles in `knowledge/`
that agents load during startup — language-agnostic base
principles, language-specific extensions (Rust, TypeScript,
Python, Go), and project-specific conventions in
`extensions/`.

### Plan-First Blueprint (blueprint_v2)

**Plan-first, workflow-based.** The lead starts in plan
mode, clarifies the task, spawns an Architect to write a
plan to `.ai/plans/`, and the user approves before
execution. Workflows define execution patterns — adding a
new workflow is just adding a file. Language-specific
guidance loads automatically via conditional rules (no
manual knowledge loading).

**Agents:** Lead, Architect, Auditor, Committer, Developer,
Test Engineer, Security Engineer, Reviewer

| Agent | Model | Role |
|-------|-------|------|
| **Architect** | opus | Reads codebase, writes plans, decomposes and feeds tasks |
| **Auditor** | haiku | Checks CLAUDE.md accuracy |
| **Committer** | haiku | Stages and commits files |
| **Developer** | sonnet | Implements all code (source + tests) |
| **Test Engineer** | sonnet | Advisory — designs test specs, verifies coverage |
| **Security Engineer** | sonnet | Advisory — checks security gaps |
| **Reviewer** | sonnet | Independent quality gate — reviews, does not commit |

**Workflows:**

- **Develop-Review** — test-list-driven development with
  security review and independent quality gate. The
  Reviewer reviews but does not commit (Committer handles
  commits).

**Best for:** Projects wanting plan-first development with
flexible workflow selection and automatic language-specific
guidance. See `blueprint_v2/README.md` for full details.

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
# Test-list blueprint
cp -r blueprint_testlist/.claude/ /path/to/your/project/.claude/

# OR plan-first blueprint
cp -r blueprint_v2/.claude/ /path/to/your/project/.claude/
cp -r blueprint_v2/.ai/ /path/to/your/project/.ai/
```

Start Claude Code in your project directory. The CLAUDE.md
loads automatically and configures your session as the team
lead.

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
