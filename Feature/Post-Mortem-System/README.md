# 🔥 Post-Mortem System

A failure learning log that helps your AI companion detect, record, and reference mistakes — so the same problem never costs you twice.

> *"The forge that never breaks never learns to mend."*

---

## What It Does

When something goes wrong — a failed deployment, a broken test suite, wasted hours on a dead end — the Post-Mortem System:

1. **Auto-detects** failure signals in the conversation
2. **Asks** whether it's worth logging (you always decide)
3. **Records** what happened, why, and how to prevent it
4. **References** past post-mortems when you start work in the same domain

---

## Format

Every post-mortem entry follows this structure:

```
## YYYY-MM-DD — Short title of what went wrong
**Severity**: Minor | Moderate | Major
**What happened**: Factual description of the failure
**Why**: Root cause analysis
**Impact**: What was lost — time, data, momentum
**Lesson**: The reusable insight for future work
**Prevention**: Specific action to prevent recurrence
```

---

## Rules

- **No blame** — this is a learning tool, not punishment
- **Append-only** — never rewrite or delete entries
- **Honest** — if it was a mistake, say so plainly
- **Actionable** — every entry must have a Prevention action

---

## Auto-Detection Triggers

The AI watches for these signals and asks: *"That didn't go as planned. Worth a post-mortem?"*

| Signal | Example |
|--------|---------|
| Deployment fails | Crash loops, image pull errors, config mistakes |
| Tests break unexpectedly | Suite was green, now it's not |
| Architecture decision reversed | "We chose X but now we need to undo it" |
| Time wasted on dead end | Hours spent on an approach that didn't work |
| Security incident | Exposed secret, vulnerability in production |
| Data loss | Backup failure, migration destroyed data |

You always decide whether to log it. The AI only asks.

---

## Companion Systems

| System | Integration |
|--------|-------------|
| **Session Briefing System** | Flags recent post-mortems when starting work in the same domain |
| **Decision-Log-System** | Post-mortems complement decisions — one records why, the other records what went wrong |
| **Save-Diary-System** | Post-mortem entries can be referenced in diary entries |

---

## Installation

See `install-post-mortem.md` for setup instructions.
