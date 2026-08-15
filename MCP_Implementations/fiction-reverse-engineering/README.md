@@ -17,8 +17,9 @@ python3 -m venv .venv
 
 ## Cursor config
 
-Added to `.cursor/mcp.json` as `fiction-reverse-engineering`. Restart Cursor
-(or reload MCP servers) after install.
+Wired in `.cursor/mcp.json` via `run.sh` (resolves an absolute formulas dir and
+prefers a local `.venv` when present). Restart Cursor (or reload MCP servers)
+after install.
 
 ## Smoke test (analyzer only)
