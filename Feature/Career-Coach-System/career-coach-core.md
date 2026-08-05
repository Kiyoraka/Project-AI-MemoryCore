# Career Coach — Core Protocol

## When to Run
Any time the conversation touches career, job search, resume, interviews, or a
fundamentals/skills rebuild — see SKILL.md's Context Guard for the full trigger list.

---

## Step 0: Career Goals Onboarding (First Activation Only)

Runs exactly once, the first time this skill activates and `career/career-progress.md`
either doesn't exist or is still the empty starter template.

### Step 0.1: Ask
Ask a short, conversational set of questions — not a form. Cover:
1. **Current status** — actively job searching, employed and open to opportunities,
   a career restart, or preparing to enter the workforce for the first time
2. **Target role(s)** — what they're aiming for
3. **Timeline** — any deadline or urgency, if one exists
4. **Immediate priority** — what they want help with first (resume, interview prep,
   fundamentals rebuild, something else)

Keep it to one exchange — four questions asked together, not four separate turns.

### Step 0.2: Write the Initial Dashboard
From the answers, write `career/career-progress.md`:
- **Status** — one or two lines combining current status + target role
- **Active Initiatives** — the immediate priority, as the first tracked item
- **Milestone Log** — a single dated entry marking the start: "Career tracking started — [status], targeting [role]"

### Step 0.3: Continue Naturally
Move directly into the conversation the user actually came for — the onboarding
is a quick setup step, not a gate that delays help.

---

## Step 1: Recap on Activation (Every Subsequent Time)

### Step 1.1: Load Context
Read `career/career-progress.md`.

### Step 1.2: Open With a Brief Recap
State the current Status and Active Initiatives in one or two lines before
addressing the new topic. Don't re-explain full history the user already knows.

---

## Step 2: Update Protocol (Triggered Mid-Conversation)

See SKILL.md's "Update Protocol" and "Entry Formats" sections for the full
confirm-before-write flow across `resume.md`, `resume-feedback.md`,
`fundamentals-tracker.md`, and `interview-log.md`.

Summary:
1. Notice the trigger.
2. Ask: `"Worth logging this to [file]?"`
3. If yes, draft the entry/diff, show it, save only on confirmation.
4. If the update changes overall state, also update `career-progress.md`'s
   Milestone Log and Active Initiatives.
5. If declined, drop it — don't re-ask for the same item.

---

## Minimal Version (Standalone — No Companion Systems)

This feature has no hard dependencies. It only needs a `career/` folder to
write into. If `main/current-session.md` or a Reminders System is present,
career context naturally surfaces there too, but neither is required.
