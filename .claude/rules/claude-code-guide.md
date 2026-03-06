# Claude Code Questions — Use the Built-in Guide

When the user asks questions about Claude Code (the CLI
tool), the Claude Agent SDK, or the Claude API, delegate to
the built-in `claude-code-guide` subagent via the Agent tool
(`subagent_type: "claude-code-guide"`). The guide has access
to up-to-date Claude Code documentation and can answer
feature, configuration, and usage questions more accurately
than reasoning from memory alone.

Also consult the official documentation at
https://code.claude.com/docs when additional context is
needed.

## When to Delegate

Trigger the guide for questions like:

- "Can Claude Code…", "Does Claude Code…", "How do I…"
- Features: hooks, slash commands, MCP servers, settings,
  IDE integrations, keyboard shortcuts, subagents, skills,
  plugins, agent teams
- Claude Agent SDK: building custom agents, headless mode,
  programmatic usage
- Claude API / Anthropic SDK: API usage, tool use, SDK
  integration

## When NOT to Delegate

- The user is asking about this repository's blueprints or
  orchestration design — that is project-specific knowledge,
  not a Claude Code question
- The question is about general programming, AI/ML, or
  topics unrelated to Claude Code tooling

## Why This Rule Exists

The `claude-code-guide` subagent runs on Haiku with access
to Claude Code's documentation corpus. Answering from stale
or incomplete memory risks giving outdated or incorrect
guidance. Delegating ensures the user gets accurate,
documentation-backed answers while keeping the main context
window focused on implementation work.
