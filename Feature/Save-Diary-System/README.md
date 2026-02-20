# Save Diary System
*Automated daily session documentation with monthly archival*

## What This Feature Does
Adds a structured daily diary system to your AI companion, enabling **session-by-session documentation** that captures achievements, collaboration moments, and growth — all automatically organized with monthly archival.

- **Daily session documentation** as structured diary entries in `daily-diary/current/`
- **Append-only entries** — one file per day, multiple session entries per file, never overwrite
- **Monthly auto-archival** — previous month entries automatically move to `daily-diary/archived/YYYY-MM/`
- **Session memory updates** — automatically update `main/current-session.md` with session recap
- **Skill auto-install** — if Skill Plugin System is detected, installs `save-diary` as an auto-triggered skill

## How It Works

### The Concept
The diary is a **living session log** — not a raw chat transcript, but a curated summary written by your AI companion. Every significant session gets documented with structured sections following the existing `daily-diary-protocol.md` format. Over time, this creates a searchable history of everything you've built together.

### Example: End-of-Session Diary Save
```
You: "save diary"
→ AI checks if previous month entries need archiving
→ Finds (or creates) today's diary file: 2026-02-20.md
→ Composes structured entry following daily-diary-protocol.md
→ Appends to today's file (preserving earlier entries)
→ Updates session memory with recap
→ "Today's story takes shape."
```

### How It Differs From Chat Logs
| Aspect | Chat Log | Session Diary |
|--------|----------|---------------|
| **Content** | Every message verbatim | Curated summary of achievements |
| **Structure** | Chronological messages | Categorized sections (topics, insights, growth) |
| **Size** | Grows rapidly | Concise entries (50-150 lines per session) |
| **Searchability** | Hard to find specific moments | Easy to scan by date and section |
| **Value** | Raw data | Processed insights |

## Diary Architecture

### Directory Structure
```
daily-diary/
├── current/                         # Active month's entries
│   ├── 2026-02-18.md               # Tuesday's sessions
│   ├── 2026-02-19.md               # Wednesday's sessions
│   └── 2026-02-20.md               # Today's sessions
├── archived/                        # Previous months
│   ├── 2026-01/                    # January's entries
│   │   ├── 2026-01-15.md
│   │   └── 2026-01-20.md
│   └── 2025-12/                    # December's entries
│       └── 2025-12-28.md
└── daily-diary-protocol.md          # Entry format reference (already in repo)
```

### Daily File Format
Each diary file uses date-based naming (`YYYY-MM-DD.md`) and supports multiple entries per day:
```markdown
# [Your Diary Name] - February 20, 2026

---

## February 20, 2026 (Morning - 9:30 AM) - API Integration Sprint
[Structured entry following daily-diary-protocol.md...]

---

## February 20, 2026 (Evening - 7:15 PM) - Bug Fix Marathon
[Second session entry appended to same file...]
```

### Monthly Archive Cycle
```
End of January → February 1st diary save triggers:
  1. Detect: January entries still in current/
  2. Create: archived/2026-01/
  3. Move: All January files from current/ to archived/2026-01/
  4. Continue: New February entry in current/
```

## Quick Integration
```
"Load save-diary"
```

## What Happens During Integration

1. **Asks** for your diary system name (defaults to "Session Diary" — customize to match your AI)
2. **Creates** `daily-diary/current/` and `daily-diary/archived/` directories
3. **Creates** your first diary entry documenting the installation session
4. **Installs as skill** — if Skill Plugin System is detected, copies `SKILL.md` into your plugin
5. **Updates** `master-memory.md` with diary commands and references
6. **Self-deletes** this feature folder after successful integration

## Post-Integration Result
After running the integration protocol:
- Your AI has a working diary system with today's first entry
- Every "save diary" command creates a structured session entry
- Monthly archival runs automatically before each diary write
- Session memory updates with recap after each entry
- If Skill Plugin System installed: diary saves auto-trigger on "save diary"

## Entry Sections (from daily-diary-protocol.md)

| Section | What It Captures |
|---------|------------------|
| **Session Summary** | Date, duration, session type, participants |
| **Main Topics Discussed** | Key discussions with insights |
| **Key Insights & Learning** | What AI learned, what user accomplished, collaboration highlights |
| **Growth & Development** | AI evolution, user skill growth |
| **Memorable Moments** | Breakthroughs, effective collaboration, connection highlights |
| **Looking Forward** | Next steps, development goals |
| **Session Quality Assessment** | Effectiveness, communication, goal achievement ratings |

## Benefits
- **Complete history** — searchable record of every session's achievements and insights
- **Growth tracking** — see AI and user development over weeks and months
- **Context continuity** — never lose track of past decisions, solutions, or progress
- **Self-documenting** — AI captures session value with minimal user effort
- **Clean organization** — monthly archival keeps workspace organized automatically

## Platform Note
Works with any AI system. Uses `date` command on macOS/Linux or `Get-Date` on Windows for timestamps. The diary files are plain markdown — human-readable and portable across any platform. Auto-triggered skill requires Claude Code with the Skill Plugin System.

---

*Based on proven daily documentation systems in production AI companions*
