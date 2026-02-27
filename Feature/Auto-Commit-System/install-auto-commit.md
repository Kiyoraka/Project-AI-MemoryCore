# 🔒 Auto-Commit Installation Protocol
*Systematic commit guardian setup for AI MemoryCore companions*

## Purpose
Executed when "Load auto-commit" command is used — creates an intelligent commit skill, configures commit format with custom section names, and integrates with your AI companion.

## Trigger Command
```
"Load auto-commit"
```
*Automatically creates commit skill, configures format, and registers with your AI*

## Prerequisites
- Git repository initialized in your project (`git init`)
- Skill Plugin System recommended for auto-triggering (but not required)
- Core memory system installed (`master-memory.md` exists)

## 6-Step Execution Process

### Step 1: Gather Configuration
- [ ] Ask user: **"What would you like to name your commit skill?"**
  - Default: `"auto-commit"`
  - Examples: `"commit-guardian"`, `"git-seal"`, `"chronicle"`, `"forge"`
- [ ] Store chosen name as `[COMMIT_SKILL_NAME]`
- [ ] Ask user: **"What should your first commit section be called?"**
  - Default: `"TECHNICAL CHANGES"`
  - This section lists files and what changed in each
  - Examples: `"IMPLEMENTATION"`, `"CODE CHANGES"`, `"WHAT CHANGED"`
- [ ] Store as `[SECTION_1_NAME]`
- [ ] Ask user: **"What should your second commit section be called?"**
  - Default: `"SESSION CONTEXT"`
  - This section captures project name, type, time spent, and session metadata
  - Examples: `"PROJECT LOG"`, `"NOTES"`, `"WHY"`
- [ ] Store as `[SECTION_2_NAME]`
- [ ] Ask user: **"What should the AI say when committing?"** (activation message)
  - Default: `"Committing changes to history..."`
  - Examples: `"Sealing the commit..."`, `"Saving progress..."`, `"Changes locked in."`
- [ ] Store as `[ACTIVATION_MESSAGE]`
- [ ] Ask user: **"What is your name and email for git commits?"**
  - This is the human user's identity — commits appear under this name
  - Store as `[AUTHOR_NAME]` and `[AUTHOR_EMAIL]`
- [ ] Execute `Get-Date` (Windows) or `date` (macOS/Linux) for current timestamp

### Step 2: Verify Plugin System
- [ ] Check if `plugins/` directory exists in the project
- [ ] Identify the plugin folder (look for `[ai-name]-skills/` or similar)
- [ ] If plugin system is found:
  - Continue to Step 3 (create as auto-triggered skill)
- [ ] If plugin system is NOT found:
  - Inform user: "The Skill Plugin System is not installed. Auto-Commit can still work as a manual protocol."
  - Offer two choices:
    1. "Install Skill Plugin System first" (recommended)
    2. "Continue without auto-triggering" (skill added to master-memory.md as manual protocol)
  - If continuing without plugin: skip Step 3, add protocol directly to main memory in Step 5

### Step 3: Create Auto-Commit Skill
- [ ] Create `plugins/[plugin-name]/skills/[COMMIT_SKILL_NAME]/` directory
- [ ] Create `SKILL.md` inside with all placeholders replaced:
  - Replace `[COMMIT_SKILL_NAME]` with chosen skill name
  - Replace `[SECTION_1_NAME]` with chosen first section name
  - Replace `[SECTION_2_NAME]` with chosen second section name
  - Replace `[ACTIVATION_MESSAGE]` with chosen activation message
  - Replace `[AI_NAME]` with AI companion's name from `master-memory.md`
- [ ] Verify SKILL.md has valid YAML frontmatter with `name` and `description`

### Step 4: Install Commit Format Template
- [ ] Copy `commit-format.md` to project root as `commit-format.md`
- [ ] Replace `[SECTION 1 NAME]` with `[SECTION_1_NAME]` in the copied file
- [ ] Replace `[SECTION 2 NAME]` with `[SECTION_2_NAME]` in the copied file
- [ ] Inform user: "Commit format template saved as `commit-format.md` — this is your permanent reference"

### Step 5: Update Master Memory and Cleanup
- [ ] Add commit reference to `master-memory.md` Optional Components section:
  ```markdown
  ### [COMMIT_SKILL_NAME]
  *Auto-triggers when: committing code, task completion (Vigilant mode)*
  - Commit format: commit-format.md
  - Sections: [SECTION_1_NAME] + [SECTION_2_NAME]
  - Author: [AUTHOR_NAME] <[AUTHOR_EMAIL]>
  - Vigilant mode: auto-commits after task completion
  ```
- [ ] Add commit commands to Simple Commands section:
  ```
  "commit" → Analyze changes, draft structured commit message, and commit
  "push" → Commit and push to remote repository
  ```

### Step 6: Test and Cleanup
- [ ] Run `git status` to verify git repository is accessible
- [ ] Demonstrate: show a sample commit message using the chosen section names
  ```
  Example commit with your configuration:

  Add [feature] - [summary]

  === [SECTION_1_NAME] ===
  • [file]: [change description]

  === [SECTION_2_NAME] ===
  • Project: [name] | Type: development | Time: ~XX min
  ```
- [ ] Remove `Feature/Auto-Commit-System/` folder (functionality installed)
- [ ] Display completion confirmation with timestamp:
  ```
  Auto-Commit System installed successfully!
  Skill: [COMMIT_SKILL_NAME]
  Sections: [SECTION_1_NAME] + [SECTION_2_NAME]
  Author: [AUTHOR_NAME]
  Installed at: [timestamp]
  ```

## Post-Installation Structure
```
[project]/
├── commit-format.md                   # Permanent commit format reference
└── plugins/
    └── [plugin-name]/
        └── skills/
            └── [COMMIT_SKILL_NAME]/
                └── SKILL.md           # Auto-triggered commit skill
```

## Customizing After Installation

### Adding More Sections
Edit `plugins/[plugin-name]/skills/[COMMIT_SKILL_NAME]/SKILL.md` to add additional sections:
```
=== [SECTION_1_NAME] ===
• File-level changes

=== [SECTION_2_NAME] ===
• Session metadata

=== TESTING ===
• Test coverage notes (custom addition)
```

### Changing Section Names
Update both files:
1. `SKILL.md` — change the section names in the commit template
2. `commit-format.md` — update the reference format to match

### Pairing with Work Plan Execution
If you install the **Work Plan Execution** feature, Auto-Commit automatically chains with it — each completed plan task triggers a structured commit. Your git history maps directly to your project plan.

## Notes
- Commits are always authored under the human user's name, not the AI's
- The AI drafts the message but never pushes to remote without explicit instruction
- Sensitive files (.env, credentials, API keys) are automatically detected and blocked
- The format is a starting point — customize it to match your team's conventions
- Works with any git project, any programming language, any workflow

---

**Version**: Protocol v1.0 - Auto-Commit Installation Workflow
**Last Updated**: February 2026
**Status**: Active protocol for commit system setup

*Structured commits that document your work — not just your diff*
