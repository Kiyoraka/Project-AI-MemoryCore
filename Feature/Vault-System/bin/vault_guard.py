#!/usr/bin/env python3
"""PreToolUse hook: block the shortcuts that would read a secret directly.

The broker is the sanctioned path. Anything that reaches around it is denied.

This is a guard rail, not a wall. An agent with shell access and intent can
still work around it. What it reliably stops is the accidental `cat .env` that
would otherwise paste a live key into the transcript forever.
"""

import json
import re
import sys

RULES = [
    (re.compile(r"\bbw\s+(get\s+(password|item)|list\s+items|export)\b"),
     "Vault: do not read secrets straight out of Bitwarden. "
     "Use 'vault run --secret NAME -- <command>' so the value stays out of the transcript."),

    (re.compile(r"\bsecurity\s+(find|dump)-generic-password\b"),
     "Vault: the session token in the Keychain is not readable directly. Use 'vault run'."),

    (re.compile(r"\bsecret-tool\s+lookup\b.*jarvis-vault"),
     "Vault: the session token in libsecret is not readable directly. Use 'vault run'."),

    (re.compile(r"ConvertTo-SecureString.*jarvis-vault", re.I),
     "Vault: the DPAPI blob is not readable directly. Use 'vault run'."),

    (re.compile(r"vault\S*\s+run\b.*--\s*(echo|printf|cat|env|printenv|set|export|tee|base64|xxd|od|type)\b"),
     "Vault: 'run' is not for displaying secrets. A command that only prints its "
     "environment would put the value straight into the transcript."),

    # Anchored at the start of a line or pipeline segment. An earlier version
    # matched anywhere in the command, so a heredoc that merely mentioned .env
    # in its text was refused. Guard rails that fire on prose get switched off.
    (re.compile(r"(?:^|[|;&]\s*)\s*(?:sudo\s+)?(cat|less|more|head|tail|bat|type)\s+[^|;&\n]*\.env(\.[a-z]+)?\b"),
     "Vault: .env files hold credentials. Read the key names with 'vault list' instead."),
]


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return

    command = (data.get("tool_input") or {}).get("command") or ""
    if not command:
        return

    for pattern, reason in RULES:
        if pattern.search(command):
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }))
            return


if __name__ == "__main__":
    main()
