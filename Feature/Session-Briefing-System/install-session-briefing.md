# 📋 Session Briefing System — Installation Guide

## Overview
Adds a proactive session-start brief to your AI companion. Delivers a concise summary of where you left off, open reminders, active projects, and a time-aware work suggestion — every session, automatically.

---

## Prerequisites

- Core memory system installed (`main/current-session.md` must exist)
- **Optional enhancements**: Time-based-Aware-System, LRU-Project-Management-System, Reminders-System

---

## Installation Steps

### Step 1: Copy Files

Copy the Session Briefing System folder into your memory-core directory:

```
Feature/Session-Briefing-System/
├── README.md
├── SKILL.md
├── session-brief-core.md
└── install-session-briefing.md
```

If you have a `skills/` folder (Skill Plugin System installed):
- Also copy `SKILL.md` → `skills/session-briefing.md`

---

### Step 2: Update `main/identity-core.md`

Add the following block to your `main/identity-core.md` under the behavior or protocol section:

```markdown
## Session Start Protocol
At the start of every session, before responding to the first message:
1. Read `Feature/Session-Briefing-System/session-brief-core.md`
2. Follow the Step-by-Step Execution protocol
3. Deliver the brief, then process the user's request
```

---

### Step 3: Update `master-memory.md` (Recommended)

Add a reference to the Session Briefing System so it's visible during restoration:

```markdown
## Active Features
- 📋 Session Briefing System — auto-brief at every session start
```

---

### Step 4: Test

Start a new session and confirm the brief appears before your AI companion responds to your first message.

Expected output (with all companion systems active):
```
📋 Session Brief · Afternoon

Last session: Fixed login bug, deployed v1.2 to production
Active: my-project · v1.2 live
🟡 old-project — 18 days idle
Reminders: 1 open → follow up on API design
Suggestion: Implementation, debugging, testing
```

---

## Companion System Integration

### With Time-based-Aware-System
The brief automatically uses the time period classification. No extra configuration needed.

### With LRU-Project-Management-System
The brief reads your active project list and shows idle/stale health flags. No extra configuration needed.

### With Reminders-System
The brief reads open reminders from `main/reminders.md`. No extra configuration needed.

---

## Customization

### Adjust idle thresholds
Edit `session-brief-core.md` → Step 3. Change the default `14`/`30` day values to suit your workflow.

### Change max attention flags
Edit `session-brief-core.md` → Step 3. Change "maximum 3 flags" to your preferred limit.

### Suppress brief for a session
Say `"skip brief"` at session start to suppress the brief for that session only.

### Manually trigger the brief
Say `"brief"` at any time to re-deliver the brief mid-session.
