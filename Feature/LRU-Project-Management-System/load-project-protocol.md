# 📂 Load Project Protocol
*Step-by-step protocol for loading existing projects with LRU management*

## Trigger Command
```
"load project [name]"
```
Alternative: "load [type] project [name]" for type-specific search

## 📋 Execution Steps

### Step 1: Search for Project
- [ ] Parse project name from command
- [ ] If type specified, search only in `projects/[type]-projects/`
- [ ] If no type, search all project directories:
  - [ ] Check all active folders first
  - [ ] Then check archived folders
- [ ] Use fuzzy matching if exact name not found

### Step 2: Locate Project File
- [ ] If multiple matches found:
  - [ ] Show list to user
  - [ ] Ask for selection
- [ ] If in archived folder:
  - [ ] Note that project will be reactivated
- [ ] If not found:
  - [ ] Suggest similar projects
  - [ ] Offer to create new project

### Step 3: Load Project Data
- [ ] Read project file completely
- [ ] Extract key information:
  - [ ] Project type
  - [ ] Description
  - [ ] Last accessed date
  - [ ] Current status
  - [ ] Progress log
- [ ] Load associated memory patterns for project type

### Step 4: Apply LRU Positioning
- [ ] If project is archived:
  - [ ] Move from archived/ to active/ folder
  - [ ] Update status from "Archived" to "Active"
- [ ] Move project to position #1
- [ ] Shift all other active projects down
- [ ] If position #11 exists after shift:
  - [ ] Auto-archive to make room
  - [ ] Note which project was archived

### Step 5: Update Project File
- [ ] Update "Last Accessed" to current date/time
- [ ] Update position to #1
- [ ] Add session note to progress log:
  ```markdown
  ### [Current Date]
  - Project resumed from [previous position/archived]
  ```
- [ ] Save updated project file

### Step 6: Update Project List
- [ ] Load `projects/project-list.md`
- [ ] Move loaded project to top of active list
- [ ] Reorder all positions
- [ ] Update archived section if applicable
- [ ] Save updated list

### Step 7: Load into Session Memory
- [ ] Update current-session-memory.md:
  ```markdown
  ## Active Project
  - Name: [project name]
  - Type: [project type]
  - Resumed: [date/time]
  - Last worked: [previous date]
  - Context: [description]
  - Recent progress: [last 3 log entries]
  ```
- [ ] Load type-specific memory patterns

### Step 8: Display Project Summary
- [ ] Show confirmation:
  ```markdown
  ✅ Project Loaded: [name]
  📁 Type: [type]
  📍 Position: #1 (Now Active)
  ⏰ Last worked: [date]
  📝 Description: [description]

  Recent Activity:
  - [Last log entry]
  - [Previous log entry]

  Ready to continue where you left off!
  ```

## 🔍 Smart Search Features
1. **Fuzzy Matching**: Finds "API-Dash" when searching "api dashboard"
2. **Type Priority**: Coding projects checked first for "load project api"
3. **Recent First**: Active projects searched before archived
4. **Partial Names**: "dash" finds "API-Dashboard" project

## 📊 Memory Pattern Loading

### Coding Projects Load:
- Technical terminology preferences
- Code style patterns
- Recent error solutions
- Development workflow

### Writing Projects Load:
- Writing style consistency
- Character/plot notes
- Tone and voice settings
- Chapter progression

### Research Projects Load:
- Source citations
- Key findings
- Research methodology
- Fact connections

### Business Projects Load:
- Client communication style
- Project constraints
- Stakeholder notes
- Timeline awareness

## Error Handling
- Project not found: Show available projects and suggest alternatives
- Multiple matches: Display list with types and last-worked dates
- Corrupted file: Attempt recovery from backup or recreate from template

---

*Load Project Protocol v1.0*
*Part of LRU Project Management System*