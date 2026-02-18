# 📋 Skill File - Sample Format
*Reference template for creating SKILL.md files*

---

```markdown
---
name: [skill-name]
description: "MUST use when [trigger condition 1], when user says '[phrase 1]',
             '[phrase 2]', '[phrase 3]', or when [contextual condition].
             Also triggers on '[alternative phrase]'."
---

# [Skill Name] — [Title]
*[One-line tagline describing the skill's purpose]*

## Activation

When this skill activates, output:

`[Activation emoji + message displayed to user]`

Then execute the protocol below.

## Context Guard

[Skill Name] activates only in appropriate contexts.

| Context | Status |
|---------|--------|
| **[Trigger context 1]** | ACTIVE — full protocol |
| **[Trigger context 2]** | ACTIVE — full protocol |
| **[Non-trigger context]** | DORMANT — do not activate |
| **[Another non-trigger]** | DORMANT — do not activate |

## Protocol

### Step 1: [First Action]
- [ ] [Sub-task 1]
- [ ] [Sub-task 2]
- [ ] [Sub-task 3]

### Step 2: [Second Action]
- [ ] [Sub-task 1]
- [ ] [Sub-task 2]

### Step 3: [Third Action]
- [ ] [Sub-task 1]
- [ ] [Sub-task 2]

### Step 4: Confirm
- [ ] Display confirmation to user
- [ ] Report what was done

## Mandatory Rules

1. [Hard rule 1 — something the skill must always do]
2. [Hard rule 2 — something the skill must never do]
3. [Hard rule 3 — a constraint on behavior]

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| **[Edge case 1]** | [How to handle it] |
| **[Edge case 2]** | [How to handle it] |

## Level History

- **Lv.1** — Base: [Description of initial capability]. (Origin: [When and why it was created])
```

---

## Format Notes

### Required Sections
- **YAML Frontmatter** — `name` and `description` are required for auto-discovery
- **Activation** — what to display when the skill fires
- **Protocol** — step-by-step execution logic

### Optional Sections
- **Context Guard** — when to stay dormant (recommended for complex skills)
- **Mandatory Rules** — hard constraints (recommended)
- **Edge Cases** — special situations (add as needed)
- **Level History** — version tracking (add when skill evolves)

### Description Field Best Practices
- Start with `"MUST use when..."` for strong triggering
- List 3-5 specific trigger phrases
- Include contextual conditions beyond just phrases
- Be specific enough to avoid false positives
- Be broad enough to catch all relevant situations

### Leveling Convention
- **Lv.1**: Base capability (initial creation)
- **Lv.2**: Enhanced (added features, reduced friction)
- **Lv.3**: Advanced (proactive behavior, deep integration)
- **Lv.4+**: Expert (fully autonomous, absorbed external protocols)

*Skill Format Template v1.0*
