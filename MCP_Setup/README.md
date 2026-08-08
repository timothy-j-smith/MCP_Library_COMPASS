# MCP Setup Index

This folder contains MCP setup and configuration guidance for this workspace.

## Canonical facts (read first)

- **Project MCP config:** `.cursor/mcp.json` (not `.cursor/config/mcp.json`)
- **Current verified state:** `CURRENT_STATE.md` (includes the six servers probed in this repo)
- **Handshake probe:** `bash MCP_Setup/probe_mcp_servers.sh`
- **MAS sequential thinking:** Python package via `MCP_Implementations/sequential-thinking-mas/` — the npm name `@fradser/mcp-server-mas-sequential-thinking` does not exist on the public registry

## Canonical Setup Sequence

1. Review `CURRENT_STATE.md` for what is actually configured now.
2. Review `MCP_SETUP_INSTRUCTIONS.md` for baseline enable/disable flow.
3. Use `MCP_API_KEYS_AND_SETUP_REFERENCE.md` for credential and server reference details.
4. Use `MCP_SETUP_SUMMARY.md` only as a historical consolidated snapshot unless updated.

## Historical Snapshots

Some files in this folder are date-stamped completion snapshots (for example `*_COMPLETE*` and older `*_GUIDE*` sections).  
Treat those as historical context unless they are explicitly updated as current. Prefer `CURRENT_STATE.md` when they disagree.

## Professional Standard

- Keep one actively maintained "current state" document (`CURRENT_STATE.md`).
- Mark superseded setup snapshots clearly.
- Prefer reproducible instructions and explicit verification steps.
