# 📋 Session Briefing System

A proactive session-start intelligence layer that delivers a concise brief at the beginning of every conversation — covering where you left off, open reminders, active project status, and a time-aware work suggestion.

---

## What It Does

At every session start, the Session Briefing System automatically delivers a structured brief (under 12 lines) before processing the user's first request:

- **Where we left off** — last session recap from `current-session.md`
- **Open reminders** — items from Reminders System (only if items exist)
- **Active project** — LRU #1 status from Project Management System
- **Attention flags** — idle or stale projects worth noting (max 3)
- **Time-adaptive suggestion** — work type recommendation based on time of day

---

## Output Format

```
📋 Session Brief · [Time Period]

Last session: [1-line recap]
Active: [project name] · [status]
🔴/🟡 [project] — [N] days idle    ← max 3 flags, skip if none
Reminders: [N] open → [preview]    ← skip if none
Suggestion: [time-appropriate work type]
```

---

## Companion Systems

Works best alongside these existing systems, but each is optional:

| System | Enhancement |
|--------|-------------|
| **Time-based-Aware-System** | Powers the time-adaptive work suggestion |
| **LRU-Project-Management-System** | Provides active project + idle/stale health flags |
| **Reminders-System** | Surfaces open reminders in the brief |

Can be used standalone with just `main/current-session.md`.

---

## Commands

| Input | Action |
|-------|--------|
| Session start | Brief auto-delivers (no command needed) |
| `"brief"` | Manually trigger the brief at any time |
| `"skip brief"` | Suppress the brief for this session only |

---

## Requirements

- `main/current-session.md` — required (last session recap source)
- `main/reminders.md` — optional (Reminders System)
- Project list file — optional (LRU Project Management System)
- Time detection — optional (Time-based-Aware System)

---

## Installation

See `install-session-briefing.md` for step-by-step setup.
