@@ -6,6 +6,21 @@
 
 **Last compiled:** July 14, 2026, from the documentation in this repo (primarily `MCP_Research/MCP_COMPLETE_ACTIVE_LIST.md`, dated Jan 24, 2026). **Nothing below has been checked against your actual live `mcp.json` files** — this reflects what the docs say should be true, not a confirmed scan of your Mac. Treat the "Status" column accordingly until you've walked through and confirmed each one.
 
+### This repo’s project `mcp.json` (verified Aug 8, 2026)
+
+**Config path:** `.cursor/mcp.json` (not `.cursor/config/mcp.json`).  
+**Probe:** `bash MCP_Setup/probe_mcp_servers.sh` — all configured servers returned initialize + `tools/list` OK after the MAS / memory fixes (five after removing the stale structured clone).
+
+| MCP | Command | Handshake | Notes |
+|---|---|---|---|
+| sequential-thinking | `npx -y @modelcontextprotocol/server-sequential-thinking` | OK | Official Anthropic package; keep |
+| sequential-thinking-tools | `npx -y mcp-sequentialthinking-tools` | OK | Scratchpad + optional tool-plan validation; requires Node ≥22 |
+| knowledge-graph-memory | `bash MCP_Implementations/knowledge-graph-memory/run.sh` | OK | Absolute `MEMORY_FILE_PATH` to `.cursor/memory.json` (relative paths resolve under npx `dist/`, not the repo) |
+| sequential-thinking-mas | `bash MCP_Implementations/sequential-thinking-mas/run.sh` | OK | Needs host `DEEPSEEK_API_KEY` for tool calls; pin `agno==1.8.4` + package `0.2.3` (see launcher README). Do not set empty API key strings in `mcp.json`. |
+| fiction-reverse-engineering | `bash …/run.sh` | OK | Absolute formulas dir via launcher; `pip install -r MCP_Implementations/fiction-reverse-engineering/requirements.txt` |
+
+Removed from config: **`sequential-thinking-structured`** (`mcp-sequential-thinking`) — unofficial republish of the official tool, same `sequentialthinking` tool name, stale SDK pin. Use official `sequential-thinking` only.
+
 ---
 
 ## How to read the "Scope" column
