"""Tests that all required files and directories exist."""

import pytest

from blueprint_contracts import (
    REQUIRED_CLAUDE_FILES,
    REQUIRED_DIRECTORIES,
    REQUIRED_ROOT_FILES,
)
from conftest import CLAUDE_DIR, BLUEPRINT_ROOT

pytestmark = pytest.mark.static


@pytest.mark.parametrize("filename", REQUIRED_CLAUDE_FILES)
def test_claude_file_exists(filename):
    path = CLAUDE_DIR / filename
    assert path.exists(), f"Missing required file: .claude/{filename}"


@pytest.mark.parametrize("dirname", REQUIRED_DIRECTORIES)
def test_directory_exists(dirname):
    path = BLUEPRINT_ROOT / dirname
    assert path.is_dir(), f"Missing required directory: {dirname}"


@pytest.mark.parametrize("filepath", REQUIRED_ROOT_FILES)
def test_root_file_exists(filepath):
    path = BLUEPRINT_ROOT / filepath
    assert path.exists(), f"Missing required file: {filepath}"
