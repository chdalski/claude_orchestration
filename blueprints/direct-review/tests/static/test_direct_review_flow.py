"""Tests for the direct-review contracts: advise by default, implement on
explicit request, security pre/post gates, and a user review per task."""

import re

import pytest

from blueprint_contracts import AGENT_FILES
from conftest import AGENTS_DIR, CLAUDE_DIR, CLAUDE_MD, RULES_DIR

pytestmark = pytest.mark.static


@pytest.fixture
def lead_instructions():
    return CLAUDE_MD.read_text()


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


# --- Structure ---


def test_no_workflows_directory():
    """The single flow lives in the lead's CLAUDE.md, not a workflows/ dir."""
    assert not (CLAUDE_DIR / "workflows").exists(), (
        "direct-review has one flow — a workflows/ directory implies "
        "a workflow menu the lead would try to present"
    )


def test_agents_directory_has_exactly_contract_agents():
    """No developer or test-engineer agent — the lead implements."""
    present = {p.name for p in AGENTS_DIR.glob("*.md")}
    assert present == set(AGENT_FILES.values()), (
        f"agents/ must contain exactly {sorted(AGENT_FILES.values())}, "
        f"found {sorted(present)}"
    )


@pytest.mark.parametrize("filename", sorted(AGENT_FILES.values()))
def test_agents_name_no_workflow(filename):
    """Agent files define role only — no workflow names (agent-design rule)."""
    text = (AGENTS_DIR / filename).read_text()
    for term in ("Security-Hybrid", "Reviewer-only", "Develop-Review", "Direct-Review"):
        assert term not in text, f"{filename} names workflow path '{term}'"


# --- Advise mode ---


def test_advise_mode_is_default(lead_instructions):
    role = _extract_section(lead_instructions, "Your Role").lower()
    assert "advise mode (default)" in role
    assert "only when the user\n   explicitly asks you to implement" in role


def test_advise_mode_forbids_edits(lead_instructions):
    advise = _extract_section(lead_instructions, "Advise Mode").lower()
    assert "do not edit project files" in advise


def test_imperative_commands_do_not_authorize_edits(lead_instructions):
    clarification = _extract_section(lead_instructions, "Clarification").lower()
    assert "does not authorize edits" in clarification


def test_advise_mode_security_consultation_is_stateless(lead_instructions):
    """A named Agent call spawns a teammate; advise-mode consults must not."""
    advise = _extract_section(lead_instructions, "Advise Mode")
    assert "security-engineer" in advise and "no `name`" in advise


# --- Implement mode ---


def test_implementation_step_order(lead_instructions):
    """Pre-gate before implementing; post-gate before review; user review
    before commit; wait for the user's go last."""
    section = _extract_section(lead_instructions, "Implementing a Task")
    order = [
        _step_number(section, "Spawn the task's teammates"),
        _step_number(section, "Security pre-gate"),
        _step_number(section, "Implement"),
        _step_number(section, "Security post-gate"),
        _step_number(section, "Reviewer handoff"),
        _step_number(section, "User review"),
        _step_number(section, "Commit"),
        _step_number(section, "Shut down the teammates"),
        _step_number(section, "Wait for the user's go"),
    ]
    assert order == sorted(order), f"Implementation steps out of order: {order}"


def test_user_review_has_no_exceptions(lead_instructions):
    section = _extract_section(lead_instructions, "Implementing a Task").lower()
    assert "there are no exceptions" in section
    assert "never chain tasks" in section


def test_reviewer_handoff_states_both_security_gates(lead_instructions):
    section = _extract_section(lead_instructions, "Implementing a Task")
    flat = " ".join(section.split())
    assert (
        "security-engineer pre-implementation signed off; "
        "security-engineer post-implementation signed off"
    ) in flat


# --- Risk assessment ---


def test_risk_assessment_defines_three_paths():
    text = (RULES_DIR / "risk-assessment.md").read_text()
    for heading in ("## Reviewer-Only", "## Security-Hybrid", "## Escalate to the User"):
        assert heading in text, f"risk-assessment.md missing '{heading}'"


def test_escalation_requires_explicit_user_choice():
    section = _extract_section(
        (RULES_DIR / "risk-assessment.md").read_text(), "Escalate to the User"
    )
    assert "Proceed with Security-Hybrid anyway" in section
    assert "Handle the task outside this blueprint" in section
    assert "make no implementation edit" in section
