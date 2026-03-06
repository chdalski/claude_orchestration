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
    ".claude/rules",
    ".claude/templates",
    ".claude/workflows",
]

# Required files relative to blueprint root (outside .claude/)
REQUIRED_ROOT_FILES: list[str] = [
    ".claude/templates/plan-format.md",
    ".claude/workflows/CLAUDE.md",
    ".claude/workflows/solo.md",
]

# Settings.json required configuration
REQUIRED_SETTINGS: dict[str, object] = {
    "plansDirectory": ".ai/plans/",
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
    "Architect": "architect.md",
    "Auditor": "auditor.md",
    "Committer": "committer.md",
    "Plan Init": "plan-init.md",
    "Developer": "developer.md",
    "Reviewer": "reviewer.md",
    "Test Engineer": "test-engineer.md",
    "Security Engineer": "security-engineer.md",
}

# Agent tools — exact tool set for each agent
AGENT_TOOLS: dict[str, set[str]] = {
    "Architect": {
        "Read", "Glob", "Grep", "Write", "Edit",
        "SendMessage", "TaskCreate", "TaskUpdate",
        "TaskList", "TaskGet",
    },
    "Auditor": {"Read", "Glob", "Grep", "SendMessage"},
    "Committer": {"Read", "Glob", "Bash", "SendMessage"},
    "Plan Init": {"Read", "Glob", "Write", "Bash", "SendMessage"},
    "Developer": {
        "Read", "Write", "Edit", "Bash", "Glob", "Grep",
        "WebSearch", "WebFetch", "SendMessage", "TaskUpdate",
        "TaskList", "TaskGet",
    },
    "Reviewer": {
        "Read", "Glob", "Grep", "Bash", "SendMessage",
        "TaskList", "TaskGet",
    },
    "Test Engineer": {
        "Read", "Glob", "Grep", "Bash", "SendMessage",
        "TaskList", "TaskGet",
    },
    "Security Engineer": {
        "Read", "Glob", "Grep", "Bash", "SendMessage",
        "TaskList", "TaskGet",
    },
}

# Agent models — required model for each agent
AGENT_MODELS: dict[str, str] = {
    "Architect": "opus",
    "Auditor": "haiku",
    "Committer": "haiku",
    "Plan Init": "haiku",
    "Developer": "sonnet",
    "Reviewer": "sonnet",
    "Test Engineer": "sonnet",
    "Security Engineer": "sonnet",
}

DYNAMIC_CONTENT_ALLOWLIST: list[str] = [
    "YYYY-MM-DD",          # placeholder format strings
    "HH:MM:SS",            # placeholder format strings
    r"\d{4}-\d{2}-\d{2}",  # the pattern itself in contracts file
    r"\d{2}/\d{2}/\d{4}",
    r"\d{1,2}:\d{2}:\d{2}",
    r"version\s*[:=]\s*\d+\.\d+",
]
