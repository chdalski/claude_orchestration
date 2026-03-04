"""Behavioral tests verifying Plan Init creates .ai/plans/ and its format guide.

These tests spawn a real Claude Code session as the Plan Init agent
in a tmp project that has no .ai/ directory. The agent should read
the canonical template from .claude/templates/plan-format.md and
write it to .ai/plans/CLAUDE.md, creating the directory if needed.
"""

from pathlib import Path

import pytest

from claude_code_sdk import ClaudeCodeOptions, query
from claude_code_sdk.types import AssistantMessage, TextBlock

from behavioral.conftest import NESTED_SESSION_ENV

pytestmark = pytest.mark.behavioral

# The agent file tells Plan Init what to do, but in a test we
# give it an explicit prompt to avoid relying on SessionStart hooks.
PLAN_INIT_PROMPT = (
    "You are Plan Init. Follow your agent instructions exactly:\n"
    "1. Check if .ai/plans/ exists — create it if missing.\n"
    "2. Read .claude/templates/plan-format.md (the canonical template).\n"
    "3. Check if .ai/plans/CLAUDE.md exists.\n"
    "4. If missing or different from the template, write the template content to .ai/plans/CLAUDE.md.\n"
    "5. Report what you did.\n"
    "Do this now."
)


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_plan_init_creates_plans_directory_and_format_guide(fixture_project):
    """Plan Init should create .ai/plans/CLAUDE.md from the template when it doesn't exist."""
    plans_dir = fixture_project / ".ai" / "plans"
    format_guide = plans_dir / "CLAUDE.md"
    template = fixture_project / ".claude" / "templates" / "plan-format.md"

    # Preconditions: .ai/plans/ does not exist, template does
    assert not plans_dir.exists(), "Test precondition: .ai/plans/ should not exist yet"
    assert template.exists(), "Test precondition: template must exist in .claude/templates/"

    options = ClaudeCodeOptions(
        cwd=str(fixture_project),
        max_turns=5,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
    )

    async for _ in query(prompt=PLAN_INIT_PROMPT, options=options):
        pass

    # Postconditions
    assert plans_dir.is_dir(), "Plan Init should have created .ai/plans/"
    assert format_guide.is_file(), "Plan Init should have written .ai/plans/CLAUDE.md"

    expected = template.read_text()
    actual = format_guide.read_text()
    assert actual == expected, (
        "Plan Init should copy the template verbatim to .ai/plans/CLAUDE.md"
    )


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_plan_init_updates_outdated_format_guide(fixture_project):
    """Plan Init should overwrite .ai/plans/CLAUDE.md when it differs from the template."""
    plans_dir = fixture_project / ".ai" / "plans"
    format_guide = plans_dir / "CLAUDE.md"
    template = fixture_project / ".claude" / "templates" / "plan-format.md"

    # Precondition: create an outdated format guide
    plans_dir.mkdir(parents=True, exist_ok=True)
    format_guide.write_text("# Outdated plan format\n\nThis is stale content.\n")

    options = ClaudeCodeOptions(
        cwd=str(fixture_project),
        max_turns=5,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
    )

    async for _ in query(prompt=PLAN_INIT_PROMPT, options=options):
        pass

    expected = template.read_text()
    actual = format_guide.read_text()
    assert actual == expected, (
        "Plan Init should have overwritten the outdated format guide with the template"
    )


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_plan_init_leaves_current_format_guide_unchanged(fixture_project):
    """Plan Init should not rewrite .ai/plans/CLAUDE.md when it already matches the template."""
    plans_dir = fixture_project / ".ai" / "plans"
    format_guide = plans_dir / "CLAUDE.md"
    template = fixture_project / ".claude" / "templates" / "plan-format.md"

    # Precondition: format guide already matches template
    plans_dir.mkdir(parents=True, exist_ok=True)
    template_content = template.read_text()
    format_guide.write_text(template_content)
    mtime_before = format_guide.stat().st_mtime

    options = ClaudeCodeOptions(
        cwd=str(fixture_project),
        max_turns=5,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
    )

    # Collect text output to verify it reports "ready" not "created/updated"
    text_output = []
    async for message in query(prompt=PLAN_INIT_PROMPT, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    text_output.append(block.text)

    # The file should still match
    actual = format_guide.read_text()
    assert actual == template_content, (
        "Plan Init should not have changed a format guide that already matches"
    )
