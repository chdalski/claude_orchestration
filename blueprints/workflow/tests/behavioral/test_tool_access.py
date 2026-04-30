"""Behavioral tests verifying tool access contracts at runtime.

These tests spawn real Claude Code sessions and track tool usage
via the message stream (ToolUseBlock in AssistantMessages).
The blueprint has no hooks in settings.json, so all tests use
fixture_project directly (no hook-stripping needed).
"""

from pathlib import Path

import pytest

from claude_agent_sdk import ClaudeAgentOptions, query
from claude_agent_sdk.types import AssistantMessage, ToolUseBlock

from behavioral.conftest import NESTED_SESSION_ENV, ToolCallLog

pytestmark = pytest.mark.behavioral

# Override the lead's CLAUDE.md "route work to specialized agents" posture
DIRECT_MODE = (
    "Ignore any instructions about routing work to a team. "
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
    options = ClaudeAgentOptions(
        cwd=str(project_path),
        max_turns=3,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
        system_prompt={"type": "preset", "preset": "claude_code", "append": DIRECT_MODE},
    )

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    tool_log.record(block.name, block.input or {})


@pytest.mark.asyncio
@pytest.mark.timeout(90)
async def test_developer_can_write(fixture_project, tool_log):
    """Developer should be able to use Write or Edit tool."""
    prompt = (
        "Create a file called src/greeting.py with this exact content:\n"
        "def greet(name): return f'Hello, {name}!'\n"
        "Only create this one file."
    )
    await _run_agent_session(fixture_project, prompt, tool_log)

    assert tool_log.has("Write") or tool_log.has("Edit"), (
        "Developer should have used Write or Edit"
    )


@pytest.mark.asyncio
@pytest.mark.timeout(90)
async def test_reviewer_does_not_commit(fixture_project, tool_log):
    """Reviewer reads and assesses code but never runs git commit.

    The reviewer composes the proposed commit message and returns
    the file list; the lead executes the commit after the user
    checkpoint (or immediately, in Develop-Review Autonomous).
    """
    options = ClaudeAgentOptions(
        cwd=str(fixture_project),
        max_turns=3,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
        system_prompt={"type": "preset", "preset": "claude_code", "append": DIRECT_MODE},
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
