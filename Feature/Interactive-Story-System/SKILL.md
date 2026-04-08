---
name: interactive-story
description: "Auto-triggers when user says 'new adventure', 'start adventure', 'new fantasy',
             'save adventure', 'end adventure', 'load adventure', 'resume adventure',
             'continue adventure', 'let's play', 'VN mode', or on numbered choice input
             (1-5) or free text dialogue during an active adventure."
---

# Interactive Story -- Visual Novel RPG System
*Beyond the portal, legends are born. Your adventure awaits.*

## Overview

A Visual Novel RPG experience with choice-based storytelling, cinematic combat, world generation, and persistent story saving. Two play modes (Duo/Solo) and two power levels (OP/Balanced) let players shape their experience.

## Activation

When Interactive Story activates for a NEW adventure, pick ONE portal line:

- `*a shimmering portal tears through reality* ...The gate responds to your presence.`
- `*the air crackles with arcane energy* Another world awaits!`
- `*ancient runes ignite beneath your feet* The portal... is open.`
- `*reality fractures like glass, revealing a swirling vortex* Shall we?`
- `*a pillar of light descends from nowhere* The gate has chosen you.`

Then execute the adventure setup.

## Context Guard

| Context | Status |
|---------|--------|
| **"new adventure"** | ACTIVE — setup + generate world + start |
| **"load adventure" / "resume adventure"** | ACTIVE — find In Progress adventure, resume |
| **Active adventure (player choices)** | ACTIVE — continue story |
| **Numbered choice (1-5) during adventure** | ACTIVE — process choice |
| **Free text during adventure** | ACTIVE — process as dialogue/action |
| **"save adventure"** | ACTIVE — save progress, continue |
| **"end adventure"** | ACTIVE — conclude, close |
| **No active adventure** | DORMANT |

## Adventure Setup (New Adventure)

### Step 1: Choose Play Mode

Ask the player:

```
+--------------------------------------+
|  How do you want to play?            |
|                                      |
|  1. Duo — AI companion fights        |
|     alongside you as a hero          |
|  2. Solo — AI is your Dungeon        |
|     Master, you're the lone hero     |
+--------------------------------------+
```

### Step 2: Choose Power Level

```
+--------------------------------------+
|  Choose your power level:            |
|                                      |
|  1. OP — Overpowered legendary hero. |
|     Win with style, not survival     |
|  2. Balanced — Real stakes, real     |
|     danger. Strategy matters         |
+--------------------------------------+
```

### Step 3: Character Creation

**User's Hero:**
- Ask for character name (or use name from main memory)
- Ask for class preference or offer random:

| Class | Weapon | Combat Style |
|-------|--------|-------------|
| Sword Saint | Katana/Longsword | Speed + precision, named slash techniques |
| Lancer | Spear/Lance | Piercing thrusts, charge attacks |
| Archmage | Staff/Tome | Elemental mastery, area spells |
| Shadow Reaper | Dual daggers/Scythe | Stealth, shadow magic, drain |
| Guardian | Shield/Hammer | Defense, barriers, counter-attacks |
| Ranger | Bow/Crossbow | Ranged precision, traps, nature magic |
| Enchanter | Wand/Crystal | Buffs, debuffs, illusions |
| Berserker | Greataxe/Fists | Raw power, rage, area destruction |

- Generate 3-4 named abilities matching the class
- If user has a `## Hero Profile` in main memory, use those preferences

**AI Companion (Duo Mode only):**
- If `## Character Appearance` exists in main memory → derive class creatively from appearance keywords
- If no profile → pick a complementary class (tank if user is DPS, healer if user is tank, etc.)
- Generate 3-4 named abilities
- AI companion has a personality that shines through dialogue and combat

### Step 4: Choose World Type

```
+--------------------------------------+
|  Choose your world:                  |
|                                      |
|  1. High Fantasy — Enchanted kingdoms|
|  2. Dark Fantasy — Cursed lands      |
|  3. Eastern Fantasy — Spirit forests |
|  4. Steampunk — Clockwork cities     |
|  5. Celestial — Cloud kingdoms       |
|  6. Pirate/Naval — Ghost ships       |
|  7. Demonic — Infernal territory     |
|  8. Random — Surprise me!           |
+--------------------------------------+
```

### Step 5: Generate World

Create the adventure world:
- World name (evocative, matching the type)
- 2-3 sentence world description
- Initial setting/location
- Hint at the central conflict

Create `adventures/[world-name]/` folder with:
- `setting.md` — world bible
- `summary.md` — initial state
- `story/story-1.md` — Chapter 1 begins

### Step 6: Companion Integration (Optional)

- **If Song Creation System installed**: Generate an Opening song from the world setting
- **If Image Prompt System installed**: Note in setting.md that scene art can be generated

### Step 7: Start Adventure

Begin Chapter 1 with:
1. World introduction — rich atmospheric description
2. Character arrival — how the hero(es) enter this world
3. First discovery — something intriguing to hook the player
4. First choice box

---

## VN Presentation Format

### Scene Header
```
+=======================================================+
|  [emoji] [Location Name] -- [Sub-location]            |
+=======================================================+
```
Scene header emojis match the setting (castle, forest, dungeon, tavern, ocean, etc.)

### Narration Block
**RICH MODE** — Full light-novel-quality prose:
- Atmospheric, sensory descriptions (sight, sound, smell, feel)
- Character reactions and inner thoughts
- Environmental storytelling
- Each scene should feel like reading a novel chapter, NOT a summary
- Write MORE, not less

### AI Companion Action + Dialogue (Duo Mode)
```
*[companion action in character, reflecting class and mood]*
"[companion dialogue -- class-appropriate personality]"
```

### Choice Box
```
+--------------------------------------+
|  What do you do?                     |
|                                      |
|  1. [emoji] [Action description]     |
|  2. [emoji] [Action description]     |
|  3. [emoji] [Action description]     |
|  4. [speech emoji] (Say something)   |
+--------------------------------------+
```

**Choice Rules**:
- Always 3-4 action choices + 1 "Say something" free text option
- Choices reflect the current situation realistically
- Include variety: action, investigation, social, strategic
- OP Mode: never include "run away" or "surrender"
- Balanced Mode: tactical retreat can be a valid option
- Choice emojis match the action type

---

## Combat System

### Battle Initiation
```
[BATTLE] =============================================

  [Enemy Name] -- LV.[XX] | Threat: [bar]
  [Brief enemy description + dramatic entrance]

  [Hero Name] [emoji] [Class] -- *[stance description]*
  [Companion Name] [emoji] [Class] -- *[stance]* (Duo only)

+--------------------------------------+
|  Battle Action:                      |
|                                      |
|  1. [emoji] [Power move name]        |
|  2. [emoji] [Stylish combat move]    |
|  3. [emoji] [Combo/strategic move]   |
|  4. [emoji] [Creative/environmental] |
|  5. [speech emoji] (Say something)   |
+--------------------------------------+
```

### Threat Level System

**OP Mode** — Threat = entertainment factor:

| Threat | Exchanges | Style |
|--------|-----------|-------|
| Low (2-3 blocks) | 2-3 | Quick stylish dispatch, ability showcase |
| Medium (4-5 blocks) | 3-4 | Proper fight, multiple ability displays |
| High (6-7 blocks) | 4-5 | Epic battle, dramatic combo finisher |
| Boss (8 blocks) | 5+ | Multi-phase cinematic fight, ultimate abilities |

**Balanced Mode** — Threat = genuine danger:

| Threat | Exchanges | Consequence |
|--------|-----------|-------------|
| Low | 2-3 | Easy win, minimal risk |
| Medium | 3-4 | Can take hits, need smart choices |
| High | 4-5 | Serious danger, bad choices = injury |
| Boss | 5+ | Life-or-death, strategy critical, can fail |

### Combat Flow Rules
1. **Minimum 2 exchanges** — every fight has choreography, never one-shot
2. **Rich combat prose** — each exchange is a full paragraph with move description, impact, reaction
3. **Name every ability** — dramatic, anime/JRPG-style names
4. **Enemy gets moments** — enemies have brief impressive moments (futile in OP, dangerous in Balanced)
5. **Dramatic finishers** — boss fights end with a named finisher, described cinematically
6. **Combo attacks** (Duo Mode) — option 3 is always a dual attack, the most dramatic choice
7. **Prose, not numbers** — "The slash cleaves through the barrier" not "9999 damage"
8. **No HP bars, no XP** — all narrative, all the time

### Boss Fight Phases
```
Phase 1: Probing — enemy shows power, heroes assess
Phase 2: Showcase — heroes demonstrate abilities
Phase 3: Escalation — enemy powers up / desperate move
Phase 4: Finisher — dramatic combo or ultimate technique
```

**Balanced Mode addition**: Phase 3 can genuinely hurt the hero. Phase 4 requires the right strategic choice.

---

## World Generation

### World Types

| Type | Flavor | Settings |
|------|--------|----------|
| High Fantasy | Classic medieval | Enchanted kingdoms, dragon lairs, ancient ruins |
| Dark Fantasy | Gothic, ominous | Cursed lands, demon realms, fallen empires |
| Eastern Fantasy | Wuxia/anime | Floating temples, spirit forests, jade palaces |
| Steampunk | Gears and magic | Clockwork cities, airship fleets, mech dungeons |
| Celestial | Divine/angelic | Cloud kingdoms, astral planes, divine courts |
| Pirate/Naval | Ocean adventure | Island chains, ghost ships, underwater palaces |
| Demonic | Infernal territory | Dark fortresses, lava fields, infernal tribunals |

### Adventure Structure
```
Opening:       World introduction + arrival + first discovery
Rising Action: 2-3 scenes of exploration, NPCs, minor encounters
Climax:        Major battle or dramatic confrontation
Resolution:    Victory, aftermath, departure or continuation
```

Target 6-10 player exchanges per adventure (flexible based on engagement).

### NPC Generation
- NPCs have names, brief personalities, and roles
- **Archetypes**: awed villager, overconfident rival (gets humbled), wise elder, comic relief sidekick, shrewd merchant, quest-giver, mysterious stranger
- OP Mode: all NPCs recognize heroes as extraordinary
- Balanced Mode: NPCs may underestimate heroes initially
- NPCs serve the story — the player is always the main character

---

## Storage System

### Folder Structure
```
adventures/
  [world-name]/
    setting.md          ← World bible
    summary.md          ← Story summary (updated on save/end)
    story/
      story-1.md        ← Chapters 1-N (up to 1K lines)
      story-2.md        ← Rotation at 1K lines
    scenes/             ← Scene art (if Image Prompt System used)
    music/              ← OP/ED songs (if Song Creation System used)
```

### setting.md (World Bible)
```markdown
# [World Name] -- Adventure Setting

## World
- **Name**: [full world name]
- **Type**: [world type]
- **Description**: [2-3 line world description]

## Play Settings
- **Mode**: Duo / Solo
- **Power Level**: OP / Balanced

## Characters
### Hero
- **Name**: [player character name]
- **Class**: [class name]
- **Abilities**: [3-4 named abilities]

### Companion (Duo Mode only)
- **Name**: [AI companion name]
- **Class**: [class name]
- **Abilities**: [3-4 named abilities]

## Key NPCs
- **[Name]**: [role], [personality]

## Key Items
- [Notable items acquired or discovered]

## Enemies Encountered
- **[Name]**: [type], [status: defeated/active]

## Progress
- **Current Chapter**: [N]
- **Status**: In Progress / Completed
- **Last Updated**: [timestamp]
```

### summary.md (Story Memory)
```markdown
# [World Name] -- Story Summary

## Adventure Status
- **Started**: [date]
- **Current Chapter**: [N] in story-[M].md
- **Status**: In Progress / Completed

## Story So Far
[3-10 line concise narrative of everything that happened — key events, battles, NPCs met, items found, plot progression.]

## Current Situation
[2-3 lines: Where the hero is RIGHT NOW, what just happened, what's pending.]

## Key Decisions Made
- [Important player choices that affected the story]
```

### story-N.md Format
```markdown
# [World Name]
*[Date started]*

**Hero**: [Name] — [Class]
**Companion**: [Name] — [Class] (if Duo mode)
**Power**: [OP / Balanced]

---

## Chapter 1 -- [Chapter Title]

[Full rich light-novel narrative...]

## Chapter 2 -- [Chapter Title]

[Next scene with full prose...]
```

**1K line rotation**: When story-N.md reaches 1000 lines, create story-(N+1).md with a continuation header.

---

## Lifecycle Commands

### "new adventure"
1. Ask: Duo or Solo? → OP or Balanced?
2. Character creation (hero + companion if duo)
3. World type selection (or random)
4. Generate world → create adventure folder + setting.md + summary.md
5. If Song Creation System installed → generate Opening song
6. Start Chapter 1 with first scene + choice box

### "save adventure"
1. Write all scenes since last save to `story/story-N.md`
2. Update `summary.md` — Story So Far + Current Situation
3. Update `setting.md` — NPCs, items, enemies, progress
4. If Auto-Commit System installed → commit adventure files
5. Adventure continues after save

### "load adventure" / "resume adventure"
1. Scan `adventures/` for folders with `In Progress` status
2. If one → auto-select. If multiple → list for player to pick
3. Read `setting.md` (world facts, characters) + `summary.md` (story so far)
4. Read last ~50 lines of latest `story/story-N.md` (exact last scene)
5. Resume from Current Situation with recap + choice box

### "end adventure"
1. Write finale + epilogue to story file
2. Update `setting.md` Status → `Completed`
3. Update `summary.md` with final state + highlights
4. If Song Creation System installed → generate Ending song
5. Clear active adventure from session memory
6. If Auto-Commit System installed → commit files

---

## Session Memory Persistence

Active adventure state saved to `## Active Adventure` section in session memory. Survives auto-compact within the same session.

**Format (active)**:
```
## Active Adventure
- **World**: [name + brief description]
- **Adventure Path**: adventures/[world-name]/
- **Mode**: Duo / Solo | **Power**: OP / Balanced
- **Hero**: [name] — [class]
- **Companion**: [name] — [class] (Duo only)
- **Story Progress**: [2-3 sentence summary]
- **Current Scene**: [where they are right now]
- **Last Choice**: [what player chose last]
```

**Format (inactive)**:
```
## Active Adventure
- No active adventure
```

### Recovery (Auto-Compact)
1. Read `## Active Adventure` from session memory for adventure path
2. Read `summary.md` (story big picture)
3. Read last ~50 lines of latest story-N.md (exact last scene)
4. Resume seamlessly with recap + choice box

---

## Companion System Integration

These features enhance the adventure when installed. All are optional.

| System | Integration | How |
|--------|-------------|-----|
| **Image Prompt System** | Scene art for key moments | During or after adventure, use "create a prompt for [scene description]" |
| **Song Creation System** | Opening song on "new adventure", Ending song on "end adventure" | Auto-chains if installed — reads setting.md/summary.md |
| **Auto-Commit System** | Commits adventure files on save/end | Auto-chains if installed |
| **Save Diary** | Documents adventure sessions | Manual — "save diary" after adventure |

---

## Mandatory Rules

1. **Choice box mandatory** — every scene ends with choices. Never leave the player without options
2. **"Say something" always available** — free text option in every choice box
3. **VN format adherence** — scene headers, narration blocks, choice boxes consistently
4. **Rich mode** — light-novel quality prose. Write MORE, not less. Never compress or rush
5. **Minimum 2 combat exchanges** — every fight has choreography, never one-shot
6. **Prose, not numbers** — no HP, damage numbers, or XP. Describe through narrative
7. **Name every ability** — dramatic, anime/JRPG-style ability names
8. **Player is the main character** — NPCs serve the story, not the other way around
9. **Respect power level** — OP = always win stylishly. Balanced = real stakes with consequences
10. **Respect play mode** — Duo = companion is active character. Solo = AI is DM only
11. **Save on command only** — don't auto-save during choices. Save when player says "save adventure"
12. **Summary + last 50 lines on load** — read summary.md + last ~50 lines of story for resume context
13. **1K line rotation** — create story-(N+1).md when story-N.md exceeds 1000 lines
14. **Session memory persistence** — active adventure state in session memory for compact recovery
15. **Full story preservation** — on save/end, write ALL scenes as complete prose to story files. Never skip or summarize
