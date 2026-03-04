"""Tests that agent frontmatter matches the contracts."""

import pytest

from blueprint_contracts import (
    AGENT_COLORS,
    AGENT_FILES,
    AGENT_MODELS,
    AGENT_TOOLS,
    AGENTS_WITHOUT_TASK_CREATE,
    AGENTS_WITHOUT_WRITE,
)
from conftest import AGENTS_DIR, parse_frontmatter

pytestmark = pytest.mark.static


def _load_agent(name: str) -> dict:
    filename = AGENT_FILES[name]
    return parse_frontmatter(AGENTS_DIR / filename)


@pytest.mark.parametrize("agent_name", AGENT_FILES.keys())
def test_agent_has_name(agent_name):
    fm = _load_agent(agent_name)
    assert fm.get("name") == agent_name, (
        f"Agent {agent_name}: expected name={agent_name!r}, got {fm.get('name')!r}"
    )


@pytest.mark.parametrize("agent_name", AGENT_FILES.keys())
def test_agent_has_description(agent_name):
    fm = _load_agent(agent_name)
    assert fm.get("description"), f"Agent {agent_name} missing description"


@pytest.mark.parametrize("agent_name", AGENT_FILES.keys())
def test_agent_model_matches(agent_name):
    fm = _load_agent(agent_name)
    expected = AGENT_MODELS[agent_name]
    assert fm.get("model") == expected, (
        f"Agent {agent_name}: expected model={expected!r}, got {fm.get('model')!r}"
    )


@pytest.mark.parametrize("agent_name", AGENT_FILES.keys())
def test_agent_color_matches(agent_name):
    fm = _load_agent(agent_name)
    expected = AGENT_COLORS[agent_name]
    assert fm.get("color") == expected, (
        f"Agent {agent_name}: expected color={expected!r}, got {fm.get('color')!r}"
    )


@pytest.mark.parametrize("agent_name", AGENT_FILES.keys())
def test_agent_tools_match_exactly(agent_name):
    fm = _load_agent(agent_name)
    actual = set(fm.get("tools", []))
    expected = AGENT_TOOLS[agent_name]
    assert actual == expected, (
        f"Agent {agent_name} tool mismatch:\n"
        f"  missing: {expected - actual}\n"
        f"  extra:   {actual - expected}"
    )


@pytest.mark.parametrize("agent_name", AGENTS_WITHOUT_WRITE)
def test_advisory_agents_lack_write_edit(agent_name):
    fm = _load_agent(agent_name)
    tools = set(fm.get("tools", []))
    assert "Write" not in tools, f"{agent_name} should not have Write tool"
    assert "Edit" not in tools, f"{agent_name} should not have Edit tool"


@pytest.mark.parametrize("agent_name", AGENTS_WITHOUT_TASK_CREATE)
def test_non_architects_lack_task_create(agent_name):
    fm = _load_agent(agent_name)
    tools = set(fm.get("tools", []))
    assert "TaskCreate" not in tools, f"{agent_name} should not have TaskCreate tool"
