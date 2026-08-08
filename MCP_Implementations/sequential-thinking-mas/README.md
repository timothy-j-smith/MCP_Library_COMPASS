# Sequential Thinking MAS (launcher)

Wrapper + pinned deps for the
[`mcp-server-mas-sequential-thinking`](https://pypi.org/project/mcp-server-mas-sequential-thinking/)
MCP used by this workspace’s `.cursor/mcp.json`.

## Why this folder exists

A bare `mcp-server-mas-sequential-thinking` entry fails in common setups:

1. **Agno API break** — PyPI `0.2.3` imports `agno.tools.thinking.ThinkingTools`,
   which was removed in Agno 2.x. Pin `agno==1.8.4`.
2. **Empty API key override** — `"DEEPSEEK_API_KEY": ""` in `mcp.json` clears a
   real host env var and breaks the provider.
3. **Hard `EXA_API_KEY` at init** — PyPI `0.2.3` constructs `ExaTools()` during
   startup. The launcher supplies a non-secret placeholder when unset so the
   MCP can connect; set a real Exa key for research.

Newer GitHub releases (e.g. `v0.8.0`) move to `ReasoningTools` and optional Exa,
but currently fail against `mcp` 1.28 with
`ModuleNotFoundError: mcp.server.mcpserver`. Stay on the pinned PyPI pair until
upstream is verified.

**Note:** The npm package `@fradser/mcp-server-mas-sequential-thinking` does
**not** exist on the public registry (404). Install the Python package.

## Install

```bash
pip install --user -r MCP_Implementations/sequential-thinking-mas/requirements.txt
```

## Configure

`.cursor/mcp.json` should launch via this script and **must not** set empty
API key strings:

```json
"sequential-thinking-mas": {
  "command": "bash",
  "args": [
    "MCP_Implementations/sequential-thinking-mas/run.sh"
  ],
  "env": {
    "LLM_PROVIDER": "deepseek"
  }
}
```

Set in the **host environment** (not committed):

| Variable | Required for | Notes |
|----------|--------------|-------|
| `DEEPSEEK_API_KEY` | Tool calls when `LLM_PROVIDER=deepseek` | Other providers: `GROQ_API_KEY`, `OPENROUTER_API_KEY`, etc. |
| `EXA_API_KEY` | Live Exa research | Optional; placeholder used only so the process can start |

## Verify

```bash
bash MCP_Setup/probe_mcp_servers.sh
```

Expect `sequential-thinking-mas` → `OK` (initialize + `tools/list`).
