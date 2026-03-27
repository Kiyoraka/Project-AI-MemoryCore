---
name: manage-project
description: "Auto-triggers on 'new project [name]', 'load project [name]',
             'save project', 'list projects'. Also triggers on 'create project',
             'resume project', 'open project', 'show projects', or when user
             mentions switching between active projects."
---

# Manage Project -- LRU Project Management Skill
*Smart project tracking with automatic memory management.*

## Activation

When this skill activates, silently determine which command was triggered and execute the matching protocol section.

## Context Guard

| Context | Status |
|---------|--------|
| **User says "new project [name]"** | ACTIVE -- create project |
| **User says "load project [name]"** | ACTIVE -- load and resume |
| **User says "save project"** | ACTIVE -- save current progress |
| **User says "list projects"** | ACTIVE -- display all projects |
| **Mid-conversation (no project command)** | DORMANT |

---

## Protocol: New Project

**Trigger**: `"new project [name]"` or `"create project [name]"`

### Step 1: Parse Command
- [ ] Extract project name from command
- [ ] Check if project name already exists in active or archived
- [ ] If exists: suggest loading instead, or ask for a different name

### Step 2: Gather Project Details
- [ ] Ask user for brief description (1-2 sentences)
- [ ] Get current date using platform-appropriate time command
- [ ] Note any initial requirements, goals, or tech stack

### Step 3: Create Project File
- [ ] Generate project file from **Embedded Project Template** (see below)
- [ ] Fill in: name, description, created date, status (Active)
- [ ] Save to `projects/active/[name].md`

### Step 4: Apply LRU Positioning
- [ ] Insert new project at position #1
- [ ] Shift all existing active projects down by 1
- [ ] If position #11 exists after shift:
  - Move to `projects/archived/`
  - Update status to "Archived (LRU)"
  - Add archive date

### Step 5: Update Project List
- [ ] Regenerate `projects/project-list.md` (see **Project List Format**)
- [ ] New project at top of active section
- [ ] Note any auto-archived project

### Step 6: Update Session Memory
- [ ] Add to current-session.md:
  ```markdown
  ## Active Project
  - Name: [project name]
  - Started: [date/time]
  - Context: [description]
  ```

### Step 7: Confirm
- [ ] Display confirmation with project name, position #1, and description

---

## Protocol: Load Project

**Trigger**: `"load project [name]"` or `"resume project [name]"`

### Step 1: Search for Project
- [ ] Parse project name from command
- [ ] Search `projects/active/` first
- [ ] Then search `projects/archived/`
- [ ] Use fuzzy matching if exact name not found (partial names, case-insensitive)

### Step 2: Handle Search Results
- [ ] If multiple matches: show list, ask for selection
- [ ] If in archived: note that project will be reactivated
- [ ] If not found: suggest similar projects, offer to create new

### Step 3: Load Project Data
- [ ] Read project file completely
- [ ] Extract: description, last accessed, status, recent sessions, duration

### Step 4: Apply LRU Positioning
- [ ] If archived: move from `archived/` to `active/`
- [ ] Move project to position #1
- [ ] Shift all other active projects down
- [ ] If position #11 exists: auto-archive

### Step 5: Update Project File
- [ ] Update "Last Accessed" to current date/time
- [ ] Add session note to progress:
  ```markdown
  ### [Current Date]
  - Project resumed from [previous position/archived]
  ```

### Step 6: Update Project List
- [ ] Regenerate `projects/project-list.md`

### Step 7: Load into Session Memory
- [ ] Update current-session.md:
  ```markdown
  ## Active Project
  - Name: [project name]
  - Resumed: [date/time]
  - Last worked: [previous date]
  - Context: [description]
  - Recent progress: [last 3 session entries]
  ```

### Step 8: Display Summary
- [ ] Show: name, position #1, last worked date, description, recent activity

---

## Protocol: Save Project

**Trigger**: `"save project"` -- saves current project only, NOT AI memory

### Step 1: Identify Active Project
- [ ] Check current-session.md for active project
- [ ] If no active project: inform user, suggest loading or creating one
- [ ] If project exists: proceed to save

### Step 2: Gather Session Progress
- [ ] Collect work done in current session
- [ ] Capture code changes, decisions, milestones
- [ ] Note issues resolved or discovered
- [ ] Document resources or references added

### Step 3: Parse Duration
- [ ] Read recent commit messages from session: `git log --oneline --format="%s%n%b" -20`
- [ ] Search for `Time:` field in commit bodies (from Auto-Commit System)
- [ ] Sum all `Time: ~XX min` values for this session
- [ ] Add to project's accumulated duration
- [ ] Format using **Duration Thresholds** (see below)

### Step 4: Update Project File
- [ ] Load project file from `projects/active/[name].md`
- [ ] Update "Last Accessed" to current date/time
- [ ] Update "Duration" with accumulated total
- [ ] Update "Current Status" section
- [ ] Add session entry to Session History:
  ```markdown
  ### [Current Date] - [Session Title]
  - **Changes**: [Summary of session work]
  - **Time Spent**: ~XX min
  ```

### Step 5: Line Limit Check
- [ ] Count lines in project file
- [ ] If over 1000 lines: run **Line Limit Enforcement** (see below)
- [ ] Verify file is under 1000 lines after enforcement

### Step 6: Update Project List
- [ ] Regenerate `projects/project-list.md` with updated timestamps

### Step 7: Confirm Save
- [ ] Display: project name, saved timestamp, session summary, total duration

---

## Protocol: List Projects

**Trigger**: `"list projects"` or `"show projects"`

### Step 1: Read Project List
- [ ] Load `projects/project-list.md`
- [ ] Parse active projects (positions 1-10) and archived projects

### Step 2: Display
- [ ] Show active projects with: position, name, last updated, status
- [ ] Show archived project count and names
- [ ] Highlight currently loaded project (if any)

---

## LRU Engine

### Rules
- **Fixed Capacity**: 10 active projects (positions 1-10)
- **Position-Based**: Projects ranked by most recent access/creation
- **Auto-Archiving**: Position #11 gets archived when new project added or existing one loaded
- **Reactivation**: Archived projects can be loaded back (replaces position #10, archives it)

### Operations

**Move to Position #1**:
1. Identify project location (active position or archived)
2. Remove from current position
3. Insert at position #1
4. Shift all others down by 1
5. Archive position #11 if it exists
6. Regenerate project-list.md

**Auto-Archive**:
1. Move project file from `active/` to `archived/`
2. Update project metadata: status = "Archived (LRU)", archive date added
3. Update project-list.md

### Project List Format

```markdown
# Project Portfolio - Dynamic List
*Auto-generated by LRU Project Management System*

## Active Projects (X/10)

| Pos | Project | Last Updated | Status |
|-----|---------|--------------|--------|
| 1 | **[Project Name](./active/name.md)** | [Date] | [Brief status] |
| 2 | ... | ... | ... |

## Archived Projects (X)

| Project | Status |
|---------|--------|
| **[Project Name](./archived/name.md)** | Archived (LRU) - [Date] |

---
## System Status
- **Total Projects**: X (Y active + Z archived)
- **Last Updated**: [Date] - [Action taken]
```

---

## Duration Tracking

### Parsing
- Read commit messages for `Time: ~XX min` or `Time: XX min` patterns
- Source: Auto-Commit System's SESSION CONTEXT section
- Sum all time values from commits made during the current session

### Accumulation
- Each "save project" adds session time to the project's total Duration
- Duration stored in project file's Overview section

### Display Thresholds

| Total Minutes | Display Format | Example |
|---------------|----------------|---------|
| 1-59 | X min | 45 min |
| 60-1439 | X hours | 3 hours |
| 1440-43199 | X days | 2 days |
| 43200+ | X months | 1 month |

- Round to nearest 0.5 for clean display (e.g., "2.5 hours", "1.5 days")
- Conversion: 60 min = 1 hour, 1440 min = 1 day (24h), 43200 min = 1 month (30d)

---

## Line Limit Enforcement

**Maximum: 1000 lines per project file**

### When to Check
- Before completing any "save project" operation
- After adding new session content

### When project file exceeds 1000 lines:

**Step 1: Summarize Old Sessions**
- [ ] Identify sessions older than last 5
- [ ] Extract key info: dates, major changes
- [ ] Create/update Historical Summary paragraph
- [ ] Remove detailed old session entries

**Step 2: Trim Verbose Sections**
- [ ] Keep only: Overview, Status, Sessions (5), History, Notes
- [ ] Remove any extra sections not in the template

**Step 3: Verify**
- [ ] Count lines after summarization
- [ ] If still > 1000: repeat summarization more aggressively
- [ ] Ensure file is under 1000 lines

### Historical Summary Format
```markdown
## Historical Summary
Project started [Start Date] as [initial scope]. Over [X] sessions spanning
[timeframe], developed [major features/changes]. Key milestones: [milestone 1],
[milestone 2], [milestone 3]. Previous sessions covered: [brief theme list].
```

---

## Embedded Project Template

When creating a new project, use this template:

```markdown
# [Project Name] - [Brief Description]
*[One-line project summary]*

## Project Overview
- **Type**: [Category: Web App/API/Library/Game/Tool/etc.]
- **Period**: [Start Date] - Active
- **Tech Stack**: [Backend] + [Frontend] + [Database]
- **Completion**: 0%
- **Duration**: 0 min

## Current Status
- **Last Session**: [Date] - Project created
- **Next Steps**: [Initial goals]
- **Known Issues**: None

## Session History (Last 5)

### [Date] - Project Created
- **Changes**: Initial project setup
- **Time Spent**: ~0 min

## Historical Summary
[No history yet -- this section is populated when session count exceeds 5]

## Technical Notes
- **Repository**: [Git URL or local path]
- **Key Dependencies**: [Critical packages or services]

---
**Last Updated**: [Date] | **Position**: #1/10 Active
```

---

## Mandatory Rules

1. **10 active slots** -- auto-archive at position #11. No exceptions
2. **project-list.md regenerated** after every LRU operation (new, load, save)
3. **Line limit 1000** -- auto-summarize when exceeded, keep last 5 sessions
4. **Duration tracking** -- parse `Time:` from Auto-Commit messages, accumulate per project
5. **Generic template** -- no type-specific fields. One universal project format
6. **"save project" is project-only** -- does NOT save AI memory, personality, or preferences
7. **Explicit save only** -- no auto-save. User controls when to save
8. **Fuzzy search on load** -- partial names, case-insensitive matching
9. **Preserve data on archive** -- archived projects retain all history and can be reloaded
10. **Command separation** -- `save` = AI memory (handled elsewhere), `save project` = project progress

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| No active project on "save project" | Inform user, suggest load or create |
| Project name already exists on "new" | Suggest loading existing or choosing different name |
| Project not found on "load" | Show available projects, offer fuzzy matches |
| Archive folder has 50+ projects | Suggest cleanup of old archives |
| No Auto-Commit time data available | Use `~XX min` estimate or ask user |
| Multiple projects match search | Display list with positions and dates, ask for selection |

## Synergy with Other Features

| Feature | Integration |
|---------|-------------|
| **Auto-Commit System** | Duration tracking parses `Time:` from commit messages |
| **Save Diary System** | Diary captures daily narrative; project captures project-specific progress |
| **Reminders System** | "Revisit this project next week" becomes a reminder |
| **Decision Log System** | Project decisions can reference the decision log |

## Level History
- **Lv.1** -- Base: new/load/save/list commands, LRU engine (10 slots), auto-archiving, session history, project-list.md auto-generation. (Origin: Absorbed from separate protocol files + adapted from production AI companion project manager v3.1)
- **Lv.2** -- Duration Tracking: Parse Auto-Commit time estimates, accumulate per project, progressive display format. Line Limit Enforcement: 1000-line cap with auto-summarization.
