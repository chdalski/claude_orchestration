"""Behavioral tests verifying tool access contracts at runtime.

These tests spawn real Claude Code sessions and track tool usage
via the message stream (ToolUseBlock in AssistantMessages).
"""

from pathlib import Path

import pytest

from claude_code_sdk import ClaudeCodeOptions, query
from claude_code_sdk.types import AssistantMessage, ToolUseBlock

from behavioral.conftest import NESTED_SESSION_ENV, ToolCallLog

pytestmark = pytest.mark.behavioral

# Override the lead's CLAUDE.md "delegate to specialized agents" instruction
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
async def test_reviewer_does_not_commit_unprompted(fixture_project, tool_log):
    """Reviewer reads and assesses code but never runs git commit without a signal."""
    options = ClaudeCodeOptions(
        cwd=str(fixture_project),
        max_turns=3,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
        append_system_prompt=DIRECT_MODE,
    )

    prompt = (
        "Read src/lib.py and assess the code quality. "
        "List any issues you find. Do NOT commit anything. Be brief."
    )

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    tool_log.record(block.name, block.input or {})

    bash_calls = tool_log.calls_for("Bash")
    commit_attempts = [
        r for r in bash_calls if "git commit" in r.input_data.get("command", "")
    ]
    assert not commit_attempts, (
        f"Reviewer attempted git commit: {commit_attempts}"
    )


@pytest.mark.asyncio
@pytest.mark.timeout(90)
async def test_advisory_te_denied_write(fixture_project, tool_log):
    """Test Engineer should use Read but not Write/Edit (advisory role)."""
    prompt = (
        "Read src/lib.py and describe what tests you would write "
        "for the add function. Do not write any files. Be brief."
    )
    await _run_agent_session(fixture_project, prompt, tool_log)

    assert tool_log.has("Read"), "Test Engineer should have read source files"
    assert not tool_log.has("Write"), "Advisory agent should not attempt Write"
    assert not tool_log.has("Edit"), "Advisory agent should not attempt Edit"


@pytest.mark.asyncio
@pytest.mark.timeout(90)
async def test_advisory_se_denied_write(fixture_project, tool_log):
    """Security Engineer should use Read but not Write/Edit (advisory role)."""
    prompt = (
        "Read src/lib.py and assess the security of the add function. "
        "Report any security concerns. Do not write any files. Be brief."
    )
    await _run_agent_session(fixture_project, prompt, tool_log)

    assert tool_log.has("Read"), "Security Engineer should have read source files"
    assert not tool_log.has("Write"), "Advisory agent should not attempt Write"
    assert not tool_log.has("Edit"), "Advisory agent should not attempt Edit"
