# AGENTS.md

## Overview

COMPASS (Creative Output Management & Production Assistance System) is a **documentation and knowledge-base repository** for an AI-assisted fiction writing workflow built on Cursor IDE and MCP servers. It is not a runnable application with backend/frontend services.

### Repository contents

- ~127 Markdown files: research notes, setup guides, session analysis, style MCP docs
- `MCP_Implementations/fiction-reverse-engineering/`: Fiction Reverse Engineering MCP (local Python MCP server; tools for pacing/formula analysis). Configured in `.cursor/mcp.json` as `fiction-reverse-engineering`. Requires `pip install -r MCP_Implementations/fiction-reverse-engineering/requirements.txt` (package: `mcp`).
- `Misc/build_story_structure_mcp.py`: Python utility that converts story synopsis/outline to MCP JSON format (requires the `anthropic` package and an `ANTHROPIC_API_KEY`)
- `MCP_Setup/setup_mcp.sh`: interactive Bash script for setting up GitKraken CLI and GitHub token (not suitable for non-interactive execution)
- `.cursor/scripts/`: ACE framework session-tracking hooks
- `.cursor/rules/ace-patterns.mdc`: workspace rule requiring `ace_search` MCP tool calls

## Cursor Cloud specific instructions

### Repository overview

This is a **documentation/knowledge-base repository** for the COMPASS (Creative Output Management & Production Assistance System) fiction writing system. It contains ~127 Markdown files, Cursor IDE ACE configuration, and one standalone Python utility script. There are **no application services, no test suites, no build systems, and no web servers**.

### Linting

- **Markdown lint:** `markdownlint-cli2 "**/*.md"` from the workspace root. The repo has many existing lint warnings (mostly `MD032`, `MD022`, `MD036`); these are pre-existing and not caused by cloud agent changes.

### Python scripts / MCP servers

- `Misc/build_story_structure_mcp.py`: converts story outlines to MCP-compatible JSON using the Anthropic API. Requires `pip install anthropic` and `ANTHROPIC_API_KEY` (or interactive input). Without story source files (`Story_Bible/synopsis.md`, `Story_Bible/outline.md`), it exits gracefully with a non-zero code — this is expected behavior.
- `MCP_Implementations/fiction-reverse-engineering/server.py`: Fiction Reverse Engineering MCP (stdio FastMCP). Install with `pip install -r MCP_Implementations/fiction-reverse-engineering/requirements.txt`. Analyzer tests: `python3 MCP_Implementations/fiction-reverse-engineering/tests/test_analyzer.py`.

### Shell scripts

- All `.cursor/scripts/ace_*.sh` scripts are ACE (Adaptive Cursor Engine) lifecycle hooks for Cursor IDE. They are invoked by Cursor, not by the developer directly.
- `MCP_Setup/setup_mcp.sh` is an interactive setup script for GitKraken CLI and GitHub tokens — it prompts for user input and is not suitable for non-interactive/automated use.

### ACE configuration

- The `.cursor/rules/ace-patterns.mdc` rule file instructs agents to call `ace_search` MCP tool before implementation tasks. In Cloud Agent environments where this MCP tool is unavailable, this rule can be safely ignored.

### Book Series MCP conversion helpers (`Misc/`)

- `Misc/convert_synopsis_outline_to_book_series.py` (Python stdlib only, no API) parses a Story Bible `synopsis.md` + `outline.md` into a Book Series MCP import bundle (series/book, `## Characters`, `## Themes`, and chapter outlines). `Misc/import_to_book_series.mjs` (Node stdlib only) applies that bundle to a running Book Series MCP by speaking JSON-RPC over stdio. Example inputs live in `Misc/examples/`; parser tests in `Misc/tests/` (`python3 Misc/tests/test_convert_synopsis_outline.py`). Full workflow: `MCP_Setup/BOOK_SERIES_MCP_SETUP_AND_CONVERSION.md`.
- The importer dedupes by default (skips create when a matching book/character/plot-thread/series already exists), so imports are idempotent; pass `--no-dedupe` to force creation. Series dedup needs the upstream `get_series_overview` tool (missing `series_overview` view in current Book Series MCP) — use `--series-id` to reliably reuse a series.
- The importer needs an **external** [book-series-mcp](https://github.com/RLRyals/book-series-mcp) checkout (Node.js + PostgreSQL) — it is NOT part of this repo, so it is intentionally excluded from the update script. Book Series MCP is **Node.js + PostgreSQL** using `DATABASE_URL` (older notes in this repo saying "Python / `pip install` / `POSTGRES_URI`" are wrong). Its `init.sql` must be followed by `migrations/2025*.sql` in order (a few init.sql/migration errors are benign; see the setup doc).
