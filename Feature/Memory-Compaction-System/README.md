# Memory Compaction System
*Intelligent memory compression that summarizes old entries instead of deleting them*

## What This Feature Does

Adds a **size-aware compaction layer** to your AI companion. When a memory file grows past a configurable budget, the AI **compresses the oldest, lowest-signal entries into a dense summary** — preserving facts, decisions, and preferences while reclaiming space.

- **Budget-aware** — each memory file has a line/character budget (e.g. 500 lines or 8000 chars)
- **Compress, don't delete** — old entries are summarized into a `## Compacted History` block, not thrown away
- **Signal-preserving** — verified facts, user preferences, and decisions survive; chatter and redundancy are dropped
- **Tiered retention** — recent entries stay verbatim, mid-age entries get light summarization, old entries get heavy compaction
- **Reversible by design** — a pre-compaction snapshot is written to `compaction/snapshots/` before any rewrite
- **Skill auto-install** if Skill Plugin System is detected

## How It Works

### The Concept

Most memory systems handle growth by **truncation** — when the file gets too big, they delete the oldest content. That loses knowledge permanently.

Memory Compaction takes a different path: when a file exceeds its budget, the AI **reads the oldest entries, distills them into a concise summary, and replaces the verbose originals with that summary**. The file stays small, but the knowledge survives.

Think of it like a journal you periodically rewrite — keeping the lessons, dropping the noise.

### Example: A Memory File Hits Its Budget

```text
You: "save this"
AI: "Memory file is at 512/500 lines. Compacting oldest entries before saving."
AI:
  1. Snapshots the current file to compaction/snapshots/main-memory-2026-06-06.md
  2. Reads the oldest 30% of entries
  3. Summarizes them into a dense "Compacted History" block (facts + decisions preserved)
  4. Replaces the verbose originals with the summary
  5. Appends the new save
  6. Confirms: "Compacted 47 lines into 9. File now 474/500 lines."
```

### How It Differs From Existing Features

| Aspect | Memory Consolidation | Session Memory Limit | Memory Compaction |
|--------|----------------------|----------------------|-------------------|
| **Purpose** | Merge split files into one | Cap session RAM size | Keep growing files within budget |
| **Method** | Structural merge | Hard reset, preserve recap | Summarize old entries, preserve knowledge |
| **On overflow** | N/A (one-time upgrade) | Delete detail, keep recap | Compress detail into summary |
| **Knowledge loss** | None (merge) | High (detail discarded) | Minimal (summarized, snapshotted) |
| **Runs** | Once (architecture upgrade) | Every session reset | Continuously, when budget exceeded |

> **Companion, not replacement.** Memory Consolidation unifies *which* files exist. Session Memory Limit caps *session RAM*. Memory Compaction keeps *long-lived files* (main memory, relationship memory, topic diaries) within budget without losing what they learned.

## Directory Structure

```text
compaction/
├── compaction-policy.md             # Active budgets and retention tiers
└── snapshots/                       # Pre-compaction backups (reversible)
    └── main-memory-2026-06-06.md
```

## Quick Integration

```text
"Load memory-compaction"
```

## What Happens During Integration

1. **Creates** `compaction/` and `compaction/snapshots/` directories
2. **Creates** `compaction/compaction-policy.md` using `policy-format.md`
3. **Adds** compaction triggers and budget-check behavior to `master-memory.md`
4. **Installs as skill** if Skill Plugin System is detected
5. **Touches no content yet** — first compaction only runs when a file actually exceeds budget

## Post-Integration Result

After running the integration protocol:

- Every long-lived memory file has a defined budget
- Before each `save`, the AI checks whether the target file is over budget
- When over budget, the AI snapshots, compacts the oldest tier, then saves
- A `## Compacted History` block preserves distilled knowledge from old entries
- You can always recover the pre-compaction state from `compaction/snapshots/`

## Safety Rules

1. **Snapshot before compaction** — never rewrite a file without a backup
2. **Never compact the newest tier** — recent context stays verbatim
3. **Preserve all facts, decisions, and preferences** — only redundancy and chatter are dropped
4. **Never compact secrets** — tokens, passwords, and credentials are excluded, never summarized into shared blocks
5. **Confirm before first compaction** of any file if the user has customized it
6. **Do not self-delete** this feature folder unless the user explicitly requests cleanup

---

*Compaction keeps memory small without making it forget.*
