#!/usr/bin/env bash

# Copy host settings into the container volume so Claude Code
# picks up the user's configuration (model preferences, API
# keys, etc.). The host file is bind-mounted read-only by
# devcontainer.json; this script copies it to the writable
# volume location that Claude Code reads at startup.
#
# Permission bypass is handled by the shell alias in the
# Dockerfile (--dangerously-skip-permissions), not here.

set -euo pipefail

SEP="============================================================"
HOST_SETTINGS="/home/vscode/.claude-host-settings.json"
CONTAINER_SETTINGS="/home/vscode/.claude/settings.json"

echo "$SEP"
echo "Initializing Claude Settings"
echo "$SEP"

mkdir -p "$(dirname "$CONTAINER_SETTINGS")"

if [ -f "$HOST_SETTINGS" ]; then
    echo "Copying host settings from $HOST_SETTINGS"
    cp "$HOST_SETTINGS" "$CONTAINER_SETTINGS"
    echo "Written container settings to $CONTAINER_SETTINGS"
else
    echo "No host settings found at $HOST_SETTINGS"
    echo "Creating default settings"
    echo '{}' > "$CONTAINER_SETTINGS"
fi

echo "$SEP"
echo "Claude settings initialized"
echo "$SEP"

echo "$SEP"
echo "Initializing Git Identity"
echo "$SEP"

NAMES=("Claus Coder" "Claudia Coder" "Mr. Robot" "Mrs. Robot")
SELECTED="${NAMES[$((RANDOM % ${#NAMES[@]}))]}"

FIRST=$(echo "$SELECTED" | awk '{print $1}' | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9')
SECOND=$(echo "$SELECTED" | awk '{print $2}' | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9')
EMAIL="${FIRST}.${SECOND}@codecentric.de"

git config --global user.name "$SELECTED"
git config --global user.email "$EMAIL"

echo "Git identity set: $SELECTED <$EMAIL>"
echo "$SEP"