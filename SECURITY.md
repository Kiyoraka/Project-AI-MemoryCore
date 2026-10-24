# Security Policy

## Security maintainer

**Afif Maahi** (GitHub: [Kiyoraka](https://github.com/Kiyoraka)) is the security maintainer for AI MemoryCore and the point of contact for vulnerability reports. He reviews every report personally.

## Reporting a vulnerability

Please do not open a public issue for a security problem.

- Use GitHub's **private vulnerability reporting** on this repository (Security tab, "Report a vulnerability"), or
- Email **wings.dark7@gmail.com** with `MemoryCore security` in the subject line.

You will receive an acknowledgement within **7 days**. Once a report is confirmed, a fix lands on `main` and the reporter is credited in the commit unless they ask otherwise.

## Supported versions

| Branch / snapshot | Supported |
|-------------------|-----------|
| `main`            | Yes       |
| Older snapshots   | No        |

## Scope

AI MemoryCore is a file-based memory architecture for AI assistants: Markdown memory files, a master index, a setup guide and a setup wizard. Reports in scope include:

- prompt-injection paths through memory files, diary entries or library items that an assistant loads as context;
- secret or credential leakage in the templates, examples or setup wizard;
- unsafe file handling in the setup flow (path traversal, overwriting files outside the memory folder);
- any instruction in the templates that would make an assistant act unsafely on a user's machine.

Out of scope: vulnerabilities in the AI models or hosting platforms the architecture is used with, and issues in forks that changed the templates.

## Responsible use

This project is a template others build companions on. Please test only against your own copy.
