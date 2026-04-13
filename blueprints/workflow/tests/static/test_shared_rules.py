"""Tests that shared rule files stay in sync across blueprints.

Rule files that exist in both blueprints (workflow and
autonomous) are intended to be identical — they encode
cross-cutting concerns like simplicity, code style, and
testing principles. When one copy is updated but the other
is not, agents in the stale blueprint follow outdated
guidance. This test catches that drift.
"""

from pathlib import Path

import pytest

from conftest import REPO_ROOT, RULES_DIR

pytestmark = pytest.mark.static

WORKFLOW_RULES = RULES_DIR
AUTONOMOUS_RULES = REPO_ROOT / "blueprints" / "autonomous" / ".claude" / "rules"

# Files that exist in both blueprints but differ
# intentionally — they contain blueprint-specific content.
KNOWN_DIVERGENT: set[str] = {
    "advisor-gate-independence.md",
    "risk-assessment.md",
}


def _shared_rule_files() -> list[str]:
    """Return filenames that exist in both blueprints' rules dirs."""
    if not WORKFLOW_RULES.is_dir() or not AUTONOMOUS_RULES.is_dir():
        return []
    workflow_names = {p.name for p in WORKFLOW_RULES.glob("*.md")}
    autonomous_names = {p.name for p in AUTONOMOUS_RULES.glob("*.md")}
    return sorted(workflow_names & autonomous_names - KNOWN_DIVERGENT)


@pytest.mark.parametrize("filename", _shared_rule_files(), ids=lambda f: f)
def test_shared_rule_file_is_identical(filename):
    workflow_file = WORKFLOW_RULES / filename
    autonomous_file = AUTONOMOUS_RULES / filename
    workflow_text = workflow_file.read_text()
    autonomous_text = autonomous_file.read_text()
    assert workflow_text == autonomous_text, (
        f"Shared rule file {filename} has drifted between blueprints. "
        f"Update both copies to match, or add the filename to "
        f"KNOWN_DIVERGENT if the difference is intentional."
    )
