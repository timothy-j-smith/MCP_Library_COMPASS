# .cursor Configuration Guide

This folder contains project-level Cursor configuration for rules, command helpers, and session hooks used by agent workflows.

## Folder Layout

- `rules/` - always-applied guidance and guardrails for this workspace
- `commands/` - slash-command helper docs for ACE workflows
- `scripts/` - hook scripts for session lifecycle and trajectory capture
- `ace/` - local ACE runtime state and trajectory files
- `http/` - request-file guidance for HTTP request artifacts

## Cursor 3 Agent Workflow in This Template

Use this operating model for consistency:

- **Ask mode**: research, planning, and analysis without file edits
- **Agent mode**: implementation, edits, testing, and git operations
- **Background agent**: longer-running autonomous work with full lifecycle ownership

## Rules and Commands

- Start with `rules/ace-patterns.mdc` for required ACE usage
- Use `rules/ace-domain-search.md` and `rules/ace-continuous-search.md` for follow-on searches
- Use `commands/ace-help.md` for the current command/tool reference

## Session Hooks

Scripts in `scripts/` track session trajectories:

- `ace_session_start.sh` initializes session context
- `ace_track_mcp.sh`, `ace_track_shell.sh`, `ace_track_response.sh`, `ace_track_edit.sh` record activity
- `ace_session_end.sh` writes session analytics

Do not treat files under `ace/` as durable documentation; they are runtime artifacts.
