---
name: video-generation
description: MUST use when the user wants to RENDER or GENERATE an actual video / MP4 from a description, or ANIMATE a local image. Triggers on "render a video", "generate video", "make a video", "create a video", "animate this", "animate this image", "bring this to life". Builds the motion prompt from what the user types (subject-agnostic, no built-in persona), optionally pulls a saved reference from the Library System, supports text-to-video and image-to-video, confirms cost (video is expensive), then calls the Seedance API (async submit/poll/download) and saves an MP4.
---

# Video Generation System — Render descriptions into real MP4 video

## Overview

This skill renders an actual video by calling the Seedance API (BytePlus ModelArk) through an async
submit → poll → download flow. It is the motion companion to the Image Generation System. It is
**subject-agnostic**: it builds the prompt from whatever the user types and has **no built-in
character, persona, or stored identity**. Whatever the user describes is what gets animated.

**Video is expensive** — a single clip can cost ~$1–$3.50. The cost-confirmation gate (Step 5) is
mandatory and non-negotiable.

## Protocol

1. **Extract motion intent from user input.** Read the typed description and pull out: subject,
   scene/setting, **camera movement** (static / slow push-in / orbit / handheld / dolly / crane),
   **pacing** (calm drift vs energetic), and mood. The prompt is built *from their words only* —
   never from a stored character profile, an "appearance" file, or any baked-in identity.

2. **(Optional) Consult the Library System.** IF the Library System feature is installed AND the user
   references a saved entry (e.g. *"use my noir style"*), read that user-authored entry and fold it
   into the prompt. This is the only persisted source the skill reads, and it is 100% user-owned
   content — never a shipped persona.

3. **(Optional) Image-to-video.** IF the user wants to animate a local still (e.g. one produced by
   the Image Generation System), pass it to the helper as `-FirstFrame` (opening frame),
   `-LastFrame` (closing frame), or `-ReferenceImages` (style/subject anchors). The helper base64's
   local files automatically — no hosting needed. URLs are also accepted.

4. **Resolve the output path.**
   - Default folder: `media-generation/video-generation/` inside the user's memory root (created at
     install; its path is recorded in `master-memory.md`).
   - Honor an explicit `to [path]` override.
   - Sanitize the filename (strip `< > : " / \ | ? *`, lowercase, hyphenate whitespace) and append a
     `-YYYYMMDD-HHmmss.mp4` timestamp suffix.

5. **MANDATORY cost-confirmation gate.** Run the helper with `-WhatIfCost` (no API call) to get the
   estimate for the chosen resolution/duration. Present it clearly, **emphasizing video is pricey**,
   and get an explicit go-ahead. NEVER auto-fire a paid render.

6. **Invoke the render helper** (async submit → poll → download) and report the result.
   - PowerShell:
     ```powershell
     & Invoke-VideoGen.ps1 -Prompt "<final prompt>" -OutFile "<resolved path>" -Resolution "<480p|720p|1080p>" -Duration <seconds> -AspectRatio "16:9" [-FirstFrame "<path|url>"]
     ```
   - Bash:
     ```bash
     invoke-video-gen.sh --prompt "<final prompt>" --outfile "<resolved path>" --resolution "<res>" --duration <seconds> [--first-frame "<path|url>"]
     ```
   - Report back the `saved_path`, the cost estimate, elapsed time, and `task_id`.

## Resolution & Duration Reference

| Resolution | Indicative cost/sec (USD) | Notes |
|------------|---------------------------|-------|
| `480p` | ~$0.05 | cheapest — good for drafts/smoke tests |
| `720p` | ~$0.10 | balanced |
| `1080p` | ~$0.23 | highest quality, highest cost |

Cost ≈ rate × duration. Default to a short duration unless the user asks otherwise. **Verify current
pricing at BytePlus ModelArk** — these are indicative only.

## Mandatory Rules

1. **Build prompts only from user input** (plus optional user-owned Library entries). The feature is
   subject-agnostic — no baked-in character, persona, or appearance.
2. **Always confirm the cost** via `-WhatIfCost` before a paid render (Step 5). No silent paid calls.
   Video is expensive — never skip this.
3. **Always save into `media-generation/video-generation/`** unless the user overrides with a path.
4. **Never commit `.env`**, never print the API key, never include the key in any output.
5. **Surface sanitized errors** (the scripts strip `ark-`/`sk-` patterns). Never auto-retry a failed
   render — API errors (moderation, quota, malformed) need human diagnosis.
6. **The helper is canonical** — never inline the HTTP submit/poll/download logic in conversation;
   always call the script.
