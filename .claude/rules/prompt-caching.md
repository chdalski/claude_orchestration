# Prompt Caching Rules for Blueprint Design

Every blueprint in this repository must align with Claude
Code's prompt caching architecture. Caching dominates cost
and latency — a cache miss means paying full price for the
entire context window on every turn.

## Cache Prefix Order (immutable)

The API caches content as a cumulative prefix in this fixed
order. Changing anything at level N invalidates levels N+1
and beyond.

1. **System prompt** — globally cached across all sessions
2. **Tools** — globally cached; defined once, never modified
3. **CLAUDE.md & Memory** — cached per project
4. **Session state** (env, MCP, output style) — cached per
   session
5. **Messages** (user messages, tool results) — grows each
   turn, auto-cached with advancing breakpoint

## Six Rules

### 1. Static before dynamic

All content in levels 1–4 must be fully static. No
timestamps, counters, git status, or any data that changes
between turns.

### 2. Dynamic updates via messages only

When information changes mid-session (time, file state,
status), inject it as a `<system-reminder>` in the next user
message or tool result. Never modify the system prompt or
CLAUDE.md content mid-session.

### 3. Tool set stability

Tools must be identical at every turn of the conversation.
Never add or remove tools mid-session. Use state-transition
tools (like EnterPlanMode/ExitPlanMode) instead of swapping
tool sets. For optional tools, use `defer_loading: true`
stubs discovered via ToolSearch.

### 4. No model switches mid-session

Prompt caches are unique per model. Switching models
mid-conversation rebuilds the entire cache. Use subagents
(separate conversations) for model delegation.

### 5. Dynamic content size

Keep injected dynamic content small per turn:
- < 2,000 characters — good
- 2,000–10,000 characters — acceptable, watch cost
- \> 10,000 characters — must be trimmed

### 6. Fork safety (compaction & subagents)

When context compaction occurs or subagents fork, the new
request must use the identical system prompt and tool
definitions as the parent conversation to get cache hits on
the parent's prefix.

## Implications for Blueprint Design

- Agent instructions load via CLAUDE.md and agent files
  (level 3) — keep them static
- Knowledge and practices are read at session start via
  hooks — content must not change mid-session
- SessionStart hooks inject context into messages (level 5),
  which is correct
- Hooks that modify system prompt or tools violate caching
- All agents in a team share the same tool definitions per
  their agent type — do not conditionally alter tool sets
- Plan mode uses tools (EnterPlanMode/ExitPlanMode), not
  tool-set swaps
