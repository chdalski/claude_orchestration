"""Shared fixtures for blueprint_v2 tests."""

import sys
from pathlib import Path

import yaml

# Ensure this blueprint's test directory is on sys.path for imports
_tests_dir = str(Path(__file__).parent)
if _tests_dir not in sys.path:
    sys.path.insert(0, _tests_dir)

from dotenv import load_dotenv

# Path constants
BLUEPRINT_ROOT = Path(__file__).parent.parent
REPO_ROOT = BLUEPRINT_ROOT.parent

# Load .env.local from repo root (if it exists) before tests run
load_dotenv(REPO_ROOT / ".env.local")

CLAUDE_DIR = BLUEPRINT_ROOT / ".claude"
AGENTS_DIR = CLAUDE_DIR / "agents"
SETTINGS_FILE = CLAUDE_DIR / "settings.json"
CLAUDE_MD = CLAUDE_DIR / "CLAUDE.md"

WORKFLOWS_DIR = CLAUDE_DIR / "workflows"
WORKFLOWS_CLAUDE_MD = WORKFLOWS_DIR / "CLAUDE.md"

AI_DIR = BLUEPRINT_ROOT / ".ai"
PLANS_DIR = AI_DIR / "plans"
PLANS_CLAUDE_MD = PLANS_DIR / "CLAUDE.md"


def parse_frontmatter(filepath: Path) -> dict:
    """Extract YAML frontmatter from a markdown file.

    Expects files starting with '---', YAML content, then '---'.
    Returns the parsed YAML as a dict, or empty dict if no frontmatter.
    """
    text = filepath.read_text()
    if not text.startswith("---"):
        return {}
    end = text.index("---", 3)
    yaml_text = text[3:end].strip()
    return yaml.safe_load(yaml_text) or {}
