"""Shared fixtures for behavioral tests.

SDK quirks and design decisions (claude-agent-sdk 0.1.48, CLI 2.1.76):

- can_use_tool callback: Does not fire with this CLI version. The SDK
  sets --permission-prompt-tool stdio, but the CLI never sends
  can_use_tool control requests. Track tools via ToolUseBlock in the
  message stream instead.

- Nested sessions: The CLI refuses to start inside another Claude Code
  session (CLAUDECODE env var). Pass env={"CLAUDECODE": ""} to unset it.

- Blueprint CLAUDE.md conflict: The lead's CLAUDE.md says "delegate to
  specialized agents." Behavioral tests that need the agent to use tools
  directly must pass system_prompt (with preset append) to override this.
"""

import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "minimal_project"
BLUEPRINT_CLAUDE_DIR = Path(__file__).parent.parent.parent / ".claude"


def _has_claude_auth() -> bool:
    """Check whether any valid Claude Code authentication is available.

    The SDK spawns the CLI as a subprocess, so it inherits
    whatever auth the CLI has — API key, OAuth, or cloud
    provider credentials. Checking only ANTHROPIC_API_KEY
    would skip tests for OAuth users who are fully
    authenticated.
    """
    # API key (direct Anthropic API)
    if os.environ.get("ANTHROPIC_API_KEY"):
        return True

    # OAuth (claude login) — credentials stored by the CLI
    credentials_file = Path.home() / ".claude" / ".credentials.json"
    if credentials_file.is_file():
        try:
            import json

            creds = json.loads(credentials_file.read_text())
            if creds.get("claudeAiOauth"):
                return True
        except (json.JSONDecodeError, OSError):
            pass

    # Cloud providers (Bedrock, Vertex, Azure)
    if os.environ.get("CLAUDE_CODE_USE_BEDROCK"):
        return True
    if os.environ.get("CLAUDE_CODE_USE_VERTEX"):
        return True

    return False


def pytest_collection_modifyitems(config, items):
    """Skip behavioral tests if no Claude Code authentication is available."""
    if not _has_claude_auth():
        skip = pytest.mark.skip(reason="No Claude Code auth (API key, OAuth, or cloud provider)")
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
    The .ai/plans/ directory is created at runtime by the
    ensure-plans-dir skill, so it does not need to be pre-created.
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


# Environment overrides for spawning nested Claude Code sessions.
# Unsetting CLAUDECODE avoids "cannot be launched inside another session" error.
NESTED_SESSION_ENV: dict[str, str] = {"CLAUDECODE": ""}
