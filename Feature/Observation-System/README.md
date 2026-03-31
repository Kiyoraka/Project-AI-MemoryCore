# Observation System
*Tiered code awareness — see clearly before you act*

## What This Feature Does

Adds a **4-tier observation system** to your AI companion, enabling structured project inspection at different depths — from a 30-second health check to a full system audit.

- **Survey** (Lv.1) — Quick bird's-eye view of project health (~30 sec)
- **Investigate** (Lv.2) — Deep dive into a specific area, bug, or file (~5 min)
- **Refine** (Lv.2) — Review and fix changed code for quality (~5 min)
- **Audit** (Lv.3) — Full system audit with architecture mapping (~15 min)

## Why Tiered Observation?

Most AI companions either do nothing (respond to what's asked) or dump everything (overwhelming output). The tier system solves this:

```
"How's the project?"     → Survey    (30 sec, one screen)
"What's going on here?"  → Investigate (5 min, focused)
"Clean up my code"       → Refine    (5 min, corrective)
"Show me everything"     → Audit     (15 min, exhaustive)
```

**The right depth for the right question.** Don't audit when you need a survey. Don't survey when you need an audit.

## Key Innovation: Corrective vs Investigative

Three tiers are **investigative** — they observe and report:
- Survey, Investigate, Audit → "Here's what I found"

One tier is **corrective** — it observes AND fixes:
- Refine → "Here's what I found, and here's the fix (with your permission)"

This distinction matters. Refine is the quality gate you run before every commit.

## Escalation Pattern

```
Survey spots problem    →  Investigate that area
Investigate finds depth →  Audit the full system
Any tier finds code     →  Refine specific files
Refine finds systemic   →  Audit the full system
```

Tiers are aware of each other and suggest escalation when appropriate.

## Cross-Feature Integration

The Observation System integrates with other MemoryCore features when installed:

| Feature | Integration |
|---------|------------|
| **Library System** | Link findings to knowledge entries; suggest new entries for undocumented patterns |
| **Post-Mortem System** | Cross-reference project against past incidents during Survey |
| **Work-Plan Execution** | Survey before planning; Refine after each task; Audit at milestones |
| **Auto-Commit System** | Refine → fix → auto-commit chain |

All integrations are optional — the Observation System works independently.

## Cost Awareness

Each tier has a different computational cost. Match tier to effort for optimal resource usage:

| Tier | Effort | Delegation | Why |
|------|--------|-----------|-----|
| **Survey** | Low | Can delegate to lighter model/agent | Mostly file scanning, git status |
| **Investigate** | Medium | Primary AI recommended | Code comprehension, flow tracing |
| **Refine** | Medium | Primary AI recommended | Must understand intent before fixing |
| **Audit** | High | Primary AI recommended | Cross-system analysis, risk assessment |

**The cost-saving pattern**: frequent cheap observation prevents expensive deep audits. Survey daily, Refine before every commit, Audit at milestones.

## Quick Start

```
"survey"                        → Quick project health check
"investigate authentication"    → Deep dive into auth system
"investigate bug login fails"   → Trace a bug to root cause
"refine"                        → Review all changed files
"refine src/services/Auth.cs"   → Review specific file
"audit"                         → Full system audit
"audit cross"                   → Cross-project comparison
```

## Origin

Developed and refined across multiple production projects. Every protocol step exists because something went wrong without it — especially the dependency scan (which prevents false findings from assumed library behavior).

---

*Observation System v1.0*
