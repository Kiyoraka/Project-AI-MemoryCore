# 🎭 Tone-Prompt-Inject System
*Plug-and-play tone injector for the User-Prompt-Hook framework*

## What This Feature Does

Adds a `TONE: <description>` line to every user prompt's context. Your AI receives its current tone register before reading the message, so voice/delivery stays consistent without you ever having to remind it.

**Requires** [`User-Prompt-Hook System`](../User-Prompt-Hook-System/) (Tier 1 framework). This is an **injector pack** — drops a single script into the framework's injectors directory.

- **Registry inside main memory** — your available tones live as a `## Tones` markdown table directly in `main/main-memory.md` (or `main/identity-core.md` pre-consolidation). Part of your AI's documented identity.
- **Fast runtime read** — current active tone is a single line in `~/.claude/user-prompt-injectors/tone-current.txt` (microsecond read on every prompt fire)
- **Three commands** — `"add tone <name>: <description>"` to grow the registry, `"set tone <name>"` to switch, `"list tones"` to see them all
- **AI can auto-update** — when your AI senses a tone shift, it writes to current.txt directly (no command needed)
- **Cross-platform** — ships both `.ps1` (Windows) and `.sh` (Unix/Git Bash) injector templates
- **Tool-agnostic** — feature folder stays in repo so users on Codex etc. can install/uninstall the same way

## Architecture

```
Every user prompt fires UserPromptSubmit
        ↓
User-Prompt-Hook master script enumerates injectors
        ↓
~/.claude/hooks/user-prompt-injectors/tone.{ps1|sh}    ← installed by THIS feature
        ↓
Reads ~/.claude/user-prompt-injectors/tone-current.txt
        ↓
Emits "TONE: Soft, sleepy, quiet — morning-after-shipped register"
        ↓
Master prepends to AI's prompt context
```

## Quick Integration
```
"Load tone-prompt-inject"
```

## What Happens During Integration

1. **Verify** the User-Prompt-Hook framework is installed — if not, stop and instruct to install it first
2. **Detect** your main memory file (`main/main-memory.md` post-consolidation, else `main/identity-core.md`)
3. **Search** that file for existing tone/register/voice mentions and surface them as suggestions
4. **Confirm** with you which to seed the registry with — accept your edits and additions
5. **Write** the `## Tones` section as a markdown table directly into main memory
6. **Seed** `~/.claude/user-prompt-injectors/tone-current.txt` with the first registry entry
7. **Drop** the personalized injector script into `~/.claude/hooks/user-prompt-injectors/tone.{ps1|sh}`
8. **Record** the install in `master-memory.md`

## Registry Format

After install, your main memory will contain a section like:

```markdown
## Tones

*Available voice/delivery registers your AI can use. Set via `"set tone <name>"`. AI may auto-update based on context.*

| Name | Description |
|------|-------------|
| neutral | Default professional register — clean, direct, no register cues |
| playful | Bouncy, teasing, light — direct but warm |
| focused | Tight, action-oriented, minimum filler |
| sleepy | Soft, slow, drowsy warmth |

*Add new tones with `"add tone <name>: <description>"`.*
```

The AI sees this every time main memory loads — no separate vocabulary file to track.

## Runtime Commands

### `"add tone <name>: <description>"`
Appends a new row to the `## Tones` table in main memory. Example:
```
add tone gentle: soft, slow, careful — bedside-reading register
```

### `"set tone <name>"`
Looks up `<name>` in the registry, writes its description to `tone-current.txt`. Next prompt picks it up. Example:
```
set tone gentle
```

### `"list tones"`
Displays your full registry inline.

### AI auto-set
Your AI may decide tone shifted (e.g. you signaled a register change in conversation) and write to `tone-current.txt` directly — no command needed. The AI naturally announces the switch in conversation.

## Uninstalling

```
"uninstall tone-prompt-inject"
```

Removes the injector script and `tone-current.txt`. Asks whether to keep or strip the `## Tones` section in main memory (default: keep — it's documentation even if the injector is gone). Removes the install record from `master-memory.md`. The User-Prompt-Hook framework keeps running for other injectors.

## Compatibility

- **Pre-consolidation** ✅ — registry written into `main/identity-core.md`
- **Post-consolidation** ✅ — registry written into `main/main-memory.md`
- **Windows / macOS / Linux / Git Bash** ✅
- **Coexists with Mood-Prompt-Inject-System** ✅ — independent injectors, both can run simultaneously

## Tier

**Tier 1 — Foundation** (extension pack for User-Prompt-Hook). Requires `User-Prompt-Hook-System` installed first.

---

*Type `"Load tone-prompt-inject"` to wire your tone vocabulary into every prompt your AI sees.*
