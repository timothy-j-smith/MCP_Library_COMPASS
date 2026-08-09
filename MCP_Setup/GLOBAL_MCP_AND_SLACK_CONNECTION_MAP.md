# Global MCP + Slack Connection Map

**Purpose:** Connect Slack (and Slackbot) to Cursor once, so it works in **every** repo — not only this COMPASS library or a single Slack-related project. Same rule applies to every other MCP: decide **global vs project** by whether the config is repo-specific.

**Last updated:** August 9, 2026

---

## The rule that unlocks all repos

| Scope | File | Who sees it |
|-------|------|-------------|
| **Global (personal, all projects)** | `~/.cursor/mcp.json` | You, in every Cursor workspace |
| **Project (one repo)** | `.cursor/mcp.json` inside that repo | Anyone who opens that repo (safe to commit if no secrets) |
| **Team / Cloud Agents** | Cursor Dashboard → **Integrations & MCP** | Cloud Agents + optional Team Marketplace |

Cursor **merges** global + project configs. If the same server name appears in both, **project wins**.

**If Slack only lives in one repo’s `.cursor/mcp.json`, you are restricted to that repo.** Put Slack in **global** (or Team MCP) instead.

---

## Recommended layout

```text
~/.cursor/mcp.json          ← Slack, GitHub, Linear, Exa, Firecrawl, Sequential Thinking, …
                              (anything that does NOT point at one novel/repo folder)

repo-A/.cursor/mcp.json     ← filesystem roots, MEMORY_FILE_PATH, novel-specific style MCPs
repo-B/.cursor/mcp.json     ← same pattern for that repo only
COMPASS/.cursor/mcp.json    ← fiction-reverse-engineering + other COMPASS-local servers
```

**Scope test:** If neither `args` nor `env` names a path/file unique to one project, put it in **global**. If it does (novel folder, `MEMORY_FILE_PATH`, local `server.py` inside the repo), put it in **project**.

---

## Part 1 — Connect Slack + Slackbot (all Cursor repos)

Pick **one** primary path. Prefer A for modern OAuth; use B if you already have a Slack App bot token.

### Option A — Official Slack remote MCP (OAuth, recommended)

Works across all repos when added to **global** `~/.cursor/mcp.json` (or via Cursor Settings → Tools & MCP, which writes the same place for personal servers).

1. Workspace admin must allow Slack MCP / Agents & AI Apps if your org gates that.
2. In Cursor Desktop: **Settings → Cursor Settings → Tools & MCP** → add Slack, or put this in `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "slack": {
      "url": "https://mcp.slack.com/mcp",
      "auth": {
        "CLIENT_ID": "3660753192626.8903469228982"
      }
    }
  }
}
```

3. Click **Connect** next to the Slack server and finish OAuth in the browser.
4. Reload Cursor (**Cmd/Ctrl+Shift+P → Reload Window**).
5. Verify in any repo (not just COMPASS): ask the agent to list recent messages in a channel you can access.

Notes:

- Desktop OAuth callback: `http://localhost:8787/callback`
- Web / Cloud Agents callback: `https://www.cursor.com/agents/mcp/oauth/callback`
- Do **not** also define a project-level `"slack"` entry unless you intentionally want that one repo to override global.

### Option B — Slackbot via Bot Token (stdio package)

Use when you created a Slack App and have `xoxb-…` + Team ID (`T…`).

1. Create/install a Slack App at [api.slack.com/apps](https://api.slack.com/apps).
2. Bot Token Scopes (minimum): `channels:history`, `channels:read`, `chat:write`, `reactions:write`, `users:read`, `users.profile:read`.
3. Install to workspace → copy **Bot User OAuth Token** (`xoxb-…`).
4. Team ID: Slack → workspace menu → **Settings & administration → Workspace settings** (URL contains `/T…`) or from the app’s install page.
5. Invite the bot to channels it should read/write (`/invite @YourBot`).
6. Put tokens in your shell profile (not in git):

```bash
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_TEAM_ID="T..."
```

7. Add to **global** `~/.cursor/mcp.json` (not a single project file):

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${env:SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "${env:SLACK_TEAM_ID}"
      }
    }
  }
}
```

Optional: `SLACK_CHANNEL_IDS` to limit which channels are listed.

8. Restart Cursor and test from two different repos to confirm it is global.

### Option C — Zapier MCP Slack actions

Use when you want Slack **plus** Gmail/Calendar/etc. from one connector.

1. Install/connect Zapier MCP in **Settings → Tools & MCP**.
2. At [mcp.zapier.com](https://mcp.zapier.com) enable Slack actions (e.g. Find Message, Send Channel Message).
3. Prefer **native Slack MCP** (A/B) for Slack-heavy work; don’t run the same Slack send through both Zapier and native Slack for one action.

### Cloud Agents / every repo in the team

Personal `~/.cursor/mcp.json` does **not** automatically follow you into Cloud Agent VMs.

To expose Slack (and other shared MCPs) to Cloud Agents across repositories:

1. Cursor Dashboard → **Integrations & MCP** (Team MCP).
2. Add the Slack server there.
3. Optionally **Add to Team Marketplace** so IDE/CLI teammates can install the same server from Customize.

---

## Part 2 — Connection map for all MCPs

Use this when adding any new MCP. Goal: never re-bind a shared tool to one “Slate/Slack/COMPASS” repo by accident.

### Global by default (put in `~/.cursor/mcp.json`)

| MCP | Why global | Auth / env |
|-----|------------|------------|
| **slack** | Workspace comms, not repo-owned | OAuth (Option A) or `SLACK_BOT_TOKEN` + `SLACK_TEAM_ID` (Option B) |
| **github** / GitKraken | Multi-repo git | `GITHUB_TOKEN` / `gk auth login` |
| **linear** | Issue tracking across products | Remote OAuth (`https://mcp.linear.app/mcp`) |
| **exa** / brave-search / duckduckgo / firecrawl | Web research | API keys as needed |
| **sequential-thinking*** | Generic reasoning | None |
| **perplexity**, **figma**, **supabase**, etc. | Cross-project services | See `MCP_API_KEYS_AND_SETUP_REFERENCE.md` |
| **open-library** / literary lookup | Shared research | Usually none / API key |

\*Variants that don’t write novel-specific memory files.

### Project-only (put in that repo’s `.cursor/mcp.json`)

| MCP | Why project | Config cue |
|-----|-------------|------------|
| **filesystem** (named novel/root) | Path *is* the config | Absolute folder in `args` |
| **knowledge-graph-memory** | Must not mix novels | `MEMORY_FILE_PATH` per project |
| **fiction-reverse-engineering** | Lives in this repo | Local `server.py` path |
| **book-series** / writer DB tools | DB + story data | `DATABASE_URL` / story-specific |
| Novel style MCPs (e.g. Dennis Lehane) | Story-specific | Local implementation path |

### Merge / override pitfalls

| Mistake | Result | Fix |
|---------|--------|-----|
| Slack only in `COMPASS/.cursor/mcp.json` | Missing in other repos | Move Slack to `~/.cursor/mcp.json` |
| Same name `"slack"` in project + global | Project silently overrides | Remove project copy unless intentional |
| Secrets committed in project `mcp.json` | Token leak | Use `${env:…}` + shell/Cursor secrets |
| Expecting Cloud Agent to see personal global MCP | Tools missing in cloud | Add Team MCP / dashboard secrets |

---

## Part 3 — Copy-paste global starter template

Merge with any servers you already have. Keep secrets in the environment.

```json
{
  "mcpServers": {
    "slack": {
      "url": "https://mcp.slack.com/mcp",
      "auth": {
        "CLIENT_ID": "3660753192626.8903469228982"
      }
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_TOKEN}"
      }
    }
  }
}
```

Leave novel-specific and COMPASS-local servers in each repo’s `.cursor/mcp.json` (this repo already has fiction-reverse-engineering there).

---

## Part 4 — Verify you are not locked to one repo

1. Confirm Slack appears under **Tools & MCP** with scope that is not “this folder only.”
2. Open **Repo A** → ask Cursor to use Slack (list channels / find a message).
3. Open **Repo B** (unrelated) → repeat the same Slack ask.
4. If it works only in one repo, search that repo’s `.cursor/mcp.json` for `"slack"` and remove the project-only entry after global is set.
5. For Cloud Agents: run an agent on a second repository and confirm Slack tools appear (Team MCP required).

---

## Quick decision flowchart

```text
New MCP to connect
        │
        ├─ Does config/env point at ONE repo or novel folder?
        │         yes → project `.cursor/mcp.json`
        │         no  → global `~/.cursor/mcp.json`
        │
        ├─ Need it in Cloud Agents across many repos?
        │         yes → also add under Dashboard → Integrations & MCP
        │
        └─ Is it Slack?
                  → Prefer Option A (official remote) in GLOBAL
                  → Invite Slackbot to channels if using Option B
```

---

## Related docs in this repo

- `CURRENT_STATE.md` — what’s believed active + scope column
- `MCP_FILESYSTEM_SETUP_GUIDE.md` — global vs project path rule (novels)
- `MCP_API_KEYS_AND_SETUP_REFERENCE.md` — env vars per MCP
- Cursor docs: [cursor.com/docs/mcp](https://cursor.com/docs/mcp)
