#!/usr/bin/env python3
"""jarvis_vault - a secret broker for MemoryCore.

Secrets live in Bitwarden. The unlock token lives in the operating system's own
credential store. The AI agent can use a secret without ever reading its value.

Standard library only. Works on macOS, Windows and Linux.

    vault setup-biometrics       enable fingerprint or face unlock
    vault add NAME               store a secret (hidden input)
    vault list                   names only, never values
    vault run --secret NAME -- <command>

Design note: no command in this file prints a secret value to stdout. The only
way a secret leaves the vault is as an environment variable handed to a child
process that an allowlist has approved in advance.
"""

import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from getpass import getpass
from pathlib import Path

HOME = Path(os.environ.get("JARVIS_VAULT_HOME", Path.home() / ".jarvis-vault"))
ALLOWLIST = HOME / "allowlist.json"
AUDIT_LOG = HOME / "audit.log"
CACHE = HOME / "cache"

SERVICE = "jarvis-vault"
ACC_SESSION = "bw-session"
ACC_MASTER = "bw-master"
ITEM_PREFIX = "jarvis/"
FOLDER_NAME = os.environ.get("JARVIS_VAULT_FOLDER", "JARVIS Vault")

OS_NAME = {"Darwin": "macos", "Windows": "windows"}.get(platform.system(), "linux")


class VaultError(Exception):
    pass


def audit(status, secret, actor):
    HOME.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with AUDIT_LOG.open("a", encoding="utf-8") as fh:
        fh.write(f"{stamp}\t{status}\t{secret}\t{actor}\n")


def run(cmd, **kw):
    kw.setdefault("capture_output", True)
    kw.setdefault("text", True)
    return subprocess.run(cmd, **kw)


# ---------------------------------------------------------------- keystore

class KeyStore:
    """Per-OS credential storage. Values never appear in argv where avoidable."""

    def get(self, account):
        raise NotImplementedError

    def set(self, account, value):
        raise NotImplementedError

    def delete(self, account):
        raise NotImplementedError

    @property
    def label(self):
        return self.__class__.__name__


class MacKeyStore(KeyStore):
    """macOS Keychain. Uses `security -i` so values stay out of the process list."""

    label = "macOS Keychain"

    def get(self, account):
        r = run(["security", "find-generic-password", "-s", SERVICE, "-a", account, "-w"])
        return r.stdout.strip() if r.returncode == 0 else ""

    def set(self, account, value):
        # `security -i` reads the command from stdin, which keeps the value out
        # of the process list. It tokenizes like a shell, so quote it properly.
        quoted = '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
        script = f'add-generic-password -s {SERVICE} -a {account} -w {quoted} -U\n'
        r = run(["security", "-i"], input=script)
        if r.returncode != 0:
            raise VaultError(f"keychain write failed: {r.stderr.strip()}")

    def delete(self, account):
        run(["security", "delete-generic-password", "-s", SERVICE, "-a", account])


class WindowsKeyStore(KeyStore):
    """Windows DPAPI. The ciphertext is bound to the current user account,
    so a copied file is useless on another machine or under another login."""

    label = "Windows DPAPI"

    def _path(self, account):
        base = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "jarvis-vault"
        base.mkdir(parents=True, exist_ok=True)
        return base / f"{account}.dpapi"

    def _ps(self, script, value=None):
        env = dict(os.environ)
        if value is not None:
            env["JV_VALUE"] = value
        return run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
            env=env,
        )

    def get(self, account):
        p = self._path(account)
        if not p.exists():
            return ""
        script = (
            f"$s = Get-Content -Raw '{p}' | ConvertTo-SecureString; "
            "$b = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($s); "
            "[Runtime.InteropServices.Marshal]::PtrToStringAuto($b)"
        )
        r = self._ps(script)
        return r.stdout.strip() if r.returncode == 0 else ""

    def set(self, account, value):
        p = self._path(account)
        script = (
            "ConvertTo-SecureString -String $env:JV_VALUE -AsPlainText -Force "
            f"| ConvertFrom-SecureString | Set-Content -NoNewline '{p}'"
        )
        r = self._ps(script, value)
        if r.returncode != 0:
            raise VaultError(f"DPAPI write failed: {r.stderr.strip()}")

    def delete(self, account):
        self._path(account).unlink(missing_ok=True)


class SecretToolKeyStore(KeyStore):
    """Linux with libsecret, which is what GNOME Keyring and KWallet speak."""

    label = "Linux libsecret"

    def get(self, account):
        r = run(["secret-tool", "lookup", "service", SERVICE, "account", account])
        return r.stdout.strip() if r.returncode == 0 else ""

    def set(self, account, value):
        r = run(
            ["secret-tool", "store", "--label", f"{SERVICE}/{account}",
             "service", SERVICE, "account", account],
            input=value,
        )
        if r.returncode != 0:
            raise VaultError(f"secret-tool write failed: {r.stderr.strip()}")

    def delete(self, account):
        run(["secret-tool", "clear", "service", SERVICE, "account", account])


class FileKeyStore(KeyStore):
    """Last resort when no OS keystore is reachable, such as a headless server.

    The file is readable by the owner only. That is weaker than a real keystore
    and the CLI says so out loud rather than pretending otherwise.
    """

    label = "plain file (0600, no OS keystore found)"

    def _path(self, account):
        d = HOME / "keystore"
        d.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(d, 0o700)
        except OSError:
            pass
        return d / account

    def get(self, account):
        p = self._path(account)
        return p.read_text(encoding="utf-8").strip() if p.exists() else ""

    def set(self, account, value):
        p = self._path(account)
        fd = os.open(str(p), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(value)

    def delete(self, account):
        self._path(account).unlink(missing_ok=True)


def keystore():
    if OS_NAME == "macos" and shutil.which("security"):
        return MacKeyStore()
    if OS_NAME == "windows" and shutil.which("powershell"):
        return WindowsKeyStore()
    if OS_NAME == "linux" and shutil.which("secret-tool"):
        return SecretToolKeyStore()
    return FileKeyStore()


# -------------------------------------------------------------- biometrics

TOUCHID_SWIFT = '''
import Foundation
import LocalAuthentication
let reason = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "unlock vault"
let ctx = LAContext()
ctx.localizedFallbackTitle = ""
var err: NSError?
guard ctx.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &err) else { exit(2) }
let sem = DispatchSemaphore(value: 0)
var ok = false
ctx.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: reason) { s, _ in
    ok = s; sem.signal()
}
sem.wait()
exit(ok ? 0 : 1)
'''

# Windows Hello through WinRT. PowerShell has no await, so we poll the async
# operation's status, which is the accepted workaround for calling WinRT here.
HELLO_PS = '''
$ErrorActionPreference = "Stop"
[void][Windows.Security.Credentials.UI.UserConsentVerifier, Windows.Security.Credentials.UI, ContentType=WindowsRuntime]
$op = [Windows.Security.Credentials.UI.UserConsentVerifier]::RequestVerificationAsync($env:JV_REASON)
while ($op.Status -eq 0) { Start-Sleep -Milliseconds 100 }
if ($op.Status -ne 1) { exit 2 }
if ($op.GetResults() -eq 0) { exit 0 } else { exit 1 }
'''


def biometrics_available():
    if OS_NAME == "macos":
        return bool(shutil.which("swiftc") or _touchid_binary(compile_if_missing=False))
    if OS_NAME == "windows":
        return bool(shutil.which("powershell"))
    return bool(shutil.which("fprintd-verify"))


def _touchid_binary(compile_if_missing=True):
    CACHE.mkdir(parents=True, exist_ok=True)
    binary = CACHE / "touchid"
    if binary.exists():
        return binary
    if not compile_if_missing or not shutil.which("swiftc"):
        return None
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "touchid.swift"
        src.write_text(TOUCHID_SWIFT, encoding="utf-8")
        r = run(["swiftc", "-O", "-o", str(binary), str(src)])
    return binary if r.returncode == 0 else None


def verify_user(reason):
    """Ask the OS to confirm the human is present. True only on a clear yes."""
    if OS_NAME == "macos":
        binary = _touchid_binary()
        if not binary:
            return False
        return run([str(binary), reason]).returncode == 0

    if OS_NAME == "windows":
        env = dict(os.environ, JV_REASON=reason)
        return run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", HELLO_PS],
            env=env,
        ).returncode == 0

    if shutil.which("fprintd-verify"):
        return run(["fprintd-verify"]).returncode == 0
    return False


# ------------------------------------------------------------------ bitwarden

def bw(*args, session=None, **kw):
    cmd = ["bw", *args]
    if session:
        cmd += ["--session", session]
    return run(cmd, **kw)


def require_bw():
    if not shutil.which("bw"):
        raise VaultError(
            "Bitwarden CLI not found.\n"
            "  macOS   brew install bitwarden-cli\n"
            "  Windows winget install Bitwarden.CLI\n"
            "  Linux   npm install -g @bitwarden/cli   (or snap install bw)"
        )


def token_is_live(token):
    if not token:
        return False
    r = bw("status", session=token)
    return r.returncode == 0 and '"status":"unlocked"' in r.stdout


def ensure_session(ks):
    """Return a live Bitwarden session token, unlocking first if needed."""
    require_bw()
    token = ks.get(ACC_SESSION)
    if token_is_live(token):
        return token

    master = ks.get(ACC_MASTER)
    if master and biometrics_available():
        if not verify_user("unlock the MemoryCore vault"):
            audit("DENY", "-", "biometrics")
            raise VaultError("biometric check refused")
        env = dict(os.environ, BW_PASSWORD=master)
        r = run(["bw", "unlock", "--passwordenv", "BW_PASSWORD", "--raw"], env=env)
        token = r.stdout.strip()
        if not token_is_live(token):
            raise VaultError(
                "the stored master password no longer works. "
                "Run: vault setup-biometrics"
            )
        ks.set(ACC_SESSION, token)
        audit("UNLOCK", "-", "biometrics")
        return token

    if not sys.stdin.isatty():
        raise VaultError(
            "unlocking needs a real terminal. Open a terminal and run: vault unlock"
        )
    token = run(["bw", "unlock", "--raw"], capture_output=True, text=True).stdout.strip()
    if not token_is_live(token):
        raise VaultError("unlock failed, vault is still locked")
    ks.set(ACC_SESSION, token)
    audit("UNLOCK", "-", "password")
    return token


# ------------------------------------------------------------------ allowlist

def load_allowlist():
    if not ALLOWLIST.exists():
        return {}
    try:
        return json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise VaultError(f"allowlist.json is not valid JSON: {exc}")


def is_allowed(secret, program):
    """Deny by default. A secret with no entry never leaves the vault."""
    if secret.startswith("_"):
        return False
    programs = load_allowlist().get(secret)
    return isinstance(programs, list) and program in programs


# ------------------------------------------------------------------ commands

def cmd_status(_args):
    ks = keystore()
    token = ks.get(ACC_SESSION)
    live = token_is_live(token)
    print(f"Platform        : {OS_NAME}")
    print(f"Key storage     : {ks.label}")
    print(f"Bitwarden CLI   : {'found' if shutil.which('bw') else 'MISSING'}")
    print(f"Biometrics      : {'available' if biometrics_available() else 'not available'}")
    print(f"Biometric setup : {'done' if ks.get(ACC_MASTER) else 'not set up'}")
    print(f"Vault           : {'ready' if live else 'locked'}")


def cmd_unlock(_args):
    ensure_session(keystore())
    print("Vault unlocked. Token stored in the OS key storage.")


def cmd_lock(_args):
    ks = keystore()
    ks.delete(ACC_SESSION)
    if shutil.which("bw"):
        bw("lock")
    print("Vault locked.")


def cmd_setup_biometrics(_args):
    require_bw()
    if not biometrics_available():
        raise VaultError(
            {
                "macos": "Touch ID needs Xcode Command Line Tools: xcode-select --install",
                "windows": "Windows Hello is not set up for this account.",
            }.get(OS_NAME, "No fingerprint reader found. Install fprintd and enroll a finger.")
        )
    if not sys.stdin.isatty():
        raise VaultError("this needs a real terminal")
    if not verify_user("confirm it is you before storing the master password"):
        raise VaultError("biometric check refused")

    master = getpass("Bitwarden master password (hidden): ")
    if not master:
        raise VaultError("empty")
    env = dict(os.environ, BW_PASSWORD=master)
    r = run(["bw", "unlock", "--passwordenv", "BW_PASSWORD", "--raw"], env=env)
    if not token_is_live(r.stdout.strip()):
        raise VaultError("wrong master password, nothing was stored")

    keystore().set(ACC_MASTER, master)
    audit("SETUP", "-", "biometrics")
    print("Done. From now on your fingerprint opens the vault.")


def cmd_forget_biometrics(_args):
    keystore().delete(ACC_MASTER)
    audit("FORGET", "-", "biometrics")
    print("Master password removed. Back to typing it manually.")


def index_path():
    """Where the name index lives. Inside MemoryCore when one is present."""
    override = os.environ.get("JARVIS_VAULT_INDEX")
    if override:
        return Path(override)
    for core in (Path(os.environ.get("JARVIS_CORE", "")), Path.home() / "JARVIS-Core"):
        if core.name and (core / "memory").is_dir():
            return core / "memory" / "vault-index.md"
    return HOME / "vault-index.md"


def refresh_index(session):
    """Write the list of secret names to MemoryCore. Names only, never values.

    This is what lets the agent answer "do I have a Trello key saved?" without
    opening the vault at all.
    """
    items = folder_items(session)
    rules = load_allowlist()

    rows = []
    for item in sorted(items, key=lambda i: i["name"]):
        name = item["name"][len(ITEM_PREFIX):]
        added = (item.get("creationDate") or "")[:10] or "unknown"
        allowed = rules.get(name)
        permitted = ", ".join(allowed) if isinstance(allowed, list) else "not set"
        rows.append(f"| `{name}` | {added} | {permitted} |")

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    body = [
        "# Vault Index",
        "*Names of the secrets held in the vault. Values live in Bitwarden and never appear here.*",
        "",
        f"Last synced: {stamp}",
        f"Count: {len(rows)}",
        "",
        "| Secret | Added | Programs allowed |",
        "|--------|-------|------------------|",
    ]
    body += rows or ["| _(empty)_ | | |"]
    body += [
        "",
        "## How to use these",
        "",
        "```bash",
        "vault run --secret NAME -- <command>",
        "```",
        "",
        "The value is handed to the child process as an environment variable. "
        "Nothing here can reveal it, and neither can the agent.",
        "",
        "A secret showing `not set` under permitted programs cannot be used yet. "
        "Add it to the allowlist first.",
        "",
        "*Regenerated automatically on every add, capture and remove. "
        "Rebuild by hand with `vault index`.*",
        "",
    ]

    path = index_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(body), encoding="utf-8")


def cmd_index(_args):
    session = ensure_session(keystore())
    refresh_index(session)
    print(f"Index written to {index_path()}")


def _unique_name(name, session):
    taken = {i["name"] for i in folder_items(session)}
    final, n = name, 2
    while ITEM_PREFIX + final in taken:
        final, n = f"{name}_{n}", n + 1
    return final


def ensure_folder(session):
    """Find the vault's Bitwarden folder, creating it the first time.

    Without this every secret lands in No Folder, mixed in with everything else
    the user keeps. A folder makes the vault's contents obvious in the Bitwarden
    apps, which matters on the day someone has to clean up or hand over.
    """
    result = bw("list", "folders", session=session)
    if result.returncode == 0:
        for folder in json.loads(result.stdout or "[]"):
            if folder.get("name") == FOLDER_NAME:
                return folder["id"]

    encoded = bw("encode", input=json.dumps({"name": FOLDER_NAME})).stdout.strip()
    created = bw("create", "folder", session=session, input=encoded)
    if created.returncode != 0:
        return None
    bw("sync", session=session)
    return json.loads(created.stdout)["id"]


def folder_items(session):
    """Every secret the vault owns, and nothing else.

    Scoped by folder id, not by name. This is the line that keeps the vault
    away from the rest of your Bitwarden account: your bank login lives in the
    same vault, and no command here can reach it.
    """
    folder_id = ensure_folder(session)
    if not folder_id:
        return []
    result = bw("list", "items", "--folderid", folder_id, session=session)
    if result.returncode != 0:
        return []
    return [i for i in json.loads(result.stdout or "[]") if i["name"].startswith(ITEM_PREFIX)]


def find_item(name, session):
    for item in folder_items(session):
        if item["name"] == ITEM_PREFIX + name:
            return item
    return None


def cmd_organize(_args):
    """Move secrets created before folder support into the vault folder."""
    session = ensure_session(keystore())
    folder_id = ensure_folder(session)
    if not folder_id:
        raise VaultError("could not create the Bitwarden folder")

    # Sengaja carian global: inilah satu-satunya arahan yang memang perlu
    # menjenguk ke luar folder, untuk mengutip item lama yang tersasar.
    result = bw("list", "items", "--search", ITEM_PREFIX, session=session)
    items = [i for i in json.loads(result.stdout or "[]")
             if i["name"].startswith(ITEM_PREFIX) and i.get("folderId") != folder_id]
    if not items:
        print(f"Everything is already in '{FOLDER_NAME}'.")
        return

    for item in items:
        item["folderId"] = folder_id
        encoded = bw("encode", input=json.dumps(item)).stdout.strip()
        if bw("edit", "item", item["id"], session=session, input=encoded).returncode == 0:
            print(f"  moved {item['name'][len(ITEM_PREFIX):]}")
    bw("sync", session=session)
    print(f"Done. {len(items)} secret(s) now live in '{FOLDER_NAME}'.")


def _store(name, value, session):
    payload = json.dumps({
        "type": 1,
        "name": ITEM_PREFIX + name,
        "folderId": ensure_folder(session),
        "notes": "Managed by jarvis_vault",
        "login": {"username": "jarvis", "password": value},
    })
    encoded = bw("encode", input=payload).stdout.strip()
    r = bw("create", "item", session=session, input=encoded)
    if r.returncode != 0:
        raise VaultError(f"could not save: {r.stderr.strip()}")
    bw("sync", session=session)


def cmd_add(args):
    if not args:
        raise VaultError("usage: vault add NAME")
    if not sys.stdin.isatty():
        raise VaultError(f"this needs a real terminal. Run: vault add {args[0]}")
    ks = keystore()
    session = ensure_session(ks)
    value = getpass(f"Value for {args[0]} (hidden): ")
    if not value:
        raise VaultError("empty value")
    name = _unique_name(args[0], session)
    _store(name, value, session)
    audit("ADD", name, "-")
    refresh_index(session)
    print(f"Stored: {name}")
    print(f"Not usable yet. Add an allowlist entry in {ALLOWLIST}")


def cmd_capture(args):
    """Automation path. The value arrives on stdin, never in argv."""
    if not args:
        raise VaultError("usage: echo VALUE | vault capture NAME")
    value = sys.stdin.read().strip()
    if not value:
        raise VaultError("empty value")
    session = ensure_session(keystore())
    name = _unique_name(args[0], session)
    _store(name, value, session)
    audit("CAPTURE", name, "hook")
    refresh_index(session)
    sys.stdout.write(name)


def cmd_list(_args):
    session = ensure_session(keystore())
    for item in folder_items(session):
        print(item["name"][len(ITEM_PREFIX):])


def cmd_remove(args):
    if not args:
        raise VaultError("usage: vault remove NAME")
    session = ensure_session(keystore())
    item = find_item(args[0], session)
    if not item:
        raise VaultError(f"secret '{args[0]}' is not in the vault")
    if bw("delete", "item", item["id"], session=session).returncode != 0:
        raise VaultError("delete failed")
    bw("sync", session=session)
    audit("REMOVE", args[0], "-")
    refresh_index(session)
    print(f"Removed: {args[0]}")


def cmd_rules(_args):
    rules = load_allowlist()
    if not rules:
        print(f"No allowlist yet. Create {ALLOWLIST}")
        return
    for key, programs in rules.items():
        if not key.startswith("_"):
            print(f"{key:28} -> {', '.join(programs)}")


def cmd_run(args):
    names, command = None, []
    while args:
        head = args.pop(0)
        if head == "--secret":
            names = args.pop(0) if args else None
        elif head == "--":
            command = args
            break
        else:
            raise VaultError(f"unexpected argument: {head}")
    if not names or not command:
        raise VaultError("usage: vault run --secret NAME[,NAME] -- <command>")

    program = Path(command[0]).stem if OS_NAME == "windows" else Path(command[0]).name
    session = ensure_session(keystore())

    env = dict(os.environ)
    for name in names.split(","):
        if not is_allowed(name, program):
            audit("DENY", name, program)
            raise VaultError(
                f"'{program}' is not allowed to use '{name}'. "
                f"Add it to {ALLOWLIST} if that is intended."
            )
        item = find_item(name, session)
        value = (item or {}).get("login", {}).get("password")
        if not value:
            audit("MISSING", name, program)
            raise VaultError(f"secret '{name}' is not in the vault")
        env[name] = value
        audit("ALLOW", name, program)

    try:
        sys.exit(subprocess.run(command, env=env).returncode)
    except FileNotFoundError:
        raise VaultError(f"command not found: {command[0]}")


USAGE = """jarvis_vault - secret broker for MemoryCore

  status                             show platform, key storage and vault state
  unlock                             unlock the vault
  lock                               lock it again and drop the token
  setup-biometrics                   unlock with fingerprint or face from now on
  forget-biometrics                  undo the above
  add NAME                           store a secret (hidden input)
  list                               names only, never values
  remove NAME                        delete a secret
  rules                              show the allowlist
  index                              rewrite the name index in MemoryCore
  organize                           move older secrets into the Bitwarden folder
  run --secret A[,B] -- <command>    run a command with secrets as env vars

No command prints a secret value. Secrets reach approved child processes only.
"""

COMMANDS = {
    "status": cmd_status,
    "unlock": cmd_unlock,
    "lock": cmd_lock,
    "setup-biometrics": cmd_setup_biometrics,
    "forget-biometrics": cmd_forget_biometrics,
    "add": cmd_add,
    "capture": cmd_capture,
    "list": cmd_list,
    "remove": cmd_remove,
    "rules": cmd_rules,
    "index": cmd_index,
    "organize": cmd_organize,
    "run": cmd_run,
}


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] not in COMMANDS:
        print(USAGE)
        sys.exit(1)
    try:
        COMMANDS[argv[0]](argv[1:])
    except VaultError as exc:
        print(f"vault: {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
