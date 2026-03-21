# Decision Log System
*Append-only record of non-obvious decisions your AI companion helps you make*

## What This Feature Does
Adds a dedicated decision log that captures the reasoning behind important choices:

- **Append-only log** of architectural, technical, and strategic decisions
- **Context + Decision + Rationale** format for each entry
- **Searchable history** of "why did we do it this way?"
- **Never edited** -- past decisions are immutable, new context creates new entries
- **Cross-session persistence** -- survives memory resets and context changes

## The Problem It Solves

You and your AI companion make dozens of decisions during a project:
- "Should we use approach A or B?"
- "Why did we structure it this way?"
- "What was the trade-off we accepted?"

Without a log, these decisions exist only in conversation history, which gets
compacted, archived, or lost. Weeks later, you wonder "why did we do it this
way?" and nobody remembers.

The Decision Log captures the WHY behind non-obvious choices, creating an
immutable record that future sessions can reference.

## Quick Integration
```bash
# Load this feature into your AI companion:
"Load decision-log"
```

## How It Works After Integration

### **Decision Entry Format**
```markdown
## YYYY-MM-DD -- Short title of the decision
**Context**: What situation prompted this decision
**Decision**: What was chosen and what was rejected
**Rationale**: Why this choice was made (trade-offs, constraints, evidence)
```

### **Example Entries**
```markdown
## 2025-10-01 -- Database: PostgreSQL over MongoDB
**Context**: Starting new project, need to choose database. Data is relational
with many foreign key relationships.
**Decision**: PostgreSQL with Prisma ORM. Rejected MongoDB (document model
doesn't fit relational data), rejected raw SQL (maintenance burden).
**Rationale**: Prisma provides type-safe queries and migration management.
PostgreSQL handles our relational model naturally. The team has more SQL
experience than NoSQL. Trade-off: less flexible schema evolution, accepted
because our data model is well-defined.

## 2025-10-03 -- Auth: session-based over JWT
**Context**: Need authentication for web app. Considering JWT tokens vs
server-side sessions.
**Decision**: Server-side sessions with Redis store. Rejected JWT
(can't revoke tokens without blacklist, which re-introduces server state anyway).
**Rationale**: Our app requires immediate session revocation (admin can
deactivate users). JWT's stateless advantage disappears when you need a
blacklist. Sessions in Redis give us revocation + horizontal scaling.
```

### **When to Log a Decision**
Your AI automatically detects decision-worthy moments:
- "Let's go with X instead of Y"
- "We chose this because..."
- "The trade-off is..."
- "Should we use A or B?" (after the decision is made)
- Architecture changes, technology choices, workflow decisions
- Anything where future-you would wonder "why?"

### **What NOT to Log**
- Obvious choices (using git for version control)
- Temporary decisions (formatting preferences that can change anytime)
- Implementation details (how, not why)

## Why Append-Only?

The append-only constraint is deliberate:

1. **Immutability** -- past decisions reflect past context. Editing them would rewrite history.
2. **Audit trail** -- you can see how your thinking evolved over time.
3. **Contradiction is fine** -- if you reverse a decision, log a NEW entry explaining why. Both entries stay.
4. **Searchable** -- grep for keywords to find when and why a decision was made.

## Post-Integration Structure
```
main/
├── identity-core.md          # Existing
├── relationship-memory.md    # Existing
├── current-session.md        # Existing
└── decisions.md              # NEW: append-only decision log
```

## Proven System
Based on production AI companion systems with 4+ months of daily use:
- 20+ architectural decisions logged and referenced across sessions
- Prevents "why did we do it this way?" confusion weeks later
- Contradiction tracking reveals how understanding evolved
- Natural detection means decisions are captured without extra effort

## Synergy with Other Features

| Feature | Synergy |
|---------|---------|
| **Echo Memory Recall** | Search decision log with "do you remember why we chose X?" |
| **Save Diary System** | Diary captures what happened; decision log captures why |
| **Auto-Commit System** | Decision log entries can trigger a commit for version tracking |
| **Reminders System** | "Revisit this decision in 2 weeks" becomes a reminder |

## Benefits
- **Institutional memory** across sessions and context resets
- **Faster onboarding** when returning to a project after weeks
- **Confident reversals** -- know exactly what trade-offs were accepted
- **Zero maintenance** -- AI detects and logs decisions naturally
- **Immutable history** -- past reasoning preserved exactly as it was

---

*Capture the WHY behind every important choice -- future you will thank present you*
