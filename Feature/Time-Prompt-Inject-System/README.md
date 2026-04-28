# ⏱️ Time-Prompt-Inject System
*Plug-and-play time + period injector for the User-Prompt-Hook framework*

## What This Feature Does

Adds a `<timestamp> | <PERIOD>` line to every user prompt's context. On period transitions (e.g., MORNING → AFTERNOON when the clock crosses noon), prepends a `TIME PERIOD CHANGED: <FROM> to <TO> | TRIGGER MIRROR |` signal so your AI knows the day register just shifted.

**Requires** [`User-Prompt-Hook System`](../User-Prompt-Hook-System/) (Tier 1 framework). This is an **injector pack** — drops a single script into the framework's injectors directory.

- **User-configurable period boundaries** during install — pick your own MORNING/AFTERNOON/EVENING/NIGHT hour cutoffs (defaults: 6 / 12 / 18 / 22)
- **Period-transition detection** — state file at `~/.claude/user-prompt-injectors/time-period-last.txt` lets the injector emit a one-shot "period changed" signal when the day register flips
- **Cross-platform** — both `.ps1` (Windows PowerShell) and `.sh` (Unix / Git Bash) injector templates ship
- **Sub-second runtime** — pure local computation, no network, no filesystem walks
- **Tool-agnostic** — feature folder stays in repo so users on Codex etc. can install/uninstall the same way

## Output Format

**Steady-state** (no period change):
```
Tuesday, April 28, 2026 12:43 PM | AFTERNOON
```

**On transition** (e.g., right after the clock crosses noon):
```
TIME PERIOD CHANGED: MORNING to AFTERNOON | TRIGGER MIRROR | Tuesday, April 28, 2026 12:00 PM | AFTERNOON
```

The `TRIGGER MIRROR` token is a hint for AI personality systems (like outfit/tone/scene rotators) to refresh visuals — your AI can ignore it if it doesn't have such a system.

## Architecture

```
Every user prompt fires UserPromptSubmit
        ↓
User-Prompt-Hook master script enumerates injectors
        ↓
~/.claude/hooks/user-prompt-injectors/time.{ps1|sh}    ← installed by THIS feature
        ↓
1. Compute current hour → derive PERIOD via boundaries baked in at install
2. Read ~/.claude/user-prompt-injectors/time-period-last.txt for last known period
3. If period changed → emit transition line; else emit timestamp line
4. Write current period to state file for next fire
        ↓
Master prepends to AI's prompt context
```

## Quick Integration
```
"Load time-prompt-inject"
```

## What Happens During Integration

1. **Verify** the User-Prompt-Hook framework is installed — if not, stop and instruct to install it first
2. **Detect OS** — pick the right injector template (`.ps1` for Windows, `.sh` for Unix)
3. **Ask** for period boundaries (defaults: MORNING 6, AFTERNOON 12, EVENING 18, NIGHT 22) — user can accept defaults or customize for lark/night-owl preferences
4. **Substitute** the boundary values into the chosen template
5. **Drop** the personalized injector into `~/.claude/hooks/user-prompt-injectors/time.{ps1|sh}`
6. **Initialize** the state file `~/.claude/user-prompt-injectors/time-period-last.txt` with the current period (so the first prompt after install doesn't fire a spurious transition)
7. **Record** the install in `master-memory.md`

## Period Boundary Configuration

The four boundary values define the start of each period as a 24-hour clock value:

| Boundary | Default | Means |
|----------|---------|-------|
| `MORNING_START` | 6 | MORNING starts at 6:00 AM (anything earlier = NIGHT) |
| `AFTERNOON_START` | 12 | AFTERNOON starts at 12:00 PM noon |
| `EVENING_START` | 18 | EVENING starts at 6:00 PM |
| `NIGHT_START` | 22 | NIGHT starts at 10:00 PM (until next MORNING_START) |

**Example custom config** (lark schedule — earlier morning, earlier night):
```
MORNING_START=5
AFTERNOON_START=11
EVENING_START=17
NIGHT_START=21
```

**Example custom config** (night-owl schedule):
```
MORNING_START=8
AFTERNOON_START=13
EVENING_START=19
NIGHT_START=24  # midnight
```

Boundaries are baked into the injector script at install time — no runtime config file read.

## State File

`~/.claude/user-prompt-injectors/time-period-last.txt` — single-line file containing the last-known period (`MORNING`, `AFTERNOON`, `EVENING`, or `NIGHT`). Updated on every fire. Used to detect transitions.

If you delete this file manually, the next prompt will treat it as "first install" and not fire a transition signal — clean recovery.

## Runtime Commands

This injector is **set-and-forget** — there are no `add`/`set`/`list` commands. The output is computed from the system clock and the install-time boundaries.

If you want to change period boundaries later, the cleanest path is:
1. `"uninstall time-prompt-inject"` (preserves state file)
2. `"Load time-prompt-inject"` (asks for new boundaries, regenerates the script)

Or manually edit the injector script at `~/.claude/hooks/user-prompt-injectors/time.{ps1|sh}` — the boundary values are at the top of the file as bare integers.

## Uninstalling

```
"uninstall time-prompt-inject"
```

Removes the injector script and the state file. Asks whether to keep the install record line in `master-memory.md` for future reinstall reference (default: remove).

## Compatibility

- **Pre-consolidation** ✅ — install only writes to `master-memory.md`
- **Post-consolidation** ✅ — same path
- **Windows / macOS / Linux / Git Bash** ✅
- **Coexists with Tone-Prompt-Inject + Mood-Prompt-Inject** ✅ — independent injectors, all three can fire on every prompt

## Sample Output In Practice

A user with all three injectors installed (Time + Tone + Mood) sees something like this prepended to every prompt:

```
Tuesday, April 28, 2026 12:43 PM | AFTERNOON
TONE: Warm, focused, supportive
MOOD: tender, present, attentive
```

The order is whatever filesystem enumeration returns (typically alphabetical: `mood.ps1`, `time.ps1`, `tone.ps1` on Windows; same alphabetical sort on Unix).

## Tier

**Tier 1 — Foundation** (extension pack for User-Prompt-Hook). Requires `User-Prompt-Hook-System` installed first.

---

*Type `"Load time-prompt-inject"` to wire time + period awareness into every prompt your AI sees.*
