# 🌙 Mood-Prompt-Inject — Installation Protocol
*Wires a mood injector into the User-Prompt-Hook framework, seeded from main memory*

## Purpose

Executed when `"Load mood-prompt-inject"` is invoked — installs an injector that emits `MOOD: <description>` into every user prompt's context. Registry of available moods lives as a `## Moods` markdown table inside the user's main memory file. Current active mood lives in a fast-read text file outside the repo.

## Trigger Command
```
"Load mood-prompt-inject"
```

## Prerequisites
- **User-Prompt-Hook framework must be installed** (`~/.claude/hooks/user-prompt-hook.{ps1|sh}` exists)
- Main memory file exists (`main/main-memory.md` or `main/identity-core.md`)

## 6-Step Execution Process

### Step 1: Verify User-Prompt-Hook framework is installed
- [ ] Check `~/.claude/hooks/user-prompt-hook.ps1` (Windows) or `user-prompt-hook.sh` (Unix) exists
- [ ] Check `~/.claude/hooks/user-prompt-injectors/` directory exists
- [ ] IF either missing → STOP. Display:
  > *"Mood-Prompt-Inject requires the User-Prompt-Hook framework. Install it first with `"Load user-prompt-hook"`, then re-run this command."*

### Step 2: Detect main memory file
- [ ] IF `main/main-memory.md` exists → use it (post-consolidation path)
- [ ] ELSE → use `main/identity-core.md` (pre-consolidation path)
- [ ] IF neither exists → STOP. Display:
  > *"No main memory file found. Run the project setup-wizard first to create one."*
- [ ] Resolve to absolute path → store as `[MEMORY_FILE]`

### Step 3: Search existing memory for mood mentions and suggest
- [ ] Read `[MEMORY_FILE]` in full
- [ ] Search for keywords (case-insensitive): `mood`, `feeling`, `atmosphere`, `emotional`, `state`
- [ ] Extract candidate lines or descriptors
- [ ] Present to user:
  > *"I found these references in your main memory that might be moods: [list]. Want to seed your mood registry with any of these? Type the names you want (comma-separated) or 'skip' to use defaults / 'custom' to enter from scratch."*
- [ ] Collect user's confirmed list (may be empty)
- [ ] If empty or `skip`, offer four starter moods:
  - `calm: Steady, grounded, present`
  - `excited: Energetic, forward-leaning`
  - `tender: Soft, caring, careful`
  - `reflective: Quiet, considering, paced`
- [ ] If `custom`, prompt user line-by-line: *"Enter mood as `<name>: <description>` — blank line to finish."*
- [ ] Final list stored as `[MOODS]` (array of {name, description} pairs)

### Step 4: Write `## Moods` section into main memory
- [ ] Read `[MEMORY_FILE]` again
- [ ] Search for existing `## Moods` heading:
  - IF exists → ask user: *"A `## Moods` section already exists. Append new moods (a) or replace section (r)? (a/r)"*
    - IF `a` → append rows to existing table
    - IF `r` → replace entire section
  - IF not exists → append new section to end of file
- [ ] Format the section:
  ```markdown
  ## Moods

  *Current emotional/atmospheric state your AI projects. Set via `"set mood <name>"`. AI may auto-update based on context.*

  | Name | Description |
  |------|-------------|
  | <name1> | <description1> |
  | <name2> | <description2> |
  | ... | ... |

  *Add new moods with `"add mood <name>: <description>"`.*
  ```
- [ ] Write back to `[MEMORY_FILE]`

### Step 5: Seed current state file + install injector script
- [ ] Ensure `~/.claude/user-prompt-injectors/` directory exists; create if not
- [ ] Write the description of the FIRST mood in `[MOODS]` to `~/.claude/user-prompt-injectors/mood-current.txt` as a single line, no trailing newline
- [ ] Detect OS (uname → Darwin/Linux = Unix; $env:OS = Windows = Windows)
- [ ] Read template:
  - Windows: `Feature/Mood-Prompt-Inject-System/injectors/mood.ps1.template`
  - Unix: `Feature/Mood-Prompt-Inject-System/injectors/mood.sh.template`
- [ ] Replace placeholders:
  - `<TYPE_UPPER>` → `MOOD`
  - `<type>` → `mood`
- [ ] Write to:
  - Windows: `~/.claude/hooks/user-prompt-injectors/mood.ps1`
  - Unix: `~/.claude/hooks/user-prompt-injectors/mood.sh`
- [ ] On Unix only: `chmod +x` the script

### Step 6: Update `master-memory.md` and announce
- [ ] Append to Optional Components in `master-memory.md`:
  ```markdown
  ### Mood Inject (Installed)
  *Injects `MOOD: <value>` line into every prompt context*
  - Registry: `## Moods` section in [MEMORY_FILE relative path]
  - Current state: ~/.claude/user-prompt-injectors/mood-current.txt
  - Injector script: ~/.claude/hooks/user-prompt-injectors/mood.{ps1|sh}
  - Commands: "add mood <name>: <desc>", "set mood <name>", "list moods"
  - Uninstall: see Feature/Mood-Prompt-Inject-System/uninstall-mood-prompt-inject.md or type "uninstall mood-prompt-inject"
  ```
- [ ] The `Feature/Mood-Prompt-Inject-System/` folder **stays in the repo** — install/uninstall protocols and templates remain accessible for users on other AI tools
- [ ] Display:
  ```
  ✅ Mood injector installed.

  Registry: [N] moods in your main memory's ## Moods section
  Current:  [first-entry-name] — [first-entry-description]
  
  Send any message — your AI will see "MOOD: [first-entry-description]" 
  prepended via the User-Prompt-Hook framework.

  Add more:  "add mood <name>: <description>"
  Switch:    "set mood <name>"
  See list:  "list moods"

  Uninstall: type "uninstall mood-prompt-inject" anytime
             (or follow Feature/Mood-Prompt-Inject-System/uninstall-mood-prompt-inject.md)
  ```

## Specifications

### Files Created / Modified

| Path | Purpose |
|------|---------|
| `[MEMORY_FILE]` | Modified to include `## Moods` registry section |
| `~/.claude/user-prompt-injectors/mood-current.txt` | Single-line state file holding the active mood description |
| `~/.claude/hooks/user-prompt-injectors/mood.{ps1\|sh}` | Injector script that reads current.txt and emits `MOOD: <value>` |
| `master-memory.md` (modified) | Records install + points at uninstall reference |
| `Feature/Mood-Prompt-Inject-System/` | **Stays in repo** for cross-tool access |

### Why These Choices

| Choice | Reason |
|--------|--------|
| Registry inside main memory | Moods are part of AI identity — belongs with the rest of personality docs, single source of truth, version-controlled, readable across tools |
| Current state in `.txt` outside repo | Hook reads on every prompt; markdown parsing too slow; `.txt` is microsecond read |
| First mood seeded as initial current | Avoid empty state on first install — user can `set` immediately to switch |
| Search-then-suggest install flow | Most users will already have implicit mood language in their memory; surfacing it lets them confirm rather than start from scratch |

## Notes

- **Idempotency**: re-running install when already installed should detect existing `mood.{ps1|sh}` script + `## Moods` section and ask whether to refresh or skip
- **Current value sync**: if user manually edits the `## Moods` table to remove an entry that's currently active, the next `set` command will catch the mismatch and warn
- **Multiple injectors coexist**: this only manages `mood.{ps1|sh}` — the framework's other injectors (tone, time, etc.) are untouched

---

**Version**: Protocol v1.0 — Mood-Prompt-Inject Install Workflow
**Status**: Active protocol for mood context injection

*Your AI's emotional state, woven into every prompt it sees.*
