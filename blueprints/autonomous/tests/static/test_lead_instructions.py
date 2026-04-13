"""Tests that lead instructions (CLAUDE.md) contain required contracts."""

import re

import pytest

from conftest import CLAUDE_MD

pytestmark = pytest.mark.static


@pytest.fixture
def lead_instructions():
    return CLAUDE_MD.read_text()


def _extract_section(text, heading):
    """Extract content from ## heading to the next ## heading or EOF."""
    pattern = rf"^## {re.escape(heading)}\b.*?(?=\n## |\Z)"
    match = re.search(pattern, text, re.DOTALL | re.MULTILINE)
    return match.group(0) if match else ""


# --- Plan progress ---


def test_reviewer_owns_plan_updates_during_execution(lead_instructions):
    """Lead must delegate plan tracking to the reviewer during execution."""
    text = lead_instructions.lower()
    assert "reviewer" in text and "plan update" in text, (
        "CLAUDE.md must state that the reviewer updates the plan "
        "during execution — without this, no agent verifies scope "
        "completeness against the plan"
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


def test_skill_output_commit_covers_ensure_ai_dirs(lead_instructions):
    """The rule must list /ensure-ai-dirs as a covered skill."""
    assert "/ensure-ai-dirs" in lead_instructions, (
        "The skill-output commit rule must explicitly list "
        "/ensure-ai-dirs outputs — without this, the format "
        "guide goes uncommitted between sessions"
    )


def test_skill_output_commit_covers_plan_status(lead_instructions):
    """Plan status changes must be listed under skill-output commits."""
    text = lead_instructions.lower()
    assert "plan status" in text and "skill-output commit" in text, (
        "Plan status changes (Completed, Canceled) must be documented "
        "as skill-output commits — task-level updates are committed "
        "by the reviewer, but plan-level status is the lead's decision"
    )


# --- No standalone startup section ---


def test_no_startup_section(lead_instructions):
    """Lead instructions must not have a standalone Startup section.

    Startup procedures that rely on proactive execution before
    the user's first message are not enforced by Claude Code.
    Preconditions belong in the Clarification section where
    they fire on user interaction.
    """
    headings = re.findall(r"^## .+", lead_instructions, re.MULTILINE)
    startup_headings = [h for h in headings if "startup" in h.lower()]
    assert not startup_headings, (
        f"CLAUDE.md must not have a Startup section — "
        f"found: {startup_headings}. Preconditions belong in "
        f"the Clarification section"
    )


# --- Clarification preconditions ---


def test_project_init_in_clarification(lead_instructions):
    """Clarification section must include /project-init check.

    Without this, new projects lack the context all agents
    need to produce project-appropriate code.
    """
    clarification = _extract_section(lead_instructions, "Clarification")
    assert "/project-init" in clarification, (
        "The Clarification section must reference /project-init — "
        "without this precondition, new projects get no project "
        "context and agents default to generic patterns"
    )


def test_existing_plan_scan_in_clarification(lead_instructions):
    """Clarification section must instruct scanning for existing plans.

    Without this, incomplete work from prior sessions is
    silently ignored when the lead starts a new session.
    """
    clarification = _extract_section(
        lead_instructions, "Clarification"
    ).lower()
    assert "existing plan" in clarification, (
        "The Clarification section must instruct the lead to "
        "scan for existing plan files — without this, prior "
        "session work is silently ignored"
    )
