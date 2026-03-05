# 📐 Architecture Entry Format
*Template for system design pattern entries - Visual reference books*

## Philosophy
Library entries should be like **reference books**:
- ASCII diagrams as PRIMARY content
- Only relevant architectural information
- No implementation checklists (that's project management)
- Generic and reusable across projects

## Required Fields
- Pattern name and one-line description
- When to use (brief)
- ASCII diagrams (main content!)
- Real-world reference implementation (brief, at end)

## Template

```markdown
# [Pattern Name]
*[One-line description of what this pattern does]*

## Overview

### What is [Pattern Name]?
[Brief explanation - 2-3 sentences]

### When to Use
- [Condition 1]
- [Condition 2]
- [Condition 3]

---

## Architecture Diagrams

### [Diagram 1 Title]
```
[ASCII diagram - MAIN CONTENT]
```

### [Diagram 2 Title]
```
[ASCII diagram]
```

(Add more diagrams as needed - diagrams are the PRIMARY content!)

---

## Key Concepts

### [Concept 1]
[Brief explanation with code example if needed]

```language
// Code example
```

### [Concept 2]
[Brief explanation]

---

## Tech Stack Options

| Component | Option 1 | Option 2 | Option 3 |
|-----------|----------|----------|----------|
| [Component 1] | [Option] | [Option] | [Option] |
| [Component 2] | [Option] | [Option] | [Option] |

---

## Benefits

| Benefit | Description |
|---------|-------------|
| [Benefit 1] | [Description] |
| [Benefit 2] | [Description] |

## When NOT to Use
- [Anti-pattern 1]
- [Anti-pattern 2]

---

## Reference Implementation

### [Project Name] ([Year])
[Brief description - 3-5 bullet points, NO project-specific diagrams]
- [Key detail 1]
- [Key detail 2]
- [Key detail 3]

---
*Documented: [Date]*
*Based on: [Real project reference]*
```

## Section Order (Important!)
1. **Overview** - What & When
2. **Architecture Diagrams** - MAIN CONTENT (generic diagrams)
3. **Key Concepts** - Code examples, brief explanations
4. **Tech Stack Options** - Technology choices table
5. **Benefits** - Why use this pattern
6. **When NOT to Use** - Anti-patterns
7. **Reference Implementation** - Brief mention at END (no diagrams)

## Diagram Guidelines
- Use box-drawing characters: `┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼`
- Use arrows: `→ ← ↑ ↓ ▲ ▼ ► ◄`
- Use icons sparingly: `📖 💾 🔒 📚 🏫 💰`
- Keep diagrams readable (not too wide)
- Multiple focused diagrams > one cluttered diagram
- **GENERIC labels only** (Module A, DB1) - no project-specific names

## Example Entry Names
- `multi-app-ecosystem-pattern` - Multiple apps sharing resources
- `dual-database-pattern` - Separate public/private databases
- `rank-based-access-pattern` - Hierarchical content access
- `cache-layer-pattern` - Multi-layer caching strategy

---
*Format v2.1 - January 4, 2026*
*Philosophy: Visual reference books, not implementation guides*
*Updated to match multi-app-ecosystem-pattern.md structure*
