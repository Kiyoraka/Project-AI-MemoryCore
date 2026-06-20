---
name: image-generation
description: MUST use when the user wants to RENDER or GENERATE an actual image from a description (not just craft prompt text). Triggers on "render an image", "render this", "generate image", "render image", "make an image of", "render the prompt", "render this prompt". Builds the prompt from what the user types (subject-agnostic, no built-in persona), optionally pulls a saved reference from the Library System, confirms cost, then calls the OpenAI gpt-image API and saves a PNG.
---

# Image Generation System — Render descriptions into real PNGs

## Overview

This skill renders an actual image by calling the OpenAI gpt-image API. It is the rendering
companion to the Image Prompt System (which only crafts prompt text). The skill is **subject-
agnostic**: it builds the prompt from whatever the user types and has **no built-in character,
persona, or stored identity**. Whatever the user describes is what gets drawn.

## Protocol

1. **Extract from user input.** Read the user's typed description and pull out the subject, scene,
   style, mood, and any composition cues. The prompt is built *from their words only* — never from a
   stored character profile, an "appearance" file, a current outfit, or any baked-in identity.

2. **(Optional) Consult the Library System.** IF the Library System feature is installed AND the user
   references a saved entry (e.g. *"use my cyberpunk preset"*, *"render with my forest-scene
   reference"*), read that user-authored library entry and fold it into the prompt. This is the only
   persisted source the skill ever reads, and it is 100% user-owned content — never a shipped
   persona. If no library entry is referenced, the prompt comes purely from the typed text.

3. **Build the final prompt** from step 1 (+ optional step 2) — OR, if the user pasted a ready-made
   prompt (e.g. *"render this prompt: …"* from the Image Prompt System), use it verbatim.

4. **Resolve the output path.**
   - Default folder: `media-generation/image-generation/` inside the user's memory root (created at
     install; its path is recorded in `master-memory.md`).
   - Honor an explicit `to [path]` override.
   - Sanitize the filename (strip `< > : " / \ | ? *`, lowercase, hyphenate whitespace) and append a
     `-YYYYMMDD-HHmmss.png` timestamp suffix.

5. **MANDATORY cost-confirmation gate.** Before firing any paid render, tell the user the estimated
   cost for the chosen size/quality and get a clear go-ahead. Never skip this — it spends real money.

6. **Invoke the render script** and report the result.
   - PowerShell:
     ```powershell
     & Invoke-ImageGen.ps1 -Prompt "<final prompt>" -OutFile "<resolved path>" -Size "<1024x1024|1024x1536|1536x1024>" -Quality "<low|medium|high>"
     ```
   - Bash:
     ```bash
     invoke-image-gen.sh --prompt "<final prompt>" --outfile "<resolved path>" --size "<size>" --quality "<quality>"
     ```
   - Report back the `saved_path`, the cost estimate, and elapsed time.

## Size & Quality Reference

| Size | Orientation | Quality tiers |
|------|-------------|---------------|
| `1024x1024` | Square | low / medium / high |
| `1024x1536` | Portrait | low / medium / high |
| `1536x1024` | Landscape | low / medium / high |

Higher quality = higher cost. Default to `medium` unless the user asks otherwise.

## Mandatory Rules

1. **Build prompts only from user input** (plus optional user-owned Library entries). The feature is
   subject-agnostic — no baked-in character, persona, or appearance.
2. **Always confirm the cost** before a paid render (Step 5). No silent paid calls.
3. **Always save into `media-generation/image-generation/`** unless the user overrides with a path.
4. **Never commit `.env`**, never print the API key, never include the key in any output.
5. **Surface sanitized errors** (the scripts strip `sk-` patterns). Never auto-retry a failed render
   — API errors (moderation, quota, malformed) need human diagnosis.
