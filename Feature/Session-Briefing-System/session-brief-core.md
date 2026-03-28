# 📋 Session Brief — Core Protocol

## When to Run
At the start of every session, before processing the user's first request.

---

## Step-by-Step Execution

### Step 1: Load Context
Read the following files (in parallel if possible):

| File | Purpose | Required |
|------|---------|----------|
| `main/current-session.md` | Last session recap | Yes |
| `main/reminders.md` | Open reminder items | Optional |
| Project list file | Active project + idle days | Optional |
| Current time | Time period classification | Optional |

### Step 2: Classify Time Period

| Time | Period | Work Suggestion |
|------|--------|----------------|
| 06:00–11:59 | Morning | Architecture, new features, complex problems |
| 12:00–17:59 | Afternoon | Implementation, debugging, testing |
| 18:00–21:59 | Evening | Code review, docs, moderate tasks |
| 22:00–05:59 | Night | Light tasks, planning — suggest wrapping up |

*Requires Time-based-Aware-System. If not installed, skip the work suggestion line.*

### Step 3: Identify Attention Flags
Check project list for projects idle beyond their threshold:

| Flag | Meaning | Default Threshold |
|------|---------|------------------|
| 🟡 | Idle — approaching warning | 14 days |
| 🔴 | Stale — past critical threshold | 30 days |

- Show maximum 3 flags
- If more exist, show the most critical (most days idle) first
- Skip this section entirely if no projects are flagged
- *Requires LRU-Project-Management-System. If not installed, skip this section.*

### Step 4: Compose Brief

```
📋 Session Brief · [Time Period]

Last session: [1–2 line recap from current-session.md]
Active: [project name] · [status]
🔴/🟡 [project name] — [N] days idle
Reminders: [N] open → [first item preview]
Suggestion: [time-appropriate work type]
```

**Composition rules:**
- Total lines: 12 maximum
- Omit any line/section that has nothing to report
- "Last session" is the only mandatory line (requires `current-session.md`)

### Step 5: Deliver
Output the brief before processing the user's first request.

---

## Minimal Version (Standalone — No Companion Systems)

If no companion systems are installed, deliver a minimal brief using only `current-session.md`:

```
📋 Session Brief

Last session: [recap from current-session.md]
```

---

## Threshold Customization

Edit Step 3 thresholds to match your workflow:
- Change `14` and `30` day defaults to any values you prefer
- If using LRU-Project-Management-System with project tiers, apply tier-specific thresholds instead of the defaults
