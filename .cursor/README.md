# .cursor Configuration Guide

This folder contains project-level Cursor configuration for workspace rules
and optional HTTP request guidance.

## Folder Layout

- `mcp.json` - project MCP server definitions (stdio servers for this workspace)
- `memory.json` - knowledge-graph-memory store (`MEMORY_FILE_PATH`)
- `rules/` - always-applied guidance and guardrails for this workspace
- `http/` - request-file guidance for HTTP request artifacts

To verify every entry in `mcp.json` can initialize: `bash MCP_Setup/probe_mcp_servers.sh`.

## Cursor 3 Agent Workflow in This Template

Use this operating model for consistency:

- **Ask mode**: research, planning, and analysis without file edits
- **Agent mode**: implementation, edits, testing, and git operations
- **Background agent**: longer-running autonomous work with full lifecycle
  ownership

## Notes

- Advanced telemetry add-ons are intentionally omitted from this template.
- Keep `.cursor` configuration lightweight and stable.
