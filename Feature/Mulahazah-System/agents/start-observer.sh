#!/usr/bin/env bash
# start-observer.sh — Start the Mulahazah background observer
# Checks for an existing instance, cleans up stale PIDs, and launches observer-loop.sh.

set -euo pipefail

MULAHAZAH_DIR="${HOME}/.claude/mulahazah"
PID_FILE="${MULAHAZAH_DIR}/observer.pid"
LOG_FILE="${MULAHAZAH_DIR}/observer.log"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOOP_SCRIPT="${SCRIPT_DIR}/observer-loop.sh"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
print_status() {
  local pid="$1"
  echo "Mulahazah observer is running (PID ${pid})"
  echo ""
  echo "  Force immediate analysis:  kill -USR1 ${pid}"
  echo "  Stop observer:             kill ${pid}"
  echo "  View logs:                 tail -f ${LOG_FILE}"
  echo "  PID file:                  ${PID_FILE}"
}

# ---------------------------------------------------------------------------
# Validate dependencies
# ---------------------------------------------------------------------------
if ! command -v jq &>/dev/null; then
  echo "Error: jq is required but not installed." >&2
  exit 1
fi

if ! command -v claude &>/dev/null; then
  echo "Error: claude CLI is required but not installed." >&2
  exit 1
fi

if [[ ! -f "$LOOP_SCRIPT" ]]; then
  echo "Error: observer-loop.sh not found at ${LOOP_SCRIPT}" >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Check for existing running instance
# ---------------------------------------------------------------------------
if [[ -f "$PID_FILE" ]]; then
  EXISTING_PID="$(cat "$PID_FILE" 2>/dev/null || true)"

  if [[ -n "$EXISTING_PID" ]] && kill -0 "$EXISTING_PID" 2>/dev/null; then
    # Process is alive
    echo "Mulahazah observer is already running."
    echo ""
    print_status "$EXISTING_PID"
    exit 0
  else
    # Stale PID file — process is gone
    echo "Cleaning up stale PID file (PID ${EXISTING_PID:-unknown} is no longer running)"
    rm -f "$PID_FILE"
  fi
fi

# ---------------------------------------------------------------------------
# Ensure Mulahazah directory structure exists
# ---------------------------------------------------------------------------
mkdir -p "${MULAHAZAH_DIR}/projects"
mkdir -p "${MULAHAZAH_DIR}/instincts/global"

# ---------------------------------------------------------------------------
# Initialize config.json if it doesn't exist
# ---------------------------------------------------------------------------
CONFIG_FILE="${MULAHAZAH_DIR}/config.json"
if [[ ! -f "$CONFIG_FILE" ]]; then
  # Check if a repo-level config exists next to this script's parent
  REPO_CONFIG="$(dirname "$SCRIPT_DIR")/config.json"
  if [[ -f "$REPO_CONFIG" ]]; then
    cp "$REPO_CONFIG" "$CONFIG_FILE"
    echo "Initialized config from ${REPO_CONFIG}"
  else
    cat > "$CONFIG_FILE" <<'EOF'
{
  "version": "2.0",
  "observer": {
    "enabled": true,
    "run_interval_minutes": 5,
    "min_observations_to_analyze": 20,
    "model": "haiku"
  }
}
EOF
    echo "Created default config at ${CONFIG_FILE}"
  fi
fi

# ---------------------------------------------------------------------------
# Launch observer-loop.sh in background with nohup
# ---------------------------------------------------------------------------
nohup bash "$LOOP_SCRIPT" >> "$LOG_FILE" 2>&1 &
OBSERVER_PID=$!

# Write PID file
printf '%d\n' "$OBSERVER_PID" > "$PID_FILE"

# Brief pause to confirm the process started
sleep 1
if ! kill -0 "$OBSERVER_PID" 2>/dev/null; then
  echo "Error: observer-loop.sh failed to start. Check logs:" >&2
  echo "  ${LOG_FILE}" >&2
  rm -f "$PID_FILE"
  exit 1
fi

echo "Mulahazah observer started."
echo ""
print_status "$OBSERVER_PID"
