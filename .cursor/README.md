@@ -5,9 +5,15 @@ and optional HTTP request guidance.
 
 ## Folder Layout
 
+- `mcp.json` - project MCP server definitions (stdio servers for this workspace)
+- `memory.json` - knowledge-graph-memory store (must be opened via
+  `MCP_Implementations/knowledge-graph-memory/run.sh` so the path is absolute;
+  a relative `MEMORY_FILE_PATH` writes into the npx package cache instead)
 - `rules/` - always-applied guidance and guardrails for this workspace
 - `http/` - request-file guidance for HTTP request artifacts
 
+To verify every entry in `mcp.json` can initialize: `bash MCP_Setup/probe_mcp_servers.sh`.
+
 ## Cursor 3 Agent Workflow in This Template
 
 Use this operating model for consistency: