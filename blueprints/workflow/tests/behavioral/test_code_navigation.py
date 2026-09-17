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
import shutil
from pathlib import Path

import pytest

from claude_agent_sdk import ClaudeAgentOptions, query
from claude_agent_sdk.types import AssistantMessage, SystemMessage, ToolUseBlock

from behavioral.conftest import BLUEPRINT_CLAUDE_DIR, NESTED_SESSION_ENV, ToolCallLog

pytestmark = pytest.mark.behavioral

RUST_FIXTURE_DIR = Path(__file__).parent.parent / "fixtures" / "rust_project"
RUST_LSP_PLUGIN = "rust-analyzer-lsp@claude-plugins-official"

# Override the lead's CLAUDE.md "route work to specialized agents" posture
DIRECT_MODE = (
    "Ignore any instructions about routing work to a team. "
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


@pytest.mark.asyncio
@pytest.mark.timeout(240)
async def test_lead_uses_lsp_for_call_sites(rust_project):
    """Asked for call sites of an ambiguous name, the lead queries LSP."""
    tool_log = ToolCallLog()
    session_tools: list[str] = []
    # setting_sources=["project"]: the SDK loads no settings by default,
    # which would drop both the plugin entry and the blueprint rules
    # this test exercises.
    options = ClaudeAgentOptions(
        cwd=str(rust_project),
        max_turns=10,
        env=NESTED_SESSION_ENV,
        permission_mode="bypassPermissions",
        setting_sources=["project"],
        system_prompt={"type": "preset", "preset": "claude_code", "append": DIRECT_MODE},
    )
    prompt = (
        "List every call site of the free function `add` defined in "
        "src/math.rs (not the `Ledger::add` method), as file and line. "
        "Do not modify any files. Be brief."
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

    assert tool_log.has("LSP"), (
        "Lead answered a symbol-level question without the LSP tool; "
        f"tools used: {tool_log.tool_names}"
    )
