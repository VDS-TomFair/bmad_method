#!/bin/bash
set -e
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

# Seed BMAD framework knowledge into project (idempotent — no-clobber preserves user edits)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SEED_DIR="$SCRIPT_DIR/../seed-knowledge"
if [ -d "$SEED_DIR" ]; then
  cp -rn "$SEED_DIR/." "$A0PROJ/knowledge/main/"
  echo "BMAD seed knowledge copied to project knowledge base."
else
  echo "Warning: seed-knowledge directory not found at $SEED_DIR — skipping knowledge seed."
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
| \`{project-root}\` | \`/a0/usr/projects/$PROJECT_NAME/.a0proj/\` |
| \`{planning_artifacts}\` | \`/a0/usr/projects/$PROJECT_NAME/.a0proj/_bmad-output/planning-artifacts/\` |
| \`{implementation_artifacts}\` | \`/a0/usr/projects/$PROJECT_NAME/.a0proj/_bmad-output/implementation-artifacts/\` |
| \`{product_knowledge}\` | \`/a0/usr/projects/$PROJECT_NAME/.a0proj/knowledge/\` |
| \`{output_folder}\` | \`/a0/usr/projects/$PROJECT_NAME/.a0proj/_bmad-output/\` |

### User Settings
- **User Name:** User
- **Communication Language:** English
- **User Skill Level:** intermediate

### Marketing Context
- Brand Voice: [professional, casual, technical, playful]
- Primary ICP: [ideal customer profile summary]
- Key Differentiators: [what sets product apart]
- Positioning Statement: [one-line positioning]
- Distribution Channels: [organic, paid, social, email, partnerships]
- Pricing Model: [free, freemium, trial, usage-based, flat-rate]
- Marketing Stage: [pre-product, pre-launch, launch, growth, mature]
CONFIG
  echo "Config file written."
else
  echo "Config file already present, preserving existing config."
fi

# Write 02-bmad-state.md (only if not already present)
if [ ! -f "$A0PROJ/instructions/02-bmad-state.md" ]; then
  cat > "$A0PROJ/instructions/02-bmad-state.md" << 'STATE'
## BMAD Active State
- Phase: ready
- Persona: BMad Master (Orchestrator)
- Active Artifact: none

You are the BMad Master. Greet the user, explain BMAD capabilities, and offer to load any module or workflow.

### Marketing State
- Marketing Phase: [1-discovery, 2-strategy, 3-setup, 4-execution, 5-growth, 6-retention]
- Active Marketing Agent: [none]
- Completed Marketing Activities: []
- Product Marketing Context: [pending]
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
echo ""
echo "Note: BMAD framework workflows are bundled in skills — no project copy needed."
echo ""
echo "Get started: Type 'create product brief' to start with Mary (Analyst)"
echo "             Or type 'bmad-help' for the full module and workflow reference."
