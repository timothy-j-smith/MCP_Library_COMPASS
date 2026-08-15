@@ -8,7 +8,8 @@
 
 **To disable an MCP server:** Add `"disabled": true` to its config  
 **To enable an MCP server:** Set `"disabled": false` or remove the disabled field  
-**Config location:** `.cursor/config/mcp.json` (project) or `~/.cursor/mcp.json` (global)
+**Config location:** `.cursor/mcp.json` (project; canonical for this repo) or `~/.cursor/mcp.json` (global)  
+**Note:** Older docs saying `.cursor/mcp.json` are outdated — use `.cursor/mcp.json`.
 
 ---
 
@@ -84,7 +85,7 @@ echo $GITHUB_TOKEN
 ### 3. Update MCP Configuration
 
 The configuration is already set up in:
-- **Project:** `.cursor/config/mcp.json`
+- **Project:** `.cursor/mcp.json`
 - **Global:** `~/.cursor/mcp.json` (optional backup)
 
 **All servers are disabled by default except `walk-this-way-files`.**
@@ -234,7 +235,7 @@ curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
 ```
 
 ### MCP Server Not Loading
-1. Check for JSON syntax errors in `.cursor/config/mcp.json`
+1. Check for JSON syntax errors in `.cursor/mcp.json`
 2. Restart Cursor completely
 3. Check Cursor logs: Help → Toggle Developer Tools → Console
 
@@ -244,7 +245,7 @@ curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
 
 **Project MCP Config:**
 ```
-.cursor/config/mcp.json
+.cursor/mcp.json
 ```
 
 **Global MCP Config (backup):**
