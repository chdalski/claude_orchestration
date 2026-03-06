"""Tests that the blueprint complies with prompt caching constraints."""

import json
import re

import pytest

from blueprint_contracts import (
    DYNAMIC_CONTENT_ALLOWLIST,
    DYNAMIC_CONTENT_PATTERNS,
    MAX_HOOK_OUTPUT_CHARS,
)
from conftest import (
    AGENTS_DIR,
    CLAUDE_MD,
    KNOWLEDGE_BASE_DIR,
    KNOWLEDGE_EXTENSIONS_DIR,
    KNOWLEDGE_LANGUAGES_DIR,
    SETTINGS_FILE,
)

pytestmark = pytest.mark.static


def _static_files():
    """Yield all files that must be static (CLAUDE.md, agents, knowledge)."""
    yield CLAUDE_MD
    for f in sorted(AGENTS_DIR.glob("*.md")):
        yield f
    for d in [KNOWLEDGE_BASE_DIR, KNOWLEDGE_LANGUAGES_DIR, KNOWLEDGE_EXTENSIONS_DIR]:
        for f in sorted(d.glob("*.md")):
            yield f


def _line_has_dynamic_content(line: str) -> str | None:
    """Check if a line contains dynamic content. Returns the match or None."""
    for pattern in DYNAMIC_CONTENT_PATTERNS:
        match = re.search(pattern, line)
        if match:
            matched_text = match.group(0)
            # Check allowlist — skip if the line contains an allowlisted string
            for allowed in DYNAMIC_CONTENT_ALLOWLIST:
                if allowed in line:
                    return None
            return matched_text
    return None


@pytest.mark.parametrize(
    "filepath",
    list(_static_files()),
    ids=lambda p: str(p.relative_to(p.parents[3])),
)
def test_no_dynamic_content_in_static_files(filepath):
    content = filepath.read_text()
    violations = []
    for i, line in enumerate(content.splitlines(), 1):
        match = _line_has_dynamic_content(line)
        if match:
            violations.append(f"  line {i}: {match!r} in {line.strip()!r}")

    assert not violations, (
        f"Dynamic content found in {filepath.name}:\n" + "\n".join(violations)
    )


def test_hook_output_sizes_under_limit():
    settings = json.loads(SETTINGS_FILE.read_text())
    hooks = settings.get("hooks", {})

    violations = []
    for event, groups in hooks.items():
        for group_idx, group in enumerate(groups):
            for hook_idx, hook in enumerate(group.get("hooks", [])):
                if hook.get("type") != "command":
                    continue
                command = hook["command"]
                # Estimate output: extract echo string content
                # For commands that conditionally echo, take the longest echo
                echo_matches = re.findall(r'echo\s+["\']([^"\']*)["\']', command)
                for echo_content in echo_matches:
                    # Unescape \n to count actual output chars
                    unescaped = echo_content.replace("\\n", "\n")
                    if len(unescaped) > MAX_HOOK_OUTPUT_CHARS:
                        violations.append(
                            f"  {event}[{group_idx}].hooks[{hook_idx}]: "
                            f"echo output ~{len(unescaped)} chars > {MAX_HOOK_OUTPUT_CHARS}"
                        )

    assert not violations, (
        "Hook outputs exceed size limit:\n" + "\n".join(violations)
    )


def test_hooks_inject_via_echo_only():
    """Hooks must inject content via echo (messages), not file redirects."""
    settings = json.loads(SETTINGS_FILE.read_text())
    hooks = settings.get("hooks", {})

    violations = []
    for event, groups in hooks.items():
        for group_idx, group in enumerate(groups):
            for hook_idx, hook in enumerate(group.get("hooks", [])):
                if hook.get("type") != "command":
                    continue
                command = hook["command"]
                # Check for file redirects that would modify static files
                # Allow redirects in subshells or to /dev/null
                redirect_patterns = [
                    r'>\s*\.\s*claude/',         # redirect to .claude/
                    r'>>\s*\.\s*claude/',        # append to .claude/
                    r'>\s*CLAUDE\.md',           # redirect to CLAUDE.md
                    r'tee\s+.*\.claude/',        # tee to .claude/
                ]
                for rp in redirect_patterns:
                    if re.search(rp, command):
                        violations.append(
                            f"  {event}[{group_idx}].hooks[{hook_idx}]: "
                            f"file redirect detected (pattern: {rp})"
                        )

    assert not violations, (
        "Hooks must inject via echo only, not file redirects:\n"
        + "\n".join(violations)
    )


def test_no_conditional_tool_loading():
    """No defer_loading in settings (tool set must be fixed)."""
    settings_text = SETTINGS_FILE.read_text()
    assert "defer_loading" not in settings_text, (
        "settings.json must not use defer_loading (tool set must be fixed per caching rules)"
    )


def test_no_tool_set_changes_in_agent_files():
    """Agent files must not reference conditional tool loading."""
    for agent_file in sorted(AGENTS_DIR.glob("*.md")):
        content = agent_file.read_text()
        assert "defer_loading" not in content, (
            f"{agent_file.name} must not reference defer_loading"
        )
