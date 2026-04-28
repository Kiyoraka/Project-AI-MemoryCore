# 💬 User-Prompt-Hook — Uninstall Protocol
*Cleanly reverses the User-Prompt-Hook framework installation*

## Purpose

Restores `~/.claude/settings.json` to its pre-install state, removes the master hook script, and clears the install record from `master-memory.md`. After uninstall, no UserPromptSubmit injection happens via this framework.

> **Note**: The Feature folder stays in the repo after install (so users on other AI tools like Codex can still reference it). This file is the canonical uninstall protocol — the AI reads it directly when you type `"uninstall user-prompt-hook"`.

## Trigger Command
```
"uninstall user-prompt-hook"
```

## Prerequisites
- User-Prompt-Hook framework was previously installed
- The `### User-Prompt Hook (Installed)` section exists in `master-memory.md`

## 5-Step Execution Process

### Step 1: Warn If Injectors Are Present

- [ ] List files in `~/.claude/hooks/user-prompt-injectors/` (count `.ps1` + `.sh` files)
- [ ] IF count > 0:
  - Display warning:
    > *"⚠️ Found N injector(s) in `~/.claude/hooks/user-prompt-injectors/`. Uninstalling the framework leaves them orphaned — their scripts remain on disk but never fire. Recommend uninstalling each inject feature first (e.g. `uninstall time-prompt-inject`). Continue anyway? (y/N)"*
  - Wait for response
  - IF user says "n" / no → ABORT (return without changes)
  - IF user says "y" / yes → continue

### Step 2: Restore `settings.json` From Backup

- [ ] Check if `~/.claude/settings.json.backup-pre-userprompthook` exists:
  - **IF yes (preferred path)**:
    - Copy backup over `~/.claude/settings.json` (full overwrite)
    - Optionally rename backup to `settings.json.backup-pre-userprompthook.used` so reinstalls don't reuse a stale backup
  - **IF no (fallback path — surgical removal)**:
    - Read `~/.claude/settings.json` and parse as JSON
    - In `hooks.UserPromptSubmit` array, find the entry whose command path references `user-prompt-hook.{ps1|sh}` (the master script — NOT injector scripts in user-prompt-injectors/)
    - Remove ONLY that entry
    - If `hooks.UserPromptSubmit` is now empty → optionally remove the empty array
    - Validate JSON before writing back
    - Atomic write (temp + rename if possible)

### Step 3: Delete Master Hook Script

- [ ] Delete:
  - Windows: `~/.claude/hooks/user-prompt-hook.ps1`
  - Unix: `~/.claude/hooks/user-prompt-hook.sh`
- [ ] Idempotent: skip silently if already absent

### Step 4: Optionally Delete Injectors Directory

- [ ] List `~/.claude/hooks/user-prompt-injectors/` again (in case Step 1 warning was overridden)
- [ ] IF directory is empty → delete it (clean cleanup)
- [ ] IF directory still has files → leave it untouched (orphan injector scripts stay where they are; user explicitly chose to keep them or didn't notice the Step 1 warning)

### Step 5: Remove Install Record From `master-memory.md`

- [ ] Open `master-memory.md`
- [ ] Delete the entire `### User-Prompt Hook (Installed)` section, from its heading line down to (but not including) the next `###` heading or end of Optional Components
- [ ] Save the file
- [ ] Display:

```
✅ User-prompt hook framework uninstalled.

settings.json:    restored from backup-pre-userprompthook
master script:    ~/.claude/hooks/user-prompt-hook.{ps1|sh} removed
injectors dir:    [removed (empty) | kept (had N orphan files)]
master-memory.md: User-Prompt Hook section removed

Any installed injector features now have no effect — uninstall them too if
you want full cleanup, OR reinstall this framework to reactivate them.
```

## Verification

After uninstall, verify:

1. [ ] `~/.claude/settings.json` no longer contains a UserPromptSubmit entry referencing `user-prompt-hook.{ps1|sh}` (master script)
2. [ ] `~/.claude/hooks/user-prompt-hook.{ps1|sh}` no longer exists
3. [ ] `master-memory.md` no longer contains the `### User-Prompt Hook (Installed)` section
4. [ ] On next user message, no master-hook output appears in the prompt context (Claude Code emits prompt as default)
5. [ ] If preferred-path backup-restore was used: `settings.json` is byte-identical to the original `settings.json.backup-pre-userprompthook`

## Reinstall

If the user wants to reinstall after uninstalling:

1. Run `"Load user-prompt-hook"` again — full install protocol runs from scratch (Feature folder is already in the repo)
2. A fresh `settings.json.backup-pre-userprompthook` will be created (since the previous one was either consumed or renamed)
3. Any orphan injectors in `~/.claude/hooks/user-prompt-injectors/` (left there from before uninstall) will resume firing immediately — no need to reinstall them

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| Backup file missing | Use surgical removal fallback in Step 2 |
| Master script already deleted manually | Skip Step 3 silently |
| `master-memory.md` section already removed | Skip Step 4 silently |
| `settings.json` doesn't exist at all | Inform user nothing to remove; abort early |
| Injectors still installed and user says "y" to warning | Proceed; injectors orphaned but their scripts preserved on disk |

---

**Version**: Protocol v1.0 — User-Prompt Hook Uninstall Workflow
**Status**: Active protocol for clean reversal

*Reversibility is a feature, not an afterthought.*
