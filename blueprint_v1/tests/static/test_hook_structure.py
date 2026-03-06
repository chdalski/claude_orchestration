"""Tests that hook configuration matches the contracts."""

import json

import pytest

from blueprint_contracts import HOOK_EVENTS_REQUIRED
from conftest import SETTINGS_FILE

pytestmark = pytest.mark.static


@pytest.fixture
def settings() -> dict:
    return json.loads(SETTINGS_FILE.read_text())


@pytest.fixture
def hooks(settings) -> dict:
    return settings.get("hooks", {})


def test_agent_teams_enabled(settings):
    env = settings.get("env", {})
    assert env.get("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS") == "1", (
        "Agent teams must be enabled via env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS"
    )


def test_teammate_mode_in_process(settings):
    assert settings.get("teammateMode") == "in-process", (
        "teammateMode must be 'in-process'"
    )


@pytest.mark.parametrize("event", HOOK_EVENTS_REQUIRED)
def test_required_hook_event_present(hooks, event):
    assert event in hooks, f"Missing required hook event: {event}"


def test_session_start_outputs_checklist(hooks):
    session_start = hooks.get("SessionStart", [])
    assert len(session_start) > 0, "SessionStart must have at least one hook group"

    # Collect all commands from all hook groups
    commands = []
    for group in session_start:
        for hook in group.get("hooks", []):
            if hook.get("type") == "command":
                commands.append(hook["command"])

    combined = " ".join(commands)
    assert "Startup Checklist" in combined or "checklist" in combined.lower(), (
        "SessionStart hook must output a startup checklist"
    )


def test_pre_tool_use_matches_git_commit(hooks):
    pre_tool_use = hooks.get("PreToolUse", [])
    assert len(pre_tool_use) > 0, "PreToolUse must have at least one hook group"

    matchers = [group.get("matcher", "") for group in pre_tool_use]
    has_git_commit = any("git commit" in m for m in matchers)
    assert has_git_commit, (
        "PreToolUse must have a matcher for Bash(git commit*)"
    )


def test_pre_tool_use_has_documentation_check(hooks):
    pre_tool_use = hooks.get("PreToolUse", [])
    commands = []
    for group in pre_tool_use:
        for hook in group.get("hooks", []):
            if hook.get("type") == "command":
                commands.append(hook["command"])

    combined = " ".join(commands)
    assert "DOCUMENTATION CHECK" in combined or "documentation" in combined.lower(), (
        "PreToolUse must include documentation check"
    )


def test_pre_tool_use_has_housekeeping_check(hooks):
    pre_tool_use = hooks.get("PreToolUse", [])
    commands = []
    for group in pre_tool_use:
        for hook in group.get("hooks", []):
            if hook.get("type") == "command":
                commands.append(hook["command"])

    combined = " ".join(commands)
    assert "HOUSEKEEPING" in combined, (
        "PreToolUse must include housekeeping check"
    )


def test_pre_compact_has_status_reminder(hooks):
    pre_compact = hooks.get("PreCompact", [])
    assert len(pre_compact) > 0, "PreCompact must have at least one hook group"

    commands = []
    for group in pre_compact:
        for hook in group.get("hooks", []):
            if hook.get("type") == "command":
                commands.append(hook["command"])

    combined = " ".join(commands)
    assert "compacted" in combined.lower() or "status" in combined.lower(), (
        "PreCompact hook must remind about status"
    )


def test_all_hooks_are_command_type(hooks):
    for event, groups in hooks.items():
        for group in groups:
            for hook in group.get("hooks", []):
                assert hook.get("type") == "command", (
                    f"Hook in {event} must be type 'command', got {hook.get('type')!r}"
                )
