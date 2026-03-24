# AGENTS.md

## Overview

COMPASS (Creative Output Management & Production Assistance System) is a **documentation and knowledge-base repository** for an AI-assisted fiction writing workflow built on Cursor IDE and MCP servers. It is not a runnable application with backend/frontend services.

### Repository contents

- ~127 Markdown files: research notes, setup guides, session analysis, style MCP docs
- `Misc/build_story_structure_mcp.py`: Python utility that converts story synopsis/outline to MCP JSON format (requires the `anthropic` package and an `ANTHROPIC_API_KEY`)
- `MCP_Setup/setup_mcp.sh`: interactive Bash script for setting up GitKraken CLI and GitHub token (not suitable for non-interactive execution)
- `.cursor/scripts/`: ACE framework session-tracking hooks
- `.cursor/rules/ace-patterns.mdc`: workspace rule requiring `ace_search` MCP tool calls

## Cursor Cloud specific instructions

### Dependencies

The only installable dependency is the `anthropic` Python package, used by `Misc/build_story_structure_mcp.py`. It is installed via `pip install anthropic`.

### No build/lint/test/dev-server

This is a pure documentation repository. There is:
- No package manager lockfile, `package.json`, `requirements.txt`, `Makefile`, or `Dockerfile`
- No linter, test suite, or build system
- No dev server or services to start

### Running the Python utility

```bash
python3 Misc/build_story_structure_mcp.py
```

This script expects `Story_Bible/synopsis.md` and `Story_Bible/outline.md` relative to the `Misc/` directory, and an `ANTHROPIC_API_KEY` environment variable. Without the story files it exits gracefully with exit code 1 — this is expected behavior, not an error.

### ACE framework

The `.cursor/rules/ace-patterns.mdc` workspace rule instructs agents to call `ace_search` MCP tool before any implementation task. The ACE MCP server may not be available in Cloud Agent environments; if unavailable, skip ACE calls and proceed normally.

### `MCP_Setup/setup_mcp.sh`

This script is **interactive** (uses `read -p` prompts) and should not be run non-interactively in Cloud Agent VMs.
