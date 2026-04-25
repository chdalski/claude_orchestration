"""Single source of truth for all workflow blueprint behavioral contracts.

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
    ".claude/skills/ensure-ai-dirs",
    ".claude/skills/project-init",
    ".claude/skills/project-sanity",
    ".claude/skills/test-list",
    ".claude/workflows",
]

# Required files relative to blueprint root (outside .claude/)
REQUIRED_ROOT_FILES: list[str] = [
    ".claude/skills/ensure-ai-dirs/SKILL.md",
    ".claude/skills/ensure-ai-dirs/claude-md-template.md",
    ".claude/skills/project-init/SKILL.md",
    ".claude/skills/project-sanity/SKILL.md",
    ".claude/skills/project-sanity/codecov-sanity.md",
    ".claude/skills/ensure-ai-dirs/plan-format.md",
    ".claude/skills/ensure-ai-dirs/plan-review-checklist.md",
    ".claude/skills/project-init/project-context.md",
    ".claude/skills/test-list/SKILL.md",
    ".claude/workflows/CLAUDE.md",
    ".claude/workflows/direct-review.md",
    ".claude/workflows/develop-review-supervised.md",
    ".claude/workflows/develop-review-autonomous.md",
    ".claude/workflows/tdd-user-in-the-loop.md",
]

# Settings.json required configuration
REQUIRED_SETTINGS: dict[str, object] = {
    "plansDirectory": ".ai/plans/",
    "autoMemoryDirectory": ".ai/memory/",
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
    "plan-reviewer": "plan-reviewer.md",
    "reviewer": "reviewer.md",
    "test-engineer": "test-engineer.md",
    "security-engineer": "security-engineer.md",
    "test-list": "test-list.md",
}

# Agent tools — exact tool set for each agent
AGENT_TOOLS: dict[str, set[str]] = {
    "plan-reviewer": {
        "Read", "Glob", "Grep",
    },
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
    "test-list": {
        "Read",
    },
}

# Agent models — required model for each agent
AGENT_MODELS: dict[str, str] = {
    "plan-reviewer": "sonnet",
    "architect": "opus",
    "developer": "sonnet",
    "reviewer": "opus",
    "test-engineer": "sonnet",
    "security-engineer": "sonnet",
    "test-list": "sonnet",
}

# Rule file length — hard ceiling for the static test.
# The documented recommendation is 200 lines; this ceiling
# allows some buffer for code-heavy files (e.g., language
# idioms with inline examples) while still catching runaway
# growth.  The test message points to 200 as the target.
RULE_FILE_LINE_LIMIT: int = 250

# Rule files that exceed the line limit and need splitting.
# Each entry is a filename (not a path) in .claude/rules/.
# These are tracked as known tech debt — remove entries as
# files are split to comply with the limit.
RULE_FILE_LENGTH_EXEMPTIONS: set[str] = set()

DYNAMIC_CONTENT_ALLOWLIST: list[str] = [
    "YYYY-MM-DD",          # placeholder format strings
    "HH:MM:SS",            # placeholder format strings
    r"\d{4}-\d{2}-\d{2}",  # the pattern itself in contracts file
    r"\d{2}/\d{2}/\d{4}",
    r"\d{1,2}:\d{2}:\d{2}",
    r"version\s*[:=]\s*\d+\.\d+",
]
