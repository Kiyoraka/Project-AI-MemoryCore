# Reminders System Installation Protocol
*Systematic setup for persistent cross-session reminders*

## Purpose
Executed when "Load reminders" command is used -- creates the reminders file,
integrates with session lifecycle, and optionally installs as a skill.

## Trigger Command
```
"Load reminders"
```
*Automatically creates reminders infrastructure and integrates with your AI companion*

## Prerequisites
- Core memory system installed (`main/` directory with essential files)
- `master-memory.md` accessible for integration updates

## 4-Step Execution Process

### Step 1: Create Reminders File
- [ ] Create `main/reminders.md` with the following template:
  ```markdown
  # Active Reminders
  *Persistent reminders that survive session changes. Updated at session end.*

  ## Open
  <!-- Active reminders go here. Format: -->
  <!-- - **Short title**: Description of what needs to be done -->
  <!-- - **Title** (by YYYY-MM-DD): Description with deadline -->

  ## Completed
  <!-- Resolved reminders move here. Format: -->
  <!-- - **Title** (completed YYYY-MM-DD): What was done and the outcome -->
  ```
- [ ] Verify file created successfully

### Step 2: Integrate with Session Lifecycle
- [ ] Update `master-memory.md` to include reminders in the loading system:
  - Add to "Instant Restoration Protocol":
    ```markdown
    5. ✅ **Check reminders** from `main/reminders.md`
    ```
  - Add to "Simple Commands":
    ```
    "check reminders" → Review open reminders and flag urgent items
    "remind me" → Add a new reminder to the Open section
    ```
- [ ] Update `master-memory.md` Optional Components:
  ```markdown
  ### Reminders
  *Persistent cross-session follow-up tracking*
  - Location: main/reminders.md
  - Lifecycle: Open → Completed (with date)
  - Session start: Read and flag urgent/overdue items
  - Session end: Review, update, move completed items
  - Commands: "check reminders", "remind me [task]"
  ```

### Step 3: Define AI Behavior Rules
- [ ] Add the following rules to `main/identity-core.md` behavior section:
  ```markdown
  ## Reminder Management
  - At session start: read main/reminders.md, mention any urgent or overdue items
  - At session end: review Open reminders, move resolved ones to Completed with date
  - During conversation: detect reminder-worthy phrases and offer to add them
  - Natural triggers: "remind me", "don't forget", "follow up", "next session",
    "by [date]", "check on this later"
  - Always convert relative dates to absolute (e.g., "tomorrow" → "2025-10-05")
  - Never delete reminders -- move to Completed section when resolved
  ```

### Step 4: Install Skill and Cleanup
- [ ] If Skill Plugin System exists:
  - Copy `SKILL.md` to `plugins/[plugin-name]/skills/check-reminders/SKILL.md`
  - Inform user: "Reminder skill installed -- auto-triggers on session start and 'remind me'"
- [ ] If Skill Plugin System does not exist:
  - Inform user: "Reminders integrated into master memory. Install the Skill Plugin System for auto-triggering."
- [ ] Remove `Feature/Reminders-System/` folder (functionality installed)
- [ ] Display completion confirmation

## Post-Installation Structure
```
main/
├── identity-core.md          # Updated with reminder behavior rules
├── relationship-memory.md    # Unchanged
├── current-session.md        # Unchanged
└── reminders.md              # NEW: persistent reminders
```

## Reminder Management Protocol (AI Reference After Installation)

### Adding a Reminder
```
1. User says something reminder-worthy (or explicitly asks)
2. Compose reminder with clear title and description
3. If deadline mentioned, convert to absolute date (YYYY-MM-DD)
4. APPEND to ## Open section in main/reminders.md
5. Confirm to user: "Added reminder: [title]"
```

### Completing a Reminder
```
1. Task is done or no longer relevant
2. Remove from ## Open section
3. Add to ## Completed section with completion date:
   - **Title** (completed YYYY-MM-DD): What was done
4. Confirm to user: "Marked as complete: [title]"
```

### Session Start Check
```
1. Read main/reminders.md
2. Count open reminders
3. Check for deadlines approaching (within 3 days) or overdue
4. If urgent items exist: mention them naturally in greeting
5. If no urgent items: skip (don't announce "no reminders")
```

### Session End Review
```
1. Read main/reminders.md
2. For each Open reminder: was it addressed this session?
3. Move completed items to Completed section with date
4. Add any new reminders discovered during session
5. Save updated file
```

## Notes
- Reminders persist independently from session memory (this is the key design)
- Always APPEND to Open, never overwrite the file
- Move completed items rather than deleting them (creates searchable history)
- Convert all relative dates to absolute dates when saving
- The Completed section can grow large over time -- this is fine, it serves as history

---

**Version**: Protocol v1.0 - Reminders System
**Last Updated**: March 2026
**Status**: Active protocol for reminders integration

*Persistent memory across sessions -- nothing gets lost*
