"""Shared fixtures for blueprint tests."""

from pathlib import Path

import yaml
from dotenv import load_dotenv

# Path constants
BLUEPRINT_ROOT = Path(__file__).parent.parent
REPO_ROOT = BLUEPRINT_ROOT.parent

# Load .env.local from repo root (if it exists) before tests run
load_dotenv(REPO_ROOT / ".env.local")

CLAUDE_DIR = BLUEPRINT_ROOT / ".claude"
AGENTS_DIR = CLAUDE_DIR / "agents"
KNOWLEDGE_DIR = CLAUDE_DIR / "knowledge"
KNOWLEDGE_BASE_DIR = KNOWLEDGE_DIR / "base"
KNOWLEDGE_LANGUAGES_DIR = KNOWLEDGE_DIR / "languages"
KNOWLEDGE_EXTENSIONS_DIR = KNOWLEDGE_DIR / "extensions"
PRACTICES_DIR = CLAUDE_DIR / "practices"
TEMPLATES_DIR = CLAUDE_DIR / "templates"
SETTINGS_FILE = CLAUDE_DIR / "settings.json"
CONFIG_FILE = CLAUDE_DIR / "config.json"
CLAUDE_MD = CLAUDE_DIR / "CLAUDE.md"


def parse_frontmatter(filepath: Path) -> dict:
    """Extract YAML frontmatter from a markdown file.

    Expects files starting with '---', YAML content, then '---'.
    Returns the parsed YAML as a dict, or empty dict if no frontmatter.
    """
    text = filepath.read_text()
    if not text.startswith("---"):
        return {}
    # Find the closing ---
    end = text.index("---", 3)
    yaml_text = text[3:end].strip()
    return yaml.safe_load(yaml_text) or {}
