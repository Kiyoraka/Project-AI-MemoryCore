# 🔄 Workflow Entry Format
*Template for business process flow entries*

## Required Fields
- Workflow name and description
- Trigger/start point
- Steps with actors
- End states
- Projects using this

## Template

```markdown
# [Workflow Name]
*[What this workflow accomplishes]*

## Overview
- **Trigger**: [What starts this workflow]
- **Actors**: [Who is involved]
- **End State**: [What completion looks like]
- **Duration**: [Typical time to complete]

## Flow Diagram

```
[ASCII diagram of the workflow]

Example:
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Start   │────▶│ Step 1  │────▶│ Step 2  │
└─────────┘     └────┬────┘     └────┬────┘
                     │               │
                     ▼               ▼
                ┌─────────┐     ┌─────────┐
                │ Error   │     │ Success │
                └─────────┘     └─────────┘
```

## Steps

### Step 1: [Step Name]
- **Actor**: [Who performs this]
- **Action**: [What happens]
- **Input**: [What's needed]
- **Output**: [What's produced]
- **Next**: [Where to go next]

### Step 2: [Step Name]
- **Actor**: [Who performs this]
- **Action**: [What happens]
- **Input**: [What's needed]
- **Output**: [What's produced]
- **Next**: [Where to go next]

## Decision Points

| Condition | Path |
|-----------|------|
| [If X] | [Go to Y] |
| [If A] | [Go to B] |

## Error Handling
- [Error scenario 1]: [Recovery action]
- [Error scenario 2]: [Recovery action]

## Notifications
- [Event 1]: [Who gets notified, how]
- [Event 2]: [Who gets notified, how]

## Database Changes
- [Table affected]: [What changes]

## Projects Using This
- [Project 1]: [Variations if any]
- [Project 2]: [Variations if any]

---
*Documented: [Date]*
```

## Example Entry Names
- `order-to-delivery` - Complete order fulfillment
- `booking-confirmation` - Booking with confirmation
- `subscription-renewal` - Auto/manual renewal
- `refund-process` - Refund request handling
- `user-registration` - Registration with verification

---
*Format v1.0 - January 3, 2026*
