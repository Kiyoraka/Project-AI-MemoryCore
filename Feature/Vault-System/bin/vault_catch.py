#!/usr/bin/env python3
"""UserPromptSubmit hook: take credentials out of a message before the model sees it.

When a message contains something shaped like a credential, the value is stored
in the vault and the message is erased. The model never receives it.

Only very specific patterns are caught. When in doubt the message goes through,
because blocking real work is worse than missing one catch.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

VAULT = str(Path(__file__).with_name("jarvis_vault.py"))

# (suggested name, pattern). Each anchors on a vendor prefix that will not turn
# up by accident in ordinary prose.
PATTERNS = [
    ("ANTHROPIC_API_KEY", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}")),
    ("OPENAI_API_KEY",    re.compile(r"\bsk-(?!ant-)[A-Za-z0-9_\-]{20,}")),
    ("GITHUB_TOKEN",      re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}")),
    ("GITHUB_TOKEN",      re.compile(r"\bgithub_pat_[A-Za-z0-9_]{60,}")),
    ("SLACK_TOKEN",       re.compile(r"\bxox[baprs]-[A-Za-z0-9\-]{10,}")),
    ("AWS_ACCESS_KEY_ID", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("GOOGLE_API_KEY",    re.compile(r"\bAIza[A-Za-z0-9_\-]{35}\b")),
    ("HF_TOKEN",          re.compile(r"\bhf_[A-Za-z0-9]{30,}")),
    ("REPLICATE_TOKEN",   re.compile(r"\br8_[A-Za-z0-9]{30,}")),
    ("STRIPE_SECRET_KEY", re.compile(r"\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{20,}")),
    ("SESSION_TOKEN",     re.compile(r"\b[A-Za-z0-9+/]{60,}={1,2}")),
]

MULTILINE_KEY = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
NAME_HINT = re.compile(r"(?:save as|store as|name it)\s+([A-Z][A-Z0-9_]{2,})", re.I)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return

    prompt = data.get("prompt") or data.get("prompt_text") or ""
    if not prompt:
        return

    hint = NAME_HINT.search(prompt)
    hinted = hint.group(1).upper() if hint else None

    found = [
        (hinted or default, value)
        for default, rx in PATTERNS
        for value in rx.findall(prompt)
    ]
    has_private_key = bool(MULTILINE_KEY.search(prompt))

    if not found and not has_private_key:
        return

    saved, failed = [], []
    for name, value in found:
        try:
            result = subprocess.run(
                [sys.executable, VAULT, "capture", name],
                input=value, capture_output=True, text=True, timeout=90,
            )
            if result.returncode == 0 and result.stdout.strip():
                saved.append(result.stdout.strip())
            else:
                failed.append(name)
        except Exception:
            failed.append(name)

    lines = ["This message was blocked because it contains a credential. "
             "The value was not sent to the model."]
    if saved:
        lines += [
            "",
            "Saved to the vault: " + ", ".join(saved),
            f"Use it later: vault run --secret {saved[0]} -- <command>",
            "Add an allowlist entry before it can be used.",
        ]
    if failed:
        lines += ["", "Could not save: " + ", ".join(failed) + ". Add it manually with: vault add NAME"]
    if has_private_key:
        lines += ["", "A private key block was detected. Add it manually with: vault add NAME"]
    lines += [
        "",
        "Treat this credential as exposed. It passed through your keyboard and "
        "local logs before the hook caught it, so rotate it if it matters.",
        "Send your message again without the value and refer to it by name.",
    ]

    print(json.dumps({"decision": "block", "reason": "\n".join(lines)}))


if __name__ == "__main__":
    main()
