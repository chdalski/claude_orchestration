"""Tests that lead instructions (CLAUDE.md) contain required contracts."""

import pytest

from conftest import CLAUDE_MD

pytestmark = pytest.mark.static


@pytest.fixture
def lead_instructions():
    return CLAUDE_MD.read_text()


# --- Plan progress ---


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


# --- Skill-output commits ---


def test_skill_output_commit_rule_exists(lead_instructions):
    """Lead instructions must define the skill-output commit rule."""
    assert "skill-output commits" in lead_instructions.lower(), (
        "CLAUDE.md must contain a 'Skill-Output Commits' section — "
        "this is the unified rule that allows the lead to commit "
        "files that skills explicitly name as outputs"
    )


def test_skill_output_commit_scoped_to_skill_outputs(lead_instructions):
    """The rule must limit commits to files a skill's SKILL.md names."""
    text = lead_instructions.lower()
    assert "`skill.md`" in text and "explicitly\nnames as outputs" in text, (
        "The skill-output commit rule must state that only files a "
        "skill's SKILL.md explicitly names as outputs may be committed "
        "by the lead — without this constraint, the lead can use the "
        "rule to bypass the reviewer for arbitrary files"
    )


def test_skill_output_commit_immediately_after(lead_instructions):
    """The rule must require committing immediately after the skill."""
    assert "immediately after" in lead_instructions.lower(), (
        "The skill-output commit rule must require committing "
        "immediately after the skill completes — deferred commits "
        "can accumulate unrelated changes under the skill-output "
        "exception"
    )


def test_skill_output_commit_not_general_permission(lead_instructions):
    """The rule must explicitly state it is not a general commit permission."""
    text = lead_instructions.lower()
    assert "not a general permission" in text, (
        "The skill-output commit rule must explicitly state that it "
        "is not a general permission to commit — without this "
        "guardrail, the lead can rationalize any commit as a "
        "'skill-like' operation"
    )


def test_skill_output_commit_removal_test(lead_instructions):
    """The rule must include the removal test for identifying skill outputs."""
    text = lead_instructions.lower()
    assert "removed the skill invocation" in text, (
        "The skill-output commit rule must include the removal test: "
        "'if you removed the skill invocation, would this file still "
        "need to exist?' — this gives the lead a bright-line test "
        "to distinguish skill infrastructure from project work"
    )


def test_skill_output_commit_covers_project_init(lead_instructions):
    """The rule must list /project-init as a covered skill."""
    assert "/project-init" in lead_instructions, (
        "The skill-output commit rule must explicitly list "
        "/project-init outputs — without this, the lead has no "
        "guidance on committing the project context files"
    )


def test_skill_output_commit_covers_ensure_plans_dir(lead_instructions):
    """The rule must list /ensure-plans-dir as a covered skill."""
    assert "/ensure-plans-dir" in lead_instructions, (
        "The skill-output commit rule must explicitly list "
        "/ensure-plans-dir outputs — without this, the format "
        "guide goes uncommitted between sessions"
    )


def test_skill_output_commit_covers_plan_progress(lead_instructions):
    """Plan progress updates must be listed under skill-output commits."""
    text = lead_instructions.lower()
    assert "plan progress" in text and "skill-output commit" in text, (
        "Plan progress updates must be documented as skill-output "
        "commits — they are outputs of the lead's plan-management "
        "instructions, not ad-hoc commits"
    )
