#!/usr/bin/env bash
# Launcher for sequential-thinking-mas that keeps the MCP process connectable.
#
# PyPI 0.2.3 constructs ExaTools at startup and hard-requires EXA_API_KEY.
# Research stays optional in practice: a placeholder lets the server
# initialize/list tools; set a real EXA_API_KEY for live Exa research.
#
# LLM calls need a real provider key matching LLM_PROVIDER (default: deepseek).
#
# Cursor’s MCP process often has a stripped PATH that omits ~/.local/bin
# (Linux) or ~/Library/Python/*/bin (macOS) after `pip install --user`.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_NAME="mcp-server-mas-sequential-thinking"

resolve_bin() {
  local candidate
  if command -v "$BIN_NAME" >/dev/null 2>&1; then
    command -v "$BIN_NAME"
    return 0
  fi
  for candidate in \
    "${HOME}/.local/bin/${BIN_NAME}" \
    "${HOME}"/Library/Python/*/bin/"${BIN_NAME}"
  do
    if [[ -x "$candidate" ]]; then
      echo "$candidate"
      return 0
    fi
  done
  # Last resort: ask the active python where the console script lives.
  local from_py
  from_py="$(python3 - <<'PY' 2>/dev/null || true
import sys
from pathlib import Path
for base in [Path(sys.prefix) / "bin", Path.home() / ".local" / "bin"]:
    p = base / "mcp-server-mas-sequential-thinking"
    if p.is_file():
        print(p)
        break
PY
)"
  if [[ -n "$from_py" && -x "$from_py" ]]; then
    echo "$from_py"
    return 0
  fi
  return 1
}

MAS_BIN="$(resolve_bin || true)"
if [[ -z "${MAS_BIN}" ]]; then
  echo "sequential-thinking-mas: package not installed (or not on PATH)." >&2
  echo "Run: pip install --user -r \"${ROOT}/requirements.txt\"" >&2
  echo "Then ensure the console script is reachable (often ~/.local/bin)." >&2
  exit 1
fi

# Empty string in mcp.json env would override a real shell key — never do that.
# Inherit host env; only set a non-secret placeholder when EXA is unset.
if [[ -z "${EXA_API_KEY:-}" ]]; then
  export EXA_API_KEY="placeholder-not-for-research"
  echo "sequential-thinking-mas: EXA_API_KEY unset; using placeholder so the MCP can start. Set a real key for Exa research." >&2
fi

if [[ -z "${LLM_PROVIDER:-}" ]]; then
  export LLM_PROVIDER="deepseek"
fi

case "${LLM_PROVIDER}" in
  deepseek)
    if [[ -z "${DEEPSEEK_API_KEY:-}" ]]; then
      echo "sequential-thinking-mas: warning: DEEPSEEK_API_KEY unset. Server will connect, but tool calls will fail until the key is set in the host environment." >&2
    fi
    ;;
  groq)
    if [[ -z "${GROQ_API_KEY:-}" ]]; then
      echo "sequential-thinking-mas: warning: GROQ_API_KEY unset. Server will connect, but tool calls will fail until the key is set." >&2
    fi
    ;;
  openrouter)
    if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
      echo "sequential-thinking-mas: warning: OPENROUTER_API_KEY unset. Server will connect, but tool calls will fail until the key is set." >&2
    fi
    ;;
  ollama)
    ;;
  *)
    echo "sequential-thinking-mas: using LLM_PROVIDER=${LLM_PROVIDER}" >&2
    ;;
esac

exec "$MAS_BIN" "$@"
