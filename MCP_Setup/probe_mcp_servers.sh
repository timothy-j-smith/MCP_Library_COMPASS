#!/usr/bin/env bash
# Probe every MCP listed in .cursor/mcp.json with a short JSON-RPC handshake.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

INIT='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"compass-mcp-probe","version":"0.1.0"}}}'
NOTIFY='{"jsonrpc":"2.0","method":"notifications/initialized"}'
LIST='{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'

FAILURES=0

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
    FAILURES=$((FAILURES + 1))
  fi
  rm -f "$out" "$err"
}

echo "Probing MCPs from .cursor/mcp.json (cwd=$ROOT)"
probe sequential-thinking npx -y @modelcontextprotocol/server-sequential-thinking
probe sequential-thinking-tools npx -y mcp-sequentialthinking-tools
probe knowledge-graph-memory bash MCP_Implementations/knowledge-graph-memory/run.sh
probe sequential-thinking-mas env LLM_PROVIDER=deepseek bash MCP_Implementations/sequential-thinking-mas/run.sh
probe fiction-reverse-engineering bash MCP_Implementations/fiction-reverse-engineering/run.sh

if (( FAILURES > 0 )); then
  exit 1
fi
