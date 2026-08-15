#!/usr/bin/env bash
set -euo pipefail

MCP_CONFIG=".cursor/mcp.json"

if [ ! -f "$MCP_CONFIG" ]; then
    echo "⚠️  MCP config file not found: $MCP_CONFIG"
fi

echo "1. If you set up GitHub token, restart your terminal or run:"
echo "   source ~/.zshrc"
echo ""
echo "2. Enable MCP servers in .cursor/mcp.json (see Step 4 above)"
echo ""
echo "3. Restart Cursor completely"
