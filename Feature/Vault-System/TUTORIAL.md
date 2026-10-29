# Vault System, start to finish

*For anyone who has never used Bitwarden or a terminal password manager. No prior knowledge assumed. About 20 minutes.*

## What you are building, in one picture

Right now your API keys probably live in a `.env` file, or in a note, or you paste them into chat when the AI needs one.

After this, they live in one encrypted place, and the AI can *use* them without ever *seeing* them.

The closest everyday comparison is a hotel key card. The front desk never tells you the master combination for the electronic lock. They hand you a card that opens your door for three nights. You get in, you never learn the secret, and when you check out the card is dead.

That is exactly what happens here. The AI gets the door opened for one command. It never learns the key.

## What each piece does

Four things are involved. You only ever interact with the last one.

**Bitwarden** is a password manager. Think of it as a safe deposit box that syncs between your devices. It is free, it has been independently audited, and it is where your actual keys will live.

**The Bitwarden CLI** is Bitwarden without the pretty window. It is how a script talks to your safe deposit box. You install it once and mostly forget it exists.

**Your operating system's key storage** is the built-in secure spot every OS already has. macOS calls it Keychain, Windows calls it DPAPI, Linux calls it the keyring. It holds the ticket that keeps your vault open, so you are not typing your master password all day.

**`vault`** is the command you actually use. Everything else sits underneath it.

---

## Step 1: Get a Bitwarden account

Skip if you already have one.

1. Go to [bitwarden.com](https://bitwarden.com) and create a free account.
2. Choose a master password you can remember but nobody can guess. A short sentence works well, something like `PurpleTeapotOnFriday7`.
3. **Write it down on paper and put it somewhere safe.** Bitwarden cannot reset it for you. That is the point of the design, and it is also the one way to lose everything.
4. Turn on two-factor authentication in the settings. Any authenticator app will do.

The free tier covers everything here. There is nothing to pay for.

## Step 2: Install the Bitwarden CLI

Pick your platform.

**macOS**

```bash
brew install bitwarden-cli
```

No Homebrew? Install it first from [brew.sh](https://brew.sh), then run the line above.

**Windows**

Open PowerShell and run:

```powershell
winget install Bitwarden.CLI
```

**Linux**

```bash
npm install -g @bitwarden/cli
```

Or `snap install bw` if you prefer snaps.

Check it worked:

```bash
bw --version
```

A version number means you are fine. "Command not found" means the install did not finish, or your terminal needs to be closed and reopened so it picks up the new command.

## Step 3: Install the Vault System

From your MemoryCore folder:

```bash
python3 Feature/Vault-System/bin/install.py
```

This creates a settings folder, registers two safety hooks with Claude Code, and adds the `vault` command. It backs up your Claude settings first and leaves anything already there alone.

Confirm:

```bash
vault status
```

You want to see something like this:

```
Platform        : macos
Key storage     : macOS Keychain
Bitwarden CLI   : found
Biometrics      : available
Vault           : locked
```

If "Key storage" says `plain file`, your OS keystore was not reachable. On Linux that usually means one missing package: install `libsecret-tools` and run `vault status` again. Everything still works either way, it is just a weaker place to keep the ticket.

## Step 4: Log in to Bitwarden

```bash
bw login
```

It asks for your email, your master password, and your two-factor code.

When it finishes, it prints a long string starting with `BW_SESSION=`. **Do not copy that string anywhere.** It is a live key to your vault. Leave it in the terminal and move on. If you paste it into a chat by accident, run `bw lock` straight away and it becomes worthless.

## Step 5: Turn on fingerprint unlock

Optional, but it is the difference between this being pleasant and being annoying.

```bash
vault setup-biometrics
```

Fingerprint first, then your master password one last time, then it is stored in your OS keystore so your fingerprint can open the vault from then on.

The trade is worth understanding before you run it. Your master password ends up saved on this machine. That is the same arrangement the Bitwarden desktop app makes when you turn on biometric unlock. Anyone at your unlocked computer who can use your fingerprint can open the vault. Undo it any time with `vault forget-biometrics`.

## Step 6: Store your first key

```bash
vault add OPENAI_API_KEY
```

It asks for the value. **Nothing appears as you type.** That is deliberate, not a frozen terminal. Paste or type the key and press Enter.

Naming: use the same name the program expects as an environment variable. `OPENAI_API_KEY`, `STRIPE_SECRET_KEY`, `TRELLO_API_TOKEN`. Capital letters and underscores. Getting this right now saves confusion later.

Check it landed:

```bash
vault list
```

You will see the name. You will never see the value, from this command or any other.

## Step 7: Say who is allowed to use it

A stored secret is not usable yet. You have to say which programs may receive it.

Open `~/.jarvis-vault/allowlist.json` in any text editor. On Windows that is `C:\Users\<you>\.jarvis-vault\allowlist.json`.

```json
{
  "OPENAI_API_KEY": ["python3", "node", "curl"]
}
```

Left side is the secret name. Right side is the list of programs allowed to receive it. Anything not listed is refused.

Why bother, when you are the only person here? Because you are not the only one typing commands any more. The AI is too. This list is how you decide in advance what it can reach, at a moment when you are thinking clearly, rather than in the middle of debugging at midnight.

Never add `echo`, `cat`, `env`, `printenv`, `bash` or `sh`. The first four exist to print things, and printing is how a key ends up in a chat log forever. The last two hand your secret to any command at all, which makes the list meaningless.

Check your work:

```bash
vault rules
```

## Step 8: Use it

```bash
vault run --secret OPENAI_API_KEY -- python3 my_script.py
```

Read it as: run this command, and while it runs, give it this secret.

Inside `my_script.py` the key is a normal environment variable:

```python
import os
key = os.environ["OPENAI_API_KEY"]
```

The value exists for exactly as long as the script runs. It never touches your screen, your shell history, or the AI's transcript.

Two or more at once:

```bash
vault run --secret TRELLO_API_KEY,TRELLO_API_TOKEN -- python3 sync.py
```

## Step 9: Let the AI do it

Restart Claude Code so the hooks load, then just ask for what you want.

```
You:   run the sync script, it needs the Trello keys
Agent: $ vault run --secret TRELLO_API_KEY,TRELLO_API_TOKEN -- python3 sync.py
       done, 24 cards updated
```

The AI wrote a command naming the secrets. It did not see them, and it did not need to.

If you ever paste a key into chat by mistake, the catch hook takes it out of the message, stores it, and erases the message before the model receives it. You get told the name it was saved under.

That is a safety net, not a habit. A key that reaches the hook has already gone through your keyboard and your local logs, so treat it as exposed and replace it.

---

## Where everything lives

| What | Where |
|------|-------|
| Your secrets | Bitwarden, in a folder named **JARVIS Vault** |
| The allowlist | `~/.jarvis-vault/allowlist.json` |
| The activity log | `~/.jarvis-vault/audit.log` |
| The name list the AI reads | `memory/vault-index.md` in MemoryCore |

Open the Bitwarden app any time and look in the **JARVIS Vault** folder. Everything the AI can reach is in there, and nothing outside it can be touched by these commands. Your bank login sits in the same account and stays completely out of reach.

## When something goes wrong

**"Vault is locked" and no fingerprint prompt appears**
Run `vault unlock` in a real terminal window. Some environments, including the `!` shortcut inside Claude Code, cannot show a password prompt.

**"'python3' is not allowed to use 'OPENAI_API_KEY'"**
Working as designed. Add `python3` to that secret's list in `allowlist.json`.

**"secret 'X' is not in the vault"**
Check `vault list` for the exact spelling. Names are case sensitive.

**The AI refuses to read a `.env` file**
Also working as designed. That is the guard hook. Ask it to use `vault run` instead.

**A long message got blocked for no obvious reason**
The catch hook treats long base64 strings as possible session tokens. If it keeps catching something harmless, tell the AI and it can loosen that one pattern.

**You forgot your Bitwarden master password**
Nobody can recover it, including Bitwarden. This is why step 1 says to write it on paper.

## Commands worth remembering

```bash
vault status      # is everything set up
vault list        # what do I have
vault rules       # who may use what
vault index       # rebuild the list the AI reads
vault lock        # close the vault now
```

Five commands. Everything else is occasional.

## The honest limits

A tool like this is only useful if you know exactly where it stops.

If you allow `python3`, an AI can write a Python script that prints the secret. The allowlist is a guard rail, not a wall. It reliably stops the accidental paste, the wrong command, the reflex `cat .env`. It does not stop deliberate effort.

The catch hook fires after your keystroke, not before. Anything it catches has already touched your machine.

Biometric unlock means your master password sits in the OS keystore.

The real boundary is your operating system and your locked screen. Everything here is a layer on top of that. Worth having, in the same way a seatbelt is worth having in a car with good brakes, and worth understanding for the same reason.
