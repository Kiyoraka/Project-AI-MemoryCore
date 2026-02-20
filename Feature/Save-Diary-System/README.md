# Save Diary System
*Automated daily session documentation with monthly archival*

## What This Feature Does
Adds a structured daily diary system to your AI companion, enabling **session-by-session documentation** that captures achievements, collaboration moments, and growth — all automatically organized with monthly archival.

- **Daily session documentation** as structured diary entries in `daily-diary/current/`
- **Append-only entries** — one file per day, multiple session entries per file, never overwrite
- **Monthly auto-archival** — previous month entries automatically move to `daily-diary/archived/YYYY-MM/`
- **Session memory updates** — automatically update `main/current-session.md` with session recap
- **Dual format support** — works with flat files (`YYYY-MM-DD.md`) and folder format (`YYYY-MM-DD/`)

## How It Works

### The Concept
The diary is a **living session log** — not a raw chat transcript, but a curated summary written by your AI companion. Every significant session gets documented with structured sections covering achievements, collaboration quality, and emotional reflection. Over time, this creates a searchable history of everything you've built together.

### Example: End-of-Session Diary Save
```
You: "save diary"
→ AI checks if previous month entries need archiving
→ Finds (or creates) today's diary file: 2026-02-20.md
→ Composes structured entry with session achievements
→ Appends to today's file (preserving earlier entries)
→ Updates session memory with recap
→ "Diary entry saved for February 20, 2026!"
```

### How It Differs From Chat Logs
| Aspect | Chat Log | Session Diary |
|--------|----------|---------------|
| **Content** | Every message verbatim | Curated summary of achievements |
| **Structure** | Chronological messages | Categorized sections (technical, collaboration, impact) |
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
│   │   ├── 2026-01-16.md
│   │   └── 2026-01-20.md
│   └── 2025-12/                    # December's entries
│       └── 2025-12-28.md
├── diary-entry-format.md            # Permanent format reference
└── diary-auto-archive-protocol.md   # Monthly archival logic
```

### Daily File Format
Each diary file uses date-based naming (`YYYY-MM-DD.md`) and supports multiple entries per day:
```markdown
# [Your Diary Name] - February 20, 2026

---

## February 20, 2026 (Morning - 9:30 AM) - API Integration Sprint
[Structured entry with achievements, collaboration, impact...]

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
3. **Installs** diary entry format template and auto-archive protocol
4. **Creates** your first diary entry documenting the installation
5. **Installs as skill** — if Skill Plugin System is detected, installs `save-diary` as an auto-triggered skill
6. **Updates** `master-memory.md` with diary commands and references
7. **Self-deletes** this feature folder after successful integration

## Post-Integration Result
After running the integration protocol:
- Your AI has a working diary system with today's first entry
- Every "save diary" command creates a structured session entry
- Monthly archival runs automatically before each diary write
- Session memory updates with recap after each entry
- Format template is permanently available for reference

## Entry Sections Explained

| Section | When to Include | What It Captures |
|---------|----------------|------------------|
| **Technical Achievements** | Always | Work accomplished, problems solved, features built |
| **Collaboration Moments** | Always | AI-user partnership highlights, effective teamwork |
| **System Impact** | Work sessions | Business value, measurable outcomes, quality results |
| **Innovation Notes** | Discovery sessions | Growth, learning, creative breakthroughs |
| **Emotional Reflection** | Meaningful sessions | How the session felt, what stood out personally |

Not every session needs all sections — use the ones that fit. Technical Achievements and Collaboration Moments are the minimum.

## Benefits
- **Complete history** — searchable record of every session's achievements and insights
- **Growth tracking** — see AI and user development over weeks and months
- **Context continuity** — never lose track of past decisions, solutions, or progress
- **Self-documenting** — AI captures session value with minimal user effort
- **Clean organization** — monthly archival keeps workspace organized automatically

## Platform Note
Works with any AI system. Uses `date` command on macOS/Linux or `Get-Date` on Windows for timestamps. The diary files are plain markdown — human-readable and portable across any platform.

---

*Based on proven daily documentation systems in production AI companions*
