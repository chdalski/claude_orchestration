# Plan Format

Every plan file in this directory must follow this
structure. Plans are living documents — update them as
work progresses. This consistency ensures any agent or
user can pick up a plan mid-session and understand its
state without guessing.

## Required Sections

### Goal

What was requested and why. One to three sentences that
capture the intent, not just the action — an agent that
understands intent can make better decisions when
unexpected situations arise.

Bad: "Add a login page."
Good: "Users need to authenticate before accessing the
dashboard. Add a login page with email/password that
integrates with the existing auth service."

### Context

Relevant background that someone picking up this plan
would need. Without context, a new agent or user will
repeat investigation work or make decisions that
contradict earlier ones.

- Constraints or requirements from the user
- Related prior decisions or plans
- Key files, modules, or systems involved
- Anything that narrows the solution space

### Steps

A checklist of concrete steps. Use `- [ ]` for pending
and `- [x]` for completed — checkboxes make progress
visible at a glance and prevent re-doing finished work
when a session resumes.

```markdown
- [x] Clarify requirements with user
- [x] Review existing auth service
- [ ] Implement login form component
- [ ] Add route and navigation
- [ ] Write tests
```

Keep steps granular enough to track progress but not so
fine-grained that the list becomes noise — a 50-item
checklist obscures status rather than revealing it.

### Decisions

Key choices made during planning or execution, with brief
reasoning. Recording the "why" prevents future agents
from revisiting settled decisions or unknowingly
contradicting them.

```markdown
- **Auth method:** JWT tokens (user preference, aligns
  with existing API)
- **Form library:** None — plain HTML form is sufficient
  for two fields
```

Only record decisions that someone resuming this plan
would need to know. Skip obvious ones — documenting every
micro-decision adds noise that makes important decisions
harder to find.

### Status

Current state of the plan. One of:

- **In Progress** — actively being worked on
- **Paused** — work stopped, can be resumed
- **Completed** — all steps done
- **Abandoned** — superseded or no longer needed

A clear status lets the lead's startup check quickly
identify which plans need attention without reading every
step.

## Conventions

- Use plain markdown. No frontmatter — plans are runtime
  artifacts, not agent configuration, so frontmatter
  parsing adds complexity with no benefit.
- File names should be descriptive:
  `add-user-authentication.md`, not `plan-001.md` —
  descriptive names let the lead scan the directory and
  present plans to the user without opening each file.
- One plan per task or feature. Don't combine unrelated
  work into a single plan — mixed plans make progress
  tracking ambiguous and complicate resumption.
- Update the status and checkboxes as work progresses —
  stale plans mislead the next session into repeating or
  skipping work.
- Plans are committed to git alongside the code they
  describe — this ties decisions to the code that
  implemented them, making future archaeology easier.
