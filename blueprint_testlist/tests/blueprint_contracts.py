"""Single source of truth for all blueprint behavioral contracts.

When the blueprint changes, update this file and the tests follow.
"""

# Agent name → filename mapping
AGENT_FILES: dict[str, str] = {
    "Architect": "architect.md",
    "Developer": "developer.md",
    "Test Engineer": "test-engineer.md",
    "Security Engineer": "security-engineer.md",
    "Reviewer": "reviewer.md",
}

# Agent name → exact tool set (from frontmatter)
AGENT_TOOLS: dict[str, set[str]] = {
    "Architect": {
        "Read", "Write", "Edit", "Glob", "Grep", "Bash",
        "Task", "SendMessage", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet",
    },
    "Developer": {
        "Read", "Write", "Edit", "Bash", "Glob", "Grep",
        "WebSearch", "WebFetch", "SendMessage", "TaskUpdate", "TaskList", "TaskGet",
    },
    "Test Engineer": {
        "Read", "Glob", "Grep", "Bash",
        "SendMessage", "TaskUpdate", "TaskList", "TaskGet",
    },
    "Security Engineer": {
        "Read", "Glob", "Grep", "Bash",
        "SendMessage", "TaskUpdate", "TaskList", "TaskGet",
    },
    "Reviewer": {
        "Read", "Glob", "Grep", "Bash",
        "SendMessage", "TaskUpdate", "TaskList", "TaskGet",
    },
}

# Agent name → model
AGENT_MODELS: dict[str, str] = {
    "Architect": "sonnet",
    "Developer": "sonnet",
    "Test Engineer": "sonnet",
    "Security Engineer": "sonnet",
    "Reviewer": "opus",
}

# Agent name → color
AGENT_COLORS: dict[str, str] = {
    "Architect": "yellow",
    "Developer": "green",
    "Test Engineer": "blue",
    "Security Engineer": "red",
    "Reviewer": "purple",
}

# Advisory agents — lack Write and Edit tools
AGENTS_WITHOUT_WRITE: set[str] = {"Test Engineer", "Security Engineer", "Reviewer"}

# Agents that cannot create tasks (only Architect has TaskCreate)
AGENTS_WITHOUT_TASK_CREATE: set[str] = {
    "Developer", "Test Engineer", "Security Engineer", "Reviewer",
}

# Lead (CLAUDE.md) forbidden tools
LEAD_FORBIDDEN_TOOLS: set[str] = {"Edit", "Write"}

# Hook constraints
MAX_HOOK_OUTPUT_CHARS = 2000
HOOK_EVENTS_REQUIRED: set[str] = {"SessionStart", "PreToolUse", "PreCompact"}

# Required file structure
REQUIRED_AGENT_FILES: list[str] = [
    "architect.md",
    "developer.md",
    "test-engineer.md",
    "security-engineer.md",
    "reviewer.md",
]

REQUIRED_KNOWLEDGE_BASE: list[str] = [
    "principles.md",
    "architecture.md",
    "data.md",
    "functional.md",
    "testing.md",
    "security.md",
    "code-mass.md",
    "documentation.md",
    "caching.md",
]

REQUIRED_KNOWLEDGE_LANGUAGES: list[str] = [
    "typescript.md",
    "python.md",
    "go.md",
    "rust.md",
]

REQUIRED_PRACTICES: list[str] = [
    "test-list.md",
    "conventional-commits.md",
]

REQUIRED_TEMPLATES: list[str] = [
    "commit-message.md",
]

REQUIRED_TOP_LEVEL_FILES: list[str] = [
    "settings.json",
    "CLAUDE.md",
    "config.json",
]

REQUIRED_DIRECTORIES: list[str] = [
    "agents",
    "knowledge",
    "knowledge/base",
    "knowledge/languages",
    "knowledge/extensions",
    "practices",
    "templates",
]

# Caching compliance — patterns that indicate dynamic content
DYNAMIC_CONTENT_PATTERNS: list[str] = [
    r"\d{4}-\d{2}-\d{2}",          # dates (YYYY-MM-DD)
    r"\d{2}/\d{2}/\d{4}",          # dates (MM/DD/YYYY)
    r"\d{1,2}:\d{2}:\d{2}",        # timestamps (HH:MM:SS)
    r"counter\s*[:=]\s*\d+",       # counters
    r"version\s*[:=]\s*\d+\.\d+",  # version numbers used as state
]

# Allowlist for date-like patterns that are actually static content
DYNAMIC_CONTENT_ALLOWLIST: list[str] = [
    "Conventional Commits 1.0.0",
    "YYYY-MM-DD",          # placeholder format strings
    "HH:MM:SS",            # placeholder format strings
    r"\d{4}-\d{2}-\d{2}",  # the pattern itself in this contracts file
    r"\d{2}/\d{2}/\d{4}",
    r"\d{1,2}:\d{2}:\d{2}",
    r"version\s*[:=]\s*\d+\.\d+",
]

# Coordination rules — named contracts with descriptions
COORDINATION_RULES: dict[str, str] = {
    "lead_delegates": "Lead never implements code — always delegates to Architect",
    "architect_decomposes": "Architect decomposes stories into tasks, not lead",
    "developer_owns_code": "Developer writes all code (source and tests)",
    "te_advisory": "Test Engineer is advisory — designs specs, does not write code",
    "se_advisory": "Security Engineer is advisory — reviews security, does not write code",
    "reviewer_commits": "Only Reviewer commits code",
    "developer_no_commit": "Developer does not commit",
    "single_handoff": "Only lead sends work to Reviewer",
    "three_signals": "All three dev-team agents must report before review",
}

# Settings.json required configuration
REQUIRED_SETTINGS_KEYS: dict[str, object] = {
    "env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1",
    "teammateMode": "in-process",
    "includeCoAuthoredBy": False,
}

# Code block markers that indicate language-specific content in base knowledge
LANGUAGE_CODE_MARKERS: list[str] = [
    "```python",
    "```typescript",
    "```javascript",
    "```rust",
    "```go",
    "```java",
    "```ruby",
    "```c++",
    "```cpp",
    "```csharp",
    "```c#",
    "```swift",
    "```kotlin",
]
