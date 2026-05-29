# Install Topic Diary System
*Integration protocol for topic-based memory journals*

## Activation

When the user says `Load topic-diary`, install the Topic Diary System into the active MemoryCore.

## Prerequisites

- Existing MemoryCore root with `master-memory.md`
- Optional but recommended: Skill Plugin System
- Optional companion features: Save Diary System and Echo Memory Recall

## Installation Steps

### Step 1: Confirm MemoryCore Root

Locate the active MemoryCore root. It should contain:

```text
master-memory.md
main/
```

If the user's MemoryCore uses customized folder names, ask for confirmation before writing files.

### Step 2: Create Topic Diary Directories

Create these directories if missing:

```text
topic-diary/
topic-diary/topics/
topic-diary/archived/
```

Never delete or overwrite existing topic files.

### Step 3: Create Topic Index

If `topic-diary/index.md` does not exist, create it using `index-format.md`.

If it exists, append a short installation note instead of replacing it.

### Step 4: Add Master Memory References

Update `master-memory.md` with:

```markdown
### Topic Diary System
*Load when user says: "save topic", "save to topic diary", "remember this under [topic]", or when reusable knowledge should be preserved by subject.*
- Stores long-term knowledge in `topic-diary/topics/[topic].md`
- Uses `topic-diary/index.md` for topic aliases and recall keywords
- Complements Daily Diary and Session RAM
```

Also add save routing guidance:

```markdown
When user says "save" and the target is unclear, ask whether to save to session memory, daily diary, topic diary, or all relevant targets.
```

### Step 5: Install Skill Plugin

If Skill Plugin System is installed:

1. Copy `SKILL.md` into the configured skills/plugin folder as `topic-diary/SKILL.md`
2. Preserve existing skill files
3. Confirm the trigger phrases are available

If no Skill Plugin System is installed, leave the feature folder in place and record the manual commands in `master-memory.md`.

### Step 6: First Topic Entry

Ask whether the user wants to create a first topic entry.

Suggested prompt:

```text
Topic Diary is installed. Do you want to create a first topic entry now, or leave it ready for the next save?
```

## Commands After Installation

| Command | Behavior |
|---------|----------|
| `save topic` | Save current reusable knowledge to a topic diary |
| `save to topic diary` | Ask for or infer topic, then append entry |
| `remember this under [topic]` | Append to the named topic file |
| `review topic [topic]` | Read and summarize the topic diary |
| `list topics` | Show topics from `topic-diary/index.md` |
| `save` | Ask target if ambiguous: session, daily diary, topic diary, or all |

## Safety Rules

1. **Append only** — never overwrite topic entries
2. **Ask when ambiguous** — especially for generic `save`
3. **Keep layers distinct** — session memory is for continuity; diary is for story; topic diary is for reusable knowledge
4. **Use kebab-case filenames** — `Docker Compose` becomes `docker-compose.md`
5. **Update the index** after every new or changed topic
6. **Do not self-delete** this feature folder unless the user explicitly requests cleanup

## Uninstall

To uninstall manually:

1. Remove Topic Diary references from `master-memory.md`
2. Remove the installed `topic-diary` skill from the plugin folder
3. Keep `topic-diary/` unless the user explicitly wants to delete saved knowledge

---

*Topic Diary installs as a companion to memory, not a replacement for it.*
