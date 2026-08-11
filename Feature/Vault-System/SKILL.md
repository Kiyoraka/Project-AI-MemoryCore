# Vault System Skill

*How the AI should handle credentials once this feature is loaded.*

## Activation

When the user says `Load vault-system`, read this file and follow it for the rest of the session.

## Core rule

Never ask for, read, echo, or write down a secret value. Refer to secrets by name only.

When a task needs a credential, run the command through the broker:

```bash
vault run --secret OPENAI_API_KEY -- python3 script.py
```

The value arrives in the child process as an environment variable. You will not see it, and you do not need to.

## What to do in common situations

**The user asks you to use an API key.**
Check `vault list` for the name. If it is there, use `vault run`. If it is not, tell the user to add it in their own terminal with `vault add NAME`, because the input is hidden there and never reaches the transcript.

**A command fails with an authentication error.**
Check `vault rules` first. The usual cause is a missing allowlist entry, not a wrong key. Suggest the exact line to add. Never try to read the key to compare it.

**The user pastes a credential into chat anyway.**
The catch hook should have taken it. If it slipped through, say so plainly, tell them to rotate it, and offer to store the replacement properly. Do not repeat the value back to them, not even partially masked.

**You need a secret inside code you are writing.**
Write `os.environ["OPENAI_API_KEY"]` and let the broker supply it at run time. Never write a literal key into a file, not even a placeholder that looks real.

**The user asks you to print or check a secret.**
Decline and offer what actually answers the question underneath: `vault list` to confirm it exists, `vault rules` to confirm it is permitted, or a command that uses the key and reports whether the call succeeded.

## Writing allowlist entries

Suggest the narrowest entry that does the job. One secret, the specific programs that need it.

```json
{
  "STRIPE_SECRET_KEY": ["python3"]
}
```

Never suggest adding `echo`, `cat`, `env`, `printenv`, `bash` or `sh`. Those either print the environment or hand it to an arbitrary child, which defeats the point.

## Honest framing

If the user asks whether this makes them safe, do not oversell it.

The allowlist stops accidents and wrong commands. It does not stop a determined script running under a permitted interpreter. The catch hook fires after the keystroke, so anything it catches has already touched the local machine and should be rotated. The operating system is the real boundary.

Say this once, when it is relevant, then get on with the work.
