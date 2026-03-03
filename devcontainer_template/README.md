# Container Template v2

Devcontainer template that uses an external Claude API proxy.

## Setup

1. Copy the contents of this directory to your project's `.devcontainer/` folder
2. Ensure the proxy from `container_template/` is running on your host
3. Open your project in VS Code and use "Reopen in Container"

## How It Works

- **Project-scoped volume**: Claude config is stored in a Docker volume named
  `claude-code-config-{project-name}`. All devcontainers for the same project
  share history. Different projects have separate histories.

- **Host settings as template**: Your `~/.claude/settings.json` is mounted
  read-only. On container startup, it's copied and modified to point to the
  external proxy at `host.docker.internal:3000`.

- **No proxy inside container**: The proxy runs externally (from
  `container_template/`), so multiple devcontainers and your local system can
  share it.

## Mounts

| Source | Target | Purpose |
|--------|--------|---------|
| `claude-code-config-${project}` (volume) | `/home/vscode/.claude` | Project-scoped Claude config and history |
| `~/.claude/settings.json` (bind, ro) | `/home/vscode/.claude-host-settings.json` | Template for container settings |
| `claude-code-bashhistory-${id}` (volume) | `/commandhistory` | Shell history persistence |

## Configuration

Set `CLAUDE_PROXY_URL` in your devcontainer to override the default proxy URL:

```json
{
  "containerEnv": {
    "CLAUDE_PROXY_URL": "http://host.docker.internal:3001"
  }
}
```

Default: `http://host.docker.internal:3000`
