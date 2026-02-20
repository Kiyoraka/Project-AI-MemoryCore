# Save Diary Skill
*Ready-made auto-triggered skill for session documentation*

## What This Skill Does
An auto-triggered skill that documents your AI sessions as structured daily diary entries. When you say "save diary", your AI automatically archives old entries, finds or creates today's file, composes a structured session summary, and updates session memory.

- **Auto-triggered** on "save diary", "write diary", "diary entry", "document session"
- **Monthly auto-archival** — previous month entries move to `daily-diary/archived/YYYY-MM/`
- **Append-only** — one file per day, multiple entries per file, never overwrite
- **Session memory update** — keeps `main/current-session.md` current after each entry

## How to Install

**Requires**: [Skill Plugin System](../Skill-Plugin-System/) installed first.

1. Copy the `SKILL.md` file to your plugin's skills directory:
   ```
   plugins/[your-plugin]/skills/save-diary/SKILL.md
   ```
2. The skill auto-activates — no configuration needed
3. Say "save diary" to test it

## How It Works

```
You: "save diary"
→ Skill activates: "Today's story takes shape."
→ Archives old month entries (if any)
→ Finds or creates today's file (YYYY-MM-DD.md)
→ Composes structured entry following daily-diary-protocol.md
→ Appends to today's file
→ Updates session memory
→ Done!
```

## Directory Structure Created

```
daily-diary/
├── current/                    # Active month entries
│   └── YYYY-MM-DD.md          # Today's diary
├── archived/                   # Previous months
│   └── YYYY-MM/               # Monthly archive folders
└── daily-diary-protocol.md    # Entry format reference (already in repo)
```

## Entry Sections

The skill follows the existing `daily-diary-protocol.md` format:

| Section | What It Captures |
|---------|------------------|
| **Session Summary** | Date, duration, session type |
| **Main Topics** | Key discussions and decisions |
| **Insights & Learning** | What AI learned, what user accomplished |
| **Collaboration Highlights** | Teamwork moments |
| **Growth & Development** | AI and user evolution |
| **Memorable Moments** | Breakthroughs and highlights |
| **Looking Forward** | Next steps and goals |

## Platform Note
Requires **Claude Code** with the Skill Plugin System for auto-triggering. On other platforms, use the protocol in `SKILL.md` as a manual reference.

---

*Based on proven daily documentation systems in production AI companions*
