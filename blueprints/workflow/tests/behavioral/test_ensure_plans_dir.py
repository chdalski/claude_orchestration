"""Behavioral tests verifying the ensure-plans-dir skill creates .ai/plans/ and its format guide.

These tests spawn a real Claude Code session and invoke the /ensure-plans-dir
skill in a tmp project that has no .ai/ directory. The skill should read
the canonical template from .claude/templates/plan-format.md and
write it to .ai/plans/CLAUDE.md, creating the directory if needed.
"""

from pathlib import Path

import pytest

from claude_agent_sdk import ClaudeAgentOptions, query
from claude_agent_sdk.types import AssistantMessage, TextBlock

from behavioral.conftest import NESTED_SESSION_ENV

pytestmark = pytest.mark.behavioral

# Invoke the skill via its slash command. The skill instructions are injected
# into context automatically; the prompt triggers execution.
ENSURE_PLANS_DIR_PROMPT = (
    "Run /ensure-plans-dir now. Follow the skill instructions exactly:\n"
    "1. Check if .ai/plans/CLAUDE.md exists.\n"
    "2. If missing, read .claude/templates/plan-format.md and write its content "
    "to .ai/plans/CLAUDE.md.\n"
    "3. If present and matching the template, do nothing.\n"
    "4. If present but different from the template, overwrite it.\n"
    "5. Report what you did.\n"
    "Do this now."
)


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_ensure_plans_dir_creates_directory_and_format_guide(fixture_project):
    """The skill should create .ai/plans/CLAUDE.md from the template when it doesn't exist."""
    plans_dir = fixture_project / ".ai" / "plans"
    format_guide = plans_dir / "CLAUDE.md"
    template = fixture_project / ".claude" / "templates" / "plan-format.md"

    # Preconditions: .ai/plans/ does not exist, template does
    assert not plans_dir.exists(), "Test precondition: .ai/plans/ should not exist yet"
    assert template.exists(), "Test precondition: template must exist in .claude/templates/"

    options = ClaudeAgentOptions(
        cwd=str(fixture_project),
        max_turns=5,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
    )

    async for _ in query(prompt=ENSURE_PLANS_DIR_PROMPT, options=options):
        pass

    assert plans_dir.is_dir(), "Skill should have created .ai/plans/"
    assert format_guide.is_file(), "Skill should have written .ai/plans/CLAUDE.md"

    expected = template.read_text()
    actual = format_guide.read_text()
    assert actual == expected, (
        "Skill should copy the template verbatim to .ai/plans/CLAUDE.md"
    )


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_ensure_plans_dir_overwrites_outdated_format_guide(fixture_project):
    """The skill should overwrite .ai/plans/CLAUDE.md when it differs from the template."""
    plans_dir = fixture_project / ".ai" / "plans"
    format_guide = plans_dir / "CLAUDE.md"
    template = fixture_project / ".claude" / "templates" / "plan-format.md"

    # Precondition: create an outdated format guide
    plans_dir.mkdir(parents=True, exist_ok=True)
    format_guide.write_text("# Outdated plan format\n\nThis is stale content.\n")

    options = ClaudeAgentOptions(
        cwd=str(fixture_project),
        max_turns=5,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
    )

    async for _ in query(prompt=ENSURE_PLANS_DIR_PROMPT, options=options):
        pass

    expected = template.read_text()
    actual = format_guide.read_text()
    assert actual == expected, (
        "Skill should have overwritten the outdated format guide with the template"
    )


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_ensure_plans_dir_leaves_current_format_guide_unchanged(fixture_project):
    """The skill should not rewrite .ai/plans/CLAUDE.md when it already matches the template."""
    plans_dir = fixture_project / ".ai" / "plans"
    format_guide = plans_dir / "CLAUDE.md"
    template = fixture_project / ".claude" / "templates" / "plan-format.md"

    # Precondition: format guide already matches template
    plans_dir.mkdir(parents=True, exist_ok=True)
    template_content = template.read_text()
    format_guide.write_text(template_content)

    options = ClaudeAgentOptions(
        cwd=str(fixture_project),
        max_turns=5,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
    )

    async for _ in query(prompt=ENSURE_PLANS_DIR_PROMPT, options=options):
        pass

    actual = format_guide.read_text()
    assert actual == template_content, (
        "Skill should not have changed a format guide that already matches the template"
    )
