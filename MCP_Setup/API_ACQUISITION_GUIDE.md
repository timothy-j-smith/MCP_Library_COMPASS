@@ -151,7 +151,7 @@
 ### **Where to Store API Keys:**
 
 **Option 1: Cursor Environment Variables (Recommended)**
- Cursor automatically reads `env:VARIABLE_NAME` from your system
+ Cursor can interpolate `"${env:VARIABLE_NAME}"` from the host environment (omit the key entirely to inherit; never set `""`)
 - Set in your shell profile (`.zshrc` or `.bash_profile`)
 
 **Option 2: Direct in mcp.json (Not Recommended)**
@@ -266,8 +266,8 @@ curl -X POST "https://api.vectara.io/v1/query" \
 1. **Restart Cursor** (to load environment variables)
 
 2. **Check MCP Configuration:**
 -   - Open `.cursor/config/mcp.json`
 -   - Verify all `env:VARIABLE_NAME` references are correct
+   - Open `.cursor/mcp.json`
+   - Verify all `"${env:VARIABLE_NAME}"` references are correct (and none are empty strings)
 
 3. **Test MCPs:**
    - Try using Style Emulation MCP
@@ -307,7 +307,7 @@ curl -X POST "https://api.vectara.io/v1/query" \
 
 ### **DO:**
 - ✅ Store API keys in environment variables
 - ✅ Use `env:VARIABLE_NAME` in mcp.json
+- ✅ Use `"${env:VARIABLE_NAME}"` in mcp.json (or omit and inherit host env)
 - ✅ Never commit API keys to Git
 - ✅ Rotate keys periodically
 - ✅ Use different keys for different projects
@@ -332,7 +332,7 @@ curl -X POST "https://api.vectara.io/v1/query" \
 
 ### **Problem: MCP not connecting**
 **Solution:**
 -1. Check MCP configuration in `.cursor/config/mcp.json`
+1. Check MCP configuration in `.cursor/mcp.json`
 2. Verify environment variable name matches
 3. Check MCP server logs
 4. Restart Cursor
