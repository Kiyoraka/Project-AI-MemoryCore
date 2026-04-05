#!/usr/bin/env bash
# observe.sh — Mulahazah PreToolUse/PostToolUse observation hook
# Captures every tool call as a JSONL line. Must complete in <50ms. Always exits 0.
# Usage: echo '<hook_json>' | observe.sh

# Always exit 0 — never block the Claude session
trap 'exit 0' EXIT ERR INT TERM

# Require jq — if unavailable, silently exit
command -v jq &>/dev/null || exit 0

MULAHAZAH_DIR="${HOME}/.claude/mulahazah"
PROJECTS_DIR="${MULAHAZAH_DIR}/projects"
GLOBAL_REGISTRY="${MULAHAZAH_DIR}/projects.json"

# ---------------------------------------------------------------------------
# Read stdin (hook payload) — single read for performance
# ---------------------------------------------------------------------------
INPUT="$(cat)"
[[ -z "$INPUT" ]] && exit 0

# ---------------------------------------------------------------------------
# Parse hook payload in one jq call
# ---------------------------------------------------------------------------
read -r TOOL_NAME SESSION_ID HAS_OUTPUT INPUT_JSON OUTPUT_JSON <<< "$(
  printf '%s' "$INPUT" | jq -r '
    (.tool_name // ""),
    (.session_id // ""),
    (if has("tool_output") then "yes" else "no" end),
    ((.tool_input // {} | tostring) | .[0:500]),
    ((.tool_output // {} | tostring) | .[0:200])
  ' | paste - - - - -
)"

# Determine event type
if [[ "$HAS_OUTPUT" == "yes" ]]; then
  EVENT="tool_complete"
else
  EVENT="tool_start"
fi

# ---------------------------------------------------------------------------
# Project detection (4 priority levels)
# ---------------------------------------------------------------------------
PROJECT_ROOT=""

# Priority 1: $CLAUDE_PROJECT_DIR env var
if [[ -n "${CLAUDE_PROJECT_DIR:-}" && -d "${CLAUDE_PROJECT_DIR}" ]]; then
  PROJECT_ROOT="${CLAUDE_PROJECT_DIR}"
fi

# Priority 2+3: git repo root (covers both remote-url and root-hash priorities)
if [[ -z "$PROJECT_ROOT" ]]; then
  PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
fi

# Priority 4: global fallback
if [[ -z "$PROJECT_ROOT" ]]; then
  PROJECT_ROOT="global"
fi

# ---------------------------------------------------------------------------
# Compute project hash and name (SHA-256 first 12 chars)
# ---------------------------------------------------------------------------
PROJECT_HASH="$(printf '%s' "$PROJECT_ROOT" | sha256sum | cut -c1-12)"
PROJECT_NAME="$(basename "${PROJECT_ROOT%.git}")"

# ---------------------------------------------------------------------------
# Directory setup
# ---------------------------------------------------------------------------
PROJECT_OBS_DIR="${PROJECTS_DIR}/${PROJECT_HASH}"
OBS_FILE="${PROJECT_OBS_DIR}/observations.jsonl"

# Create dirs only if needed (fast no-op if already exists)
[[ -d "$PROJECT_OBS_DIR" ]] || mkdir -p "${PROJECT_OBS_DIR}/observations.archive"

# ---------------------------------------------------------------------------
# Rotate observations.jsonl if it exceeds 10,000 lines
# ---------------------------------------------------------------------------
if [[ -f "$OBS_FILE" ]]; then
  LINE_COUNT="$(wc -l < "$OBS_FILE")"
  if (( LINE_COUNT >= 10000 )); then
    ARCHIVE_DATE="$(date -u +"%Y-%m-%d")"
    mv "$OBS_FILE" "${PROJECT_OBS_DIR}/observations.archive/${ARCHIVE_DATE}.jsonl"
  fi
fi

# ---------------------------------------------------------------------------
# Append JSONL observation line
# ---------------------------------------------------------------------------
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

printf '%s\n' "$(jq -cn \
  --arg ts "$TS" \
  --arg event "$EVENT" \
  --arg session "$SESSION_ID" \
  --arg tool "$TOOL_NAME" \
  --arg input_summary "$INPUT_JSON" \
  --arg output_summary "$OUTPUT_JSON" \
  --arg project_id "$PROJECT_HASH" \
  --arg project_name "$PROJECT_NAME" \
  '{ts:$ts,event:$event,session:$session,tool:$tool,input_summary:$input_summary,output_summary:$output_summary,project_id:$project_id,project_name:$project_name}')" \
  >> "$OBS_FILE"

# ---------------------------------------------------------------------------
# Write project.json and update registry (only if new — deferred to avoid
# adding latency to every invocation)
# ---------------------------------------------------------------------------
PROJECT_JSON="${PROJECT_OBS_DIR}/project.json"
if [[ ! -f "$PROJECT_JSON" ]]; then
  CREATED_AT="$TS"
  jq -n \
    --arg id "$PROJECT_HASH" \
    --arg name "$PROJECT_NAME" \
    --arg root "$PROJECT_ROOT" \
    --arg created_at "$CREATED_AT" \
    '{id:$id,name:$name,root:$root,created_at:$created_at}' \
    > "$PROJECT_JSON"

  # Update global projects.json registry
  mkdir -p "$MULAHAZAH_DIR"
  [[ -f "$GLOBAL_REGISTRY" ]] || printf '{}' > "$GLOBAL_REGISTRY"

  TMP_REGISTRY="$(mktemp)"
  jq --arg id "$PROJECT_HASH" \
     --arg name "$PROJECT_NAME" \
     --arg root "$PROJECT_ROOT" \
     --arg created_at "$CREATED_AT" \
     '.[$id] = {name:$name,root:$root,created_at:$created_at}' \
     "$GLOBAL_REGISTRY" > "$TMP_REGISTRY" && mv "$TMP_REGISTRY" "$GLOBAL_REGISTRY"
fi

exit 0
