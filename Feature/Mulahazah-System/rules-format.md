# Rules Format -- Mulahazah Learning Output
*The structure of rules.md and how rules are created, read, and maintained.*

## Overview

Rules are stored in `~/.claude/mulahazah/rules.md`. This file is written by `analyze.sh` and by session reflections. Your AI companion reads it at session start and follows the rules silently -- no reminders needed.

## File Structure

```markdown
# Learned Rules

Rules extracted from session observations by Mulahazah.
Remove any rule that causes problems. Keep what helps.

---

## YYYY-MM-DD analysis

- Rule: [specific actionable rule based on observed pattern]
- Rule: [another rule from the same analysis]

## YYYY-MM-DD analysis

- Rule: [rule from a different session]
```

## What Makes a Good Rule

Good rules are:

- **Specific** -- "Use Grep → Read → Edit for code modifications" not "Be careful when editing"
- **Actionable** -- describes what to do, not just what to avoid
- **Evidence-based** -- extracted from actual session observations, not invented
- **Self-maintaining** -- remove rules that cause problems, keep what helps

## Example Rules

```markdown
- Rule: Use Grep → Read → Edit workflow for code modifications -- search to locate, read to understand context, edit to apply
- Rule: Always check API rate limits before setting polling intervals -- prevents hitting quotas
- Rule: Run npm run build before committing -- catches type errors early
- Rule: When debugging, read the error message first before searching -- saves context window
```

## Rule Lifecycle

1. **Created** -- by `analyze.sh` (Haiku analysis of JSONL observations) or by Step 2 reflection ("Rule to add")
2. **Read** -- by your AI companion at session start from `~/.claude/mulahazah/rules.md`
3. **Reinforced** -- when the same pattern is observed again in a future session
4. **Removed** -- manually by you if a rule causes problems or no longer applies
