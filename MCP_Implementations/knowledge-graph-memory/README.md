# Knowledge Graph Memory (launcher)

Wrapper for `@modelcontextprotocol/server-memory` so persistence lands in this
workspace.

## Why this folder exists

That server resolves a **relative** `MEMORY_FILE_PATH` against its own package
`dist/` directory (under the npx cache), not the project cwd. Configuring
`".cursor/memory.json"` therefore fails on write with `ENOENT` under
`…/server-memory/dist/.cursor/…` and never updates the repo file.

This launcher always exports an **absolute** path (default:
`<repo>/.cursor/memory.json`).

## Configure

`.cursor/mcp.json`:

```json
"knowledge-graph-memory": {
  "command": "bash",
  "args": [
    "MCP_Implementations/knowledge-graph-memory/run.sh"
  ]
}
```

Override the store location with an absolute path if needed:

```bash
MEMORY_FILE_PATH=/absolute/path/to/novel-memory.jsonl \
  bash MCP_Implementations/knowledge-graph-memory/run.sh
```

The on-disk format is JSONL (one entity/relation object per line), even when
the filename ends in `.json`.
