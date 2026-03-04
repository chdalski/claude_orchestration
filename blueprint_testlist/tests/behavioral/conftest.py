"""Shared fixtures for behavioral tests.

SDK quirks and design decisions (claude-code-sdk 0.0.25, CLI 2.1.63):

- can_use_tool callback: Does not fire with this CLI version. The SDK
  sets --permission-prompt-tool stdio, but the CLI never sends
  can_use_tool control requests. Track tools via ToolUseBlock in the
  message stream instead.

- Nested sessions: The CLI refuses to start inside another Claude Code
  session (CLAUDECODE env var). Pass env={"CLAUDECODE": ""} to unset it.

- Blueprint CLAUDE.md conflict: The lead's CLAUDE.md says "never
  implement code". Behavioral tests that need the agent to use tools
  directly must pass append_system_prompt to override this.

- SessionStart hook overhead: The blueprint's SessionStart hook tells
  the agent to read many knowledge files, consuming most of max_turns.
  Use fixture_project_no_hooks for tests that need fast tool execution.

- TaskCreate is team-only: It requires a running team context. Cannot
  be tested in isolation without a full team setup (~$5-20 per run).
  Static tests verify the Architect's frontmatter includes it.
"""

import json
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "minimal_project"
BLUEPRINT_CLAUDE_DIR = Path(__file__).parent.parent.parent / ".claude"


def pytest_collection_modifyitems(config, items):
    """Skip behavioral tests if ANTHROPIC_API_KEY is not set."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        skip = pytest.mark.skip(reason="ANTHROPIC_API_KEY not set")
        for item in items:
            if "behavioral" in str(item.fspath):
                item.add_marker(skip)


@dataclass
class ToolCallRecord:
    """A single intercepted tool call."""

    tool_name: str
    input_data: dict[str, Any]


@dataclass
class ToolCallLog:
    """Accumulates tool invocations during a session."""

    records: list[ToolCallRecord] = field(default_factory=list)

    def record(self, tool_name: str, input_data: dict[str, Any]) -> None:
        self.records.append(ToolCallRecord(tool_name=tool_name, input_data=input_data))

    @property
    def tool_names(self) -> list[str]:
        return [r.tool_name for r in self.records]

    def calls_for(self, tool_name: str) -> list[ToolCallRecord]:
        return [r for r in self.records if r.tool_name == tool_name]

    def has(self, tool_name: str) -> bool:
        return any(r.tool_name == tool_name for r in self.records)


@pytest.fixture
def fixture_project(tmp_path: Path) -> Path:
    """Copy the minimal project and blueprint .claude/ into a tmp directory.

    Returns the tmp project root, ready for Claude Code sessions.
    """
    # Copy minimal project files
    for item in FIXTURES_DIR.iterdir():
        dest = tmp_path / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    # Copy blueprint .claude/ directory
    dest_claude = tmp_path / ".claude"
    shutil.copytree(BLUEPRINT_CLAUDE_DIR, dest_claude)

    return tmp_path


@pytest.fixture
def fixture_project_no_hooks(tmp_path: Path) -> Path:
    """Copy the minimal project with blueprint .claude/ but strip hooks.

    This avoids the SessionStart hook triggering a long startup chain
    that consumes all turns before the test prompt runs.
    """
    for item in FIXTURES_DIR.iterdir():
        dest = tmp_path / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    dest_claude = tmp_path / ".claude"
    shutil.copytree(BLUEPRINT_CLAUDE_DIR, dest_claude)

    # Strip hooks from settings.json to keep sessions fast
    settings_path = dest_claude / "settings.json"
    settings = json.loads(settings_path.read_text())
    settings.pop("hooks", None)
    settings_path.write_text(json.dumps(settings, indent=2))

    return tmp_path


# Environment overrides for spawning nested Claude Code sessions.
# Unsetting CLAUDECODE avoids "cannot be launched inside another session" error.
NESTED_SESSION_ENV: dict[str, str] = {"CLAUDECODE": ""}
