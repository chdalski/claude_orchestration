# Claude Orchestration Kit

Blueprints for Claude Code multi-agent orchestration. Not a
runnable application — each blueprint directory contains a
`.claude/` setup that gets copied into target projects to
enable coordinated multi-agent workflows.

## Build and Test

This project runs in a Docker container. Install `uv` on
first use — it is required to run the test suite.

```sh
which uv || curl -LsSf https://astral.sh/uv/install.sh | sh
uv run pytest blueprints/workflow/tests/ -m static -v
uv run pytest blueprints/autonomous/tests/ -m static -v
```

## Components

| Path | Purpose |
|---|---|
| `blueprints/workflow/` | Clarify-first blueprint — user chooses workflow |
| `blueprints/autonomous/` | Autonomous blueprint — plan queue + developer |
| `devcontainer_templates/` | Devcontainer setup for sandboxed agent execution |
| `CONTRIBUTING.md` | How to develop and extend blueprints |

### workflow

Clarify-first: the lead clarifies the task, then presents
workflow options. The user chooses: Direct-Review for simple
tasks, Develop-Review (Supervised or Autonomous) for complex
ones, or TDD User-in-the-Loop. 5 team agents (Architect,
Developer, Test Engineer, Security Engineer, Reviewer)
plus the lead, with two on-demand subagents launched
during planning and TDD entry: `plan-reviewer` (reviews
draft plans before user presentation) and `test-list`
(converts an example mapping into a minimum required
test list).
Workflows defined as separate files — adding one requires
no changes to CLAUDE.md or agents.

### autonomous

Autonomous after clarification: the lead clarifies, writes
a plan, manages a plan queue. For each task, the lead
assesses risk and directs the developer to consult advisors
when warranted. The developer implements, the reviewer
approves and commits. 4 team agents (Developer, Reviewer,
Test Engineer, Security Engineer) plus the lead and the
`plan-reviewer` subagent (launched before user plan
presentation). The lead stays responsive to the user
during execution.

### devcontainer_templates

Docker-based sandboxing for agent execution. Project-scoped
volume for Claude config, dual auth mode (`proxy`/`oauth`)
via `CLAUDE_AUTH` env var, base and audio variants.

## Conventions

<!-- Agents: add non-obvious project conventions discovered
during work — things a future agent would need to know to
avoid mistakes. One line each. Remove when no longer true. -->

- Two levels of `.claude/`: project-level (`/.claude/`) is tooling for this repo, never copied; blueprint-level (`blueprints/*/.claude/`) gets copied to target projects
- Use "lead" not "orchestrator" — Claude Code's native term for the session that manages the team
- Every directive in blueprint markdown files must include its rationale (see `reasoned-instructions.md` rule)
- Agent files define role and capability only — no named teammates, no workflow-specific coordination (see `agent-design.md` rule)
- Agent `name:` fields in frontmatter use lowercase hyphenated form: `developer`, `test-engineer`
- Use official terminology: "launch" subagents, "create" teams, "spawn" teammates, "message" within teams (see `terminology.md` rule)
- Rule files and CLAUDE.md files target under 200 lines — agent adherence degrades beyond that threshold
- Blueprint files are cached at prompt cache level 3 — no dynamic content (dates, counters, versions)
- Test suite uses pytest with `-m static` marker for structural verification

## References

<!-- Agents: add authoritative sources used to make
implementation decisions. One line each. -->

- [Claude Code documentation](https://code.claude.com/docs)

## Session Checklist

Before ending a session that modified blueprint files:

1. Verify all changes are safe, sound, and concise
2. Verify this file (`CLAUDE.md`) still reflects reality
3. Verify root `README.md` matches current blueprints
4. Run `uv run pytest blueprints/<name>/tests/ -m static -v`
