"""Tests that the plans CLAUDE.md template is slim and points to plan-format.md.

The CLAUDE.md written to the plans directory must NOT embed the full plan
format guide — it should instruct agents to read plan-format.md on demand.
This prevents every agent that touches the plans directory from loading
the format guide into their context unnecessarily.
"""

import pytest

from conftest import CLAUDE_MD_TEMPLATE, PLAN_FORMAT_TEMPLATE

pytestmark = pytest.mark.static


def test_claude_md_template_references_plan_format():
    """The template must tell agents to read plan-format.md."""
    content = CLAUDE_MD_TEMPLATE.read_text()
    assert "plan-format.md" in content, (
        "claude-md-template.md must reference plan-format.md — "
        "without this pointer, agents writing plans won't know "
        "where to find the format guide"
    )


def test_claude_md_template_does_not_use_at_import():
    """The template must not use @import syntax to reference plan-format.md.

    @imports are eagerly expanded at session start, which would load the
    full format guide into every agent's context — defeating the purpose
    of the slim CLAUDE.md.
    """
    content = CLAUDE_MD_TEMPLATE.read_text()
    assert "@plan-format" not in content, (
        "claude-md-template.md must not use @plan-format imports — "
        "@imports are eagerly loaded by Claude Code, which would "
        "embed the full format guide in every agent's context"
    )


def test_claude_md_template_does_not_embed_format_guide():
    """The template must not contain plan format sections.

    If the template contains section headers from the plan format guide
    (Required Header, Required Sections, Conventions), it is embedding
    the format guide instead of pointing to it.
    """
    content = CLAUDE_MD_TEMPLATE.read_text()
    format_sections = ["Required Header", "Required Sections", "Conventions"]
    for section in format_sections:
        assert section not in content, (
            f"claude-md-template.md must not contain '{section}' — "
            f"this section belongs in plan-format.md, not the slim "
            f"CLAUDE.md template"
        )


def test_claude_md_template_is_slim():
    """The template should be significantly smaller than the format guide.

    A slim CLAUDE.md should be under 15 lines. The format guide is 150+
    lines. If the template is more than 20 lines, it is likely embedding
    content that belongs in plan-format.md.
    """
    content = CLAUDE_MD_TEMPLATE.read_text()
    line_count = len(content.strip().splitlines())
    assert line_count <= 20, (
        f"claude-md-template.md is {line_count} lines — expected under "
        f"20. The template should be a slim pointer to plan-format.md, "
        f"not a copy of the format guide"
    )
