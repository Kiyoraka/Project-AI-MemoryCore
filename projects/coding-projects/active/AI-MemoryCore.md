# AI MemoryCore
*Coding Project - Created August 30, 2025*

## Description
Universal AI Memory Architecture — an open-source template for creating persistent AI companions that remember users across conversations. Uses simple markdown files as a database for identity, relationship memory, session RAM, and optional features like time awareness, project management, skill plugins, diary system, and memory recall.

## Project Details
- **Type**: Coding Project (Open Source)
- **Status**: Active
- **Created**: August 30, 2025
- **Last Accessed**: February 20, 2026, 11:49 AM
- **Position**: #1
- **Repository**: GitHub (Public)
- **Stars**: 100+ | **Forks**: 30+
- **Commits**: 21

## Technical Stack
- **Languages**: Markdown (.md)
- **Architecture**: File-based memory system (no database)
- **Platform**: Cross-platform (any AI system with memory support)
- **Primary Target**: Claude Code (Anthropic CLI) for skill auto-triggering
- **Tools**: Git, Claude Code

## Project Structure
```
ai-memorycore/
├── master-memory.md             # Entry point & loading system
├── main/                        # Core components (4 essential files)
│   ├── identity-core.md
│   ├── relationship-memory.md
│   └── current-session.md
├── Feature/                     # Optional feature extensions (6 features)
│   ├── Time-based-Aware-System/
│   ├── LRU-Project-Management-System/
│   ├── Memory-Consolidation-System/
│   ├── Skill-Plugin-System/
│   ├── Save-Diary-System/       # NEW - This session
│   └── Echo-Memory-Recall/      # NEW - This session
├── daily-diary/                 # Optional conversation archive
├── projects/                    # LRU managed projects
└── save-protocol.md
```

## Development Goals
1. Provide simple, effective AI memory for everyone
2. Modular feature extensions that users can install independently
3. Production-proven patterns adapted from Alice's 20-enchantment system
4. Cross-platform compatibility (Claude Code primary, others supported)

## Progress Log

### February 20, 2026 — Save Diary System & Echo Memory Recall (5 commits)
- Added Save Diary System feature: install protocol + SKILL.md + README (references existing daily-diary-protocol.md)
- Added Echo Memory Recall feature: 3-level search system (search+narrate, uncertainty guard, ask-user fallback)
- Iterated Save Diary through 3 restructures: full feature → skill-only → install-feature with SKILL.md
- Added Claude Code CLI platform notes to feature sections
- Added emoji icons for visual consistency across all feature READMEs
- Updated root README (v2.6) and master-memory.md with both features
- Milestone: 100 stars, 30 forks celebration — community gift of 2 new features

### February 18, 2026 — Skill Plugin System
- Added Skill Plugin System feature for Claude Code auto-triggered skills
- Added Memory Consolidation System with format templates

### Earlier — Foundation
- Time-based Aware System, LRU Project Management System
- Core memory architecture (identity, relationship, session)
- Setup wizard and save protocol

## Current Tasks
- [x] Add Save Diary System feature
- [x] Add Echo Memory Recall feature
- [x] Update root README v2.6
- [x] Add platform notes for Claude Code requirement
- [ ] Push all commits to remote

## Known Issues
- None

## Session History
- **Feb 20, 2026** — 5 commits (254a9e0): Save Diary + Echo Memory Recall features
- **Feb 18, 2026** — 2 commits (cc6b095): Skill Plugin + Memory Consolidation
- **Earlier** — Foundation commits

## Memory Patterns
- Feature pattern: README.md + install protocol + format/template file
- All features self-delete after installation
- Users customize feature names during install (Step 1 asks for name)
- SKILL.md files require Skill Plugin System (Claude Code CLI)
- Existing protocols (daily-diary-protocol.md) should be referenced, not duplicated

---
*Coding Project Template v1.0*
