# AGENTS.md

## Cursor Cloud specific instructions

### Repository Overview

This is **COMPASS v2.0** — a documentation and configuration knowledge base for a Cursor IDE-based AI writing assistant framework. It is **not** a traditional deployable application. The repository contains:

- ~127 Markdown documentation files (guides, research, session analysis)
- Cursor IDE configuration (`.cursor/` directory with ACE patterns, rules, commands, scripts)
- One Python utility script (`Misc/build_story_structure_mcp.py`) for converting story outlines to MCP format
- One interactive bash setup script (`MCP_Setup/setup_mcp.sh`) for configuring GitKraken CLI and GitHub tokens

### No Build/Lint/Test Pipeline

There is no `package.json`, `Makefile`, CI/CD config, test suite, or build system. There are no lint checks, automated tests, or application servers to run.

### Executable Artifacts

| Script | Language | Purpose | Dependencies |
|--------|----------|---------|--------------|
| `Misc/build_story_structure_mcp.py` | Python 3 | Converts synopsis/outline to MCP JSON format | `anthropic` Python package, `ANTHROPIC_API_KEY` env var |
| `MCP_Setup/setup_mcp.sh` | Bash | Interactive setup for GitKraken CLI and GitHub token | None (interactive, not suited for headless/automated use) |
| `.cursor/scripts/ace_*.sh` | Bash | ACE session tracking hooks for Cursor IDE | `jq` (for JSON parsing) |

### Running the Python Script

`Misc/build_story_structure_mcp.py` expects:
1. Source files at `Misc/Story_Bible/synopsis.md` and `Misc/Story_Bible/outline.md`
2. An `ANTHROPIC_API_KEY` environment variable (or it will prompt interactively)
3. The `anthropic` Python package installed (`pip install anthropic`)

Without source files, the script exits gracefully with a warning.

### ACE Pattern System

The `.cursor/rules/ace-patterns.mdc` rule requires calling `ace_search` MCP tool before any implementation work. This is a Cursor IDE-specific MCP integration and is **not available in headless Cloud Agent environments** — it can be safely ignored during automated cloud sessions.
