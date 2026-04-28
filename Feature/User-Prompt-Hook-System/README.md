# 💬 User-Prompt-Hook System
*Generic UserPromptSubmit hook framework — plug-and-play context injection on every user message*

## What This Feature Does

Wires a single `UserPromptSubmit` hook into your Claude Code `~/.claude/settings.json`. The hook fires on **every user message** before the AI sees it, runs all injector scripts in `~/.claude/hooks/user-prompt-injectors/`, concatenates their outputs, and prepends the result into the prompt context.

**This feature is the framework, not a specific behavior.** What gets injected (time, tone, mood, project status, etc.) lives in **separate sibling injector features** that drop their scripts into a known directory. Install this base once; layer injectors on top whenever you want.

- **Plug-and-play architecture** — drop a `.ps1` or `.sh` into the injectors directory, next prompt picks it up
- **Single hook entry** — one entry in `settings.json` no matter how many injectors you install
- **Fail-isolated** — if one injector errors, master catches it and the others still run
- **Cross-platform** — ships both Windows (PowerShell) and Unix (Bash) master scripts
- **Safely reversible** — backs up `settings.json` before any modification
- **Tool-agnostic** — feature folder stays in the repo so users on other AI tools (Codex, etc.) can read and run the same protocols

## Why a Framework?

The naive approach would be one feature per behavior — `Time-Hook-System`, `Tone-Hook-System`, `Mood-Hook-System` — each wiring its own UserPromptSubmit entry. That works, but it bloats `settings.json` with N hook entries and makes uninstall fragile.

This framework flips it: **one master hook, N pluggable injectors**. Each injector is just a tiny script that produces one line of output. The master enumerates them on every fire, runs them, joins their outputs, emits the result.

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│ Claude Code emits UserPromptSubmit event (every user message)    │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
        ┌────────────────────────────────────────────────┐
        │ ~/.claude/hooks/user-prompt-hook.{ps1|sh}      │ ← master script
        │ (the only entry in settings.json)              │
        │                                                │
        │  1. Drain stdin                                │
        │  2. Enumerate injectors directory              │
        │  3. For each injector: invoke + collect stdout │
        │  4. Join with newlines                         │
        │  5. Emit result                                │
        └─────────────┬──────────────────────────────────┘
                      │
                      ▼
       ┌────────────────────────────────────────────────┐
       │ ~/.claude/hooks/user-prompt-injectors/         │
       │   ├── time.ps1           ← future feature      │
       │   ├── tone.ps1           ← future feature      │
       │   └── ...                ← any future inject   │
       └────────────────────────────────────────────────┘
```

## Quick Integration
```
"Load user-prompt-hook"
```

## What Happens During Integration

1. **Detect OS** — pick the right master script template (`.ps1` for Windows, `.sh` for Unix)
2. **Create master hook** at `~/.claude/hooks/user-prompt-hook.{ps1|sh}`
3. **Create empty injectors directory** at `~/.claude/hooks/user-prompt-injectors/`
4. **Backup** your current `~/.claude/settings.json` to `settings.json.backup-pre-userprompthook`
5. **Merge** the new `UserPromptSubmit` entry into `settings.json` (preserving any existing hooks)
6. **Record** the install in `master-memory.md` Optional Components

After install, the framework is live but **does nothing** until you install at least one injector — the master hook fires, enumerates an empty directory, emits no output, returns.

## Adding Injectors

Two paths:

**Path A: Install a sibling injector feature** (preferred)
- `Feature/Time-Prompt-Inject-System/` (coming) — injects timestamp + period
- `Feature/Tone-Prompt-Inject-System/` (coming) — injects current AI tone from session memory
- Each runs its own install protocol that drops its script into `~/.claude/hooks/user-prompt-injectors/`

**Path B: Write your own injector**
See `injector-format.md` for the canonical contract. The `examples/` folder contains a working "hello world" timestamp injector you can copy and modify.

## Hook Configuration

After install, the relevant slice of `~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "<platform-specific path to master script>",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

| Setting | Value | Reason |
|---------|-------|--------|
| `timeout` | `10` | Hook must complete before AI sees the prompt — keep it tight |
| `async` | *(absent)* | UserPromptSubmit must NOT be async — async would race against prompt processing |

## Uninstalling

After install, type:
```
"uninstall user-prompt-hook"
```

If you have injectors installed, the uninstall will **warn first** — uninstalling the framework leaves their scripts orphan (still on disk, never fire). Recommend uninstalling each injector feature before the framework.

The uninstall will:
1. Restore `settings.json` from backup
2. Delete the master hook script from `~/.claude/hooks/`
3. Optionally delete the injectors directory (only if empty)
4. Remove the install record from `master-memory.md`

Result: clean revert. Your AI's prompt context goes back to whatever Claude Code emits by default.

## Compatibility

- **Pre-consolidation** ✅ — install only writes to `master-memory.md`, agnostic to your memory architecture
- **Post-consolidation** ✅ — same path
- **Windows / macOS / Linux / Git Bash** ✅ — both `.ps1` and `.sh` master scripts ship
- **Coexists with Auto-Load-Hook-System** ✅ — different hook events (SessionStart vs UserPromptSubmit)
- **Coexists with Time-based-Aware-System** ✅ — Time-Aware tells the AI how to query time on demand; this framework + a Time-Inject injector pre-injects time without the AI having to ask

## Tier

**Tier 1 — Foundation**, alongside Memory Consolidation, Skill Plugin, Time-Aware, Auto-Load-Hook. No dependencies; install in any order.

---

*Type `"Load user-prompt-hook"` to wire the framework. Then layer injectors as you build them.*
