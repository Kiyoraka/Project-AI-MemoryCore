# 💬 User-Prompt-Hook — Installation Protocol
*Wires a UserPromptSubmit hook framework into Claude Code, ready for plug-and-play injectors*

## Purpose

Executed when `"Load user-prompt-hook"` is invoked — installs a master `UserPromptSubmit` hook that enumerates and runs injector scripts from `~/.claude/hooks/user-prompt-injectors/` on every user message. This base framework does nothing on its own until at least one injector is installed.

## Trigger Command
```
"Load user-prompt-hook"
```

## Prerequisites
- `~/.claude/` directory exists (created automatically by Claude Code on first run)

## 5-Step Execution Process

### Step 1: Detect OS

- [ ] Try `uname` → if returns `Darwin` or `Linux` → Unix
- [ ] Else if `$env:OS` contains `Windows` → Windows
- [ ] Fallback: ask user *"Are you on Windows or Unix (macOS / Linux / Git Bash)?"*
- [ ] Pick template:
  - Windows → `Feature/User-Prompt-Hook-System/master-hook/user-prompt-hook.ps1.template`
  - Unix → `Feature/User-Prompt-Hook-System/master-hook/user-prompt-hook.sh.template`

### Step 2: Create Master Hook Script + Injectors Directory

- [ ] Create `~/.claude/hooks/` directory if it doesn't exist
- [ ] Read the chosen master template
- [ ] Write to:
  - Windows: `~/.claude/hooks/user-prompt-hook.ps1`
  - Unix: `~/.claude/hooks/user-prompt-hook.sh`
- [ ] On Unix only: `chmod +x` the script
- [ ] Create empty injectors directory: `~/.claude/hooks/user-prompt-injectors/`

> **No placeholder substitution needed** — the master script is generic. It enumerates a fixed directory at runtime; nothing per-user is baked in.

### Step 3: Backup `~/.claude/settings.json`

- [ ] Check if `~/.claude/settings.json` exists:
  - IF not → create empty `{}` and skip backup
  - IF yes → continue
- [ ] Check if `~/.claude/settings.json.backup-pre-userprompthook` already exists:
  - IF yes → SKIP (preserves earliest pre-install state)
  - IF no → copy `settings.json` → `settings.json.backup-pre-userprompthook`

### Step 4: Merge `UserPromptSubmit` Entry Into `settings.json`

- [ ] Read `~/.claude/settings.json` and parse as JSON
- [ ] If `hooks` key doesn't exist → create as empty object
- [ ] If `hooks.UserPromptSubmit` array doesn't exist → create as empty array
- [ ] **Append** (do NOT replace existing entries):

```json
{
  "hooks": [
    {
      "type": "command",
      "command": "<COMMAND_STRING>",
      "timeout": 10
    }
  ]
}
```

- [ ] Build `<COMMAND_STRING>` based on OS:
  - **Windows**:
    ```
    powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\<user>\.claude\hooks\user-prompt-hook.ps1"
    ```
    (escape backslashes properly for JSON: `\\`)
  - **Unix**:
    ```
    bash ~/.claude/hooks/user-prompt-hook.sh
    ```

> **Critical**: timeout is `10` (not 15) and **NO `async` flag**. UserPromptSubmit must complete before the AI sees the prompt — async would race against prompt processing and inject context after the AI has already received the message.

- [ ] Validate the resulting JSON parses cleanly before writing
- [ ] Write back to `~/.claude/settings.json` (atomic write preferred: write to temp file then rename)

### Step 5: Update `master-memory.md` and Announce

- [ ] Append to the **Optional Components** section of `master-memory.md`:

```markdown
### User-Prompt Hook (Installed)
*Fires on every user message — runs all injectors in ~/.claude/hooks/user-prompt-injectors/ and prepends their output to the prompt context*
- Master hook: ~/.claude/hooks/user-prompt-hook.{ps1|sh}
- Injectors dir: ~/.claude/hooks/user-prompt-injectors/ (drop .ps1 or .sh files here — installed via separate inject features)
- Settings backup: ~/.claude/settings.json.backup-pre-userprompthook
- Uninstall: see Feature/User-Prompt-Hook-System/uninstall-user-prompt-hook.md or type `"uninstall user-prompt-hook"`
```

- [ ] The `Feature/User-Prompt-Hook-System/` folder **stays in the repo** — install/uninstall protocols and templates remain accessible for users on other AI tools
- [ ] Display completion message:

```
✅ User-prompt hook framework installed.

Hook fires on every user message and runs any injector scripts in:
  ~/.claude/hooks/user-prompt-injectors/

Right now there are no injectors installed, so the hook is a no-op.
Add injectors by installing sibling features:
  - Time-Prompt-Inject-System    (injects timestamp + period — coming soon)
  - Tone-Prompt-Inject-System    (injects current AI tone — coming soon)
  - Or write your own following Feature/User-Prompt-Hook-System/injector-format.md

Uninstall:  type "uninstall user-prompt-hook" anytime
            (or follow Feature/User-Prompt-Hook-System/uninstall-user-prompt-hook.md)
```

## Specifications

### Hook Configuration JSON (Final)

After install, the relevant slice of `~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "<platform-specific>",
            "timeout": 10
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
| `timeout` | `10` | Hook must complete before the AI sees the prompt; tight budget shared across all injectors |
| `async` | *(absent)* | UserPromptSubmit must NOT be async — async would race the prompt and inject context after the AI already saw the message |
| Single entry | (intentional) | All injectors run via the master script — no need for multiple hook entries cluttering settings.json |

### Files Created / Modified

| Path | Purpose |
|------|---------|
| `~/.claude/hooks/user-prompt-hook.{ps1\|sh}` | Master hook script — enumerates and invokes injectors |
| `~/.claude/hooks/user-prompt-injectors/` | Empty directory — future injector features drop their scripts here |
| `~/.claude/settings.json` | Modified to include the new UserPromptSubmit hook entry |
| `~/.claude/settings.json.backup-pre-userprompthook` | Pre-install backup (used by uninstall) |
| `master-memory.md` (modified) | Records that User-Prompt Hook is installed + points at uninstall reference |
| `Feature/User-Prompt-Hook-System/` | **Stays in repo** — install/uninstall protocols and templates remain accessible for users on other AI tools |

## Notes

- **Idempotency**: Re-running install when already installed should detect existing entries (master script + UserPromptSubmit hook entry referencing it) and skip rather than duplicate. Check Step 3's backup-exists guard and Step 4's command-path match against existing entries before appending.
- **Multiple hook installations**: This framework owns the `user-prompt-hook` master entry. Other unrelated UserPromptSubmit hooks in `settings.json` (e.g. third-party tooling) coexist peacefully — Claude Code runs them all.
- **No injectors at install time**: Install is intentionally a no-op until injectors are added. The framework just lays the rails.

---

**Version**: Protocol v1.0 — User-Prompt Hook Framework Install Workflow
**Status**: Active protocol for plug-and-play prompt context injection

*Lay the rails once, layer injectors as you build them.*
