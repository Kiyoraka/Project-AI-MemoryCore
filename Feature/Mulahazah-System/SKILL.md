---
name: mulahazah
description: "MUST use when user says 'continuous-improve', 'instinct status',
             'what have you learned', 'show instincts', 'mulahazah status',
             'what patterns have you noticed', 'behavioral learning', 'what instincts do you have',
             'show learned behaviors', or when user asks about unconscious learning,
             habit formation, or behavioral patterns Claude has observed."
---

# Mulahazah — Instinct-Based Behavioral Learning
*Unconscious observation that shapes how Claude works with you*

## Activation

When this skill activates, output:

`Mulahazah active — reading instincts for this project...`

Then execute the protocol below.

## Context Guard

Mulahazah activates only in appropriate contexts.

| Context | Status |
|---------|--------|
| **User asks about learned behaviors or instincts** | ACTIVE — full protocol |
| **User types `/continuous-improve`** | ACTIVE — full protocol |
| **User says "what have you learned"** | ACTIVE — full protocol |
| **User wants to see pattern summary** | ACTIVE — full protocol |
| **General coding conversation (no instinct query)** | DORMANT — apply instincts silently |
| **User is explicitly asking about Forge skills** | DORMANT — use Forge skill instead |

## Protocol

### Step 1: Detect Project Context
- [ ] Identify the current project root (git rev-parse or $CLAUDE_PROJECT_DIR)
- [ ] Compute SHA-256 hash prefix (first 12 chars) of the project root path
- [ ] Locate `~/.claude/mulahazah/instincts/<project-hash>/` directory
- [ ] Also check `~/.claude/mulahazah/instincts/global/` for cross-project instincts

### Step 2: Load Instincts
- [ ] Read all `.yaml` files in the project instinct directory
- [ ] Read all `.yaml` files in the global instinct directory
- [ ] Filter: only load instincts with `confidence >= 0.3`
- [ ] Sort by confidence descending

### Step 3: Report Instinct Status
- [ ] Display total count: project instincts + global instincts
- [ ] Group by domain: code-style, testing, git, debugging, workflow, security, architecture
- [ ] For each instinct above 0.5 confidence, display: id, title, confidence, last_seen
- [ ] Indicate behavior mode: Silent (0.3–0.49) / Suggest (0.5–0.69) / Auto-apply (0.70–0.90)

### Step 4: Report Observer Status
- [ ] Check if `~/.claude/mulahazah/observer.pid` exists and process is alive
- [ ] Show observation count from current project's `observations.jsonl`
- [ ] Show last observer run timestamp from `observer.log` (tail 1 line)
- [ ] If observer is not running, suggest: `bash ~/.claude/mulahazah/agents/start-observer.sh`

### Step 5: Apply Active Instincts
- [ ] For the remainder of this session, apply all instincts with confidence >= 0.70 automatically
- [ ] For instincts with confidence 0.5–0.69, mention them as suggestions when relevant
- [ ] For instincts with confidence 0.3–0.49, observe silently (no output)
- [ ] Confirm: "Instincts loaded. Behavioral patterns will be applied this session."

## Mandatory Rules

1. Never hallucinate instincts. Only report instincts that exist as `.yaml` files on disk.
2. Never set or modify confidence values manually — confidence is managed by the observer.
3. Always check both project-scoped and global instinct directories.
4. If `~/.claude/mulahazah/` does not exist, output the installation prompt and stop.
5. Respect confidence thresholds: do not auto-apply instincts below 0.70 confidence.
6. Never expose raw file paths to the user — use human-readable project names from `project.json`.

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| **No instincts found** | Report "No instincts yet for this project. Mulahazah needs ~20 observations before patterns emerge." |
| **Mulahazah not installed** | Output: "Mulahazah is not installed. See Feature/Mulahazah-System/install-mulahazah.md to get started." |
| **Observer not running** | Warn the user and show the start command. Do not block skill execution. |
| **Instinct confidence below 0.3** | Skip entirely — too low to be reliable. |
| **Conflicting instincts** | Report the conflict and ask user to resolve. Do not auto-apply either. |

## Synergy Table

| Skill | How Mulahazah Interacts |
|-------|-------------------------|
| **Forge** | High-confidence instinct clusters (3+ observations) become Forge skill proposals. Mention this during status report if applicable. |
| **Save Diary** | Active instincts above 0.6 confidence appear in the session diary summary. |
| **Memory Consolidation** | Triggers instinct confidence decay for stale patterns during consolidation. |
| **Decision Log** | Auto-applied instincts (0.7+) are logged as behavioral decisions. |

## Level History

- **Lv.1** — Base: Instinct status reporting, project detection, observer health check, confidence-graduated behavior. Hook observation via `observe.sh`. Background Haiku analysis via `observer-loop.sh`. (Origin: continuous-improve v1.0, ported to MemoryCore as Mulahazah System)
