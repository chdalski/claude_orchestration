# Blueprint v3 — Autonomous

Multi-agent orchestration blueprint for Claude Code.
After clarification and user-approved planning, the lead
feeds tasks to the developer autonomously. The developer
implements and sends to the reviewer for independent
quality review and commit. No user checkpoints gate
individual tasks after plan approval. 4 agents (developer,
reviewer, test-engineer, security-engineer) plus the lead.

## Build and Test

```sh
uv run pytest blueprints/autonomous/tests/ -m static -v
```

## Components

| Path | Purpose |
|---|---|
| `.claude/CLAUDE.md` | Lead instructions — clarification, planning, plan queue, task dispatch |
| `.claude/settings.json` | Agent teams config, plans directory path |
| `.claude/agents/developer.md` | Implements all code — source and tests (Sonnet) |
| `.claude/agents/reviewer.md` | Quality gate — scope verification, plan tracking, commits (Opus) |
| `.claude/agents/test-engineer.md` | Advisory — test design on demand (Sonnet) |
| `.claude/agents/security-engineer.md` | Advisory — security assessment on demand (Sonnet) |
| `.claude/rules/` | Unconditional + conditional rules injected by Claude Code |
| `.claude/skills/ensure-plans-dir/` | Skill: creates `.ai/plans/` directory and format guide |
| `.claude/skills/project-init/` | Skill: scans project, generates `CLAUDE.md` per `project-context.md` |
| `.claude/skills/project-sanity/` | Skill: audits repo for common issues (report-only) |
| `tests/blueprint_contracts.py` | Single source of truth for required structure and agent frontmatter |
| `tests/static/` | Structure, caching compliance, agent frontmatter, rule length tests |

## Conventions

<!-- Agents: add non-obvious project conventions discovered during work — things a future agent would need to know to avoid mistakes. One line each. Remove when no longer true. -->

- Agent files define role only — no named teammates, no workflow coordination, no workflow conditionals
- Use "the requester" / "the implementor" in agent files — never role-specific names
- Agent `name:` fields use lowercase hyphenated form: `developer`, `test-engineer`
- Unconditional rules (no `paths:` frontmatter): `simplicity.md`, `risk-assessment.md`, `procedural-fidelity.md`, `acceptance-criteria.md`, `safe-git.md`, `claim-verification.md`
- Conditional rules load automatically when agents touch matching file extensions
- Universal principles stated once in unconditional rules — language rules extend without restating
- Adding a new language: create `lang-<language>.md` with `paths:` frontmatter, update `functional-style.md`/`code-mass.md`/`code-principles.md` paths — no changes to CLAUDE.md or agents
- Lead-directed advisor consultation — lead assesses risk at dispatch time per `risk-assessment.md`
- Advisor consultation requires two gates in the dispatch message: input gate (consult before implementing) and output gate (get sign-off before submitting to reviewer)
- Developer may add advisor consultations but not remove lead's directives
- Reviewer owns plan file during execution — marks tasks done, records commit SHAs
- Developer makes WIP commits during implementation — reviewer squashes at approval time via `git reset <baseline-sha>`
- Reviewer backstop: rejects if non-trivial behavioral changes lack tests and no advisor was consulted
- Infeasibility claims require specific evidence (file, function, scope, own code vs dependency) per `claim-verification.md` — category labels are not sufficient
- Lead verifies plan goal at completion — adds follow-up tasks if quantitative targets not met
- All blueprint files must be fully static — no dates, counters, versions (prompt cache level 3)
- Rule files target under 200 lines — agent adherence degrades beyond that threshold
- Skills run at startup before team exists — lead commits skill outputs directly per skill-output commit rule
- Templates live in their skill's directory, not a separate `templates/` directory
- Generated project `CLAUDE.md` follows `project-context.md`: Overview, Build and Test, Components, Conventions, References
- On `CLAUDE.md` re-generation: Overview/Build/Components refresh; Conventions/References entries preserve
- Execution pipeline: Lead → Developer → Reviewer → Lead (developer-reviewer rejection loop is opaque to lead)
- Team is cycled (TeamDelete + TeamCreate) between task slices — prevents developer context degradation across tasks
- Plan queue supports multiple concurrent plans — ordered by dependency and impact, with supersession detection
- Blueprint does not prescribe architecture, security practices, data modeling, CI/CD, formatting, or testing methodology
- Terminology: "launch" subagents, "create" teams, "spawn" teammates, "message" within teams

## References

<!-- Agents: add authoritative sources used to make implementation decisions. One line each. -->

- [Claude Code documentation](https://code.claude.com/docs)
