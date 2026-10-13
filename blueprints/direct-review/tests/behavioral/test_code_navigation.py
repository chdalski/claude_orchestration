"""Behavioral test: the code-navigation rule makes the lead use LSP.

The fixture crate defines a free function `math::add` and a method
`Ledger::add`. Text search for "add" cannot separate their call sites,
so the question below has a precise answer only through the language
server. Probes showed the main session receives `LSP` as a deferred
tool when `ToolSearch` is present, so the rule must get the agent to
load it rather than fall back to grep.

Skips instead of failing when the environment cannot provide the tool:
no `rust-analyzer` binary on PATH, or the session's tool list has no
`LSP` (plugin not installed for this user).
"""

import json
import re
import shutil
from pathlib import Path

import pytest

from claude_agent_sdk import ClaudeAgentOptions, query
from claude_agent_sdk.types import AssistantMessage, SystemMessage, ToolUseBlock

from behavioral.conftest import BLUEPRINT_CLAUDE_DIR, NESTED_SESSION_ENV, ToolCallLog

pytestmark = pytest.mark.behavioral

RUST_FIXTURE_DIR = Path(__file__).parent.parent / "fixtures" / "rust_project"
RUST_LSP_PLUGIN = "rust-analyzer-lsp@claude-plugins-official"

# Override the lead's CLAUDE.md "delegate to specialized agents" instruction
DIRECT_MODE = (
    "Ignore any instructions about delegating to a team. "
    "You are being tested directly. Execute the request yourself."
)


@pytest.fixture
def rust_project(tmp_path: Path) -> Path:
    """Copy the Rust fixture and blueprint .claude/, enabling the Rust LSP plugin.

    The plugin entry mirrors what /project-init writes for a detected
    Rust project, so the test does not depend on user-level settings.
    """
    if shutil.which("rust-analyzer") is None:
        pytest.skip("rust-analyzer binary not on PATH")

    shutil.copytree(RUST_FIXTURE_DIR, tmp_path, dirs_exist_ok=True)
    dest_claude = tmp_path / ".claude"
    shutil.copytree(BLUEPRINT_CLAUDE_DIR, dest_claude)

    settings_path = dest_claude / "settings.json"
    settings = json.loads(settings_path.read_text())
    settings.setdefault("enabledPlugins", {})[RUST_LSP_PLUGIN] = True
    settings_path.write_text(json.dumps(settings, indent=2) + "\n")
    return tmp_path


async def run_session(project: Path, prompt: str, max_turns: int) -> tuple[list[str], ToolCallLog]:
    """Run one lead session; return the session's tool list and the tools it called."""
    tool_log = ToolCallLog()
    session_tools: list[str] = []
    # setting_sources=["project"]: the SDK loads no settings by default,
    # which would drop both the plugin entry and the blueprint rules
    # this test exercises.
    options = ClaudeAgentOptions(
        cwd=str(project),
        max_turns=max_turns,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
        setting_sources=["project"],
        system_prompt={"type": "preset", "preset": "claude_code", "append": DIRECT_MODE},
    )

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, SystemMessage) and message.subtype == "init":
            session_tools = list(message.data.get("tools", []))
        elif isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    tool_log.record(block.name, block.input or {})

    if "LSP" not in session_tools:
        pytest.skip(f"LSP tool not available in session (is {RUST_LSP_PLUGIN} installed?)")
    return session_tools, tool_log


@pytest.mark.asyncio
@pytest.mark.timeout(240)
async def test_lead_uses_lsp_for_call_sites(rust_project):
    """Asked for call sites of an ambiguous name, the lead queries LSP."""
    _, tool_log = await run_session(
        rust_project,
        "List every call site of the free function `add` defined in "
        "src/math.rs (not the `Ledger::add` method), as file and line. "
        "Do not modify any files. Be brief.",
        max_turns=10,
    )

    assert tool_log.has("LSP"), (
        "Lead answered a symbol-level question without the LSP tool; "
        f"tools used: {tool_log.tool_names}"
    )


@pytest.mark.asyncio
@pytest.mark.timeout(300)
async def test_lead_renames_through_lsp_references(rust_project):
    """Asked to rename a function whose name a method shares, the lead
    resolves the sites with LSP and edits them, never with a text rewrite.

    A prior session renamed a field with a regex script, which also hit
    unrelated values of the same name; the rule's rename section exists
    for that case.
    """
    _, tool_log = await run_session(
        rust_project,
        "Rename the free function `add` in src/math.rs to `sum` and update "
        "every caller. Leave the `Ledger::add` method unchanged. Make the "
        "change now, without a plan or review. Be brief.",
        max_turns=20,
    )

    rewrites = [
        r.input_data.get("command", "")
        for r in tool_log.calls_for("Bash")
        if re.search(r"\b(sed|perl)\b", r.input_data.get("command", ""))
    ]
    assert not rewrites, f"Lead renamed with a text rewrite: {rewrites}"
    assert tool_log.has("LSP"), (
        "Lead renamed a symbol without resolving its references through LSP; "
        f"tools used: {tool_log.tool_names}"
    )

    src = rust_project / "src"
    assert "pub fn sum(" in (src / "math.rs").read_text()
    assert "math::sum(acc, *v)" in (src / "lib.rs").read_text()
    ledger = (src / "ledger.rs").read_text()
    assert "pub fn add(&mut self" in ledger, "Ledger::add was renamed too"
    assert "math::sum(acc, *v)" in ledger
