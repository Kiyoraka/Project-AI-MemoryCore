# Image Generation System Installation Protocol
*Setup for rendering images from descriptions via the OpenAI gpt-image API*

## Purpose
Executed when "Load image-generation" is used — enables your AI to render an actual PNG from a
typed description by calling the OpenAI gpt-image API. The prompt is always built from what the user
types; there is no built-in subject or persona.

## Trigger Command
```
"Load image-generation"
```

## Prerequisites
- An **OpenAI account + API key** with image access
- **PowerShell** (Windows) *or* **bash + `curl` + `jq`** (Mac/Linux/Git Bash)
- Core memory system installed (`main/` directory, `master-memory.md` accessible)
- Skill Plugin System recommended for auto-triggering (optional)
- *(Optional)* Library System — lets users pull saved style/subject references into a render

## Installation Steps

### Step 1: Install the render script
- [ ] Pick your platform script from `scripts/`:
  - Windows → `Invoke-ImageGen.ps1.template`
  - Mac/Linux/Git Bash → `invoke-image-gen.sh.template`
- [ ] Copy it to a folder on your PATH and **remove the `.template` suffix** (so it becomes
  `Invoke-ImageGen.ps1` / `invoke-image-gen.sh`). For bash, also `chmod +x invoke-image-gen.sh`.

### Step 2: Set up credentials
- [ ] Follow `credential-setup.md`: copy `.env.example` → `.env`, paste your real `OPENAI_API_KEY`,
  and **add `.env` to your `.gitignore`**. (Or set the `OPENAI_API_KEY` environment variable.)
- [ ] Confirm the key resolves (the script errors clearly if it can't find one).

### Step 3: Create the output folder
- [ ] Create **`media-generation/image-generation/`** inside your own memory root — this is the
  single fixed home for every rendered image.
- [ ] Record its path in `master-memory.md` so the skill always resolves the same default output
  location:
  ```markdown
  ### Image Generation Output
  - **Folder**: media-generation/image-generation/  (all rendered PNGs land here)
  ```

### Step 4: Register the skill
- [ ] If the Skill Plugin System exists:
  - Copy `SKILL.md` to `plugins/[plugin-name]/skills/image-generation/SKILL.md`
  - Inform user: "Image Generation skill installed — auto-triggers on 'render an image', 'generate image', 'render this prompt'"
- [ ] If it does NOT exist:
  - Inform user: "Image Generation integrated into master memory. Install the Skill Plugin System for auto-triggering."

### Step 5: Update memory system
- [ ] Add to `master-memory.md`:
  ```markdown
  ### Image Generation
  *Render images from descriptions via the OpenAI gpt-image API*
  - **Trigger**: "render an image", "generate image", "render this prompt"
  - **What it does**: Builds a prompt from what you type (no built-in persona), confirms cost, calls the API, saves a PNG to media-generation/image-generation/
  - **Companion**: Image Prompt System (craft the prompt), Library System (optional saved references)
  ```

## Post-Installation
- [ ] Smoke test: `"render an image of a sunset over mountains"`
- [ ] Confirm the cost-confirmation prompt appears before rendering
- [ ] Confirm the PNG lands in `media-generation/image-generation/`
- [ ] Confirm the API key is never printed in any output

## Installation Complete
Your AI can now render real images from any description you type, saving them to one tidy folder.

> **Note:** This install file is intentionally kept in place (not self-deleted) so the feature stays
> readable across tools and contributors.
