# AGENTS.md

## Cursor Cloud specific instructions

### Repository overview

This is a **documentation/knowledge-base repository** for the COMPASS (Creative Output Management & Production Assistance System) fiction writing system. It contains ~127 Markdown files, Cursor IDE ACE configuration, and one standalone Python utility script. There are **no application services, no test suites, no build systems, and no web servers**.

### Linting

- **Markdown lint:** `markdownlint-cli2 "**/*.md"` from the workspace root. The repo has many existing lint warnings (mostly `MD032`, `MD022`, `MD036`); these are pre-existing and not caused by cloud agent changes.

### Python script

- The only executable code is `Misc/build_story_structure_mcp.py`, a standalone utility that converts story outlines to MCP-compatible JSON using the Anthropic API.
- It requires `pip install anthropic` and the `ANTHROPIC_API_KEY` environment variable (or interactive input). Without story source files (`Story_Bible/synopsis.md`, `Story_Bible/outline.md`), it exits gracefully with a non-zero code — this is expected behavior.

### Shell scripts

- All `.cursor/scripts/ace_*.sh` scripts are ACE (Adaptive Cursor Engine) lifecycle hooks for Cursor IDE. They are invoked by Cursor, not by the developer directly.
- `MCP_Setup/setup_mcp.sh` is an interactive setup script for GitKraken CLI and GitHub tokens — it prompts for user input and is not suitable for non-interactive/automated use.

### ACE configuration

- The `.cursor/rules/ace-patterns.mdc` rule file instructs agents to call `ace_search` MCP tool before implementation tasks. In Cloud Agent environments where this MCP tool is unavailable, this rule can be safely ignored.
