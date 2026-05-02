#!/bin/bash
set -euo pipefail
PROJECT_PATH="${1:-$(pwd)}"
A0PROJ="$PROJECT_PATH/.a0proj"
PROJECT_NAME=$(basename "$PROJECT_PATH")

echo "Initializing BMAD at: $A0PROJ"

# Create output and knowledge directories (idempotent)
mkdir -p "$A0PROJ/_bmad-output/planning-artifacts/research"
mkdir -p "$A0PROJ/_bmad-output/implementation-artifacts"
mkdir -p "$A0PROJ/_bmad-output/test-artifacts"
mkdir -p "$A0PROJ/knowledge/main"
mkdir -p "$A0PROJ/knowledge/fragments"
mkdir -p "$A0PROJ/knowledge/solutions"
mkdir -p "$A0PROJ/instructions"
mkdir -p "$A0PROJ/agents"
mkdir -p "$A0PROJ/skills"
mkdir -p "$A0PROJ/_bmad/custom/"

# Create project-context.md stub (no-clobber — preserves user content on re-init)
touch "$A0PROJ/knowledge/main/project-context.md"

# Seed BMAD framework knowledge into project (idempotent — no-clobber preserves user edits)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SEED_DIR="$SCRIPT_DIR/../seed-knowledge"
if [ -d "$SEED_DIR" ]; then
  if command -v rsync &>/dev/null; then
    rsync -a --ignore-existing "$SEED_DIR/." "$A0PROJ/knowledge/main/"
  else
    cp -Rn "$SEED_DIR/." "$A0PROJ/knowledge/main/"
  fi
  echo "BMAD seed knowledge copied to project knowledge base."
else
  echo "Warning: seed-knowledge directory not found at $SEED_DIR — skipping knowledge seed." >&2
fi

# Write 01-bmad-config.md (only if not already present — immutable config)
if [ ! -f "$A0PROJ/instructions/01-bmad-config.md" ]; then
  INIT_DATE=$(date '+%Y-%m-%d')
  cat > "$A0PROJ/instructions/01-bmad-config.md" << CONFIG
## BMAD Configuration

**Project:** $PROJECT_NAME
**Initialized:** $INIT_DATE

### Path Conventions
| Alias | Resolved Path |
|---|---|
| \`{project-root}\` | \`$A0PROJ/\` |
| \`{planning_artifacts}\` | \`$A0PROJ/_bmad-output/planning-artifacts/\` |
| \`{implementation_artifacts}\` | \`$A0PROJ/_bmad-output/implementation-artifacts/\` |
| \`{product_knowledge}\` | \`$A0PROJ/knowledge/\` |
| \`{output_folder}\` | \`$A0PROJ/_bmad-output/\` |

CONFIG
  echo "Config file written."
else
  echo "Config file already present, preserving existing config."
fi

# Write bmad-user-prefs.promptinclude.md (no-clobber — preserves user edits on re-init)
if [ ! -f "$A0PROJ/instructions/bmad-user-prefs.promptinclude.md" ]; then
  cat > "$A0PROJ/instructions/bmad-user-prefs.promptinclude.md" << 'PREFS'
## User Settings
- **User Name:** User
- **Communication Language:** English
- **User Skill Level:** intermediate
PREFS
  echo "User prefs file written."
else
  echo "User prefs file already present, preserving existing preferences."
fi

# Write 02-bmad-state.md (only if not already present)
if [ ! -f "$A0PROJ/instructions/02-bmad-state.md" ]; then
  cat > "$A0PROJ/instructions/02-bmad-state.md" << 'STATE'
## BMAD Active State
- Phase: ready
- Persona: BMad Master (Orchestrator)
- Active Artifact: none

You are the BMad Master. Greet the user, explain BMAD capabilities, and offer to load any module or workflow.

STATE
  echo "State file written."
else
  echo "State file already present, preserving existing state."
fi

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║      BMAD Method Framework — Initialized         ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "Workspace: $A0PROJ"
echo ""
echo "Directories:"
echo "  .a0proj/_bmad-output/             <- Artifacts"
echo "    planning-artifacts/research/"
echo "    implementation-artifacts/"
echo "    test-artifacts/"
echo "  .a0proj/knowledge/                <- Project knowledge base"
echo "    main/ | fragments/ | solutions/"
echo "  .a0proj/instructions/             <- Auto-injected state"
echo "  .a0proj/agents/                   <- BMB agent output (A0 discovers)"
echo "  .a0proj/skills/                   <- BMB skill output (A0 discovers)"
echo ""
echo "Note: BMAD framework workflows are bundled in skills — no project copy needed."
echo ""
echo "Get started: Type 'create product brief' to start with Mary (Analyst)"
echo "             Or type 'bmad-help' for the full module and workflow reference."
