# AGENTS.md

## Overview

COMPASS (Creative Output Management & Production Assistance System) is a **documentation and knowledge-base repository** for an AI-assisted fiction writing workflow built on Cursor IDE and MCP servers. It is not a full-stack application with backend/frontend services, but it does contain local MCP server code and helper utilities with tests.

### Repository contents

- ~127 Markdown files: research notes, setup guides, session analysis, style MCP docs
- `MCP_Implementations/fiction-reverse-engineering/`: Fiction Reverse Engineering MCP (local Python MCP server; tools for pacing/formula analysis). Configured in `.cursor/mcp.json` as `fiction-reverse-engineering`. Requires `pip install -r MCP_Implementations/fiction-reverse-engineering/requirements.txt` (package: `mcp`).
- `Misc/build_story_structure_mcp.py`: Python utility that converts story synopsis/outline to MCP JSON format (requires the `anthropic` package and an `ANTHROPIC_API_KEY`)
- `Misc/convert_synopsis_outline_to_book_series.py` + `Misc/import_to_book_series.mjs`: Book Series MCP conversion helpers (stdlib only; see below)
- `MCP_Setup/setup_mcp.sh`: interactive Bash script for setting up GitKraken CLI and GitHub token (not suitable for non-interactive execution)
- `MCP_Setup/CURRENT_STATE.md`: single source of truth for MCP status — read this first for "what's actually true now"

## Cursor Cloud specific instructions

### Repository overview

Primarily a documentation/knowledge-base repo plus a few local Python/Node helpers and one in-repo MCP server (`fiction-reverse-engineering`). There is **no web app, no docker-compose stack, and no long-running HTTP server** to start for day-to-day work. Book Series MCP is an **external** dependency (separate checkout + PostgreSQL) and is intentionally out of the update script.

### Dependencies / update script gotchas

- **Pin `mcp` to 1.x:** install must resolve `mcp>=1.25.0,<2`. Bare `mcp>=1.25.0` can pull **mcp 2.0**, which removes `mcp.server.fastmcp.FastMCP` and breaks `MCP_Implementations/fiction-reverse-engineering/server.py`.
- **User-local bins:** `markdownlint-cli2` (and some pip scripts) install under `~/.local/bin`. Ensure that directory is on `PATH` before linting.
- **Cloud Agent Builds:** `.cursor/environment.json` defines the install-only bootstrap (no `start`/`terminals` — this repo has no long-running services). Do **not** put Book Series MCP / PostgreSQL startup in install.
- Do **not** put Book Series MCP / PostgreSQL startup in the update script — see Book Series section below.

### Linting

- **Markdown lint:** `markdownlint-cli2 "**/*.md"` from the workspace root. The repo has many existing lint warnings (mostly `MD032`, `MD022`, `MD036`); these are pre-existing and not caused by cloud agent changes.

### Tests / Python scripts / MCP servers

- Fiction RE analyzer + MCP tool tests: `python3 MCP_Implementations/fiction-reverse-engineering/tests/test_analyzer.py`
- Book Series converter parser tests: `python3 Misc/tests/test_convert_synopsis_outline.py`
- `Misc/build_story_structure_mcp.py`: converts story outlines to MCP-compatible JSON using the Anthropic API. Requires `pip install anthropic` and `ANTHROPIC_API_KEY` (or interactive input). Without story source files (`Story_Bible/synopsis.md`, `Story_Bible/outline.md`), it exits gracefully with a non-zero code — this is expected behavior.
- `MCP_Implementations/fiction-reverse-engineering/server.py`: Fiction Reverse Engineering MCP (stdio FastMCP). Install with `pip install -r MCP_Implementations/fiction-reverse-engineering/requirements.txt`.

### Shell scripts

- `MCP_Setup/setup_mcp.sh` is an interactive setup script for GitKraken CLI and GitHub tokens — it prompts for user input and is not suitable for non-interactive/automated use.

### ACE configuration (removed)

- ACE pattern-learning integration was **removed** from this workspace (PRs #6/#7). Ignore any leftover docs that mention `.cursor/scripts/ace_*.sh`, `ace_search`, or `.cursor/rules/ace-patterns.mdc` — those files are gone.

### Book Series MCP conversion helpers (`Misc/`)

- `Misc/convert_synopsis_outline_to_book_series.py` (Python stdlib only, no API) parses a Story Bible `synopsis.md` + `outline.md` into a Book Series MCP import bundle. Example: `python3 Misc/convert_synopsis_outline_to_book_series.py --synopsis Misc/examples/synopsis.example.md --outline Misc/examples/outline.example.md --out /tmp/bundle.json`.
- `Misc/import_to_book_series.mjs` (Node stdlib only) applies that bundle to a running Book Series MCP over JSON-RPC/stdio. Parser tests: `python3 Misc/tests/test_convert_synopsis_outline.py`. Full workflow: `MCP_Setup/BOOK_SERIES_MCP_SETUP_AND_CONVERSION.md`.
- The importer dedupes by default (idempotent); pass `--no-dedupe` to force creation. Use `--series-id` to reliably reuse a series.
- The importer needs an **external** [book-series-mcp](https://github.com/RLRyals/book-series-mcp) checkout (Node.js + PostgreSQL) — it is NOT part of this repo. Book Series MCP uses `DATABASE_URL` (older notes saying "Python / `pip install` / `POSTGRES_URI`" are wrong).
