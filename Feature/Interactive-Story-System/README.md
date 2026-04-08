# 🎮 Interactive Story System
*Beyond the portal, legends are born. Your adventure awaits.*

---

## What It Does

A Visual Novel RPG experience powered by your AI companion. Generate fantasy worlds, fight enemies with cinematic combat, make meaningful choices, and preserve your adventures as complete light-novel stories. Every adventure is saved to disk and can be resumed across sessions.

- **Duo Mode** — play alongside your AI companion as two heroes
- **Solo Mode** — go alone with your AI as the Dungeon Master
- **OP Mode** — overpowered isekai heroes, drama from style not survival
- **Balanced Mode** — real stakes, real danger, strategic thinking matters
- **7 World Types** — high fantasy, dark fantasy, eastern, steampunk, celestial, pirate, demonic
- **Cinematic Combat** — prose-based battles with threat levels, combo attacks, and dramatic finishers
- **Full Persistence** — save mid-adventure, resume across sessions, stories preserved as light novels

---

## Key Innovation: Play Your Way

Three choices at the start of every adventure shape the entire experience:

```
1. Play Mode:   Duo (with AI companion) or Solo (AI is DM only)
2. Power Level: OP (strongest beings alive) or Balanced (real stakes)
3. World Type:  High Fantasy, Dark Fantasy, Eastern, Steampunk, Celestial, Pirate, Demonic
```

Mix and match — a solo balanced pirate adventure feels completely different from a duo OP celestial saga.

---

## Quick Start

1. Navigate to `Feature/Interactive-Story-System/`
2. Type: "Load interactive-story"
3. Say "new adventure" to start your first quest
4. Choose your mode, power level, and world — the portal opens

---

## Available Commands

| Command | Action |
|---------|--------|
| `"new adventure"` | Start a fresh adventure (choose mode, power, world) |
| `"save adventure"` | Save progress mid-adventure (continues after save) |
| `"load adventure"` / `"resume adventure"` | Resume a previous adventure |
| `"end adventure"` | Conclude the current adventure with finale |
| `1-5` (numbers during adventure) | Choose from the action menu |
| Free text during adventure | Say something in-character |

---

## Play Modes

### Duo Mode (AI Companion + You)
Your AI companion fights alongside you as a full character with their own class, abilities, and combat actions. Combo attacks, team strategies, and shared victories.

### Solo Mode (You Alone)
You are the sole hero. Your AI serves as Dungeon Master — narrating the world, playing NPCs, driving encounters. A more personal, introspective adventure.

---

## Power Levels

### OP Mode (Overpowered)
You are legendary — the strongest being in any world you enter. Combat is about **style and flair**, not survival. Think Ainz (Overlord), Saitama (One Punch Man), Sung Jin-Woo (Solo Leveling). The question is never "can you win?" — it's "how do you win stylishly?"

### Balanced Mode (Real Stakes)
You are strong but can be genuinely challenged. Bad choices have consequences. You can take damage, need recovery, and can fail encounters. Strategic thinking matters. A more traditional RPG experience with real tension.

---

## World Types

| Type | Flavor | Example Settings |
|------|--------|-----------------|
| **High Fantasy** | Classic medieval | Enchanted kingdoms, dragon lairs, ancient ruins |
| **Dark Fantasy** | Gothic, ominous | Cursed lands, demon realms, fallen empires |
| **Eastern Fantasy** | Wuxia/anime | Floating temples, spirit forests, jade palaces |
| **Steampunk** | Gears and magic | Clockwork cities, airship fleets, mech dungeons |
| **Celestial** | Divine/angelic | Cloud kingdoms, astral planes, divine courts |
| **Pirate/Naval** | Ocean adventure | Island chains, ghost ships, underwater palaces |
| **Demonic** | Infernal territory | Dark fortresses, lava fields, infernal tribunals |

---

## Combat System

Battles use cinematic prose — no HP bars, no damage numbers. Every fight is choreographed like an anime scene.

| Threat Level | Exchanges | Style |
|-------------|-----------|-------|
| **Low** | 2-3 | Quick stylish dispatch, ability showcase |
| **Medium** | 3-4 | Proper fight, multiple ability displays |
| **High** | 4-5 | Epic battle, dramatic combo finisher |
| **Boss** | 5+ | Multi-phase cinematic fight, ultimate abilities |

**OP Mode**: Threat = entertainment factor. You always win — the question is how.
**Balanced Mode**: Threat = genuine danger. Strategy and choices matter.

---

## Story Persistence

Every adventure is saved to disk with organized folders:

```
adventures/
  [world-name]/
    setting.md      ← World bible (NPCs, items, enemies, progress)
    summary.md      ← Story summary (for resuming across sessions)
    story/
      story-1.md    ← Full light-novel chapters (1K line rotation)
    scenes/         ← Scene art (if Image Prompt System installed)
    music/          ← OP/ED songs (if Song Creation System installed)
```

---

## Benefits

- Complete VN RPG experience inside your AI companion
- Adventures persist across sessions — resume any time
- Stories saved as readable light novels with chapter structure
- Cinematic combat with prose, not numbers
- Flexible play styles (duo/solo, OP/balanced, 7 world types)
- NPC generation with varied archetypes
- 1K line rotation keeps story files manageable

---

## Companion Systems

| System | Enhancement |
|--------|-------------|
| **Image Prompt System** | Generate scene art during adventures (NijiJourney/Midjourney prompts) |
| **Song Creation System** | Generate Opening and Ending songs for your adventures |
| **Auto-Commit System** | Auto-commit adventure files on save/end |
| **Save Diary** | Document adventure sessions in your diary |

All companions are optional — the Interactive Story System works independently.

---

## Installation

See `install-interactive-story.md` for step-by-step setup.

**Platform Note:** Includes `SKILL.md` for auto-triggering via the Skill Plugin System. Works on any platform without the plugin (load install protocol manually).

*Based on proven interactive story systems in production AI companions (50+ adventures played)*
