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
    ".claude/skills",
    ".claude/skills/ensure-plans-dir",
    ".claude/skills/project-init",
    ".claude/skills/project-sanity",
    ".claude/templates",
    ".claude/workflows",
]

# Required files relative to blueprint root (outside .claude/)
REQUIRED_ROOT_FILES: list[str] = [
    ".claude/skills/ensure-plans-dir/SKILL.md",
    ".claude/skills/project-init/SKILL.md",
    ".claude/skills/project-sanity/SKILL.md",
    ".claude/skills/project-sanity/codecov-sanity.md",
    ".claude/templates/plan-format.md",
    ".claude/templates/project-context.md",
    ".claude/workflows/CLAUDE.md",
    ".claude/workflows/direct-review.md",
    ".claude/workflows/develop-review-supervised.md",
    ".claude/workflows/develop-review-autonomous.md",
    ".claude/workflows/tdd-user-in-the-loop.md",
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
    "architect": "architect.md",
    "developer": "developer.md",
    "reviewer": "reviewer.md",
    "test-engineer": "test-engineer.md",
    "security-engineer": "security-engineer.md",
}

# Agent tools — exact tool set for each agent
AGENT_TOOLS: dict[str, set[str]] = {
    "architect": {
        "Read", "Glob", "Grep", "Write", "Edit",
        "SendMessage", "TaskCreate", "TaskUpdate",
        "TaskList", "TaskGet",
    },
    "developer": {
        "Read", "Write", "Edit", "Bash", "Glob", "Grep",
        "WebSearch", "WebFetch", "SendMessage",
        "TaskList", "TaskGet",
    },
    "reviewer": {
        "Read", "Glob", "Grep", "Bash", "SendMessage",
    },
    "test-engineer": {
        "Read", "Glob", "Grep", "Bash", "SendMessage",
        "TaskList", "TaskGet",
    },
    "security-engineer": {
        "Read", "Glob", "Grep", "Bash", "SendMessage",
        "TaskList", "TaskGet",
    },
}

# Agent models — required model for each agent
AGENT_MODELS: dict[str, str] = {
    "architect": "opus",
    "developer": "sonnet",
    "reviewer": "opus",
    "test-engineer": "sonnet",
    "security-engineer": "sonnet",
}

DYNAMIC_CONTENT_ALLOWLIST: list[str] = [
    "YYYY-MM-DD",          # placeholder format strings
    "HH:MM:SS",            # placeholder format strings
    r"\d{4}-\d{2}-\d{2}",  # the pattern itself in contracts file
    r"\d{2}/\d{2}/\d{4}",
    r"\d{1,2}:\d{2}:\d{2}",
    r"version\s*[:=]\s*\d+\.\d+",
]
