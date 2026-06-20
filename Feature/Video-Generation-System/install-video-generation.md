# Video Generation System Installation Protocol
*Setup for rendering MP4 video from descriptions via the Seedance API*

## Purpose
Executed when "Load video-generation" is used — enables your AI to render an actual MP4 from a typed
description (text-to-video) or animate a local image (image-to-video) by calling the Seedance API
(BytePlus ModelArk). The prompt is always built from what the user types; there is no built-in
subject or persona.

## Trigger Command
```
"Load video-generation"
```

## Prerequisites
- A **BytePlus ModelArk account + API key** (`ARK_API_KEY`)
- **PowerShell** (Windows) *or* **bash + `curl` + `jq`** (Mac/Linux/Git Bash)
- Core memory system installed (`main/` directory, `master-memory.md` accessible)
- Skill Plugin System recommended for auto-triggering (optional)
- *(Optional)* Image Generation System — generate a still, then animate it here
- *(Optional)* Library System — pull saved style/subject references into a render

## Installation Steps

### Step 1: Install the render script
- [ ] Pick your platform script from `scripts/`:
  - Windows → `Invoke-VideoGen.ps1.template`
  - Mac/Linux/Git Bash → `invoke-video-gen.sh.template`
- [ ] Copy it to a folder on your PATH and **remove the `.template` suffix** (so it becomes
  `Invoke-VideoGen.ps1` / `invoke-video-gen.sh`). For bash, also `chmod +x invoke-video-gen.sh` and
  confirm `curl` + `jq` are installed.

### Step 2: Set up credentials
- [ ] Follow `credential-setup.md`: copy `.env.example` → `.env`, paste your real `ARK_API_KEY`, and
  **add `.env` to your `.gitignore`**. (Or set the `ARK_API_KEY` environment variable.)
- [ ] Confirm the key resolves (the script errors clearly if it can't find one).

### Step 3: Create the output folder
- [ ] Create **`media-generation/video-generation/`** inside your own memory root — this is the
  single fixed home for every rendered clip.
- [ ] Record its path in `master-memory.md` so the skill always resolves the same default output
  location:
  ```markdown
  ### Video Generation Output
  - **Folder**: media-generation/video-generation/  (all rendered MP4s land here)
  ```

### Step 4: Register the skill
- [ ] If the Skill Plugin System exists:
  - Copy `SKILL.md` to `plugins/[plugin-name]/skills/video-generation/SKILL.md`
  - Inform user: "Video Generation skill installed — auto-triggers on 'render a video', 'generate video', 'animate this image'"
- [ ] If it does NOT exist:
  - Inform user: "Video Generation integrated into master memory. Install the Skill Plugin System for auto-triggering."

### Step 5: Update memory system
- [ ] Add to `master-memory.md`:
  ```markdown
  ### Video Generation
  *Render MP4 video from descriptions via the Seedance API (BytePlus ModelArk)*
  - **Trigger**: "render a video", "generate video", "animate this image"
  - **What it does**: Builds a prompt from what you type (no built-in persona), supports text-to-video and image-to-video, confirms cost, runs the async submit/poll/download flow, saves an MP4 to media-generation/video-generation/
  - **Companion**: Image Generation (animate a still), Image Prompt System (craft the prompt), Library System (optional saved references)
  ```

## Post-Installation
- [ ] **Dry-run first (no spend):** `"render a video of a sunset over mountains"` — when the cost
  estimate appears (via `-WhatIfCost`), confirm the wiring works *before* approving a real render.
- [ ] Then approve one short **480p** clip and confirm the MP4 lands in
  `media-generation/video-generation/`.
- [ ] Confirm the cost-confirmation prompt always appears before rendering.
- [ ] Confirm the API key is never printed in any output.

## Installation Complete
Your AI can now render real video from any description you type — and animate your own stills —
saving every clip to one tidy folder.

> **Note:** This install file is intentionally kept in place (not self-deleted) so the feature stays
> readable across tools and contributors.
