# Interactive Story System Installation Protocol
*Setup for Visual Novel RPG adventures with your AI companion*

## Purpose
Executed when "Load interactive-story" command is used -- enables your AI to run interactive VN RPG adventures with world generation, cinematic combat, and persistent story saving.

## Trigger Command
```
"Load interactive-story"
```
*Enables AI-powered interactive storytelling with VN RPG mechanics*

## Prerequisites
- Core memory system installed (`main/` directory with essential files)
- `master-memory.md` accessible for integration updates
- Skill Plugin System recommended for full auto-triggering (optional but enhances experience)

## 3-Step Installation Process

### Step 1: Install Interactive Story Skill
- [ ] If Skill Plugin System exists:
  - Copy `SKILL.md` to `plugins/[plugin-name]/skills/interactive-story/SKILL.md`
  - Inform user: "Interactive Story skill installed -- auto-triggers on 'new adventure', 'load adventure', 'resume adventure'"
- [ ] If Skill Plugin System does NOT exist:
  - Inform user: "Interactive Story integrated into master memory. Install the Skill Plugin System for auto-triggering."
  - Add interactive story protocol reference to `master-memory.md`

### Step 2: Create Adventure Directory
- [ ] Create `adventures/` directory in project root for adventure storage:
  ```
  adventures/
  └── (adventures will be saved here)
  ```
- [ ] Add to `master-memory.md`:
  ```markdown
  ### Interactive Story
  *Visual Novel RPG adventure system*
  - **Trigger**: "new adventure", "save adventure", "load adventure", "end adventure"
  - **What it does**: Runs interactive VN RPG adventures with world generation and cinematic combat
  - **Modes**: Duo (with AI companion) / Solo (AI as DM) | OP / Balanced
  - **Storage**: `adventures/[world-name]/` with setting.md, summary.md, and story/
  ```

### Step 3: Configure Preferences (Optional)
- [ ] Ask user: "Default play mode?" → Duo or Solo
- [ ] Ask user: "Default power level?" → OP or Balanced
- [ ] Ask user: "Would you like to define your hero character now?"
  - If YES, collect: Character name, preferred class/archetype, special abilities
  - Save to master memory under `## Hero Profile`
  - If NO, inform: "No problem! You'll choose your character at the start of each adventure."

## Optional Companion Systems
- [ ] **Image Prompt System**: Install for NijiJourney/Midjourney scene art during adventures
- [ ] **Song Creation System**: Install for Opening/Ending songs on new/end adventure
- [ ] **Auto-Commit System**: Install for auto-committing adventure files on save/end

## Post-Installation
- [ ] Test with: "new adventure"
- [ ] Choose play mode, power level, and world type
- [ ] Play through a few scenes to verify VN format and combat work
- [ ] Test save with: "save adventure"
- [ ] Test resume with: "load adventure"
- [ ] Delete this installation file: `rm install-interactive-story.md`

## Installation Complete
Your AI can now run interactive VN RPG adventures. Say "new adventure" to begin!
