# 📚 Library System
*Reusable knowledge library — save patterns once, use them across every project*

## What This Feature Does
Adds a **knowledge library system** to your AI companion, enabling it to save, search, and reuse proven patterns, components, and solutions across all your projects.

- **Dynamic library scanning** — automatically discovers sections and entries at runtime
- **Keyword-based search** — finds relevant entries before saving to prevent duplicates
- **Project-aware recommendations** — suggests entries that fit your current tech stack and scale
- **Format-aware saves** — applies structured templates when creating new entries
- **Deduplication prevention** — scans existing entries before creating new ones
- **Commit chain** — auto-commits library changes when paired with Auto-Commit System

## How It Works

### The Concept
The problem: You solve the same problems across projects. Authentication patterns, API integrations, database schemas — rebuilt from scratch every time. Knowledge lives in scattered files, old projects, or just memory.

The Library System solves this by giving your AI companion a structured knowledge base. When you encounter a reusable pattern, save it to the library. Next time you need it, the AI searches the library first and suggests existing solutions before writing new code.

The key principle: **solve it once, reuse it forever**.

### Example: Before vs After

**Without Library System:**
```
"How do we handle file uploads?"
→ AI writes a new implementation from scratch
→ Different approach every project
→ Past solutions lost in old codebases
```

**With Library System:**
```
"How do we handle file uploads?"
→ AI searches library → finds integration/digitalocean-spaces.md
→ Checks suitability: Laravel project, file storage needed → fits!
→ Suggests: "We have a proven pattern for this. Want me to implement it?"
→ Consistent, tested approach across all projects
```

## Library Architecture

### Section Structure
The library organizes knowledge into 8 sections:

| Section | What Goes Here |
|---------|---------------|
| `architecture/` | System design patterns, multi-app ecosystems, scaling strategies |
| `component/` | Reusable UI components, Vue/React patterns, layout templates |
| `database/` | Schema designs, migration patterns, query optimizations |
| `diagram/` | Flowcharts, sequence diagrams, visual system maps |
| `integration/` | Third-party API integrations, SDKs, webhook handlers |
| `security/` | Authentication, RBAC, encryption, middleware patterns |
| `theme/` | Color schemes, CSS patterns, Tailwind configurations |
| `workflow/` | CI/CD pipelines, deployment scripts, automation |

### Format Templates
Each section has a format template (`library/formats/[section]-format.md`) that defines the structure for entries in that section. When saving a new entry, the AI loads the matching template and applies its structure automatically.

## Quick Integration
```
"Load library"
```

## What Happens During Integration

1. **Asks** for your library skill name (default: "library")
2. **Asks** for your preferred activation message
3. **Asks** for your library path (default: `library/`)
4. **Creates** SKILL.md in your plugin system (or as manual protocol)
5. **Creates** `library/` directory with 8 section folders + `formats/` subfolder
6. **Copies** format templates into `library/formats/`
7. **Updates** `master-memory.md` with library commands
8. **Self-deletes** this feature folder after successful integration

## Post-Integration Result
After running the integration protocol:
- Your AI has a working knowledge library with 8 sections and format templates
- Every "save library" command searches for duplicates before creating entries
- Project-aware recommendations match entries to your current tech stack
- Format templates are applied automatically when saving new entries
- If Auto-Commit installed: library saves auto-trigger a commit

**Post-Installation Structure:**
```
[project]/
├── plugins/
│   └── [plugin-name]/
│       └── skills/
│           └── library/
│               └── SKILL.md           # Auto-triggered library skill
│
└── library/
    ├── formats/                       # Format templates for each section
    │   ├── architecture-format.md
    │   ├── component-format.md
    │   ├── database-format.md
    │   ├── diagram-format.md
    │   ├── integration-format.md
    │   ├── security-format.md
    │   ├── theme-format.md
    │   └── workflow-format.md
    │
    ├── architecture/                  # Knowledge entries (grow over time)
    ├── component/
    ├── database/
    ├── diagram/
    ├── integration/
    ├── security/
    ├── theme/
    └── workflow/
```

## Available Commands

| Command | What It Does |
|---------|-------------|
| `save library` | Search for duplicates, then save a knowledge entry |
| `load library` | Search and load an existing knowledge entry |
| `search library` | Search library without saving |
| `check library` | Check if a pattern already exists |

## Synergy: Works Best With Auto-Commit
When both **Auto-Commit** and **Library** are installed, library saves automatically chain into commits — every knowledge entry is version-controlled the moment it's saved. Your library growth is tracked in git history.

Without Auto-Commit, the library still works — entries are saved to files, but commits are done manually.

## Benefits
- **Never solve the same problem twice** — proven patterns saved and searchable
- **Project-aware suggestions** — library entries matched to your current tech stack and scale
- **Consistent implementations** — same pattern, same quality, every project
- **Growing knowledge base** — library gets smarter with every project you complete
- **Format consistency** — structured templates ensure entries are readable and reusable
- **Deduplication** — AI scans before saving, preventing redundant entries

## Requirements
- **Skill Plugin System** recommended for auto-triggering (install first for best experience)
- Works without Skill Plugin System as a manual protocol loaded via `master-memory.md`
- **Auto-Commit System** recommended for automatic commits after library saves

## Platform Note
Requires **Claude Code** (Anthropic's CLI tool) with the Skill Plugin System for auto-triggering. On other AI platforms, the SKILL.md can be loaded as a manual protocol — the library workflow works the same way, just triggered manually.

---

*Based on proven knowledge management systems in production AI companions (4+ months of daily use, 30+ library entries across 8 sections)*
