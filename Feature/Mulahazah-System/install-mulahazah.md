# Mulahazah Installation Protocol
*Systematic setup for behavioral learning from session observations*

## Purpose

Executed when setting up the Mulahazah instinct learning system -- creates directory infrastructure, wires hooks into Claude Code, fetches analysis scripts, and activates the `/continuous-improvement` command. After installation, your AI companion silently observes every tool call and learns from the patterns.

## Trigger Command

```
npx continuous-improvement install --target claude
```

*Or follow the manual path below if you prefer to inspect each script before running.*

## Prerequisites

- Claude Code installed and configured
- `jq` installed (`apt install jq` / `brew install jq`)
- `sha256sum` available (standard on Linux; `gsha256sum` on macOS via coreutils)
- Bash 4.0+

## 7-Step Installation Process

### Step 1: Run the npx Installer (Recommended)

- [ ] Execute: `npx continuous-improvement install --target claude`
- [ ] The installer creates `~/.claude/mulahazah/` directory structure
- [ ] Fetches `observe.sh`, `analyze.sh`, and observer scripts from GitHub
- [ ] Wires `PreToolUse`/`PostToolUse` hooks in `~/.claude/settings.json`
- [ ] Installs `/continuous-improvement` command to `~/.claude/commands/`
- [ ] Initializes `rules.md` and `projects.json`

### Step 2: Create Directory Structure (Manual Path)

- [ ] Run:
  ```bash
  mkdir -p ~/.claude/mulahazah/bin
  mkdir -p ~/.claude/mulahazah/agents
  mkdir -p ~/.claude/mulahazah/projects
  mkdir -p ~/.claude/commands
  ```

### Step 3: Fetch Scripts (Manual Path)

- [ ] Run:
  ```bash
  BASE="https://raw.githubusercontent.com/naimkatiman/continuous-improvement/main"

  curl -fsSL "$BASE/hooks/observe.sh"        -o ~/.claude/mulahazah/observe.sh
  curl -fsSL "$BASE/bin/analyze.sh"          -o ~/.claude/mulahazah/bin/analyze.sh
  curl -fsSL "$BASE/agents/observer-loop.sh" -o ~/.claude/mulahazah/agents/observer-loop.sh
  curl -fsSL "$BASE/agents/start-observer.sh" -o ~/.claude/mulahazah/agents/start-observer.sh
  curl -fsSL "$BASE/agents/observer.md"      -o ~/.claude/mulahazah/agents/observer.md
  curl -fsSL "$BASE/commands/continuous-improvement.md" -o ~/.claude/commands/continuous-improvement.md
  ```

### Step 4: Make Scripts Executable (Manual Path)

- [ ] Run:
  ```bash
  chmod +x ~/.claude/mulahazah/observe.sh
  chmod +x ~/.claude/mulahazah/bin/analyze.sh
  chmod +x ~/.claude/mulahazah/agents/observer-loop.sh
  chmod +x ~/.claude/mulahazah/agents/start-observer.sh
  ```

### Step 5: Copy Config and Initialize Data Files (Manual Path)

- [ ] Copy config: `cp Feature/Mulahazah-System/config.json ~/.claude/mulahazah/config.json`
- [ ] Initialize: `touch ~/.claude/mulahazah/rules.md && echo '{}' > ~/.claude/mulahazah/projects.json`

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

### Step 6: Configure Hooks in settings.json (Manual Path)

- [ ] Open `~/.claude/settings.json` and add the following under the `hooks` key:
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
- [ ] If you already have hooks configured, merge these entries -- do not replace existing hooks

### Step 7: Verify Installation

- [ ] Restart Claude Code
- [ ] Perform a few tool calls
- [ ] Check observations directory: `ls ~/.claude/mulahazah/projects/`
- [ ] Check observation count: `wc -l ~/.claude/mulahazah/projects/*/observations.jsonl`
- [ ] Run `/continuous-improvement` or ask "what have you learned"

## Installation Complete Message

```
Mulahazah installed successfully.

  Hooks: PreToolUse + PostToolUse → observe.sh
  Analysis: ~/.claude/mulahazah/bin/analyze.sh (Haiku-powered)
  Rules: ~/.claude/mulahazah/rules.md (persistent across sessions)
  Command: /continuous-improvement

Restart Claude Code to activate observation.
After a few tool calls, run /continuous-improvement to extract your first rules.
```

## What This System Does

1. Silently captures every tool call as structured JSONL -- no performance impact
2. Accumulates observations per project in `~/.claude/mulahazah/projects/<hash>/`
3. On `/continuous-improvement` -- sends observations to Haiku for pattern extraction
4. Writes extracted rules to `rules.md` -- your AI reads them next session
5. Optional background observer auto-analyzes every 5 minutes when 20+ observations exist

## Notes

- The hook always exits 0 and completes in under 50ms -- it never blocks Claude Code
- Rules decay without reinforcement -- rules that stop being observed are candidates for removal
- To start the background observer: `bash ~/.claude/mulahazah/agents/start-observer.sh`
- To check observer status: `cat ~/.claude/mulahazah/observer.pid`
- To troubleshoot hooks: `cat ~/.claude/settings.json | grep mulahazah`

---

**Version**: Protocol v1.0

*Your AI companion gets wiser with every session -- one rule at a time.*
