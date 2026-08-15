@@ -133,17 +133,19 @@
 ## TIER 3: HIGHLY RECOMMENDED - ADD WHEN READY (Advanced Capabilities)
 
 ### 12. Sequential Thinking MAS (Multi-Agent System) ⭐⭐⭐⭐⭐
-**Status:** ⚠️ **NEEDS SETUP**  
+**Status:** ⚠️ **NEEDS SETUP** (Python package + provider API key)  
 **Priority:** HIGHLY RECOMMENDED - Multi-perspective reasoning  
 **Setup Instructions:**
-1. Add to `.cursor/config/mcp.json`:
+1. `pip install --user -r MCP_Implementations/sequential-thinking-mas/requirements.txt`
+2. Add to `.cursor/mcp.json` (npm `@fradser/mcp-server-mas-sequential-thinking` is a **404** — do not use):
 ```json
 "sequential-thinking-mas": {
-  "command": "npx",
-  "args": ["-y", "@fradser/mcp-server-mas-sequential-thinking"],
-  "disabled": false
+  "command": "bash",
+  "args": ["MCP_Implementations/sequential-thinking-mas/run.sh"],
+  "env": { "LLM_PROVIDER": "deepseek" }
 }
 ```
+3. Export host `DEEPSEEK_API_KEY` (tool calls). See `MCP_Implementations/sequential-thinking-mas/README.md`.
