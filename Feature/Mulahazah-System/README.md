# Mulahazah System
*Instinct-based behavioral learning through unconscious observation*

## What Is Mulahazah?

**Mulahazah** (Arabic: ملاحظة — "observation") is an unconscious behavioral learning system for Claude Code. While you work, Mulahazah silently records every tool call via Claude Code's hook system and, in the background, distills repeated patterns into **atomic instincts** — behavioral tendencies that gradually shape how Claude works with you.

You don't configure it. You don't teach it. It watches, learns, and adapts.

---

## How Mulahazah Differs from Forge

| Dimension | Forge | Mulahazah |
|-----------|-------|-----------|
| **Learning type** | Deliberate, conscious | Automatic, unconscious |
| **Unit of knowledge** | Skill (structured protocol) | Instinct (behavioral tendency) |
| **Trigger** | User explicitly runs `/forge` | Always on — fires on every tool call |
| **Input** | User reflection + session summary | Raw tool observations (JSONL) |
| **Output** | `SKILL.md` files | `instinct.yaml` files |
| **Author** | Human + AI collaboration | Background Haiku observer |
| **Confidence** | High (deliberate review) | Graduated 0.3–0.9 (evidence-based) |
| **Scope** | Global by default | Project-scoped by default |

Think of Forge as **deliberate practice** and Mulahazah as **muscle memory**. They are complementary — instinct clusters detected by Mulahazah naturally become candidates for Forge skill proposals.

---

## Key Features

### 1. 100% Hook Observation
Every `PreToolUse` and `PostToolUse` event is captured by `observe.sh`. The hook is designed to complete in under 50ms and always exits 0 — it never blocks your Claude session.

### 2. Atomic Instincts with Confidence Scoring
Each learned behavior is stored as a YAML instinct with a confidence score (0.3–0.9). Confidence rises with repeated evidence and decays when a behavior is no longer observed or contradicted.

```yaml
id: prefer-edit-over-write
confidence: 0.72
domain: workflow
content: |
  When modifying an existing file, always use the Edit tool
  rather than Write. Write is reserved for creating new files only.
```

### 3. Project-Scoped Isolation
Instincts are stored under a SHA-256 hash of the project root path. Patterns learned in one codebase do not contaminate another. Global patterns require the same behavior appearing across 3+ distinct projects.

### 4. Graduated Behavior
The system transitions through three modes based on instinct confidence:

| Mode | Confidence Range | Behavior |
|------|-----------------|----------|
| **Silent** | 0.3–0.49 | Observes only, no output |
| **Suggest** | 0.5–0.69 | Mentions the instinct as a suggestion |
| **Auto-apply** | 0.70–0.90 | Applies the instinct automatically |

### 5. Background Haiku Observer
`observer-loop.sh` runs as a background process, waking every 5 minutes to analyze accumulated observations. It uses the Haiku model for cost efficiency — pattern detection doesn't require the full capabilities of Sonnet.

### 6. Three Learning Channels
Mulahazah recognizes three signal types, in priority order:

1. **User Corrections** — immediately undoing or redoing what Claude just produced (highest signal)
2. **Error Resolution Sequences** — compact chains of tools that fix a failure (strong signal)
3. **Repeated Workflows** — the same sequence of 3+ tools appearing across 3+ sessions (medium signal)

---

## Directory Structure (after install)

```
~/.claude/mulahazah/
├── config.json                    # Observer settings
├── observer.pid                   # Background observer PID
├── observer.log                   # Observer activity log
├── projects.json                  # Global project registry
├── projects/
│   └── <project-hash>/
│       ├── project.json           # Project metadata
│       ├── observations.jsonl     # Raw tool observations
│       └── observations.archive/  # Rotated archives (>10k lines)
└── instincts/
    ├── global/                    # Cross-project instincts
    └── <project-hash>/            # Project-scoped instincts
        └── <instinct-id>.yaml
```

---

## Synergy Table

| System | How Mulahazah Integrates |
|--------|--------------------------|
| **Forge** | Instinct clusters with 3+ supporting observations become Forge skill proposals. Run `/forge` to promote instincts to full skills. |
| **Observation System** | Mulahazah IS an observation system — `observe.sh` is its hook. They share the same JSONL format. |
| **Decision Log** | High-confidence instincts (0.7+) that were auto-applied are logged as decisions for traceability. |
| **Save Diary** | On session end, active instincts above 0.6 confidence are included in the diary summary. |
| **Memory Consolidation** | During consolidation, Mulahazah instincts are reviewed — stale instincts (not seen in 30+ days) have their confidence decayed automatically. |

---

## Installation

See [install-mulahazah.md](./install-mulahazah.md) for the full step-by-step installation protocol.

**Quick install:**
```
Load Mulahazah
```

---

## Skill Reference

See [SKILL.md](./SKILL.md) for the MemoryCore skill definition that enables the `/continuous-improve` command and instinct status reporting.

---

*Mulahazah v1.0 — part of the AI MemoryCore feature ecosystem*
