# 🩹 Patch File - Standard Format
*Reference template for creating AI-executable patch files*

## Frontmatter (Required)

Every patch file begins with metadata:

```yaml
---
patch-id: PATCH-XXX
title: "Human-readable title of what this patch fixes"
version: 1.0.0
priority: critical | high | medium | low
date: YYYY-MM-DD
affects:
  - path/to/file1.md
  - path/to/file2.md
prerequisites:
  - PATCH-000
  - none
compatibility:
  pre-consolidation: true | false
  post-consolidation: true | false
---
```

### Field Descriptions
| Field | Required | Description |
|-------|----------|-------------|
| `patch-id` | Yes | Unique ID (PATCH-001, PATCH-002, etc.) |
| `title` | Yes | Short description of what this patch fixes |
| `version` | Yes | Semantic version of the fix |
| `priority` | Yes | Urgency level (critical/high/medium/low) |
| `date` | Yes | Date the patch was created (YYYY-MM-DD) |
| `affects` | Yes | List of files modified by this patch |
| `prerequisites` | Yes | List of patch IDs that must be applied first, or `none` |
| `compatibility` | Yes | Whether patch works with pre/post Memory Consolidation states |

## Patch Body Structure

### Per-File Sections

Each affected file gets its own section with numbered changes:

```markdown
## File: path/to/affected-file.md

### Change 1: [Description of this specific change]

**Section**: [Name of the section in the file being modified]
**Action**: replace

#### FIND:
```
[Exact text to locate in the file — include enough context for unambiguous matching]
```

#### REPLACE:
```
[New text that replaces the FIND block]
```
```

### Available Actions

#### Action: `replace`
Find exact text and replace with new text.

```markdown
**Action**: replace

#### FIND:
```
Original text to locate
```

#### REPLACE:
```
New text to put in its place
```
```

#### Action: `insert-after`
Find anchor text and insert new content after it.

```markdown
**Action**: insert-after

#### FIND:
```
Anchor text to locate (stays unchanged)
```

#### INSERT-AFTER:
```
New text added after the anchor
```
```

#### Action: `insert-before`
Find anchor text and insert new content before it.

```markdown
**Action**: insert-before

#### FIND:
```
Anchor text to locate (stays unchanged)
```

#### INSERT-BEFORE:
```
New text added before the anchor
```
```

#### Action: `remove`
Find exact text and remove it entirely.

```markdown
**Action**: remove

#### FIND:
```
Text to remove entirely from the file
```

#### REMOVE: yes
```

## Conditional Sections

For patches that need different behavior based on system state (e.g., whether Memory Consolidation has been run):

```markdown
### Change N: [Description] (CONDITIONAL)

**Condition**: IF `main/main-memory.md` exists (post-consolidation)

**Action**: replace

#### FIND:
```
[Post-consolidation version of the text]
```

#### REPLACE:
```
[Post-consolidation replacement]
```

---

**Condition**: IF `main/identity-core.md` exists (pre-consolidation)

**Action**: replace

#### FIND:
```
[Pre-consolidation version of the text]
```

#### REPLACE:
```
[Pre-consolidation replacement]
```
```

**Rules for conditional sections:**
- AI checks file existence to determine which condition applies
- Only ONE condition branch is executed per change
- If neither condition is met, skip the change and note it in verification

## Verification Section (Required)

Every patch must end with a verification checklist:

```markdown
## Verification

After applying all changes, verify:

1. [ ] [Specific check — e.g., "master-memory.md line 83 now references daily-diary-protocol.md"]
2. [ ] [Another check — e.g., "save-protocol.md no longer references critical-thinking.md"]
3. [ ] No broken markdown formatting in any modified file
4. [ ] All FIND blocks were located and replaced successfully
5. [ ] Record patch in patches/applied.md with timestamp
```

## Rollback Section (Required)

Every patch must include rollback instructions:

```markdown
## Rollback

To undo this patch:
1. Reverse each FIND/REPLACE block (current REPLACE becomes FIND, current FIND becomes REPLACE)
2. Apply in reverse order (last change first, first change last)
3. For insert-after/insert-before: remove the inserted text
4. For remove: re-insert the removed text at its original location
5. Remove patch entry from patches/applied.md
```

## Format Rules

1. **FIND blocks must be unambiguous** — include enough surrounding context (2-3 lines) so the text appears only once in the target file
2. **Use text matching, not line numbers** — line numbers shift when files are edited; text matching is robust
3. **Whitespace matters** — FIND text must match exactly, including indentation
4. **One patch = one logical fix** — a patch can span multiple files but should address one issue
5. **Sequential application** — patches are numbered and applied in order (PATCH-001 before PATCH-002)
6. **Template placeholders** — if the target repo uses `[AI_NAME]`/`[YOUR_NAME]` placeholders and the user has personalized their files, note this in the patch so the AI can adapt FIND text

## Example Patch Structure

```markdown
---
patch-id: PATCH-001
title: "Fix broken file references"
version: 1.0.0
priority: high
date: 2026-02-24
affects:
  - master-memory.md
  - save-protocol.md
prerequisites:
  - none
compatibility:
  pre-consolidation: true
  post-consolidation: true
---

# PATCH-001: Fix Broken File References

## Summary
Fixes file paths that reference non-existent files.

## File: master-memory.md

### Change 1: Fix diary format reference

**Section**: Session Diary (Optional Components)
**Action**: replace

#### FIND:
- Format: daily-diary/diary-entry-format.md

#### REPLACE:
- Format: daily-diary/daily-diary-protocol.md

## Verification
1. [ ] master-memory.md references correct diary format path
2. [ ] No broken markdown formatting
3. [ ] Record in patches/applied.md

## Rollback
Reverse each FIND/REPLACE block above. Apply in reverse order.
```

---

**Version**: Format v1.0 - AI-Executable Patch Standard
**Last Updated**: February 2026
**Status**: Permanent format reference for all patch files

*Structured, traceable, reversible — every change accounted for*
