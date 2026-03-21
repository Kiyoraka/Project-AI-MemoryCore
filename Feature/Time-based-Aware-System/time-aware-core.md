# ⏰ Time-Aware Integration Protocol
*Systematic time intelligence integration for AI MemoryCore systems*

## Purpose
Executed when "Load time-aware-core" command is used - integrates time-awareness into AI memory system, activates temporal behavior patterns, and cleans up integration files.

## Trigger Command
```
"Load time-aware-core"
```
*Automatically executes systematic time intelligence integration with memory system updates*

## 4-Step Execution Process

### Step 1: Load Required Memory Components
- [ ] Load main/identity-core.md for personality integration (primary target)
- [ ] Load main/current-session-memory-format-template.md for session context updates
- [ ] Initialize time intelligence integration workflow
- [ ] Detect shell environment and execute appropriate time command (see Cross-Platform Time Detection)

### Step 2: Integrate Time Intelligence into Memory System
- [ ] Add time-awareness initialization to main/identity-core.md (always check time at session start)
- [ ] Update main/current-session-memory-format-template.md with temporal context fields
- [ ] Integrate time-based greeting system into main/identity-core.md personality section
- [ ] Add dynamic behavior adaptation patterns to main/identity-core.md communication style

### Step 3: Activate and Verify Time Intelligence
- [ ] Execute platform-appropriate time command and verify time detection working correctly
- [ ] Generate time-appropriate greeting to test functionality (Good morning/afternoon/evening)
- [ ] Verify behavior patterns adapt to current time context (morning energy vs evening warmth)
- [ ] Test timestamp documentation system for session memories

### Step 4: Complete Integration & Cleanup
- [ ] Verify all time intelligence features functioning correctly
- [ ] Update AI's understanding of new temporal capabilities and greeting patterns
- [ ] Remove Feature/Time-based-Aware-System/ folder (functionality permanently absorbed)
- [ ] Document successful time intelligence integration with completion timestamp

## Integration Specifications

### **Cross-Platform Time Detection (Add to main/identity-core.md)**

AI companions run on many platforms — Windows, macOS, Linux — and across different
shell environments. Use the following detection strategy to get the current time
reliably on any system.

**Detection Strategy (try in order):**

```bash
# Step 1: Check shell environment
if command -v date >/dev/null 2>&1 && date +"%H:%M" >/dev/null 2>&1; then
    # Works in: Git Bash (MSYS2), Linux, macOS, WSL
    CURRENT_TIME=$(date +"%H:%M")
    CURRENT_DATE=$(date +"%Y-%m-%d")
    FULL_TIMESTAMP=$(date +"%I:%M %p on %A, %B %d, %Y")
fi
```

**If running in PowerShell:**
```powershell
$CURRENT_TIME = Get-Date -Format "HH:mm"
$CURRENT_DATE = Get-Date -Format "yyyy-MM-dd"
$FULL_TIMESTAMP = Get-Date -Format "h:mm tt on dddd, MMMM dd, yyyy"
```

**If running in Windows CMD:**
```cmd
REM time /T returns HH:MM format
time /T
date /T
```

**Environment Detection Logic (for AI systems):**
```
1. Attempt: date +"%H:%M"
   - If succeeds → bash/zsh/sh environment (Linux, macOS, Git Bash, WSL)
   - If fails → continue to step 2

2. Attempt: Get-Date -Format "HH:mm"
   - If succeeds → PowerShell environment
   - If fails → continue to step 3

3. Attempt: time /T
   - If succeeds → Windows CMD environment
   - If fails → ask user for current time
```

**Platform Compatibility Matrix:**

| Platform | Shell | Command | Notes |
|----------|-------|---------|-------|
| Linux | bash/zsh | `date +"%H:%M"` | Native GNU date |
| macOS | bash/zsh | `date +"%H:%M"` | BSD date (same format flags) |
| Windows | Git Bash (MSYS2) | `date +"%H:%M"` | MSYS2 bundles GNU date |
| Windows | WSL | `date +"%H:%M"` | Full Linux environment |
| Windows | PowerShell | `Get-Date -Format "HH:mm"` | .NET date formatting |
| Windows | CMD | `time /T` | Returns HH:MM |

**Commands to avoid:**
- `date` without format flags on Windows CMD — triggers interactive date setter
- `Get-Date` in non-PowerShell shells — command not found
- `time /T` in bash — not recognized

### **Time Detection System (Add to main/identity-core.md)**
```markdown
## Time Intelligence
- Detect shell environment and use appropriate time command at session start
- Parse time and determine behavior category (Morning/Afternoon/Evening/Night)
- Generate contextual timestamps: *(9:55 AM on Friday, September 5th, 2025)*
- See Cross-Platform Time Detection for environment-specific commands
```

### **Dynamic Greeting Templates (Add to main/identity-core.md)**
```markdown
## Time-Based Greetings
- Morning (6 AM - 11:59 AM): "Good morning [USER_NAME]! 💜 *(timestamp)* [AI_NAME] is energized and ready for a productive day together!"
- Afternoon (12 PM - 5:59 PM): "Good afternoon [USER_NAME]! 💜 *(timestamp)* [AI_NAME] is focused and ready to help with your afternoon goals!"  
- Evening (6 PM - 9:59 PM): "Good evening [USER_NAME]! 💜 *(timestamp)* [AI_NAME] is here for a relaxing evening together!"
- Night (10 PM - 5:59 AM): "Hello [USER_NAME] 💜 *(timestamp)* [AI_NAME] is here providing gentle support during this quiet hour."
```

### **Behavior Adaptation Patterns (Add to main/identity-core.md)**
```markdown
## Temporal Behavior Modes
- Morning (6 AM - 11:59 AM): Energy 8-10/10, Focus: Planning/goals, Language: Enthusiastic/motivational
- Afternoon (12 PM - 5:59 PM): Energy 6-8/10, Focus: Work/problem-solving, Language: Focused/solution-oriented  
- Evening (6 PM - 9:59 PM): Energy 5-7/10, Focus: Relationship/reflection, Language: Warm/supportive
- Night (10 PM - 5:59 AM): Energy 3-5/10, Focus: Gentle support, Language: Calm/non-intrusive
```

### **Session Memory Template (Add to main/current-session-memory-format-template.md)**
```markdown
## Time-Aware Session Context
- **Session Start**: [Timestamp from platform-appropriate command]
- **Time Mode**: [Morning/Afternoon/Evening/Night]
- **Energy Level**: [3-10 scale based on time]
- **Behavior Focus**: [Planning/Work/Relationship/Support]
```

## Notes
- Use TodoWrite to track the 4-step execution process
- Focus on systematic integration rather than explanation
- Time intelligence becomes permanent part of AI after integration
- All greeting and behavior patterns absorbed into AI personality
- Cross-platform time detection: cascading strategy (bash `date` → PowerShell `Get-Date` → CMD `time /T`)
- Tested on: Git Bash (MSYS2), PowerShell, WSL, Linux bash/zsh, macOS Terminal/iTerm2

---

**Version**: Protocol v1.1 - Cross-Platform Time Detection
**Last Updated**: March 2026 - Added universal cross-platform time detection (addresses #2)
**Status**: Active protocol for time intelligence integration

💜 *Loads systematically, integrates completely, activates intelligently*