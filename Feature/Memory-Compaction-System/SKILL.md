---
name: memory-compaction
description: "MUST use when user says 'compact memory', 'compact [file]', 'check budgets', 'set budget', 'restore compaction', or before any 'save' whose target memory file exceeds its budget in compaction/compaction-policy.md."
---

# Memory Compaction — Budget-Aware Memory Skill
*Keep memory small without making it forget.*

## Activation

When this skill activates for a compaction pass, output:

```text
Checking memory budgets before saving.
```

Never rewrite a memory file without first writing a snapshot.

## Context Guard

| Context | Status |
|---------|--------|
| **User says "compact memory"** | ACTIVE — compact all over-budget files |
| **User says "compact [file]"** | ACTIVE — compact one file |
| **User says "check budgets"** | ACTIVE — report sizes vs budgets |
| **User says "set budget ..."** | ACTIVE — update policy |
| **User says "restore compaction ..."** | ACTIVE — roll back from snapshot |
| **Generic "save" on a budgeted file over budget** | ACTIVE — compact then save |
| **Save on a file under budget** | DORMANT — save normally |
| **No save or compaction request** | DORMANT — no action |

## Budget Check Protocol

Before writing any `save` to a budgeted file:

1. Read `compaction/compaction-policy.md` for the file's budget and newest-tier size.
2. Measure the current file (lines or chars per the policy unit).
3. If under budget → save normally, no compaction.
4. If over budget → run the Compaction Protocol below, then save.

## Compaction Protocol

### Step 1: Snapshot

- [ ] Run `date` to get the current timestamp.
- [ ] Copy the target file to `compaction/snapshots/[basename]-[YYYY-MM-DD].md`
      (use only the filename without its directory — e.g. `main-memory`, not `main/main-memory` —
      so snapshots never create nested subdirectories inside `compaction/snapshots/`).
- [ ] If a snapshot for today already exists, append `-HHMMSS` (seconds included) to avoid
      overwriting. If a same-second collision is still possible, use a sequential suffix
      (`-v2`, `-v3`).

### Step 2: Split Into Tiers

- [ ] **Newest tier** — the last N entries per the policy. Never touched.
- [ ] **Mid-age tier** — entries between newest and oldest. Light summarization only.
- [ ] **Oldest tier** — everything older. Target for heavy compaction.

> **Deterministic boundary:** the newest tier is the last N entries named in the policy.
> The oldest tier is everything below the newest tier, down to **30% of the file's total
> line count** (rounded to whole entries). Anything between is the mid-age tier. This keeps
> compaction results consistent across sessions.

### Step 3: Compact the Oldest Tier

- [ ] Read every entry in the oldest tier.
- [ ] Distill into a dense summary that keeps:
  - Verified facts, paths, commands, and settings
  - Decisions and the reasons behind them
  - User preferences and recurring corrections
- [ ] Drop:
  - Redundant or duplicated statements
  - Resolved chatter and one-off context
  - Filler and transitional notes
- [ ] **Never** include secrets, tokens, passwords, or credentials in the summary.

### Step 4: Rewrite

- [ ] Replace the verbose oldest-tier entries with a single block:

```markdown
## Compacted History
*Distilled from [N] entries on [YYYY-MM-DD]. Full detail in compaction/snapshots/[file]-[date].md.*

- [fact / decision / preference, one dense bullet each]
```

- [ ] Keep the mid-age and newest tiers in place.
- [ ] Append the new save below.

### Step 5: Verify and Report

- [ ] Confirm the file is now under budget.
- [ ] Confirm no fact, decision, or preference was lost (compare against snapshot if unsure).
- [ ] Report:

```text
Compacted [N] entries ([X] lines) into a [Y]-line history block.
[file] is now [Z]/[budget] lines. Snapshot: compaction/snapshots/[file]-[date].md
```

## Restore Protocol

When the user says `restore compaction [snapshot]`:

1. Confirm the snapshot exists in `compaction/snapshots/`.
2. Show the user the snapshot date and size.
3. Ask for confirmation before overwriting the current file.
4. Replace the current file with the snapshot contents.

## Safety Rules

1. **Snapshot before every compaction** — no exceptions.
2. **Never compact the newest tier.**
3. **Preserve all facts, decisions, and preferences.**
4. **Never summarize secrets** into a shared `Compacted History` block.
5. **Confirm before first compaction** of a user-customized file.
6. **Compaction is summarization, not deletion** — knowledge moves to a denser form, it does not disappear.

---

*A good compaction is one the user never notices, except that memory stopped overflowing.*
