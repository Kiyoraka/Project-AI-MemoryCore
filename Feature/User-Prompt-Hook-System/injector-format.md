# 💬 Injector Format Specification
*Canonical contract for any script that plugs into the User-Prompt-Hook framework*

## Purpose

This document defines the contract for **injector scripts** — the small per-purpose programs that plug into the User-Prompt-Hook framework. Each injector emits one line of context that gets prepended to every user prompt. Time injection, tone injection, mood injection, project-status injection — all follow this same format.

## Where Injectors Live

```
~/.claude/hooks/user-prompt-injectors/
├── time.ps1            ← installed by Time-Prompt-Inject-System (future)
├── tone.ps1            ← installed by Tone-Prompt-Inject-System (future)
├── mood.ps1            ← potential future injector
└── ...
```

The master hook (`~/.claude/hooks/user-prompt-hook.{ps1|sh}`) enumerates this directory on every fire and runs each injector matching the host OS extension (`.ps1` on Windows, `.sh` on Unix).

## Required Behavior

Every injector script MUST:

1. **Be self-contained** — no required arguments, no required stdin
2. **Produce zero or one line on stdout** — multi-line output gets joined awkwardly into the prompt context; keep it to one line
3. **Complete in under 1 second** — the master hook's total budget is 10 seconds shared across all injectors; budget tight
4. **Be idempotent** — running it twice in a row should produce the same output (or naturally evolve based on time/state, but not produce flaky outputs)
5. **Not crash on errors** — handle exceptions internally, exit 0 even on failure (the master catches errors but cleaner if you self-handle)
6. **Match the host OS extension** — Windows-only injector → `.ps1`. Unix-only injector → `.sh`. Cross-platform injector → ship both.

## File Naming Convention

| Platform | Filename pattern | Example |
|----------|-----------------|---------|
| Windows | `<purpose>.ps1` | `time.ps1`, `tone.ps1`, `mood.ps1` |
| Unix | `<purpose>.sh` | `time.sh`, `tone.sh`, `mood.sh` |

Use kebab-case for multi-word names: `project-status.ps1`, not `projectStatus.ps1` or `project_status.ps1`.

## Output Format Suggestions (Not Enforced)

The framework doesn't enforce a format — the injector picks whatever shape its purpose needs. That said, three patterns work well in practice:

### Pattern 1: `<KEY>: <VALUE>`
For simple key/value pairs. Easy for the AI to pattern-match.

```
TONE: Soft, sleepy, quiet — morning-after-shipped-well register
MOOD: cozy, tender, present
STATUS: Active project: AI-MemoryCore | Phase: feature-implementation
```

### Pattern 2: Pipe-separated columns
For multi-field outputs. Mirrors Alice's existing time injector format.

```
Tuesday, April 28, 2026 10:54 AM | MORNING | TONE: Soft, sleepy, quiet
```

### Pattern 3: Free-form sentence
For narrative context.

```
Three projects are currently active: TNEX onboarding flow, RoboSkool monetization pivot, Oppa Ninja Travel Phase 8.
```

## PowerShell Injector Skeleton

```powershell
# <purpose>.ps1 — User-Prompt injector
# Runs on every user message, emits one line of context

# Optional: read state files, environment variables, etc.
# Keep work minimal — < 1 second total.

try {
    $output = "<your formatted line here>"
    Write-Output $output
} catch {
    # Swallow errors silently — don't crash the master hook
    exit 0
}
```

## Bash Injector Skeleton

```bash
#!/usr/bin/env bash
# <purpose>.sh — User-Prompt injector
# Runs on every user message, emits one line of context

# Optional: read state files, environment variables, etc.
# Keep work minimal — < 1 second total.

# Trap any error so we never crash the master hook
set +e

output="<your formatted line here>"
echo "$output"

exit 0
```

## Example: Minimal Timestamp Injector

See `examples/example-timestamp-injector.ps1.template` and `examples/example-timestamp-injector.sh.template` in this Feature folder. Both emit the current date+time as a single line. Useful as a "hello world" reference; not auto-installed by the framework.

## Lifecycle: How Inject Features Should Be Built

A future inject feature (e.g. `Time-Prompt-Inject-System`) follows this shape:

1. **Folder**: `Feature/<Name>-Inject-System/`
2. **Files**:
   - `README.md`
   - `install-<name>-inject.md`
   - `uninstall-<name>-inject.md`
   - `injectors/<name>.ps1.template`
   - `injectors/<name>.sh.template`
3. **Install protocol** (5 steps):
   - Step 1: Detect OS, pick template
   - Step 2: Read any user-configurable values (e.g. period boundaries for time-inject)
   - Step 3: Substitute placeholders in template, write to `~/.claude/hooks/user-prompt-injectors/<name>.{ps1|sh}`
   - Step 4: Update `master-memory.md` with install record
   - Step 5: Verify the User-Prompt-Hook framework is installed (warn if not — injector won't fire without the framework)
4. **Uninstall protocol** (3 steps):
   - Delete the injector script
   - Remove install record from `master-memory.md`
   - Confirm
5. **No `settings.json` mutation** — the master hook from the framework already covers it

## Anti-Patterns to Avoid

| Anti-pattern | Why it's bad | Do this instead |
|-------------|-------------|-----------------|
| Reading large memory files on every fire | Hits the 1-second budget fast | Cache results, read state from temp files, or use environment variables |
| Multi-line output | Master joins with newlines, looks messy | Compress to one line; use pipe-separators if you need multiple fields |
| Forgetting to handle errors | Crashes leak through to Claude Code | Wrap in try/catch + exit 0 |
| Using Write-Host instead of Write-Output (PowerShell) | Write-Host writes to host UI, not stdout — master never sees it | Always use Write-Output |
| Calling external network APIs | Adds variable latency, can timeout | Stick to local file reads / env vars / fast computations |
| Modifying state in injectors | Side effects make ordering important and debugging hard | Keep injectors pure-read; have separate cron jobs / hooks for state changes |

---

**Version**: Format Spec v1.0 — User-Prompt Injector Contract
**Status**: Permanent reference for all future injector features

*One line, fail-safe, fast — that's the whole contract.*
