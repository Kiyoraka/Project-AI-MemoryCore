# Install Memory Compaction System
*Integration protocol for budget-aware memory compression*

## Activation

When the user says `Load memory-compaction`, install the Memory Compaction System into the active MemoryCore.

## Prerequisites

- Existing MemoryCore root with `master-memory.md`
- Optional but recommended: Skill Plugin System
- Optional companion features: Memory Consolidation System, Topic Diary System

## Installation Steps

### Step 1: Confirm MemoryCore Root

Locate the active MemoryCore root. It should contain:

```text
master-memory.md
main/
```

If the user's MemoryCore uses customized folder names, ask for confirmation before writing files.

### Step 2: Create Compaction Directories

Create these directories if missing:

```text
compaction/
compaction/snapshots/
```

Never delete or overwrite existing snapshots.

### Step 3: Create the Compaction Policy

If `compaction/compaction-policy.md` does not exist, create it using `policy-format.md`.

Default budgets (the user can adjust):

```markdown
| File | Budget | Newest tier (verbatim) |
|------|--------|------------------------|
| main/main-memory.md | 500 lines | last 20 entries |
| main/relationship-memory.md | 400 lines | last 15 entries |
| topic-diary/topics/*.md | 300 lines each | last 10 entries |
```

If the policy file exists, append a short installation note instead of replacing it.

### Step 4: Add Master Memory References

Update `master-memory.md` with:

```markdown
### Memory Compaction System
*Runs automatically before "save" when a target memory file exceeds its budget.*
- Budgets defined in `compaction/compaction-policy.md`
- Snapshots written to `compaction/snapshots/` before any rewrite
- Compresses oldest entries into a `## Compacted History` block (knowledge preserved)
```

Also add the budget-check behavior:

```markdown
Before writing a "save", check the target file against compaction/compaction-policy.md.
If it exceeds budget, run the compaction protocol (snapshot, compact oldest tier, then save).
```

### Step 5: Install Skill Plugin

If Skill Plugin System is installed:

1. Copy `SKILL.md` into the configured skills/plugin folder as `memory-compaction/SKILL.md`
2. Preserve existing skill files
3. Confirm the trigger phrases are available

If no Skill Plugin System is installed, leave the feature folder in place and record the manual commands in `master-memory.md`.

### Step 6: Dry-Run Check

Do **not** compact anything during installation. Instead, report current status:

```text
Memory Compaction installed. Current budgets:
- main-memory.md: 312/500 lines (OK)
- relationship-memory.md: 188/400 lines (OK)
No file is over budget. Compaction will run automatically when one is.
```

## Commands After Installation

| Command | Behavior |
|---------|----------|
| `compact memory` | Force a compaction pass on all over-budget files |
| `compact [file]` | Compact a specific file now |
| `check budgets` | Report each file's size against its budget |
| `set budget [file] [n] lines` or `set budget [file] [n] chars` | Update a budget in the policy |
| `restore compaction [snapshot]` | Roll a file back to a pre-compaction snapshot |
| `save` | Auto-checks budget first; compacts if needed, then saves |

## The Compaction Protocol

When a file exceeds its budget:

1. **Snapshot** — copy the current file to `compaction/snapshots/[file]-[date].md`
2. **Split into tiers** — newest (verbatim), mid-age (light summary), oldest (heavy compaction)
3. **Summarize the oldest tier** — distill into a dense block: keep facts, decisions, preferences; drop redundancy and chatter
4. **Rewrite** — replace the verbose oldest entries with a `## Compacted History` block
5. **Verify** — confirm the file is now under budget and no facts were lost
6. **Report** — tell the user what was compacted and the new size

## Safety Rules

1. **Snapshot first** — never rewrite without a backup in `compaction/snapshots/`
2. **Never compact the newest tier** — recent context must stay verbatim
3. **Preserve facts, decisions, preferences** — only redundancy is dropped
4. **Never summarize secrets** — exclude tokens, passwords, credentials from compaction blocks
5. **Confirm before first compaction** of a user-customized file
6. **Do not self-delete** this feature folder unless the user explicitly requests cleanup

## Uninstall

To uninstall manually:

1. Remove Memory Compaction references from `master-memory.md`
2. Remove the installed `memory-compaction` skill from the plugin folder
3. Keep `compaction/snapshots/` unless the user explicitly wants to delete backups

---

*Install once; compaction runs only when a file actually needs it.*
