# 📋 Session Briefing — Skill Plugin

## Skill Name
Session Briefing

## Trigger Words
- Session start (automatic — fires before first response)
- `"brief"`
- `"session brief"`
- `"what did we do last time"`
- `"where did we leave off"`

## Suppress Trigger
- `"skip brief"` — suppresses for this session only

## Activation Condition
Fires automatically at the start of every new conversation session, before processing the user's first message.

## Behavior
1. Read `main/current-session.md` — extract last session recap (1–2 lines)
2. Read `main/reminders.md` — count open items (skip section if none)
3. Read project list — identify active project + 🔴/🟡 health flags (if LRU System installed)
4. Check current time — determine time period (if Time-based-Aware System installed)
5. Compose and deliver brief (max 12 lines) before responding to user

## Output Rules
- Maximum 12 lines total
- Maximum 3 attention flags — show most critical first
- Skip any section that has nothing to report
- Deliver before processing the user's first request

## Companion Skills
- Time-based-Aware-System → time period + work suggestion
- LRU-Project-Management-System → active project + health flags
- Reminders-System → open reminder items

## Level History
- **Lv.1** — Base: session recap + time suggestion
- **Lv.2** — Reminders integration (requires Reminders-System)
- **Lv.3** — Project health flags (requires LRU-Project-Management-System)
