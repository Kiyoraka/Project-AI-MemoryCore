# 💼 Career Coach System - Installation Protocol
*Career and job-search tracking with a first-use goals onboarding, for AI companions*

## Quick Install Command
```
"install career coach"
```

## Prerequisites
- Core memory system installed (`main/` directory with essential files)
- `master-memory.md` accessible for integration updates
- Skill Plugin System recommended for auto-triggering (optional)

## 4-Step Installation Process

### Step 1: Create Career Folder Structure
- [ ] Create `career/` folder in root directory
- [ ] Create `career/career-progress.md` — **leave empty**. Its emptiness is what triggers the first-use goals onboarding.
- [ ] Create `career/resume.md` with initial template:
  ```markdown
  PROFILE SUMMARY

  WORK EXPERIENCES

  PROJECTS

  TECHNICAL SKILLS

  EDUCATION
  ```
- [ ] Create `career/resume-feedback.md` with a header only:
  ```markdown
  # Resume Feedback — Change Log for resume.md
  ```
- [ ] Create `career/fundamentals-tracker.md` with initial template:
  ```markdown
  # Fundamentals Tracker

  ## Concept Checklist
  | Concept | Confidence | Last Practiced | Notes |
  |---------|-----------|-----------------|-------|

  ## Practice Log
  ```
- [ ] Create `career/interview-log.md` with initial template:
  ```markdown
  # Interview Log

  | Date | Company/Role | Stage Reached | Outcome | Notes |
  |------|--------------|----------------|---------|-------|
  ```

### Step 2: Install Skill (If Skill Plugin System Exists)
- [ ] If Skill Plugin System is installed:
  - Copy `SKILL.md` to `plugins/[plugin-name]/skills/career-coach/SKILL.md`
  - Inform user: "Career coach skill installed -- auto-triggers on 'career', 'resume', 'job hunt', 'interview', 'screening call'"
- [ ] If Skill Plugin System is NOT installed:
  - Inform user: "Career Coach integrated into master memory. Install the Skill Plugin System for auto-triggering."
  - Add career protocol reference to `master-memory.md`

### Step 3: Update Memory System
- [ ] Add to `master-memory.md`:
  ```markdown
  ## Career Coach Commands
  - Career conversations auto-trigger on mentions of career, resume, job hunt, interview, screening call
  - First activation runs a short goals-onboarding conversation, then tracks status in career/career-progress.md
  - "Worth logging this?" is offered before any resume or log update -- nothing saves silently
  ```

### Step 4: Verify and Cleanup
- [ ] Verify `career/` folder structure exists with all 5 files
- [ ] Verify `career/career-progress.md` is genuinely empty (onboarding readiness check)
- [ ] Remove `Feature/Career-Coach-System/install-career-coach.md` (installation script no longer needed)
- [ ] Keep `Feature/Career-Coach-System/career-coach-core.md` in place -- unlike LRU, this system's onboarding and update protocol live in a separate core file that `SKILL.md` references at runtime, not embedded entirely in `SKILL.md` itself
- [ ] Display completion message

## Installation Complete Message
```
Career Coach System Installed Successfully!

First activation: goals onboarding (status, target role, timeline, priority)
Every activation after: status recap from career-progress.md

Tracked Files:
  career-progress.md      - Dashboard: status, active initiatives, milestone log
  resume.md                - Living resume, single source of truth
  resume-feedback.md       - Resume revision history
  fundamentals-tracker.md  - Concept checklist + practice log
  interview-log.md         - Application/interview outcomes

Features:
  First-use goals onboarding (runs once)
  Confirm-before-write on every log/resume update
  Recap-on-activation for session continuity

Your AI companion now has career and job-search memory!
```

## What This System Does
1. **Captures Career Goals on First Use** - a short onboarding conversation seeds the dashboard instead of starting blank
2. **Opens Every Career Conversation with a Recap** - status + active initiatives before the new topic
3. **Tracks the Resume as a Living Document** - revisions logged with reasoning
4. **Logs Fundamentals/Skills Practice** - concept checklist + dated practice log
5. **Tracks Interview Outcomes Over Time** - simple dated log of applications and results
6. **Never Writes Silently** - every save is drafted and shown first

## Notes
- Onboarding runs exactly once -- clearing `career-progress.md` back to empty re-triggers it
- `resume.md` and `career-progress.md` are living documents, edited in place; `resume-feedback.md`, the practice log, and `interview-log.md` are append-only
- No dependency on Skill Plugin System, but auto-triggering works best with it installed

---
*Version 1.0*
*Career and job-search tracking for AI companions*
