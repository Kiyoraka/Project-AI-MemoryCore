# 💼 Career Coach System

A career-tracking layer for your AI companion — turns the job search, resume
iteration, and a fundamentals/skills rebuild into an ongoing, file-backed
thread instead of something re-explained from scratch every session.

---

## What It Does

- **Asks about your career goals on first use** — a short onboarding
  conversation (current status, target role, timeline, immediate priority)
  the very first time the skill activates, so the dashboard starts with real
  content instead of an empty template
- **Opens every career conversation with a recap** — current status + active
  initiatives, pulled from `career-progress.md`, before diving into the new topic
- **Tracks the resume as a living document** — `resume.md` stays current,
  with every revision logged (with reasoning) to `resume-feedback.md`
- **Logs fundamentals/skills practice** — a concept checklist plus a dated
  practice log, useful for anyone rebuilding technical fundamentals alongside
  a job search
- **Tracks interview outcomes over time** — a simple dated log of applications,
  stages reached, and results
- **Never writes silently** — every log update and resume edit is drafted and
  shown before it's saved

---

## Example: First Activation

```
You: help me improve my resume

AI: Before we dive in — a few quick questions so I can track this properly:
    1. Where are you at right now — actively searching, employed and open,
       a career restart, or entering the workforce for the first time?
    2. What role(s) are you targeting?
    3. Any timeline or deadline?
    4. What do you want help with first?

You: [answers]

AI: Got it — logged that to career-progress.md. Now, let's look at your resume...
```

## Example: Every Activation After That

```
📋 Career status: Actively searching, targeting Backend Engineer roles.
Active: Resume — Round 2 revision in progress.

What's on your mind today?
```

---

## Companion Systems

Works standalone — only needs a `career/` folder. Optionally enhanced by:

| System | Enhancement |
|--------|-------------|
| **Session Briefing System** | Could surface career status in the session-start brief |
| **Topic Diary System** | Complementary — topic-diary is for reusable general knowledge, `career/` is for this one ongoing life domain |
| **Post-Mortem System** | A failed interview round or a bad resume send could be post-mortem material if the lesson generalizes beyond this one job search |

---

## Commands

| Input | Action |
|-------|--------|
| First career-related message, ever | Onboarding runs automatically, then the dashboard is created |
| Any career/resume/job-search/interview message after that | Recap delivers, skill engages |
| A resume edit is discussed | Offers to log to `resume-feedback.md` |
| A shipped project comes up | Offers to draft a `resume.md` update |
| A fundamentals practice session happens | Offers to log to `fundamentals-tracker.md` |
| An interview outcome is mentioned | Offers to log to `interview-log.md` |

---

## Requirements

- A `career/` folder the AI companion can write to — nothing else is required
- No dependency on Skill Plugin System, but works well as one if you have it installed

---

## Installation

See `install-career-coach.md` for step-by-step setup.
