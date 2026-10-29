# Install Vault System

*Integration protocol for credential storage in MemoryCore*

## Activation

When the user says `Load vault-system`, install the Vault System into the active MemoryCore.

## Steps

1. **Check the prerequisites**

   ```bash
   python3 --version    # 3.8 or newer
   bw --version         # Bitwarden CLI
   ```

   If the Bitwarden CLI is missing, install it for their platform:

   | Platform | Command |
   |----------|---------|
   | macOS | `brew install bitwarden-cli` |
   | Windows | `winget install Bitwarden.CLI` |
   | Linux | `npm install -g @bitwarden/cli` or `snap install bw` |

2. **Run the installer**

   ```bash
   python3 Feature/Vault-System/bin/install.py
   ```

   It creates `~/.jarvis-vault/`, seeds an allowlist, registers the two Claude Code hooks, and puts a `vault` launcher on PATH. It backs up `~/.claude/settings.json` first and keeps any hooks already there.

3. **Confirm the platform was detected correctly**

   ```bash
   vault status
   ```

   Check that "Key storage" names a real OS keystore. If it says `plain file`, the OS keystore was not reachable. On Linux that usually means libsecret is missing: install `libsecret-tools` and run it again.

4. **Log in to Bitwarden**

   ```bash
   bw login
   ```

   The user does this themselves. Do not offer to run it for them, and if they paste the resulting `BW_SESSION` into chat, tell them to run `bw lock` because that token is a live key to their vault.

5. **Offer biometric unlock**

   ```bash
   vault setup-biometrics
   ```

   Must be run in a real terminal. Explain the trade before they run it: the master password will be stored in the OS keystore so their fingerprint can open the vault, which is the same arrangement the Bitwarden desktop app uses.

6. **Add the first secret**

   ```bash
   vault add OPENAI_API_KEY
   ```

   In their terminal, not through the agent. Input is hidden there.

7. **Add the matching allowlist entry**

   Edit `~/.jarvis-vault/allowlist.json`. Suggest the narrowest set of programs that does the job.

8. **Restart the agent** so the hooks load, then verify with `vault status`.

## Post-install update

Add to the MemoryCore feature list in `master-memory.md`:

```markdown
- **Vault-System** - Credential broker (Bitwarden + OS keystore + per-secret allowlist)
```

## Verification

| Check | Command | Expected |
|-------|---------|----------|
| Platform detected | `vault status` | a real keystore name, not `plain file` |
| Secret stored | `vault list` | the name appears, no value |
| Allowlist works | `vault run --secret NAME -- python3 -c "print(1)"` | prints `1` |
| Denial works | `vault run --secret NAME -- node -e "1"` | refused, if `node` is not listed |
| Guard works | ask the agent to read a `.env` file | denied with a reason |

## Uninstall

```bash
vault lock
vault forget-biometrics
```

Then remove the two hook entries from `~/.claude/settings.json`, delete `~/.jarvis-vault/`, and delete the `vault` launcher. The secrets stay in Bitwarden, untouched.
