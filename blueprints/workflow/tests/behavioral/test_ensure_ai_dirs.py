"""Behavioral tests verifying the ensure-ai-dirs skill creates .ai/ directories and syncs templates.

These tests spawn a real Claude Code session and invoke the /ensure-ai-dirs
skill in a tmp project that has no .ai/ directory. The skill should:
- Copy .claude/skills/ensure-ai-dirs/plan-format.md to .ai/plans/plan-format.md
- Copy .claude/skills/ensure-ai-dirs/claude-md-template.md to .ai/plans/CLAUDE.md
- Create .ai/memory/ for Claude Code's auto-memory system
"""

from pathlib import Path

import pytest

from claude_agent_sdk import ClaudeAgentOptions, query
from claude_agent_sdk.types import AssistantMessage, TextBlock

from behavioral.conftest import NESTED_SESSION_ENV

pytestmark = pytest.mark.behavioral

# Invoke the skill via its slash command. The skill instructions are injected
# into context automatically; the prompt triggers execution.
ENSURE_AI_DIRS_PROMPT = (
    "Run /ensure-ai-dirs now. Follow the skill instructions exactly:\n"
    "1. Read .claude/settings.json for plansDirectory and autoMemoryDirectory.\n"
    "2. Sync two files to the plans directory:\n"
    "   a. Read .claude/skills/ensure-ai-dirs/plan-format.md and write to .ai/plans/plan-format.md\n"
    "   b. Read .claude/skills/ensure-ai-dirs/claude-md-template.md and write to .ai/plans/CLAUDE.md\n"
    "3. Ensure .ai/memory/ directory exists.\n"
    "4. Report what you did.\n"
    "Do this now."
)


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_ensure_ai_dirs_creates_directories_and_syncs_templates(fixture_project):
    """The skill should create .ai/plans/ with both templates and .ai/memory/ when they don't exist."""
    plans_dir = fixture_project / ".ai" / "plans"
    memory_dir = fixture_project / ".ai" / "memory"
    format_guide = plans_dir / "plan-format.md"
    plans_claude_md = plans_dir / "CLAUDE.md"
    format_template = fixture_project / ".claude" / "templates" / "plan-format.md"
    claude_md_template = fixture_project / ".claude" / "templates" / "claude-md-template.md"

    # Preconditions: .ai/ does not exist, templates do
    assert not plans_dir.exists(), "Test precondition: .ai/plans/ should not exist yet"
    assert not memory_dir.exists(), "Test precondition: .ai/memory/ should not exist yet"
    assert format_template.exists(), "Test precondition: plan-format.md template must exist"
    assert claude_md_template.exists(), "Test precondition: claude-md-template.md must exist"

    options = ClaudeAgentOptions(
        cwd=str(fixture_project),
        max_turns=5,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
    )

    async for _ in query(prompt=ENSURE_AI_DIRS_PROMPT, options=options):
        pass

    assert plans_dir.is_dir(), "Skill should have created .ai/plans/"
    assert format_guide.is_file(), "Skill should have written .ai/plans/plan-format.md"
    assert plans_claude_md.is_file(), "Skill should have written .ai/plans/CLAUDE.md"
    assert memory_dir.is_dir(), "Skill should have created .ai/memory/"

    expected_format = format_template.read_text()
    actual_format = format_guide.read_text()
    assert actual_format == expected_format, (
        "Skill should copy plan-format.md template verbatim to .ai/plans/plan-format.md"
    )

    expected_claude_md = claude_md_template.read_text()
    actual_claude_md = plans_claude_md.read_text()
    assert actual_claude_md == expected_claude_md, (
        "Skill should copy claude-md-template.md verbatim to .ai/plans/CLAUDE.md"
    )


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_ensure_ai_dirs_overwrites_outdated_format_guide(fixture_project):
    """The skill should overwrite .ai/plans/plan-format.md when it differs from the template."""
    plans_dir = fixture_project / ".ai" / "plans"
    format_guide = plans_dir / "plan-format.md"
    format_template = fixture_project / ".claude" / "templates" / "plan-format.md"

    # Precondition: create an outdated format guide
    plans_dir.mkdir(parents=True, exist_ok=True)
    format_guide.write_text("# Outdated plan format\n\nThis is stale content.\n")

    options = ClaudeAgentOptions(
        cwd=str(fixture_project),
        max_turns=5,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
    )

    async for _ in query(prompt=ENSURE_AI_DIRS_PROMPT, options=options):
        pass

    expected = format_template.read_text()
    actual = format_guide.read_text()
    assert actual == expected, (
        "Skill should have overwritten the outdated format guide with the template"
    )


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_ensure_ai_dirs_leaves_current_format_guide_unchanged(fixture_project):
    """The skill should not rewrite .ai/plans/plan-format.md when it already matches the template."""
    plans_dir = fixture_project / ".ai" / "plans"
    format_guide = plans_dir / "plan-format.md"
    format_template = fixture_project / ".claude" / "templates" / "plan-format.md"

    # Precondition: format guide already matches template
    plans_dir.mkdir(parents=True, exist_ok=True)
    template_content = format_template.read_text()
    format_guide.write_text(template_content)

    options = ClaudeAgentOptions(
        cwd=str(fixture_project),
        max_turns=5,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
    )

    async for _ in query(prompt=ENSURE_AI_DIRS_PROMPT, options=options):
        pass

    actual = format_guide.read_text()
    assert actual == template_content, (
        "Skill should not have changed a format guide that already matches the template"
    )
