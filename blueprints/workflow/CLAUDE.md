# Blueprint v2 — Workflow

Multi-agent orchestration blueprint for Claude Code.
Clarify-first: the lead clarifies the task, writes a plan
(reviewed by the plan-reviewer subagent and approved by
the user), then presents workflow options. The user
chooses: Direct-Review for simple tasks, Develop-Review
(Supervised or Autonomous) for complex ones, or TDD
User-in-the-Loop. 4 agents (developer, reviewer,
test-engineer, security-engineer) plus the lead.

## Build and Test

```sh
uv run pytest blueprints/workflow/tests/ -m static -v
```

## Components

| Path | Purpose |
|---|---|
| `.claude/CLAUDE.md` | Lead instructions — clarification, planning, workflow proposal, agent coordination |
| `.claude/settings.json` | Agent teams config, plans and memory directory paths |
| `.claude/agents/developer.md` | Implements all code — source and tests (Sonnet) |
| `.claude/agents/reviewer.md` | Quality gate — scope verification, commits approved work (Opus) |
| `.claude/agents/test-engineer.md` | Advisory — test design and verification (Sonnet) |
| `.claude/agents/plan-reviewer.md` | Plan quality gate — launched as subagent before user presentation (Sonnet) |
| `.claude/agents/security-engineer.md` | Advisory — security assessment (Sonnet) |
| `.claude/agents/test-list.md` | Subagent — converts an example mapping into a minimum-required test list (Sonnet) |
| `.claude/rules/` | Unconditional + conditional rules injected by Claude Code |
| `.claude/skills/ensure-ai-dirs/` | Skill: creates `.ai/plans/` and `.ai/memory/` directories, syncs plan format guide and review checklist, archives plans older than 14 days |
| `.claude/skills/example-mapping/` | Skill: facilitates an Example Mapping session and writes a structured mapping file for `/test-list` or clarification |
| `.claude/skills/project-init/` | Skill: scans project, generates `CLAUDE.md` per `project-context.md` |
| `.claude/skills/project-sanity/` | Skill: audits repo for common issues (report-only) |
| `.claude/skills/test-list/` | Skill: TDD entry path — invokes the test-list subagent and embeds the confirmed list in the plan |
| `.claude/skills/project-init/project-context.md` | Output format for generated project `CLAUDE.md` |
| `.claude/workflows/` | Workflow definitions — one file per workflow variant |
| `tests/blueprint_contracts.py` | Single source of truth for required structure and agent frontmatter |
| `tests/static/` | Structure, caching compliance, agent frontmatter, rule length tests |

## Conventions

<!-- Agents: add non-obvious project conventions discovered during work — things a future agent would need to know to avoid mistakes. One line each. Remove when no longer true. -->

- Agent files define role only — no named teammates, no workflow coordination, no workflow conditionals
- Use "the requester" / "the implementor" in agent files — never role-specific names
- Agent `name:` fields use lowercase hyphenated form: `developer`, `test-engineer`
- Workflow files define team composition, coordination sequences, and sign-off requirements
- Adding a new workflow: create a file in `.claude/workflows/` — no changes to CLAUDE.md, agents, or rules
- Unconditional rules (no `paths:` frontmatter): `acceptance-criteria.md`, `advisor-gate-independence.md`, `claim-verification.md`, `no-silent-target-weakening.md`, `procedural-fidelity.md`, `risk-assessment.md`, `root-cause-discipline.md`, `simplicity.md`
- Conditional rules load automatically when agents touch matching file extensions
- Universal principles stated once in unconditional rules — language rules extend without restating
- Adding a new language: create `lang-<language>.md` with `paths:` frontmatter, update `functional-style.md`/`code-mass.md`/`code-principles.md` paths — no changes to CLAUDE.md, agents, or workflows
- Risk assessment at workflow selection: high-risk indicators require Develop-Review, not Direct-Review
- Lead does not prescribe security mitigations — names risk categories and routes to Security Engineer
- All blueprint files must be fully static — no dates, counters, versions (prompt cache level 3)
- Rule files target under 200 lines — agent adherence degrades beyond that threshold
- Templates live in their skill's directory, not a separate `templates/` directory
- Generated project `CLAUDE.md` follows `project-context.md`: Overview, Build and Test, Components, Conventions, References
- On `CLAUDE.md` re-generation: Overview/Build/Components refresh; Conventions/References entries preserve
- Blueprint does not prescribe architecture, security practices, data modeling, CI/CD, formatting, or testing methodology
- Terminology: "launch" subagents, "create" teams, "spawn" teammates, "message" within teams

## References

<!-- Agents: add authoritative sources used to make implementation decisions. One line each. -->

- [Claude Code documentation](https://code.claude.com/docs)
