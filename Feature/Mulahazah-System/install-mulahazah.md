# Install Mulahazah
*Two paths to install the Mulahazah instinct learning system*

---

## Prerequisites

- Claude Code installed and configured
- `jq` installed (`apt install jq` / `brew install jq`)
- `sha256sum` available (standard on Linux; `gsha256sum` on macOS via coreutils)
- Bash 4.0+

---

## Path 1: npx (Recommended)

The npm installer handles everything — directory creation, script download, hook configuration, and command setup.

```bash
npx continuous-improve-skill --target claude
```

That's it. The installer will:
1. Create `~/.claude/mulahazah/` directory structure
2. Fetch `observe.sh`, `analyze.sh`, and observer scripts from GitHub
3. Wire up `PreToolUse`/`PostToolUse` hooks in `~/.claude/settings.json`
4. Install `/continuous-improve` command to `~/.claude/commands/`
5. Initialize `rules.md` and `projects.json`

**Verify the install:**
```bash
# Check hook script exists and is executable
ls -la ~/.claude/mulahazah/observe.sh

# Check analysis script
ls -la ~/.claude/mulahazah/bin/analyze.sh

# Confirm hooks are in settings.json
cat ~/.claude/settings.json | grep mulahazah
```

Then restart Claude Code and run `/continuous-improve` after a few tool calls.

---

## Path 2: Manual Install

Use this path if you prefer to inspect each script before running it, or if npx is unavailable.

All scripts are fetched from:
`https://raw.githubusercontent.com/naimkatiman/continuous-improve-skill/main/`

### Step 1: Create Directory Structure

```bash
mkdir -p ~/.claude/mulahazah/bin
mkdir -p ~/.claude/mulahazah/agents
mkdir -p ~/.claude/mulahazah/projects
mkdir -p ~/.claude/commands
```

### Step 2: Fetch Scripts

```bash
BASE="https://raw.githubusercontent.com/naimkatiman/continuous-improve-skill/main"

# Hook (fires on every tool call)
curl -fsSL "$BASE/hooks/observe.sh" -o ~/.claude/mulahazah/observe.sh

# Analysis pipeline (Haiku extracts rules from observations)
curl -fsSL "$BASE/bin/analyze.sh" -o ~/.claude/mulahazah/bin/analyze.sh

# Background observer (optional)
curl -fsSL "$BASE/agents/observer-loop.sh" -o ~/.claude/mulahazah/agents/observer-loop.sh
curl -fsSL "$BASE/agents/start-observer.sh" -o ~/.claude/mulahazah/agents/start-observer.sh
curl -fsSL "$BASE/agents/observer.md" -o ~/.claude/mulahazah/agents/observer.md

# /continuous-improve command
curl -fsSL "$BASE/commands/continuous-improve.md" -o ~/.claude/commands/continuous-improve.md
```

### Step 3: Make Scripts Executable

```bash
chmod +x ~/.claude/mulahazah/observe.sh
chmod +x ~/.claude/mulahazah/bin/analyze.sh
chmod +x ~/.claude/mulahazah/agents/observer-loop.sh
chmod +x ~/.claude/mulahazah/agents/start-observer.sh
```

### Step 4: Copy config.json

```bash
cp Feature/Mulahazah-System/config.json ~/.claude/mulahazah/config.json
```

Default configuration:
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

Adjust `run_interval_minutes` and `min_observations_to_analyze` to your preference.

### Step 5: Initialize Data Files

```bash
touch ~/.claude/mulahazah/rules.md
echo '{}' > ~/.claude/mulahazah/projects.json
```

### Step 6: Configure Hooks in settings.json

Open `~/.claude/settings.json` (create it if it does not exist) and add the following under the `hooks` key:

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

If you already have hooks configured, merge these entries — do not replace existing hooks. The hook always exits 0 and completes in under 50ms.

### Step 7 (Optional): Start the Background Observer

```bash
bash ~/.claude/mulahazah/agents/start-observer.sh
```

The observer wakes every 5 minutes and runs analysis when 20+ observations are accumulated. To check status:
```bash
cat ~/.claude/mulahazah/observer.pid   # PID of running observer
tail -f ~/.claude/mulahazah/observer.log
```

---

## Verification

Restart Claude Code and perform a few tool calls. Then verify:

```bash
# Observations directory should appear
ls ~/.claude/mulahazah/projects/

# After your first session, a hash directory should exist:
# ~/.claude/mulahazah/projects/<12-char-hash>/observations.jsonl

# Check observation count
wc -l ~/.claude/mulahazah/projects/*/observations.jsonl
```

Run the main command from within Claude Code:
```
/continuous-improve
```

Or ask directly:
```
what have you learned
```

---

## Troubleshooting

**Observations not being written:**
- Verify `observe.sh` is executable: `ls -la ~/.claude/mulahazah/observe.sh`
- Verify hooks are in `~/.claude/settings.json`: `cat ~/.claude/settings.json | grep mulahazah`
- Test manually: `echo '{"tool_name":"Bash","session_id":"test"}' | bash ~/.claude/mulahazah/observe.sh`

**analyze.sh not extracting rules:**
- Check minimum observation threshold (default: 5 for analyze.sh, 20 for background observer)
- Run manually: `bash ~/.claude/mulahazah/bin/analyze.sh`
- Verify `claude` CLI is in PATH: `which claude`

**rules.md not being created:**
- Run `/continuous-improve` after some tool calls
- Verify analyze.sh is executable: `ls -la ~/.claude/mulahazah/bin/analyze.sh`

**jq not found:**
- Ubuntu/Debian: `sudo apt install jq`
- macOS: `brew install jq`

---

*Mulahazah v2.0 — install protocol*
