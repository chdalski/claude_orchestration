"""Tests that all required files and directories exist in the blueprint."""

import pytest

from blueprint_contracts import (
    REQUIRED_AGENT_FILES,
    REQUIRED_DIRECTORIES,
    REQUIRED_KNOWLEDGE_BASE,
    REQUIRED_KNOWLEDGE_LANGUAGES,
    REQUIRED_PRACTICES,
    REQUIRED_TEMPLATES,
    REQUIRED_TOP_LEVEL_FILES,
)
from conftest import (
    AGENTS_DIR,
    CLAUDE_DIR,
    KNOWLEDGE_BASE_DIR,
    KNOWLEDGE_EXTENSIONS_DIR,
    KNOWLEDGE_LANGUAGES_DIR,
    PRACTICES_DIR,
    TEMPLATES_DIR,
)

pytestmark = pytest.mark.static


@pytest.mark.parametrize("filename", REQUIRED_TOP_LEVEL_FILES)
def test_top_level_file_exists(filename):
    path = CLAUDE_DIR / filename
    assert path.exists(), f"Missing required file: .claude/{filename}"


@pytest.mark.parametrize("dirname", REQUIRED_DIRECTORIES)
def test_directory_exists(dirname):
    path = CLAUDE_DIR / dirname
    assert path.is_dir(), f"Missing required directory: .claude/{dirname}"


@pytest.mark.parametrize("filename", REQUIRED_AGENT_FILES)
def test_agent_file_exists(filename):
    path = AGENTS_DIR / filename
    assert path.exists(), f"Missing agent file: .claude/agents/{filename}"


@pytest.mark.parametrize("filename", REQUIRED_KNOWLEDGE_BASE)
def test_knowledge_base_file_exists(filename):
    path = KNOWLEDGE_BASE_DIR / filename
    assert path.exists(), f"Missing knowledge base file: knowledge/base/{filename}"


@pytest.mark.parametrize("filename", REQUIRED_KNOWLEDGE_LANGUAGES)
def test_knowledge_language_file_exists(filename):
    path = KNOWLEDGE_LANGUAGES_DIR / filename
    assert path.exists(), f"Missing knowledge language file: knowledge/languages/{filename}"


@pytest.mark.parametrize("filename", REQUIRED_PRACTICES)
def test_practice_file_exists(filename):
    path = PRACTICES_DIR / filename
    assert path.exists(), f"Missing practice file: practices/{filename}"


@pytest.mark.parametrize("filename", REQUIRED_TEMPLATES)
def test_template_file_exists(filename):
    path = TEMPLATES_DIR / filename
    assert path.exists(), f"Missing template file: templates/{filename}"


def test_extensions_dir_has_readme():
    readme = KNOWLEDGE_EXTENSIONS_DIR / "README.md"
    assert readme.exists(), "Missing knowledge/extensions/README.md"
