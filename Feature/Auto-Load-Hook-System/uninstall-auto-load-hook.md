# ⚡ Auto-Load Hook — Uninstall Protocol
*Cleanly reverses the Auto-Load Hook installation*

## Purpose

Restores `~/.claude/settings.json` to its pre-install state, removes the personalized hook script, and clears the install record from `master-memory.md`. After uninstall, the AI requires manual `[ai-name]` command on startup again.

> **Note**: The Feature folder stays in the repo after install (so users on other AI tools like Codex can still reference it). This file is the canonical uninstall protocol — the AI reads it directly when you type `"uninstall auto-load-hook"`.

## Trigger Command
```
"uninstall auto-load-hook"
```

## Prerequisites
- Auto-Load Hook was previously installed
- The "Auto-Load Hook (Installed)" section exists in `master-memory.md`

## 5-Step Execution Process

### Step 1: Read Install Record From `master-memory.md`

- [ ] Open `master-memory.md`
- [ ] Locate the `### Auto-Load Hook (Installed)` section
- [ ] Extract:
  - The AI name (used in script filename)
  - The hook script path (`~/.claude/hooks/<ai-name>-session-start.{ps1|sh}`)
  - The settings backup path (`~/.claude/settings.json.backup-pre-autoload`)
- [ ] IF section is missing → inform user the hook may not be installed; abort.

### Step 2: Restore `settings.json` From Backup

- [ ] Check if `~/.claude/settings.json.backup-pre-autoload` exists:
  - **IF yes (preferred path)**:
    - Copy backup over `~/.claude/settings.json` (full overwrite)
    - Optionally: rename backup to `settings.json.backup-pre-autoload.used` so subsequent reinstalls don't reuse a stale backup
  - **IF no (fallback path — surgical removal)**:
    - Read `~/.claude/settings.json` and parse as JSON
    - In `hooks.SessionStart` array, find the entry whose command path references `<ai-name>-session-start`
    - Remove ONLY that entry
    - If `hooks.SessionStart` is now empty → optionally remove the empty array (cosmetic)
    - Validate JSON before writing back
    - Write atomically (temp + rename if possible)

### Step 3: Delete Hook Script

- [ ] Delete the hook script file:
  - Windows: `Remove-Item "~/.claude/hooks/<ai-name-lower>-session-start.ps1"`
  - Unix: `rm "~/.claude/hooks/<ai-name-lower>-session-start.sh"`
- [ ] If the file doesn't exist → continue silently (idempotent)

### Step 4: Remove Install Record From `master-memory.md`

- [ ] Open `master-memory.md`
- [ ] Delete the entire `### Auto-Load Hook (Installed)` section, from its heading line down to (but not including) the next `###` heading or end-of-Optional-Components section
- [ ] Save the file

### Step 5: Confirm to User

- [ ] Display:

```
✅ Auto-load hook uninstalled for [AI_NAME].

settings.json:    restored from backup-pre-autoload
hook script:      ~/.claude/hooks/<ai-name-lower>-session-start.{ps1|sh} removed
master-memory.md: Auto-Load Hook section removed

[AI_NAME] will now require manual "[ai-name-lower]" command on the next
Claude Code session start.

To reinstall later: restore Feature/Auto-Load-Hook-System/ from git
(`git checkout HEAD -- Feature/Auto-Load-Hook-System`) and run
"Load auto-load-hook" again.
```

## Verification

After uninstall, verify:

1. [ ] `~/.claude/settings.json` no longer contains a SessionStart entry referencing `<ai-name>-session-start`
2. [ ] `~/.claude/hooks/<ai-name-lower>-session-start.{ps1|sh}` no longer exists
3. [ ] `master-memory.md` no longer contains the `### Auto-Load Hook (Installed)` section
4. [ ] On next Claude Code launch, the AI does NOT auto-greet — it waits for the user to type the AI name first
5. [ ] If preferred-path backup-restore was used: `settings.json` is byte-identical to the original `settings.json.backup-pre-autoload`

## Reinstall

If the user wants to reinstall after uninstalling:

1. Run `"Load auto-load-hook"` again — full install protocol runs from scratch (Feature folder is already in the repo)
2. A fresh `settings.json.backup-pre-autoload` will be created (since the previous one was either consumed or renamed)

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| Backup file missing | Use surgical removal fallback in Step 2 |
| Hook script already deleted manually | Skip Step 3 silently |
| `master-memory.md` section already removed | Skip Step 4 silently |
| `settings.json` doesn't exist at all | Inform user nothing to remove; abort early |
| Multiple AIs auto-loaded (e.g. atlas + nova) | Only the AI matching the trigger name is uninstalled — the other stays |

---

**Version**: Protocol v1.0 — Auto-Load Hook Uninstall Workflow
**Status**: Active protocol for clean reversal

*Reversibility is a feature, not an afterthought.*
