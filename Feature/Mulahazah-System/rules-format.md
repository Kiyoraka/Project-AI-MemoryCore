# Rules Format — Mulahazah Learning Output

Rules are stored in `~/.claude/mulahazah/rules.md` using this format:

## Structure

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

## Rule Qualities

Good rules are:
- **Specific** — "Use Grep → Read → Edit for code modifications" not "Be careful when editing"
- **Actionable** — describes what to do, not just what to avoid
- **Evidence-based** — extracted from actual session observations
- **Self-maintaining** — remove rules that cause problems, keep what helps

## Example Rules

```markdown
- Rule: Use Grep → Read → Edit workflow for code modifications: search to locate changes, read to understand context, edit to apply changes
- Rule: Always check API rate limits before setting polling intervals — prevents hitting quotas
- Rule: Run npm run build before committing — catches type errors early
- Rule: When debugging, read the error message first before searching — saves context window
```

## Lifecycle

1. **Created** by `analyze.sh` (Haiku analysis of JSONL observations) or by Law 5 reflection ("Rule to add")
2. **Read** by the agent at session start from `~/.claude/mulahazah/rules.md`
3. **Reinforced** when the same pattern is observed again
4. **Removed** manually by the user if a rule causes problems
