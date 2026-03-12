#!/usr/bin/env bash
# Build Bible installer
# Usage: curl -fsSL https://raw.githubusercontent.com/lee-fuhr/build-bible/main/install.sh | bash

set -euo pipefail

REPO_URL="https://github.com/lee-fuhr/build-bible.git"
INSTALL_DIR="$HOME/build-bible"
CLAUDE_DIR="$HOME/.claude"

echo ""
echo "Build Bible installer"
echo "---------------------"

# Clone or update
if [ -d "$INSTALL_DIR/.git" ]; then
  echo "→ Updating existing install at $INSTALL_DIR"
  git -C "$INSTALL_DIR" pull --quiet
else
  echo "→ Cloning to $INSTALL_DIR"
  git clone --quiet "$REPO_URL" "$INSTALL_DIR"
fi

# Create target dirs if needed
mkdir -p "$CLAUDE_DIR/commands"
mkdir -p "$CLAUDE_DIR/rules"

# Install files
cp "$INSTALL_DIR/commands/qq-bible-add.md" "$CLAUDE_DIR/commands/"
cp "$INSTALL_DIR/rules/build-bible.md"     "$CLAUDE_DIR/rules/"

echo ""
echo "Installed:"
echo "  ~/.claude/commands/qq-bible-add.md  — /qq-bible-add slash command"
echo "  ~/.claude/rules/build-bible.md      — auto-loaded reference card"
echo ""
echo "Start a new Claude Code session and the Bible is active."
echo "Run /qq-bible-add [url or paste] to evolve it."
echo ""
