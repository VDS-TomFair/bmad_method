#!/usr/bin/env bash
# promote.sh — Copy agents/skills from project scope to BMad plugin scope
#
# Usage:
#   promote.sh <type> <name> [project_root]
#
# Arguments:
#   type          "agent" or "workflow"
#   name          the agent or skill/workflow name
#   project_root  path to the project (default: current directory)
#
# Exit codes:
#   0  success
#   1  usage error
#   2  source not found
#   3  target already exists (requires --force to overwrite)

set -euo pipefail

# --- Parse arguments ---
if [[ $# -lt 2 ]]; then
    echo "Usage: promote.sh <type> <name> [project_root]"
    echo "  type: 'agent' or 'workflow'"
    echo "  name: the agent or skill/workflow directory name"
    echo "  project_root: path to the project (default: current directory)"
    exit 1
fi

TYPE="$1"
NAME="$2"
PROJECT_ROOT="${3:-$(pwd)}"
FORCE="${PROMOTE_FORCE:-false}"

# --- Validate type ---
case "$TYPE" in
    agent)
        SUBDIR="agents"
        ;;
    workflow)
        SUBDIR="skills"
        ;;
    *)
        echo "ERROR: Invalid type '$TYPE'. Must be 'agent' or 'workflow'."
        exit 1
        ;;
esac

# --- Construct paths ---
SOURCE="${PROJECT_ROOT}/.a0proj/${SUBDIR}/${NAME}"
TARGET="/a0/usr/plugins/bmad_method/${SUBDIR}/${NAME}"

# --- Validate source exists ---
if [[ ! -d "$SOURCE" ]]; then
    echo "ERROR: Source directory does not exist: $SOURCE"
    echo "  Make sure '$NAME' exists in project scope at .a0proj/${SUBDIR}/${NAME}/"
    exit 2
fi

# --- Check target ---
if [[ -d "$TARGET" || -f "$TARGET" ]]; then
    if [[ "$FORCE" != "true" ]]; then
        echo "WARNING: Target already exists: $TARGET"
        echo "  Set PROMOTE_FORCE=true to overwrite, or remove the existing target first."
        exit 3
    fi
    echo "WARNING: Overwriting existing target: $TARGET"
    rm -rf "$TARGET"
fi

# --- Ensure target parent directory exists ---
mkdir -p "$(dirname "$TARGET")"

# --- Copy ---
cp -R "$SOURCE" "$TARGET"

# --- Verify ---
if [[ -d "$TARGET" ]]; then
    echo "SUCCESS: Promoted $TYPE '$NAME'"
    echo "  Source: $SOURCE"
    echo "  Target: $TARGET"
    echo ""
    echo "The $TYPE is now available globally across all projects."
else
    echo "ERROR: Copy completed but target verification failed."
    exit 1
fi
