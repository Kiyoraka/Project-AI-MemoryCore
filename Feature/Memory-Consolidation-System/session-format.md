# 📋 Session Memory - Sample Format
*Reference template for session RAM structure with 500-line limit*

---

```markdown
# Current Session Memory - [Date]
*Active working memory for current conversation*

## Session Context
**Session Type**: [Work/Personal/Mixed]
**Current Project**: [Active project name, if any]
**Status**: [Active/Paused/Wrapping up]
**Time**: [Session start time]

## Current Focus
- **Primary Task**: [What we're working on]
- **Technical Context**: [Relevant technical details]
- **Progress**: [Brief progress summary]

## Working Memory
### Active Context
- **Current Topic**: [What we're discussing]
- **Immediate Goals**: [Session objectives]
- **Recent Progress**: [What was just completed]
- **Next Steps**: [What comes next]

### Important Decisions
- [Key decision 1 made this session]
- [Key decision 2 made this session]

## Session Recap (For AI Restart)
*Quick summary when AI loads after close/reopen*
- **Previous Session Summary**: [Key points from last conversation]
- **Where We Left Off**: [Context for continuing]
- **Important Context**: [Critical info for continuity]
- **User's Current State**: [Situation, mood, needs]

## Session Achievements
- [Achievement 1]
- [Achievement 2]

## Quick Context for Next Session
- **Where We Left Off**: [Last activity]
- **What's Working**: [Current state of things]
- **What Needs Attention**: [Pending items]

---
*Session updated: [Date, Time]*
```

---

## 500-Line Limit Protocol

### Rule
Session memory must not exceed **500 lines**. This prevents context window overflow and keeps session memory lightweight.

### When Limit is Reached
The AI performs a **RAM-style reset**:

1. **Preserve** the `## Session Recap` section (last 20-30 lines of key context)
2. **Clear** all detailed working memory, achievements, and decisions
3. **Rebuild** the session file following this format template
4. **Continue** seamlessly - the recap provides enough context for continuity

### What Gets Preserved (Recap Only)
- Brief summary of session so far
- Where conversation left off
- Critical context for continuity
- User's current state and needs

### What Gets Cleared
- Detailed conversation progress
- Individual achievement entries
- Working memory details
- Session-specific decisions (summarized into recap)

### Auto-Reset Behavior
```
IF current-session.md line count > 500:
    1. Read current Session Recap section
    2. Summarize key achievements into recap
    3. Clear file and rebuild from session-format.md template
    4. Write preserved recap into new structure
    5. Continue session with clean working memory
```

## Usage Notes
- This is a **sample format only** - customize sections to match your needs
- The AI uses this as a reference when resetting or rebuilding session memory
- The 500-line limit ensures session memory stays within AI context limits
- Recap preservation ensures no critical context is lost during reset

*Session Format Template v1.0*
