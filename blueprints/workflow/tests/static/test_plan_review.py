"""Tests for the plan-review severity contract: only open decisions block,
so the review cycle converges instead of adding precision every pass."""

import pytest

from conftest import ENSURE_AI_DIRS_SKILL

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
