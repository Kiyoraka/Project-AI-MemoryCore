# Plan File - Sample Format
*Reference template for project plan execution files*

## Standard Plan File

```markdown
# Project Plan - [Project Name]
Created: [YYYY-MM-DD]
Source: [plan filename or "manual"]

## Instructions
- Auto-commit code after each completed todo item (chains with Auto-Commit if installed)
- Update this file every 5 completed items (checkpoint save)
- Do not commit this plan file — it is your AI's working reference

## Architecture
[Optional: diagrams, wireframes, ASCII art, mermaid diagrams from the original plan]
[Preserve all visual elements from the source plan — they help with context recovery]

## Implementation Plan

### Phase 1: [Phase Name]
- [ ] Task 1 description
- [ ] Task 2 description
- [ ] Task 3 description

### Phase 2: [Phase Name]
- [ ] Task 4 description
- [ ] Task 5 description
- [ ] Task 6 description

### Phase 3: [Phase Name]
- [ ] Task 7 description
- [ ] Task 8 description

## Progress Log

[Date] - [Summary of items completed this session]
[Date] - [Summary of items completed this session]
```

---

## Format Notes

### Checkbox Convention

| Symbol | Meaning |
|--------|---------|
| `- [ ]` | Pending — not yet started |
| `- [x]` | Completed — done and committed |
| `- [~]` | Blocked — flagged, skip for now |

### Phase Organization
- Group related tasks under named phases
- Phases can be feature areas, time periods, or implementation layers
- Tasks within a phase should be ordered by dependency
- Keep phase names descriptive (e.g., "Phase 1: Database Schema" not "Phase 1")

### Line Limit Rule
- Maximum **1,000 lines** per plan file (configurable during installation)
- When a plan file exceeds the limit during an append:
  1. Rename the current file to `project-plan-YYYYMMDD.md` (archived)
  2. Create a fresh `project-plan.md` with the new content
  3. Report: "Previous plan archived, new plan created"

### Resume Convention
After a context reset or auto-compact, the plan file is the recovery mechanism:
1. **Count `[x]` items** — know what is already done
2. **Find first `[ ]` item** — know where to resume
3. **Read Architecture section** — restore technical context
4. **Check Progress Log** — understand recent session activity

The AI reads the file and picks up exactly where it left off — no user explanation needed.

### Progress Log Format
Append a one-line summary after each work session:
```markdown
## Progress Log

2026-02-15 - Completed Phase 1 (3 items): database schema, migrations, seeders
2026-02-16 - Completed 2 items in Phase 2: API endpoints for users and auth
2026-02-17 - Resumed after reset, completed Phase 2 (remaining 3 items)
```

### What to Include
- All tasks as checkboxes (one per line)
- Architecture diagrams (ASCII, mermaid) from the original plan
- Phase groupings with descriptive names
- Progress log entries after each session
- Any notes about blocked items or dependencies

### What NOT to Include
- Emoji (plan files are parsed programmatically — emoji can interfere)
- Large code blocks (put those in actual code files, not the plan)
- Raw chat transcripts or conversation history
- Completed plan files from previous projects (archive those separately)

---

*Plan Format Template v1.0*
