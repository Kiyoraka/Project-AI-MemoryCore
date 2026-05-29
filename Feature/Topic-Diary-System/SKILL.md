---
name: topic-diary
description: "MUST use when user says 'save topic', 'save to topic diary', 'remember this under', 'review topic', 'list topics', or when a generic 'save' request needs routing between session memory, daily diary, topic diary, or all targets."
---

# Topic Diary — Subject-Based Memory Skill
*A subject remembers what the calendar forgets.*

## Activation

When this skill activates for a topic save, output:

```text
Capturing this under the right topic.
```

For a generic `save` request, do not write immediately if the target is unclear. Ask one short routing question.

## Context Guard

| Context | Status |
|---------|--------|
| **User says "save topic"** | ACTIVE — topic diary write |
| **User says "save to topic diary"** | ACTIVE — topic diary write |
| **User says "remember this under [topic]"** | ACTIVE — named topic write |
| **User says "review topic [topic]"** | ACTIVE — read and summarize topic |
| **User says "list topics"** | ACTIVE — read topic index |
| **User says generic "save"** | ACTIVE — route save target before writing |
| **No save or recall request** | DORMANT — no topic diary action |

## Save Routing Protocol

When the user says `save`, `save memory`, `remember this`, or another ambiguous save phrase:

1. Infer the likely target from context.
2. If confidence is high, briefly state the target and proceed.
3. If unclear, ask:

```text
Save where: session memory, daily diary, topic diary, or all?
```

Use these rules:

| Target | Use When |
|--------|----------|
| **Session memory** | Needed to continue current work after restart |
| **Daily diary** | Captures session story, collaboration, or achievements |
| **Topic diary** | Captures reusable knowledge about a subject |
| **All** | Information is both immediately important and reusable long-term |

## Topic Save Protocol

### Step 1: Determine Topic

- [ ] Use explicit topic if user says `under [topic]`
- [ ] Otherwise infer from session context
- [ ] If uncertain, ask one short question:

```text
Which topic should I save this under?
```

### Step 2: Normalize Topic Filename

- [ ] Convert topic to lowercase kebab-case
- [ ] Remove unsafe path characters
- [ ] Use `topic-diary/topics/[topic].md`
- [ ] Examples:
  - `Docker Compose` -> `docker-compose.md`
  - `9router Kiro` -> `9router-kiro.md`
  - `Writing Style` -> `writing-style.md`

### Step 3: Create Topic File If Missing

If the topic file does not exist, create it using `topic-format.md` header structure:

```markdown
# [Topic Name] Topic Diary
*Reusable discoveries, fixes, decisions, and lessons for this subject.*

## Topic Metadata
- **Created**: [date]
- **Last Updated**: [date]
- **Aliases**: [related names]
- **Recall Keywords**: [search terms]

---
```

### Step 4: Compose Entry

- [ ] Get real timestamp via platform command
- [ ] Write a concise, evidence-based entry using these sections:
  - Context
  - Discovery
  - Confirmed Details
  - Pitfalls
  - Recall Keywords
  - Follow-ups
- [ ] Include commands, paths, links, error messages, and decisions when relevant
- [ ] Avoid raw transcript dumps

### Step 5: Append Entry

- [ ] Append with `---` separator
- [ ] Never overwrite previous entries
- [ ] Keep entries concise and high-signal

### Step 6: Update Index

- [ ] Create `topic-diary/index.md` if missing using `index-format.md`
- [ ] Add topic if new
- [ ] Update latest date, aliases, and recall keywords

### Step 7: Confirm

Confirm the save target and file:

```text
Saved to topic diary: topic-diary/topics/[topic].md
```

## Review Protocol

When user says `review topic [topic]`:

1. Open the matching topic file.
2. Summarize current understanding.
3. Highlight confirmed facts, open questions, and latest entries.
4. Mention the source file path.

## List Protocol

When user says `list topics`:

1. Read `topic-diary/index.md`.
2. Show topic names, aliases, and latest update.
3. If the index is missing, scan `topic-diary/topics/` and offer to rebuild it.

## Mandatory Rules

1. **Always append** — never overwrite topic entries
2. **Ask when ambiguous** — generic `save` must route to the correct memory layer
3. **Keep memory layers distinct** — session, daily diary, and topic diary have different purposes
4. **Use real timestamps** — do not invent dates or times
5. **Prefer evidence** — save verified commands, paths, decisions, and lessons
6. **Update index** — every topic write should keep recall metadata fresh
7. **Respect privacy** — do not save sensitive secrets, tokens, or credentials into topic files

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| No `topic-diary/` folder | Create required directories first |
| Topic unclear | Ask for topic name before writing |
| User says `save all` | Save to all relevant memory layers, if available |
| Sensitive content detected | Ask before saving or redact secrets |
| Topic file too large | Suggest archive or split, but do not delete content |
| Index missing | Recreate from existing topic files |

## Level History

- **Lv.1** — Base: topic-based append-only journals, save target routing, topic index updates, and review/list commands.
