# 🆕 New Project Protocol
*Step-by-step protocol for creating and managing new projects with LRU*

## Trigger Command
```
"new [type] project [name]"
```
Examples: "new coding project API-Dashboard", "new writing project Chapter-5"

## 📋 Execution Steps

### Step 1: Parse Command
- [ ] Extract project type from command (coding/writing/research/business)
- [ ] Extract project name from command
- [ ] Validate project type exists in system
- [ ] Check if project name already exists

### Step 2: Gather Project Details
- [ ] Ask user for brief description (1-2 sentences)
- [ ] Capture current date and time
- [ ] Note any initial requirements or goals
- [ ] Identify primary technologies/tools (if coding project)

### Step 3: Create Project File
- [ ] Load template from `projects/templates/[type]-template.md`
- [ ] Fill in project details:
  - [ ] Project name
  - [ ] Description
  - [ ] Created date
  - [ ] Type
  - [ ] Status: Active
  - [ ] Last accessed: Now
- [ ] Save to `projects/[type]-projects/active/[name].md`

### Step 4: Apply LRU Positioning
- [ ] Move new project to position #1 in project list
- [ ] Shift existing projects down by one position
- [ ] If position #11 exists:
  - [ ] Move to `projects/[type]-projects/archived/`
  - [ ] Update status to "Archived (LRU)"
  - [ ] Add archive date

### Step 5: Update Project List
- [ ] Load `projects/project-list.md`
- [ ] Add new project at top of active section
- [ ] Update project count
- [ ] Reorder all positions (1-10)
- [ ] Note any auto-archived project
- [ ] Save updated list

### Step 6: Update Session Memory
- [ ] Add to current-session-memory.md:
  ```markdown
  ## Active Project
  - Name: [project name]
  - Type: [project type]
  - Started: [date/time]
  - Context: [description]
  ```
- [ ] Note project creation in session log

### Step 7: Confirm Creation
- [ ] Display success message:
  ```markdown
  ✅ Project Created: [name]
  📁 Type: [type]
  📍 Position: #1 (Most Recent)
  📝 Description: [description]

  Project is now active and ready for work!
  ```

## 📊 LRU Rules
1. New projects always start at position #1
2. Maximum 10 active projects per type
3. Position #11 auto-archives to make room
4. Archived projects can be reloaded anytime
5. Each project maintains its complete history

## 🗂️ Project File Structure
```markdown
# [Project Name]
*[Type] Project - Created [Date]*

## Description
[User provided description]

## Details
- Type: [coding/writing/research/business]
- Status: Active
- Created: [Date Time]
- Last Accessed: [Date Time]
- Position: #[1-10]

## Progress Log
### [Date]
- [Initial creation note]

## Notes
[Any additional context or requirements]

## Resources
[Links, references, dependencies]
```

## Error Handling
- If project name exists: Suggest alternative or ask to load existing
- If type invalid: Show available types and ask again
- If archives full (>50): Suggest cleanup of old archives

---

*New Project Protocol v1.0*
*Part of LRU Project Management System*