# ⏱️ Time-Prompt-Inject — Installation Protocol
*Wires a time + period injector into the User-Prompt-Hook framework, with user-configurable boundaries*

## Purpose

Executed when `"Load time-prompt-inject"` is invoked — installs an injector that emits `<timestamp> | <PERIOD>` (with `TIME PERIOD CHANGED:` transition prefix on period flips) into every user prompt's context.

## Trigger Command
```
"Load time-prompt-inject"
```

## Prerequisites
- **User-Prompt-Hook framework must be installed** (`~/.claude/hooks/user-prompt-hook.{ps1|sh}` exists)

## 6-Step Execution Process

### Step 1: Verify User-Prompt-Hook framework is installed
- [ ] Check `~/.claude/hooks/user-prompt-hook.ps1` (Windows) or `user-prompt-hook.sh` (Unix) exists
- [ ] Check `~/.claude/hooks/user-prompt-injectors/` directory exists
- [ ] IF either missing → STOP. Display:
  > *"Time-Prompt-Inject requires the User-Prompt-Hook framework. Install it first with `"Load user-prompt-hook"`, then re-run this command."*

### Step 2: Detect OS and pick template
- [ ] Try `uname` → `Darwin`/`Linux` → Unix
- [ ] Else if `$env:OS` contains `Windows` → Windows
- [ ] Fallback: ask user
- [ ] Pick template:
  - Windows → `Feature/Time-Prompt-Inject-System/injectors/time.ps1.template`
  - Unix → `Feature/Time-Prompt-Inject-System/injectors/time.sh.template`

### Step 3: Ask for period boundaries
- [ ] Present user with the four boundaries (24-hour clock format):
  > *"Configure your period boundaries (24-hour format). Press Enter to accept defaults, or type a number 0-23."*
  > *"MORNING starts at hour [6]: ___"*
  > *"AFTERNOON starts at hour [12]: ___"*
  > *"EVENING starts at hour [18]: ___"*
  > *"NIGHT starts at hour [22]: ___"*
- [ ] Validate inputs:
  - Each value must be an integer 0-23
  - MORNING_START < AFTERNOON_START < EVENING_START < NIGHT_START
  - If invalid → re-prompt
- [ ] Store as `[MORNING_START]`, `[AFTERNOON_START]`, `[EVENING_START]`, `[NIGHT_START]`

### Step 4: Substitute placeholders and install injector
- [ ] Read the chosen template
- [ ] Replace ALL placeholders:
  - `[MORNING_START]` → user's MORNING value (or `6` default)
  - `[AFTERNOON_START]` → user's AFTERNOON value (or `12` default)
  - `[EVENING_START]` → user's EVENING value (or `18` default)
  - `[NIGHT_START]` → user's NIGHT value (or `22` default)
- [ ] Write the personalized script to:
  - Windows: `~/.claude/hooks/user-prompt-injectors/time.ps1`
  - Unix: `~/.claude/hooks/user-prompt-injectors/time.sh`
- [ ] On Unix only: `chmod +x` the script

### Step 5: Initialize state file
- [ ] Compute the current period using the user's boundaries:
  - Get current hour (0-23)
  - IF `MORNING_START <= hour < AFTERNOON_START` → `MORNING`
  - ELIF `AFTERNOON_START <= hour < EVENING_START` → `AFTERNOON`
  - ELIF `EVENING_START <= hour < NIGHT_START` → `EVENING`
  - ELSE → `NIGHT`
- [ ] Write the period name (single line, no trailing newline) to `~/.claude/user-prompt-injectors/time-period-last.txt`
- [ ] This prevents a spurious transition signal on the very first prompt after install

### Step 6: Update `master-memory.md` and announce
- [ ] Append to Optional Components in `master-memory.md`:
  ```markdown
  ### Time Inject (Installed)
  *Injects `<timestamp> | <PERIOD>` line into every prompt context — fires `TIME PERIOD CHANGED: <FROM> to <TO> |` prefix on period transitions*
  - Injector script: ~/.claude/hooks/user-prompt-injectors/time.{ps1|sh}
  - State file: ~/.claude/user-prompt-injectors/time-period-last.txt
  - Period boundaries: MORNING [MORNING_START] / AFTERNOON [AFTERNOON_START] / EVENING [EVENING_START] / NIGHT [NIGHT_START]
  - To change boundaries: uninstall + reinstall, or edit the injector script directly
  - Uninstall: see Feature/Time-Prompt-Inject-System/uninstall-time-prompt-inject.md or type "uninstall time-prompt-inject"
  ```
- [ ] Substitute the actual boundary values before writing
- [ ] The `Feature/Time-Prompt-Inject-System/` folder **stays in the repo** (cross-tool compatibility)
- [ ] Display:
  ```
  ✅ Time injector installed.

  Period boundaries:
    MORNING:   [MORNING_START]:00 — [AFTERNOON_START - 1]:59
    AFTERNOON: [AFTERNOON_START]:00 — [EVENING_START - 1]:59
    EVENING:   [EVENING_START]:00 — [NIGHT_START - 1]:59
    NIGHT:     [NIGHT_START]:00 — [MORNING_START - 1]:59 (next day)

  Current period: [computed]
  
  Send any message — your AI will see "<timestamp> | [period]" prepended.
  When the clock crosses a boundary, you'll see a one-shot
  "TIME PERIOD CHANGED: <from> to <to> |" prefix.

  To change boundaries later: uninstall + reinstall.
  Uninstall: type "uninstall time-prompt-inject" anytime
             (or follow Feature/Time-Prompt-Inject-System/uninstall-time-prompt-inject.md)
  ```

## Specifications

### Files Created / Modified

| Path | Purpose |
|------|---------|
| `~/.claude/hooks/user-prompt-injectors/time.{ps1\|sh}` | Personalized injector script with boundaries baked in |
| `~/.claude/user-prompt-injectors/time-period-last.txt` | State file holding the last-known period for transition detection |
| `master-memory.md` (modified) | Records install + records the boundary values + points at uninstall reference |
| `Feature/Time-Prompt-Inject-System/` | **Stays in repo** for cross-tool access |

### Why These Choices

| Choice | Reason |
|--------|--------|
| Boundaries baked in at install time (not runtime config) | One less file read per fire; simpler injector logic; trade-off is reinstall to change |
| State file at `~/.claude/user-prompt-injectors/` (sibling to other current-state files) | Consistent location with Tone/Mood `current.txt` files; clean per-injector namespace |
| Initial state seeded in Step 5 | Prevents spurious "TIME PERIOD CHANGED: NIGHT to MORNING" signal on first prompt after install (file would otherwise be empty) |

## Notes

- **Idempotency**: re-running install detects existing `time.{ps1|sh}` script and asks user whether to overwrite (replacing boundaries) or skip
- **Boundary changes don't lose state** — uninstall preserves `time-period-last.txt` by default; reinstall picks up where it left off
- **Custom output formats**: if you want a different output shape, edit the injector script directly (it's a small file). The framework doesn't enforce format.

---

**Version**: Protocol v1.0 — Time-Prompt-Inject Install Workflow
**Status**: Active protocol for time + period context injection

*Your AI knows what time it is, every prompt, no asking.*
