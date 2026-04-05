---
name: continuous-improve
description: "Reflect on the current session, analyze observations for patterns, and review learned rules. Run after finishing significant work."
---

# /continuous-improve

Run this after completing significant work. It does three things in order.

## Step 1: Reflect

Generate a reflection for this session based on what happened:

```
## Reflection — [Date]
- What worked:
- What failed:
- What I'd do differently:
- Rule to add:
```

If there's a "Rule to add", check `~/.claude/mulahazah/rules.md` to see if it already exists. If not, append it.

## Step 2: Analyze Observations

Check if `~/.claude/mulahazah/observations.jsonl` or `~/.claude/mulahazah/projects/*/observations.jsonl` has data.

If observations exist (5+ lines), run the analysis:
```bash
bash ~/.claude/mulahazah/bin/analyze.sh
```

Report what the analysis found (new rules or "no new patterns yet").

If no observations exist, say so — hooks may not be installed.

## Step 3: Show Status

Read `~/.claude/mulahazah/rules.md` and display all learned rules.

Show:
- Total rule count
- Rules grouped by date they were added
- Any rules that should be reviewed (contradictory, outdated, too vague)

If no rules file exists yet, explain this is expected for new installs — rules accumulate over sessions.

## Output Format

```
=== continuous-improve ===

## Session Reflection
- What worked: [from this session]
- What failed: [from this session]  
- What I'd do differently: [from this session]
- Rule to add: [captured and saved]

## Observation Analysis
[N] observations analyzed
[N] new rules extracted (or "no new patterns yet")

## Learned Rules ([N] total)
[list all rules from rules.md]

## Next Steps
- Keep working — hooks capture automatically
- Run /continuous-improve again after your next major task
```
