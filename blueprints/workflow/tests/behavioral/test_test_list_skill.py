"""Behavioral test for the /test-list skill.

Invokes the test-list subagent with a real example mapping
for a concrete target framework (Vitest / TypeScript) and
validates the agent's framework-specific Test Case List
output:

- A Vitest describe(...) block wrapping the cases
- At least 3 it.todo(...) pending placeholders
- The first case handles the simplest scenario (empty / zero input)
- No imports in the list (the implementor adds those when saving)
- Pending placeholders only — no executable-test patterns
- A Metadata block follows with Feature / Target / etc.

The agent's Output Format spec also promises an Advanced
Features marker in the metadata. That is checked softly
(warning, not failure) because LLM output occasionally
omits it; the describe + it.todo contract is the core
regression gate.
"""

import re
import warnings

import pytest

from claude_agent_sdk import ClaudeAgentOptions, query
from claude_agent_sdk.types import (
    AssistantMessage,
    TextBlock,
    ToolResultBlock,
    UserMessage,
)

from behavioral.conftest import NESTED_SESSION_ENV

pytestmark = pytest.mark.behavioral

# Override the lead's CLAUDE.md "clarify first / route to team" posture —
# this is an automated test; just execute the request.
DIRECT_MODE = (
    "This is an automated behavioral test. Do not clarify, do not "
    "propose a workflow, do not create a plan, and do not ask the "
    "user anything. Execute the request exactly as given."
)

EXAMPLE_MAPPING = """Story: As a user, I want to add comma-separated
numbers so I can compute simple sums.

Rules:
1. An empty string returns 0.
2. A single number returns itself.
3. Two numbers separated by a comma return their sum.
4. Any number of comma-separated numbers returns their sum.

Examples:
Rule 1: "" -> 0
Rule 2: "1" -> 1; "42" -> 42
Rule 3: "1,2" -> 3; "10,20" -> 30
Rule 4: "1,2,3" -> 6; "1,2,3,4,5" -> 15

Open questions:
- Should whitespace around numbers be allowed (e.g. "1, 2")?
"""

PROMPT = (
    'Launch the test-list subagent via the Agent tool with '
    'subagent_type: "test-list". Pass it this launch prompt '
    "verbatim:\n\n"
    "---\n"
    "Feature name: String Calculator\n"
    "Target language/framework: Vitest / TypeScript\n"
    "Target test file path: src/string-calculator.spec.ts\n"
    "Target implementation file path: src/string-calculator.ts\n\n"
    "Example mapping content:\n"
    f"{EXAMPLE_MAPPING}"
    "---\n\n"
    "After the subagent returns its result, quote the subagent's "
    "complete final message verbatim inside a fenced code block "
    "as your response. Do not summarize, do not add commentary, "
    "do not ask for user confirmation."
)


@pytest.mark.asyncio
@pytest.mark.timeout(300)
async def test_test_list_agent_produces_conforming_list(fixture_project):
    """Agent produces a structurally valid minimum required test list."""
    options = ClaudeAgentOptions(
        cwd=str(fixture_project),
        max_turns=8,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
        # Load project-level settings so the subagents defined in
        # .claude/agents/ (including test-list) are registered with
        # the Agent tool; without this the SDK only exposes built-ins.
        setting_sources=["project"],
        system_prompt={
            "type": "preset",
            "preset": "claude_code",
            "append": DIRECT_MODE,
        },
    )

    # Capture both the lead's relayed text and the raw subagent
    # output (returned to the lead as a ToolResultBlock). Asserting
    # against the union of both avoids false negatives when the
    # lead summarizes or truncates what it quotes back.
    texts: list[str] = []
    async for message in query(prompt=PROMPT, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    texts.append(block.text)
        elif isinstance(message, UserMessage):
            for block in message.content:
                if isinstance(block, ToolResultBlock):
                    content = block.content
                    if isinstance(content, str):
                        texts.append(content)
                    elif isinstance(content, list):
                        for item in content:
                            if (
                                isinstance(item, dict)
                                and item.get("type") == "text"
                            ):
                                texts.append(item.get("text", ""))

    output = "\n".join(texts)
    assert output.strip(), "Agent session returned no text output"
    flat = re.sub(r"\s+", " ", output)

    # --- Vitest describe(...) block present ---
    assert "describe(" in output, (
        f"Expected a Vitest describe(...) block wrapping the test "
        f"cases (target was Vitest / TypeScript). "
        f"Full output:\n{output}"
    )

    # --- At least 3 it.todo(...) placeholders ---
    todo_descs = re.findall(
        r"it\.todo\s*\(\s*['\"]([^'\"]+)['\"]",
        output,
    )
    assert len(todo_descs) >= 3, (
        f"Expected at least 3 it.todo(...) placeholders; got "
        f"{len(todo_descs)}. Full output:\n{output}"
    )

    # --- First placeholder handles the simplest case (empty/zero) ---
    first = todo_descs[0].lower()
    assert (
        "empty" in first
        or "zero" in first
        or re.search(r"\b0\b", first)
    ), (
        f"First it.todo(...) should handle empty/zero input "
        f"(simple → complex ordering); got: {todo_descs[0]!r}. "
        f"Full output:\n{output}"
    )

    # --- No imports in the test case list ---
    # The user's design: the list is a ready-to-embed block without
    # import statements (the implementor adds them when saving to a
    # test file). An import leaks implementation-file concerns into
    # the list.
    assert 'import ' not in output or 'from "vitest"' not in output, (
        "Test case list should omit imports (e.g. `import { describe, "
        "it } from \"vitest\"`) — the implementor adds those when "
        f"saving the list to a file. Full output:\n{output}"
    )

    # --- Placeholders only: no executable-test patterns ---
    forbidden = [
        r"\bexpect\([^)]*\)\s*\.",       # Vitest/Jest: expect(x).toBe(...)
        r"\bit\s*\(\s*['\"][^'\"]*['\"]\s*,",   # it("...", fn) with body
        r"\btest\s*\(\s*['\"][^'\"]*['\"]\s*,", # test("...", fn) with body
        r"\bassertEqual\(",              # unittest
        r"^\s*assert\s+\w+\s*[=!<>]=",   # Python `assert x == y`
    ]
    impl_hits = [
        pat for pat in forbidden
        if re.search(pat, output, re.MULTILINE)
    ]
    assert not impl_hits, (
        f"Output contains executable-test patterns {impl_hits}; "
        f"only pending placeholders are allowed. Full output:\n{output}"
    )

    # --- Metadata block present (Feature + Target) ---
    assert "Feature:" in flat and "Target:" in flat, (
        "Expected Metadata block with 'Feature:' and 'Target:' "
        f"fields. Full output:\n{output}"
    )

    # --- Soft check for Advanced Features marker ---
    if "advanced" not in flat.lower() and "deferred" not in flat.lower():
        warnings.warn(
            "Metadata missing 'Advanced Features' deferral marker"
        )
