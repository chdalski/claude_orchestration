"""Behavioral tests verifying the ensure-ai-dirs skill creates .ai/ directories and plan format guide.

These tests spawn a real Claude Code session and invoke the /ensure-ai-dirs
skill in a tmp project that has no .ai/ directory. The skill should read
the canonical template from .claude/skills/ensure-ai-dirs/plan-format.md
and write it to .ai/plans/CLAUDE.md, creating the directory if needed.
It should also create .ai/memory/ for Claude Code's auto-memory system.

When plansDirectory or autoMemoryDirectory is absent from settings.json,
the skill should create settings.local.json with the default values rather
than silently defaulting.
"""

import json
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
    "1. Check if .ai/plans/CLAUDE.md exists.\n"
    "2. If missing, read .claude/skills/ensure-ai-dirs/plan-format.md and write "
    "its content to .ai/plans/CLAUDE.md.\n"
    "3. If present and matching the template, do nothing.\n"
    "4. If present but different from the template, overwrite it.\n"
    "5. Ensure .ai/memory/ directory exists.\n"
    "6. Report what you did.\n"
    "Do this now."
)


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_ensure_ai_dirs_creates_directories_and_format_guide(fixture_project):
    """The skill should create .ai/plans/CLAUDE.md from the template and .ai/memory/ when they don't exist."""
    plans_dir = fixture_project / ".ai" / "plans"
    memory_dir = fixture_project / ".ai" / "memory"
    format_guide = plans_dir / "CLAUDE.md"
    template = fixture_project / ".claude" / "skills" / "ensure-ai-dirs" / "plan-format.md"

    # Preconditions: .ai/ does not exist, template does
    assert not plans_dir.exists(), "Test precondition: .ai/plans/ should not exist yet"
    assert not memory_dir.exists(), "Test precondition: .ai/memory/ should not exist yet"
    assert template.exists(), "Test precondition: template must exist in .claude/skills/ensure-ai-dirs/"

    options = ClaudeAgentOptions(
        cwd=str(fixture_project),
        max_turns=5,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
    )

    async for _ in query(prompt=ENSURE_AI_DIRS_PROMPT, options=options):
        pass

    assert plans_dir.is_dir(), "Skill should have created .ai/plans/"
    assert format_guide.is_file(), "Skill should have written .ai/plans/CLAUDE.md"
    assert memory_dir.is_dir(), "Skill should have created .ai/memory/"

    expected = template.read_text().rstrip("\n")
    actual = format_guide.read_text().rstrip("\n")
    assert actual == expected, (
        "Skill should copy the template verbatim to .ai/plans/CLAUDE.md"
    )


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_ensure_ai_dirs_overwrites_outdated_format_guide(fixture_project):
    """The skill should overwrite .ai/plans/CLAUDE.md when it differs from the template."""
    plans_dir = fixture_project / ".ai" / "plans"
    format_guide = plans_dir / "CLAUDE.md"
    template = fixture_project / ".claude" / "skills" / "ensure-ai-dirs" / "plan-format.md"

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

    expected = template.read_text().rstrip("\n")
    actual = format_guide.read_text().rstrip("\n")
    assert actual == expected, (
        "Skill should have overwritten the outdated format guide with the template"
    )


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_ensure_ai_dirs_leaves_current_format_guide_unchanged(fixture_project):
    """The skill should not rewrite .ai/plans/CLAUDE.md when it already matches the template."""
    plans_dir = fixture_project / ".ai" / "plans"
    format_guide = plans_dir / "CLAUDE.md"
    template = fixture_project / ".claude" / "skills" / "ensure-ai-dirs" / "plan-format.md"

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

    async for _ in query(prompt=ENSURE_AI_DIRS_PROMPT, options=options):
        pass

    actual = format_guide.read_text()
    assert actual == template_content, (
        "Skill should not have changed a format guide that already matches the template"
    )


# Prompt that covers the missing config keys → settings.local.json flow.
# Separate from the main prompt because the main one re-states steps that
# don't include this behavior, and mixing them could confuse the agent.
ENSURE_AI_DIRS_MISSING_CONFIG_PROMPT = (
    "Run /ensure-ai-dirs now. Follow the skill instructions exactly:\n"
    "1. Read .claude/settings.json and check for plansDirectory and autoMemoryDirectory.\n"
    "2. If plansDirectory is absent, read .claude/settings.local.json (if it "
    "exists), add plansDirectory set to '.ai/plans/' to it, and write it back "
    "to .claude/settings.local.json. If settings.local.json does not exist, "
    'create it with just {"plansDirectory": ".ai/plans/"}.\n'
    "3. Read .claude/skills/ensure-ai-dirs/plan-format.md and write its "
    "content to .ai/plans/CLAUDE.md (creating the directory if needed).\n"
    "4. Ensure .ai/memory/ directory exists.\n"
    "5. Report what you did.\n"
    "Do this now."
)


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_ensure_ai_dirs_creates_settings_local_when_plans_directory_missing(
    fixture_project,
):
    """When plansDirectory is absent from settings.json, the skill should create
    settings.local.json with the default value instead of silently defaulting.

    Silently defaulting leaves future sessions and other agents without a
    configured path — they would each need to re-derive the default.
    """
    settings_file = fixture_project / ".claude" / "settings.json"
    settings_local_file = fixture_project / ".claude" / "settings.local.json"
    plans_dir = fixture_project / ".ai" / "plans"
    format_guide = plans_dir / "CLAUDE.md"
    template = fixture_project / ".claude" / "skills" / "ensure-ai-dirs" / "plan-format.md"

    # Precondition: remove plansDirectory from settings.json
    settings = json.loads(settings_file.read_text())
    del settings["plansDirectory"]
    settings_file.write_text(json.dumps(settings, indent=2) + "\n")

    # Precondition: no settings.local.json exists
    assert not settings_local_file.exists(), (
        "Test precondition: settings.local.json should not exist yet"
    )

    options = ClaudeAgentOptions(
        cwd=str(fixture_project),
        max_turns=10,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
    )

    async for _ in query(
        prompt=ENSURE_AI_DIRS_MISSING_CONFIG_PROMPT, options=options
    ):
        pass

    # The skill should have created settings.local.json with plansDirectory
    assert settings_local_file.is_file(), (
        "Skill should have created .claude/settings.local.json "
        "when plansDirectory is absent from settings.json"
    )

    local_settings = json.loads(settings_local_file.read_text())
    assert "plansDirectory" in local_settings, (
        "settings.local.json should contain plansDirectory"
    )
    assert local_settings["plansDirectory"] == ".ai/plans/", (
        "settings.local.json plansDirectory should default to .ai/plans/"
    )

    # The skill should still have created the plans directory and format guide
    assert plans_dir.is_dir(), "Skill should have created .ai/plans/"
    assert format_guide.is_file(), "Skill should have written .ai/plans/CLAUDE.md"

    expected = template.read_text().rstrip("\n")
    actual = format_guide.read_text().rstrip("\n")
    assert actual == expected, (
        "Skill should copy the template verbatim to .ai/plans/CLAUDE.md"
    )
