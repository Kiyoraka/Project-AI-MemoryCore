# 📦 Library Items — Pre-Made Knowledge Entries
*Production-tested patterns ready to install into your library*

## What Are Library Items?

Library items are **pre-made knowledge entries** that follow the Library System's format templates. Instead of building your library from scratch, install proven patterns instantly and start using them in your projects right away.

## Prerequisites

- **Library System** must be installed first (see `Feature/Library-System/`)
- A working `library/` directory with section folders

## How to Install

Tell your AI companion:

```
"install item security-headers"
```

The AI will:
1. Find the item in `library-items/`
2. Show you what it contains
3. Copy it to your `library/[section]/` folder
4. Commit the change (if Auto-Commit is installed)

You can also browse items manually and copy any `.md` file directly into your `library/[section]/` folder.

## Available Items

| Section | Item | Description |
|---------|------|-------------|
| `security` | `security-headers` | HTTP security headers with CSP — framework-agnostic (Laravel, Express, Spring Boot, Nginx/Apache) |

## Item Format

Each item follows its section's format template (from `library/formats/[section]-format.md`). Items are ready to use as-is — no modification required, though you can customize them for your specific needs.

## Contributing Items

Want to add a new item? Create a `.md` file following the appropriate format template:

1. Pick the right section folder (or create a new one)
2. Follow the format from `Feature/Library-System/formats/[section]-format.md`
3. Write generic, reusable content — no project-specific references
4. Include implementation examples for multiple frameworks where applicable
5. Submit a pull request

### Guidelines
- **Generic over specific** — items should work across projects and frameworks
- **Production-tested** — only share patterns you've used in real projects
- **Format-compliant** — follow the section's format template
- **Self-contained** — each item should be usable without external dependencies

---

*Solve it once, share it forever — community-driven knowledge for AI companions*
