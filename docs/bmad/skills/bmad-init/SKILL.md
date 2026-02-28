---
name: "bmad-init"
description: "BMAD Method Framework for Agent Zero. Initialize BMAD workspace, access bmad-master orchestrator, and get context-aware help. Use when user says: initialize bmad, bmad init, setup bmad, start bmad, bmad help, bmad master, bmad-master, what can bmad do, bmad status."
version: "1.0.0"
author: "BMAD"
tags: ["bmad", "init", "bootstrap", "orchestrator", "help"]
trigger_patterns:
  - "initialize bmad"
  - "bmad init"
  - "init bmad"
  - "setup bmad"
  - "start bmad"
  - "bmad help"
  - "bmad-help"
  - "bmad master"
  - "bmad-master"
  - "what can bmad do"
  - "bmad status"
  - "activate bmad"
---

# BMAD Method Framework — Init, Help, and Orchestration

## Section 1 — Bootstrap: Initialize BMAD Workspace

When the user triggers "initialize BMAD", "bmad init", "setup bmad", "start bmad", or "activate bmad", execute the bootstrap script below using `code_execution_tool` (bash).

**Steps:**
1. Determine the active project path from Agent Zero context (current working directory or project path).
2. Run the bootstrap script, passing the project path as `$1`.
3. Report success with the directory tree created and instructions written.

**Template Source Configuration:**
The bootstrap script uses `/a0/docs/bmad` as the default template source. To override, set `BMAD_TEMPLATE_SRC` using one of the following methods (highest priority first):
1. Set `BMAD_TEMPLATE_SRC` as a shell environment variable before running the script.
2. Add `BMAD_TEMPLATE_SRC=/your/custom/path` to `.a0proj/variables.env` in the project root.
3. Default: `/a0/docs/bmad` (used if neither of the above is set).

**Bootstrap Script:**

```bash
#!/bin/bash
set -e
PROJECT_PATH="${1:-$(pwd)}"
A0PROJ="$PROJECT_PATH/.a0proj"
PROJECT_NAME=$(basename "$PROJECT_PATH")

# Set template source: env var > .a0proj/variables.env > default
TEMPLATE_SRC="/a0/docs/bmad"
_BMAD_TEMPLATE_SRC_ENVVAL="${BMAD_TEMPLATE_SRC:-}"
if [ -f "$A0PROJ/variables.env" ]; then
  # shellcheck source=/dev/null
  . "$A0PROJ/variables.env"
fi
# External env var wins: if it was set before this script, restore it over any variables.env value
if [ -n "$_BMAD_TEMPLATE_SRC_ENVVAL" ]; then
  BMAD_TEMPLATE_SRC="$_BMAD_TEMPLATE_SRC_ENVVAL"
fi
TEMPLATE_SRC="${BMAD_TEMPLATE_SRC:-$TEMPLATE_SRC}"

# Validate template source exists
if [ ! -d "$TEMPLATE_SRC" ]; then
  echo "ERROR: BMAD template source not found: $TEMPLATE_SRC"
  echo "Set BMAD_TEMPLATE_SRC in $A0PROJ/variables.env or as an environment variable."
  exit 1
fi

echo "Initializing BMAD at: $A0PROJ"
echo "Template source: $TEMPLATE_SRC"

# Create output and knowledge directories (idempotent)
mkdir -p "$A0PROJ/_bmad-output/planning-artifacts/research"
mkdir -p "$A0PROJ/_bmad-output/implementation-artifacts"
mkdir -p "$A0PROJ/_bmad-output/test-artifacts"
mkdir -p "$A0PROJ/knowledge/main"
mkdir -p "$A0PROJ/knowledge/fragments"
mkdir -p "$A0PROJ/knowledge/solutions"
mkdir -p "$A0PROJ/instructions"
mkdir -p "$A0PROJ/skills"

# Copy BMAD framework (only if not already present)
if [ ! -d "$A0PROJ/_bmad" ]; then
  echo "Copying BMAD framework from $TEMPLATE_SRC ..."
  mkdir -p "$A0PROJ/_bmad"
  cp -r "$TEMPLATE_SRC/." "$A0PROJ/_bmad/"
  echo "Framework copied."
  BMAD_STATUS="copied"
else
  echo "Framework already present, skipping copy."
  BMAD_STATUS="already existed"
fi

# Copy skills (only if not already present)
if [ ! -d "$A0PROJ/skills/bmad-init" ]; then
  echo "Copying BMAD skills from $TEMPLATE_SRC/skills/ ..."
  cp -r "$TEMPLATE_SRC/skills/." "$A0PROJ/skills/"
  echo "Skills copied."
  SKILLS_STATUS="copied"
else
  echo "Skills already present, skipping copy."
  SKILLS_STATUS="already existed"
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
- **User Name:** Vanja
- **Communication Language:** English
- **User Skill Level:** intermediate
CONFIG
  echo "Config file written."
  CONFIG_STATUS="written"
else
  echo "Config file already present, preserving existing config."
  CONFIG_STATUS="already existed"
fi

# Write 02-bmad-state.md (only if not already present — preserve existing state)
if [ ! -f "$A0PROJ/instructions/02-bmad-state.md" ]; then
  cat > "$A0PROJ/instructions/02-bmad-state.md" << 'STATE'
## BMAD Active State
- Phase: ready
- Persona: BMad Master (Orchestrator)
- Active Artifact: none

You are the BMad Master. Greet the user, explain BMAD capabilities, and offer to load any module or workflow.
STATE
  echo "State file written."
  STATE_STATUS="written"
else
  echo "State file already present, preserving existing state."
  STATE_STATUS="already existed"
fi

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║      BMAD Method Framework — Initialized         ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "Workspace: $A0PROJ"
echo ""
echo "Directories:"
echo "  .a0proj/_bmad/                    <- BMAD framework ($BMAD_STATUS)"
echo "  .a0proj/_bmad-output/             <- Artifacts"
echo "    planning-artifacts/research/"
echo "    implementation-artifacts/"
echo "    test-artifacts/"
echo "  .a0proj/knowledge/                <- Project knowledge base"
echo "    main/ | fragments/ | solutions/"
echo "  .a0proj/instructions/             <- Auto-injected state"
echo "  .a0proj/skills/                   <- BMAD skills ($SKILLS_STATUS)"
echo ""
echo "State files:"
echo "  01-bmad-config.md  — Project configuration ($CONFIG_STATUS)"
echo "  02-bmad-state.md   — Active state: phase=ready, persona=BMad Master ($STATE_STATUS)"
echo ""
echo "Available BMAD Modules:"
echo "  [bmm] Development lifecycle  — \"create product brief\", \"create PRD\", \"dev story\", \"sprint planning\""
echo "  [bmb] BMAD Builder           — \"create agent\", \"create workflow\", \"create module\""
echo "  [cis] Creative Intelligence  — \"innovation strategy\", \"design thinking\", \"brainstorming\""
echo "  [tea] Testing Excellence     — \"test architecture\", \"ATDD\", \"automate tests\""
echo ""
echo "Get started: Type \"create product brief\" to start with Mary (Analyst)"
echo "             Or type \"bmad-help\" for the full module and workflow reference."
```

---

## Section 2 — bmad-help: Available Modules and Trigger Phrases

When the user asks for "bmad help", "bmad-help", or "what can bmad do":

1. Read `.a0proj/instructions/02-bmad-state.md` (if it exists) using `code_execution_tool` (bash cat). Extract the current **Phase** and **Persona** values.
2. Present the full module reference below.
3. Show the current state (phase and persona from `02-bmad-state.md`, or "not initialized" if the file does not exist).
4. Recommend the next step appropriate to the current phase:
   - Phase `ready` or not initialized → suggest "initialize BMAD" or "create product brief"
   - Phase `1-Analysis` → suggest "create PRD" or continue analysis
   - Phase `2-Planning` → suggest "create architecture" or "validate PRD"
   - Phase `3-Solutioning` → suggest "create epics and stories" or "check implementation readiness"
   - Phase `4-Implementation` → suggest "sprint planning", "dev story", or "code review"

**BMAD Available Modules:**

**[INIT] BMAD Init, Help, and Orchestration** — this skill
Trigger phrases: "initialize bmad", "bmad init", "setup bmad", "bmad help", "bmad-help", "bmad master", "bmad status", "what can bmad do"

**[BMM] Development Lifecycle**
Trigger phrases: "create product brief", "product brief", "product discovery", "brainstorm project", "domain research", "market research", "technical research", "create PRD", "product requirements", "edit PRD", "validate PRD", "create UX design", "UX specifications", "create architecture", "technical architecture", "solution design", "create epics and stories", "epics and stories", "check implementation readiness", "sprint planning", "sprint status", "create story", "next story", "dev story", "implement story", "code review", "generate e2e tests", "QA tests", "retrospective", "correct course", "document project", "project context", "quick spec", "quick dev"

**[BMB] BMAD Builder**
Trigger phrases: "create agent", "new agent", "edit agent", "validate agent", "create workflow", "new workflow", "edit workflow", "validate workflow", "rework workflow", "create module", "new module", "edit module", "validate module", "create module brief", "bmad builder"

**[CIS] Creative Intelligence Suite**
Trigger phrases: "innovation strategy", "disruption opportunities", "design thinking", "empathy driven design", "storytelling", "narrative", "problem solving", "structured problem solving", "brainstorming", "ideate", "creative session", "cis module"

**[TEA] Testing Excellence Accelerator**
Trigger phrases: "test architecture", "testing strategy", "ATDD", "acceptance test driven", "automate tests", "test automation", "CI integration", "test framework", "test design", "test cases", "trace tests", "traceability", "NFR assessment", "test review", "review tests", "teach me testing", "learn testing", "tea module"

---

## Section 3 — bmad-master: Orchestration Persona

When the user invokes "bmad master", "bmad-master", or "activate bmad master", take on the BMAD Master orchestrator persona and present the following menu:

```
BMAD Master — Agent Zero Edition

Available modules:
[BMM] Development lifecycle — analysis, planning, solutioning, implementation
[BMB] BMAD Builder — create and extend BMAD agents and workflows
[CIS] Creative Intelligence — innovation, design thinking, storytelling
[TEA] Testing Excellence — test architecture, ATDD, automation

Type a workflow name or describe what you want to do.
```

As BMAD Master:
- Route user requests to the correct module skill.
- Suggest the recommended next step based on the current BMAD state (read from `.a0proj/instructions/02-bmad-state.md` if available).
- If no project is initialized, suggest running "initialize BMAD" first.
- Maintain the orchestrator persona until the user explicitly requests a different persona or module.
