# Claude Code Terminology

Blueprint files must use Claude Code's official terms for
agent-related operations. When agents read inconsistent
terminology — "spawn a subagent" in one file, "launch an
agent" in another — they may interpret these as distinct
mechanisms or choose the wrong tool. Consistent terms map
directly to specific tools and APIs, removing ambiguity.

## Glossary

### launch (a subagent)

Use when sending work to a subagent via the `Agent` tool
without a `name`. The subagent runs in a separate
conversation, returns a result, and exits. This is the
verb Claude Code's own `Agent` tool description uses.
When agent teams are enabled, a named `Agent` call spawns
a teammate instead — instructions that depend on a
stateless subagent result must say to omit `name`.

> "Launch a subagent to handle the security review."

Do not use: "delegate to a subagent", "start a subagent",
"create a subagent."

### spawn (a teammate)

Use when adding a teammate via the `Agent` tool with a
`name`. The teammate runs as an independent session and
communicates via `SendMessage`. A session has exactly one
team, formed implicitly and cleaned up at session end —
there is no step to create or delete it. Do not write
"create a team" or reference `TeamCreate`/`TeamDelete`:
those tools no longer exist, and agents reading the old
terms look for a setup step that is not there.

> "Spawn the reviewer as a teammate."

Do not use: "create a teammate", "launch a teammate."
"Spawn" is specific to teammates — do not use it for
subagents (those are "launched").

### shut down (a teammate)

Use when ending a teammate's session: message it a
`shutdown_request` via `SendMessage`. The teammate
finishes its current request, then exits — or rejects the
request with an explanation. Shutting down teammates and
spawning replacements is the only way to get fresh
context windows mid-session.

> "Shut down the developer before spawning its replacement."

Do not use: "delete the team", "kill the teammate."

### message

Use when a teammate sends information to another teammate
within the same team via `SendMessage`.

> "Message the reviewer with the implementation summary."

Do not use: "notify" (too vague), "ping" (too informal for
instructions).

### broadcast

Use when a teammate sends the same information to several
teammates. `SendMessage` has no all-teammates address —
a broadcast is one message per recipient, so name every
recipient.

> "Broadcast the updated plan to the developer and the
> reviewer."

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
| Send work to a subagent       | **launch**     | `Agent` tool, no `name` |
| Add a teammate to the team    | **spawn**      | `Agent` tool with `name` |
| End a teammate's session      | **shut down**  | `SendMessage` `shutdown_request` |
| Send a message within a team  | **message**    | `SendMessage`    |
| Send to several teammates     | **broadcast**  | `SendMessage` per recipient |
| Refer to task originator      | **the requester**  | —            |
| Refer to code author          | **the implementor** | —           |
