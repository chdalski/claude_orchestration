"""Tests that rule files stay within the recommended line limit.

Long rule files degrade agent adherence — Claude is less
likely to follow every directive in a file that exceeds
~200 lines.  This test enforces a hard ceiling from
blueprint_contracts and reports the target in the failure
message so authors know what to aim for.
"""

import pytest

from blueprint_contracts import RULE_FILE_LENGTH_EXEMPTIONS, RULE_FILE_LINE_LIMIT
from conftest import RULES_DIR

pytestmark = pytest.mark.static

TARGET_LINES = 200  # documented recommendation


def _rule_files():
    if RULES_DIR.is_dir():
        yield from sorted(RULES_DIR.glob("*.md"))


@pytest.mark.parametrize(
    "filepath",
    list(_rule_files()),
    ids=lambda p: p.name,
)
def test_rule_file_within_line_limit(filepath):
    if filepath.name in RULE_FILE_LENGTH_EXEMPTIONS:
        pytest.skip(f"{filepath.name} is exempt (known tech debt — needs split)")
    line_count = len(filepath.read_text().splitlines())
    assert line_count <= RULE_FILE_LINE_LIMIT, (
        f"{filepath.name} has {line_count} lines "
        f"(limit: {RULE_FILE_LINE_LIMIT}, target: {TARGET_LINES}). "
        f"Split into focused files — long rule files degrade agent adherence."
    )
