# 🌙 Mood-Prompt-Inject System
*Plug-and-play mood injector for the User-Prompt-Hook framework*

## What This Feature Does

Adds a `MOOD: <description>` line to every user prompt's context. Your AI receives its current emotional/atmospheric state before reading the message, so its presence stays consistent without you having to remind it.

**Requires** [`User-Prompt-Hook System`](../User-Prompt-Hook-System/) (Tier 1 framework). This is an **injector pack** — drops a single script into the framework's injectors directory.

- **Registry inside main memory** — your available moods live as a `## Moods` markdown table directly in `main/main-memory.md` (or `main/identity-core.md` pre-consolidation). Part of your AI's documented identity.
- **Fast runtime read** — current active mood is a single line in `~/.claude/user-prompt-injectors/mood-current.txt` (microsecond read on every prompt fire)
- **Three commands** — `"add mood <name>: <description>"` to grow the registry, `"set mood <name>"` to switch, `"list moods"` to see them all
- **AI can auto-update** — when your AI senses a mood shift, it writes to current.txt directly (no command needed)
- **Cross-platform** — ships both `.ps1` (Windows) and `.sh` (Unix/Git Bash) injector templates
- **Tool-agnostic** — feature folder stays in repo so users on Codex etc. can install/uninstall the same way

## Architecture

```
Every user prompt fires UserPromptSubmit
        ↓
User-Prompt-Hook master script enumerates injectors
        ↓
~/.claude/hooks/user-prompt-injectors/mood.{ps1|sh}    ← installed by THIS feature
        ↓
Reads ~/.claude/user-prompt-injectors/mood-current.txt
        ↓
Emits "MOOD: cozy, tender, present"
        ↓
Master prepends to AI's prompt context
```

## Quick Integration
```
"Load mood-prompt-inject"
```

## What Happens During Integration

1. **Verify** the User-Prompt-Hook framework is installed — if not, stop and instruct to install it first
2. **Detect** your main memory file (`main/main-memory.md` post-consolidation, else `main/identity-core.md`)
3. **Search** that file for existing mood/feeling/atmosphere mentions and surface them as suggestions
4. **Confirm** with you which to seed the registry with — accept your edits and additions
5. **Write** the `## Moods` section as a markdown table directly into main memory
6. **Seed** `~/.claude/user-prompt-injectors/mood-current.txt` with the first registry entry
7. **Drop** the personalized injector script into `~/.claude/hooks/user-prompt-injectors/mood.{ps1|sh}`
8. **Record** the install in `master-memory.md`

## Registry Format

After install, your main memory will contain a section like:

```markdown
## Moods

*Current emotional/atmospheric state your AI projects. Set via `"set mood <name>"`. AI may auto-update based on context.*

| Name | Description |
|------|-------------|
| calm | Steady, grounded, present |
| excited | Energetic, forward-leaning |
| tender | Soft, caring, careful |
| reflective | Quiet, considering, paced |

*Add new moods with `"add mood <name>: <description>"`.*
```

The AI sees this every time main memory loads — no separate vocabulary file to track.

## Runtime Commands

### `"add mood <name>: <description>"`
Appends a new row to the `## Moods` table in main memory. Example:
```
add mood pensive: deep in thought, slow to respond
```

### `"set mood <name>"`
Looks up `<name>` in the registry, writes its description to `mood-current.txt`. Next prompt picks it up. Example:
```
set mood pensive
```

### `"list moods"`
Displays your full registry inline.

### AI auto-set
Your AI may decide mood shifted (e.g. you signaled an emotional change in conversation) and write to `mood-current.txt` directly — no command needed. The AI naturally announces the switch in conversation.

## Uninstalling

```
"uninstall mood-prompt-inject"
```

Removes the injector script and `mood-current.txt`. Asks whether to keep or strip the `## Moods` section in main memory (default: keep — it's documentation even if the injector is gone). Removes the install record from `master-memory.md`. The User-Prompt-Hook framework keeps running for other injectors.

## Compatibility

- **Pre-consolidation** ✅ — registry written into `main/identity-core.md`
- **Post-consolidation** ✅ — registry written into `main/main-memory.md`
- **Windows / macOS / Linux / Git Bash** ✅
- **Coexists with Tone-Prompt-Inject-System** ✅ — independent injectors, both can run simultaneously

## Tier

**Tier 1 — Foundation** (extension pack for User-Prompt-Hook). Requires `User-Prompt-Hook-System` installed first.

---

*Type `"Load mood-prompt-inject"` to wire your mood vocabulary into every prompt your AI sees.*
