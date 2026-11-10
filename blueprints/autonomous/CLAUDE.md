# Blueprint v3 — Autonomous

Multi-agent orchestration blueprint for Claude Code.
After clarification and user-approved planning, the lead
feeds tasks to the developer autonomously. The developer
implements and sends to the reviewer for independent
quality review. No user checkpoints gate
individual tasks after plan approval. 4 agents (developer,
reviewer, test-engineer, security-engineer) plus the lead
and two subagents (plan-reviewer, design-advisor).

## Build and Test

```sh
uv run pytest blueprints/autonomous/tests/ -m static -v
```

## Components

| Path | Purpose |
|---|---|
| `.claude/CLAUDE.md` | Lead instructions — clarification, planning, plan queue, task dispatch |
| `.claude/settings.json` | Agent teams config, plans directory path, auto memory off |
| `.claude/agents/developer.md` | Implements all code — source and tests (Sonnet) |
| `.claude/agents/reviewer.md` | Quality gate — scope verification, code review (Opus) |
| `.claude/agents/test-engineer.md` | Advisory — test design on demand (Sonnet) |
| `.claude/agents/security-engineer.md` | Advisory — security assessment on demand (Sonnet) |
| `.claude/agents/plan-reviewer.md` | Plan quality gate — launched as subagent before user presentation (Sonnet) |
| `.claude/agents/design-advisor.md` | Advisory — proposes the change's shape, preparatory refactors, and larger redesigns; launched as subagent while planning (Opus) |
| `.claude/rules/` | Unconditional + conditional rules injected by Claude Code |
| `.claude/skills/ensure-ai-dirs/` | Skill: creates `.ai/plans/` and `.ai/backlog.md`, syncs plan format guide and review checklist, moves Completed/Canceled plans into a frozen `completed/` directory |
| `.claude/skills/project-init/` | Skill: scans project, generates `CLAUDE.md` per `project-context.md`, enables code intelligence plugins for detected languages |
| `.claude/skills/project-sanity/` | Skill: audits repo for common issues (report-only) |
| `tests/blueprint_contracts.py` | Single source of truth for required structure and agent frontmatter |
| `tests/static/` | Structure, caching compliance, agent frontmatter, rule length tests |

## Conventions

<!-- Agents: add non-obvious project conventions discovered during work — things a future agent would need to know to avoid mistakes. One line each. Remove when no longer true. -->

- Agent files define role only — no named teammates, no workflow coordination, no workflow conditionals
- Use "the requester" / "the implementor" in agent files — never role-specific names
- Agent `name:` fields use lowercase hyphenated form: `developer`, `test-engineer`
- Agents set no `tools:` or `disallowedTools:` frontmatter — each inherits the full tool set (a static test checks it); role limits such as read-only, or the reviewer's "edit nothing under review", stand in the agent's text
- A specification the project's References name that defines behavior a task adds, changes, or promises to keep unchanged goes into the plan's Context (the plan-reviewer blocks without it, and the Reviewer checks behavior and tests against it); such behavior triggers the test-engineer, which takes expected outcomes from the specification and cites the clause, and a known deviation the plan keeps is a Decisions entry
- Unconditional rules (no `paths:` frontmatter): `acceptance-criteria.md`, `advisor-gate-independence.md`, `claim-verification.md`, `code-navigation.md`, `communication-hygiene.md`, `instruction-feedback.md`, `introduced-defects.md`, `no-silent-target-weakening.md`, `procedural-fidelity.md`, `risk-assessment.md`, `root-cause-discipline.md`, `safe-git.md`, `simplicity.md`, `verify-external-identifiers.md`, `waiting-on-commands.md`
- Conditional rules load automatically when agents touch matching file extensions
- Universal principles stated once in unconditional rules — language rules extend without restating
- Adding a new language: create `lang-<language>.md` with `paths:` frontmatter, update `functional-style.md`/`code-mass.md`/`code-principles.md` paths — no changes to CLAUDE.md or agents
- Lead-directed advisor consultation — lead assesses risk at dispatch time per `risk-assessment.md`
- Advisor consultation requires two gates in the dispatch message: input gate (consult before implementing) and output gate (get sign-off before submitting to reviewer)
- Developer may add advisor consultations but not remove lead's directives
- Lead owns plan progress — marks tasks done, commits code with plan updates in a single commit per task
- Developer makes WIP commits during implementation — lead squashes at commit time via `git reset <baseline-sha>`
- Lead's ad-hoc commits happen only in team-down windows — mid-task commits land in the squash reset range and are lost
- Reviewer backstop: rejects if non-trivial behavioral changes lack tests and no advisor was consulted, and if Context names a specification for the task's behavior and no test-engineer signed off
- Infeasibility claims require specific evidence (file, function, scope, own code vs dependency) per `claim-verification.md` — category labels are not sufficient
- The design-advisor is a stateless subagent; every code-changing plan rests on its report, and before the plan is written the user decides its Shape proposals together as one design and every other proposal on its own
- The lead collects its questions and asks them in one round once research and the design-advisor report are done: an overview first, then one question per dialog, each with a concrete example of what every option does (lead `Asking the User`)
- An adopted preparatory refactor is its own task ahead of the feature work; when no test covers the behavior it preserves, a preceding task pins that behavior with tests
- Duplication the change must edit in several places is removed before it (design-advisor: `do first` or `separate plan before`); a separate plan before is completed first and the change then gets a fresh design-advisor report, one after goes into the plan's Non-Goals as `(separate plan after this one)` and is offered at completion
- Plans are reviewed by Sonnet subagents before user presentation — three in parallel on the first pass, one per checklist focus (`scope`, `criteria`, `impact`), then single follow-up passes on the diff of each revision until a pass reports no blocking issues
- Plan review checklist and format guide are synced to the plans directory by `/ensure-ai-dirs`
- Plan-format.md contains `<!-- agent: -->` comments as authoring hints for the lead
- Plans are committed only after user approval, not before; several plans from one request are approved one at a time, and approval covers the whole plan through closure
- Lead verifies plan goal at completion — adds follow-up tasks if quantitative targets not met
- Auto memory is off (`autoMemoryEnabled: false`); `instruction-feedback.md` says where each kind of knowledge goes, and open findings go into `.ai/backlog.md`, created by `/ensure-ai-dirs` and owned by the lead
- A defect the task itself introduces blocks the reviewer and the security engineer at every severity: it is fixed in the task or the user accepts it, and only an accepted one goes into `.ai/backlog.md` (`introduced-defects.md`); a defect counts as pre-existing only with the baseline check that shows it
- After approval a plan changes only through Task Notes (how an open task is implemented safely), a revision with a follow-up review and new approval (open tasks only, the Goal stands or gains something), a gate's demand on the running task (criteria adapted, Decisions entry, no new approval), or cancellation with the reason in Decisions (Goal no longer holds); a rebase that invalidates a checked task's text is the only reason to correct it
- The plan file is created uncommitted at the user's first decision in planning; an untracked plan is not approved, and resuming starts from `git status` with fresh gates
- The reviewer's follow-up pass after a rejection, or after a change to its approved state, reviews only the diff between the recorded tree of its last pass and the resubmission; build and tests run only when a change can affect them, never for prose alone
- Every review verdict names the tree recorded before the review started (`approved state` / `reviewed state`); before the commit the lead stages the approved files and checks them against it (`git diff --cached`), and an unseen change goes back for a follow-up pass
- Teammates run builds and tests in the foreground (`waiting-on-commands.md`): the end of a teammate's background command does not wake it while it is idle (a Claude Code bug), and the lead treats a teammate waiting on its own background command as a stall
- Files under `.claude/` never name their origin — projects know nothing of the template they came from
- All blueprint files must be fully static — no dates, counters, versions (prompt cache level 3)
- Rule files target under 200 lines — agent adherence degrades beyond that threshold
- Skills run before teammates are spawned — lead commits skill outputs directly per skill-output commit rule
- Templates live in their skill's directory, not a separate `templates/` directory
- Generated project `CLAUDE.md` follows `project-context.md`: Overview, Build and Test, Components, Conventions, References
- On `CLAUDE.md` re-generation: Overview/Build/Components refresh; Conventions/References entries preserve
- Execution pipeline: Lead → Developer → Reviewer → Lead (developer-reviewer rejection loop is opaque to lead)
- Teammates are cycled (shut down + re-spawn) between task slices — prevents developer context degradation across tasks
- Plan queue supports multiple concurrent plans — ordered by dependency and impact, with supersession detection
- Blueprint does not prescribe architecture, security practices, data modeling, CI/CD, formatting, or testing methodology
- Terminology: "launch" subagents, "spawn" and "shut down" teammates, "message" within teams

## References

<!-- Agents: add authoritative sources used to make implementation decisions. One line each. -->

- [Claude Code documentation](https://code.claude.com/docs)
