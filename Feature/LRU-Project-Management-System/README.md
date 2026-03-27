# 📦 LRU Project Management System
*Intelligent project tracking with automatic memory management for AI companions*

## What This Feature Does
Adds smart project management capabilities to any AI MemoryCore system:

- **LRU positioning** for up to 10 active projects
- **Automatic archiving** when capacity is reached (position #11)
- **Duration tracking** that accumulates time from Auto-Commit messages
- **Line limit enforcement** (1000 lines max with auto-summarization)
- **Seamless context switching** between different projects
- **Fuzzy search** for loading projects by partial name

## Quick Integration
```bash
# Install this feature into your AI companion:
"install lru projects"
```

## How It Works After Integration

### **Project Management Commands**

**Create New Project**
```
"new project API-Dashboard"
  Creates project at position #1
  Shifts other projects down
  Auto-archives position #11 if needed
```

**Load Existing Project**
```
"load project API-Dashboard"
  Searches active then archived (fuzzy matching)
  Restores project context
  Moves to position #1
```

**Save Project Progress**
```
"save project"
  Saves current project only (NOT AI memory)
  Updates progress log with session work
  Accumulates duration from Auto-Commit time data
  Enforces 1000-line limit with auto-summarization
```

**List All Projects**
```
"list projects"
  Shows all active projects (positions 1-10)
  Shows archived projects
  Displays last accessed dates
```

### **LRU (Least Recently Used) System**

**How Positioning Works:**
1. **Position #1** = Most recently accessed project
2. **Positions #2-10** = Other active projects in order
3. **Position #11** = Automatically archived
4. **Archived** = Can be reloaded anytime

**Example Flow:**
```
Projects: [API, Website, Docs, Blog, App, Tool, SDK, CLI, Bot, Test]
"new project Database"
  Database moves to #1
  All others shift down
  Test archives (was #10, now #11)
Result: [Database, API, Website, Docs, Blog, App, Tool, SDK, CLI, Bot]
```

### **Duration Tracking**
Automatically tracks time spent on each project:
- Parses `Time: ~XX min` from Auto-Commit System commit messages
- Accumulates across sessions into total project duration
- Progressive display: minutes -> hours -> days -> months
- Works best with Auto-Commit System installed (falls back to manual estimates)

### **Line Limit Enforcement**
Keeps project files lean and readable:
- Maximum 1000 lines per project file
- When exceeded: old sessions (beyond last 5) are condensed into a Historical Summary
- Verbose sections are trimmed automatically
- Project history is preserved in summary form, never lost

### **Project File Structure**
```
projects/
├── active/
│   ├── api-dashboard.md (position #1)
│   ├── website-redesign.md (position #2)
│   └── ... (up to 10 projects)
├── archived/
│   └── old-project.md
└── project-list.md (auto-generated overview)
```

## Post-Integration Result
After running the integration protocol, your AI will:
- Track multiple projects with intelligent LRU management
- Automatically organize projects by recent access
- Switch contexts seamlessly between different work
- Remember exactly where you left off in each project
- Track cumulative time spent per project
- Keep project files under 1000 lines automatically

## Command Separation Philosophy
**Clean, purposeful commands:**
- `save project` -- Saves current project progress only
- `save diary` -- Saves session documentation (Save Diary System)
- No ambiguity, no redundancy, explicit user control

## Synergy with Other Features

| Feature | Integration |
|---------|-------------|
| **Auto-Commit System** | Duration tracking parses time from commit messages |
| **Save Diary System** | Diary captures daily narrative; projects capture project-specific progress |
| **Reminders System** | "Revisit this project next week" becomes a reminder |
| **Decision Log System** | Project decisions can reference the decision log |

## Proven System
Based on production AI companion project management:
- Tested with 70+ projects across active and archived states
- LRU auto-archiving keeps workspace clean without losing data
- Duration tracking provides accurate time investment records
- Line limit enforcement prevents file bloat over months of use

## Benefits
- **Never Lose Track**: All projects organized and accessible
- **Context Preservation**: Pick up exactly where you left off
- **Smart Organization**: Automatic archiving keeps workspace clean
- **Time Awareness**: Know exactly how much time you've invested
- **File Discipline**: 1000-line cap prevents project file bloat
- **User Control**: Explicit save commands, no surprises

**Platform Note:** Includes `SKILL.md` for auto-triggering via the Skill Plugin System. Works on any platform without the plugin (load install protocol manually).

---

*Run `install-lru-projects-core.md` and your AI gains intelligent project memory management!*
