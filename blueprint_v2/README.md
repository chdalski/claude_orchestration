# Plan-First Blueprint (v2)

Plan-first, workflow-based blueprint for Claude Code
multi-agent orchestration. The lead clarifies and plans
before any execution begins. Workflows define how work
gets done.

## How It Works

### Planning Approach

The lead starts every session in plan mode. It clarifies
the task with the user, writes a plan to `.ai/plans/`,
then proposes a workflow from `.claude/workflows/`. No
agents are spawned and no code is touched until the user
approves the approach. This front-loads understanding and
avoids wasting tokens on misunderstood requirements.

### Startup

1. Lead spawns the Auditor in the background to check
   CLAUDE.md integrity.
2. Lead checks for existing plans from previous sessions.
3. Lead begins clarification with the user.
4. When the Auditor reports, the lead notes any
   discrepancies and prepends a fix step to the plan if
   codebase changes are involved.

### Agents

| Agent | Model | Role | Writes Code |
|-------|-------|------|-------------|
| **Auditor** | haiku | Checks CLAUDE.md accuracy | No (read-only) |
| **Committer** | haiku | Stages and commits files | No (git only) |

The Auditor runs at session start to catch stale
instructions. The Committer is a shared utility — any
workflow can use it to commit work without bundling commit
logic into review or implementation agents.

Workflow-specific agents (Developer, Reviewer, etc.) are
added as workflows are defined.

### Workflows

Workflows live in `.claude/workflows/` as separate
markdown files. Each workflow defines which agents it
needs, the step-by-step execution flow, and completion
criteria. Adding a new workflow requires no changes to
CLAUDE.md — just add a file.

See `.claude/workflows/CLAUDE.md` for the required format
and the list of shared agents available to all workflows.

### Conventional Commits

All commits use conventional prefixes (`feat:`, `fix:`,
`chore:`, etc.) for scannable git history. The Committer
receives the full commit message from its caller — it
does not choose the prefix or message itself.

## Setup

```bash
cp -r .claude/ /path/to/your/project/.claude/
cp -r .ai/ /path/to/your/project/.ai/
```

Optionally, copy the devcontainer for sandboxed execution
with a network firewall and autopilot permissions:

```bash
cp -r .devcontainer/ /path/to/your/project/.devcontainer/
```

See the repository README for prerequisites, devcontainer
details, and configuration options.
