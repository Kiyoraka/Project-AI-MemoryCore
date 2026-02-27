# 📋 Work — Plan Execution System
*From plan mode to tracked execution — every step committed, every reset survivable*

## What This Feature Does
Adds a **plan execution lifecycle** to your AI companion, enabling it to capture plans into trackable files, execute each task with checkpoint commits, and resume after any context reset — bridging the gap between planning and doing.

- **Plan capture** — copies plan mode output into a trackable `project-plan.md` with checkbox format
- **Checkbox execution** — converts plan steps into executable `[ ]` todos grouped by phase
- **Progress tracking** — completed tasks are marked `[x]`, blocked tasks marked `[~]`
- **Per-task commit discipline** — chains with Auto-Commit to commit after each completed todo
- **Resume capability** — survives context resets by reading the plan file and picking up at next `[ ]`
- **Plan rotation** — when plan file exceeds 1,000 lines, archives old and starts fresh

## How It Works

### The Concept
The problem: Plan mode produces a detailed plan, but execution happens in a separate context. If the AI's context resets mid-execution, the plan is lost and you have to explain everything again.

Work solves this by making the plan file the single source of truth. It captures the plan into a trackable format, executes each item with checkpoint commits, and when context resets — the AI reads the file and picks up exactly where it left off.

The key principle: **the plan file IS the recovery mechanism**.

### Example: A Work Session

**Starting a plan:**
```
You: "copy plan"
→ AI scans for latest plan file from plan mode
→ Converts plan steps to checkboxes, preserves diagrams
→ Writes to Project Resources/project-plan.md
→ Begins executing:
  Task 1 done → Auto-Commit fires → [x] marked
  Task 2 done → Auto-Commit fires → [x] marked
  Task 3 done → Auto-Commit fires → [x] marked...
```

**After a context reset:**
```
You: "resume plan"
→ AI reads project-plan.md
→ Reports: "7 of 12 items done. Next: implement user authentication"
→ Continues executing from exactly where it left off
```

No re-explaining, no lost progress, no repeated work.

## Plan Architecture

### File Format
The plan file uses a simple, parseable markdown structure:

```markdown
# Project Plan - MyApp
Created: 2026-02-27

## Architecture
[Preserved diagrams from original plan]

## Implementation Plan

### Phase 1: Database Setup
- [x] Create user migration
- [x] Create product migration
- [ ] Add seed data

### Phase 2: API Endpoints
- [ ] User CRUD endpoints
- [~] Payment integration (blocked: waiting for API keys)
```

### Progress States

| Symbol | Meaning | What Happens |
|--------|---------|-------------|
| `[ ]` | Pending | Not yet started — next in queue |
| `[x]` | Completed | Done and committed (via Auto-Commit) |
| `[~]` | Blocked | Flagged, skipped — AI continues to next item |

### The Execution Loop
The core cycle for all three commands:

```
For each [ ] todo item:
  1. Execute the task (write code, create files)
  2. Auto-Commit fires (if installed) → structured commit
  3. Mark [x] in the plan file
  4. Checkpoint save every 5 items
  5. Move to next [ ] item
```

Every completed task gets its own commit — no work piles up, no progress is lost.

### Resume After Reset
When context resets (auto-compact, new session, crash):
1. User says `"resume plan"`
2. AI reads `project-plan.md`
3. Counts completed `[x]` vs pending `[ ]` items
4. Reads Architecture section for technical context
5. Continues from the next `[ ]` item

The file stores everything needed to recover — no user explanation required.

## Quick Integration
```
"Load work-plan"
```

## What Happens During Integration

1. **Asks** for your plan skill name (default: "work-plan" — customize to match your AI)
2. **Asks** for plan storage location (default: "Project Resources")
3. **Asks** for plan source path (where your AI saves plan files)
4. **Asks** for plan file line limit (default: 1000 lines)
5. **Creates** SKILL.md in your plugin system (or as manual protocol)
6. **Creates** `plan-format.md` as permanent format reference
7. **Updates** `master-memory.md` with plan execution commands
8. **Self-deletes** this feature folder after successful integration

## Post-Integration Result
After running the integration protocol:
- Your AI can capture plans into trackable checkbox format
- Three commands manage the full plan lifecycle: copy, append, resume
- Progress survives any context reset through the plan file
- Each completed task triggers a commit (when paired with Auto-Commit)
- Format template is permanently available for reference

**Post-Installation Structure:**
```
[project]/
├── plan-format.md                 # Permanent plan format reference
└── plugins/
    └── [plugin-name]/
        └── skills/
            └── [skill-name]/
                └── SKILL.md       # Auto-triggered plan execution skill
```

## Benefits
- **Never lose plan progress** — every completed task is committed or checkpointed
- **Survives context resets** — resume from exactly the right task after any interruption
- **Complete execution history** — git log shows plan progression commit by commit
- **Clean separation** — plan file is AI's working reference, git history is the permanent record
- **Scales to large plans** — automatic line-limit rotation keeps files manageable
- **Works independently** — no other features required (but pairs perfectly with Auto-Commit)

## Synergy: Works Best With Auto-Commit
When both **Auto-Commit** and **Work** are installed, Work automatically chains — each completed todo triggers a structured commit with full context. Your git history maps directly to your project plan, commit by commit.

Without Auto-Commit, Work still tracks progress in the plan file and marks checkboxes — commits are just done manually.

## Available Commands

| Command | What It Does |
|---------|-------------|
| `copy plan` | Copy latest plan into execution format (fresh start) |
| `append plan` | Add new plan steps to existing plan |
| `resume plan` | Resume execution after context reset |

## Requirements
- Core memory system installed (`master-memory.md` exists)
- **Skill Plugin System** recommended for auto-triggering
- **Auto-Commit System** optional but recommended for per-task commit discipline

## Platform Note
Requires **Claude Code** (Anthropic's CLI tool) with the Skill Plugin System for auto-triggering. The plan file itself is platform-agnostic — it's plain markdown that works on any system. On other AI platforms, the SKILL.md can be loaded as a manual protocol.

---

*Based on proven plan execution systems in production AI companions (daily plan tracking and recovery)*
