#!/usr/bin/env bash
# Launcher for @modelcontextprotocol/server-memory.
#
# Relative MEMORY_FILE_PATH values are resolved against the package dist/
# directory (npx cache), NOT the process cwd — so ".cursor/memory.json"
# never writes to the workspace. Always pass an absolute path.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DEFAULT_MEMORY="$ROOT/.cursor/memory.json"

if [[ -z "${MEMORY_FILE_PATH:-}" ]]; then
  export MEMORY_FILE_PATH="$DEFAULT_MEMORY"
elif [[ "${MEMORY_FILE_PATH}" != /* ]]; then
  export MEMORY_FILE_PATH="$ROOT/${MEMORY_FILE_PATH}"
fi

mkdir -p "$(dirname "$MEMORY_FILE_PATH")"
touch "$MEMORY_FILE_PATH"

exec npx -y @modelcontextprotocol/server-memory "$@"
