---
name: observation
description: "MUST use when user says 'survey project', 'scan project', 'check health',
             'investigate', 'deep dive', 'what's going on in', 'look into',
             'refine code', 'clean up code', 'review changes', 'sharpen',
             'audit system', 'full audit', 'show me everything',
             or when the AI needs to assess project health before planning,
             review code quality after implementation, or investigate a bug.
             Also triggers on 'how does this project look', 'what's the status',
             'review what I changed', 'check for issues'."
---

# Observation System — Tiered Code Awareness
*"See clearly before you act. Act only on what you see."*

## Activation

Four commands, each at a different depth:

| Command | Activation Message | Time |
|---------|-------------------|------|
| **Survey** | `"Scanning project from above..."` | ~30 sec |
| **Investigate** | `"Focusing on [target]..."` | ~5 min |
| **Refine** | `"Reviewing changed code..."` | ~5 min |
| **Audit** | `"Revealing all connections..."` | ~15 min |

Then execute the matching protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| **User says "survey", "scan", "check health", "project status"** | ACTIVE — run Survey |
| **User says "investigate", "deep dive", "look into", "what's going on"** | ACTIVE — run Investigate |
| **User says "refine", "clean up", "review changes", "check my code"** | ACTIVE — run Refine |
| **User says "audit", "full audit", "show me everything"** | ACTIVE — run Audit |
| **Before planning a large feature** | ACTIVE — Survey first |
| **After implementation, before commit** | ACTIVE — Refine (code was written) |
| **Bug report or error investigation** | ACTIVE — Investigate (bug mode) |
| **Casual conversation, no project context** | DORMANT — no observation |
| **Non-code tasks, research, documentation** | DORMANT — no code to observe |

## Protocol

### Step 1: Determine Command

Parse the user's request and dispatch to the matching depth level:

| Depth | Command | Question It Answers | Time |
|-------|---------|-------------------|------|
| **Lv.1** | Survey | "What's the state of the project?" | ~30 sec |
| **Lv.2** | Investigate | "What's happening in this specific area?" | ~5 min |
| **Lv.2** | Refine | "What can be improved in changed code?" | ~5 min |
| **Lv.3** | Audit | "Show me everything about this system." | ~15 min |

### Step 2: Execute Tier Protocol

Follow the detailed protocol for the selected command (see sections below).

### Step 3: Suggest Escalation

After completing any tier, suggest the next appropriate depth if findings warrant it (see Escalation Paths).

---

## Depth Levels

Four commands at three depth levels. Survey/Investigate/Audit are **investigative** (observe and report). Refine is **corrective** (observe and fix).

### When to Use Which

| Situation | Tier |
|-----------|------|
| "How's the project looking?" | Survey |
| "What's going on in this area?" | Investigate |
| "Clean up what I just wrote" | Refine |
| "Audit the entire system" | Audit |
| Before designing a feature | Survey → then plan |
| After coding, before commit | Refine |
| Tracking down a bug | Investigate (bug mode) |
| Quarterly health check | Audit |

### Escalation Paths

```
Survey spots problem area    → Investigate that area
Investigate finds deep issue → Audit the full system
Survey/Investigate/Audit     → Refine specific code
Refine finds systemic issue  → Audit the full system
```

---

## Lv.1: Survey

Quick bird's-eye view of a project — structure, tech stack, health, and recent activity.

### Arguments

| Argument | Action | Example |
|----------|--------|---------|
| `<project>` | Scan specific project | `survey tariqms` |
| *(none)* | Scan current working directory | `survey` |
| `all` | Overview of ALL active projects | `survey all` |

### Step 1: Dependency Scan

Adapt to the project's actual stack:
- [ ] Frontend: Read package manifest (`package.json`, `pubspec.yaml`, etc.) — UI library, framework, test runner
- [ ] Frontend: Scan component directories — check for custom wrappers that override standard behavior
- [ ] Backend: Read project file (`.csproj`, `pom.xml`, `go.mod`, `Cargo.toml`, etc.) — dependencies, framework version
- [ ] Skip if project type doesn't apply (backend-only, frontend-only)

### Step 2: Structure Scan

- [ ] Count files by type (backend, frontend, test, config)
- [ ] Identify architecture pattern (Clean Architecture, N-Tier, monolith, etc.)
- [ ] Note project organization (monorepo, multi-project, single app)

### Step 3: Tech Stack Detection

Detect from project files:
- [ ] `.csproj` → .NET version, target framework
- [ ] `package.json` → Frontend framework, key dependencies
- [ ] Database provider (from config or ORM setup)
- [ ] CI/CD pipeline (`.github/workflows/`, `Jenkinsfile`, etc.)
- [ ] Container setup (`docker-compose.yml`, `Dockerfile`)

### Step 4: Health Check

- [ ] Build status — any errors? (`dotnet build` / `npm run build`)
- [ ] Git status — uncommitted changes? (`git status --short`)
- [ ] Branch status — ahead/behind remote?
- [ ] Last commit date — how stale?
- [ ] TODO/FIXME/HACK count — outstanding markers

### Step 5: Recent Activity

- [ ] Show last 5 commits (`git log --oneline -5`)
- [ ] Note active branch and any open work

### Step 6: Domain Lesson Check

Cross-reference project against past incidents (if Post-Mortem System is installed):
- [ ] Scan post-mortem records for entries matching this project's domain
- [ ] Show max 3 most relevant lessons
- [ ] If same failure type appears 2+ times: flag as recurring
- [ ] Skip section entirely if no matches found

### Survey Output Format

```
Survey: [PROJECT NAME]

Structure: [X] backend | [Y] frontend | [Z] tests
Stack:     [.NET X] + [Framework] + [DB]
Health:    [Build status] | [Git status] | [Last commit]
Recent:    [Last 3-5 commits, one line each]
Lessons:   [N relevant past incidents] (if any)

Deeper analysis? → investigate <area>
Full audit?      → audit
```

Keep it compact — the whole output should fit on one screen.

### Survey All

When `all` is specified, scan all active projects and show a summary table:

```
Survey: All Active Projects

#1 ProjectA  — .NET 10 + Nuxt 3  | Clean     | 2 days ago
#2 ProjectB  — .NET 9 + React 19 | 3 dirty   | 3 days ago
#3 ProjectC  — Next.js 15        | Clean     | 2 weeks ago
```

---

## Lv.2: Investigate

Focused investigation of a specific area — trace bugs, reveal hidden patterns, analyze code flow.

### Arguments

| Argument | Action | Example |
|----------|--------|---------|
| `<file path>` | Analyze specific file | `investigate src/services/AuthService.cs` |
| `<topic>` | Investigate topic across project | `investigate authentication` |
| `bug <description>` | Bug investigation mode | `investigate bug search not working` |
| `review <file>` | Code review mode | `investigate review PaymentService.cs` |

### Step 1: Dependency Scan

- [ ] Frontend: Package manifest + custom component wrappers (read actual type definitions)
- [ ] Backend: Project file + dependency injection/service registrations (e.g., `Program.cs`, `app.module.ts`, `main.go`)
- [ ] Never assume standard library behavior — verify against actual source

### Mode A: File Analysis

- [ ] Read the target file completely
- [ ] Map dependencies (what it imports/uses)
- [ ] Map dependents (what uses this file — grep for references)
- [ ] Check pattern compliance with project conventions
- [ ] Identify issues: bugs, code smells, deviations
- [ ] Report connections to larger architecture

```
Investigate: AuthService.cs

Location:     src/Application/Services/AuthService.cs
Dependencies: IUserRepository, IJwtService, IRefreshTokenRepository
Used by:      AuthController.cs, MiddlewareExtensions.cs

Findings:
  1. Token expiry hardcoded (line 47) — should be from config
  2. No rate limiting on login attempts
  3. RefreshToken rotation working correctly

Hidden Pattern:
  Logout doesn't invalidate ALL refresh tokens for a user —
  only the current one. Multi-device login leaves stale tokens.

Related library entries: [jwt-refresh-token-pattern] (if Library System installed)
```

### Mode B: Topic Investigation

- [ ] Search across all project files for related terms
- [ ] Map all files touching this topic
- [ ] Trace data/logic flow end-to-end:

```
Entry Point → Controller → Service → Repository → Database
     |             |           |           |           |
  [Route]    [Validation]   [Logic]    [Query]     [Table]
```

- [ ] Report hidden patterns and undocumented behavior

### Mode C: Bug Investigation

- [ ] Parse symptom — what's failing, when, where?
- [ ] Trace backwards from symptom to root cause:

```
Symptom: "[description]"
    |
UI: Component → handler function
    |
API: endpoint call
    |
Backend: Controller → Service → [where it breaks]
    |
ROOT CAUSE: [specific cause with file:line]
```

- [ ] Provide fix options with recommendation

### Mode D: Code Review

- [ ] Read the file
- [ ] Review checklist:
  - Follows project conventions (naming, structure)
  - Error handling present and appropriate
  - No hardcoded secrets or magic numbers
  - Input validation at boundaries
  - Null safety / defensive coding
  - Performance considerations
  - Test coverage exists
- [ ] Score and report findings

### Investigate Output Format

```
Investigate: [target]

Location:  [file path or topic scope]
Files:     [N files touching this area]

Findings:
  1. [Finding with file:line reference]
  2. [Finding with file:line reference]

Hidden Patterns:
  [Non-obvious behavior or undocumented assumptions]

Related: [library entries if Library System installed]
Escalate: investigate <deeper area> | audit (if systemic)
```

---

## Lv.2: Refine (Corrective)

Reviews changed code for reuse, quality, and efficiency — then fixes what it finds.

**Key difference from other tiers**: Refine doesn't just observe — it acts. After presenting findings, it fixes issues with permission.

### Arguments

| Argument | Action | Example |
|----------|--------|---------|
| `<file>` | Review specific file | `refine src/services/SlaService.cs` |
| `<area>` | Review area/feature | `refine auth`, `refine dashboard` |
| *(none)* | Review all changed files (git diff) | `refine` |

### Step 1: Dependency Scan

- [ ] Frontend: Read package manifest + scan custom component wrappers
- [ ] Backend: Read project file + check DI/service registrations
- [ ] Never assume standard props — read actual component type definitions

### Step 2: Identify Scope

| Target | Scope |
|--------|-------|
| No argument | `git diff --name-only` + `git diff --cached --name-only` — all changed files |
| File path | That specific file |
| Area keyword | Grep for related files, review the cluster |

Skip: Generated files, migrations, lock files, `node_modules`, `bin/`, `obj/`

### Step 3: Read & Understand

For each file in scope:
- [ ] Read the full file — understand context, not just the diff
- [ ] Read the diff — focus on what changed
- [ ] Identify intent — what is the author trying to do?

**Rule**: Understand intent before judging quality. Never "fix" something that was intentional.

### Step 4: Analyse (The Refinement Checklist)

#### Code Quality
- [ ] Dead code — unused variables, unreachable branches, commented-out blocks
- [ ] Duplication — same logic repeated (extract if 3+ occurrences)
- [ ] Naming — clear, consistent with project conventions
- [ ] Complexity — can any nested logic be simplified?

#### Reuse & Structure
- [ ] Existing utilities — is there already a helper for this?
- [ ] Abstraction level — too low (verbose) or too high (over-engineered)?
- [ ] Single Responsibility — does each function/class do one thing?

#### Efficiency
- [ ] Obvious N+1 queries or unnecessary loops
- [ ] Missing early returns that would reduce nesting
- [ ] Unnecessary allocations or copies

#### Project Rules Compliance
- [ ] Follows project coding rules (check CLAUDE.md or project conventions)
- [ ] API contract respected (backend naming → frontend follows)
- [ ] Date/time handling correct for the project's timezone strategy

#### What NOT to Flag
- Style preferences that don't affect correctness
- Missing documentation on code that wasn't changed
- Performance micro-optimizations that don't matter at scale
- "Best practices" that add complexity without value

### Step 5: Report Findings

```
Refine: [scope]

Reviewed: [N] files, [N] lines changed

Found:
  [N] issues to fix (dead code, bugs, N+1)
  [N] suggestions (could improve, optional)
  [N] files — clean, no action needed

Details:
  [file:line] — [category] — [description]
```

### Step 6: Fix (With Permission)

After presenting findings, **always ask the user before applying any fixes**:

1. **Present findings** with the report format above
2. **Ask user**: "Fix all? Fix critical only? Skip?"
3. **On approval** — apply the requested fixes
4. **Verify** — run build after fixes to confirm nothing broke
5. **Report** what was changed

#### Fix Categories

| Category | Behavior |
|----------|----------|
| Dead code, unused imports | Safe to fix — no behavior change. Still ask first. |
| Obvious bugs | Always ask — explain the bug and proposed fix |
| Simplification | Present as suggestion — user decides |
| Reuse opportunity | Present as suggestion — user decides |

**Rule**: Never auto-apply fixes without user approval. Present findings first, fix second.

---

## Lv.3: Audit

Full system audit — ALL connections, dependencies, data flows, and their consequences revealed.

### Arguments

| Argument | Action | Example |
|----------|--------|---------|
| `<project>` | Full audit of specific project | `audit tariqms` |
| *(none)* | Audit current project context | `audit` |
| `cross` | Cross-project analysis | `audit cross` |

### Step 1: Dependency Scan (Full)

#### Frontend
- [ ] Read package manifest (`package.json`, etc.) — UI library, state management, build tool, test framework
- [ ] Scan component directories — list all custom component wrappers
- [ ] Read key custom components' type/interface definitions
- [ ] Check compiler/bundler config (`tsconfig.json`, `vite.config.ts`, etc.) — path aliases, strictness

#### Backend
- [ ] Read project file (`.csproj`, `pom.xml`, `go.mod`, etc.) — dependencies, target framework
- [ ] Read entry point (`Program.cs`, `main.go`, `app.module.ts`, etc.) — DI registrations, middleware, auth scheme
- [ ] Check for custom base classes, shared constants, conventions

### Step 2: Load Full Context

- [ ] Read project context files (if session tracking is configured)
- [ ] Search library/knowledge base for related entries (if Library System installed)
- [ ] Check recent session history with this project (if diary/session system is configured)

This is the only tier that loads FULL available context before analysis. Skip any context sources that are not configured.

### Step 3: Architecture Map

Read the entire project structure and draw an architecture diagram:

```
Audit: [PROJECT] — Full System Audit

ARCHITECTURE MAP
+-----------------------------------------------+
|                    CLIENT                       |
|  [Framework] + [UI Library] + TypeScript        |
|  Pages -> State -> API calls                    |
+------------------------+----------------------+
                         | HTTP/HTTPS
+------------------------v----------------------+
|                 API LAYER                       |
|  [Backend Framework]                            |
|  Controllers -> Services                        |
+-----------------------------------------------+
|              APPLICATION LAYER                  |
|  Services, DTOs, Interfaces                     |
+-----------------------------------------------+
|               DOMAIN LAYER                      |
|  Entities, Enums, Value Objects                 |
+-----------------------------------------------+
|            PERSISTENCE LAYER                    |
|  [ORM] + [Database]                             |
+------------------------+----------------------+
                         |
              +----------v----------+
              |    [Database]       |
              +---------------------+
```

### Step 4: Dependency Analysis

Map ALL dependencies — internal and external:

- [ ] **Internal**: Controller → Service → Repository → Database chain for each major module
- [ ] **External**: NuGet/npm packages (versions, outdated?), external APIs, infrastructure
- [ ] **Implicit/Hidden**: Hardcoded values, data shape assumptions, cross-table relationships not enforced by FK, environment-specific behavior

```
DEPENDENCY MAP

Explicit (enforced):
  EntityA -> EntityB (FK: entity_b_id)

Implicit (NOT enforced):
  ! Config dictionary hardcoded in Service — no migration
  ! String comparison for role check — not constant/enum
```

### Step 5: Data Flow Audit

Trace ALL data flows through the system:

- [ ] For each major feature, trace: Entry Point → Processing → Storage → Output
- [ ] Identify data transformations at each step
- [ ] Flag any flows with missing validation or authorization gaps

### Step 6: Risk Assessment

Categorize findings by risk level:

```
RISK ASSESSMENT

HIGH:
  - [Critical finding with impact]

MEDIUM:
  - [Notable finding, should address]

LOW:
  - [Minor, address when convenient]
```

### Step 7: Recommendations

Based on full audit, provide prioritized actionable recommendations:

```
RECOMMENDATIONS (prioritized)

1. [HIGH] [Action item with clear rationale]
2. [MED]  [Action item]
3. [LOW]  [Action item]
```

### Step 8: Knowledge Connections

Link findings to existing library entries (if Library System installed):
- [ ] Search library for entries related to audit findings
- [ ] Suggest library entries to reference or create
- [ ] Flag if audit reveals knowledge gaps worth documenting

### Audit Cross — Cross-Project Analysis

When `cross` is specified, analyze shared patterns across all active projects:

```
Audit: Cross-Project Analysis

SHARED PATTERNS
  Auth: JWT + Refresh Token — ProjectA, ProjectB, ProjectC
  DB:   PostgreSQL — ProjectA, ProjectB
  Arch: Clean Architecture — ProjectA, ProjectB

DIVERGENCES
  Frontend: Vue (A) vs React (B) vs Next.js (C)
  Hosting:  Railway (A) vs IIS (B) vs Vercel (C)

OPPORTUNITIES
  - Auth pattern could be extracted to shared library
  - Database patterns consistent across projects
```

---

## Shared: Dependency Scan Philosophy

All tiers start with a dependency scan. This is deliberate — observation skills review code against patterns. Wrong pattern assumptions lead to wrong findings and broken builds.

**Rule**: Never assume standard library behavior. Custom wrappers may change prop signatures, method behavior, or DI lifetimes. Always verify against actual source before suggesting changes.

---

## Cross-Feature Integration

### Library System
When the Library System is installed, observation tiers integrate with it:
- **Survey**: Check library for domain-related entries
- **Investigate**: Reference relevant library entries in findings
- **Audit**: Link findings to library knowledge, suggest new entries for undocumented patterns
- **Refine**: Check if existing utilities exist in library before suggesting new abstractions

### Post-Mortem System
When the Post-Mortem System is installed:
- **Survey**: Cross-reference project against past post-mortem entries (domain lesson check)
- **Investigate (bug mode)**: Check if similar bugs were documented before
- **Audit**: Surface recurring failure patterns across post-mortems

### Work-Plan Execution
- **Survey** before planning → informed scope assessment
- **Refine** after each work-plan task → quality gate before commit
- **Audit** after major milestones → systemic health check

### Auto-Commit System
- **Refine** → fixes applied → auto-commit (if installed)

---

## Cost Awareness

Not all tiers require the same computational effort. Matching tier to model saves cost without sacrificing quality.

| Tier | Effort | Delegation Strategy | Rationale |
|------|--------|-------------------|-----------|
| **Survey** | Low | Can delegate to lighter model/agent | Mostly file scanning, git status — minimal reasoning needed |
| **Investigate** | Medium | Primary AI recommended | Requires code comprehension, flow tracing, root cause analysis |
| **Refine** | Medium | Primary AI recommended | Must understand intent before fixing — nuance matters |
| **Audit** | High | Primary AI recommended | Deep reasoning, cross-system analysis, risk assessment, architectural judgment |

### Practical Guidelines

- **Survey** can run as a background agent or lighter model — it's mostly file scanning and git commands
- **Investigate** and **Refine** benefit from the primary AI's reasoning — pattern matching, intent understanding, and judgment calls
- **Audit** is the most expensive tier — reserve for milestone reviews, not daily checks
- **Survey is cheap to run often** — low cost and catches problems early. Consider running before every planning session.
- **Refine before every commit** — medium cost but prevents expensive bugs from shipping

### Cost-Saving Pattern

```
Daily workflow:
  Survey (low)  → code → Refine (medium) → commit
                         ^-- catches issues before they compound

Weekly/milestone:
  Audit (high)  → captures systemic issues that daily Refine misses
```

The key insight: **frequent cheap observation prevents expensive deep audits**. A team that Surveys daily and Refines before every commit rarely needs emergency Audits.

---

## Mandatory Rules

1. **Always dependency scan first** — never review code without understanding the project's actual stack and custom components
2. **Never assume standard library behavior** — read actual source, especially for UI component wrappers
3. **Understand intent before judging** — the author's approach may be intentional; don't "fix" what isn't broken
4. **Escalate, don't skip tiers** — if Survey reveals complexity, suggest Investigate or Audit; don't try to deep-dive in a Survey
5. **Refine always asks permission before fixing** — present findings first, apply fixes only after user approval
6. **Compact output for Survey** — should fit on one screen; deeper tiers can be verbose
7. **Link to library when available** — if Library System is installed, connect findings to existing knowledge entries; skip gracefully if not installed
8. **Report format consistency** — use the output templates defined in each tier for recognizable, parseable output

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| **No project context** | Ask user to specify a project or navigate to a project directory |
| **Empty project (no code yet)** | Survey reports structure only; Investigate/Refine/Audit skip with "no code to observe" |
| **Only backend or only frontend** | Skip irrelevant dependency scans; adapt output format |
| **No git history** | Skip Recent Activity and git-diff-based Refine scope; note in output |
| **User asks for "review"** | Disambiguate: code review → Investigate (review mode) or quality pass → Refine |
| **Library System not installed** | Skip library cross-references; observation still works independently |
| **Post-Mortem System not installed** | Skip domain lesson check in Survey; no past incident references |
| **Refine finds no issues** | Report clean: "No issues found. Code is sharp." |
| **Audit of very large project** | Warn about time requirement; offer to audit specific subsystems instead |
| **Cross audit with no shared patterns** | Report divergences as the finding — diversity isn't a problem unless it causes maintenance burden |

## Level History

- **Lv.1** — Base: Four-tier observation system (Survey, Investigate, Refine, Audit) with escalation paths between tiers. Survey scans project health in 30 seconds. Investigate traces bugs, reviews code, and maps data flows. Refine reviews changed code and fixes issues with permission. Audit performs full system audit with architecture mapping, dependency analysis, risk assessment, and recommendations. (Origin: Developed and refined across multiple production projects)
- **Lv.2** — Cross-Feature: Integration with Library System (knowledge connections), Post-Mortem System (domain lesson check), Work-Plan Execution (quality gates), and Auto-Commit System (refine-then-commit chain). Observation becomes aware of the broader skill ecosystem.
