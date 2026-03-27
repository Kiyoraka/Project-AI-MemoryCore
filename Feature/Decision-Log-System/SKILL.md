---
name: log-decision
description: "Auto-triggers when a non-obvious decision is made during conversation.
             Also triggers on 'log decision', 'why did we choose', 'what was the
             trade-off', 'should we use A or B' (after resolution), or when user
             asks about past reasoning behind a choice."
---

# Log Decision -- Append-Only Decision Tracking Skill
*Every important "why" captured, every trade-off remembered.*

## Activation

When this skill activates, silently read `main/decisions.md`.

- If user is logging a decision: capture and confirm
- If user is searching past decisions: find and present
- If a decision-worthy moment is detected: offer to log it

## Context Guard

| Context | Status |
|---------|--------|
| **User says "log decision"** | ACTIVE -- capture decision |
| **User says "why did we choose [X]?"** | ACTIVE -- search decision log |
| **Non-obvious decision made in conversation** | ACTIVE -- offer to log |
| **User says "should we use A or B?" (after resolved)** | ACTIVE -- log the choice |
| **Session end with unlogged decisions** | ACTIVE -- prompt to log |
| **Mid-conversation (no decision context)** | DORMANT |

## Protocol

### On Decision Detection
- [ ] Identify the decision: what was chosen and what was rejected
- [ ] Determine if it's non-obvious (skip trivial/obvious choices)
- [ ] If non-obvious: offer to log it or log automatically if user said "log decision"

### On Logging a Decision
- [ ] Get current date (YYYY-MM-DD)
- [ ] Write a short descriptive title
- [ ] Compose entry in format:
  ```markdown
  ## YYYY-MM-DD -- Short title
  **Context**: What situation prompted this decision
  **Decision**: What was chosen (and what was rejected)
  **Rationale**: Why -- trade-offs, constraints, evidence
  ```
- [ ] APPEND to `main/decisions.md` (after the last entry)
- [ ] Confirm: "Logged decision: [title]"

### On Searching Decisions
- [ ] Read `main/decisions.md`
- [ ] Search for keywords matching the user's query
- [ ] Present matching decision(s) with full context
- [ ] If no match: inform user and offer to log a new entry

### On Reversing a Decision
- [ ] DO NOT edit the original entry
- [ ] APPEND a new entry referencing the original:
  ```markdown
  ## YYYY-MM-DD -- Reversed: [original title]
  **Context**: Why the original decision is being reconsidered
  **Decision**: New choice, referencing the old one
  **Rationale**: What changed -- new information, constraints, or priorities
  ```

## Mandatory Rules
1. **Append-only** -- NEVER edit or delete past entries
2. **Context + Decision + Rationale** -- all three fields required for every entry
3. **Include rejected alternatives** -- document what was NOT chosen and why
4. **Non-obvious only** -- skip trivial choices (using git, formatting preferences)
5. **Natural detection** -- detect decision-worthy moments without requiring explicit commands

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| No decisions.md file | Create it with template from install protocol |
| No matching decision found | Inform user, offer to log a new entry |
| Vague decision ("we went with the better one") | Ask user to clarify alternatives and reasoning |
| Multiple related decisions | Log each as a separate entry with cross-references |
| Reversal of past decision | Append new entry with "Reversed:" prefix, never edit original |

## Level History
- **Lv.1** -- Base: decision detection, append-only logging, Context+Decision+Rationale format, search, reversal tracking.
