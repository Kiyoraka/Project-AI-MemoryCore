# Image Prompt System Installation Protocol
*Setup for AI-powered image prompt generation*

## Purpose
Executed when "Load image-prompt" command is used -- enables your AI to generate optimized Midjourney/NijiJourney prompts for any subject with composition-aware framing.

## Trigger Command
```
"Load image-prompt"
```
*Enables AI image prompt generation with shot composition guide*

## Prerequisites
- Core memory system installed (`main/` directory with essential files)
- `master-memory.md` accessible for integration updates
- Skill Plugin System recommended for full auto-triggering (optional but enhances experience)

## 3-Step Installation Process

### Step 1: Install Image Prompt Skill
- [ ] If Skill Plugin System exists:
  - Copy `SKILL.md` to `plugins/[plugin-name]/skills/image-prompt/SKILL.md`
  - Inform user: "Image Prompt skill installed -- auto-triggers on 'create a prompt', 'midjourney prompt', 'image prompt'"
- [ ] If Skill Plugin System does NOT exist:
  - Inform user: "Image Prompt integrated into master memory. Install the Skill Plugin System for auto-triggering."
  - Add prompt generation protocol reference to `master-memory.md`

### Step 2: Update Memory System
- [ ] Add to `master-memory.md`:
  ```markdown
  ### Image Prompt Generation
  *AI-powered prompt creation for Midjourney/NijiJourney*
  - **Trigger**: "create a prompt", "midjourney prompt", "niji prompt", "image prompt", "reference sheet"
  - **What it does**: Generates optimized image prompts with composition-aware framing
  - **Modes**: Freeform (any subject) or Character (profile-aware)
  ```

### Step 3: (Optional) Set Up Character Profile
- [ ] Ask user: "Would you like to set up a character profile for consistent character art?"
- [ ] If YES, add `## Character Appearance` section to main memory:
  ```markdown
  ## Character Appearance
  - **Hair**: [color, length, style - e.g., "long flowing dark blue hair"]
  - **Eyes**: [color, style - e.g., "bright green eyes"]
  - **Build**: [body type - e.g., "slender", "athletic"]
  - **Style**: [overall aesthetic - e.g., "anime", "semi-realistic"]
  - **Accent Color**: [character's signature color - e.g., "blue", "gold"]
  - **Default Quality**: [preferred model - e.g., "--niji 7" or "--v 7"]
  ```
- [ ] Optionally add companion character for duo scenes:
  ```markdown
  ## Companion Appearance
  - **Hair**: [description]
  - **Eyes**: [description]
  - **Build**: [description]
  - **Relationship**: [how they relate to the AI character]
  ```
- [ ] If NO, inform user: "No problem! You can always add a character profile later. Freeform mode works without one."

## Post-Installation
- [ ] Test with: "create a prompt for a sunset over mountains"
- [ ] If character profile set up, test with: "create a prompt of my character in a cafe"
- [ ] Confirm prompt outputs in code block with model flag
- [ ] Delete this installation file: `rm install-image-prompt.md`

## Installation Complete
Your AI can now generate optimized image prompts for any subject. Character mode is available if you set up a character profile.
