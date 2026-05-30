# Topic Diary Format
*Canonical format for `topic-diary/topics/[topic].md` files*

Use this format for every topic diary file.

## File Naming

Topic filenames use lowercase kebab-case:

```text
topic-diary/topics/docker.md
topic-diary/topics/docker-compose.md
topic-diary/topics/9router.md
topic-diary/topics/writing-style.md
```

## File Template

```markdown
# [Topic Name] Topic Diary
*Reusable discoveries, fixes, decisions, and lessons for this subject.*

## Topic Metadata
- **Created**: YYYY-MM-DD HH:MM
- **Last Updated**: YYYY-MM-DD HH:MM
- **Aliases**: [alias 1], [alias 2]
- **Recall Keywords**: [keyword 1], [keyword 2], [keyword 3]

---

## YYYY-MM-DD HH:MM — [Entry Title]

### Context
- What prompted this discovery or save?
- What problem, project, or question was being handled?

### Discovery
- What did we learn, decide, or confirm?
- Why does it matter for future sessions?

### Confirmed Details
- Commands, paths, settings, examples, or facts verified during the session.
- Include exact errors or outputs when useful.

### Pitfalls
- Mistakes, false assumptions, warnings, or edge cases to avoid.

### Recall Keywords
- Keywords and aliases future AI sessions should use to find this entry.

### Follow-ups
- Optional next steps, unresolved questions, or related topics.
```

## Entry Guidelines

- Keep entries concise and high-signal.
- Prefer verified facts over speculation.
- Include exact commands, paths, and error messages when useful.
- Do not save secrets, tokens, passwords, or private credentials.
- Append new entries below older entries, separated by `---`.
- Update `Last Updated` and recall keywords after each write.

## Good Entry Example

```markdown
---

## 2026-04-08 14:30 — Docker Compose Port Conflict Fix

### Context
- Local service failed to start because Docker reported port 3000 was already allocated.
- User was testing a web app through Docker Compose.

### Discovery
- The conflict came from an old container still binding port 3000.
- Removing the stopped container freed the port and allowed the stack to start.

### Confirmed Details
- `docker ps -a` showed the old container.
- `docker rm [container]` removed it.
- `docker compose up -d` started successfully after cleanup.

### Pitfalls
- `docker compose down` only affects the current compose project. It may not remove unrelated containers using the same port.

### Recall Keywords
- docker, compose, port conflict, address already in use, container cleanup

### Follow-ups
- Consider documenting common Docker cleanup commands in a separate Docker topic entry.
```

---

*A topic diary is a living notebook, not a transcript.*
