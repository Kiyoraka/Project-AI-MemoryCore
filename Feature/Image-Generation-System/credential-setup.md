# Credential Setup — OpenAI API Key
*How to give the Image Generation System a key, safely*

The render scripts need an OpenAI API key to call the gpt-image endpoint. They look for it in this
order:

1. The `OPENAI_API_KEY` environment variable
2. A `.env` file — the explicit path you pass (`-EnvFile` / `--env-file`), then `.env` in the
   current directory, then `.env` next to the script
3. If none is found, the script stops with a clear error

You only need **one** of these.

---

## Option A — `.env` file (recommended)

1. Get an API key from <https://platform.openai.com/api-keys>.
2. Copy the example file:
   ```
   cp .env.example .env
   ```
3. Open `.env` and replace the placeholder with your real key:
   ```
   OPENAI_API_KEY=sk-your-real-key-here
   ```
4. **Add `.env` to your `.gitignore`** (critical — see below).

Place `.env` either in the folder you run renders from, next to the render script, or pass its path
explicitly with `-EnvFile` (PowerShell) / `--env-file` (bash).

---

## Option B — Environment variable

**PowerShell:**
```powershell
$env:OPENAI_API_KEY = "sk-your-real-key-here"   # current session
# Persist across sessions:
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-your-real-key-here", "User")
```

**Bash:**
```bash
export OPENAI_API_KEY="sk-your-real-key-here"
# Persist by adding that line to ~/.bashrc or ~/.zshrc
```

---

## Key-safety checklist

A leaked API key can cost you real money. These practices keep it safe:

- [ ] **Gitignore the secret** — add `.env` to `.gitignore` so it can never be committed. Only
      `.env.example` (with the placeholder) belongs in version control.
- [ ] **Never `git add -A` blindly** — stage files by name, or confirm `git status` first, so a
      stray `.env` doesn't slip in.
- [ ] **The scripts never echo the key** — and they strip any `sk-...` pattern out of error messages
      before printing, so a failed render won't leak it to your terminal or logs.
- [ ] **The key is never returned** in the scripts' structured output — only the saved path, cost,
      and timing.
- [ ] **Rotate if exposed** — if a key ever lands somewhere public, revoke it immediately at
      <https://platform.openai.com/api-keys> and issue a new one.

---

## Verifying it works

Run a small render after setup:

```powershell
& Invoke-ImageGen.ps1 -Prompt "a sunset over mountains" -OutFile ".\test.png" -Quality "low"
```
```bash
invoke-image-gen.sh --prompt "a sunset over mountains" --outfile ./test.png --quality low
```

If the key is missing or still the placeholder, the script tells you exactly which sources it tried.
On success it writes the PNG and prints the saved path + estimated cost.
