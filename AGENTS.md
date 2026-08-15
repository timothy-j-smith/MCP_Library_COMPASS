@@ -7,9 +7,12 @@ COMPASS (Creative Output Management \u0026 Production Assistance System) is a **docum
 ### Repository contents
 
 - ~127 Markdown files: research notes, setup guides, session analysis, style MCP docs
-- `MCP_Implementations/fiction-reverse-engineering/`: Fiction Reverse Engineering MCP (local Python MCP server; tools for pacing/formula analysis). Configured in `.cursor/mcp.json` as `fiction-reverse-engineering`. Requires `pip install -r MCP_Implementations/fiction-reverse-engineering/requirements.txt` (package: `mcp`).
+- `MCP_Implementations/fiction-reverse-engineering/`: Fiction Reverse Engineering MCP (local Python MCP server; tools for pacing/formula analysis). Configured in `.cursor/mcp.json` as `fiction-reverse-engineering` via `run.sh` (absolute formulas dir). Requires `pip install -r MCP_Implementations/fiction-reverse-engineering/requirements.txt` (package: `mcp`).
+- `MCP_Implementations/sequential-thinking-mas/`: Launcher + pinned deps for the MAS sequential-thinking MCP (`mcp-server-mas-sequential-thinking==0.2.3` + `agno==1.8.4`). Configured in `.cursor/mcp.json` via `run.sh`. Host must supply `DEEPSEEK_API_KEY` (or another provider key) for tool calls; see that folder’s README.
+- `MCP_Implementations/knowledge-graph-memory/`: Launcher for `@modelcontextprotocol/server-memory` that forces an absolute `MEMORY_FILE_PATH` (relative paths write into the npx package cache).
 - `Misc/build_story_structure_mcp.py`: Python utility that converts story synopsis/outline to MCP JSON format (requires the `anthropic` package and an `ANTHROPIC_API_KEY`)
 - `MCP_Setup/setup_mcp.sh`: interactive Bash script for setting up GitKraken CLI and GitHub token (not suitable for non-interactive execution)
+- `MCP_Setup/probe_mcp_servers.sh`: non-interactive JSON-RPC handshake probe for every server in `.cursor/mcp.json`
 - `.cursor/scripts/`: ACE framework session-tracking hooks
 - `.cursor/rules/ace-patterns.mdc`: workspace rule requiring `ace_search` MCP tool calls
