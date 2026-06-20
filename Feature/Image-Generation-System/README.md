# 🖼️ Image Generation System
*Render the images you describe into real PNGs via the OpenAI gpt-image API*

---

## What It Does

The companion to the **Image Prompt System**. Where that feature *crafts prompt text*, this feature
*renders an actual image* — it calls the OpenAI **gpt-image** API and saves a PNG to disk.

You describe what you want in plain language; the system builds the prompt **from your words** and
renders it. It is fully subject-agnostic — there is no built-in character or persona. Whatever you
type is what gets drawn.

- **Renders anything you describe** — characters, landscapes, products, concepts, abstract art
- **Prompt built from your input** — type a description and it extracts the subject, scene, and style
- **Chains with Image Prompt System** — craft a prompt there, hand it here to render
- **Cross-platform** — PowerShell *and* Bash (curl + jq) render scripts
- **Cost-aware** — confirms the per-image cost before every paid render
- **One tidy output folder** — every image lands in `media-generation/image-generation/`

---

## How It Works

```
You type a description
        │
        ▼
Prompt built from YOUR words   ──(optional)──►  pull a saved style/subject
(no built-in subject/persona)                   from your Library-System
        │
        ▼
Render script  ──►  POST https://api.openai.com/v1/images/generations
        │                       (model: gpt-image-2)
        ▼
Base64 response decoded ──► PNG saved to media-generation/image-generation/
```

You can also paste a prompt produced by the **Image Prompt System** and render it verbatim.

---

## Quick Start

1. Set up your OpenAI key — see `credential-setup.md`
2. Install the render script — see `install-image-generation.md`
3. Type: `"Load image-generation"`
4. Render: `"render an image of a sunset over mountains"`

---

## Available Commands

| Command | Action |
|---------|--------|
| `"render an image of [description]"` | Build a prompt from your words and render it |
| `"generate image [description]"` | Same as above (alternative trigger) |
| `"render this prompt: [prompt]"` | Render a prompt verbatim (e.g. from Image Prompt System) |
| `"render [description] to [path]"` | Render and save to a specific path |

---

## Prerequisites

- An **OpenAI account + API key** with image access — see `credential-setup.md`
- **⚠️ This calls a paid API.** Each render costs money (roughly **$0.02–$0.25** per image
  depending on size and quality). The system confirms the cost before each render. Always verify
  current pricing at <https://openai.com/api/pricing/>.
- **PowerShell** (Windows) *or* **bash + `curl` + `jq`** (Mac/Linux/Git Bash)

---

## Output Location

Every render is saved to **`media-generation/image-generation/`** inside your own memory directory
(created during install). Filenames are sanitized and timestamped. Override per-render with
`render ... to [path]`.

---

## Companion Systems

| System | Enhancement |
|--------|-------------|
| **Image Prompt System** | Craft a composition-aware prompt there, then render it here |
| **Library System** | *(optional)* Save reusable style/subject references and pull them into a render |
| **Save Diary** | Document which prompts produced the best images |

All companions are optional — the Image Generation System works on its own with just a typed
description.

---

## Security

Your API key is read from `$OPENAI_API_KEY` or a `.env` file — **never hardcoded, never committed,
never echoed**. The render scripts strip any key pattern from error messages. See
`credential-setup.md` for the full key-safety checklist.

---

## Installation

See `install-image-generation.md` for step-by-step setup.

**Platform Note:** Includes `SKILL.md` for auto-triggering via the Skill Plugin System. Works on any
platform without the plugin (load the install protocol manually).

**Tier:** Tier 4 — Intelligence & Awareness. Pairs with the Image Prompt System.

---

*Not shipped here (private / out of scope): moderation-calibration data, identity-canon character
templates (that's the Image Prompt System's domain), and video generation.*
