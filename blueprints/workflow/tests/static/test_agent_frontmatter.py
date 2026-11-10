"""Tests that agent definition files have correct frontmatter matching contracts."""

import pytest

from blueprint_contracts import AGENT_FILES, AGENT_MODELS
from conftest import AGENTS_DIR, parse_frontmatter

pytestmark = pytest.mark.static


@pytest.mark.parametrize(
    "agent_name,filename",
    list(AGENT_FILES.items()),
    ids=list(AGENT_FILES.keys()),
)
def test_agent_has_name(agent_name, filename):
    """Frontmatter 'name' must match the contract key exactly."""
    fm = parse_frontmatter(AGENTS_DIR / filename)
    assert fm.get("name") == agent_name, (
        f"Agent {filename}: expected name {agent_name!r}, got {fm.get('name')!r}"
    )


@pytest.mark.parametrize(
    "agent_name,filename",
    list(AGENT_FILES.items()),
    ids=list(AGENT_FILES.keys()),
)
def test_agent_has_description(agent_name, filename):
    """Frontmatter 'description' must be a non-empty string."""
    fm = parse_frontmatter(AGENTS_DIR / filename)
    desc = fm.get("description", "")
    assert isinstance(desc, str) and desc.strip(), (
        f"Agent {filename}: description must be a non-empty string"
    )


@pytest.mark.parametrize(
    "agent_name,filename",
    list(AGENT_FILES.items()),
    ids=list(AGENT_FILES.keys()),
)
def test_agent_model_matches(agent_name, filename):
    """Frontmatter 'model' must match the contract."""
    fm = parse_frontmatter(AGENTS_DIR / filename)
    expected = AGENT_MODELS[agent_name]
    assert fm.get("model") == expected, (
        f"Agent {filename}: expected model {expected!r}, got {fm.get('model')!r}"
    )


@pytest.mark.parametrize(
    "agent_name,filename",
    list(AGENT_FILES.items()),
    ids=list(AGENT_FILES.keys()),
)
def test_agent_has_no_tool_restriction(agent_name, filename):
    """Frontmatter names no 'tools' or 'disallowedTools': every agent
    inherits the full tool set. An allowlist withheld the web tools a
    test designer needed to read a specification, and every new tool
    had to be added to each list by hand."""
    fm = parse_frontmatter(AGENTS_DIR / filename)
    restricted = {"tools", "disallowedTools"} & fm.keys()
    assert not restricted, (
        f"Agent {filename}: remove {sorted(restricted)} from the frontmatter"
    )
