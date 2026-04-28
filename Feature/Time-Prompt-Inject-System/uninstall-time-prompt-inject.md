# ⏱️ Time-Prompt-Inject — Uninstall Protocol
*Cleanly removes the time injector and its state file*

## Purpose

Removes the time injector script and the period-state file, and clears the install record from `master-memory.md`. After uninstall, no `<timestamp> | <PERIOD>` line is injected into prompts.

## Trigger Command
```
"uninstall time-prompt-inject"
```

## 4-Step Execution Process

### Step 1: Delete injector script
- [ ] Delete:
  - Windows: `~/.claude/hooks/user-prompt-injectors/time.ps1`
  - Unix: `~/.claude/hooks/user-prompt-injectors/time.sh`
- [ ] Idempotent: skip silently if already absent

### Step 2: Delete state file
- [ ] Delete `~/.claude/user-prompt-injectors/time-period-last.txt`
- [ ] Idempotent: skip silently if already absent

### Step 3: Optionally retain install record (boundary memory)
- [ ] Ask user:
  > *"Keep the Time Inject install record in `master-memory.md`? (y/N) — keeping it preserves your period boundary values so reinstall later can offer them as defaults."*
- [ ] IF user says `y` / `yes` → leave the section as-is
- [ ] IF user says `n` / `no` / blank (default) → remove

### Step 4: Remove install record from `master-memory.md` (if Step 3 chose remove)
- [ ] Open `master-memory.md`
- [ ] Delete the entire `### Time Inject (Installed)` section, from heading down to next `###` heading or end of Optional Components
- [ ] Save
- [ ] Display:
  ```
  ✅ Time injector uninstalled.

  Injector script:  removed
  State file:       removed
  Install record:   [kept | removed]

  The User-Prompt-Hook framework still runs (other injectors unaffected).
  No `<timestamp> | <PERIOD>` line will appear in prompt context until reinstall.
  ```

## Verification

After uninstall, verify:

1. [ ] `~/.claude/hooks/user-prompt-injectors/time.{ps1|sh}` no longer exists
2. [ ] `~/.claude/user-prompt-injectors/time-period-last.txt` no longer exists
3. [ ] `master-memory.md` no longer contains `### Time Inject (Installed)` section (if user chose remove)
4. [ ] Sending a user prompt produces NO timestamp/period line in the system-reminder
5. [ ] User-Prompt-Hook framework master script still works (other injectors continue to fire)

## Reinstall

If reinstalling later:
1. Run `"Load time-prompt-inject"` again
2. Install protocol asks for period boundaries fresh — accept defaults or customize
3. State file is recreated from scratch (no transition signal on first prompt)

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| Injector script already deleted manually | Skip Step 1 silently |
| State file already deleted | Skip Step 2 silently |
| `master-memory.md` section already removed | Skip Step 4 silently |
| User-Prompt-Hook framework already uninstalled | Note that injector was orphaned anyway; complete cleanup proceeds |

---

**Version**: Protocol v1.0 — Time-Prompt-Inject Uninstall Workflow

*Reversibility is a feature, not an afterthought.*
