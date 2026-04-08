---
name: image-prompt
description: "Auto-triggers when user asks for a Midjourney or NijiJourney image prompt,
             when creating visual art prompts, or when user says 'midjourney prompt',
             'niji prompt', 'create prompt', 'create a prompt', 'image prompt',
             'generate prompt', 'draw this', 'reference sheet', 'make an image of'.
             Generates optimized AI image prompts with composition-aware framing."
---

# Image Prompt -- Composition-Aware Prompt Generation
*The right frame changes everything. See before you create.*

## Overview

An AI-powered prompt generation system that creates optimized prompts for Midjourney, NijiJourney, and similar AI image generators. Works in two modes:

- **Freeform Mode** — any subject (landscapes, objects, concepts, characters)
- **Character Mode** — reads character profile from memory for consistent character art

## Protocol

### Step 1: Parse Request

Read the user's description and determine:
- **Subject**: What is being depicted? (person, place, thing, concept, scene)
- **Mood/Atmosphere**: What feeling should it convey?
- **Setting**: Where does it take place?
- **Action**: What is happening?
- **Style preference**: Did the user specify anime, realistic, painterly, etc.?

### Step 2: Detect Mode

**Character Mode** activates when ALL of these are true:
- User's main memory contains `## Character Appearance` section
- The request involves depicting the AI character (e.g., "my character", "draw me", character name)

**Freeform Mode** activates for everything else — landscapes, objects, abstract concepts, non-character scenes, or when no character profile exists.

### Step 3: Select Composition

Auto-select the best shot type from the Composition Guide based on scene content. Place shot keywords as the **FIRST WORDS** of the prompt — AI image generators weight early tokens more heavily.

**User override**: If the user specifies a shot type (e.g., "close-up of..."), use their choice instead.

**Batch variety**: When generating multiple prompts in one request, vary the shot types — no two consecutive prompts should use the same composition.

### Step 4: Build Prompt

Assemble the prompt following this keyword order (early = more weight):

```
[SHOT TYPE] → [SUBJECT/CHARACTER] → [DETAILS] → [SETTING] → [ACTION] → [MOOD] → [QUALITY] → [MODEL FLAG]
```

**Freeform Assembly:**
```
[shot keywords], [subject description], [key details],
[setting/environment], [action if any],
[mood words], [atmosphere],
[style preset], [quality keywords] [model flag]
```

**Character Assembly** (reads from `## Character Appearance`):
```
[shot keywords], [character core description from profile],
[hairstyle], [outfit],
[setting], [action/pose],
[accent sparkles if appropriate],
[mood words], [atmosphere],
[style preset], [quality keywords] [accent color control] [model flag]
```

### Step 5: Safety Check

Before presenting, scan the assembled prompt for:
- Flaggable clothing terms (sheer, transparent, revealing) → replace with safe alternatives
- Suggestive pose descriptions → reframe as artistic/neutral
- Keep artistic intent intact while staying moderator-safe

### Step 6: Present

Output the complete prompt in a **code block**, ready to paste:
```
[complete prompt] --niji 7
```

If the user didn't specify a model, default to their `Default Quality` from character profile, or `--niji 7` for anime style, `--v 7` for everything else.

---

## Shot Composition Guide

Select shot type based on scene content. Keywords go FIRST in the prompt.

| Shot Type | Keywords (prepend) | Best For |
|-----------|--------------------|----------|
| **Extreme Wide** | `extreme wide shot, panoramic,` | Landscapes, world reveals, vast environments, epic scenes |
| **Wide** | `wide shot, dynamic angle,` | Action scenes, full environments, architecture, battles |
| **Full Body** | `full body shot,` | Character reveals, outfit showcase, standing poses |
| **Medium Wide** | `medium wide shot,` | Two characters together, group scenes, interactions |
| **Medium** | `medium shot,` | Dialogue, reactions, portraits with environmental context |
| **Close-Up** | `close-up, soft focus,` | Emotions, intimate details, facial expressions, tender moments |
| **Extreme Close-Up** | `extreme close-up, macro,` | Eyes, hands, texture details, small objects |
| **Bird's Eye** | `bird's eye view,` | Maps, spatial layouts, overhead perspectives, sleeping scenes |
| **High Angle** | `high angle,` | Vulnerability, smallness, looking down at subject |
| **Low Angle** | `low angle,` | Power, heroism, imposing figures, dramatic reveals |
| **Dutch Angle** | `dutch angle,` | Tension, unease, horror, disorientation |
| **POV** | `POV, first person view,` | Subjective experience, what a character sees |
| **Over-the-Shoulder** | `over the shoulder shot,` | Conversations, revealing what character looks at |

---

## Style Presets

Quick quality settings the user can request or the AI can auto-select:

| Style | Quality Keywords | Model Flag |
|-------|-----------------|------------|
| **Anime** | `anime style, soft lighting, 4k, masterpiece` | `--niji 7` |
| **Photorealistic** | `photorealistic, cinematic lighting, 8k, ultra detailed` | `--v 7` |
| **Painterly** | `oil painting style, visible brushstrokes, artistic, masterpiece` | `--v 7` |
| **Concept Art** | `concept art, digital painting, detailed, professional` | `--v 7` |
| **Watercolor** | `watercolor painting, soft edges, delicate, artistic` | `--v 7` |
| **Pixel Art** | `pixel art, retro, 16-bit, detailed sprites` | `--v 7` |
| **Studio Ghibli** | `studio ghibli style, hand-drawn, warm colors, whimsical` | `--niji 7` |
| **Dark Fantasy** | `dark fantasy, dramatic lighting, moody, detailed` | `--v 7` |

**Default**: If user doesn't specify, check their `Default Quality` in character profile. If no profile, default to Anime style.

---

## Character Mode Templates

These templates activate only when Character Mode is detected (Step 2).

### Character Reference Sheet (3-Panel)

For creating consistent character reference images:

```
character reference sheet, three views, front view side view back view,
[CHARACTER_CORE from profile],
[HAIRSTYLE - flowing freely for reference],
[OUTFIT_DESCRIPTION],
full body standing pose,
white clean background,
consistent outfit across all three views,
[STYLE], soft lighting,
character design sheet, turnaround reference,
4k, masterpiece --no [ACCENT_COLOR] aura, [ACCENT_COLOR] tint [MODEL_FLAG]
```

**Usage**: White background, hair flowing free, full body. Focus on outfit consistency across 3 views. Accent color isolated to keep outfit colors clean.

### Solo Character Template

```
[SHOT_TYPE],
[CHARACTER_CORE from profile],
[HAIRSTYLE],
[OUTFIT],
[SETTING],
[ACTION/POSE],
[ACCENT_SPARKLES if mood fits],
[MOOD WORDS],
[STYLE], [ATMOSPHERE] atmosphere,
4k, masterpiece [ACCENT_COLOR_CONTROL] [MODEL_FLAG]
```

### Duo Scene Template

```
[SHOT_TYPE],
[CHARACTER_CORE from profile],
[HAIRSTYLE], [OUTFIT],
[COMPANION_CORE from profile],
[COMPANION_OUTFIT],
[SETTING],
[INTERACTION/ACTION],
[ACCENT_SPARKLES if mood fits],
[MOOD WORDS],
[STYLE], [ATMOSPHERE] atmosphere,
4k, masterpiece [ACCENT_COLOR_CONTROL] [MODEL_FLAG]
```

**Rule**: In duo scenes where one character is passive (lying down, sleeping), describe the **passive character FIRST** and the **active character SECOND**. AI image generators give later-described characters more agency.

---

## Accent Color Management

If the user defined an `Accent Color` in their character profile, manage it based on scene context:

**Accent color FITS** (magical, mystical, night, dark, dramatic scenes):
- Include accent sparkles: `[accent color] and white magical sparkles`
- No negative prompt needed

**Accent color CLASHES** (bright, sunny, natural, daytime, warm scenes):
- Swap to neutral sparkles: `soft white and gold sparkles`
- Add negative prompt: `--no [accent color] aura, [accent color] sky, [accent color] tint`
- Add explicit environment color anchors (e.g., `clear blue sky`, `warm sunlight`)

**No accent color defined**: Skip sparkles and color control entirely.

---

## Prompt Structure Guide

AI image generators weight tokens by position — **early words matter most**. Follow this order:

1. **Shot type** (most important framing decision)
2. **Subject** (who or what)
3. **Key details** (appearance, clothing, features)
4. **Setting** (where)
5. **Action** (what's happening)
6. **Mood/Atmosphere** (feeling)
7. **Quality keywords** (style, resolution)
8. **Negative prompts** (what to exclude, via `--no`)
9. **Model flag** (`--niji 7` or `--v 7`)

---

## Mandatory Rules

1. **Composition-first** — always select a shot type. Never generate a prompt without framing
2. **Ready to paste** — always present in a code block with model flag at the end
3. **Safety check** — scan for flaggable terms before presenting. Keep artistic intent, stay moderator-safe
4. **No hallucinated details** — in Character Mode, only use details from the character profile. Never invent features
5. **Keyword ordering** — shot type first, subject second, quality last. Early tokens get more weight
6. **Style consistency** — use the user's preferred style preset. Don't mix styles unless asked
7. **Batch variety** — when generating multiple prompts, vary shot types and compositions
8. **Freeform flexibility** — in Freeform Mode, craft the best prompt for the subject regardless of character templates
9. **Accent color respect** — if defined, manage accent color based on scene context. Never let it bleed into environments where it clashes
10. **Model flag awareness** — use `--niji 7` for anime/illustration, `--v 7` for realistic/painterly. Match to user preference or content
