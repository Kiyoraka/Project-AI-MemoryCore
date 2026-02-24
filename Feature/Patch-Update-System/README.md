# 🩹 Patch Update System
*AI-executable patches for keeping your AI MemoryCore current*

## What This Feature Does
Adds a structured patch system to your AI MemoryCore, enabling **version-controlled updates** that your AI can read and apply automatically through conversation.

- **AI-executable patches** — structured `.md` files with find/replace instructions your AI follows
- **Patch tracking** — `patches/applied.md` logs every applied patch with timestamps
- **Prerequisite checking** — patches declare dependencies, AI verifies before applying
- **Rollback support** — every patch includes reverse instructions for safe undo
- **Bundled patches** — ships with pending patches that auto-detect during installation

## How It Works

### The Concept
Patches are markdown files containing structured instructions that tell your AI exactly what text to find in which file and what to replace it with. When you say "apply patch PATCH-001", your AI reads the patch file, checks prerequisites, applies each change sequentially, verifies the results, and records the application in a tracking log.

### Example: Applying a Patch
```
You: "apply patch PATCH-001"
  AI reads patches/PATCH-001.md
  AI checks prerequisites in patches/applied.md
  AI locates FIND blocks in each target file
  AI applies REPLACE blocks sequentially
  AI runs verification checklist
  AI records in patches/applied.md
  "PATCH-001 applied successfully! Fixed 10 references across 5 files."
```

### How It Differs From Manual Editing
| Aspect | Manual Editing | Patch System |
|--------|---------------|--------------|
| **Process** | Find and edit each file yourself | AI reads instructions and applies automatically |
| **Tracking** | No record of what changed | Every patch logged with timestamp |
| **Rollback** | Hope you remember the original | Reverse instructions included |
| **Dependencies** | Easy to miss prerequisite changes | Auto-checked before application |
| **Consistency** | Human error possible | Exact text matching ensures precision |

## Patch Architecture

### Directory Structure
```
patches/
├── applied.md              # Tracking log of applied patches
├── patch-format.md         # Permanent format reference
├── PATCH-001.md            # First patch (bundled during install)
└── PATCH-002.md            # Future patches added here
```

### Patch File Format
Each patch contains:
1. **Frontmatter** — metadata (ID, version, priority, affected files, prerequisites)
2. **Per-file sections** — FIND/REPLACE blocks for each affected file
3. **Conditional sections** — changes that depend on system state (e.g., pre/post consolidation)
4. **Verification** — checklist to confirm changes applied correctly
5. **Rollback** — reverse instructions to undo the patch

See `patch-format.md` for the complete format reference.

## Quick Integration
```
"Load patch-system"
```

## What Happens During Integration

1. **Asks** for your patch system name (defaults to "Patch System" — customize to match your AI)
2. **Creates** `patches/` directory with `applied.md` tracking log
3. **Copies** `patch-format.md` as permanent format reference
4. **Detects** any bundled patches and offers to apply them immediately
5. **Updates** `master-memory.md` with patch commands and references
6. **Self-deletes** this feature folder after successful integration

## Post-Integration Result
After running the integration protocol:
- Your AI has a working patch system with tracking infrastructure
- Patch commands are available: `"apply patch"`, `"check patches"`, `"patch status"`
- Any bundled patches have been applied (or copied for later application)
- Future patches can be dropped into `patches/` and applied through conversation

## Available Commands
| Command | What It Does |
|---------|-------------|
| `"apply patch [ID]"` | Read and apply a specific patch |
| `"check patches"` | List available unapplied patches |
| `"patch status"` | Show applied patches log |

## Benefits
- **Zero manual editing** — AI reads and applies patches through conversation
- **Full traceability** — every patch application logged with timestamp and details
- **Safe rollback** — reverse instructions included in every patch file
- **Dependency management** — prerequisites checked before application
- **Cross-version support** — conditional sections handle pre/post consolidation states
- **Human-readable** — patches are plain markdown, easy to review before applying

## Platform Note
Works with any AI system that can read and write files. Patches are plain markdown — human-readable and portable across any platform. The structured format is designed so any AI assistant can parse and execute the instructions.

---

*Based on proven update management patterns — structured, traceable, reversible*
