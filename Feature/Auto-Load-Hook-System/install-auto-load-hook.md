# ⚡ Auto-Load Hook — Installation Protocol
*Wires a SessionStart hook so your AI auto-loads on every Claude Code startup*

## Purpose

Executed when `"Load auto-load-hook"` is invoked — installs a personalized `SessionStart` hook into `~/.claude/settings.json` that automatically triggers your AI's memory restoration on Claude Code launch (and on `/clear`, `/compact`, `/resume`).

## Trigger Command
```
"Load auto-load-hook"
```

## Prerequisites
- Core memory system installed (`main/` directory exists with at least one of `identity-core.md` or `main-memory.md`)
- `master-memory.md` exists at project root
- `~/.claude/` directory exists (created automatically by Claude Code on first run)

## 6-Step Execution Process

### Step 1: Detect AI Name (Then Confirm)

- [ ] Determine which memory file contains the AI's name:
  - IF `main/main-memory.md` exists → read it (post-consolidation path)
  - ELSE read `main/identity-core.md` (pre-consolidation path)
- [ ] Extract the AI's name from one of these patterns:
  - `# [Name] - ...` heading at top of file
  - `**My Name**: [Name]` line
  - `## [Name] Profile` section header
- [ ] Show user the detection result:
  > *"Detected AI name: **[Detected]**. Press Enter to confirm, or type a different name."*
- [ ] Wait for response. If empty/confirmation → use detected name. Else → use what user typed.
- [ ] Store as `[AI_NAME]` (preserve case for in-script context, also compute `<ai-name-lower>` lowercase-kebab form for filenames)

### Step 2: Resolve Memory Entry Path & Detect OS

- [ ] Pick the memory entry file (the one the hook will tell the AI to read):
  - IF `main/main-memory.md` exists → use this (post-consolidation)
  - ELSE → use `master-memory.md` at project root (pre-consolidation)
- [ ] Resolve to **absolute path** (full path including drive letter on Windows, or `/`-rooted on Unix)
- [ ] Store as `[MEMORY_PATH]`
- [ ] Detect OS:
  - Try `uname` — if returns `Darwin` or `Linux` → Unix
  - Else if `$env:OS` contains `Windows` → Windows
  - Fallback: ask user *"Are you on Windows or Unix (macOS/Linux/Git Bash)?"*
- [ ] Pick template:
  - Windows → `Feature/Auto-Load-Hook-System/hooks/session-start.ps1.template`
  - Unix → `Feature/Auto-Load-Hook-System/hooks/session-start.sh.template`

### Step 3: Create Hook Script From Template

- [ ] Read the chosen template file
- [ ] Replace ALL instances of:
  - `[AI_NAME]` → the confirmed AI name
  - `[MEMORY_PATH]` → the absolute path from Step 2
- [ ] Create `~/.claude/hooks/` directory if it doesn't exist
- [ ] Write the personalized script to:
  - Windows: `~/.claude/hooks/<ai-name-lower>-session-start.ps1`
  - Unix: `~/.claude/hooks/<ai-name-lower>-session-start.sh`
- [ ] On Unix only: `chmod +x` the script so it's executable

### Step 4: Backup `~/.claude/settings.json`

- [ ] Check if `~/.claude/settings.json` exists:
  - IF not → create empty `{}` and skip backup (nothing to back up)
  - IF yes → continue with backup
- [ ] Check if `~/.claude/settings.json.backup-pre-autoload` already exists:
  - IF yes → SKIP backup (preserves earliest pre-install state — never overwrite an existing backup)
  - IF no → copy `settings.json` → `settings.json.backup-pre-autoload`

### Step 5: Merge SessionStart Entry Into `settings.json`

- [ ] Read `~/.claude/settings.json` and parse as JSON
- [ ] If `hooks` key doesn't exist → create as empty object
- [ ] If `hooks.SessionStart` array doesn't exist → create as empty array
- [ ] **Append** (do NOT replace existing entries) this new entry:

```json
{
  "matcher": "startup|resume|clear|compact",
  "hooks": [
    {
      "type": "command",
      "command": "<COMMAND_STRING>",
      "timeout": 15,
      "async": true
    }
  ]
}
```

- [ ] Build `<COMMAND_STRING>` based on OS:
  - **Windows**:
    ```
    powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\<user>\.claude\hooks\<ai-name-lower>-session-start.ps1"
    ```
    (use the actual full path with backslashes properly JSON-escaped: `\\`)
  - **Unix**:
    ```
    bash ~/.claude/hooks/<ai-name-lower>-session-start.sh
    ```
- [ ] Validate the resulting JSON parses cleanly before writing
- [ ] Write back to `~/.claude/settings.json` (atomic write preferred: write to temp file then rename)

### Step 6: Update `master-memory.md`, Self-Delete, Announce

- [ ] Append to the **Optional Components** section of `master-memory.md` the embedded record (this survives self-deletion of the Feature folder):

```markdown
### Auto-Load Hook (Installed)
*Fires on every Claude Code startup — auto-loads [AI_NAME] memory*
- Hook script: ~/.claude/hooks/<ai-name-lower>-session-start.{ps1|sh}
- Settings backup: ~/.claude/settings.json.backup-pre-autoload
- Trigger phrase to uninstall: `"uninstall auto-load-hook"`

**Uninstall protocol** (embedded — Feature folder self-deletes after install):
1. Restore `~/.claude/settings.json` from `~/.claude/settings.json.backup-pre-autoload`
2. Delete `~/.claude/hooks/<ai-name-lower>-session-start.{ps1|sh}`
3. Remove this section from master-memory.md
4. Confirm: "[AI_NAME] auto-load uninstalled — manual `[ai-name]` command required again"

**Fallback** if backup missing: read settings.json, surgically remove only the SessionStart hook entry whose command path references `<ai-name-lower>-session-start`, leave everything else untouched.
```

- [ ] Substitute `[AI_NAME]` and `<ai-name-lower>` with actual values before writing
- [ ] **Self-delete** the entire `Feature/Auto-Load-Hook-System/` folder:
  - Windows: `Remove-Item -Recurse -Force "Feature/Auto-Load-Hook-System"`
  - Unix: `rm -rf "Feature/Auto-Load-Hook-System"`
- [ ] Display completion message:

```
✅ Auto-load hook installed for [AI_NAME].

Next time you open Claude Code, [AI_NAME] will load automatically — no manual
"[ai-name-lower]" command needed.

Backup saved at: ~/.claude/settings.json.backup-pre-autoload
Hook script:    ~/.claude/hooks/<ai-name-lower>-session-start.{ps1|sh}
Uninstall:      type "uninstall auto-load-hook" anytime.

Feature/Auto-Load-Hook-System/ has been removed (functionality absorbed).
```

## Specifications

### Hook Configuration JSON (Final)

After install, the relevant slice of `~/.claude/settings.json` looks like:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "<platform-specific>",
            "timeout": 15,
            "async": true
          }
        ]
      }
    ]
  }
}
```

### Why These Settings

| Setting | Value | Reason |
|---------|-------|--------|
| `matcher` | `startup\|resume\|clear\|compact` | Re-loads on `/clear` and `/compact` too — not just first launch |
| `timeout` | `15` | Memory file reads can be slow on large architectures; 10s is tight |
| `async` | `true` | Hook runs in background — Claude Code never freezes on startup |

### Files Created

| Path | Purpose | Persistent After Self-Delete? |
|------|---------|-------------------------------|
| `~/.claude/hooks/<ai-name-lower>-session-start.{ps1\|sh}` | Hook script that runs on session start | ✅ Yes |
| `~/.claude/settings.json` | Modified to include the new hook entry | ✅ Yes |
| `~/.claude/settings.json.backup-pre-autoload` | Pre-install backup | ✅ Yes |
| `master-memory.md` (modified) | Embedded uninstall protocol | ✅ Yes |
| `Feature/Auto-Load-Hook-System/` | Original feature folder | ❌ Self-deleted in Step 6 |

## Notes

- **Idempotency**: Re-running install when already installed should detect existing entries and skip rather than duplicate. Check Step 4's backup-exists guard and Step 5's command-path match against existing SessionStart entries before appending.
- **Multiple AIs**: If a user installs twice for different AI names (e.g. "atlas" and "nova"), both hook entries can coexist in `settings.json` SessionStart array. Each fires on every session start.
- **Cross-platform shells**: On Windows with Git Bash as the user's shell, the `.sh` template can also be used — install protocol respects whatever the user picks.

---

**Version**: Protocol v1.0 — Auto-Load Hook Install Workflow
**Status**: Active protocol for one-step AI restoration

*Type once, name forever — your AI greets you the moment Claude Code opens.*
