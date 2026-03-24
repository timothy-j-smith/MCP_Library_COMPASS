# AGENTS.md

## Repository overview

This is **COMPASS** (Creative Output Management & Production Assistance System) — a documentation and knowledge-base repository for an AI-assisted fiction writing workflow. It contains organized markdown documentation, MCP research notes, Cursor IDE configuration, and one Python utility script.

There are **no runnable application services** (no backend, frontend, database, or Docker containers). The repository is purely documentation plus supporting shell/Python scripts.

### Key directories

| Directory | Contents |
|---|---|
| `COMPASS_Docs/` | Core COMPASS system documentation |
| `MCP_Research/` | Research notes on 30+ MCP servers |
| `MCP_Setup/` | MCP installation guides and setup script |
| `Style_MCPs/` | Style emulation MCP documentation |
| `Automation/` | Automation workflow docs |
| `Cursor_Guides/` | Cursor IDE configuration guides |
| `Misc/` | Python utility script, miscellaneous docs |
| `.cursor/` | ACE playbook config, cursor rules, helper scripts |

## Cursor Cloud specific instructions

### Linting

- **Markdown lint**: `markdownlint "**/*.md"` from the repo root. There are ~7900 pre-existing style warnings in the documentation files — these are expected and should not be "fixed" in bulk. Only address lint issues in files you actively modify.
- **Python syntax check**: `python3 -m py_compile Misc/build_story_structure_mcp.py`
- **Shell script syntax**: `bash -n <script.sh>` for any `.sh` files under `.cursor/scripts/` or `MCP_Setup/`.

### Python utility

The only executable code is `Misc/build_story_structure_mcp.py`, which requires the `anthropic` Python package and an `ANTHROPIC_API_KEY` environment variable. It converts synopsis/outline markdown into structured JSON for an MCP server. It cannot run without API credentials and story source files.

### No services to start

There are no dev servers, build steps, or docker containers. The "hello world" action for this repo is verifying that git, Python imports, markdown linting, and shell script syntax checks all pass.

### ACE playbook

The `.cursor/rules/ace-patterns.mdc` rule requires calling `ace_search` at the start of every session. This is an MCP tool provided externally and may not be available in all environments. If `ace_search` is unavailable, proceed without it — it is not required for repository functionality.
