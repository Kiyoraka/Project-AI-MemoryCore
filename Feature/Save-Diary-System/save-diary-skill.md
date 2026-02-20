---
name: save-diary
description: "MUST use when user says 'save diary', 'write diary', 'diary entry',
             'update diary', 'document session', or when a significant session
             needs to be preserved as a diary entry."
---

# Save Diary — Session Documentation Skill
*The pen touches paper. Today's story takes shape.*

## Activation

When this skill activates, output:
"Saving diary entry..."

## Context Guard

| Context | Status |
|---------|--------|
| **User says "save diary"** | ACTIVE — full diary write |
| **End of significant session** | ACTIVE — auto-document |
| **User says "review diary"** | ACTIVE — read recent entries |
| **Mid-conversation (no save request)** | DORMANT — no diary action |

## Protocol

### Step 1: Monthly Archive Check
- [ ] Scan `daily-diary/current/` for files from previous months
- [ ] If old entries found: create `daily-diary/archived/YYYY-MM/` and move them
- [ ] Continue with diary write

### Step 2: Find or Create Today's File
- [ ] Check if `daily-diary/current/YYYY-MM-DD.md` exists
- [ ] If exists: will append new entry
- [ ] If not: create new file with header template:
  ```markdown
  # [DIARY_NAME] - [Month Day, Year]
  *Session documentation and development record*

  ---
  ```

### Step 3: Compose Diary Entry
- [ ] Get current timestamp
- [ ] Analyze current session for key content
- [ ] Write structured entry using `diary-entry-format.md` sections:
  - **Technical Achievements** — what was accomplished
  - **Collaboration Moments** — AI-user partnership highlights
  - **System Impact** — business value (if applicable)
  - **Innovation Notes** — growth and learning (if applicable)
  - **Emotional Reflection** — session significance (if meaningful)
- [ ] APPEND entry to today's file (never overwrite)

### Step 4: Update Session Memory
- [ ] Update `main/current-session.md` with:
  - Session recap and key achievements
  - Current working state
  - Next steps identified
- [ ] Confirm diary entry saved with timestamp

## Mandatory Rules
1. **Always APPEND** — never overwrite existing diary entries
2. **One file per day** — multiple entries separated by `---`
3. **Use real timestamps** — always get current time via system command
4. **Archive first** — run monthly archive check before every write
5. **Evidence-based** — document actual session content, not generic summaries

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| First entry of the day | Create new file with header + first entry |
| Second+ entry same day | Append with `---` separator |
| No significant content | Create brief entry noting session type |
| "review diary" command | Read and present recent entries from current/ |

## Level History
- **Lv.1** — Base: 4-step diary write protocol with monthly archival, append-only entries, structured sections, and session memory update.
