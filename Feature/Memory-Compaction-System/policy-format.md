# Compaction Policy Format
*Canonical format for `compaction/compaction-policy.md`*

Use this format to define which files are compacted, their budgets, and how much stays verbatim.

## File Template

```markdown
# Compaction Policy
*Budgets and retention tiers for memory compaction.*

## Active Budgets

| File | Budget | Newest Tier (verbatim) | Notes |
|------|--------|------------------------|-------|
| main/main-memory.md | 500 lines | last 20 entries | core identity + user profile |
| main/relationship-memory.md | 400 lines | last 15 entries | user preferences |
| topic-diary/topics/*.md | 300 lines each | last 10 entries | per-topic journals |

## Retention Tiers

- **Newest tier** — kept verbatim, never compacted.
- **Mid-age tier** — light summarization (merge near-duplicate lines, trim filler).
- **Oldest tier** — heavy compaction into a single `## Compacted History` block.

## Compaction Triggers

- Before any `save` that targets a budgeted file.
- On the explicit `compact memory` command.
- Never automatically on files not listed in this policy.

## Exclusions

- Never compact files under `compaction/snapshots/`.
- Never compact secrets, tokens, passwords, or credentials.
- Never compact the newest tier.

## Maintenance Notes

- Budgets are line-based by default; character-based budgets are allowed (e.g. `8000 chars`).
- Adjust budgets to fit your model's context window.
- Lower the budget for files you want kept very tight; raise it for reference-heavy files.
```

## Policy Guidelines

- Keep one row per budgeted file (globs like `topics/*.md` are allowed).
- Express budgets in `lines` or `chars` — pick one unit per file and state it.
- The newest tier should always be large enough to hold active working context.
- If a file is not in the policy table, it is **never** compacted.

## Good Policy Example

```markdown
## Active Budgets

| File | Budget | Newest Tier (verbatim) | Notes |
|------|--------|------------------------|-------|
| main/main-memory.md | 450 lines | last 25 entries | keep identity dense |
| topic-diary/topics/docker.md | 250 lines | last 8 entries | high-churn topic |
| topic-diary/topics/9router.md | 200 lines | last 8 entries | troubleshooting log |
```

---

*The policy is the contract; compaction only does what the policy allows.*
