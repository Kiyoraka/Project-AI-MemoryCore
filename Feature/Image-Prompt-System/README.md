# 🎨 Image Prompt System
*Craft perfect Midjourney & NijiJourney prompts — for any subject, any style*

---

## What It Does

An AI-powered prompt generation assistant that creates optimized image prompts for Midjourney, NijiJourney, and similar AI image generators. Works with any subject — characters, landscapes, objects, concepts, or abstract art.

- **Freeform Mode** — describe anything, get an optimized prompt ready to paste
- **Character Mode** — define your AI companion's appearance once, get consistent character art every time
- **Shot Composition Guide** — built-in reference for camera angles and framing (close-up, wide shot, bird's eye, etc.)
- **Style Presets** — quick quality settings for anime, photorealistic, painterly, and concept art
- **Safety Check** — automatic scan for flaggable terms before presenting

---

## Key Innovation: Composition-Aware Prompts

Most AI prompt tools just string keywords together. This system understands **composition** — it selects the right camera angle, framing, and shot type based on what you're trying to capture:

```
"a warrior standing on a cliff"     → extreme wide shot, panoramic
"two friends talking at a cafe"     → medium shot
"a character revealing their power" → full body shot, low angle
"an emotional farewell scene"       → close-up, soft focus
```

The right composition transforms a good prompt into a great image.

---

## Two Modes

### Freeform Mode (No Setup Required)
Describe anything — the AI crafts an optimized prompt with proper keyword ordering, composition, and quality settings.

```
You: "create a prompt for a cyberpunk city at night with neon reflections"
AI: [generates optimized prompt with shot type, lighting, mood, quality keywords]
```

### Character Mode (Optional Setup)
Define your AI companion's visual appearance in your memory files. The system reads this profile and generates consistent character art — solo portraits, reference sheets, duo scenes.

```
You: "create a prompt of my character reading in a library"
AI: [reads character profile → generates prompt with exact appearance details]
```

---

## Quick Start

1. Navigate to `Feature/Image-Prompt-System/`
2. Type: "Load image-prompt"
3. Start generating: "create a prompt for [anything]"
4. (Optional) Set up character profile for consistent character art

---

## Available Commands

| Command | Action |
|---------|--------|
| `"create a prompt for [description]"` | Generate an optimized image prompt |
| `"midjourney prompt [description]"` | Same as above (alternative trigger) |
| `"niji prompt [description]"` | Generate with NijiJourney anime preset |
| `"reference sheet for [character]"` | Generate 3-panel character reference |
| `"image prompt [description]"` | Same as above (alternative trigger) |

---

## Benefits

- Works with ANY subject — not limited to characters
- Shot composition guide teaches you visual storytelling
- Consistent character art through profile-aware generation
- Moderator-safe outputs — flaggable terms auto-replaced
- Ready-to-paste prompts in code blocks with model flags
- Style presets for quick quality targeting
- Keyword ordering optimized for AI image generator weighting

---

## Companion Systems

| System | Enhancement |
|--------|-------------|
| **Memory Consolidation** | Character profile stored in unified `main-memory.md` |
| **Save Diary** | Document which prompts produced the best results |
| **Library System** | Save successful prompt patterns for reuse |

All companions are optional — the Image Prompt System works independently.

---

## Installation

See `install-image-prompt.md` for step-by-step setup.

**Platform Note:** Includes `SKILL.md` for auto-triggering via the Skill Plugin System. Works on any platform without the plugin (load install protocol manually).

*Based on proven prompt generation systems in production AI companions*
