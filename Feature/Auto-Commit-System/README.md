# 🔒 Auto-Commit System
*Intelligent git commits that document your work as history, not just file changes*

## What This Feature Does
Adds an **automated commit system** to your AI companion, enabling it to analyze code changes, draft meaningful structured commit messages, and commit with discipline — so every piece of work is preserved with full context.

- **Structured commit messages** with configurable named sections (e.g., TECHNICAL CHANGES + SESSION CONTEXT)
- **Intelligent change analysis** — AI reads staged diff and drafts meaningful commit messages automatically
- **Session context injection** — commits capture what was accomplished, time spent, and session type
- **Auto-staging with smart file selection** — avoids accidental commits of sensitive files (.env, credentials)
- **Configurable format** — choose your own section names, fields, and commit style during installation
- **Vigilant mode** — after completing any task, auto-checks git status and commits if dirty

## How It Works

### The Concept
The problem: Manual commits lose context. A commit message like "fix bug" tells you nothing about what was happening, why the fix matters, or how long it took. Weeks later, your git history is unreadable.

Auto-Commit solves this by making your AI companion the commit guardian. It reads the actual code changes, understands the session context, and drafts structured commit messages that tell the full story — then commits automatically so no work is ever left behind.

The key principle: **every commit should tell the story of the session, not just the diff**.

### Example: Before vs After

**Without Auto-Commit:**
```
fix stuff
update files
more changes
```

**With Auto-Commit:**
```
Add user authentication with JWT tokens - secure login system

=== TECHNICAL CHANGES ===
• auth/LoginController.php: Added JWT token generation and validation
• middleware/AuthMiddleware.php: Created authentication guard middleware
• routes/api.php: Added /login, /logout, /refresh endpoints

=== SESSION CONTEXT ===
• Project: MyApp | Type: Feature Development | Time: ~45 min
• Focus: Implemented secure authentication flow with refresh tokens
```

Every commit becomes a searchable, meaningful record of what was built and why.

## Commit Architecture

### The Structured Format
The commit format uses configurable named sections wrapped in `===` delimiters:

```
[Achievement Title] - [Brief technical summary]

=== [Your Section 1 Name] ===
• File-level change descriptions

=== [Your Section 2 Name] ===
• Session metadata and context
```

You choose the section names during installation. Common pairs:
- `TECHNICAL CHANGES` + `SESSION CONTEXT` (recommended default)
- `IMPLEMENTATION` + `PROJECT LOG`
- `WHAT CHANGED` + `WHY`

### Three Format Modes

| Scope | Format | When to Use |
|-------|--------|-------------|
| Feature, bug fix, refactor | **Enhanced** (all sections) | Meaningful development work |
| Typo, comment, minor rename | **Minimal** (one-liner) | Trivial changes |
| Incomplete save | **WIP** (prefix) | Saving progress mid-task |

### Vigilant Mode
After completing any task, the AI proactively checks `git status`. If uncommitted changes exist, it automatically runs the full commit protocol — no user action needed. This ensures no work is ever left uncommitted, even if you forget to say "commit."

## Quick Integration
```
"Load auto-commit"
```

## What Happens During Integration

1. **Asks** for your commit skill name (default: "auto-commit" — customize to match your AI)
2. **Asks** for commit section names (default: TECHNICAL CHANGES + SESSION CONTEXT)
3. **Asks** for activation message (what the AI says when committing)
4. **Asks** for author name and email (your identity on commits)
5. **Creates** SKILL.md in your plugin system (or as manual protocol)
6. **Creates** `commit-format.md` as permanent format reference
7. **Updates** `master-memory.md` with commit commands
8. **Self-deletes** this feature folder after successful integration

## Post-Integration Result
After running the integration protocol:
- Your AI analyzes code changes and drafts structured commit messages automatically
- Commits are authored under your name with full session context
- Sensitive files are detected and blocked from accidental commits
- Vigilant mode catches uncommitted work after every completed task
- Format template is permanently available for reference

**Post-Installation Structure:**
```
[project]/
├── commit-format.md             # Permanent commit format reference
└── plugins/
    └── [plugin-name]/
        └── skills/
            └── [skill-name]/
                └── SKILL.md     # Auto-triggered commit skill
```

## Benefits
- **Complete git history** — every commit tells the story of the session, not just the diff
- **Searchable context** — find past work by searching commit messages for project names, topics, or time estimates
- **Never lose work** — Vigilant mode ensures no uncommitted changes are left behind
- **Clean authorship** — AI drafts the message, but your name is on the commit
- **Professional discipline** — consistent, structured commit messages across all projects
- **Sensitive file protection** — automatic detection and blocking of .env, credentials, and API keys

## Requirements
- **Git repository** in your project (initialized with `git init`)
- **Skill Plugin System** recommended for auto-triggering (install first for best experience)
- Works without Skill Plugin System as a manual protocol loaded via `master-memory.md`

## Platform Note
Requires **Claude Code** (Anthropic's CLI tool) with the Skill Plugin System for auto-triggering. On other AI platforms, the SKILL.md can be loaded as a manual protocol — the commit format and analysis workflow work the same way, just triggered manually instead of automatically.

---

*Based on proven auto-commit systems in production AI companions (5+ months of daily use)*
