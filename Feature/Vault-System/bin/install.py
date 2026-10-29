#!/usr/bin/env python3
"""Install the Vault System for Claude Code.

Creates the vault directory, seeds an allowlist, registers the two hooks, and
puts a `vault` launcher on PATH. Safe to run twice: existing entries are kept.
"""

import json
import os
import platform
import shutil
import stat
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
HOME = Path(os.environ.get("JARVIS_VAULT_HOME", Path.home() / ".jarvis-vault"))
SETTINGS = Path.home() / ".claude" / "settings.json"
IS_WINDOWS = platform.system() == "Windows"

SEED_ALLOWLIST = {
    "_comment": (
        "Deny by default. A secret with no entry here never leaves the vault. "
        "Key is the secret name, value is the list of programs allowed to receive it."
    ),
    "OPENAI_API_KEY": ["python3", "node", "curl"],
    "ANTHROPIC_API_KEY": ["python3", "node", "curl"],
}


def seed_vault_home():
    HOME.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(HOME, 0o700)
    except OSError:
        pass
    allowlist = HOME / "allowlist.json"
    if not allowlist.exists():
        allowlist.write_text(json.dumps(SEED_ALLOWLIST, indent=2), encoding="utf-8")
        print(f"  created {allowlist}")
    else:
        print(f"  kept    {allowlist}")


def make_launcher():
    """Put a `vault` command somewhere the shell will find it."""
    target = BIN / "jarvis_vault.py"

    if IS_WINDOWS:
        dest_dir = Path(os.environ["LOCALAPPDATA"]) / "Programs" / "jarvis-vault"
        dest_dir.mkdir(parents=True, exist_ok=True)
        launcher = dest_dir / "vault.cmd"
        launcher.write_text(f'@echo off\r\n"{sys.executable}" "{target}" %*\r\n', encoding="utf-8")
        print(f"  created {launcher}")
        print(f"  add this folder to PATH if it is not there yet: {dest_dir}")
        return

    for candidate in ("/usr/local/bin", "/opt/homebrew/bin", str(Path.home() / ".local/bin")):
        directory = Path(candidate)
        if not directory.is_dir() or not os.access(directory, os.W_OK):
            continue
        launcher = directory / "vault"
        launcher.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{target}" "$@"\n', encoding="utf-8")
        launcher.chmod(launcher.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        print(f"  created {launcher}")
        return

    print("  no writable bin directory found. Call jarvis_vault.py directly.")


def register_hooks():
    """Add the guard and catch hooks to Claude Code without touching the rest."""
    SETTINGS.parent.mkdir(parents=True, exist_ok=True)
    settings = json.loads(SETTINGS.read_text(encoding="utf-8")) if SETTINGS.exists() else {}

    if SETTINGS.exists():
        backup = SETTINGS.with_suffix(".json.bak-vault")
        shutil.copy2(SETTINGS, backup)
        print(f"  backup  {backup}")

    wanted = {
        "PreToolUse": {
            "matcher": "Bash",
            "hooks": [{
                "type": "command",
                "command": f'"{sys.executable}" "{BIN / "vault_guard.py"}"',
                "timeout": 10,
                "statusMessage": "Vault guard",
            }],
        },
        "UserPromptSubmit": {
            "hooks": [{
                "type": "command",
                "command": f'"{sys.executable}" "{BIN / "vault_catch.py"}"',
                "timeout": 90,
                "statusMessage": "Vault catch",
            }],
        },
    }

    hooks = settings.setdefault("hooks", {})
    for event, entry in wanted.items():
        existing = hooks.setdefault(event, [])
        marker = "vault_guard.py" if event == "PreToolUse" else "vault_catch.py"
        if any(marker in json.dumps(item) for item in existing):
            print(f"  kept    {event} hook (already registered)")
            continue
        existing.append(entry)
        print(f"  added   {event} hook")

    SETTINGS.write_text(json.dumps(settings, indent=2), encoding="utf-8")


def main():
    print(f"Installing Vault System on {platform.system()}")
    seed_vault_home()
    make_launcher()
    register_hooks()

    print("\nNext:")
    print("  1. Install the Bitwarden CLI and run: bw login")
    print("  2. vault setup-biometrics      (optional, skips the password later)")
    print("  3. vault add OPENAI_API_KEY")
    print("  4. Restart Claude Code so the hooks load")
    print("\nCheck anytime with: vault status")


if __name__ == "__main__":
    main()
