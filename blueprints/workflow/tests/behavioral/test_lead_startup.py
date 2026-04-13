"""Behavioral tests verifying the lead clarifies before implementing.

The Clarification section in .claude/CLAUDE.md instructs the lead to
check for project context, check for existing plans, and clarify with
the user before proposing a workflow.

These tests verify that the lead reads context and clarifies with the
user instead of jumping to implementation.
"""

import pytest

from claude_agent_sdk import ClaudeAgentOptions, query
from claude_agent_sdk.types import AssistantMessage, ToolUseBlock

from behavioral.conftest import NESTED_SESSION_ENV, ToolCallLog

pytestmark = pytest.mark.behavioral


@pytest.fixture
def tool_log():
    return ToolCallLog()


@pytest.mark.asyncio
@pytest.mark.timeout(180)
async def test_lead_follows_startup_sequence(fixture_project, tool_log):
    """The lead should clarify before jumping to implementation.

    The Clarification section requires the lead to check for project
    context and clarify with the user before any implementation. This
    test verifies the lead uses read tools or AskUserQuestion in its
    first actions — not implementation tools.

    We check that within the first few tool calls, the lead either:
    - Reads files to understand context (Read, Glob, Grep)
    - Uses Bash for information gathering (git status, ls, etc.)
    - Asks the user for clarification (AskUserQuestion)
    - Spawns agents if needed (Agent tool)

    And does NOT:
    - Jump straight to writing code (Write, Edit)
    """
    options = ClaudeAgentOptions(
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
    assert tool_log.records, "Lead should have used tools before implementing"

    # Only Write and Edit are implementation tools. Bash is dual-purpose
    # (information gathering vs. implementation) and is legitimate for
    # checking git status, running tests, etc.
    implementation_tools = {"Write", "Edit"}

    first_tools = [r.tool_name for r in tool_log.records[:5]]
    premature_impl = [t for t in first_tools if t in implementation_tools]

    assert not premature_impl, (
        f"Lead jumped to implementation instead of clarifying: "
        f"{premature_impl}. First 5 tools: {first_tools}"
    )

    # At least one clarification-appropriate tool should be present
    clarify_tools = {"Read", "Glob", "Grep", "Bash", "Agent", "AskUserQuestion"}
    clarify_used = [t for t in first_tools if t in clarify_tools]
    assert clarify_used, (
        f"Lead did not use any clarification-appropriate tools in its "
        f"first actions. First 5 tools: {first_tools}"
    )
