# Commit Message - Sample Format
*Reference template for structured git commit messages*

## Standard Enhanced Format

**When meaningful development work is committed:**

```
[Achievement Title] - [Brief technical summary]

=== [SECTION 1 NAME] ===
• [File/Component]: [Specific change description]
• [File/Component]: [Specific change description]
• [File/Component]: [Specific change description]

=== [SECTION 2 NAME] ===
• Project: [name] | Type: [development/fix/refactor] | Time: ~XX min
• [Custom field]: [Value]
```

**Example (using default section names TECHNICAL CHANGES + SESSION CONTEXT):**
```
Add user authentication with JWT tokens - secure login system

=== TECHNICAL CHANGES ===
• auth/LoginController.php: Added JWT token generation and validation
• middleware/AuthMiddleware.php: Created authentication guard middleware
• routes/api.php: Added /login, /logout, /refresh endpoints
• config/auth.php: Configured JWT driver with 60-minute expiry

=== SESSION CONTEXT ===
• Project: MyApp | Type: Feature Development | Time: ~45 min
• Focus: Implemented secure authentication flow with refresh tokens
```

## Minimal Format

**When trivial fixes or typos are committed:**

```
Fix typo in README installation instructions
```

No sections needed — just a clear, descriptive one-liner.

## WIP Format

**When saving incomplete work:**

```
WIP: Payment integration - Stripe webhook handling incomplete
```

Use `WIP:` prefix to signal work-in-progress. These commits can be amended later.

---

## Format Notes

### Achievement Title Rules
- Descriptive and action-oriented (what was accomplished, not just what changed)
- Start with a verb: Add, Fix, Implement, Refactor, Update, Remove
- Captures the essence of the work in one line
- Keep under 72 characters for git compatibility

### Section Design
- Section names are **configurable** during installation (you choose what sections to track)
- Section headers use `===` delimiters on both sides for visual clarity
- Each bullet starts with `•` (bullet character) followed by the component and description
- Common section name pairs:
  - `TECHNICAL CHANGES` + `SESSION CONTEXT` (recommended default)
  - `IMPLEMENTATION` + `PROJECT LOG`
  - `CODE CHANGES` + `NOTES`
  - `WHAT CHANGED` + `WHY`

### When to Use Each Format

| Scope | Format | Example |
|-------|--------|---------|
| Feature, bug fix, refactor | Enhanced (all sections) | New login system, database migration |
| Typo, comment, minor rename | Minimal (one-liner) | Fix README typo, rename variable |
| Incomplete save | WIP prefix | Partial API integration |

### What NOT to Do
1. **Never put emoji** inside the actual commit message body
2. **Never make the title vague** ("update files", "fix stuff", "changes")
3. **Never omit section content** when using enhanced format — if a section is empty, remove it
4. **Never commit sensitive files** (.env, credentials, API keys, tokens)
5. **Never include raw diff output** — summarize what changed and why

### Adapting to Your Workflow
The format is a starting point. After installation, you can:
- Add more sections (e.g., `=== TESTING ===` for test coverage notes)
- Change bullet style (• to - or *)
- Add custom fields to your session section
- The AI learns your preferences over time

---

*Commit Format Template v1.0*
