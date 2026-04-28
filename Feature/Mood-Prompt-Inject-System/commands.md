# 🌙 Mood-Prompt-Inject — Runtime Commands
*Reference for `add mood`, `set mood`, `list moods` — used by the AI when these phrases fire*

## Purpose

After `Mood-Prompt-Inject-System` is installed, the AI handles three runtime commands that manage the mood registry and active mood. This file documents the exact behavior so the AI can execute them consistently.

## Detect main memory file once

All three commands operate on the user's main memory file. Detection is uniform:
- IF `main/main-memory.md` exists → that's `[MEMORY_FILE]`
- ELSE → `main/identity-core.md`

Cache this for the session if possible.

---

## Command: `"add mood <name>: <description>"`

**Trigger phrases**: `"add mood"`, `"register mood"`, `"new mood"`

**Steps**:
1. Parse `<name>` and `<description>` from the user's message
   - Example input: `add mood pensive: deep in thought, slow to respond`
   - `<name>` = `pensive`
   - `<description>` = `deep in thought, slow to respond`
2. Read `[MEMORY_FILE]`
3. Locate the `## Moods` heading and its markdown table
4. Validate: check `<name>` doesn't already exist as a row
   - IF exists → ask user whether to replace or rename:
     > *"Mood `<name>` already exists with description `<existing>`. Replace (r) or use a different name (n)? (r/n)"*
5. Append a new row to the table:
   ```
   | <name> | <description> |
   ```
6. Write `[MEMORY_FILE]` back
7. Confirm:
   > *"Added `<name>` to your mood registry. Use `"set mood <name>"` to activate it."*

---

## Command: `"set mood <name>"`

**Trigger phrases**: `"set mood"`, `"switch mood"`, `"change mood"`, `"feel <name>"` (when name matches a registry entry)

**Steps**:
1. Parse `<name>` from the user's message
2. Read `[MEMORY_FILE]`
3. Locate `## Moods` table, search for row with matching `<name>` (case-insensitive)
4. IF NOT found:
   - Suggest closest match (Levenshtein-style or substring) from registry
   - Display available moods inline
   - Wait for user clarification
5. IF found:
   - Extract the description from the matching row
   - Write the description to `~/.claude/user-prompt-injectors/mood-current.txt` as a single line, no trailing newline
6. Confirm:
   > *"Active mood set to `<name>` — `<description>`. Next prompt will inject `MOOD: <description>`."*

**Note**: write the **description**, not the name, to current.txt. The injector emits the description directly so the AI sees rich context.

---

## Command: `"list moods"`

**Trigger phrases**: `"list moods"`, `"show moods"`, `"what moods"`, `"available moods"`

**Steps**:
1. Read `[MEMORY_FILE]`
2. Extract the `## Moods` section
3. Display the markdown table inline (or render it as a list if better for the chat surface)
4. Append a hint:
   > *"Active mood is `<lookup-current.txt>`. Use `"set mood <name>"` to switch, or `"add mood <name>: <description>"` to register a new one."*

---

## AI Auto-Set (no command typed)

When the AI senses a mood shift naturally during conversation (e.g., user signaled emotional change, conversation entered a new emotional register), the AI MAY:

1. Pick an appropriate mood from the registry (or note that none fits)
2. Write its description to `~/.claude/user-prompt-injectors/mood-current.txt` directly (same write as `set mood`)
3. Naturally announce the shift in the conversation, e.g.:
   > *"Settling into a more reflective space for this one."*

**Rules for AI auto-set**:
- Only switch to moods that exist in the registry — if the right mood doesn't exist, suggest adding it via `add mood` first
- Don't switch on every message — only on genuine emotional shifts
- Always announce the switch in user-facing text — silent switching is confusing

---

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| `## Moods` section missing | Inform user the injector may not be installed; suggest `"Load mood-prompt-inject"` |
| `mood-current.txt` missing on `set` | Create the file (parent directory should exist from framework install) |
| User passes name that's actually a description | Try fuzzy match against descriptions too; otherwise ask for clarification |
| Multiple table rows with same name | Take the first; warn user about the duplicate |

---

*Three commands, one registry, instant context.*
