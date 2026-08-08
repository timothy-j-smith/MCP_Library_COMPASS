# Fiction Reverse Engineering MCP

Mathematical pacing analysis and bestseller-formula comparison for fiction.

> **Note:** The original local `server.py` (documented Jan 2026 under
> `~/mcp-servers/` / Walk This Way) was never pushed to GitHub. This package
> reconstructs the documented tool surface from
> `Style_MCPs/FICTION_REVERSE_ENGINEERING_MCP_*.md` so the MCP can live in-repo.

## Install

```bash
cd MCP_Implementations/fiction-reverse-engineering
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Cursor config

Wired in `.cursor/mcp.json` via `run.sh` (resolves an absolute formulas dir and
prefers a local `.venv` when present). Restart Cursor (or reload MCP servers)
after install.

## Smoke test (analyzer only)

```bash
python3 tests/test_analyzer.py
```

## Tools

- `reverse_engineer_novel`
- `compare_to_bestseller`
- `analyze_pacing`
- `extract_dialogue_formula`
- `find_chapter_formula`
- `list_available_formulas`
