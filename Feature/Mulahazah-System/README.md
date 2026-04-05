# 👁️ Mulahazah System
*Your AI companion learns how you work -- not just what you said.*

> *"Observation is the first teacher."*

---

## What It Does

Adds unconscious behavioral learning to your AI companion:

- **Hook-based observation** that captures every tool call as JSONL (<50ms, never blocks)
- **Haiku-powered analysis** that extracts behavioral rules from session patterns
- **Persistent rules** in `rules.md` -- your AI reads them each session and follows them
- **One command** (`/continuous-improvement`) to reflect, analyze, and review learned rules
- **Background observer** (optional) for automatic periodic analysis

## The Problem It Solves

Your AI companion handles tasks through conversation. Over time, you correct the same mistakes:
- "No, use Grep before Edit"
- "Always check rate limits first"
- "Run tests before committing"

Without Mulahazah, corrections vanish between sessions. Your AI makes the same mistakes tomorrow. With Mulahazah, corrections become persistent rules that strengthen through repetition and decay without reinforcement.

## How It Differs From Forge

| Aspect | Forge | Mulahazah |
|--------|-------|-----------|
| **How it starts** | You notice a pattern and create a skill | Hooks observe your sessions automatically |
| **Effort** | Deliberate -- you write the skill | Automatic -- rules extracted without input |
| **Output** | Structured skill with full protocol | Lightweight rules in `rules.md` |
| **Trigger** | You say "Load forge" | Fires silently on every tool call |
| **Best for** | Deep, reusable skills | Behavioral corrections and preferences |

## Quick Integration

```bash
# Option 1: npx (recommended -- installs hooks, observer, and command)
npx continuous-improvement install --target claude

# Option 2: Manual (see install-mulahazah.md for full protocol)
```

## How It Works After Integration

### Automatic Observation (always on)
```
You work normally in Claude Code
  → hooks silently capture every tool call as JSONL
  → observations accumulate in ~/.claude/mulahazah/projects/<hash>/
  → no performance impact (<50ms per hook, append-only)
```

### On-Demand Analysis (/continuous-improvement)
```
You: /continuous-improvement

Mulahazah:
  Reflection -- What worked, what failed, rule to add
  Analysis -- 47 observations analyzed, 2 new rules extracted:
    - Use Grep → Read → Edit workflow for code modifications
    - Check rate limits before setting polling intervals
  Status -- 5 total rules in rules.md
```

### Persistent Rules
```
Next session, your AI reads rules.md and follows the accumulated rules.
Rules that keep being reinforced stay. Rules without evidence decay.
```

## Synergy with Other Features

| Feature | Integration |
|---------|-------------|
| **Forge** | Rule clusters from rules.md become Forge skill proposals |
| **Save Diary** | Session learning summary included in diary entries |
| **Decision Log** | Rules applied during sessions logged as behavioral decisions |
| **Memory Consolidation** | Triggers review of rules.md for stale entries |
| **Skill Plugin System** | Mulahazah activates via SKILL.md auto-trigger |

---

*Your AI companion gets wiser with every session -- one rule at a time.*
