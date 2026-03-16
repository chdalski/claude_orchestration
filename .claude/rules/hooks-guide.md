# Hooks — When and How to Use Them

Hooks are shell commands that Claude Code executes in
response to lifecycle events. They inject context, validate
actions, or perform side effects. Use them when static
files (rules, CLAUDE.md) are insufficient — typically
because the guidance must react to runtime events, validate
tool usage, or perform side effects like logging.

## When to Use a Hook vs. a Rule

| Need | Mechanism | Why |
|---|---|---|
| Static guidance (always in context) | Rule file (`.claude/rules/`) | Loaded at cache level 3, survives compaction intact |
| Dynamic context injection | **Hook** (SessionStart) | Inject runtime state (git status, env info) as messages |
| Validation before a tool executes | **Hook** (PreToolUse) | Can block or modify the action |
| Side effects after a tool executes | **Hook** (PostToolUse) | Logging, linting, notifications |
| Per-agent constraints | **Hook** (agent frontmatter) | Scoped to that agent's lifetime |

**Rules survive compaction.** Compaction summarizes the
message history (level 5), not the system instructions
(levels 1-4). Rules are level 3 — they are re-sent in
full on every API call, before and after compaction. Use
rules for guidance that must always be present. Use hooks
for runtime actions (validation, side effects, dynamic
context injection).

## Key Hook Events

### SessionStart

Fires when a session begins or resumes. Supports four
matchers:

- `"startup"` — new session
- `"resume"` — `--resume`, `--continue`, or `/resume`
- `"clear"` — after `/clear`
- `"compact"` — after auto or manual compaction

Content printed to stdout becomes context the agent sees
immediately. Useful for injecting dynamic runtime state
(current branch, environment info) at session transitions.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "cat .claude/reminders/example.txt"
          }
        ]
      }
    ]
  }
}
```

Multiple matchers can be combined — use separate entries
in the array for different matchers.

### PreToolUse

Fires before a tool executes. The matcher matches against
the tool name (e.g., `"Bash"`, `"Edit|Write"`). Can
**block** the action (exit code 2 with stderr message) or
**allow** it (exit code 0).

### PostToolUse

Fires after a tool succeeds. Same matcher syntax as
PreToolUse. Can inject additional context via JSON output.
Useful for linting after edits or logging after commands.

### PostCompact

Fires after compaction completes. Supports matchers
`"manual"` and `"auto"`. **Observability only** — cannot
inject content into the conversation. Use for logging or
cleanup, not for reminders. For post-compaction content
injection, use SessionStart with the `compact` matcher
instead.

## Content Injection

Two methods for hooks that support injection:

**Plain text (stdout):**
```bash
echo "Reminder: always execute every step in a procedure."
exit 0
```

**Structured JSON (stdout):**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Reminder text here."
  }
}
```

Use one approach per hook — not both. Keep injected
content under 2,000 characters to stay within prompt
caching guidelines (see `prompt-caching.md` rule 5).

## Configuration Locations

Hooks can be defined at four scopes (highest priority
first):

1. **`.claude/settings.local.json`** — project-local,
   not version-controlled. Use for personal overrides.
2. **`.claude/settings.json`** — project-level, shared
   via git. Use for team-wide hooks.
3. **`~/.claude/settings.json`** — user-level, all
   projects. Use for personal cross-project hooks.
4. **Managed policy** — organization-enforced.

### Agent Frontmatter Hooks

Hooks can be defined in subagent definition files
(`.claude/agents/*.md`) via YAML frontmatter:

```yaml
---
name: developer
description: Implements all code
tools: [Read, Write, Edit, Bash]
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh"
---
```

These hooks run **only while that subagent is active**
and are cleaned up when it finishes. Confirmed for
subagents launched via the Agent tool. Whether they work
for team members created via TeamCreate is unverified —
test before relying on this for team-based blueprints.

## Blueprint Design Implications

- Hook definitions in `settings.json` are static (cache
  level 2) — do not generate them dynamically.
- Reminder files read by hooks (e.g.,
  `.claude/reminders/*.txt`) are not cached — they are
  read at hook execution time, so updates take effect
  immediately.
- Hooks that inject content add to the message stream
  (level 5), which is the correct place for dynamic
  content per prompt caching rules.
- For static guidance, prefer rule files over hooks —
  rules are level 3 (always present, survive compaction).
  Hooks are for runtime actions, not static instructions.
- PostCompact is observability-only — it cannot inject
  content. Use SessionStart with the `compact` matcher
  if you need to inject dynamic context after compaction.
