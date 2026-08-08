#!/usr/bin/env bash
# Launcher for sequential-thinking-mas that keeps the MCP process connectable.
#
# PyPI 0.2.3 constructs ExaTools at startup and hard-requires EXA_API_KEY.
# Research stays optional in practice: a placeholder lets the server
# initialize/list tools; set a real EXA_API_KEY for live Exa research.
#
# LLM calls need a real provider key matching LLM_PROVIDER (default: deepseek).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v mcp-server-mas-sequential-thinking >/dev/null 2>&1; then
  echo "sequential-thinking-mas: package not installed." >&2
  echo "Run: pip install --user -r \"${ROOT}/requirements.txt\"" >&2
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

exec mcp-server-mas-sequential-thinking "$@"
