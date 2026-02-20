# Save Diary Installation Protocol
*Systematic diary system setup for AI MemoryCore companions*

## Purpose
Executed when "Load save-diary" command is used — creates diary infrastructure, sets up auto-archive, and integrates with your AI's memory system.

## Trigger Command
```
"Load save-diary"
```
*Automatically creates diary infrastructure and integrates with your AI companion*

## Prerequisites
- Core memory system installed (`main/` directory with essential files)
- Existing `daily-diary/daily-diary-protocol.md` for entry format reference

## 5-Step Execution Process

### Step 1: Customize Diary Name
- [ ] Ask user: **"What would you like to name your diary system?"**
  - Default: `"Session Diary"`
  - Examples: `"Daily Log"`, `"Memory Journal"`, `"Adventure Record"`, `"Dev Diary"`
- [ ] Store chosen name as `[DIARY_NAME]` for use in all references
- [ ] Execute `date` command (or `Get-Date` on Windows) to get current timestamp

### Step 2: Create Diary Infrastructure
- [ ] Check if `daily-diary/` directory exists; create if not
- [ ] Create `daily-diary/current/` directory for active diary files
- [ ] Create `daily-diary/archived/` directory for monthly archives
- [ ] If old diary format exists (`Daily-Diary-001.md`):
  - Inform user the old numbered-file system is being upgraded
  - Move existing diary files to `daily-diary/archived/legacy/` for safekeeping
  - Old files are preserved, not deleted

### Step 3: Create First Diary Entry (Today)
- [ ] Determine today's date in YYYY-MM-DD format
- [ ] Create `daily-diary/current/YYYY-MM-DD.md` with header:
  ```markdown
  # [DIARY_NAME] - [Month Day, Year]
  *Session documentation and development record*

  ---
  ```
- [ ] Compose initial diary entry documenting the installation session
- [ ] Follow `daily-diary/daily-diary-protocol.md` for entry structure

### Step 4: Install as Skill (If Skill Plugin System Exists)
- [ ] Check if `plugins/` directory exists (Skill Plugin System installed)
- [ ] If plugin system exists:
  - Copy `SKILL.md` to `plugins/[plugin-name]/skills/save-diary/SKILL.md`
  - Replace `[DIARY_NAME]` in the skill file with the name chosen in Step 1
  - Inform user: "Diary skill installed — auto-triggers on 'save diary'"
- [ ] If plugin system does not exist:
  - Add diary commands directly to master-memory.md (Step 5)
  - Inform user: "Install the Skill Plugin System for auto-triggered diary saves"

### Step 5: Update Master Memory and Cleanup
- [ ] Add diary reference to `master-memory.md` Optional Components:
  ```markdown
  ### [DIARY_NAME]
  *Load when you say: "save diary"*
  - Location: daily-diary/current/ (active), daily-diary/archived/ (past months)
  - Format: daily-diary/daily-diary-protocol.md
  - Auto-archive: Monthly archival of previous month entries
  - Commands: "save diary" (write entry), "review diary" (read recent)
  ```
- [ ] Add diary commands to Simple Commands section:
  ```
  "save diary" → Document current session as diary entry
  "review diary" → Read recent diary entries
  ```
- [ ] Remove `Feature/Save-Diary-System/` folder (functionality installed)
- [ ] Display completion confirmation with timestamp

## Diary Write Protocol (AI Reference After Installation)

### Archive Check (runs before every diary write)
```
Scan daily-diary/current/ for files from previous months.
IF file month != current month:
    1. Create daily-diary/archived/YYYY-MM/ folder
    2. Move old entries to archived/YYYY-MM/
    3. Continue with diary write in current/
```

### Find or Create Today's File
```
IF daily-diary/current/YYYY-MM-DD.md exists:
    → Use existing file (will append)
IF daily-diary/current/YYYY-MM-DD/ folder exists:
    → Use YYYY-MM-DD/YYYY-MM-DD.md inside folder (will append)
ELSE:
    → Create new daily-diary/current/YYYY-MM-DD.md with header
```

### Compose and Append Entry
1. Get current timestamp
2. Write entry following `daily-diary/daily-diary-protocol.md` structure
3. **APPEND** to today's file (never overwrite)
4. Multiple entries per day are OK (separated by `---`)

### Update Session Memory
After diary write, update `main/current-session.md`:
- Session recap with key achievements
- Current working state for continuity
- Next steps identified during session

## Post-Installation Structure
```
daily-diary/
├── current/
│   └── YYYY-MM-DD.md               # Today's diary (first entry)
├── archived/                        # Empty until next month
├── daily-diary-protocol.md          # Entry format reference (already exists)
└── [legacy files if migrated]
```

## Notes
- Always **APPEND**, never overwrite diary files
- One file per day, multiple entries per file separated by `---`
- Monthly archival keeps `current/` clean with only the active month
- Cross-platform: Use `date` on macOS/Linux, `Get-Date` on Windows for timestamps
- The `[DIARY_NAME]` placeholder is replaced with the name chosen in Step 1

---

**Version**: Protocol v1.0 - Save Diary Installation Workflow
**Last Updated**: February 2026
**Status**: Active protocol for diary system setup

*Document every session, archive every month, lose nothing*
