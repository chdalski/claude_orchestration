# Direct-Review

Multi-agent orchestration blueprint for Claude Code. The
lead is the user's advisor by default: it clarifies, weighs
options, and recommends — without editing files. It
implements only when the user explicitly asks, one plan
task at a time, behind an independent Reviewer gate (plus
Security Engineer pre/post gates for security-relevant
work), and waits for the user's review after every task.
3 agents (reviewer, security-engineer, plan-reviewer) plus
the lead.

## Build and Test

```sh
uv run pytest blueprints/direct-review/tests/ -m static -v
```

## Components

| Path | Purpose |
|---|---|
| `.claude/CLAUDE.md` | Lead instructions — clarification, advise mode, planning, per-task implementation gates |
| `.claude/settings.json` | Agent teams config, plans directory path |
| `.claude/agents/reviewer.md` | Quality gate — scope, code review, commit message; never commits (Opus) |
| `.claude/agents/security-engineer.md` | Advisory — decision consultations and pre/post-implementation sign-offs (Opus) |
| `.claude/agents/plan-reviewer.md` | Plan quality gate — launched as subagent before user presentation (Sonnet) |
| `.claude/rules/` | Unconditional + conditional rules injected by Claude Code |
| `.claude/skills/ensure-ai-dirs/` | Skill: creates `.ai/plans/` and `.ai/memory/`, syncs plan format guide and review checklist, moves finished plans into `completed/` |
| `.claude/skills/project-init/` | Skill: scans project, generates `CLAUDE.md` per `project-context.md`, enables code intelligence plugins |
| `.claude/skills/project-sanity/` | Skill: audits repo for common issues (report-only) |
| `tests/blueprint_contracts.py` | Single source of truth for required structure and agent frontmatter |
| `tests/static/` | Structure, caching compliance, agent frontmatter, rule length, flow contract tests |

## Conventions

<!-- Agents: add non-obvious project conventions discovered during work — things a future agent would need to know to avoid mistakes. One line each. Remove when no longer true. -->

- Derived from aida's Direct-Review workflow (Reviewer-only + Security-Hybrid paths); rules and skills come from the autonomous blueprint
- One flow, written into `.claude/CLAUDE.md` — no `workflows/` directory, no workflow menu
- Advise mode is the default; only an explicit implement request enters Implement mode — imperative phrasing ("fix X") starts clarification, not edits
- The lead implements; there is no developer or test-engineer agent
- `risk-assessment.md` is the single source for path selection: Reviewer-only, Security-Hybrid, or escalate to the user
- Escalation triggers (high-risk categories; behavioral change without covering tests) keep the lead in advise mode until the user explicitly chooses Security-Hybrid anyway or handling outside the blueprint
- Security-Hybrid requires separately named pre- and post-implementation sign-offs; `advisor-gate-independence.md` lists what cannot stand in for either
- Advise-mode Security Engineer consultations are stateless subagents (no `name`); implementation gates use teammates spawned per task
- Teammates are spawned before a task's first edit and shut down after its commit — no context carries across tasks
- The user reviews every task after Reviewer approval; the lead waits for the user's go before the next task
- The Reviewer composes the commit message and file list; the lead commits after user approval with a `Plan:` trailer
- No WIP commits and no ad-hoc commits mid-task — a mid-task commit lands inside the task's diff and escapes the gates
- Agent files define role only — no named teammates, no workflow names; use "the requester" / "the implementor"
- Agent `name:` fields use lowercase hyphenated form
- All blueprint files must be fully static — no dates, counters, versions (prompt cache level 3)
- Rule files target under 200 lines — agent adherence degrades beyond that threshold
- Terminology: "launch" subagents, "spawn" and "shut down" teammates, "message" within teams

## References

<!-- Agents: add authoritative sources used to make implementation decisions. One line each. -->

- [Claude Code documentation](https://code.claude.com/docs)
