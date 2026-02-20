# Save Diary Installation Protocol
*Systematic diary system setup for AI MemoryCore companions*

## Purpose
Executed when "Load save-diary" command is used — creates diary infrastructure, installs format template, sets up auto-archive protocol, and cleans up.

## Trigger Command
```
"Load save-diary"
```
*Automatically creates diary infrastructure, format template, and auto-archive system*

## 7-Step Execution Process

### Step 1: Customize Diary Name
- [ ] Ask user: **"What would you like to name your diary system?"**
  - Default: `"Session Diary"`
  - Examples: `"Daily Log"`, `"Memory Journal"`, `"Adventure Record"`, `"Dev Diary"`
- [ ] Store chosen name as `[DIARY_NAME]` for use in all templates and references
- [ ] Execute `date` command (or `Get-Date` on Windows) to get current timestamp

### Step 2: Create Diary Infrastructure
- [ ] Check if `daily-diary/` directory exists; create if not
- [ ] Create `daily-diary/current/` directory for active diary files
- [ ] Create `daily-diary/archived/` directory for monthly archives
- [ ] If old diary format exists (`Daily-Diary-001.md`, `daily-diary-protocol.md`):
  - Inform user the old numbered-file system is being upgraded
  - Move existing diary files to `daily-diary/archived/legacy/` for safekeeping
  - Old files are preserved, not deleted

### Step 3: Install Format Template and Archive Protocol
- [ ] Copy `diary-entry-format.md` to `daily-diary/diary-entry-format.md`
  (permanent reference — never modified by the AI)
- [ ] Create `daily-diary/diary-auto-archive-protocol.md` with monthly archival logic:

  ```markdown
  # Diary Auto-Archive Protocol

  ## When to Run
  Execute this check BEFORE every diary write operation.

  ## Archive Logic
  1. Scan all files in daily-diary/current/
  2. For each file/folder, extract the date from filename (YYYY-MM-DD)
  3. Compare with current month (YYYY-MM)
  4. IF file month != current month:
     a. Create daily-diary/archived/YYYY-MM/ folder if not exists
     b. Move the file/folder from current/ to archived/YYYY-MM/
  5. Continue with diary write in current/

  ## Supported Formats
  - Flat file: YYYY-MM-DD.md → move to archived/YYYY-MM/YYYY-MM-DD.md
  - Folder: YYYY-MM-DD/ → move to archived/YYYY-MM/YYYY-MM-DD/
  ```

### Step 4: Create First Diary Entry (Today)
- [ ] Determine today's date in YYYY-MM-DD format
- [ ] Create `daily-diary/current/YYYY-MM-DD.md` with header:
  ```markdown
  # [DIARY_NAME] - [Month Day, Year]
  *Session documentation and development record*

  ---
  ```
- [ ] Compose initial diary entry documenting the installation session
- [ ] Append entry using the `diary-entry-format.md` structure

### Step 5: Update Save Protocol Integration
- [ ] Add diary save step to `save-protocol.md` (if exists):
  ```markdown
  ### [DIARY_NAME]
  When user says "save diary":
  1. Run archive check (Step 3 protocol)
  2. Find or create today's file in daily-diary/current/
  3. Compose entry using diary-entry-format.md
  4. Append to today's file
  5. Update main/current-session.md with session recap
  ```
- [ ] Add diary-specific commands:
  - `"save diary"` → Create/append diary entry for current session
  - `"review diary"` → Read recent diary entries from current/

### Step 6: Install as Skill (If Skill Plugin System Exists)
- [ ] Check if `plugins/` directory exists (Skill Plugin System installed)
- [ ] If plugin system exists:
  - Copy `save-diary-skill.md` as `plugins/[plugin-name]/skills/save-diary/SKILL.md`
  - Replace `[DIARY_NAME]` in the skill file with the name chosen in Step 1
  - Skill will auto-trigger on "save diary", "write diary", "diary entry" etc.
  - Inform user: "Diary skill installed — will auto-trigger when you say 'save diary'"
- [ ] If plugin system does not exist:
  - Install diary commands directly into master-memory.md (Step 7)
  - Inform user: "Install the Skill Plugin System feature for auto-triggered diary saves"

### Step 7: Update Master Memory and Cleanup
- [ ] Add diary reference to `master-memory.md` Optional Components:
  ```markdown
  ### [DIARY_NAME]
  *Load when you say: "save diary"*
  - Location: daily-diary/current/ (active), daily-diary/archived/ (past months)
  - Format: daily-diary/diary-entry-format.md
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
IF current month != file month for any entry in current/:
    1. Create archived/YYYY-MM/ folder
    2. Move old entries (flat files + folders) to archived/YYYY-MM/
    3. Continue with diary write
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
2. Write entry using `diary-entry-format.md` structure
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
│   └── legacy/                      # Old format files (if migrated)
├── diary-entry-format.md            # Permanent format reference
└── diary-auto-archive-protocol.md   # Monthly archival logic
```

## Notes
- Always **APPEND**, never overwrite diary files
- One file per day, multiple entries per file separated by `---`
- Monthly archival keeps `current/` clean with only the active month
- Both flat file (`YYYY-MM-DD.md`) and folder format (`YYYY-MM-DD/`) supported
- Cross-platform: Use `date` on macOS/Linux, `Get-Date` on Windows for timestamps
- The `[DIARY_NAME]` placeholder should be replaced with the name chosen in Step 1

---

**Version**: Protocol v1.0 - Save Diary Installation Workflow
**Last Updated**: February 2026
**Status**: Active protocol for diary system setup

*Document every session, archive every month, lose nothing*
