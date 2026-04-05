# Install Mulahazah
*Step-by-step installation protocol for the Mulahazah instinct learning system*

---

## Prerequisites

- Claude Code installed and configured
- `jq` installed (`apt install jq` / `brew install jq`)
- `sha256sum` available (standard on Linux; `gsha256sum` on macOS via coreutils)
- Bash 4.0+

---

## Step 1: Create the Mulahazah Directory Structure

```bash
mkdir -p ~/.claude/mulahazah/projects
mkdir -p ~/.claude/mulahazah/instincts/global
```

This creates the root directory where all observations, instincts, and configuration will live.

---

## Step 2: Copy observe.sh and Make It Executable

Copy the observation hook from this feature directory:

```bash
cp Feature/Mulahazah-System/hooks/observe.sh ~/.claude/mulahazah/observe.sh
chmod +x ~/.claude/mulahazah/observe.sh
```

Verify it is executable:

```bash
ls -la ~/.claude/mulahazah/observe.sh
# Should show: -rwxr-xr-x
```

---

## Step 3: Configure Hooks in settings.json

Open `~/.claude/settings.json` (create it if it does not exist) and add the following hook entries under the `hooks` key:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/mulahazah/observe.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/mulahazah/observe.sh"
          }
        ]
      }
    ]
  }
}
```

If you already have hooks configured, merge the new entries with your existing configuration — do not replace existing hooks.

**Important:** The hook always exits 0 and completes in under 50ms. It will never block or slow down your Claude session.

---

## Step 4: Copy Observer Agent Files

Copy the background observer scripts:

```bash
mkdir -p ~/.claude/mulahazah/agents
cp Feature/Mulahazah-System/agents/observer.md ~/.claude/mulahazah/agents/
cp Feature/Mulahazah-System/agents/observer-loop.sh ~/.claude/mulahazah/agents/
cp Feature/Mulahazah-System/agents/start-observer.sh ~/.claude/mulahazah/agents/
chmod +x ~/.claude/mulahazah/agents/observer-loop.sh
chmod +x ~/.claude/mulahazah/agents/start-observer.sh
```

---

## Step 4b: Copy bin/analyze.sh

This is the actual analysis pipeline. It reads observations and calls Haiku to extract rules.

```bash
mkdir -p ~/.claude/mulahazah/bin
cp Feature/Mulahazah-System/bin/analyze.sh ~/.claude/mulahazah/bin/analyze.sh
chmod +x ~/.claude/mulahazah/bin/analyze.sh
```

Verify it is executable:

```bash
ls -la ~/.claude/mulahazah/bin/analyze.sh
# Should show: -rwxr-xr-x
```

---

## Step 4c: Copy the /continuous-improve command

```bash
mkdir -p ~/.claude/commands
cp Feature/Mulahazah-System/commands/continuous-improve.md ~/.claude/commands/continuous-improve.md
```

This enables the `/continuous-improve` command in Claude Code, which triggers reflection + analysis + status in one step.

---

## Step 4d: Initialize rules.md

Create the rules file that will accumulate learned behaviors:

```bash
touch ~/.claude/mulahazah/rules.md
```

On first install, this file is empty. Rules are appended automatically when you run `/continuous-improve` or when the background observer runs. You can also add rules manually.

---

## Step 5: Copy config.json

```bash
cp Feature/Mulahazah-System/config.json ~/.claude/mulahazah/config.json
```

The default configuration:

```json
{
  "version": "2.0",
  "observer": {
    "enabled": true,
    "run_interval_minutes": 5,
    "min_observations_to_analyze": 20,
    "model": "haiku"
  }
}
```

You can adjust `run_interval_minutes` (default: 5) and `min_observations_to_analyze` (default: 20) to your preference.

---

## Step 6: Initialize the Projects Registry

```bash
echo '{}' > ~/.claude/mulahazah/projects.json
```

This creates the global project registry. It will be populated automatically as you work in different projects.

---

## Step 7 (Optional): Start the Background Observer

To enable automatic pattern detection, start the background observer:

```bash
bash ~/.claude/mulahazah/agents/start-observer.sh
```

Expected output:
```
Mulahazah observer started.

Mulahazah observer is running (PID 12345)

  Force immediate analysis:  kill -USR1 12345
  Stop observer:             kill 12345
  View logs:                 tail -f ~/.claude/mulahazah/observer.log
  PID file:                  ~/.claude/mulahazah/observer.pid
```

The observer will wait until at least 20 observations have been collected before running its first analysis (configurable via `min_observations_to_analyze`).

---

## Verification

Restart Claude Code and run a few tool calls. Then verify observations are being recorded:

```bash
# Check if observations are being written
ls ~/.claude/mulahazah/projects/

# After your first project session, a hash directory should appear:
# ~/.claude/mulahazah/projects/<12-char-hash>/

# Check observation count
wc -l ~/.claude/mulahazah/projects/*/observations.jsonl
```

To trigger reflection + analysis + rule status from within Claude Code:
```
/continuous-improve
```

Or ask directly:
```
what have you learned
```

---

## Directory Reference (After Install)

```
~/.claude/mulahazah/
├── config.json                    # Observer configuration
├── observe.sh                     # PreToolUse/PostToolUse hook
├── rules.md                       # Learned rules (grows over sessions)
├── projects.json                  # Global project registry
├── observer.pid                   # Background observer PID (after start)
├── observer.log                   # Observer run log (after start)
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
        └── observations.archive/  # Rotated log archives

~/.claude/commands/
└── continuous-improve.md          # /continuous-improve command
```

---

## Troubleshooting

**Observations not being written:**
- Verify `observe.sh` is executable: `ls -la ~/.claude/mulahazah/observe.sh`
- Verify hooks are configured in `~/.claude/settings.json`
- Test the hook manually: `echo '{"tool_name":"Bash","session_id":"test"}' | bash ~/.claude/mulahazah/observe.sh`

**analyze.sh not extracting rules:**
- Check minimum observation threshold: default is 5 observations for analyze.sh, 20 for background observer
- Run analyze.sh manually: `bash ~/.claude/mulahazah/bin/analyze.sh`
- Check observer logs: `tail -20 ~/.claude/mulahazah/observer.log`
- Verify `claude` CLI is in PATH: `which claude`

**rules.md not being created:**
- Run `/continuous-improve` in a Claude Code session after some tool calls
- Verify `analyze.sh` is executable: `ls -la ~/.claude/mulahazah/bin/analyze.sh`
- Check that observations exist: `wc -l ~/.claude/mulahazah/projects/*/observations.jsonl`

**jq not found:**
- Install jq: `sudo apt install jq` (Ubuntu/Debian) or `brew install jq` (macOS)

---

*Mulahazah v2.0 — install protocol*
