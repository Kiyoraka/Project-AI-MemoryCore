# 🎬 Video Generation System
*Render the motion you describe into real MP4 video via the Seedance API*

---

## What It Does

The motion sibling of the **Image Generation System**. You describe a scene in plain language; this
feature builds the prompt **from your words** and renders an actual **MP4** by calling the **Seedance
API** (BytePlus ModelArk). It is fully subject-agnostic — there is no built-in character or persona.

- **Text-to-video** — describe a scene and motion, get a clip
- **Image-to-video** — animate a local still (e.g. one from the Image Generation System) as the
  first/last frame or a style reference
- **Prompt built from your input** — extracts subject, scene, camera move, pacing, and mood
- **Cross-platform** — PowerShell *and* Bash (curl + jq) render scripts
- **Cost-aware** — `-WhatIfCost` estimates before you spend; mandatory confirmation before each render
- **One tidy output folder** — every clip lands in `media-generation/video-generation/`

---

## How It Works

Seedance generation is **asynchronous** — submit a task, poll until it's ready, then download:

```
You describe a scene (+ optional local image to animate)
        │
        ▼
Prompt built from YOUR words   ──(optional)──►  pull a saved reference
(no built-in subject/persona)                   from your Library-System
        │
        ▼
 PHASE 1: SUBMIT   POST  …/contents/generations/tasks   ──►  task id
        │                 (model: dreamina-seedance-2-0-260128)
        ▼
 PHASE 2: POLL     GET   …/tasks/{id}   every 10s until succeeded/failed
        │
        ▼
 PHASE 3: DOWNLOAD  fetch the signed MP4 URL ──► media-generation/video-generation/
```

---

## Quick Start

1. Set up your BytePlus ModelArk key — see `credential-setup.md`
2. Install the render script — see `install-video-generation.md`
3. Type: `"Load video-generation"`
4. Render: `"render a video of a paper boat drifting down a rainy street"`

---

## Available Commands

| Command | Action |
|---------|--------|
| `"render a video of [description]"` | Build a prompt from your words and render a clip |
| `"generate video [description]"` | Same as above (alternative trigger) |
| `"animate this image: [path]"` | Image-to-video — animate a local still |
| `"render a video [description] to [path]"` | Render and save to a specific path |

---

## Prerequisites

- A **BytePlus ModelArk account + API key** (`ARK_API_KEY`) — see `credential-setup.md`
- **⚠️ This calls a paid API, and video is expensive.** A single clip can cost roughly
  **$1–$3.50** depending on resolution and duration. The system shows a `-WhatIfCost` estimate and
  asks for confirmation before every render. Always verify current BytePlus ModelArk pricing.
- **PowerShell** (Windows) *or* **bash + `curl` + `jq`** (Mac/Linux/Git Bash)

---

## Output Location

Every clip is saved to **`media-generation/video-generation/`** inside your own memory directory
(created during install). Filenames are sanitized and timestamped (`.mp4`). Override per-render with
`render ... to [path]`.

---

## Companion Systems

| System | Enhancement |
|--------|-------------|
| **Image Generation System** | Generate a still, then animate it here (image-to-video) |
| **Image Prompt System** | Craft a composition-aware base prompt, then render it as motion |
| **Library System** | *(optional)* Save reusable style/subject references and pull them into a render |

All companions are optional — the Video Generation System works on its own with just a typed
description.

---

## Security

Your API key is read from `$ARK_API_KEY` or a `.env` file — **never hardcoded, never committed,
never echoed**. The render scripts strip any `ark-`/`sk-` key pattern from error messages. See
`credential-setup.md` for the full key-safety checklist.

---

## Installation

See `install-video-generation.md` for step-by-step setup.

**Platform Note:** Includes `SKILL.md` for auto-triggering via the Skill Plugin System. Works on any
platform without the plugin (load the install protocol manually).

**Tier:** Tier 4 — Intelligence & Awareness. Pairs with the Image Generation System.

---

*Not shipped here (private / out of scope): prepaid-plan token-quota tracking, identity-canon
character templates, and reference-video / reference-audio inputs (a possible later iteration —
v1 is text-to-video + image-to-video).*
