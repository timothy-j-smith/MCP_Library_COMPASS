# Filesystem MCP Setup Guide: Project-Specific Configuration
**Date:** January 17, 2026  
**Time:** 21:38 PST  
**Project:** Walk This Way + COMPASS Advanced System  
**Purpose:** Understanding Filesystem MCP configuration for current and future novels

---

## ⚠️ CORRECTION (added July 14, 2026): This is NOT universally necessary

Everything below was written as if Filesystem MCP is required "foundation" for every client. That's only true for **Claude Desktop** (the local Mac app, not Claude Projects on claude.ai). It is redundant in other places:

- **Cursor:** Already has native, built-in file read/write/search tools for whatever folder is open as the workspace. Filesystem MCP pointed at that same folder duplicates functionality Cursor's own agent already has — it does nothing extra. It's only useful in Cursor if you want the agent to reach a folder **outside** the current workspace (e.g., a different novel's folder).
- **Claude Projects (claude.ai web):** Uses a manually-uploaded, static knowledge-base snapshot, not live disk access. It runs in the cloud with no path to your Mac's disk at all, so a local Filesystem MCP server can't attach to it regardless — this isn't a redundancy, it's a different mechanism entirely (re-upload files by hand to update what Claude sees there).
- **Claude Desktop (local app):** This is the one place Filesystem MCP does real work — the chat app has no disk access on its own, so this is the only way to give it live read/write to the novel folder.
- **HyperAgent** (and similar tools that take "docs" as input): likely closer to the Projects model — static context you feed it — but confirm against that tool's own docs rather than assuming.

**Practical takeaway for Walk This Way:** if you write exclusively inside Cursor with the folder open as the workspace, `walk-this-way-files` in that client's config is inert — safe to remove there. Keep it only for Claude Desktop, or if you want cross-folder access inside Cursor.

---

## 🎯 YOUR QUESTION ANSWERED

**Q: "Is Filesystem MCP specific to Walk This Way folder, and for the next novel I'd set it up similarly and make sure we don't forget since it's embedded in Walk This Way?"**

**A: YES - Exactly right!** Here's how it works:

---

## 📁 HOW FILESYSTEM MCP WORKS

### **Current Setup (Walk This Way):**

**Location:** `.cursor/config/mcp.json` (project-specific config)

**Configuration:**
```json
{
  "mcpServers": {
    "walk-this-way-files": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/timothy/Library/Mobile Documents/com~apple~CloudDocs/Cursor/03_Novels/Walk This Way"
      ],
      "disabled": false
    }
  }
}
```

**What This Means:**
- ✅ **Project-specific:** Config is in `.cursor/config/mcp.json` (inside the project)
- ✅ **Scoped to Walk This Way:** Path points specifically to "Walk This Way" folder
- ✅ **Isolated:** Only accesses files in that folder (doesn't see other novels)

---

## 🔄 FOR FUTURE NOVELS (Novel #2, #3, etc.)

### **What You'll Need to Do:**

**When Starting Novel #2:**
1. Create new novel folder (e.g., `04_Novels/Phantom Cowboy/`)
2. Set up project structure (`.cursor/config/` folder)
3. Create `.cursor/config/mcp.json` with Filesystem MCP
4. Update the path to point to the new novel folder

**Example for Novel #2:**
```json
{
  "mcpServers": {
    "novel-2-files": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/timothy/Library/Mobile Documents/com~apple~CloudDocs/Cursor/04_Novels/Phantom Cowboy"
      ],
      "disabled": false
    }
  }
}
```

**Key Differences:**
- ✅ **Different MCP name:** `novel-2-files` (instead of `walk-this-way-files`)
- ✅ **Different path:** Points to new novel folder
- ✅ **Same structure:** Same MCP package, same setup process

---

## 🎯 WHY PROJECT-SPECIFIC CONFIG IS BETTER

### **Advantages:**
1. ✅ **Isolation:** Each novel has its own MCP scope (no cross-contamination)
2. ✅ **Portability:** Easy to move/backup/share novel folders
3. ✅ **Version Control:** MCP config stays with the project (in Git)
4. ✅ **Flexibility:** Different novels can have different MCP setups

### **Alternative (Global Config):**
You *could* use `~/.cursor/mcp.json` (global), but:
- ❌ **Less Isolation:** All novels share the same config
- ❌ **Harder to Manage:** One config for all projects
- ❌ **Less Portable:** Config not with the project

**Recommendation:** ✅ **Stick with project-specific** (`.cursor/config/mcp.json`)

---

## 📋 COMPASS TEMPLATE: MCP SETUP CHECKLIST

### **To Prevent Forgetting, Include in COMPASS Template:**

**File:** `zz_COMPASS/Core/Universal-Fiction-Templates.md` or `zz_COMPASS/Helpful_Hints.md`

### ⚠️ Split by scope, not by list (correction, July 14 2026)

The original checklist below told you to re-add all four MCPs to every new novel's project config. That's only correct for the ones that actually point at *this* novel's folder. Sort each MCP by whether its config contains a path:

**Global — set up once in `~/.cursor/mcp.json`, never repeated per novel:**
- **Sequential Thinking MCP** — no path anywhere in its config; it's a generic reasoning tool.
  ```json
  "sequential-thinking": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
  }
  ```

**Project-specific — one entry per novel, in that novel's own `.cursor/config/mcp.json`:**
- **Filesystem MCP** — the path *is* the config; it has to point at the current novel's folder.
  ```json
  "[novel-name]-files": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/PATH/TO/NOVEL/FOLDER"]
  }
  ```
- **COMPASS Writing Guides MCP** — project-specific *if* you keep a separate `zz_COMPASS/` copy inside each novel's folder (as the paths elsewhere in this repo suggest). If it's actually one shared install referenced by every novel, it belongs in the global config instead — check where your real `COMPASS_Writing_Guides_MCP/server.py` lives before deciding.
  ```json
  "compass-writing-guides": {
    "command": "/PATH/TO/COMPASS/Writing_Guides_MCP/venv/bin/python",
    "args": ["/PATH/TO/COMPASS/Writing_Guides_MCP/server.py"]
  }
  ```

**Special case — Knowledge Graph Memory MCP:** its `command`/`args` look generic (no path), but `@modelcontextprotocol/server-memory` writes its character/plot data to a file that defaults to a fixed location inside the package install if you don't set one. That means running it "globally" without a per-novel `MEMORY_FILE_PATH` would silently mix Walk This Way's character memory with every other novel's. Set the path explicitly per novel even though the server itself is reused:
  ```json
  "knowledge-graph-memory": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-memory"],
    "env": {
      "MEMORY_FILE_PATH": "/PATH/TO/NOVEL/FOLDER/zz_COMPASS/memory.json"
    }
  }
  ```
  **The rule this reveals:** don't just check `args` for a path — also check `env` for anything that names a data file or storage location. A server can look generic and still be secretly project-specific because of where it *saves* things, not where it *runs from*.

### **Step 1: Create MCP Config Folder**
- Create `.cursor/config/` folder in novel root
- Create `.cursor/config/mcp.json` file

### **Step 2: Configure Filesystem MCP**
- Add Filesystem MCP with novel-specific path
- Name MCP appropriately (e.g., `novel-name-files`)
- Point to novel folder path

### **Step 3: Configure Core MCPs**
- Filesystem MCP (novel-specific path, project config) ✅
- Knowledge Graph Memory MCP (novel-specific `MEMORY_FILE_PATH`, project config) ✅
- COMPASS Writing Guides MCP (project config, unless shared — see above) ✅
- Sequential Thinking MCP (global config, set up once — not per novel) ✅
- (Add other MCPs as needed)

### **Step 4: Test MCPs**
- Restart Cursor completely (Cmd+Q)
- Test: "Show me the README from this project" (tests Filesystem)
- Test: "Use sequential-thinking MCP to analyze this problem" (tests Sequential Thinking)

**Template MCP Config — project-specific file (`.cursor/config/mcp.json` inside the novel folder):**
```json
{
  "mcpServers": {
    "[novel-name]-files": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/PATH/TO/NOVEL/FOLDER"
      ],
      "disabled": false
    },
    "knowledge-graph-memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {
        "MEMORY_FILE_PATH": "/PATH/TO/NOVEL/FOLDER/zz_COMPASS/memory.json"
      },
      "disabled": false
    },
    "compass-writing-guides": {
      "command": "/PATH/TO/COMPASS/Writing_Guides_MCP/venv/bin/python",
      "args": ["/PATH/TO/COMPASS/Writing_Guides_MCP/server.py"],
      "disabled": false
    }
  }
}
```

**Template MCP Config — global file (`~/.cursor/mcp.json`, set up once, applies to every novel):**
```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
      "disabled": false
    }
  }
}
```

---

## 🔧 HOW TO REMEMBER (COMPASS Integration)

### **Option 1: COMPASS Template File**
- ✅ Add MCP setup checklist to `zz_COMPASS/Core/Universal-Fiction-Templates.md`
- ✅ Include example config
- ✅ Reference in novel setup process

### **Option 2: COMPASS Helpful Hints**
- ✅ Add MCP reminder to `zz_COMPASS/Helpful_Hints.md`
- ✅ Include in "Project Setup" section

### **Option 3: COMPASS Novel Kickoff Protocol**
- ✅ Add MCP setup as Step 1 in novel kickoff checklist
- ✅ Make it part of standard novel setup process

---

## ✅ SUMMARY: YOUR UNDERSTANDING IS CORRECT

**What You Said:**
> "Filesystem MCP is specific to Walk This Way folder, and for the next novel I'd set it up similarly and make sure we don't forget since it's embedded in Walk This Way?"

**Answer:**
✅ **YES - Exactly!**

**Details:**
1. ✅ **Current:** Filesystem MCP is project-specific (embedded in "Walk This Way")
2. ✅ **Future:** Each novel needs its own `.cursor/config/mcp.json` with its own path
3. ✅ **Prevent Forgetting:** Add MCP setup to COMPASS template/checklist
4. ✅ **Isolation:** Each novel has its own MCP scope (good!)

**Recommendation:**
- ✅ Keep project-specific config (better isolation)
- ✅ Add MCP setup to COMPASS template
- ✅ Include in novel kickoff checklist
- ✅ Reference example config from "Walk This Way"

---

## 🚀 NEXT STEPS

1. ✅ **Confirm Understanding:** You've got it right!
2. ✅ **Add to COMPASS Template:** Include MCP setup checklist
3. ✅ **Document Template Config:** Create example `.cursor/config/mcp.json` template
4. ✅ **Novel #2:** Use template when starting next novel

**Bottom Line:** Project-specific config is the right approach. Add MCP setup to COMPASS template so you don't forget for Novel #2! 🎯

---

*Last Updated: January 17, 2026 21:38 PST*
