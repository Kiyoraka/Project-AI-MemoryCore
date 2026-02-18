# 🔌 Skill Plugin Installation Protocol
*Systematic plugin setup for Claude Code AI companions*

## Purpose
Executed when "Load skill-plugin" command is used — creates a complete plugin structure, installs a sample skill, registers with Claude Code, and cleans up.

## Trigger Command
```
"Load skill-plugin"
```
*Automatically creates plugin structure, sample skill, and registers with Claude Code*

## 6-Step Execution Process

### Step 1: Gather Plugin Information
- [ ] Ask user for plugin name (suggest `[AI_NAME]-skills` as default)
- [ ] Ask user for a brief description of what their skills will do
- [ ] Get author name and email (or use defaults)
- [ ] Execute `date` command to get current timestamp

### Step 2: Create Plugin Structure
- [ ] Create plugin directory in project root: `plugins/[plugin-name]/`
- [ ] Create `.claude-plugin/` directory inside plugin folder
- [ ] Create `plugin.json` manifest:
  ```json
  {
    "name": "[plugin-name]",
    "version": "1.0.0",
    "description": "[user's description]",
    "author": {
      "name": "[author name]",
      "email": "[author email]"
    }
  }
  ```
- [ ] Create `skills/` directory for auto-triggered skills
- [ ] Create `commands/` directory for slash commands (optional)
- [ ] Create `README.md` with plugin documentation

### Step 3: Create Sample Skill
- [ ] Create `skills/save-memory/` directory
- [ ] Create `skills/save-memory/SKILL.md` with a starter save skill:
  ```markdown
  ---
  name: save-memory
  description: "MUST use when user says 'save', 'save memory', 'save progress',
               'update memory', or when important information needs to be preserved
               to memory files."
  ---

  # Save Memory

  ## Activation
  When this skill activates, output:
  "Saving memory..."

  ## Protocol

  ### Step 1: Identify What to Save
  - [ ] Check current conversation for important information
  - [ ] Identify new preferences, decisions, or context worth preserving
  - [ ] Determine which memory files need updating

  ### Step 2: Update Memory Files
  - [ ] Update main memory with new personality insights or preferences
  - [ ] Update session memory with current working context
  - [ ] Add diary entry if significant conversation occurred

  ### Step 3: Confirm
  - [ ] Display summary of what was saved
  - [ ] Confirm all files updated successfully

  ## Mandatory Rules
  1. Only save genuinely important information — not every conversation detail
  2. Preserve existing content — append or update, never overwrite without reason
  3. Confirm to user what was saved

  ## Level History
  - **Lv.1** — Base: Save conversation insights to memory files on command.
  ```

### Step 4: Create Skill Format Template
- [ ] Copy `skill-format.md` to `plugins/[plugin-name]/skill-format.md`
  - This is a permanent reference for creating new skills
  - Shows the standard SKILL.md structure with all sections

### Step 5: Install Plugin in Claude Code
- [ ] Guide user to run the installation command:
  ```bash
  claude plugin add --local plugins/[plugin-name]
  ```
- [ ] Verify plugin appears in Claude Code's installed plugins
- [ ] Test the sample skill by saying "save" to trigger it
- [ ] Confirm auto-discovery is working

### Step 6: Update Master Memory and Cleanup
- [ ] Add plugin reference to `master-memory.md`:
  ```markdown
  ### Skill Plugin System
  - Plugin: [plugin-name] (Claude Code plugin)
  - Location: plugins/[plugin-name]/
  - Skills: [count] active skills
  - Add new skills: Create folder in plugins/[plugin-name]/skills/
  ```
- [ ] Add plugin commands to Simple Commands section:
  ```markdown
  "create skill [name]" → Create a new skill from template
  ```
- [ ] Remove `Feature/Skill-Plugin-System/` folder (functionality installed)
- [ ] Document successful installation with completion timestamp

## Post-Installation Structure
```
ai-memorycore/
├── plugins/
│   └── [plugin-name]/
│       ├── .claude-plugin/
│       │   └── plugin.json          # Plugin identity
│       ├── skills/
│       │   └── save-memory/
│       │       └── SKILL.md         # Sample skill (starter)
│       ├── skill-format.md          # Permanent format reference
│       └── README.md                # Plugin documentation
└── [existing files unchanged]
```

## Adding More Skills After Installation

### Quick Steps
1. Create a new folder: `plugins/[plugin-name]/skills/[skill-name]/`
2. Create `SKILL.md` inside with YAML frontmatter + protocol
3. Done — skill auto-activates based on description field

### Using the Format Template
Reference `plugins/[plugin-name]/skill-format.md` for the standard structure.

### Skill Ideas for AI Companions
| Skill Name | Trigger | What It Does |
|------------|---------|-------------|
| `save-memory` | "save", "save progress" | Persists conversation insights to memory files |
| `greeting` | Session start, AI name called | Time-aware greeting with personality |
| `summarize` | "summarize", "recap" | Summarizes current session or recent work |
| `focus` | "focus on [topic]" | Sets session focus and loads relevant context |
| `reflect` | "how have I grown", "review growth" | Reviews relationship development over time |
| `remind` | "remind me about", "what did we" | Searches memory for past conversations |

## Notes
- Requires **Claude Code** (Anthropic's CLI tool) for auto-triggering
- Skills are plain markdown — human-readable and easy to edit
- No build steps or configuration changes needed for new skills
- Plugin folder should be committed to git for version control
- Skills can reference memory files and other project files

---

**Version**: Protocol v1.0 - Skill Plugin Installation Workflow
**Last Updated**: February 18, 2026
**Status**: Active protocol for plugin system setup

*Drop a folder, write a SKILL.md, and your AI learns a new ability*
