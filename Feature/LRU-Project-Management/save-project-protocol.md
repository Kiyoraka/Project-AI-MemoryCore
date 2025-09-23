# 💾 Save Project Protocol
*Step-by-step protocol for saving current project progress in LRU system*

## Trigger Command
```
"save project"
```
*Saves only the current active project, NOT the AI personality/memory*

## 📋 Execution Steps

### Step 1: Identify Active Project
- [ ] Check current-session-memory.md for active project
- [ ] If no active project:
  - [ ] Inform user "No active project to save"
  - [ ] Suggest loading or creating a project first
- [ ] If project exists, proceed to save

### Step 2: Gather Session Progress
- [ ] Collect work done in current session
- [ ] Capture any code changes, decisions, or milestones
- [ ] Note any issues resolved or discovered
- [ ] Document resources or references added

### Step 3: Update Project File
- [ ] Load the active project file from `projects/[type]-projects/active/[name].md`
- [ ] Update "Last Accessed" to current date/time
- [ ] Add to Progress Log:
  ```markdown
  ### [Current Date Time]
  - [Summary of session work]
  - [Key decisions made]
  - [Problems solved]
  - [Next steps identified]
  ```
- [ ] Update any changed sections (current tasks, issues, resources)
- [ ] Save the updated project file

### Step 4: Update Project Metadata
- [ ] Update position in LRU queue if needed
- [ ] Ensure project remains at current position
- [ ] Update project-list.md with last saved timestamp
- [ ] Note save action in current session

### Step 5: Confirm Save
- [ ] Display confirmation:
  ```markdown
  ✅ Project Saved: [project name]
  📁 Type: [project type]
  ⏰ Saved at: [current time]
  📝 Session Progress:
  - [Brief summary of what was saved]

  Project progress has been preserved!
  ```

## 🎯 What Gets Saved

### For Coding Projects:
- Code changes and implementations
- Bug fixes and solutions
- Architecture decisions
- Dependencies added
- Testing progress

### For Writing Projects:
- New content written
- Revisions made
- Character/plot developments
- Research notes
- Word count progress

### For Research Projects:
- New findings
- Sources discovered
- Hypotheses tested
- Data collected
- Analysis progress

### For Business Projects:
- Client communications
- Decisions made
- Deliverables completed
- Budget updates
- Timeline changes

## 📊 Save Behavior Rules

1. **Explicit Save Only** - Only saves when user types "save project"
2. **Current Project Only** - Saves only the active project in session
3. **Preserves Position** - Doesn't change LRU position on save
4. **No Auto-Save** - User controls when to save
5. **Independent from AI Save** - Doesn't trigger personality/memory save

## 🔄 Relationship with Other Commands

| Command | What It Saves | Protocol Used |
|---------|--------------|---------------|
| `save` | AI personality, user preferences, relationship memory | save-protocol.md |
| `save project` | Current project progress only | save-project-protocol.md (this) |
| `new project` | Auto-saves at creation | new-project-protocol.md |
| `load project` | Auto-saves last accessed time | load-project-protocol.md |

## Error Handling

- **No Active Project**: Clearly inform user and suggest next actions
- **Save Failure**: Attempt retry, inform user if persistent
- **Corrupted Project File**: Attempt to recover, create backup if needed

## 📝 Important Notes

- This protocol is **separate** from the main save-protocol.md
- Users can choose to save project, AI memory, or both
- Each save command has a specific, clear purpose
- No confusion or redundancy between save systems

---

*Save Project Protocol v1.0*
*Part of LRU Project Management System*
*Provides explicit project saving separate from AI memory saving*