# Devcontainer Template

Devcontainer template for sandboxed Claude Code agent execution.

## Setup

1. Copy the contents of this directory to your project's `.devcontainer/` folder
2. Open your project in VS Code and use "Reopen in Container"

## Authentication Modes

The `CLAUDE_AUTH` environment variable controls how Claude Code authenticates.
On first use, `initializeCommand` creates `.devcontainer/.env.local`
(gitignored) with the default `CLAUDE_AUTH=proxy` before Docker needs it.

| Mode | `CLAUDE_AUTH` | What gets copied | Use case |
|------|---------------|------------------|----------|
| Proxy (default) | `proxy` | `settings.json` (with env vars) | Work account via API proxy (e.g. Portkey) |
| OAuth | `oauth` | `.credentials.json` + `settings.json` (env block and apiKeyHelper stripped) | Private Anthropic account |

### Proxy mode (default)

No extra setup needed. Your `~/.claude/settings.json` is copied as-is into
the container, including any `env` block with proxy configuration.

### OAuth mode

Requires `~/.claude/.credentials.json` from a prior `claude login` on the
host. The script copies it into the container and strips the entire `env`
block and `apiKeyHelper` from `settings.json` so OAuth credentials are used
and no proxy config leaks in. Any env vars needed in oauth mode (e.g.
`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`) should be added to
`.devcontainer/.env.local`.

### Switching modes

Edit `CLAUDE_AUTH` in `.devcontainer/.env.local` (gitignored):

```bash
# .devcontainer/.env.local
CLAUDE_AUTH=oauth
```

After switching, delete the Docker volume and rebuild the container (see
Troubleshooting).

## Troubleshooting

### Auth errors or "Rate limit reached" after switching modes

The Docker volume `claude-code-config-{project-name}` persists between
container restarts. If you switch authentication modes or change credentials,
stale state in the volume can cause unexpected errors (e.g. "Rate limit
reached" that isn't a real rate limit).

Fix: delete the volume and rebuild the container.

```bash
docker volume ls | grep claude-code-config
docker volume rm claude-code-config-<project-name>
```

### Claude Code ignores settings.json on first run

On fresh volumes, Claude Code >=2.0.65 may ignore `settings.json` and force
the login flow ([#13827](https://github.com/anthropics/claude-code/issues/13827)).
Deleting the volume and setting `CLAUDE_AUTH` before starting the container
resolves this.

## How It Works

- **Project-scoped volume**: Claude config is stored in a Docker volume named
  `claude-code-config-{project-name}`. All devcontainers for the same project
  share history. Different projects have separate histories.

- **Host config as template**: Your `~/.claude/` directory and `~/.claude.json`
  are mounted read-only. On container startup, the post-start script copies
  the appropriate files into the container volume based on `CLAUDE_AUTH`, and
  copies `~/.claude.json` into the container home directory.

## Mounts

| Source | Target | Purpose |
|--------|--------|---------|
| `claude-code-config-${project}` (volume) | `/home/vscode/.claude` | Project-scoped Claude config and history |
| `~/.claude/` (bind, ro) | `/home/vscode/.claude-host/` | Host config template directory |
| `~/.claude.json` (bind, ro) | `/home/vscode/.claude-host.json` | Host Claude config file (copied into container on startup) |
| `claude-code-bashhistory-${id}` (volume) | `/commandhistory` | Shell history persistence |
