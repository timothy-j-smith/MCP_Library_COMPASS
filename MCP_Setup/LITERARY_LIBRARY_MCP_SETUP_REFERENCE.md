# Literary Library MCPs: Setup Reference (Open Library + Google Books)
> **Config path note (Aug 2026):** Canonical project MCP config is `.cursor/mcp.json`. Older `.cursor/config/mcp.json` mentions in this snapshot are historical.

**Date:** July 14, 2026
**Purpose:** Copy-paste config blocks to wire the two book/library-lookup MCPs into Cursor, Claude Desktop, and Claude Code. Do this on your local machine — these files don't exist in the cloud session that generated this doc.

---

## Recommended order

1. **Open Library MCP first.** No account, no API key — best way to confirm the whole chain (client → server → tool call → response) works before adding a second server.
2. **Google Books MCP second, only if needed.** It's a redundant second source for the same kind of data (per `MCP_Research/MCPs_ADDITIONAL_CONSIDERATION_CATEGORIZED.md`) and needs a `GOOGLE_API_KEY` plus a local Python clone — more setup for overlapping value.

---

## 1. Open Library MCP (`@8enSmith/mcp-open-library`)

No API key. Searches by title/author/ISBN, returns author bios, covers, edition history.

### Cursor — project-level config
File: `.cursor/config/mcp.json` (matches your existing `walk-this-way-files` pattern)

```json
{
  "mcpServers": {
    "open-library": {
      "command": "npx",
      "args": ["-y", "@8enSmith/mcp-open-library"],
      "disabled": false
    }
  }
}
```

### Claude Desktop
File (Mac): `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "open-library": {
      "command": "npx",
      "args": ["-y", "@8enSmith/mcp-open-library"]
    }
  }
}
```

### Claude Code (CLI)
```bash
claude mcp add open-library -- npx -y @8enSmith/mcp-open-library
```
Or add the same block as above to a project `.mcp.json`.

### HyperAgent
Not referenced anywhere in this repo, and its MCP-loading convention may not match the `mcpServers` shape above — check HyperAgent's own docs/README before wiring this in rather than assuming the Cursor/Claude format applies.

### Test prompt (any client)
> "Search Open Library for Dennis Lehane's *Mystic River* and give me the ISBN and a cover image URL."

If you get real data back (not a hallucinated guess), the tool call fired correctly.

---

## 2. Google Books MCP (`juanbeniteza/mcp-google-books`)

Needs a `GOOGLE_API_KEY` and a local Python install — this one is not a plain `npx` package.

### Setup steps
```bash
git clone https://github.com/juanbeniteza/mcp-google-books.git
cd mcp-google-books
# follow the repo's README for its install command (pip/poetry/uv — check repo)
```
Get a key: [Google Cloud Console](https://console.cloud.google.com/) → enable the **Books API** → create an API key.

### Config (Cursor `.cursor/config/mcp.json` — same shape for Claude Desktop/Code)
```json
{
  "mcpServers": {
    "google-books": {
      "command": "/path/to/mcp-google-books/venv/bin/python",
      "args": ["/path/to/mcp-google-books/server.py"],
      "env": {
        "GOOGLE_API_KEY": "your_key_here"
      },
      "disabled": false
    }
  }
}
```
Replace `command`/`args` with whatever the repo's own run instructions specify — the placeholder above is a guess at the pattern, confirm against the actual README before relying on it.

### Test prompt
> "Use Google Books to look up comp titles for a literary crime novel set in 1970s Boston."

---

## Verification checklist (either MCP)

- [ ] Config saved in the right file for the client you're testing
- [ ] `"disabled": false` (or key omitted entirely if the client doesn't use that field)
- [ ] Client fully restarted (not just reloaded)
- [ ] Client's MCP status panel shows the server as active/green
- [ ] Test prompt returns real, verifiable data (not a plausible-sounding guess)

Once one client works, copy the same server block into the other two — you're not "connecting" one MCP to three clients, you're repeating the same server definition in three separate config files, and each client spawns its own instance of the process.
