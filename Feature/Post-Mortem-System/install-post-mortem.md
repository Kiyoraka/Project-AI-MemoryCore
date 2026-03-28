# 🔥 Post-Mortem System — Installation Guide

## Overview
Adds a failure learning log to your AI companion. The AI auto-detects failure signals, asks whether to log them, and references past lessons when you work in the same domain again.

---

## Prerequisites

- Core memory system installed (`main/` folder must exist)
- No other systems required — fully standalone

---

## Installation Steps

### Step 1: Copy Files

Copy the Post-Mortem System folder into your memory-core directory:

```
Feature/Post-Mortem-System/
├── README.md
├── SKILL.md
├── post-mortem-core.md
└── install-post-mortem.md
```

If you have a `skills/` folder (Skill Plugin System installed):
- Also copy `SKILL.md` → `skills/post-mortem.md`

---

### Step 2: Create the Log File

Create `main/post-mortems.md` with this starter content:

```markdown
# 🔥 Post-Mortems — Failure Learning Log
*What went wrong, why, and what we'll do differently. No blame, only growth.*

---

## Log

*(No entries yet)*
```

---

### Step 3: Update `main/identity-core.md`

Add the following block to your `main/identity-core.md` under the behavior or protocol section:

```markdown
## Post-Mortem Protocol
When a failure signal is detected (deployment failure, broken tests, wasted time, architecture reversal, security incident, data loss):
1. Ask: "That didn't go as planned. Worth a post-mortem?"
2. If yes: follow `Feature/Post-Mortem-System/post-mortem-core.md`
3. Append entry to `main/post-mortems.md`
4. When starting work in a domain, check `main/post-mortems.md` for relevant lessons
```

---

### Step 4: Update `master-memory.md` (Recommended)

Add a reference so it's visible during restoration:

```markdown
## Active Features
- 🔥 Post-Mortem System — failure learning log, auto-detected
```

---

### Step 5: Test

Simulate a failure scenario (e.g., "my deployment just failed") and verify your AI companion asks whether to log a post-mortem.

---

## Companion System Integration

### With Session Briefing System
The Session Briefing System can flag recent post-mortems at session start when you're working in a relevant domain. No extra configuration needed.

### With Decision-Log-System
Post-mortems and decisions complement each other:
- **Decision Log**: records *what you chose* and *why*
- **Post-Mortem Log**: records *what went wrong* and *what to do differently*

Both are append-only logs — consider linking related entries by date.

### With Save-Diary-System
Significant post-mortems (Major severity) are good candidates for diary entries. Log the post-mortem first, then save a diary entry referencing it.

---

## Customization

### Add more auto-detection signals
Edit `SKILL.md` → Auto-Detection Triggers table. Add phrase examples relevant to your workflow.

### Change the log file location
Default: `main/post-mortems.md`. To change, update the storage path in `post-mortem-core.md` and `identity-core.md`.

### Disable auto-detection
Remove the auto-detection block from `identity-core.md`. The manual trigger (`"post-mortem"`) will still work.
