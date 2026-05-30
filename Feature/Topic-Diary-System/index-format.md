# Topic Diary Index Format
*Canonical format for `topic-diary/index.md`*

Use this format to catalog available topic diaries and make recall easier.

## File Template

```markdown
# Topic Diary Index
*Catalog of subject-based memory journals.*

## Active Topics

| Topic | File | Aliases | Recall Keywords | Last Updated |
|-------|------|---------|-----------------|--------------|
| Docker | `topics/docker.md` | containers, compose | docker, compose, ports, volumes | YYYY-MM-DD |

## Archived Topics

| Topic | File | Reason Archived | Archived Date |
|-------|------|-----------------|---------------|

## Save Routing Notes

- **Session memory**: immediate restart continuity
- **Daily diary**: session story and chronological record
- **Topic diary**: reusable knowledge organized by subject
- **All**: important information that belongs in multiple memory layers

## Maintenance Notes

- Add a row when creating a new topic file.
- Update `Last Updated` whenever a topic receives a new entry.
- Add aliases that users or AI might naturally use.
- Keep recall keywords short and search-friendly.
```

## Index Guidelines

- Keep one row per active topic.
- Use relative links or file paths that work from `topic-diary/index.md`.
- Include aliases for alternate spellings, tool names, or project names.
- Move old topics to the archived table only when the user explicitly archives them.
- If the index is lost, rebuild it by scanning `topic-diary/topics/*.md`.

---

*The index is the map; topic files are the memory.*
