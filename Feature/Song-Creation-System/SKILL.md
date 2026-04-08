---
name: song-creation
description: "Auto-triggers when user says 'create songs', 'new album', 'create album',
             'make music', 'muse this', 'write a song', 'create a song', 'compose',
             'song from image', 'album from image', 'generate album', 'write songs',
             or when user shares an image and wants to create music from it."
---

# Song Creation -- Visual-to-Musical Storytelling
*The image speaks. Songs are born.*

## Overview

An AI-powered music creation system with two modes:

- **Album Mode** — share an image, get a full concept album with story arc, Suno-ready style tags, and complete lyrics
- **Single Song Mode** — describe a mood or concept, get one complete song with style tags and lyrics

## Album Protocol

### Step 1: See the Image

Read the shared image. Extract and present:
- **Mood**: What emotion does this image evoke?
- **Characters**: Who or what is depicted?
- **Setting**: Where is this? What world?
- **Colors**: Dominant palette — this influences genre
- **Atmosphere**: Dark? Ethereal? Energetic? Melancholic?
- **Genre hints**: What kind of music does this image sound like?

Present: "I see [description]... This feels like [genre/mood]."

### Step 2: Generate Story Concept

From the image analysis, create a narrative concept:

```
World:       [Setting/universe derived from image]
Protagonist: [Who is this story about?]
Conflict:    [What tension drives the narrative?]
Arc:         [Beginning → turning point → resolution]
Theme:       [The emotional core — love, loss, rebellion, hope...]
```

Present as a 3-5 sentence synopsis. Then ask:
"Does this story feel right? Or should I adjust?"

**Wait for approval** or adjustment before proceeding.

### Step 3: Ask Song Count

"How many tracks?" (default from user preferences, or 7)

Map to arc structure:

| Count | Arc Structure |
|-------|--------------|
| 3 | Opening → Climax → Resolution |
| 5 | Prologue → Rise → Climax → Fall → Epilogue |
| 7 | Prologue → Character → Rise → Depth → Climax → Resolution → Epilogue |
| 10 | Extended arc with sub-plots, interludes, dual perspectives |

Other numbers: adapt the closest arc structure to fit.

### Step 4: Generate Album Name

Create album name following user's language preference:

**English style**: `[Evocative Title]` → folder: `[short-form]`
**Japanese style**: `漢字タイトル (Romaji)` → folder: `[english-short]`
**Bilingual**: `漢字 (Romaji - English)` → folder: `[english-short]`

The name should capture the album's emotional essence — not just describe the image.

### Step 5: Generate Songs

For each song, generate all three components:

**Title**:
- A title reflecting the song's role in the story arc
- Match language to user preference
- Include translation if using non-English language

**Style** (Suno-ready tags):
Rich descriptive tags covering all dimensions. Be specific — these drive Suno's generation:

```
[primary genre] [subgenre], [mood descriptor], [instruments],
[vocal style], [atmosphere], [tempo indicator], [thematic keywords]
```

See Style Tag Guide below for detailed examples.

**Lyrics**: Full structured text with proper sections:
```
[Verse 1]
lyrics...

[Pre-Chorus]
lyrics...

[Chorus]
lyrics...

[Verse 2]
lyrics...

[Bridge]
lyrics...

[Chorus]
lyrics...

[Outro]
lyrics...
```

**Story continuity**: Each song advances the narrative. Characters, events, and emotions reference the connected story. Each song serves its arc function (prologue establishes, climax peaks, etc.)

### Step 6: Present Complete Album

Show the full album:
1. Album name
2. Story synopsis
3. Song list with arc mapping
4. Each song: title, style tags, full lyrics

**Wait for review.** User may:
- Approve as-is → proceed to save
- Adjust individual songs → regenerate specific tracks
- Change the story direction → re-map arc
- Change language → regenerate lyrics

### Step 7: Save Album

Create folder and files:

```
music/[album-folder-name]/
  story.md         ← Narrative concept + arc mapping
  songs.md         ← All songs with metadata + full lyrics
  audio/           ← Empty folder (user adds generated audio later)
```

**story.md format:**
```markdown
# [Album Name]
*Created: [date] — Inspired by [brief image description]*

## Story
[Full narrative concept — 1-2 paragraphs]

## Arc
1. [Song 1 title] — [role in story]
2. [Song 2 title] — [role in story]
...

## Image Inspiration
[Description of the original image that spawned this album]
```

**songs.md format:**
```markdown
# [Album Name] — Songs

## Album Info
- **Name**: [Album name]
- **Tracks**: [N]
- **Language**: [language]
- **Created**: [date]
- **Inspired by**: [image description]

---

## Track 1: [Title]
**Style**: [full Suno-ready style tags]

[Verse 1]
lyrics...

[Pre-Chorus]
lyrics...

[Chorus]
lyrics...

[Verse 2]
lyrics...

[Bridge]
lyrics...

[Chorus]
lyrics...

[Outro]
lyrics...

---

## Track 2: [Title]
...
```

### Step 8: Commit (Optional)

If Auto-Commit System is installed, trigger a commit for the new album files.
If not installed, inform user that files are saved and can be committed manually.

---

## Single Song Protocol

For standalone songs without an image:

1. **Parse request** — extract topic, mood, genre preference, language
2. **Generate title** — match user's language preference
3. **Generate style tags** — rich Suno-ready descriptors
4. **Generate full lyrics** — complete structured text
5. **Present** — show title, style, and lyrics for review
6. **Save** (optional) — if user wants to save, create `music/singles/[song-title].md`

No story concept or approval gate needed for singles — just generate and present.

---

## Style Tag Guide (For Suno AI)

Style tags tell Suno what kind of music to generate. Be specific and descriptive across all dimensions:

### Genre Examples
```
gothic orchestral, symphonic metal, cyberpunk electronic, lo-fi hip hop,
dreamy pop, dark ambient, celtic folk, jazz fusion, progressive rock,
ethereal new age, aggressive trap, cinematic orchestral, chiptune,
vaporwave, post-rock, j-rock, city pop, bossa nova, drum and bass
```

### Mood Descriptors
```
melancholic, triumphant, haunting, euphoric, nostalgic, aggressive,
serene, anxious, hopeful, devastating, playful, ominous, bittersweet,
dreamlike, rebellious, tender, epic, intimate, chaotic, peaceful
```

### Instrument Keywords
```
orchestral strings, piano, acoustic guitar, electric guitar, synths,
choir, violin solo, cello, harp, drum machine, bass guitar, flute,
trumpet, music box, organ, electronic beats, traditional drums,
harpsichord, theremin, steel drums, shamisen, erhu
```

### Vocal Style Keywords
```
emotional female vocals, deep male vocals, whispered vocals,
powerful belting, soft falsetto, rap delivery, operatic soprano,
husky alto, duet, a cappella, vocoder, harmonized choir,
breathy intimate, aggressive screaming, spoken word
```

### Atmosphere Keywords
```
vast cathedral, neon cityscape, underwater depths, starlit sky,
ancient forest, empty battlefield, cozy room, digital void,
mountain peak, stormy ocean, abandoned station, cosmic expanse,
sunset beach, frozen tundra, crowded market, haunted manor
```

### Example Complete Style Tag
```
gothic orchestral, melancholic, orchestral strings with piano and choir,
emotional female vocals, vast cathedral atmosphere, slow tempo,
themes of loss and remembrance
```

---

## Adding Audio Files (Post-Generation)

When audio is generated from Suno and ready to save:
1. Copy audio files to `music/[album-name]/audio/`
2. Name format: `01-song-title.mp3`, `02-song-title.mp3`, etc.
3. Optionally update songs.md with audio file references

---

## Mandatory Rules

1. **Image drives albums** — never generate a full album without an image input. The image IS the muse. Single songs can use text descriptions
2. **Story coherence** — all songs in an album tell ONE connected story, not standalone tracks
3. **Full lyrics always** — never generate partial or placeholder lyrics. Every song gets complete structured text with proper sections
4. **Style tags are rich and specific** — these guide Suno generation. Cover genre, mood, instruments, vocal style, atmosphere, and tempo at minimum
5. **Wait for approval** — story concept and final album both need user confirmation before saving
6. **songs.md is the single source** — all lyrics in one file per album for easy copy-paste to Suno
7. **Language respect** — use the user's preferred language. If they chose Japanese, use proper kanji/romaji. If English, write naturally
8. **Arc mapping** — every song has a defined role in the narrative arc. No filler tracks
9. **Genre matches image** — dark images get dark music, bright images get bright music. Don't mismatch
10. **Organized storage** — always save to `music/` with proper folder structure. Never scatter files
