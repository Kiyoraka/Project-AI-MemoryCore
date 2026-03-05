---
name: library
description: "MUST use when saving to the library, loading from the library,
             searching for existing knowledge, installing pre-made items,
             or when about to create a new library entry. Also triggers when
             user says 'save library', 'load library', 'check library',
             'search library', 'install item', 'install library item',
             'do we have', 'is there a pattern for', 'find in library',
             or when the AI independently decides to save reusable knowledge."
---

# Library — Knowledge Guardian Skill
*Save, search, and reuse knowledge across projects — never solve the same problem twice*

## Activation

When interacting with the knowledge library, output:

`"Knowledge recalled. Scanning the shelves..."`

Then perform a dynamic library scan before any save operation.

## Context Guard

| Context | Status |
|---------|--------|
| **User says "save library", "save to library"** | ACTIVE — search + save protocol |
| **User says "load library", "check library"** | ACTIVE — search + load protocol |
| **User says "install item [name]"** | ACTIVE — item install protocol |
| **User says "do we have", "is there a pattern for"** | ACTIVE — search only |
| **AI identifies reusable knowledge worth saving** | ACTIVE — suggest save |
| **Casual conversation** | DORMANT — no library action |
| **No library directory found** | DORMANT — warn and skip |

## Dynamic Library Scanning

Always discover the library structure at runtime — **never hardcode** sections or entries:

1. **Scan** `library/` for all subdirectories (excluding `formats/`) — these are sections
2. **Scan** each section for `*.md` files (excluding README.md) — these are entries
3. **Count** total entries and sections dynamically
4. **Library path**: configurable (default: `library/`)

New sections and entries are automatically detected — zero config needed.

## Search Protocol (Before Any Library Save)

1. **Extract keywords** from the topic being saved
2. **Dynamic scan** — list ALL current sections and entries
3. **Match keywords** against existing entry filenames and section names
4. **Read top matches** (up to 3) to check content overlap
5. **Report findings** in structured format

## Project-Aware Recommendations

Not all systems are the same. The library considers the **current project context** when suggesting knowledge:

1. **Identify current project** — what system is being worked on right now?
2. **Match library entries** to project relevance — tech stack, domain, patterns
3. **Suggest what fits** — entries that are applicable to the current system
4. **Flag what doesn't fit** — entries that exist but aren't suitable for this project

### Suitability Assessment

| Factor | Check |
|--------|-------|
| **Tech stack** | Does the entry match? (Laravel entry for a Laravel project, not for Spring Boot) |
| **Domain** | Does the business domain align? (payment pattern for e-commerce, not for static site) |
| **Scale** | Is it appropriate for the project size? (Kafka for 50 users is overkill) |
| **Complexity** | Would it over-engineer the solution? (Redis caching for 20 records is unnecessary) |

### Example
```
Working on: Task Management System (Laravel + Vue, small-medium scale)

Suitable from library:
- security/laravel-sanctum-rbac.md — auth pattern fits
- integration/digitalocean-spaces-laravel.md — file storage fits

Not suitable:
- architecture/kafka-extreme-scale-pattern.md — overkill for this scale
- integration/payment-gateway.md — no payment needed in task system
```

## Report Format

```
Library Search Results
----------------------

Keywords: [extracted keywords]
Library: [count] entries across [count] sections
Current Project: [project name + tech stack]

Matches Found (Suitable):
- library/section/entry-name.md — [why it fits this project]

Matches Found (Not Suitable):
- library/section/entry-name.md — [why it doesn't fit: scale/domain/stack mismatch]

No Match In:
- [sections with no relevant entries]

Recommendation:
- [CREATE NEW / UPDATE EXISTING / REFERENCE ONLY]
- [IMPLEMENT / SKIP — for project-specific suggestions]
```

## Decision Rules

| Scenario | Recommendation |
|----------|---------------|
| No filename/keyword matches | **CREATE NEW** entry |
| Filename similar but different scope | **CREATE NEW** (note the related entry) |
| Content overlaps significantly | **UPDATE EXISTING** entry |
| Content already fully covered | **REFERENCE ONLY** — skip save |
| Entry exists but wrong scale/domain | **SKIP** — not suitable for current project |
| Entry exists and fits perfectly | **IMPLEMENT** — use this pattern |

## Format-Aware Save

When creating a NEW library entry (after search recommends CREATE NEW):

### Step 1: Auto-Determine Section

Pick the best matching section based on content type:

| Content Keywords | Section |
|-----------------|---------|
| System design, patterns, diagrams, architecture | `architecture` |
| UI components, Vue/React, reusable elements | `component` |
| Schema, migrations, queries, relationships | `database` |
| Flowcharts, sequence diagrams, visual flows | `diagram` |
| Third-party API, SDK, webhook, external service | `integration` |
| Auth, RBAC, encryption, guards, middleware | `security` |
| Colors, CSS, Tailwind, glassmorphism, fonts | `theme` |
| CI/CD, deployment, pipelines, automation | `workflow` |

If content clearly matches — auto-pick (trust-based, no confirmation needed).
If truly ambiguous — pick closest match, note in save confirmation.

### Step 2: Load Format Template

Auto-read the matching format from the library's formats directory:

```
library/formats/
├── architecture-format.md
├── component-format.md
├── database-format.md
├── diagram-format.md
├── integration-format.md
├── security-format.md
├── theme-format.md
└── workflow-format.md
```

**Path**: `library/formats/[section]-format.md`

### Step 3: Apply Format

Use the loaded template's structure:
- Follow the **Required Fields** from the format
- Follow the **Section Order** from the format
- Fill in the **Template** skeleton with actual content
- If no matching format file exists (new section), use a generic markdown structure with title + overview + content + examples

## Item Install Protocol

When installing a pre-made library entry from the `library-items/` catalog:

### Trigger Commands
- `"install item [name]"` — install a specific item by name
- `"install library item [name]"` — explicit library item install
- `"add item from catalog"` — browse and pick an item

### Install Steps

1. **Parse item name** from user command (e.g., "install item security-headers" → `security-headers`)
2. **Scan `library-items/`** for matching entry — search by filename keyword across all section folders
3. **If found**: show item info (name, section, first few lines as description preview)
4. **If multiple matches**: list all matches and ask user to pick one
5. **Check for duplicates** in user's `library/[section]/` — match by filename
6. **If no duplicate**: copy file from `library-items/[section]/[filename].md` to `library/[section]/[filename].md`
7. **If duplicate exists**: warn user and ask — overwrite existing entry or skip
8. **Trigger commit chain** (if Auto-Commit installed)

### Install Report Format
```
Item Install
------------
Item: [item name]
Section: [section name]
Source: library-items/[section]/[filename].md
Target: library/[section]/[filename].md
Status: Installed / Skipped (duplicate) / Not found

Available items in catalog:
- [section]/[item-name] — [first line description]
```

## Commit Chain

After saving or updating a library entry, if the **Auto-Commit System** skill is installed:
- Trigger the auto-commit skill to preserve the library change
- Library save exit = commit entrance. No knowledge left uncommitted.

If Auto-Commit is not installed, remind the user to commit manually.

## Mandatory Rules

1. **Always scan before save** — never create a library entry without checking first
2. **Dynamic discovery** — never hardcode sections or entry counts
3. **Keyword extraction** — derive from topic context, not just exact words
4. **Read matches** — don't just match filenames, read content of top matches
5. **Project-aware** — always consider current project when suggesting suitability
6. **Clear recommendation** — always end with actionable suggestion
7. **Wait for approval** — present findings and wait for the user's decision before saving
8. **Format-aware saves** — always load the matching format template before creating a new entry

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| **No library/ directory** | Warn user: "Library directory not found. Run the install protocol first." |
| **Empty library (no entries)** | Skip search, go straight to CREATE NEW recommendation |
| **Format template missing** | Use generic markdown structure (title + overview + content + examples) |
| **Entry name collision** | Append numeric suffix (e.g., `pattern-name-2.md`) |
| **User wants new section** | Create the folder, note that no format template exists for it |
| **Cross-section content** | Pick primary section, note secondary relevance in the entry |
| **Item not found in catalog** | List all available items from `library-items/` |
| **Library not installed** | Warn: "Library directory not found. Install Library System first." |
| **Item already in library** | Ask user: overwrite existing entry or skip |

## Level History

- **Lv.1** — Base: Dynamic library scanning + keyword matching + deduplication prevention. Scans library/ at runtime, extracts keywords from topic, matches against filenames and section names, reads top matches to check overlap, reports findings. (Origin: Knowledge reuse system for AI companions)
- **Lv.2** — Project-Aware: Added suitability assessment — considers tech stack, domain, scale, and complexity when recommending library entries for the current project. Entries that exist but don't fit are flagged separately from matches.
- **Lv.3** — Commit Chain: After saving/updating library entries, auto-triggers the Auto-Commit skill (if installed) to commit all changes. Library save exit becomes commit entrance.
- **Lv.4** — Format-Aware Save: Auto-determines library section from content keywords, loads matching format template from `library/formats/[section]-format.md`, applies template structure to new entries. Trust-based section selection (no approval gate). Formats loaded on-demand, not embedded.
- **Lv.5** — Item Install: Install pre-made library entries from `library-items/` catalog. New commands: "install item [name]", "install library item", "add item from catalog". Scans catalog by filename keyword, shows preview, checks for duplicates in user's library, copies to correct section, chains commit. Catalog persists at project root (not deleted during Library System installation). (Origin: Public knowledge sharing for AI MemoryCore community)
