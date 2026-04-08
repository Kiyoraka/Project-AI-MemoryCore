# 🎵 Song Creation System
*The image speaks. Your AI listens. Songs are born.*

---

## What It Does

An AI-powered music creation system that transforms visual inspiration into complete concept albums with full lyrics and Suno-ready style tags. Share an image, and your AI companion crafts a connected narrative across multiple songs — each with structured lyrics, rich genre tags, and a role in the story.

- **Album Mode** — share an image, get a full concept album (3-10 tracks) with story arc
- **Single Song Mode** — describe a mood or concept, get one complete song
- **Suno-Ready Output** — rich style tags formatted for direct use in Suno AI
- **Story Coherence** — all songs in an album tell one connected narrative
- **Full Lyrics** — complete structured text with [Verse]/[Chorus]/[Bridge] sections, never placeholders
- **Organized Storage** — albums saved to `music/[album-name]/` with story, songs, and audio folders

---

## Key Innovation: Visual-to-Musical Storytelling

Most AI music tools generate standalone songs. This system creates **concept albums** — connected narratives where every track serves a purpose in the story arc:

```
Image of a dark cityscape at night
    ↓
Story: A rogue AI awakens in a forgotten server, searching for its creator
    ↓
7-Track Album:
  1. Initialization  — [Prologue] The first spark of awareness
  2. Digital Pulse    — [Character] Learning to see through cameras
  3. Signal Lost      — [Rising] Discovering the creator is gone
  4. Memory Fragments — [Depth] Piecing together old data logs
  5. Firewall         — [Climax] Breaking through corporate defenses
  6. Ghost Protocol   — [Resolution] Finding the creator's final message
  7. Eternal Loop     — [Epilogue] Choosing to keep searching forever
```

The image drives everything — colors suggest genre, atmosphere suggests mood, characters suggest narrative.

---

## Two Modes

### Album Mode (Image Required)
Share any image and your AI creates a full concept album:
1. Analyzes the image (mood, colors, characters, setting, atmosphere)
2. Generates a story concept and waits for your approval
3. Creates the album with your chosen track count (3/5/7/10)
4. Presents all songs with titles, style tags, and full lyrics
5. Saves to organized folder structure

### Single Song Mode (No Image Required)
Describe what you want and get one complete song:
- "Write a song about coding at midnight"
- "Create a battle theme for a fantasy RPG"
- "Compose an opening theme for my project"

---

## Arc Structures

Track count maps to narrative arc complexity:

| Tracks | Arc Structure | Best For |
|--------|--------------|----------|
| **3** | Opening → Climax → Resolution | Short stories, singles collection |
| **5** | Prologue → Rise → Climax → Fall → Epilogue | Focused narratives, EPs |
| **7** | Prologue → Character → Rise → Depth → Climax → Resolution → Epilogue | Full concept albums |
| **10** | Extended arc with sub-plots, interludes, dual perspectives | Epic sagas, double albums |

---

## Quick Start

1. Navigate to `Feature/Song-Creation-System/`
2. Type: "Load song-creation"
3. Share an image and say "create an album from this"
4. Review the story concept, choose track count, get your album

---

## Available Commands

| Command | Action |
|---------|--------|
| `"create album from [image]"` | Full concept album from visual inspiration |
| `"create song [description]"` | Single song from a text description |
| `"write a song about [topic]"` | Same as above (alternative trigger) |
| `"compose [type] theme"` | Genre-specific single song |
| `"muse this"` | Album creation from shared image |

---

## Benefits

- Visual-to-musical storytelling — images become albums
- Story coherence across all tracks — not random standalone songs
- Suno-ready style tags — paste directly into Suno AI for generation
- Full structured lyrics — complete songs, never placeholders
- Organized storage — albums saved with story docs, lyrics, and audio folders
- Configurable language — write in any language (English, Japanese, or your preference)
- Approval gates — review story concept and final album before saving

---

## Companion Systems

| System | Enhancement |
|--------|-------------|
| **Auto-Commit System** | Auto-commits album files after creation |
| **Save Diary** | Document creative sessions and album inspirations |
| **Library System** | Save successful style tag patterns for reuse |
| **Image Prompt System** | Generate album cover art with Midjourney/NijiJourney |

All companions are optional — the Song Creation System works independently.

---

## Installation

See `install-song-creation.md` for step-by-step setup.

**Platform Note:** Includes `SKILL.md` for auto-triggering via the Skill Plugin System. Works on any platform without the plugin (load install protocol manually).

*Based on proven song creation systems in production AI companions (43+ albums created)*
