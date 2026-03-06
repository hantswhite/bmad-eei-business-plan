#!/usr/bin/env bash
# setup.sh — Configure EEI Business Plan extension for a consumer project
# Idempotent: safe to re-run. Generates config.yaml and symlinks slash commands.
set -euo pipefail

# ── 1. Locate paths ──────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EEI_ROOT="$SCRIPT_DIR"
COMMANDS_SRC="$EEI_ROOT/business-plan/commands"

# Walk up from EEI_ROOT to find PROJECT_ROOT (directory containing .git/ or .git file)
find_project_root() {
  local dir="$EEI_ROOT"
  while [[ "$dir" != "/" ]]; do
    if [[ -d "$dir/.git" || -f "$dir/.git" ]]; then
      echo "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  echo "ERROR: Could not find project root (.git) above $EEI_ROOT" >&2
  return 1
}

PROJECT_ROOT="$(find_project_root)"
COMMANDS_DEST="$PROJECT_ROOT/.claude/commands"
CONFIG_FILE="$EEI_ROOT/config.yaml"
CONFIG_TEMPLATE="$EEI_ROOT/config.template.yaml"

echo "EEI root:      $EEI_ROOT"
echo "Project root:  $PROJECT_ROOT"
echo ""

# ── 2. Generate config.yaml ──────────────────────────────────────────────────

created_config=false

if [[ -f "$CONFIG_FILE" ]]; then
  echo "config.yaml already exists — skipping generation."
else
  if [[ ! -f "$CONFIG_TEMPLATE" ]]; then
    echo "ERROR: config.template.yaml not found at $CONFIG_TEMPLATE" >&2
    exit 1
  fi

  # Accept values from CLI args or prompt interactively
  PROJECT_NAME="${1:-}"
  USER_NAME="${2:-}"
  SKILL_LEVEL="${3:-}"
  LANGUAGE="${4:-}"
  RESEARCH_ENFORCEMENT="${5:-}"

  if [[ -z "$PROJECT_NAME" ]]; then
    read -rp "Project name: " PROJECT_NAME
  fi
  if [[ -z "$USER_NAME" ]]; then
    read -rp "Your name: " USER_NAME
  fi
  if [[ -z "$SKILL_LEVEL" ]]; then
    read -rp "Skill level [beginner/intermediate/expert] (default: intermediate): " SKILL_LEVEL
    SKILL_LEVEL="${SKILL_LEVEL:-intermediate}"
  fi
  if [[ -z "$LANGUAGE" ]]; then
    read -rp "Language (default: English): " LANGUAGE
    LANGUAGE="${LANGUAGE:-English}"
  fi
  if [[ -z "$RESEARCH_ENFORCEMENT" ]]; then
    read -rp "Research enforcement [strict/standard/permissive] (default: standard): " RESEARCH_ENFORCEMENT
    RESEARCH_ENFORCEMENT="${RESEARCH_ENFORCEMENT:-standard}"
  fi

  # Generate config from template via sed substitution
  sed \
    -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
    -e "s/{{USER_NAME}}/$USER_NAME/g" \
    -e "s/{{USER_SKILL_LEVEL}}/$SKILL_LEVEL/g" \
    -e "s/{{COMMUNICATION_LANGUAGE}}/$LANGUAGE/g" \
    -e "s/{{DOCUMENT_OUTPUT_LANGUAGE}}/$LANGUAGE/g" \
    -e "s/{{RESEARCH_ENFORCEMENT}}/$RESEARCH_ENFORCEMENT/g" \
    "$CONFIG_TEMPLATE" > "$CONFIG_FILE"

  echo "Created config.yaml"
  created_config=true
fi

echo ""

# ── 3. Symlink slash commands ─────────────────────────────────────────────────

mkdir -p "$COMMANDS_DEST"

symlinked=0
skipped=0
warned=0

for cmd_file in "$COMMANDS_SRC"/bmad-eei-bp-*.md; do
  [[ -f "$cmd_file" ]] || continue

  filename="$(basename "$cmd_file")"
  link_path="$COMMANDS_DEST/$filename"

  # Compute relative symlink target from .claude/commands/ to the source file
  rel_target="$(realpath --relative-to="$COMMANDS_DEST" "$cmd_file")"

  if [[ -L "$link_path" ]]; then
    # Symlink exists — check if it points to the right place
    existing_target="$(readlink "$link_path")"
    if [[ "$existing_target" == "$rel_target" ]]; then
      skipped=$((skipped + 1))
      continue
    fi
    # Wrong target — remove and recreate
    rm "$link_path"
  elif [[ -e "$link_path" ]]; then
    # Regular file exists where symlink should go — warn, don't overwrite
    echo "WARNING: $link_path exists as a regular file — skipping (will not overwrite)"
    warned=$((warned + 1))
    continue
  fi

  ln -s "$rel_target" "$link_path"
  symlinked=$((symlinked + 1))
done

# ── 4. Summary ────────────────────────────────────────────────────────────────

echo ""
echo "=== Setup Summary ==="
if $created_config; then
  echo "  Config:    created config.yaml"
else
  echo "  Config:    already existed (skipped)"
fi
echo "  Symlinks:  $symlinked created, $skipped already correct, $warned warnings"
echo "=== Done ==="
