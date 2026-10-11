"""Tests for the design-advisor contracts: every code-changing plan rests on
its report, adopted refactors pin behavior first, and the Reviewer honors
declined proposals."""

import re

import pytest

from conftest import (
    AGENTS_DIR,
    CLAUDE_MD,
    ENSURE_AI_DIRS_SKILL,
    PLAN_FORMAT_TEMPLATE,
    WORKFLOWS_DIR,
)

pytestmark = pytest.mark.static


def _flat(text):
    return " ".join(text.split())


def _extract_section(text, heading):
    """Extract content from ## heading to the next ## heading or EOF."""
    pattern = rf"^## {re.escape(heading)}\b.*?(?=\n## |\Z)"
    match = re.search(pattern, text, re.DOTALL | re.MULTILINE)
    return match.group(0) if match else ""


def _step_number(section, title):
    """Return the number of the numbered step whose bold title starts with title."""
    match = re.search(rf"^(\d+)\.\s+\*\*{re.escape(title)}", section, re.MULTILINE)
    assert match, f"Missing numbered step starting with '**{title}'"
    return int(match.group(1))


def _step_text(section, title):
    """Return the numbered step whose bold title starts with title, whitespace-flattened."""
    pattern = rf"^\d+\.\s+\*\*{re.escape(title)}.*?(?=^\d+\.\s+\*\*|\Z)"
    match = re.search(pattern, section, re.DOTALL | re.MULTILINE)
    assert match, f"Missing numbered step starting with '**{title}'"
    return _flat(match.group(0))


@pytest.fixture
def planning():
    return _extract_section(CLAUDE_MD.read_text(), "Planning")


def test_design_settled_before_plan_is_written(planning):
    """Every code-changing plan rests on a design-advisor report, taken
    before the plan exists — a proposal taken after review restarts it."""
    assert _step_number(planning, "Settle the design") < _step_number(planning, "Write the plan")
    step = _step_text(planning, "Settle the design")
    assert "`design-advisor`" in step and "no `name`" in step
    assert "Every plan that changes code" in step
    assert "Do not skip it for a small change" in step


def test_change_of_approach_returns_to_design(planning):
    """A changed approach invalidates the report the plan rests on."""
    design = _step_number(planning, "Settle the design")
    present = _step_text(planning, "Present the plan to the user")
    assert f"A change of approach goes back to step {design}" in present


def test_test_list_entry_path_keeps_design_step():
    """The /test-list path writes the plan too, so it must not skip the design."""
    test_list_path = _extract_section(CLAUDE_MD.read_text(), "When the User Invokes /test-list")
    assert "Settle the design and write the plan" in _flat(test_list_path)


def test_refactor_tasks_pin_behavior_with_tests():
    """A refactor task keeps its pinning tests' assertions unchanged, and
    the plan-reviewer checks for it."""
    assert "pass with their assertions unchanged" in _flat(PLAN_FORMAT_TEMPLATE.read_text())
    checklist = ENSURE_AI_DIRS_SKILL / "plan-review-checklist.md"
    assert "behavior-preserving refactor task" in _flat(checklist.read_text())


def test_reviewer_honors_refactors_and_declined_proposals():
    """Pinning tests are proportionate coverage for a refactor, and a
    declined proposal recorded in Decisions is not a finding."""
    reviewer = _flat((AGENTS_DIR / "reviewer.md").read_text())
    assert "A behavior-preserving refactor adds no behavior" in reviewer
    assert "read the plan's Decisions section" in reviewer


@pytest.mark.parametrize(
    "workflow",
    sorted(p.name for p in WORKFLOWS_DIR.glob("*.md") if p.name != "CLAUDE.md"),
)
def test_review_request_carries_decisions(workflow):
    """The Reviewer can honor a declined proposal only if the review
    request carries the plan's Decisions."""
    text = _flat((WORKFLOWS_DIR / workflow).read_text())
    assert "Decisions" in text, f"{workflow} must pass the plan's Decisions to the Reviewer"


def test_tdd_handles_tasks_without_behavior():
    """Pinning-test and refactor tasks have no Red phase."""
    tdd = _flat((WORKFLOWS_DIR / "tdd-user-in-the-loop.md").read_text())
    assert "Tasks that add no behavior" in tdd
