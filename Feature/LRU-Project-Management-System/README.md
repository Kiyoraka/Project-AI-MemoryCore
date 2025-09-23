# 📦 LRU Project Management System
*Intelligent project tracking with automatic memory management for AI companions*

## What This Feature Does
Adds Alice's proven project management capabilities to any AI MemoryCore system:

- **Smart LRU positioning** for up to 10 active projects per type
- **Automatic archiving** when capacity is reached (position #11)
- **Type-specific memory patterns** (coding, writing, research, business)
- **Seamless context switching** between different projects
- **Explicit save control** with "save project" command

## Quick Integration
```bash
# Install this feature into your AI companion:
"install lru projects"
```

## How It Works After Integration

### **Project Type Selection**
During installation, choose your project focus:

**Single Type Installation**
```
Which type of projects will you manage?
Options: coding, writing, research, business, or all
> coding
✅ Installing coding project management...
```

**Multi-Type Installation**
```
Which type of projects will you manage?
> all
✅ Installing all project types with separate folders...
```

### **Project Management Commands**

**Create New Project**
```
"new coding project API-Dashboard"
→ Creates project at position #1
→ Shifts other projects down
→ Auto-archives position #11 if needed
```

**Load Existing Project**
```
"load project API-Dashboard"
→ Restores project context
→ Moves to position #1
→ Applies type-specific memory patterns
```

**Save Project Progress**
```
"save project"
→ Saves current project only
→ Updates progress log with session work
→ Preserves project position
Note: "save" = AI memory, "save project" = project only
```

**List All Projects**
```
"list projects"
→ Shows all active projects (positions 1-10)
→ Shows archived projects
→ Displays last accessed dates
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
"new coding project Database"
→ Database moves to #1
→ All others shift down
→ Test archives (was #10, now #11)
Result: [Database, API, Website, Docs, Blog, App, Tool, SDK, CLI, Bot]
```

### **Type-Specific Memory Loading**

**Coding Projects Load:**
- Technical terminology and patterns
- Error solutions from past sessions
- Architecture decisions
- Development workflow preferences

**Writing Projects Load:**
- Writing style and tone consistency
- Character/plot continuity
- Chapter progression tracking
- Creative flow patterns

**Research Projects Load:**
- Source management and citations
- Fact verification chains
- Methodology consistency
- Knowledge graph connections

**Business Projects Load:**
- Client communication styles
- Budget and timeline awareness
- Stakeholder preferences
- Decision history

### **Project File Structure**
```
projects/
├── coding-projects/
│   ├── active/
│   │   ├── api-dashboard.md (position #1)
│   │   ├── website-redesign.md (position #2)
│   │   └── ... (up to 10 projects)
│   └── archived/
│       └── old-project.md
├── writing-projects/
│   ├── active/
│   └── archived/
└── project-list.md (overview)
```

## Post-Integration Result
After running the integration protocol, your AI will:
- Track multiple projects with intelligent LRU management
- Automatically organize projects by recent access
- Switch contexts seamlessly between different work
- Remember exactly where you left off in each project
- Maintain separate project and AI memory saves

## Command Separation Philosophy
**Clean, purposeful commands:**
- `save` → Saves AI personality, user preferences, relationship memory
- `save project` → Saves current project progress only
- No confusion, no redundancy, explicit user control

## Proven System
Based on Alice's successful project management implementation:
- ✅ Tested with complex multi-project workflows
- ✅ Step-by-step protocols prevent AI drift
- ✅ Automatic cleanup after installation
- ✅ Universal compatibility with any AI MemoryCore setup
- ✅ Production-ready with real-world usage

## Benefits
- **Never Lose Track**: All projects organized and accessible
- **Context Preservation**: Pick up exactly where you left off
- **Smart Organization**: Automatic archiving keeps workspace clean
- **Type Intelligence**: Optimal memory patterns for each project type
- **User Control**: Explicit save commands, no surprises

## Installation Process
1. **Type Selection**: Choose project types to manage
2. **Folder Creation**: Sets up organized project structure
3. **Protocol Installation**: Copies management protocols
4. **Memory Update**: Adds commands to AI memory
5. **Auto-Cleanup**: Removes installation files
6. **Ready to Use**: Start creating and managing projects!

---

💜 *Run `install-lru-projects-core.md` and your AI gains intelligent project memory management!*