# Topic Diary System
*Topic-based memory journals for discoveries, fixes, and reusable knowledge*

## What This Feature Does

Adds a structured topic diary system to your AI companion, enabling **knowledge-by-topic documentation** that captures discoveries, fixes, commands, lessons, and decisions across many sessions.

- **Topic-based journals** in `topic-diary/topics/` instead of only date-based diary files
- **Append-only entries** for each topic, preserving chronological learning history
- **Topic index** in `topic-diary/index.md` for quick scanning and recall
- **Save routing** for ambiguous `save` requests: session memory, daily diary, topic diary, or multiple targets
- **Skill auto-install** if Skill Plugin System is detected

## How It Works

### The Concept

Daily Diary answers: **What happened today?**

Topic Diary answers: **What have we learned about this subject over time?**

The system turns repeated discoveries into living notebooks. Instead of losing Docker fixes, project setup details, debugging patterns, or research insights inside dated session entries, your AI appends them to a focused topic file.

### Example: Saving a Technical Discovery

```text
You: "save this"
AI: "Save where: session, daily diary, topic diary, or all? I detected topic: docker."
You: "topic diary"
AI:
  1. Creates or opens topic-diary/topics/docker.md
  2. Appends a timestamped entry with the confirmed command, root cause, and lesson
  3. Updates topic-diary/index.md with docker keywords and latest update
  4. Confirms the save target and topic
```

### How It Differs From Daily Diary

| Aspect | Daily Diary | Topic Diary |
|--------|-------------|-------------|
| **Primary question** | What happened today? | What have we learned about this topic? |
| **Organization** | By date | By subject |
| **Best for** | Session story, achievements, collaboration | Reusable knowledge, fixes, commands, patterns |
| **Recall path** | Search by date/session | Open one focused topic file |
| **Examples** | "April 8 session recap" | `docker.md`, `9router.md`, `writing-style.md` |

## Directory Structure

```text
topic-diary/
├── index.md                         # Topic catalog and recall map
├── topics/                          # Active topic journals
│   ├── docker.md                    # Docker discoveries and fixes
│   ├── 9router.md                   # 9router setup, patches, troubleshooting
│   └── writing-style.md             # Preferences and writing patterns
└── archived/                        # Optional archived topics
    └── old-project.md
```

## Quick Integration

```text
"Load topic-diary"
```

## What Happens During Integration

1. **Creates** `topic-diary/topics/` and `topic-diary/archived/` directories
2. **Creates** `topic-diary/index.md` using `index-format.md`
3. **Adds** topic diary commands and save-routing behavior to `master-memory.md`
4. **Installs as skill** if Skill Plugin System is detected
5. **Keeps Daily Diary unchanged** so chronological and topic-based memory can coexist

## Post-Integration Result

After running the integration protocol:

- Your AI can route `save` requests to session memory, daily diary, topic diary, or all targets
- Every topic save appends to a focused markdown journal
- The index tracks available topics, aliases, latest updates, and recall keywords
- Daily Diary remains available for session storytelling
- Echo Memory Recall can use topic files as high-signal recall sources

## Save Routing

When the user says `save`, `save memory`, or `remember this`, the AI should determine the best save target:

| Target | Use When |
|--------|----------|
| **Session memory** | Needed for immediate continuation after restart |
| **Daily diary** | Captures the story or recap of a session |
| **Topic diary** | Captures reusable knowledge about a subject |
| **All** | Important information belongs in multiple memory layers |

If the save target is ambiguous, ask one short question before writing.

## Entry Sections

Each topic entry follows `topic-format.md` and captures:

| Section | What It Captures |
|---------|------------------|
| **Context** | Why the topic came up and what was being solved |
| **Discovery** | What was learned or decided |
| **Confirmed Details** | Commands, paths, settings, examples, or facts verified in-session |
| **Pitfalls** | Mistakes, false assumptions, warnings, or edge cases |
| **Recall Keywords** | Search terms and aliases for future retrieval |
| **Follow-ups** | Optional next steps or unanswered questions |

## Benefits

- **Faster recall** — recurring subjects have one focused knowledge file
- **Less noise** — reusable facts do not get buried in date-based diary entries
- **Better debugging memory** — commands, root causes, and verified fixes stay together
- **Works with existing MemoryCore** — complements Daily Diary, Session RAM, and Echo Recall
- **Portable** — plain markdown files, human-readable and AI-readable

## Platform Note

Works with any AI system. Uses plain markdown files and optional shell timestamp commands. Auto-triggered skill requires Claude Code with the Skill Plugin System.

---

*A subject remembers what the calendar forgets.*
