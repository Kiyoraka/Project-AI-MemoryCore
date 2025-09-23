# 📦 LRU Project Management System - Installation Protocol
*Smart project tracking with automatic memory management for AI companions*

## 🚀 Quick Install Command
```
"install lru projects"
```

## 📋 Installation Steps

### Step 1: Select Project Type
- [ ] Ask user: "Which type of projects will you manage? Options: coding, writing, research, business, or all"
- [ ] Capture user selection
- [ ] Load corresponding project template(s)

### Step 2: Create Project Structure
- [ ] Create `projects/` folder in root directory
- [ ] For each selected type, create:
  - [ ] `projects/[type]-projects/active/` (holds up to 10 projects)
  - [ ] `projects/[type]-projects/archived/` (auto-archived projects)
- [ ] Create `projects/project-list.md` for overview

### Step 3: Install Core Components
- [ ] Copy `new-project-protocol.md` to `projects/`
- [ ] Copy `load-project-protocol.md` to `projects/`
- [ ] Copy `save-project-protocol.md` to `projects/`
- [ ] Copy selected templates to `projects/templates/`
- [ ] Create LRU engine file in `projects/lru-manager.md`

### Step 4: Update Memory System
- [ ] Add to main-memory.md:
  ```markdown
  ## Project Management Commands
  - "new [type] project [name]" - Create new project
  - "load project [name]" - Load existing project
  - "save project" - Save current project progress
  - "list projects" - Show all projects
  - "archive project [name]" - Manually archive project

  Note: "save project" saves project only, "save" saves AI memory only
  ```
- [ ] Update current-session-memory.md with installation note
- [ ] Add project tracking section to session memory template

### Step 5: Verify Installation
- [ ] Test create dummy project
- [ ] Verify LRU rotation works
- [ ] Confirm archiving at position 11
- [ ] Delete test project

### Step 6: Cleanup
- [ ] Delete installation files from Feature/LRU-Project-Management/
- [ ] Keep only integrated components in projects/ folder
- [ ] Show success message with available commands

## ✅ Installation Complete Message
```markdown
✅ LRU Project Management Installed Successfully!
📁 Project Type: [selected type(s)]
📊 Capacity: 10 active projects per type
♻️ Auto-archiving: Enabled at position 11

Available Commands:
• new [type] project [name] - Start a new project
• load project [name] - Resume existing project
• save project - Save current project progress
• list projects - View all projects
• archive project [name] - Manually archive

Remember: "save project" for projects, "save" for AI memory!

Your AI companion now has intelligent project memory!
```

## 🎯 What This System Does
1. **Tracks Multiple Projects** - Up to 10 active projects per type
2. **Auto-Archives Old Projects** - LRU keeps recent projects accessible
3. **Context Switching** - Seamlessly switch between different projects
4. **Memory Patterns** - Loads appropriate memories based on project type
5. **Persistent Across Sessions** - Projects survive session resets

## 📝 Notes
- Projects are ordered by last access (position 1 = most recent)
- Position 11 automatically moves to archived folder
- Archived projects can be reloaded anytime
- Each project type has its own 10-slot queue

---

*Version 1.0 - LRU Project Management System*
*Auto-integrates and self-deletes after installation*