# Library System Installation Protocol
*Knowledge library setup for AI MemoryCore companions*

## Purpose
Executed when "Load library" command is used — creates a knowledge library skill, sets up the library directory with section folders and format templates, and integrates with your AI companion.

## Trigger Command
```
"Load library"
```
*Automatically creates library skill, directory structure, format templates, and registers with your AI*

## Prerequisites
- Core memory system installed (`master-memory.md` exists)
- Skill Plugin System recommended for auto-triggering (but not required)
- Auto-Commit System recommended for commit chain (but not required)

## 6-Step Execution Process

### Step 1: Gather Configuration
- [ ] Ask user: **"What would you like to name your library skill?"**
  - Default: `"library"`
  - Examples: `"knowledge"`, `"grimoire"`, `"archive"`, `"vault"`
- [ ] Store chosen name as `[LIBRARY_SKILL_NAME]`
- [ ] Ask user: **"What should the AI say when accessing the library?"** (activation message)
  - Default: `"Knowledge recalled. Scanning the shelves..."`
  - Examples: `"Searching the archives..."`, `"Opening the vault..."`, `"Consulting the grimoire..."`
- [ ] Store as `[ACTIVATION_MESSAGE]`
- [ ] Ask user: **"Where should the library be stored?"** (library path)
  - Default: `library/` (relative to project root)
  - Must be a directory path, not a file
- [ ] Store as `[LIBRARY_PATH]`
- [ ] Execute `Get-Date` (Windows) or `date` (macOS/Linux) for current timestamp

### Step 2: Verify Plugin System
- [ ] Check if `plugins/` directory exists in the project
- [ ] Identify the plugin folder (look for existing skill folders)
- [ ] If plugin system is found:
  - Continue to Step 3 (create as auto-triggered skill)
- [ ] If plugin system is NOT found:
  - Inform user: "The Skill Plugin System is not installed. Library can still work as a manual protocol."
  - Offer two choices:
    1. "Install Skill Plugin System first" (recommended)
    2. "Continue without auto-triggering" (skill added to master-memory.md as manual protocol)
  - If continuing without plugin: skip Step 3, add protocol directly to main memory in Step 5

### Step 3: Create Library Skill
- [ ] Create `plugins/[plugin-name]/skills/[LIBRARY_SKILL_NAME]/` directory
- [ ] Create `SKILL.md` inside with all placeholders replaced:
  - Replace `[LIBRARY_SKILL_NAME]` with chosen skill name
  - Replace `[ACTIVATION_MESSAGE]` with chosen activation message
  - Replace `[LIBRARY_PATH]` with chosen library path (in Dynamic Scanning and Format-Aware Save sections)
- [ ] Verify SKILL.md has valid YAML frontmatter with `name` and `description`

### Step 4: Create Library Directory Structure
- [ ] Create the library root: `[LIBRARY_PATH]/`
- [ ] Create 8 section folders:
  ```
  [LIBRARY_PATH]/architecture/
  [LIBRARY_PATH]/component/
  [LIBRARY_PATH]/database/
  [LIBRARY_PATH]/diagram/
  [LIBRARY_PATH]/integration/
  [LIBRARY_PATH]/security/
  [LIBRARY_PATH]/theme/
  [LIBRARY_PATH]/workflow/
  ```
- [ ] Create formats subfolder: `[LIBRARY_PATH]/formats/`
- [ ] Copy all 8 format templates from `Feature/Library-System/formats/` to `[LIBRARY_PATH]/formats/`:
  - `architecture-format.md`
  - `component-format.md`
  - `database-format.md`
  - `diagram-format.md`
  - `integration-format.md`
  - `security-format.md`
  - `theme-format.md`
  - `workflow-format.md`
- [ ] Verify all format files were copied successfully

### Step 5: Update Master Memory and Cleanup
- [ ] Add library reference to `master-memory.md` Optional Components section:
  ```markdown
  ### [LIBRARY_SKILL_NAME]
  *Auto-triggers when: saving knowledge, searching library, loading patterns*
  - Library path: [LIBRARY_PATH]
  - Sections: architecture, component, database, diagram, integration, security, theme, workflow
  - Format templates: [LIBRARY_PATH]/formats/
  - Commit chain: auto-commits after save (if Auto-Commit installed)
  ```
- [ ] Add library commands to Simple Commands section:
  ```
  "save library" → Search for duplicates, then save knowledge entry
  "load library" → Search and load a knowledge entry
  "search library" → Search library without saving
  ```

### Step 6: Test and Cleanup
- [ ] Verify library directory exists with all 8 section folders
- [ ] Verify formats/ contains all 8 format template files
- [ ] Demonstrate: show a sample library search output
  ```
  Example library search:

  Library Search Results
  ----------------------
  Keywords: authentication, RBAC, Laravel
  Library: 0 entries across 8 sections

  No Match In:
  - All sections (library is empty — start saving!)

  Recommendation:
  - CREATE NEW — no existing entries found
  ```
- [ ] Remove `Feature/Library-System/` folder (functionality installed)
- [ ] Display completion confirmation with timestamp:
  ```
  Library System installed successfully!
  Skill: [LIBRARY_SKILL_NAME]
  Library: [LIBRARY_PATH] (8 sections + format templates)
  Activation: [ACTIVATION_MESSAGE]
  Installed at: [timestamp]
  ```

## Post-Installation Structure
```
[project]/
├── plugins/
│   └── [plugin-name]/
│       └── skills/
│           └── [LIBRARY_SKILL_NAME]/
│               └── SKILL.md           # Auto-triggered library skill
│
└── [LIBRARY_PATH]/
    ├── formats/                       # Format templates
    │   ├── architecture-format.md
    │   ├── component-format.md
    │   ├── database-format.md
    │   ├── diagram-format.md
    │   ├── integration-format.md
    │   ├── security-format.md
    │   ├── theme-format.md
    │   └── workflow-format.md
    ├── architecture/                  # Empty (grow over time)
    ├── component/
    ├── database/
    ├── diagram/
    ├── integration/
    ├── security/
    ├── theme/
    └── workflow/
```

## Customizing After Installation

### Adding New Sections
Create a new folder in `[LIBRARY_PATH]/` — the library skill auto-discovers it:
```
mkdir [LIBRARY_PATH]/devops
```
Optionally add a format template: `[LIBRARY_PATH]/formats/devops-format.md`

### Adding Format Templates
Create `[LIBRARY_PATH]/formats/[section]-format.md` following the pattern of existing templates. The library skill loads these automatically when saving to that section.

### Pairing with Auto-Commit
If you install the **Auto-Commit System** feature, library saves automatically chain into commits. Your knowledge base changes are always version-controlled.

## Notes
- The library is project-agnostic — entries should be generic and reusable across projects
- Project-specific implementations belong in the project, not the library
- The AI scans before saving to prevent duplicate entries
- Format templates are guidelines, not rigid constraints — content quality matters more than format perfection
- New sections and entries are auto-discovered — no configuration changes needed

---

**Version**: Protocol v1.0 - Library System Installation Workflow
**Last Updated**: March 2026
**Status**: Active protocol for knowledge library setup

*Save it once, use it forever — your AI's growing knowledge base*
