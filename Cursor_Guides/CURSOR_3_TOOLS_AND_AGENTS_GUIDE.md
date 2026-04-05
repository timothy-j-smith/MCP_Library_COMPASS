# Cursor 3 Tools and Agents Guide

Professional operational reference for this workspace template.

## Purpose

Use this guide as the canonical Cursor 3 workflow baseline for:

- choosing Ask vs Agent execution paths
- using built-in tools safely and effectively
- integrating MCP tools into repeatable workflows
- running autonomous, professional execution loops

## Operating Modes

### Ask Mode (analysis-first, no edits)

Use Ask mode when you need:

- discovery and scoping
- architecture review
- risk analysis
- documentation synthesis

Deliverables in Ask mode are recommendations, plans, and findings.  
Do not claim implementation/testing completion if no edits were performed.

### Agent Mode (implementation + validation)

Use Agent mode when work requires:

- file edits
- testing and verification
- debugging and iteration
- git operations and handoff artifacts

Agent mode should include concrete evidence (tests, logs, and artifacts where relevant).

### Background Agent (long-running autonomous execution)

Use background execution for larger or multi-step tasks that benefit from autonomous flow.  
Expected behavior:

- own end-to-end task execution (plan -> implement -> test -> report)
- keep docs and code in sync
- leave reproducible evidence of results

## Built-in Cursor Tools: Practical Matrix

| Tool/Capability | Best Use | Common Pitfall | Professional Standard |
|---|---|---|---|
| Context references (`@file`, folders) | Pull exact files into scope | vague prompts without explicit file scope | reference exact files and intent in the same prompt |
| Agent TODO tracking | multi-step execution state | mixing with ad hoc TODO text files without distinction | maintain one active execution TODO list and close completed items |
| Terminal integration | deterministic checks and automation | running broad/slow commands with low signal | run scoped, high-signal commands and capture outputs |
| Search/replace | systematic updates across files | unreviewed regex bulk edits | preview matches, use scoped patterns, verify changed files |
| Command palette | discover/run workspace commands | relying on memory for shortcuts | verify command names in-product when behavior matters |

## Ask vs Agent Decision Checklist

Use Ask when most answers are explanatory and no file changes are required.  
Use Agent when at least one of these is true:

- implementation is required
- correctness depends on runtime/test evidence
- docs/config must be updated in repository

## MCP Integration Guidance

In this template, MCP usage should follow this order:

1. built-in context and repo evidence first
2. targeted MCP calls for external or specialized capabilities
3. explicit verification of MCP-sourced output before final recommendations

For MCP setup details, see:

- `MCP_Setup/`
- `.cursor/rules/ace-patterns.mdc`
- `.cursor/commands/ace-help.md`

## Professional Documentation Standard

When adding or updating guidance:

- define one canonical source for each topic
- mark legacy docs as supplemental when they overlap
- avoid undocumented assumptions about shortcuts or feature names
- prefer verifiable, reproducible instructions over speculative settings

## Recommended Read Order

1. `Cursor_Guides/CURSOR_3_TOOLS_AND_AGENTS_GUIDE.md` (this file)
2. `.cursor/README.md`
3. `Cursor_Guides/CURSOR_SETTINGS_VERIFICATION.md`
4. `Sequential_Thinking/README.md` for analysis playbooks
