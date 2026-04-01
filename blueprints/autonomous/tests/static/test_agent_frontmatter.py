"""Tests that agent definition files have correct frontmatter matching contracts."""

import pytest

from blueprint_contracts import AGENT_FILES, AGENT_MODELS, AGENT_TOOLS
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
def test_agent_tools_match_exactly(agent_name, filename):
    """Frontmatter 'tools' must match the contract set exactly."""
    fm = parse_frontmatter(AGENTS_DIR / filename)
    actual = set(fm.get("tools", []))
    expected = AGENT_TOOLS[agent_name]
    assert actual == expected, (
        f"Agent {filename}: expected tools {sorted(expected)}, got {sorted(actual)}"
    )
