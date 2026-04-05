#!/usr/bin/env bash
# observer-loop.sh — Mulahazah background observer
# Periodically runs analyze.sh to extract rules from observations.
# Started by start-observer.sh. Should not be invoked directly.

set -euo pipefail

MULAHAZAH_DIR="${HOME}/.claude/mulahazah"
CONFIG_FILE="${MULAHAZAH_DIR}/config.json"
ANALYZE_SCRIPT="${MULAHAZAH_DIR}/bin/analyze.sh"
LOG_FILE="${MULAHAZAH_DIR}/observer.log"

log() {
  printf '[%s] %s\n' "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" "$*" >> "$LOG_FILE"
}

read_config() {
  local key="$1" default="$2"
  if [ -f "$CONFIG_FILE" ]; then
    local val
    val="$(jq -r "${key} // empty" "$CONFIG_FILE" 2>/dev/null || true)"
    [ -n "$val" ] && [ "$val" != "null" ] && printf '%s' "$val" && return
  fi
  printf '%s' "$default"
}

SHUTDOWN=false
FORCE_RUN=false
trap 'log "SIGTERM received"; SHUTDOWN=true' SIGTERM
trap 'log "SIGUSR1 received — forcing run"; FORCE_RUN=true' SIGUSR1

log "Observer loop started (PID $$)"

# Validate
command -v jq &>/dev/null || { log "ERROR: jq not found"; exit 1; }
command -v claude &>/dev/null || { log "ERROR: claude CLI not found"; exit 1; }
[ -f "$ANALYZE_SCRIPT" ] || { log "ERROR: analyze.sh not found at $ANALYZE_SCRIPT"; exit 1; }

while true; do
  [ "$SHUTDOWN" = "true" ] && break

  ENABLED="$(read_config '.observer.enabled' 'true')"
  if [ "$ENABLED" != "true" ]; then
    log "Observer disabled — sleeping 60s"
    sleep 60
    continue
  fi

  if [ "$FORCE_RUN" = "true" ] || [ "$SHUTDOWN" = "false" ]; then
    FORCE_RUN=false
    log "Running analysis..."
    bash "$ANALYZE_SCRIPT" >> "$LOG_FILE" 2>&1 || log "Analysis returned non-zero"
    log "Analysis complete"
  fi

  [ "$SHUTDOWN" = "true" ] && break

  INTERVAL="$(read_config '.observer.run_interval_minutes' '5')"
  log "Sleeping ${INTERVAL}m"

  # Sleep in 1s chunks for signal responsiveness
  ELAPSED=0
  while [ "$ELAPSED" -lt "$((INTERVAL * 60))" ]; do
    sleep 1
    ELAPSED=$((ELAPSED + 1))
    [ "$SHUTDOWN" = "true" ] && break
    [ "$FORCE_RUN" = "true" ] && break
  done
done

log "Observer loop exiting"
