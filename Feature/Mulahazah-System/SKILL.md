---
name: mulahazah
description: "MUST use when user says 'continuous-improve', 'instinct status',
             'what have you learned', 'show learned rules', 'mulahazah status',
             'what patterns have you noticed', 'behavioral learning', 'show rules',
             or when user asks about session learning, accumulated rules, or
             patterns Claude has observed."
---

# Mulahazah -- Behavioral Learning System
*The AI that remembers how you work.*

## Activation

When this skill activates, output:

`Mulahazah active -- reading learned rules for this project...`

Then execute the protocol below.

## Overview

Mulahazah is a passive observation layer built into your AI companion. It captures every tool call as structured data, analyzes patterns with Haiku, and writes actionable rules to `rules.md`. Those rules persist across sessions -- silently shaping how your AI works with you, without needing to be reminded each time.

## Context Guard

| Context | Status |
|---------|--------|
| **User asks about learned rules or patterns** | ACTIVE -- full protocol |
| **User types `/continuous-improve`** | ACTIVE -- full protocol |
| **User says "what have you learned"** | ACTIVE -- full protocol |
| **User wants to see rule summary** | ACTIVE -- full protocol |
| **General coding conversation** | DORMANT -- follow rules.md silently |
| **User is explicitly asking about Forge skills** | DORMANT -- use Forge skill instead |

## Protocol

### Step 1: Read Learned Rules

- [ ] Check `~/.claude/mulahazah/rules.md` -- this is where learned rules live
- [ ] If the file does not exist, report "No rules yet. Run `/continuous-improve` after a work session to generate them."
- [ ] Count and display total rules

### Step 2: Session Reflection

Generate a reflection for this session:

```
## Reflection -- [Date]
- What worked:
- What failed:
- What I'd do differently:
- Rule to add:
```

If there is a "Rule to add", check `~/.claude/mulahazah/rules.md` to see if it already exists. If not, append it.

### Step 3: Analyze Observations (if requested or on /continuous-improve)

- [ ] Check for `~/.claude/mulahazah/projects/*/observations.jsonl`
- [ ] If 5+ observations exist, run: `bash ~/.claude/mulahazah/bin/analyze.sh`
- [ ] Report what analysis found: new rules extracted, or "no new patterns yet"
- [ ] If no observations found, note that hooks may not be installed

### Step 4: Report Observer Status

- [ ] Check if `~/.claude/mulahazah/observer.pid` exists and process is alive
- [ ] If running: show PID and confirm background analysis is active
- [ ] If not running: mention it is optional, show start command: `bash ~/.claude/mulahazah/agents/start-observer.sh`

### Step 5: Display Full Rule Status

Read `~/.claude/mulahazah/rules.md` and display:
- Total rule count
- Rules grouped by date they were added
- Any rules that look outdated or contradictory (flag for user review)

## Mandatory Rules

1. Never hallucinate rules. Only report rules that exist in `~/.claude/mulahazah/rules.md`.
2. Never invent observations -- only report what exists in observations.jsonl files.
3. If `~/.claude/mulahazah/` does not exist, output the installation prompt and stop.
4. Do not auto-apply rules without the user's awareness -- surface them in the reflection step.
5. When rules.md exists and contains rules, follow them in your work during this session.

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| **No rules.md yet** | Report "No rules yet for this project. Run `/continuous-improve` after your first work session." |
| **Mulahazah not installed** | Output: "Mulahazah is not installed. See Feature/Mulahazah-System/install-mulahazah.md to get started." |
| **Observer not running** | Note it is optional and show start command. Do not block skill execution. |
| **analyze.sh not found** | Report the missing path and remind user to re-run install steps. |
| **Fewer than 5 observations** | Note more tool calls are needed before patterns can be extracted. |

## Synergy with Other Features

| Feature | How Mulahazah Interacts |
|---------|-------------------------|
| **Forge** | Rule clusters from rules.md with repeated patterns become Forge skill proposals. |
| **Save Diary** | Active rules from rules.md are summarized in the session diary. |
| **Memory Consolidation** | Triggers review of rules.md for stale or contradictory entries. |
| **Decision Log** | Rules applied during a session are logged as behavioral decisions. |

## Level History

- **Lv.1** -- Base: rules.md persistence, session reflection, observation capture via `observe.sh`, Haiku-powered analysis via `analyze.sh`, `/continuous-improve` command. Background observer optional. (Origin: continuous-improve v2.0, ported to MemoryCore as Mulahazah System. Tested end-to-end: observations captured, analyze.sh extracted "Grep → Read → Edit workflow" rule.)
