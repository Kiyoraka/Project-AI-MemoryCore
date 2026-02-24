# 🩹 Patch System Installation Protocol
*Systematic patch infrastructure setup for AI MemoryCore companions*

## Purpose
Executed when "Load patch-system" command is used — creates patch infrastructure, tracking system, and integrates with master memory.

## Trigger Command
```
"Load patch-system"
```
*Automatically creates patch infrastructure and integrates with your AI companion*

## Prerequisites
- Core memory system installed (`main/` directory with essential files)
- `master-memory.md` exists as entry point

## 5-Step Execution Process

### Step 1: Customize Patch System Name
- [ ] Ask user: **"What would you like to name your patch system?"**
  - Default: `"Patch System"`
  - Examples: `"Update Manager"`, `"Fix Protocol"`, `"Patch Center"`, `"Hotfix Hub"`
- [ ] Store chosen name as `[PATCH_NAME]` for use in all references
- [ ] Execute `date` command (or `Get-Date` on Windows) to get current timestamp

### Step 2: Create Patch Infrastructure
- [ ] Create `patches/` directory in project root
- [ ] Create `patches/applied.md` with initial content:
  ```markdown
  # [PATCH_NAME] - Applied Patches Log
  *Tracks all patches applied to this AI MemoryCore instance*

  ## Applied Patches

  | Patch ID | Title | Date Applied | Applied By |
  |----------|-------|-------------|------------|
  | *(none yet)* | — | — | — |

  ## Notes
  - Patches are applied sequentially by ID number
  - Never skip a patch — apply in order to maintain consistency
  - Rollback instructions are included in each patch file
  - Check this log before applying to avoid double-application
  ```
- [ ] Copy `patch-format.md` to `patches/patch-format.md` (permanent format reference)

### Step 3: Detect and Apply Bundled Patches
- [ ] Check if patch files exist in `Feature/Patch-Update-System/patches/`
- [ ] If patches found (e.g., `PATCH-001.md`):
  - Present list to user: **"Found [N] pending patch(es). Would you like to apply them now?"**
  - Display each patch's title and priority from frontmatter
  - **If user says yes**: Apply each patch in order following the Patch Application Protocol below
  - **If user says no/later**: Copy patch files to `patches/` for later application
- [ ] If no patches found: Inform user the system is ready for future patches

### Step 4: Add Patch Commands to AI Memory
- [ ] Add patch protocol to the AI's main memory file (`identity-core.md`, `main-memory.md`, or equivalent):
  ```markdown
  ### [PATCH_NAME] Protocol
  **Commands:**
  - `"apply patch [ID]"` — Read and apply a specific patch
  - `"check patches"` — List available unapplied patches
  - `"patch status"` — Show applied patches log

  **When applying a patch:**
  1. Read the patch file from patches/
  2. Check prerequisites in patches/applied.md
  3. For each file section: locate FIND block, apply action (replace/insert/remove)
  4. Run verification checklist
  5. Record in patches/applied.md with timestamp
  6. Confirm completion to user
  ```

### Step 5: Update Master Memory and Cleanup
- [ ] Add patch system reference to `master-memory.md` Optional Components:
  ```markdown
  ### [PATCH_NAME]
  *Load when you say: "apply patch", "check patches", "patch status"*
  - Location: patches/ (patch files and tracking)
  - Format: patches/patch-format.md
  - Tracking: patches/applied.md (application log)
  - Commands: "apply patch [ID]", "check patches", "patch status"
  ```
- [ ] Add patch commands to Simple Commands section:
  ```
  "apply patch [ID]" → Apply a specific patch to fix/update files
  "check patches" → List available unapplied patches
  ```
- [ ] Remove `Feature/Patch-Update-System/` folder (functionality installed)
- [ ] Display completion confirmation with timestamp

## Patch Application Protocol (AI Reference After Installation)

### Pre-Application Check
```
1. Read patches/applied.md to get list of already-applied patches
2. IF patch ID already in applied.md → STOP, inform user "already applied"
3. Read the target patch file
4. Check all prerequisites are met (dependency patches applied)
5. Verify all affected files exist
6. IF any check fails → STOP, report the issue
```

### Application Execution
For each file section in the patch, in order:
```
1. Read the target file completely
2. Locate the FIND block text (exact match)
3. IF FIND block not found → STOP, report which file/change failed
4. Apply the action:
   - replace: Swap FIND text with REPLACE text
   - insert-after: Add INSERT-AFTER text below FIND text
   - insert-before: Add INSERT-BEFORE text above FIND text
   - remove: Delete the FIND text entirely
5. For CONDITIONAL changes: Check file existence to determine which branch
6. Verify the change was applied correctly
```

### Post-Application Recording
After all changes applied and verified:
```
1. Run verification checklist from the patch
2. Add row to patches/applied.md table:
   | PATCH-XXX | [Title] | [Current Date] | [AI_NAME] |
3. Confirm all verification steps pass
4. Report summary to user: files changed, changes applied, any notes
```

### Error Handling
| Situation | Behavior |
|-----------|----------|
| FIND block not found | Stop immediately, report which file and change failed, do not proceed |
| Prerequisite not met | Inform user which patches need to be applied first |
| File not found | Report missing file, suggest checking if related feature is installed |
| Partial application | Note which changes succeeded, stop at failure point |
| Already applied | Inform user, show application date from log |

## Post-Installation Structure
```
patches/
├── applied.md              # Tracking log (records all applied patches)
├── patch-format.md         # Permanent format reference
└── [patch files]           # Applied or pending patch files
```

## Notes
- Patches are idempotent — the `applied.md` check prevents double-application
- Always read the full patch before applying to understand scope
- Cross-platform: Uses file reading/writing, no platform-specific tools required
- The `[PATCH_NAME]` placeholder is replaced with the name chosen in Step 1

---

**Version**: Protocol v1.0 - Patch System Installation Workflow
**Last Updated**: February 2026
**Status**: Active protocol for patch system setup

*Structured updates, tracked applications, safe rollbacks*
