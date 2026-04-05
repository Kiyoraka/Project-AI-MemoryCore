#!/usr/bin/env bash
# analyze.sh — Read observations.jsonl, detect patterns, append rules to rules.md
# This is the actual analysis pipeline. Runs via /continuous-improve or observer-loop.
# Uses claude CLI with Haiku for cost-efficient analysis.

set -euo pipefail

MULAHAZAH_DIR="${HOME}/.claude/mulahazah"
RULES_FILE="${MULAHAZAH_DIR}/rules.md"
GLOBAL_OBS="${MULAHAZAH_DIR}/observations.jsonl"

# Detect project
PROJECT_DIR=""
PROJECT_OBS=""
if REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); then
  PROJECT_HASH=$(printf '%s' "$REPO_ROOT" | sha256sum | cut -c1-12)
  PROJECT_DIR="${MULAHAZAH_DIR}/projects/${PROJECT_HASH}"
  PROJECT_OBS="${PROJECT_DIR}/observations.jsonl"
fi

# Find observations file
OBS_FILE=""
if [ -n "$PROJECT_OBS" ] && [ -f "$PROJECT_OBS" ]; then
  OBS_FILE="$PROJECT_OBS"
elif [ -f "$GLOBAL_OBS" ]; then
  OBS_FILE="$GLOBAL_OBS"
fi

if [ -z "$OBS_FILE" ] || [ ! -s "$OBS_FILE" ]; then
  echo "No observations found. Use Claude Code with hooks installed to generate observations."
  exit 0
fi

OBS_COUNT=$(wc -l < "$OBS_FILE")
echo "Found $OBS_COUNT observations in $OBS_FILE"

if [ "$OBS_COUNT" -lt 5 ]; then
  echo "Need at least 5 observations for meaningful analysis. Keep using Claude Code."
  exit 0
fi

# Read existing rules to avoid duplicates
EXISTING_RULES=""
if [ -f "$RULES_FILE" ]; then
  EXISTING_RULES=$(cat "$RULES_FILE")
fi

# Take last 200 observations (keep prompt size manageable)
RECENT_OBS=$(tail -200 "$OBS_FILE")

# Build analysis prompt
ANALYSIS_PROMPT="Analyze these Claude Code session observations and extract behavioral patterns.

OBSERVATIONS (JSONL — each line is a tool call):
${RECENT_OBS}

EXISTING RULES (already learned — do NOT duplicate these):
${EXISTING_RULES}

YOUR TASK:
1. Look for REPEATED PATTERNS — same tool sequence used 3+ times
2. Look for ERROR-THEN-FIX sequences — tool fails, next tools fix it
3. Look for TOOL PREFERENCES — one tool consistently chosen over alternatives
4. Look for WORKFLOW PATTERNS — consistent ordering of operations

OUTPUT FORMAT — output ONLY new rules, one per line, as markdown list items:
- Rule: [specific actionable rule based on observed pattern]

Rules must be:
- Specific and actionable (not vague advice)
- Based on actual observed patterns (cite the tools/sequence you saw)
- Different from existing rules listed above
- Useful for future sessions

If no new patterns are found, output exactly: NO_NEW_PATTERNS

Output ONLY the rules list or NO_NEW_PATTERNS. No explanation, no preamble."

# Run analysis with Haiku
echo "Analyzing patterns with Haiku..."
RESULT=$(echo "$ANALYSIS_PROMPT" | claude --model haiku --print -p - 2>/dev/null) || {
  echo "Analysis failed — claude CLI error. Try running manually."
  exit 1
}

if [ "$RESULT" = "NO_NEW_PATTERNS" ] || [ -z "$RESULT" ]; then
  echo "No new patterns detected yet. Keep using Claude Code — patterns emerge over time."
  exit 0
fi

# Append new rules to rules.md
echo "" >> "$RULES_FILE" 2>/dev/null || true
mkdir -p "$(dirname "$RULES_FILE")"
{
  if [ ! -f "$RULES_FILE" ]; then
    echo "# Learned Rules"
    echo ""
    echo "Rules extracted from session observations by Mulahazah."
    echo "Remove any rule that causes problems. Keep what helps."
    echo ""
    echo "---"
    echo ""
  fi
  echo "## $(date +%Y-%m-%d) analysis"
  echo ""
  echo "$RESULT"
  echo ""
} >> "$RULES_FILE"

# Count new rules
NEW_COUNT=$(echo "$RESULT" | grep -c "^- " || true)
echo ""
echo "Added $NEW_COUNT new rules to $RULES_FILE"
echo ""
echo "$RESULT"
