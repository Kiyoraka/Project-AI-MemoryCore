# Mulahazah System
*Observation-based behavioral learning — hooks capture tool calls, Haiku extracts rules, rules persist in rules.md*

## What Is Mulahazah?

**Mulahazah** (Arabic: ملاحظة — "observation") is a behavioral learning system for Claude Code. While you work, Mulahazah silently records every tool call via Claude Code's hook system. When you run `/continuous-improve`, it passes those observations to a Haiku analysis agent which extracts actionable rules and appends them to `~/.claude/mulahazah/rules.md`.

Rules accumulate session by session. At the start of each session, Claude reads rules.md and follows what was learned.

---

## How It Actually Works

```
Tool call happens
      ↓
observe.sh (hook, <50ms, always exits 0)
      ↓
observations.jsonl (one JSONL line per tool call)
      ↓
/continuous-improve  ←  or  ←  background observer (optional)
      ↓
analyze.sh (runs Haiku on last 200 observations)
      ↓
rules.md (new rules appended with date stamp)
      ↓
Next session: Claude reads rules.md and follows them
```

---

## How Mulahazah Differs from Forge

| Dimension | Forge | Mulahazah |
|-----------|-------|-----------|
| **Learning type** | Deliberate, conscious | Automatic, observation-based |
| **Unit of knowledge** | Skill (structured protocol) | Rule (actionable instruction) |
| **Trigger** | User explicitly runs `/forge` | Hooks fire on every tool call; `/continuous-improve` extracts rules |
| **Input** | User reflection + session summary | Raw tool observations (JSONL) |
| **Output** | `SKILL.md` files | Lines in `rules.md` |
| **Author** | Human + AI collaboration | Haiku analysis agent |
| **Scope** | Global by default | Project-scoped observations, shared rules.md |

Think of Forge as **deliberate practice** and Mulahazah as **building habits**. Repeated patterns in rules.md naturally become candidates for Forge skill proposals.

---

## What Actually Works (Tested End-to-End)

The following pipeline was tested end-to-end and confirmed working:

1. **observe.sh** — captured tool calls via PreToolUse/PostToolUse hooks, writing JSONL to `projects/<hash>/observations.jsonl`
2. **analyze.sh** — passed observations to Haiku, which identified the repeated "Grep → Read → Edit workflow" pattern and extracted it as a rule
3. **rules.md** — rule was appended with date stamp and persisted correctly
4. **/continuous-improve command** — triggered reflection + analysis + status display in one step
5. **Background observer** — started via `start-observer.sh`, ran every 5 minutes, called `analyze.sh` on schedule

What is NOT in this implementation:
- Confidence scoring or graduated behavior tiers (0.3/0.5/0.7 thresholds) — removed, not implementable via system prompt reliably
- YAML instinct files — replaced with plain rules.md which Claude can actually read
- Auto-apply instincts — Claude reads rules.md and follows them naturally, no separate mechanism needed

---

## Key Components

### observe.sh
PreToolUse/PostToolUse hook. Captures every tool call as a JSONL line. Completes in under 50ms. Always exits 0 — never blocks your Claude session. Detects project root via git or `$CLAUDE_PROJECT_DIR`.

### analyze.sh
The actual analysis pipeline. Reads the last 200 observations, sends them to Haiku with a structured prompt, and appends new rules to `~/.claude/mulahazah/rules.md`. Skips if fewer than 5 observations exist.

### rules.md
Plain markdown file at `~/.claude/mulahazah/rules.md`. Rules are appended with date stamps. Claude reads this at the start of each session (when the skill is loaded) and follows the rules. Remove any rule that causes problems.

### /continuous-improve
The main user-facing command. Runs three steps in order:
1. Session reflection (what worked, what failed, rule to add)
2. Observation analysis via analyze.sh
3. Full rules.md status display

### Background Observer (optional)
`start-observer.sh` launches `observer-loop.sh` as a background process. It wakes every 5 minutes and calls `analyze.sh` when 20+ observations are accumulated. Useful for teams or long work sessions.

---

## Directory Structure (after install)

```
~/.claude/mulahazah/
├── config.json                    # Observer settings
├── observe.sh                     # PreToolUse/PostToolUse hook
├── rules.md                       # Learned rules (grows over time)
├── observer.pid                   # Background observer PID (after start)
├── observer.log                   # Observer activity log
├── projects.json                  # Global project registry
├── bin/
│   └── analyze.sh                 # Analysis pipeline (Haiku)
├── agents/
│   ├── observer.md                # Observer agent system prompt
│   ├── observer-loop.sh           # Background analysis loop
│   └── start-observer.sh         # Observer launcher
└── projects/
    └── <project-hash>/
        ├── project.json           # Project metadata
        ├── observations.jsonl     # Raw tool observations
        └── observations.archive/  # Rotated archives (>10k lines)
```

---

## Installation

See [install-mulahazah.md](./install-mulahazah.md) for the full step-by-step installation protocol.

**Quick start:**
```bash
# 1. Create dirs
mkdir -p ~/.claude/mulahazah/bin ~/.claude/mulahazah/agents ~/.claude/mulahazah/projects

# 2. Copy scripts
cp Feature/Mulahazah-System/hooks/observe.sh ~/.claude/mulahazah/observe.sh
cp Feature/Mulahazah-System/bin/analyze.sh ~/.claude/mulahazah/bin/analyze.sh
cp Feature/Mulahazah-System/agents/* ~/.claude/mulahazah/agents/
cp Feature/Mulahazah-System/config.json ~/.claude/mulahazah/config.json
chmod +x ~/.claude/mulahazah/observe.sh ~/.claude/mulahazah/bin/analyze.sh
chmod +x ~/.claude/mulahazah/agents/observer-loop.sh ~/.claude/mulahazah/agents/start-observer.sh

# 3. Initialize
echo '{}' > ~/.claude/mulahazah/projects.json
touch ~/.claude/mulahazah/rules.md

# 4. Copy the command
mkdir -p ~/.claude/commands
cp Feature/Mulahazah-System/commands/continuous-improve.md ~/.claude/commands/

# 5. Configure hooks in ~/.claude/settings.json (see install-mulahazah.md Step 3)
```

---

## Skill Reference

See [SKILL.md](./SKILL.md) for the MemoryCore skill definition that enables the `/continuous-improve` command and rule status reporting.

---

*Mulahazah v2.0 — part of the AI MemoryCore feature ecosystem*
