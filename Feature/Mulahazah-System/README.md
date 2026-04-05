# 👁️ Mulahazah System — Behavioral Learning
*Your AI learns how you work, not just what you said.*

## What This Feature Does

Adds unconscious behavioral learning to your AI companion:

- **Hook-based observation** that captures every tool call as JSONL (<50ms, never blocks)
- **Haiku-powered analysis** that extracts behavioral rules from session patterns
- **Persistent rules** in `rules.md` — your AI reads them each session and follows them
- **One command** (`/continuous-improve`) to reflect, analyze, and review learned rules
- **Background observer** (optional) for automatic periodic analysis

## The Problem It Solves

Your AI handles tasks through conversation. Over time, you correct the same mistakes:
- "No, use Grep before Edit"
- "Always check rate limits first"  
- "Run tests before committing"

Without Mulahazah, corrections vanish between sessions. Your AI makes the same mistakes tomorrow. With Mulahazah, corrections become persistent rules that strengthen through repetition and decay without reinforcement.

**Forge is deliberate** — you notice a pattern and create a skill.
**Mulahazah is automatic** — hooks observe your sessions and extract rules you never consciously noticed.

## Quick Integration

```bash
# Option 1: npx (recommended — installs hooks + observer + command)
npx continuous-improve-skill --target claude

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

### On-Demand Analysis (/continuous-improve)
```
You: /continuous-improve

Mulahazah:
  Reflection — What worked, what failed, rule to add
  Analysis — 47 observations analyzed, 2 new rules extracted:
    - Use Grep → Read → Edit workflow for code modifications
    - Check rate limits before setting polling intervals
  Status — 5 total rules in rules.md
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
| **Observation System** | Mulahazah rules inform Refine's quality checks |

## Tested End-to-End

```
observe.sh captured 7 tool calls → analyze.sh sent to Haiku →
Haiku extracted: "Use Grep → Read → Edit workflow" →
Rule saved to rules.md → Available in next session
```

## Platform Note

Includes `SKILL.md` for auto-triggering via the Skill Plugin System. Full installation (hooks, observer, analysis pipeline) requires Claude Code and is handled by the npm installer or manual install protocol.
