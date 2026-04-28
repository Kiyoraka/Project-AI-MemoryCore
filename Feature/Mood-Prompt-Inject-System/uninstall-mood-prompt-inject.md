# 🌙 Mood-Prompt-Inject — Uninstall Protocol
*Cleanly removes the mood injector while optionally preserving the registry*

## Purpose

Removes the mood injector script and current-state file, optionally strips the `## Moods` section from main memory, and clears the install record from `master-memory.md`. After uninstall, no `MOOD:` line is injected into prompts.

## Trigger Command
```
"uninstall mood-prompt-inject"
```

## 4-Step Execution Process

### Step 1: Delete injector script
- [ ] Delete:
  - Windows: `~/.claude/hooks/user-prompt-injectors/mood.ps1`
  - Unix: `~/.claude/hooks/user-prompt-injectors/mood.sh`
- [ ] Idempotent: skip silently if already absent

### Step 2: Delete current state file
- [ ] Delete `~/.claude/user-prompt-injectors/mood-current.txt`
- [ ] Idempotent: skip silently if already absent

### Step 3: Optionally remove `## Moods` section from main memory
- [ ] Detect main memory file (`main/main-memory.md` if exists, else `main/identity-core.md`)
- [ ] Ask user:
  > *"Keep your `## Moods` registry in main memory? (Y/n) — keeping it means you can reinstall later without re-entering all moods, and it stays as documentation even when the injector isn't active."*
- [ ] IF user says `n` / `no`:
  - Read main memory file
  - Locate the `## Moods` heading
  - Delete the section from the heading down to (but not including) the next `##` heading or end of file
  - Write back
- [ ] IF user says `y` / `yes` / blank (default) → leave the section as-is

### Step 4: Remove install record from `master-memory.md`
- [ ] Open `master-memory.md`
- [ ] Delete the entire `### Mood Inject (Installed)` section, from its heading down to (but not including) the next `###` heading or end of Optional Components
- [ ] Save
- [ ] Display:
  ```
  ✅ Mood injector uninstalled.

  Injector script:  removed
  Current state:    removed
  Registry:         [kept | removed]
  master-memory.md: Mood Inject section removed

  The User-Prompt-Hook framework still runs (other injectors unaffected).
  No `MOOD:` line will appear in prompt context until reinstall.
  ```

## Verification

After uninstall, verify:

1. [ ] `~/.claude/hooks/user-prompt-injectors/mood.{ps1|sh}` no longer exists
2. [ ] `~/.claude/user-prompt-injectors/mood-current.txt` no longer exists
3. [ ] If user chose to remove registry: main memory file no longer contains `## Moods` section
4. [ ] `master-memory.md` no longer contains `### Mood Inject (Installed)` section
5. [ ] Sending a user prompt produces NO `MOOD:` line in the system-reminder
6. [ ] User-Prompt-Hook framework master script still works (other injectors continue to fire)

## Reinstall

If reinstalling later:
1. Run `"Load mood-prompt-inject"` again
2. If you kept the `## Moods` registry → install detects it and offers to reuse (skipping Step 3 search-and-suggest)
3. If you removed the registry → install runs the full search-and-suggest flow as if first time

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| Injector script already deleted manually | Skip Step 1 silently |
| Current state file already deleted | Skip Step 2 silently |
| Main memory file missing | Skip Step 3 silently with note |
| `master-memory.md` section already removed | Skip Step 4 silently |
| User-Prompt-Hook framework already uninstalled | Note that injector was orphaned anyway; complete cleanup proceeds |

---

**Version**: Protocol v1.0 — Mood-Prompt-Inject Uninstall Workflow

*Reversibility is a feature, not an afterthought.*
