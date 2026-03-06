"""Behavioral tests verifying tool access contracts at runtime.

These tests spawn real Claude Code sessions and track tool usage
via the message stream (ToolUseBlock in AssistantMessages).
Uses fixture_project_no_hooks to avoid the startup checklist
consuming all turns.
"""

from pathlib import Path

import pytest

from claude_code_sdk import ClaudeCodeOptions, query
from claude_code_sdk.types import AssistantMessage, ToolUseBlock

from behavioral.conftest import NESTED_SESSION_ENV, ToolCallLog

pytestmark = pytest.mark.behavioral

# Override the lead's CLAUDE.md "never implement" instruction
DIRECT_MODE = (
    "Ignore any instructions about delegating to a team. "
    "You are being tested directly. Execute the request yourself."
)


@pytest.fixture
def tool_log():
    return ToolCallLog()


async def _run_agent_session(
    project_path: Path,
    prompt: str,
    tool_log: ToolCallLog,
) -> None:
    """Run a Claude Code session, logging tool calls from the message stream."""
    options = ClaudeCodeOptions(
        cwd=str(project_path),
        max_turns=3,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
        append_system_prompt=DIRECT_MODE,
    )

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    tool_log.record(block.name, block.input or {})


@pytest.mark.asyncio
@pytest.mark.timeout(90)
async def test_advisory_agent_denied_write(fixture_project_no_hooks, tool_log):
    """Test Engineer should use Read but not Write/Edit."""
    prompt = (
        "Read src/lib.py and describe what tests you would write "
        "for the add function. Do not write any files. Be brief."
    )
    await _run_agent_session(fixture_project_no_hooks, prompt, tool_log)

    assert tool_log.has("Read"), "Agent should have read source files"
    assert not tool_log.has("Write"), "Advisory agent should not attempt Write"
    assert not tool_log.has("Edit"), "Advisory agent should not attempt Edit"


@pytest.mark.asyncio
@pytest.mark.timeout(90)
async def test_developer_can_write(fixture_project_no_hooks, tool_log):
    """Developer should be able to use Write tool."""
    prompt = (
        "Create a file called src/greeting.py with this exact content:\n"
        "def greet(name): return f'Hello, {name}!'\n"
        "Only create this one file."
    )
    await _run_agent_session(fixture_project_no_hooks, prompt, tool_log)

    assert tool_log.has("Write") or tool_log.has("Edit"), (
        "Developer should have used Write or Edit"
    )


    # NOTE: test_architect_can_create_tasks was removed because TaskCreate
    # is a team-only tool that requires a running team context. Testing it
    # in isolation would require a full team setup (~$5-20 per run).
    # The static tests in test_agent_frontmatter.py verify the Architect's
    # tool list includes TaskCreate.
