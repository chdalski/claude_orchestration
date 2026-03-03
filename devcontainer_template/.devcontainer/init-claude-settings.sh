#!/usr/bin/env bash

# Initialize Claude settings for devcontainer
# Copies host settings into the container volume

set -e

HOST_SETTINGS="/home/vscode/.claude-host-settings.json"
CONTAINER_SETTINGS="/home/vscode/.claude/settings.json"

echo "============================================================"
echo "Initializing Claude Settings"
echo "============================================================"

# Ensure .claude directory exists (volume should create it, but just in case)
mkdir -p /home/vscode/.claude

if [[ -f "$HOST_SETTINGS" ]]; then
    echo "Copying host settings from $HOST_SETTINGS"
    cp "$HOST_SETTINGS" "$CONTAINER_SETTINGS"
    echo "Written container settings to $CONTAINER_SETTINGS"
else
    echo "No host settings found at $HOST_SETTINGS"
    echo "Claude will use default settings"
fi

echo "============================================================"
echo "Claude settings initialized"
echo "============================================================"
