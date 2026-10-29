# 🔐 Vault System

*Your AI agent can use your API keys without ever seeing them.*

## The problem

MemoryCore is markdown. That is its strength, and it is exactly why credentials have nowhere to live.

So they end up in the two places everyone already knows are wrong. Pasted into chat, where they land in the transcript and stay there. Or sitting in a `.env` file that the agent reads out loud the first time you ask it to debug a config issue.

Both leaks are quiet. Nothing breaks, nothing warns you, and the key is simply out. Rotating it later does not pull it back out of a log.

The instinct is to hide the file better. That does not hold, because the agent runs as you. Every file you can read, it can read. A vault that lives on the same disk under the same user is not a vault, it is a folder with a serious name.

## The idea

Split *knowing* a secret from *using* one.

The agent never needs to read your API key. It only needs the key to be present when a command runs. That is the same trick as `sudo`. You do not read the root password, you borrow its authority for one command and it is gone.

Everything below follows from that one line.

## Before and after

**Before**

```
You:   here is my key sk-proj-hT8vQ... put it in the script
Agent: done, I wrote it to config.py
```

The key is now in the transcript, in the provider's logs, in the local session file, and hardcoded in a file that is one `git add .` away from being public. Four copies, none of them tracked.

**After**

```
You:   $ vault add OPENAI_API_KEY          (typed in your terminal, hidden input)
You:   use the OpenAI key and run the script
Agent: $ vault run --secret OPENAI_API_KEY -- python3 script.py
       done, 40 rows processed
```

One copy, in Bitwarden. The agent wrote a command that names the secret and never holds it. If you paste a key into chat by accident, the catch hook takes it out of the message and erases the message before the model ever receives it.

Same work, same number of steps. The value stopped travelling.

## How it fits together

Three layers, each doing one job.

| Layer | Holds | Job |
|-------|-------|-----|
| Bitwarden | the secrets | sync across machines, recovery when a laptop dies |
| OS key storage | the unlock token, and optionally the master password | keep the key material off the filesystem |
| Allowlist | nothing | decide which program may receive which secret |

The OS layer is chosen at runtime, so the same file works everywhere.

| Platform | Key storage | Biometric unlock |
|----------|-------------|------------------|
| macOS | Keychain | Touch ID via LocalAuthentication |
| Windows | DPAPI, bound to your user account | Windows Hello via UserConsentVerifier |
| Linux | libsecret, meaning GNOME Keyring or KWallet | fprintd |
| Anything else | file with owner-only permissions, and the CLI says so | none |

## Install

New to Bitwarden or to terminal password managers? Start with **[TUTORIAL.md](TUTORIAL.md)**, which walks through the whole thing from a blank slate in about 20 minutes. The short version:

```bash
python3 Feature/Vault-System/bin/install.py
```

Then:

```bash
bw login
vault setup-biometrics     # optional, skips the master password from then on
vault add OPENAI_API_KEY
```

Restart Claude Code so the hooks load.

## Daily use

```bash
vault status                                       # platform, storage backend, vault state
vault list                                         # names only, never values
vault rules                                        # who may use what
vault run --secret OPENAI_API_KEY -- python3 x.py
vault run --secret A,B -- node server.js           # more than one is fine
vault index                                        # rebuild the name index in MemoryCore
vault remove NAME
vault lock
```

A locked vault does not interrupt anything. The next `run` asks for your fingerprint and carries on.

## The allowlist

`~/.jarvis-vault/allowlist.json`. The key is the secret name, the value is the list of programs allowed to receive it.

```json
{
  "OPENAI_API_KEY": ["python3", "node", "curl"]
}
```

Deny by default. A secret with no entry is refused and the attempt is logged.

`echo`, `cat`, `env` and `printenv` are deliberately absent from the examples. Their whole job is to print, and printing is how a secret gets into a transcript.

## Hooks

Two, both optional, both registered by the installer.

**Guard** runs before every Bash call and denies the obvious ways around the broker: reading Bitwarden directly, reading the OS keystore directly, piping `run` into something that only prints, and `cat`-ing a `.env` file.

**Catch** runs when you submit a message. If the message contains something shaped like a credential, the value goes into the vault and the message is erased. The model receives nothing. You get back the name it was stored under.

Catch only fires on vendor-specific patterns such as `sk-ant-`, `ghp_`, `AKIA` and `xoxb-`. Anything ambiguous is allowed through, because blocking real work is worse than missing one catch.

## Where the secrets sit in Bitwarden

Everything the vault creates goes into a folder named **JARVIS Vault**, created on first use. Item names carry a `jarvis/` prefix, so `OPENAI_API_KEY` appears as `jarvis/OPENAI_API_KEY`.

Every read is scoped to that folder by id, not by name. The rest of your Bitwarden account is unreachable from these commands. Your bank login lives in the same vault and no command here can touch it. The one exception is `vault organize`, whose entire job is to look outside the folder and collect strays.

Two reasons for the folder. Your own logins stay unmixed with the agent's, and on the day someone has to audit, clean up or hand the account over, the full contents are one click away in any Bitwarden app.

Rename it with the `JARVIS_VAULT_FOLDER` environment variable. Secrets stored before folder support existed can be moved in with `vault organize`.

## The name index

Every add, capture and removal rewrites `memory/vault-index.md` inside MemoryCore. It lists names, dates and allowlist entries, never values.

```markdown
| Secret | Added | Programs allowed |
|--------|-------|------------------|
| `TRELLO_API_KEY` | 2026-08-11 | python3, curl |
```

This is the part that makes the agent useful rather than merely safe. It can answer "do I already have a Trello key saved?" from memory, without opening the vault, without a biometric prompt, and without ever touching a value. Rebuild it by hand with `vault index`.

## Audit log

`~/.jarvis-vault/audit.log`, one line per event: time, decision, secret name, program.

```
2026-08-11 15:08:46	ALLOW	OPENAI_API_KEY	python3
2026-08-11 15:08:47	DENY	OPENAI_API_KEY	node
2026-08-11 15:09:04	UNLOCK	-	biometrics
```

## What this does not do

Worth saying plainly, because a security tool that oversells itself is worse than none.

If you allow `python3`, the agent can write a Python script that prints the secret. The allowlist is a rail, not a wall. It stops the accidental leak, the wrong command, the reflex paste. It does not stop intent.

The catch hook fires after your keystroke, not before. A credential that reaches it has already touched your keyboard buffer and your local logs. Treat anything it catches as exposed and rotate it.

Biometric unlock means your master password is stored in the OS keystore. That is the same trade the Bitwarden desktop app makes when you turn on biometrics. Anyone sitting at your unlocked machine with your finger available can open the vault. Undo it with `vault forget-biometrics`.

The real boundary is the operating system. Everything here is defence in depth on top of that, and it is worth having for the same reason seatbelts are worth having in a car with good brakes.

## Requirements

- Python 3.8 or newer, standard library only
- [Bitwarden CLI](https://bitwarden.com/help/cli/) (`brew install bitwarden-cli`, `winget install Bitwarden.CLI`, or `npm install -g @bitwarden/cli`)
- A Bitwarden account, free tier included

---

**Version**: 1.0
**Platforms**: macOS, Windows, Linux
**Agent**: built and tested against Claude Code. The CLI itself is agent-agnostic, only the two hook files are Claude-specific.
