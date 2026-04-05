# ACE Help

Available ACE commands and MCP tools.

## Slash Commands

- `/ace-status` - Show playbook statistics
- `/ace-search <query>` - Search for patterns
- `/ace-configure` - Configure ACE connection (opens UI)
- `/ace-bootstrap` - Initialize playbook from codebase
- `/ace-learn` - Capture learning from completed task
- `/ace-help` - Show this help

## MCP Tools (Use These Directly)

- `ace_search(query)` - Search for relevant patterns (call first for normal task flow)
- `ace_list_domains()` - Discover valid semantic domains for filtered searches
- `ace_learn(task, trajectory, output, success, git?)` - Capture learning after substantial work
- `ace_bootstrap(mode, thoroughness)` - Initialize playbook
- `ace_status()` - Get playbook statistics
- `ace_get_playbook()` - Full playbook export/reference (not default for normal task starts)

## Recommended Flow

1. Start with `ace_search` using a task-aligned query.
2. If needed, call `ace_list_domains` and run a domain-filtered `ace_search`.
3. Complete implementation/testing work.
4. After session summary/AI-Trail context is available, call `ace_learn` once.

## UI Commands (Command Palette)

Press `Cmd/Ctrl+Shift+P` and type "ACE" to see:
- ACE: Login / Logout
- ACE: Configure Connection
- ACE: Show Status
- ACE: Manage Devices