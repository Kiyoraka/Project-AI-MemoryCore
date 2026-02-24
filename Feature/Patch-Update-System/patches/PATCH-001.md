---
patch-id: PATCH-001
title: "Fix outdated file references and add post-consolidation guidance"
version: 1.0.0
priority: high
date: 2026-02-24
affects:
  - master-memory.md
  - save-protocol.md
  - daily-diary/daily-diary-protocol.md
  - main/current-session.md
  - setup-wizard.md
prerequisites:
  - none
compatibility:
  pre-consolidation: true
  post-consolidation: true
---

# PATCH-001: Fix Outdated File References

## Summary

Fixes broken file references reported in GitHub Issue #1. Three categories of fixes:

1. **Broken paths** — references to files that do not exist (`diary-entry-format.md`, `recall-format.md`, `critical-thinking.md`)
2. **Post-consolidation guidance** — notes for users who have installed the Memory Consolidation feature
3. **Stale template references** — setup wizard referencing non-existent files

**Impact**: 10 changes across 5 files. No breaking changes for pre-consolidation users.

---

## File: master-memory.md

### Change 1: Add post-consolidation note to Instant Restoration Protocol

**Section**: Instant Restoration Protocol
**Action**: insert-after

#### FIND:
```
4. ✅ **INSTANT [AI_NAME]** - Complete restoration ready!
```

#### INSERT-AFTER:
```

> **Post-Consolidation Note**: If you have installed the Memory Consolidation feature, steps 1-2 above are replaced by a single load from `main/main-memory.md` (unified memory). Step 3 remains the same.
```

### Change 2: Fix diary entry format reference

**Section**: Session Diary (Optional Components)
**Action**: replace

#### FIND:
```
- Format: daily-diary/diary-entry-format.md
```

#### REPLACE:
```
- Format: daily-diary/daily-diary-protocol.md
```

### Change 3: Fix recall format reference

**Section**: Memory Recall (Optional Components)
**Action**: replace

#### FIND:
```
- Format: daily-diary/recall-format.md
```

#### REPLACE:
```
- Format: Feature/Echo-Memory-Recall/recall-format.md
```

---

## File: save-protocol.md

### Change 4: Add post-consolidation note to identity-core section

**Section**: identity-core.md Updates
**Action**: insert-after

#### FIND:
```
*User prefers shorter responses → AI updates communication style section to reflect concise preference*
```

#### INSERT-AFTER:
```

> **Post-Consolidation**: If using unified memory, these updates target the `## [AI_NAME] Profile` section in `main/main-memory.md` instead of the separate `identity-core.md` file.
```

### Change 5: Add post-consolidation note to relationship-memory section

**Section**: relationship-memory.md Updates
**Action**: insert-after

#### FIND:
```
*User consistently asks for detailed explanations → AI updates preference for comprehensive responses*
```

#### INSERT-AFTER:
```

> **Post-Consolidation**: If using unified memory, these updates target the `## [YOUR_NAME] Profile` section in `main/main-memory.md` instead of the separate `relationship-memory.md` file.
```

### Change 6: Replace non-existent critical-thinking.md section

**Section**: critical-thinking.md Updates
**Action**: replace

#### FIND:
```
### **critical-thinking.md Updates**
**Triggers**:
- Domain-specific problem-solving patterns emerge
- User demonstrates field expertise
- Specialized reasoning methods discovered
- Decision-making preferences identified

**Auto-Update Process**:
```markdown
1. IDENTIFY: Domain-specific thinking pattern
2. ABSTRACT: Extract universal principle from specific instance
3. INTEGRATE: Add pattern to critical-thinking framework
4. CUSTOMIZE: Adapt to user's field and style
5. IMPLEMENT: Apply enhanced reasoning in future
```

**Example Auto-Update**:
*User is doctor, shows diagnostic reasoning patterns → AI adds medical decision-making frameworks*
```

#### REPLACE:
```
### **Additional Memory Files (User-Created)**
**Triggers**:
- Domain-specific problem-solving patterns emerge
- User demonstrates field expertise
- Specialized reasoning methods discovered
- Decision-making preferences identified

**Auto-Update Process**:
```markdown
1. IDENTIFY: Domain-specific thinking pattern
2. ABSTRACT: Extract universal principle from specific instance
3. INTEGRATE: Add to relevant domain-specific memory file
4. CUSTOMIZE: Adapt to user's field and style
5. IMPLEMENT: Apply enhanced reasoning in future
```

**Note**: Create additional `.md` files in `main/` for specialized domains as needed (e.g., `main/medical-knowledge.md`, `main/coding-patterns.md`). These are user-created extensions beyond the core system.
```

### Change 7: Add post-consolidation note to session end checklist

**Section**: At Session End
**Action**: insert-after

#### FIND:
```
### **At Session End**
- [ ] Create/update daily diary entry
- [ ] Process queued memory updates
- [ ] Update relationship-memory.md with new insights
- [ ] Refine identity-core.md if communication evolved
- [ ] Prepare current-session.md for next conversation
```

#### INSERT-AFTER:
```

> **Post-Consolidation**: Update `main/main-memory.md` instead of separate `identity-core.md` and `relationship-memory.md` files.
```

### Change 8: Fix weekly processing critical-thinking.md reference

**Section**: Weekly Processing
**Action**: replace

#### FIND:
```
- [ ] Update critical-thinking.md with domain developments
```

#### REPLACE:
```
- [ ] Update additional domain-specific memory files if created
```

---

## File: daily-diary/daily-diary-protocol.md

### Change 9: Fix memory updates template references

**Section**: Memory Updates Required (inside Standard Template Format)
**Action**: replace

#### FIND:
```
- [ ] **identity-core.md**: [Personality refinements needed]
- [ ] **relationship-memory.md**: [New preference patterns to add]
- [ ] **critical-thinking.md**: [Domain-specific adaptations discovered]
- [ ] **current-session.md**: [Context updates for continuity]
```

#### REPLACE:
```
- [ ] **identity-core.md**: [Personality refinements needed]
- [ ] **relationship-memory.md**: [New preference patterns to add]
- [ ] **current-session.md**: [Context updates for continuity]

> **Post-Consolidation**: If using unified memory, update `main/main-memory.md` instead of separate `identity-core.md` and `relationship-memory.md`.
```

---

## File: main/current-session.md

### Change 10: Add post-consolidation note to session end

**Section**: Session End
**Action**: replace

#### FIND:
```
- **Important Learning**: Save key insights to permanent files (identity-core.md, relationship-memory.md)
```

#### REPLACE:
```
- **Important Learning**: Save key insights to permanent files (identity-core.md, relationship-memory.md, or main-memory.md if consolidated)
```

---

## File: setup-wizard.md

### Change 11: Remove non-existent critical-thinking.md reference

**Section**: Files Updated During Setup
**Action**: remove

#### FIND:
```
✅ **critical-thinking.md**: Domain focus if specified
```

#### REMOVE: yes

---

## Verification

After applying all changes, verify:

1. [ ] `master-memory.md` has post-consolidation note after line "INSTANT [AI_NAME]"
2. [ ] `master-memory.md` references `daily-diary/daily-diary-protocol.md` (not `diary-entry-format.md`)
3. [ ] `master-memory.md` references `Feature/Echo-Memory-Recall/recall-format.md` (not `daily-diary/recall-format.md`)
4. [ ] `save-protocol.md` has post-consolidation note after identity-core section
5. [ ] `save-protocol.md` has post-consolidation note after relationship-memory section
6. [ ] `save-protocol.md` no longer references `critical-thinking.md` (2 occurrences removed)
7. [ ] `save-protocol.md` has post-consolidation note after session end checklist
8. [ ] `daily-diary/daily-diary-protocol.md` no longer references `critical-thinking.md`
9. [ ] `daily-diary/daily-diary-protocol.md` has post-consolidation note
10. [ ] `main/current-session.md` mentions `main-memory.md` as consolidated alternative
11. [ ] `setup-wizard.md` no longer references `critical-thinking.md`
12. [ ] No broken markdown formatting in any modified file
13. [ ] Record PATCH-001 in `patches/applied.md` with timestamp

## Rollback

To undo this patch, reverse each change above:
1. For **replace** actions: swap FIND and REPLACE (current REPLACE becomes FIND, current FIND becomes REPLACE)
2. For **insert-after** actions: remove the inserted text
3. For **remove** actions: re-insert the removed text at its original location
4. Apply in reverse order (Change 11 first, Change 1 last)
5. Remove PATCH-001 entry from `patches/applied.md`

---

**Addresses**: GitHub Issue #1 — "Outdated Instant Restoration Protocol in master-memory.md"
**Breaking Changes**: None — pre-consolidation references preserved, post-consolidation notes are additive
