@@ -144,14 +144,18 @@ Sequential Thinking MAS uses multiple specialized agents (Factual, Emotional, Cr
 
 **//CLAUDE'S RESPONSE://** ✅ **CONFIRMED - ALL COMPLEMENTARY** - Sequential Thinking "brothers" work beautifully together: Base = simple logic checks, MAS = multi-perspective complex problems, Ultra = bias detection/quality scoring, Enhanced = mode-specific (creative/evaluative). ScaleMCP intelligently routes to the right tool. Think of them as tools in a toolkit - hammer, screwdriver, wrench - each for specific jobs. **RECOMMENDATION: Keep all four Sequential Thinking variants.**
 
-**Installation:**
+**Installation (corrected Aug 2026):** Python package — not npm. `@fradser/mcp-server-mas-sequential-thinking` is a registry **404**. Use:
+```bash
+pip install --user -r MCP_Implementations/sequential-thinking-mas/requirements.txt
+```
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
+Export host `DEEPSEEK_API_KEY` for tool calls. Details: `MCP_Implementations/sequential-thinking-mas/README.md`.
