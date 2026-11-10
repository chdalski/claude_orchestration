"""Tests for the plan-review severity contract: only open decisions block,
so the review cycle converges instead of adding precision every pass."""

import re

import pytest

from conftest import AGENTS_DIR, CLAUDE_MD, ENSURE_AI_DIRS_SKILL

pytestmark = pytest.mark.static

PLAN_REVIEW_CHECKLIST = ENSURE_AI_DIRS_SKILL / "plan-review-checklist.md"


def test_checklist_blocks_unclear_criteria_only_on_open_decisions():
    """An unclear criterion blocks only when two readings deliver different results."""
    content = " ".join(PLAN_REVIEW_CHECKLIST.read_text().split())
    assert "two readings" in content and "drop the finding" in content, (
        "plan-review-checklist.md must block an unclear criterion only "
        "when the reviewer can name two readings that deliver different "
        "results — precision added for readings the code already settles "
        "is new text every fresh pass searches again, and the cycle stops "
        "converging"
    )


@pytest.fixture
def lead_instructions():
    return CLAUDE_MD.read_text()


# --- Focused first pass, diff-only follow-up passes ---


def _focus_sections(checklist):
    """Map each focus in the checklist's Focus table to its section numbers."""
    focus_table = checklist.split("## Focus", 1)[1].split("\n## ", 1)[0]
    rows = re.findall(r"^\| `([a-z]+)` \| ([\d, ]+) \|", focus_table, re.MULTILINE)
    return {focus: [int(n) for n in numbers.split(",")] for focus, numbers in rows}


def test_checklist_focus_covers_every_section_once():
    """Each checklist section belongs to exactly one first-pass focus."""
    checklist = PLAN_REVIEW_CHECKLIST.read_text()
    sections = [int(n) for n in re.findall(r"^## (\d+)\. ", checklist, re.MULTILINE)]
    assigned = [n for numbers in _focus_sections(checklist).values() for n in numbers]
    assert sections and sorted(assigned) == sorted(sections), (
        "every plan-review-checklist.md section must belong to exactly one "
        "focus — a section no focus covers goes unreviewed, since "
        "follow-up passes review only the diff of each revision"
    )


def test_lead_instructions_launch_one_reviewer_per_focus(lead_instructions):
    """The first pass launches a plan-reviewer for every focus."""
    focuses = _focus_sections(PLAN_REVIEW_CHECKLIST.read_text())
    missing = [focus for focus in focuses if f"`{focus}`" not in lead_instructions]
    assert focuses and not missing, (
        f"CLAUDE.md must launch one first-pass plan-reviewer per checklist "
        f"focus — missing: {missing}. A focus without a reviewer leaves its "
        f"sections unreviewed"
    )


def test_lead_instructions_pass_revision_diff_to_follow_up_pass(lead_instructions):
    """Follow-up passes review the diff of the revision."""
    assert "diff -u" in lead_instructions, (
        "CLAUDE.md must have the lead pass the revision's diff to the "
        "follow-up pass — only the lead holds the pre-revision copy, and "
        "without the diff the plan-reviewer cannot tell changed text from "
        "text earlier passes reviewed"
    )


def test_plan_reviewer_defines_follow_up_passes():
    """The plan-reviewer limits a follow-up pass to the revision."""
    content = (AGENTS_DIR / "plan-reviewer.md").read_text()
    assert "## Follow-up Passes" in content, (
        "plan-reviewer.md must define how a follow-up pass works — without "
        "it, every pass reviews the whole plan again and finds different "
        "points each time, so the review cycle does not converge"
    )
