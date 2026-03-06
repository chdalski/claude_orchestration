"""Tests for knowledge file integrity and cross-references."""

import pytest

from blueprint_contracts import LANGUAGE_CODE_MARKERS, REQUIRED_PRACTICES
from conftest import (
    AGENTS_DIR,
    KNOWLEDGE_BASE_DIR,
    KNOWLEDGE_LANGUAGES_DIR,
    PRACTICES_DIR,
    parse_frontmatter,
)

pytestmark = pytest.mark.static


def _base_knowledge_files():
    """Yield all base knowledge files."""
    return sorted(KNOWLEDGE_BASE_DIR.glob("*.md"))


def _agent_files():
    """Yield all agent files."""
    return sorted(AGENTS_DIR.glob("*.md"))


@pytest.mark.parametrize(
    "filepath",
    list(_base_knowledge_files()),
    ids=lambda p: p.name,
)
def test_base_knowledge_is_language_agnostic(filepath):
    """Base knowledge files must not contain language-specific code blocks."""
    content = filepath.read_text()
    violations = []
    for marker in LANGUAGE_CODE_MARKERS:
        if marker in content:
            # Find line number for better error messages
            for i, line in enumerate(content.splitlines(), 1):
                if marker in line:
                    violations.append(f"  line {i}: {marker}")

    assert not violations, (
        f"{filepath.name} contains language-specific code blocks "
        f"(base knowledge must be language-agnostic):\n"
        + "\n".join(violations)
    )


def _extract_knowledge_references(agent_content: str) -> list[str]:
    """Extract file paths referenced in agent Startup sections.

    Looks for patterns like:
    - knowledge/base/principles.md
    - .claude/knowledge/base/principles.md
    - knowledge/languages/*.md
    """
    import re

    # Match paths that look like knowledge file references
    pattern = r'(?:\.claude/)?knowledge/(?:base|languages|extensions)/[\w-]+\.md'
    return re.findall(pattern, agent_content)


@pytest.mark.parametrize(
    "agent_file",
    list(_agent_files()),
    ids=lambda p: p.name,
)
def test_agent_knowledge_references_exist(agent_file):
    """Every knowledge file referenced in an agent's Startup section must exist."""
    content = agent_file.read_text()
    refs = _extract_knowledge_references(content)

    missing = []
    for ref in refs:
        # Normalize path: remove .claude/ prefix if present
        clean = ref.removeprefix(".claude/")
        full_path = agent_file.parents[1] / clean  # .claude/ parent
        if not full_path.exists():
            missing.append(ref)

    assert not missing, (
        f"{agent_file.name} references missing knowledge files:\n"
        + "\n".join(f"  - {m}" for m in missing)
    )


def test_all_documented_languages_have_files():
    """Every language documented in knowledge/languages/ must have a file."""
    lang_files = list(KNOWLEDGE_LANGUAGES_DIR.glob("*.md"))
    assert len(lang_files) >= 1, "Must have at least one language file"


def test_all_practices_referenced_by_at_least_one_agent():
    """Each practice file should be referenced by at least one agent."""
    agent_contents = []
    for agent_file in _agent_files():
        agent_contents.append(agent_file.read_text())

    # Also check CLAUDE.md
    claude_md = AGENTS_DIR.parent / "CLAUDE.md"
    if claude_md.exists():
        agent_contents.append(claude_md.read_text())

    unreferenced = []
    for practice_name in REQUIRED_PRACTICES:
        stem = practice_name.removesuffix(".md")
        # Check if the practice name (with or without .md) appears in any agent content
        found = any(
            practice_name in content or stem in content
            for content in agent_contents
        )
        if not found:
            unreferenced.append(practice_name)

    assert not unreferenced, (
        "These practice files are not referenced by any agent:\n"
        + "\n".join(f"  - {p}" for p in unreferenced)
    )
