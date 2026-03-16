"""Tests that lead instructions (CLAUDE.md) contain required contracts."""

import pytest

from conftest import CLAUDE_MD

pytestmark = pytest.mark.static


@pytest.fixture
def lead_instructions():
    return CLAUDE_MD.read_text()


def test_plan_progress_commit_after_reviewer_approval(lead_instructions):
    """Lead must commit plan updates after each task completion."""
    assert "commit the plan update" in lead_instructions.lower(), (
        "CLAUDE.md must instruct the lead to commit plan progress "
        "after reviewer approval — without this, plan updates are "
        "lost on session crash"
    )


def test_plan_completion_commit(lead_instructions):
    """Lead must commit plan status when marking a plan complete."""
    assert "mark plan complete" in lead_instructions.lower(), (
        "CLAUDE.md must instruct the lead to commit plan completion "
        "status — without this, completed plans appear incomplete "
        "on session resume"
    )


def test_lead_plan_commit_exception_documented(lead_instructions):
    """Lead's exception to 'reviewer makes all commits' must be documented."""
    assert "docs" in lead_instructions and "plan" in lead_instructions.lower(), (
        "CLAUDE.md must document that plan progress commits (docs prefix) "
        "are the lead's responsibility, not the reviewer's"
    )
