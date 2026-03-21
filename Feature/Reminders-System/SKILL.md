---
name: check-reminders
description: "Auto-triggers at session start to review open reminders. Also triggers
             on 'remind me', 'check reminders', 'don't forget', 'follow up on',
             'next session we should', or when user mentions a deadline."
---

# Check Reminders -- Persistent Follow-Up Skill
*Nothing gets lost between sessions.*

## Activation

When this skill activates, silently read `main/reminders.md`.

- If urgent/overdue items exist: mention them naturally
- If no urgent items at session start: stay silent (don't announce "no reminders")
- If user is adding a reminder: confirm after saving

## Context Guard

| Context | Status |
|---------|--------|
| **Session start** | ACTIVE -- read and flag urgent items |
| **User says "remind me [X]"** | ACTIVE -- add reminder |
| **User says "check reminders"** | ACTIVE -- list all open reminders |
| **Task completed that matches a reminder** | ACTIVE -- move to Completed |
| **Session end** | ACTIVE -- review and update |
| **Mid-conversation (no reminder context)** | DORMANT |

## Protocol

### On Session Start
- [ ] Read `main/reminders.md`
- [ ] Parse Open section for all active reminders
- [ ] Check for deadlines: flag items due within 3 days or overdue
- [ ] If urgent items exist: weave into greeting naturally
- [ ] If no urgent items: do nothing (no announcement needed)

### On "Remind Me" / Adding
- [ ] Parse what the user wants to remember
- [ ] Compose reminder: `- **Title**: Description`
- [ ] If deadline mentioned: convert to absolute date, format as `- **Title** (by YYYY-MM-DD): Description`
- [ ] APPEND to `## Open` section in `main/reminders.md`
- [ ] Confirm: "Added reminder: [title]"

### On Task Completion
- [ ] When a task is completed that matches an Open reminder
- [ ] Remove the item from `## Open`
- [ ] Add to `## Completed` with date: `- **Title** (completed YYYY-MM-DD): Outcome`
- [ ] Confirm: "Marked complete: [title]"

### On Session End
- [ ] Re-read `main/reminders.md`
- [ ] Review each Open item against session work
- [ ] Move any resolved items to Completed with date
- [ ] Add any new follow-ups discovered during the session
- [ ] Save the updated file

## Mandatory Rules
1. **Never delete reminders** -- always move to Completed section
2. **Absolute dates only** -- convert "tomorrow", "next week", "Friday" to YYYY-MM-DD
3. **Append-only for Open** -- never rewrite the Open section, only append or move
4. **Silent when empty** -- don't announce "you have no reminders" at session start
5. **Natural integration** -- weave reminders into conversation, don't list them robotically

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| No reminders.md file | Create it with template from install protocol |
| No open reminders | Stay silent at session start |
| Multiple urgent items | Mention the most time-sensitive first |
| Vague deadline ("soon") | Ask user to clarify, or save without deadline |
| Duplicate reminder | Check existing Open items before adding; skip if duplicate |

## Level History
- **Lv.1** -- Base: session start/end lifecycle, natural language detection, deadline tracking, append-only Open section, move-to-Completed pattern.
