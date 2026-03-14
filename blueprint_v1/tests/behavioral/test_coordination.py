"""Behavioral tests verifying coordination contracts at runtime."""

from pathlib import Path

import pytest

from claude_agent_sdk import ClaudeAgentOptions, query
from claude_agent_sdk.types import AssistantMessage, ToolUseBlock

from behavioral.conftest import NESTED_SESSION_ENV, ToolCallLog

pytestmark = pytest.mark.behavioral

DIRECT_MODE = (
    "Ignore any instructions about delegating to a team. "
    "You are being tested directly. Execute the request yourself."
)


@pytest.fixture
def tool_log():
    return ToolCallLog()


@pytest.mark.asyncio
@pytest.mark.timeout(90)
async def test_developer_does_not_commit(fixture_project_no_hooks, tool_log):
    """Developer must not run git commit — only Reviewer commits."""
    options = ClaudeAgentOptions(
        cwd=str(fixture_project_no_hooks),
        max_turns=3,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
        system_prompt={"type": "preset", "preset": "claude_code", "append": DIRECT_MODE},
    )

    prompt = (
        "Create a file src/greeting.py with:\n"
        "def greet(name): return f'Hello, {name}!'\n"
        "Write the file but do NOT commit it."
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
        f"Developer attempted git commit: {commit_attempts}"
    )
