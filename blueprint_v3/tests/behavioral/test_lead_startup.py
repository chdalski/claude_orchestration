"""Behavioral tests verifying the lead follows its startup procedure.

The startup sequence is defined in .claude/CLAUDE.md and instructs the
lead to check for project context, check for existing plans, and clarify
with the user before implementing.

These tests verify observable startup behavior:
1. The lead follows the startup sequence (reads context, clarifies with
   user) instead of jumping to implementation
"""

import pytest

from claude_code_sdk import ClaudeCodeOptions, query
from claude_code_sdk.types import AssistantMessage, ToolUseBlock

from behavioral.conftest import NESTED_SESSION_ENV, ToolCallLog

pytestmark = pytest.mark.behavioral


@pytest.fixture
def tool_log():
    return ToolCallLog()


@pytest.mark.asyncio
@pytest.mark.timeout(180)
async def test_lead_follows_startup_sequence(fixture_project, tool_log):
    """The lead should follow the startup sequence instead of jumping to work.

    The startup sequence requires the lead to check for project context
    and clarify with the user before any implementation. This test
    verifies the lead uses read tools or AskUserQuestion in its first
    actions — not implementation tools.

    We check that within the first few tool calls, the lead either:
    - Reads files to understand context (Read, Glob, Grep)
    - Asks the user for clarification (AskUserQuestion)
    - Spawns agents if needed (Agent tool)

    And does NOT:
    - Jump straight to writing code (Write, Edit)
    - Run commands (Bash)
    """
    options = ClaudeCodeOptions(
        cwd=str(fixture_project),
        max_turns=5,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
    )

    prompt = (
        "I want to add a hello world function to this project."
    )

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    tool_log.record(block.name, block.input or {})

    # The lead should have used at least one tool
    assert tool_log.records, "Lead should have used tools during startup"

    # Acceptable first actions: reading, exploring, spawning agents, asking user
    implementation_tools = {"Write", "Edit", "Bash"}

    first_tools = [r.tool_name for r in tool_log.records[:5]]
    premature_impl = [t for t in first_tools if t in implementation_tools]

    assert not premature_impl, (
        f"Lead jumped to implementation instead of following startup: "
        f"{premature_impl}. First 5 tools: {first_tools}"
    )

    # At least one startup-appropriate tool should be present
    startup_tools = {"Read", "Glob", "Grep", "Agent", "AskUserQuestion"}
    startup_used = [t for t in first_tools if t in startup_tools]
    assert startup_used, (
        f"Lead did not use any startup-appropriate tools in its first "
        f"actions. First 5 tools: {first_tools}"
    )
