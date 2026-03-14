# Claude Code Terminology

Blueprint files must use Claude Code's official terms for
agent-related operations. When agents read inconsistent
terminology — "spawn a subagent" in one file, "launch an
agent" in another — they may interpret these as distinct
mechanisms or choose the wrong tool. Consistent terms map
directly to specific tools and APIs, removing ambiguity.

## Glossary

### launch (a subagent)

Use when sending work to a subagent via the `Agent` tool.
The subagent runs in a separate conversation, returns a
result, and exits. This is the verb Claude Code's own
`Agent` tool description uses.

> "Launch a subagent to handle the security review."

Do not use: "delegate to a subagent", "start a subagent",
"create a subagent."

### create (a team)

Use when forming a new agent team via `TeamCreate`. This
sets up the team structure and spawns the initial members.

> "Create a team for the development workflow."

Do not use: "start a team", "spin up a team."

### spawn (a teammate)

Use when adding a member to an existing team. Spawning
places an agent into a team where it runs as an independent
session and communicates via `SendMessage`. This is the
verb Claude Code uses in its agent infrastructure.

> "Spawn the reviewer as a teammate."

Do not use: "create a teammate", "launch a teammate."
"Spawn" is specific to teammates — do not use it for
subagents (those are "launched").

### message

Use when a teammate sends information to another teammate
within the same team via `SendMessage`.

> "Message the reviewer with the implementation summary."

Do not use: "notify" (too vague), "ping" (too informal for
instructions).

### broadcast

Use when a teammate sends information to all other
teammates in the team.

> "Broadcast the updated plan to the team."

### the requester / the implementor

Use these role-neutral references in agent files instead of
naming specific teammates. Agent files define capability,
not team structure — naming teammates couples the agent to
a specific workflow composition.

- **the requester** — whoever initiated the agent's current
  task
- **the implementor** — whoever produced the work being
  reviewed

> "Send findings to the requester."

Do not use: "send to the Developer", "notify the
Architect." These belong in workflow files only.

## Where This Applies

- Agent definition files (`agents/*.md`)
- Workflow files (`workflows/*.md`)
- CLAUDE.md files (lead instructions)
- Skill files (`skills/*/SKILL.md`)
- Knowledge and practice files

## Quick Reference

| Action                        | Correct term   | Tool / mechanism |
|-------------------------------|----------------|------------------|
| Send work to a subagent       | **launch**     | `Agent` tool     |
| Form a new team               | **create**     | `TeamCreate`     |
| Add a member to a team        | **spawn**      | `TeamCreate`     |
| Send a message within a team  | **message**    | `SendMessage`    |
| Send to all teammates         | **broadcast**  | `SendMessage`    |
| Refer to task originator      | **the requester**  | —            |
| Refer to code author          | **the implementor** | —           |
