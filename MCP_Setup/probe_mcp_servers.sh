#!/usr/bin/env bash
# Probe every MCP listed in .cursor/mcp.json with a short JSON-RPC handshake.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

INIT='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"compass-mcp-probe","version":"0.1.0"}}}'
NOTIFY='{"jsonrpc":"2.0","method":"notifications/initialized"}'
LIST='{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'

probe() {
  local name="$1"
  shift
  local out err rc
  out="$(mktemp)"
  err="$(mktemp)"
  set +e
  printf '%s\n' "$INIT" "$NOTIFY" "$LIST" | timeout 60 "$@" >"$out" 2>"$err"
  rc=$?
  set -e
  if grep -q '"id":1' "$out" && grep -q '"tools"' "$out"; then
    echo "OK   $name"
  else
    echo "FAIL $name (exit=$rc)"
    echo "  stderr: $(head -n 3 "$err" | tr '\n' ' ')"
  fi
  rm -f "$out" "$err"
}

echo "Probing MCPs from .cursor/mcp.json (cwd=$ROOT)"
probe sequential-thinking npx -y @modelcontextprotocol/server-sequential-thinking
probe sequential-thinking-tools npx -y mcp-sequentialthinking-tools
probe sequential-thinking-structured npx -y mcp-sequential-thinking
probe knowledge-graph-memory env MEMORY_FILE_PATH=".cursor/memory.json" npx -y @modelcontextprotocol/server-memory
probe sequential-thinking-mas bash MCP_Implementations/sequential-thinking-mas/run.sh
probe fiction-reverse-engineering \
  env FICTION_RE_FORMULAS_DIR="MCP_Implementations/fiction-reverse-engineering/formulas" \
  python3 MCP_Implementations/fiction-reverse-engineering/server.py
