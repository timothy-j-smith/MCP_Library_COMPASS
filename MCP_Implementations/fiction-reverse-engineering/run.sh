#!/usr/bin/env bash
# Launcher for fiction-reverse-engineering MCP.
#
# Cursor MCP processes may start with a cwd that is not the workspace root, and
# relative FICTION_RE_FORMULAS_DIR values then create/write formulas in the wrong
# place (or fail mkdir). Always resolve to an absolute path under this repo.
#
# Prefer a local .venv when present (matches README install); otherwise python3.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PKG="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_FORMULAS="$PKG/formulas"

if [[ -z "${FICTION_RE_FORMULAS_DIR:-}" ]]; then
  export FICTION_RE_FORMULAS_DIR="$DEFAULT_FORMULAS"
elif [[ "${FICTION_RE_FORMULAS_DIR}" != /* ]]; then
  export FICTION_RE_FORMULAS_DIR="$ROOT/${FICTION_RE_FORMULAS_DIR}"
fi

mkdir -p "$FICTION_RE_FORMULAS_DIR"

if [[ -x "$PKG/.venv/bin/python" ]]; then
  PY="$PKG/.venv/bin/python"
elif [[ -x "$PKG/.venv/bin/python3" ]]; then
  PY="$PKG/.venv/bin/python3"
else
  PY="$(command -v python3 || true)"
fi

if [[ -z "${PY}" ]]; then
  echo "fiction-reverse-engineering: python3 not found on PATH." >&2
  exit 1
fi

if ! "$PY" -c "import mcp" 2>/dev/null; then
  echo "fiction-reverse-engineering: Python package 'mcp' not installed for: $PY" >&2
  echo "Run: \"$PY\" -m pip install -r \"$PKG/requirements.txt\"" >&2
  exit 1
fi

cd "$ROOT"
exec "$PY" "$PKG/server.py" "$@"
