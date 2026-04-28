# 🎭 Tone-Prompt-Inject — Runtime Commands
*Reference for `add tone`, `set tone`, `list tones` — used by the AI when these phrases fire*

## Purpose

After `Tone-Prompt-Inject-System` is installed, the AI handles three runtime commands that manage the tone registry and active tone. This file documents the exact behavior so the AI can execute them consistently.

## Detect main memory file once

All three commands operate on the user's main memory file. Detection is uniform:
- IF `main/main-memory.md` exists → that's `[MEMORY_FILE]`
- ELSE → `main/identity-core.md`

Cache this for the session if possible.

---

## Command: `"add tone <name>: <description>"`

**Trigger phrases**: `"add tone"`, `"register tone"`, `"new tone"`

**Steps**:
1. Parse `<name>` and `<description>` from the user's message
   - Example input: `add tone gentle: soft, slow, careful — bedside-reading register`
   - `<name>` = `gentle`
   - `<description>` = `soft, slow, careful — bedside-reading register`
2. Read `[MEMORY_FILE]`
3. Locate the `## Tones` heading and its markdown table
4. Validate: check `<name>` doesn't already exist as a row
   - IF exists → ask user whether to replace or rename:
     > *"Tone `<name>` already exists with description `<existing>`. Replace (r) or use a different name (n)? (r/n)"*
5. Append a new row to the table:
   ```
   | <name> | <description> |
   ```
6. Write `[MEMORY_FILE]` back
7. Confirm:
   > *"Added `<name>` to your tone registry. Use `"set tone <name>"` to activate it."*

---

## Command: `"set tone <name>"`

**Trigger phrases**: `"set tone"`, `"switch tone"`, `"change tone"`, `"use tone"`

**Steps**:
1. Parse `<name>` from the user's message
2. Read `[MEMORY_FILE]`
3. Locate `## Tones` table, search for row with matching `<name>` (case-insensitive)
4. IF NOT found:
   - Suggest closest match (Levenshtein-style or substring) from registry
   - Display available tones inline
   - Wait for user clarification
5. IF found:
   - Extract the description from the matching row
   - Write the description to `~/.claude/user-prompt-injectors/tone-current.txt` as a single line, no trailing newline
6. Confirm:
   > *"Active tone set to `<name>` — `<description>`. Next prompt will inject `TONE: <description>`."*

**Note**: write the **description**, not the name, to current.txt. The injector emits the description directly so the AI sees rich context.

---

## Command: `"list tones"`

**Trigger phrases**: `"list tones"`, `"show tones"`, `"what tones"`, `"available tones"`

**Steps**:
1. Read `[MEMORY_FILE]`
2. Extract the `## Tones` section
3. Display the markdown table inline (or render it as a list if better for the chat surface)
4. Append a hint:
   > *"Active tone is `<lookup-current.txt>`. Use `"set tone <name>"` to switch, or `"add tone <name>: <description>"` to register a new one."*

---

## AI Auto-Set (no command typed)

When the AI senses a tone shift naturally during conversation (e.g., user signaled register change, conversation shifted contexts), the AI MAY:

1. Pick an appropriate tone from the registry (or note that none fits)
2. Write its description to `~/.claude/user-prompt-injectors/tone-current.txt` directly (same write as `set tone`)
3. Naturally announce the switch in the conversation, e.g.:
   > *"Switching to a more focused register for the implementation work."*

**Rules for AI auto-set**:
- Only switch to tones that exist in the registry — if the right tone doesn't exist, suggest adding it via `add tone` first
- Don't switch on every message — only on genuine context shifts
- Always announce the switch in user-facing text — silent switching is confusing

---

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| `## Tones` section missing | Inform user the injector may not be installed; suggest `"Load tone-prompt-inject"` |
| `tone-current.txt` missing on `set` | Create the file (parent directory should exist from framework install) |
| User passes name that's actually a description | Try fuzzy match against descriptions too; otherwise ask for clarification |
| Multiple table rows with same name | Take the first; warn user about the duplicate |

---

*Three commands, one registry, instant context.*
