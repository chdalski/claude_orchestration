# Devcontainer Template

Devcontainer template for sandboxed Claude Code agent execution.

## Setup

1. Copy the contents of this directory to your project's `.devcontainer/` folder
2. Open your project in VS Code and use "Reopen in Container"

## How It Works

- **Project-scoped volume**: Claude config is stored in a Docker volume named
  `claude-code-config-{project-name}`. All devcontainers for the same project
  share history. Different projects have separate histories.

- **Host settings as template**: Your `~/.claude/settings.json` is mounted
  read-only. On container startup, it's copied into the container volume so
  Claude Code picks up your existing configuration.

## Mounts

| Source | Target | Purpose |
|--------|--------|---------|
| `claude-code-config-${project}` (volume) | `/home/vscode/.claude` | Project-scoped Claude config and history |
| `~/.claude/settings.json` (bind, ro) | `/home/vscode/.claude-host-settings.json` | Template for container settings |
| `claude-code-bashhistory-${id}` (volume) | `/commandhistory` | Shell history persistence |
