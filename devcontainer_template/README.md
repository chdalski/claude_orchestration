# Devcontainer Template

A sandboxed devcontainer for running Claude Code agents in
isolation. Copy the `.devcontainer/` directory into any
project to get a firewall-restricted, non-root container
that blocks all outbound traffic except an explicit
allowlist of domains.

## What It Provides

- **Network firewall** — iptables rules that DROP all
  outbound traffic except DNS, SSH, and domains listed in
  `allowed-domains.conf`. GitHub IP ranges are fetched
  dynamically from `api.github.com/meta` and always allowed.
- **Non-root execution** — runs as user `vscode` with sudo
  only for the firewall init script.
- **Autopilot mode** — if a `.claude/` directory exists in
  the workspace, the container creates
  `.claude/settings.local.json` with `bypassPermissions`
  enabled. The container is the security boundary, so
  per-tool prompts are unnecessary.
- **Bind-mounted workspace** — your project directory is
  mounted at `/workspace` with delegated consistency.
- **Bind-mounted allowlist** — `allowed-domains.conf` is
  mounted read-only at runtime, so changes take effect on
  container restart without a rebuild.

## Quick Start

```bash
cp -r devcontainer_template/.devcontainer/ /path/to/your/project/.devcontainer/
```

Then open the project in VS Code with the Dev Containers
extension, or use the `devcontainer` CLI.

## Configuring `allowed-domains.conf`

One entry per line. Supported formats:

```
api.anthropic.com          # Domain — resolved via DNS at start
192.168.1.0/24             # CIDR range — added directly
```

Lines starting with `#` are comments. Blank lines are
ignored.

The default allowlist includes:

| Category | Domains |
|----------|---------|
| Anthropic | `api.anthropic.com`, `statsig.anthropic.com`, `statsig.com`, `sentry.io` |
| Package registries | npm, PyPI, crates.io, Go proxy, etc. |
| Language docs | docs.rs, docs.python.org, pkg.go.dev, MDN, nodejs.org |
| VS Code | marketplace, blob storage, update server |
| GitHub | All ranges from `api.github.com/meta` (hardcoded in script) |

Edit the file to match your project's needs. Uncomment or
remove registries and doc sites as appropriate.

## Setting Up `~/.claude/settings.json`

Claude Code reads `~/.claude/settings.json` for
user-level configuration (API keys, environment variables,
permissions). Inside a devcontainer, you need this file to
exist in the container so Claude Code can authenticate.

### Fresh install workaround

Claude Code 2.0.65+ has a bug where `settings.json` is
ignored on first run if `~/.claude.json` does not yet exist
([#13827](https://github.com/anthropics/claude-code/issues/13827)).
The onboarding flow runs before reading `settings.json`,
so the login prompt appears even when API credentials are
configured.

**Workaround:** create `~/.claude.json` alongside
`settings.json` to skip onboarding:

```json
{
  "hasCompletedOnboarding": true
}
```

### Recommended setup

Create `~/.claude/settings.json` with your API
configuration:

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "your-api-key"
  }
}
```

If you use a proxy (e.g., LiteLLM, Portkey):

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://your-proxy.example.com",
    "ANTHROPIC_API_KEY": "your-proxy-key"
  }
}
```

Alternatively, use `apiKeyHelper` to fetch the key from a
command (useful for vaults or credential managers):

```json
{
  "apiKeyHelper": "vault read -field=key secret/claude",
  "env": {
    "ANTHROPIC_BASE_URL": "https://your-proxy.example.com"
  }
}
```

### Mounting settings into the container

The `devcontainer.json` already mounts a persistent volume
at `/home/node/.claude`. To use your host's settings
instead, replace the volume mount with a bind mount:

```jsonc
// In devcontainer.json "mounts" array, replace:
"source=claude-code-config-${devcontainerId},target=/home/node/.claude,type=volume"
// With:
"source=${localEnv:HOME}/.claude,target=/home/vscode/.claude,type=bind,readonly"
```

This gives the container read-only access to your host
`~/.claude/` directory, including `settings.json` and any
API keys configured there.

### Full fresh-install setup

For a completely fresh environment (no existing
`~/.claude.json`), create both files before starting the
container:

```bash
mkdir -p ~/.claude
```

```bash
cat > ~/.claude/settings.json << 'EOF'
{
  "env": {
    "ANTHROPIC_API_KEY": "your-api-key"
  }
}
EOF
```

```bash
cat > ~/.claude.json << 'EOF'
{
  "hasCompletedOnboarding": true
}
EOF
```

This ensures Claude Code skips the onboarding prompt and
reads your API key from `settings.json` on first run.

## Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Ubuntu-based image with dev tools, fish shell, starship prompt, and Claude Code |
| `devcontainer.json` | Container config: mounts, capabilities, firewall init |
| `init-firewall.sh` | iptables/ipset firewall script run at container start |
| `allowed-domains.conf` | Allowlist of outbound domains (bind-mounted, editable without rebuild) |
