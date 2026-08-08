# MCP Current State — Read This First

**Purpose:** Every other doc in this repo is a snapshot of a conversation — an evaluation, a "consider this," an archived idea. This file is different: it's meant to be the one place that says *what's actually true right now*, so that when you come back after a few months, you open this file first instead of re-reading 60 markdown files to reconstruct what you built and why.

**This only works if you keep it honest.** When you add, remove, or change an MCP on your actual machine, update the row here. If a row hasn't been touched in months and you're not sure it's still accurate, that's a signal to verify it, not to trust it blindly — mark it `NEEDS VERIFICATION` rather than leave stale info looking authoritative.

**Last compiled:** July 14, 2026, from the documentation in this repo (primarily `MCP_Research/MCP_COMPLETE_ACTIVE_LIST.md`, dated Jan 24, 2026). **Nothing below has been checked against your actual live `mcp.json` files** — this reflects what the docs say should be true, not a confirmed scan of your Mac. Treat the "Status" column accordingly until you've walked through and confirmed each one.

### This repo’s project `mcp.json` (verified Aug 8, 2026)

**Config path:** `.cursor/mcp.json` (not `.cursor/config/mcp.json`).  
**Probe:** `bash MCP_Setup/probe_mcp_servers.sh` — all configured servers returned initialize + `tools/list` OK after the MAS / memory fixes (five after removing the stale structured clone).

| MCP | Command | Handshake | Notes |
|---|---|---|---|
| sequential-thinking | `npx -y @modelcontextprotocol/server-sequential-thinking` | OK | Official Anthropic package; keep |
| sequential-thinking-tools | `npx -y mcp-sequentialthinking-tools` | OK | Scratchpad + optional tool-plan validation; requires Node ≥22 |
| knowledge-graph-memory | `bash MCP_Implementations/knowledge-graph-memory/run.sh` | OK | Absolute `MEMORY_FILE_PATH` to `.cursor/memory.json` (relative paths resolve under npx `dist/`, not the repo) |
| sequential-thinking-mas | `bash MCP_Implementations/sequential-thinking-mas/run.sh` | OK | Needs host `DEEPSEEK_API_KEY` for tool calls; pin `agno==1.8.4` + package `0.2.3` (see launcher README). Do not set empty API key strings in `mcp.json`. |
| fiction-reverse-engineering | `bash …/run.sh` | OK | Absolute formulas dir via launcher; `pip install -r MCP_Implementations/fiction-reverse-engineering/requirements.txt` |

Removed from config: **`sequential-thinking-structured`** (`mcp-sequential-thinking`) — unofficial republish of the official tool, same `sequentialthinking` tool name, stale SDK pin. Use official `sequential-thinking` only.

---

## How to read the "Scope" column

Two places an MCP's config can live, and the test for which one applies (worked out the hard way — see `MCP_FILESYSTEM_SETUP_GUIDE.md`):

| Scope | Lives in | Test |
|---|---|---|
| **Global** | `~/.cursor/mcp.json` (Cursor) or `claude_desktop_config.json` (Claude Desktop) — set up once | Neither `args` nor `env` names a path/file specific to one novel |
| **Project-specific** | `.cursor/mcp.json` inside that project/novel folder (canonical Cursor path; older docs saying `.cursor/config/mcp.json` are outdated) | `args` or `env` (e.g. a data file, a `MEMORY_FILE_PATH`, a filesystem root) points at *this* novel's folder |

---

## Core Infrastructure

| MCP | What it does (one line) | Scope | Config location | Status |
|---|---|---|---|---|
| **Filesystem** (`walk-this-way-files`) | Lets the client read/write the novel folder directly | Project-specific | `.cursor/mcp.json` per novel | Documented active — **only matters in Claude Desktop**; redundant in Cursor if the folder is already the open workspace (see correction in `MCP_FILESYSTEM_SETUP_GUIDE.md`) |
| **Sequential Thinking** (base) | Step-by-step reasoning scaffold for plot/structure analysis | Global | `~/.cursor/mcp.json` | Documented active — verify it isn't currently duplicated into every novel's project config (it was, per the old template) |
| **Knowledge Graph Memory** | Persistent character/plot memory across sessions | Project-specific *(via absolute `MEMORY_FILE_PATH`, not the package itself)* | `.cursor/mcp.json` per novel | In this repo: `MCP_Implementations/knowledge-graph-memory/run.sh` → `.cursor/memory.json`. Relative paths write into the npx cache — always use absolute. |
| **GitHub** | Repo operations (PRs, issues, commits) | Global | `~/.cursor/mcp.json` | Needs `GITHUB_TOKEN` |
| **GitKraken** | Enhanced git operations with AI | Global | `~/.cursor/mcp.json` | Documented active, no key needed |
| **DuckDuckGo Search** | Quick web search / fact-checking | Global | `~/.cursor/mcp.json` | Documented active, no key |
| **Pandoc** | Document format conversion | Global | `~/.cursor/mcp.json` | Needs Pandoc installed (`brew install pandoc`) |

---

## Custom, Novel-Specific Writing MCPs

| MCP | What it does | Scope | Real code location | Status |
|---|---|---|---|---|
| **COMPASS Writing Guides** | Custom server exposing your craft rules, style guide, character frameworks | Project-specific *if* each novel has its own `zz_COMPASS/` copy; global if one shared install | `/path/to/COMPASS_Writing_Guides_MCP/server.py` (placeholder in every doc found — **never confirmed with a real path**) | **NEEDS VERIFICATION** — confirm `server.py` actually exists at the path in your real config; see gap noted in `MCP_FILESYSTEM_SETUP_GUIDE.md` |
| **Dennis Lehane Style** | Private style-analysis MCP built from *Mystic River* / *Gone Baby Gone* for Walk This Way specifically | Project-specific (novel-specific by design) | `zz_COMPASS/MCP_Implementations/DENNIS_LEHANE_MCP/server.py` | Documented "server.py created, ready to test" — confirm it still runs |
| **Style Emulation** | General style analysis/transformation (sentence length, voice blending, consistency checks) | Global (not novel-specific in concept, though your instance may differ) | `~/mcp-servers/style-emulation-mcp/` | Documented as code-complete but requiring manual install; confirm it was actually installed, not just drafted |

---

## Literary Library Lookup (added July 14, 2026)

| MCP | What it does | Scope | Status |
|---|---|---|---|
| **Open Library** | Book/author search via Internet Archive — no key | Global | Set up per `MCP_Setup/LITERARY_LIBRARY_MCP_SETUP_REFERENCE.md` — confirm which clients you actually added it to |
| **Google Books** | Second book/author metadata source | Global | Needs `GOOGLE_API_KEY` + local Python clone — only add if Open Library proves insufficient |

---

## Research & Semantic Search

| MCP | What it does | Scope | Status |
|---|---|---|---|
| **Firecrawl** | Primary web research / scraping tool | Global | Needs `FIRECRAWL_API_KEY` |
| **Vectara** | Semantic search / RAG over your own documents | Global | Needs `VECTARA_API_KEY`, `VECTARA_ENV` |
| **Cognee** | Graph-RAG, surfaces hidden connections in your writing | Global (or project-specific if data dir is per-novel — check its config) | Needs `pip install cognee` |
| **UltraRAG** | Custom-trains retrieval on your own manuscript | Likely project-specific (trains on *this* novel's text) | Needs `pip install ultrarag` |
| **RAGentA** | Multi-agent verification layer | — | Documented as possibly unavailable as a package — disable if so |

---

## Memory / Orchestration Extras

*(Documented as "ready after restart" — one-line purposes only, not independently verified here. Worth pruning if you don't actually recall using most of these.)*

| MCP | Purpose (as documented) |
|---|---|
| sequential-thinking-mas | Multi-agent sequential reasoning — **in this repo:** launch via `MCP_Implementations/sequential-thinking-mas/run.sh` + pinned deps; needs host `DEEPSEEK_API_KEY` for tool calls |
| sequential-thinking-ultra | Bias detection, quality metrics |
| enhanced-sequential-thinking | 19 reasoning modes |
| memorygraph | Context optimization |
| enhanced-mcp-memory | Learns prose style over time |
| supermemory | Cross-platform memory continuity |
| scalemcp | MCP orchestration |
| ai-writers-workshop | Narrative-pattern learning |
| anki-flashcards | Spaced-repetition flashcards for character/plot facts (needs Anki app) |

---

## Disabled / Optional

| MCP | Why it's off |
|---|---|
| google-workspace | Needs OAuth setup; only useful for cloud collaboration |
| workflow-automation (n8n) | Needs a running n8n instance; automation nice-to-have, not core |
| zen-orchestrator | Needs repo clone + 3 separate API keys; multi-model orchestration, heavy setup for the payoff |

---

## Immediate To-Do (next time you sit down with this)

- [ ] Confirm `compass-writing-guides` actually points at a real, existing `server.py` — this is the biggest open question from today's review.
- [ ] Confirm `knowledge-graph-memory` has a per-novel `MEMORY_FILE_PATH` set, not a shared default.
- [ ] Decide whether `sequential-thinking` is still duplicated into every novel's project config (it should be global-only).
- [ ] Walk through the "Memory / Orchestration Extras" table and cut anything you don't remember actually using — a shorter, accurate list beats a long unverified one.
- [ ] Re-run this file's compilation after you've verified the above, and update "Last compiled" at the top.
