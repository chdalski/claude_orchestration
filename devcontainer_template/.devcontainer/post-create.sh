#!/usr/bin/env bash

# Runs once after the container is created (postCreateCommand).
# Use this for one-time setup that only needs to happen on first build.

set -euo pipefail

# Fix pnpm store ownership — the volume is created as root by Docker,
# but pnpm runs as vscode and needs write access.
sudo chown -R vscode:vscode /home/vscode/.local/share/pnpm

# Create .env.local with defaults if it doesn't exist yet.
# The file is gitignored — users change it locally to switch auth mode.
# Docker's --env-file loads it on every container start.
ENV_LOCAL="/workspace/.devcontainer/.env.local"
if [ ! -f "$ENV_LOCAL" ]; then
  cat > "$ENV_LOCAL" << 'EOF'
# Authentication mode for Claude Code:
#   proxy - work account via API proxy (e.g. Portkey)
#   oauth - private Anthropic account via OAuth credentials
CLAUDE_AUTH=proxy
EOF
  echo "Created $ENV_LOCAL with default CLAUDE_AUTH=proxy"
fi
