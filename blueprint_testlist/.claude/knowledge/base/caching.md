# Prompt Caching Principles

## Why Caching Matters

Coding agents resend the entire context window on every
turn. Without caching, each turn pays full price for all
prior context. Prompt caching reduces repeated input tokens
to 10% of the base cost. A cache miss on a 100k-token
conversation means paying for 100k tokens at full price
instead of at 10%.

Cache hit rate is the single most important cost and
latency metric for a long-running agent.

## Cache Prefix Order

The API caches content as a cumulative prefix in this
fixed order. Changing anything at level N invalidates
all subsequent levels.

1. System prompt — globally cached across all sessions
2. Tools — globally cached; defined once, never modified
3. Project instructions and memory — cached per project
4. Session state — cached per session
5. Messages — grows each turn, auto-cached with advancing
   breakpoint

## Rules for Cache Stability

### Static content first, dynamic content last

Everything in levels 1 through 4 must be fully static
within a session. Timestamps, counters, file-change
notifications, and any data that varies between turns
must flow through messages (level 5), not through system
prompt or tool modifications.

### Update via messages, not system prompt changes

When information changes mid-session, inject it as a
system-reminder in the next user message or tool result.
Never modify the system prompt, project instructions, or
tool definitions to convey updated information.

### Tool set stability

Tools must be identical at every turn. Never add or
remove tools mid-session. Model state transitions using
tools themselves (like entering or exiting plan mode)
rather than changing the available tool set.

For optional or rarely-used tools, use deferred loading
stubs instead of removing tools entirely.

### One model per conversation

Prompt caches are unique per model. Switching models
mid-conversation forces a full cache rebuild. Delegate
to other models via subagents, which run in separate
conversations with their own caches.

### Keep dynamic injections small

Dynamic content injected per turn should be concise.
Large injections (such as full git status output with
hundreds of untracked files) add cost without caching
benefit. Trim to essential information.

### Fork operations must share the parent prefix

When the context window fills and compaction occurs,
or when a subagent forks, the new request must use
identical system prompt and tool definitions as the
parent conversation. This allows cache hits on the
parent's cached prefix.

## Practical Implications

- Agent files and knowledge files load at session start
  and remain static throughout — do not generate or
  modify them mid-session
- Hooks that need to communicate changing state should
  use message injection, not system prompt modification
- The team shares tool definitions per agent type; do
  not conditionally alter tool sets based on task phase
- Plan mode is a tool-based state transition, not a
  tool-set swap
- When reporting status between agents, use messages;
  do not embed status in system-level configuration
