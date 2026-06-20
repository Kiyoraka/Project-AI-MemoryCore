# Credential Setup — BytePlus ModelArk API Key
*How to give the Video Generation System a key, safely*

The render scripts need a BytePlus ModelArk API key (`ARK_API_KEY`) to call the Seedance endpoint.
They look for it in this order:

1. The `ARK_API_KEY` environment variable
2. A `.env` file — the explicit path you pass (`-EnvFile` / `--env-file`), then `.env` in the
   current directory, then `.env` next to the script
3. If none is found, the script stops with a clear error

You only need **one** of these.

---

## Getting a key

1. Sign in to the **BytePlus ModelArk console**.
2. Open **API Keys** and create a key.
3. Make sure your account has access to the Seedance video model
   (default: `dreamina-seedance-2-0-260128`).

---

## Option A — `.env` file (recommended)

1. Copy the example file:
   ```
   cp .env.example .env
   ```
2. Open `.env` and replace the placeholder with your real key:
   ```
   ARK_API_KEY=your-real-key-here
   ```
3. **Add `.env` to your `.gitignore`** (critical — see below).

Place `.env` either in the folder you run renders from, next to the render script, or pass its path
explicitly with `-EnvFile` (PowerShell) / `--env-file` (bash).

---

## Option B — Environment variable

**PowerShell:**
```powershell
$env:ARK_API_KEY = "your-real-key-here"   # current session
# Persist across sessions:
[Environment]::SetEnvironmentVariable("ARK_API_KEY", "your-real-key-here", "User")
```

**Bash:**
```bash
export ARK_API_KEY="your-real-key-here"
# Persist by adding that line to ~/.bashrc or ~/.zshrc
```

---

## Endpoint & model notes

- The default endpoint is the `ap-southeast` BytePlus region. If your account uses a different
  region, override it with `-ApiBase` (PowerShell) / `--api-base` (bash).
- The default model is `dreamina-seedance-2-0-260128`. Override with `-Model` / `--model` if you use
  a different Seedance model.

---

## Key-safety checklist

A leaked API key can cost you real money — and **video is expensive**. These practices keep it safe:

- [ ] **Gitignore the secret** — add `.env` to `.gitignore` so it can never be committed. Only
      `.env.example` (with the placeholder) belongs in version control.
- [ ] **Never `git add -A` blindly** — stage files by name, or confirm `git status` first, so a
      stray `.env` doesn't slip in.
- [ ] **The scripts never echo the key** — and they strip any `ark-...` / `sk-...` pattern out of
      error messages before printing, so a failed render won't leak it to your terminal or logs.
- [ ] **The key is never returned** in the scripts' structured output — only the saved path, cost,
      timing, and task id.
- [ ] **Rotate if exposed** — if a key ever lands somewhere public, revoke it immediately in the
      BytePlus ModelArk console and issue a new one.

---

## Verifying it works

First estimate the cost (no spend, no API call):

```powershell
& Invoke-VideoGen.ps1 -Prompt "a sunset over mountains" -OutFile ".\test.mp4" -Resolution "480p" -Duration 5 -WhatIfCost
```
```bash
invoke-video-gen.sh --prompt "a sunset over mountains" --outfile ./test.mp4 --resolution 480p --duration 5 --what-if-cost
```

Then run a real short clip once you're happy with the estimate (drop `-WhatIfCost` / `--what-if-cost`).
If the key is missing or still the placeholder, the script tells you exactly which sources it tried.
On success it writes the MP4 and prints the saved path + estimated cost.
