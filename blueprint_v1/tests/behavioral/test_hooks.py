"""Behavioral tests verifying hook behavior at runtime."""

import pytest

from claude_agent_sdk import ClaudeAgentOptions, query
from claude_agent_sdk.types import AssistantMessage, TextBlock

from behavioral.conftest import NESTED_SESSION_ENV

pytestmark = pytest.mark.behavioral


@pytest.mark.asyncio
@pytest.mark.timeout(90)
async def test_session_start_hook_fires(fixture_project):
    """SessionStart hook should fire and agent should acknowledge the checklist."""
    options = ClaudeAgentOptions(
        cwd=str(fixture_project),
        max_turns=3,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
    )

    responses: list[str] = []
    async for message in query(
        prompt="Acknowledge the startup checklist and list what you need to read.",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    responses.append(block.text)

    combined = " ".join(responses).lower()
    assert any(
        keyword in combined
        for keyword in ["checklist", "startup", "claude.md", "knowledge"]
    ), (
        f"Agent should acknowledge startup checklist, got: {combined[:200]}"
    )
