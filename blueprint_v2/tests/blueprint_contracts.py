"""Single source of truth for all blueprint_v2 behavioral contracts.

When the blueprint changes, update this file and the tests follow.
"""

# Required file structure — files inside .claude/
REQUIRED_CLAUDE_FILES: list[str] = [
    "CLAUDE.md",
    "settings.json",
]

# Required directories relative to blueprint root
REQUIRED_DIRECTORIES: list[str] = [
    ".claude",
    ".claude/agents",
    ".claude/workflows",
    ".ai/plans",
]

# Required files relative to blueprint root (outside .claude/)
REQUIRED_ROOT_FILES: list[str] = [
    ".ai/plans/CLAUDE.md",
    ".claude/workflows/CLAUDE.md",
]

# Settings.json required configuration
REQUIRED_SETTINGS: dict[str, object] = {
    "plansDirectory": ".ai/plans/",
}

REQUIRED_SETTINGS_NESTED: dict[str, object] = {
    "permissions.defaultMode": "plan",
}

# Caching compliance — patterns that indicate dynamic content
DYNAMIC_CONTENT_PATTERNS: list[str] = [
    r"\d{4}-\d{2}-\d{2}",          # dates (YYYY-MM-DD)
    r"\d{2}/\d{2}/\d{4}",          # dates (MM/DD/YYYY)
    r"\d{1,2}:\d{2}:\d{2}",        # timestamps (HH:MM:SS)
    r"counter\s*[:=]\s*\d+",       # counters
    r"version\s*[:=]\s*\d+\.\d+",  # version numbers used as state
]

# Allowlist for date-like patterns that are actually static content
# Agent definitions — filename must match exactly
AGENT_FILES: dict[str, str] = {
    "Auditor": "auditor.md",
    "Committer": "committer.md",
}

# Agent tools — exact tool set for each agent
AGENT_TOOLS: dict[str, set[str]] = {
    "Auditor": {"Read", "Glob", "Grep", "SendMessage"},
    "Committer": {"Read", "Glob", "Bash", "SendMessage"},
}

# Agent models — required model for each agent
AGENT_MODELS: dict[str, str] = {
    "Auditor": "haiku",
    "Committer": "haiku",
}

DYNAMIC_CONTENT_ALLOWLIST: list[str] = [
    "YYYY-MM-DD",          # placeholder format strings
    "HH:MM:SS",            # placeholder format strings
    r"\d{4}-\d{2}-\d{2}",  # the pattern itself in contracts file
    r"\d{2}/\d{2}/\d{4}",
    r"\d{1,2}:\d{2}:\d{2}",
    r"version\s*[:=]\s*\d+\.\d+",
]
