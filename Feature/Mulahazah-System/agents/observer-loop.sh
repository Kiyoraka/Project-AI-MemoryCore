#!/usr/bin/env bash
# observer-loop.sh — Mulahazah background observer loop
# Periodically analyzes observation logs and generates instincts via Haiku.
# Started by start-observer.sh. Should not be invoked directly.

set -euo pipefail

MULAHAZAH_DIR="${HOME}/.claude/mulahazah"
CONFIG_FILE="${MULAHAZAH_DIR}/config.json"
PROJECTS_DIR="${MULAHAZAH_DIR}/projects"
INSTINCTS_DIR="${MULAHAZAH_DIR}/instincts"
OBSERVER_PROMPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/observer.md"
LOG_FILE="${MULAHAZAH_DIR}/observer.log"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
log() {
  local level="$1"; shift
  printf '[%s] [%s] %s\n' "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" "$level" "$*" >> "$LOG_FILE"
}

# ---------------------------------------------------------------------------
# Read config values (with defaults)
# ---------------------------------------------------------------------------
read_config() {
  local key="$1"
  local default="$2"
  if [[ -f "$CONFIG_FILE" ]]; then
    local val
    val="$(jq -r "${key} // empty" "$CONFIG_FILE" 2>/dev/null || true)"
    if [[ -n "$val" && "$val" != "null" ]]; then
      printf '%s' "$val"
      return
    fi
  fi
  printf '%s' "$default"
}

# ---------------------------------------------------------------------------
# Signal handling
# ---------------------------------------------------------------------------
FORCE_RUN=false
SHUTDOWN=false

handle_sigterm() {
  log INFO "Received SIGTERM — shutting down gracefully"
  SHUTDOWN=true
}

handle_sigusr1() {
  log INFO "Received SIGUSR1 — forcing immediate analysis run"
  FORCE_RUN=true
}

trap handle_sigterm SIGTERM
trap handle_sigusr1 SIGUSR1

# ---------------------------------------------------------------------------
# Analyze a single project directory
# ---------------------------------------------------------------------------
analyze_project() {
  local project_dir="$1"
  local obs_file="${project_dir}/observations.jsonl"
  local project_json="${project_dir}/project.json"

  [[ -f "$obs_file" ]] || return 0

  local obs_count
  obs_count="$(wc -l < "$obs_file" 2>/dev/null || echo 0)"

  local min_obs
  min_obs="$(read_config '.observer.min_observations_to_analyze' '20')"

  if (( obs_count < min_obs )); then
    log DEBUG "Skipping ${project_dir} — only ${obs_count} observations (min: ${min_obs})"
    return 0
  fi

  local project_id project_name
  project_id="$(basename "$project_dir")"
  project_name="$(jq -r '.name // "unknown"' "$project_json" 2>/dev/null || echo "unknown")"

  log INFO "Analyzing project '${project_name}' (${project_id}) — ${obs_count} observations"

  # Build the prompt payload for claude
  local prompt
  prompt="$(cat <<PROMPT
You are the Mulahazah observer agent. Analyze the following observation data and existing instincts.

## Project
ID: ${project_id}
Name: ${project_name}

## Observations (last 500 lines of observations.jsonl)
$(tail -500 "$obs_file" 2>/dev/null || true)

## Existing Instincts
$(ls "${INSTINCTS_DIR}/${project_id}/"*.yaml 2>/dev/null | xargs -I{} cat {} 2>/dev/null || echo "(none)")

## Global Instincts
$(ls "${INSTINCTS_DIR}/global/"*.yaml 2>/dev/null | xargs -I{} cat {} 2>/dev/null || echo "(none)")

Follow the instructions in your system prompt. Output only YAML instinct blocks.
PROMPT
)"

  # Run claude with observer.md as the system prompt
  local output
  output="$(printf '%s' "$prompt" | \
    claude --model haiku --print --system-prompt "$OBSERVER_PROMPT" 2>>"$LOG_FILE" || true)"

  if [[ -z "$output" ]]; then
    log WARN "No output from observer for project '${project_name}'"
    return 0
  fi

  # Write instincts to disk
  write_instincts "$output" "$project_id"
}

# ---------------------------------------------------------------------------
# Analyze global observations
# ---------------------------------------------------------------------------
analyze_global() {
  local global_dir="${PROJECTS_DIR}/global"
  local obs_file="${global_dir}/observations.jsonl"

  [[ -f "$obs_file" ]] || return 0

  local obs_count
  obs_count="$(wc -l < "$obs_file" 2>/dev/null || echo 0)"

  local min_obs
  min_obs="$(read_config '.observer.min_observations_to_analyze' '20')"

  if (( obs_count < min_obs )); then
    log DEBUG "Skipping global observations — only ${obs_count} lines (min: ${min_obs})"
    return 0
  fi

  log INFO "Analyzing global observations — ${obs_count} lines"

  local prompt
  prompt="$(cat <<PROMPT
You are the Mulahazah observer agent. Analyze the following global observation data.

## Global Observations (last 500 lines)
$(tail -500 "$obs_file" 2>/dev/null || true)

## Existing Global Instincts
$(ls "${INSTINCTS_DIR}/global/"*.yaml 2>/dev/null | xargs -I{} cat {} 2>/dev/null || echo "(none)")

Follow the instructions in your system prompt. Output only YAML instinct blocks with scope: global.
PROMPT
)"

  local output
  output="$(printf '%s' "$prompt" | \
    claude --model haiku --print --system-prompt "$OBSERVER_PROMPT" 2>>"$LOG_FILE" || true)"

  if [[ -z "$output" ]]; then
    log WARN "No output from observer for global observations"
    return 0
  fi

  write_instincts "$output" "global"
}

# ---------------------------------------------------------------------------
# Parse and write instinct YAML blocks to disk
# ---------------------------------------------------------------------------
write_instincts() {
  local yaml_output="$1"
  local project_id="$2"

  # Split on --- separators and process each block
  local instinct_dir="${INSTINCTS_DIR}/${project_id}"
  mkdir -p "$instinct_dir"

  # Write raw output to a temp file, then split by ---
  local tmpfile
  tmpfile="$(mktemp)"
  printf '%s' "$yaml_output" > "$tmpfile"

  # Use awk to split YAML documents on '---' separator
  awk 'BEGIN{n=0; block=""} /^---$/{if(block!=""){print block > "/tmp/mulahazah_instinct_"n".yaml"; n++; block=""}} !/^---$/{block=block"\n"$0} END{if(block!=""){print block > "/tmp/mulahazah_instinct_"n".yaml"}}' "$tmpfile"

  local written=0
  for instinct_file in /tmp/mulahazah_instinct_*.yaml; do
    [[ -f "$instinct_file" ]] || continue

    # Extract the instinct id
    local instinct_id
    instinct_id="$(grep -m1 '^id:' "$instinct_file" | sed 's/^id: *//' | tr -d '"' | tr -d "'" | xargs 2>/dev/null || true)"

    if [[ -z "$instinct_id" ]]; then
      log WARN "Skipping instinct block with no id"
      rm -f "$instinct_file"
      continue
    fi

    local dest="${instinct_dir}/${instinct_id}.yaml"
    mv "$instinct_file" "$dest"
    log INFO "Wrote instinct '${instinct_id}' to ${dest}"
    (( written++ )) || true
  done

  # Clean up any leftover temp files
  rm -f /tmp/mulahazah_instinct_*.yaml "$tmpfile"

  log INFO "Wrote ${written} instincts for project '${project_id}'"
}

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
main() {
  log INFO "Mulahazah observer loop started (PID $$)"

  # Validate dependencies
  command -v jq &>/dev/null || { log ERROR "jq not found — observer cannot run"; exit 1; }
  command -v claude &>/dev/null || { log ERROR "claude CLI not found — observer cannot run"; exit 1; }
  [[ -f "$OBSERVER_PROMPT" ]] || { log ERROR "observer.md not found at ${OBSERVER_PROMPT}"; exit 1; }

  # Ensure instincts directory exists
  mkdir -p "${INSTINCTS_DIR}/global"

  while true; do
    # Check if observer is enabled
    local enabled
    enabled="$(read_config '.observer.enabled' 'true')"
    if [[ "$enabled" != "true" ]]; then
      log INFO "Observer is disabled in config — sleeping"
      sleep 60
      [[ "$SHUTDOWN" == "true" ]] && break
      continue
    fi

    if [[ "$FORCE_RUN" == "true" || "$SHUTDOWN" == "false" ]]; then
      FORCE_RUN=false
      log INFO "Starting analysis run"

      # Analyze each project directory
      if [[ -d "$PROJECTS_DIR" ]]; then
        for project_dir in "${PROJECTS_DIR}"/*/; do
          [[ -d "$project_dir" ]] || continue
          [[ "$(basename "$project_dir")" == "global" ]] && continue
          analyze_project "$project_dir" || log WARN "Analysis failed for ${project_dir}"
          [[ "$SHUTDOWN" == "true" ]] && break
        done
      fi

      # Analyze global observations
      analyze_global || log WARN "Global analysis failed"

      log INFO "Analysis run complete"
    fi

    [[ "$SHUTDOWN" == "true" ]] && break

    # Sleep for the configured interval
    local interval_minutes
    interval_minutes="$(read_config '.observer.run_interval_minutes' '5')"
    local interval_seconds=$(( interval_minutes * 60 ))

    log DEBUG "Sleeping for ${interval_minutes} minutes"

    # Sleep in 1-second chunks to remain responsive to signals
    local elapsed=0
    while (( elapsed < interval_seconds )); do
      sleep 1
      (( elapsed++ )) || true
      [[ "$SHUTDOWN" == "true" ]] && break
      [[ "$FORCE_RUN" == "true" ]] && break
    done
  done

  log INFO "Mulahazah observer loop exiting"
}

main "$@"
