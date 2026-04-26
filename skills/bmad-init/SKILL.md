---
name: "bmad-init"
description: "BMAD Method Framework for Agent Zero. Initialize BMAD workspace, access bmad-master orchestrator, and get context-aware help. Use when user says: initialize bmad, bmad init, setup bmad, start bmad, bmad help, bmad master, bmad-master, what can bmad do, bmad status."
version: "1.0.0"
author: "BMAD"
tags: ["bmad", "init", "bootstrap", "orchestrator", "help"]
trigger_patterns:
  - /bmad
  - /bmad-init
  - /bmad-help
  - /bmad-status
  - initialize bmad
  - bmad init
  - init bmad
  - setup bmad
  - start bmad
  - bmad help
  - bmad-help
  - bmad master
  - bmad-master
  - what can bmad do
  - bmad status
  - activate bmad
---

# BMAD Method Framework — Init, Help, and Orchestration

## Section 1 — Bootstrap: Initialize BMAD Workspace

When the user triggers "initialize BMAD", "bmad init", "setup bmad", "start bmad", or "activate bmad", execute the standalone bootstrap script.

**Steps:**
1. Determine the active project path from Agent Zero context (current working directory or project path).
2. Locate the bootstrap script relative to this skill at `scripts/bmad-init.sh`.
3. Execute the script using `code_execution_tool` with runtime `terminal`:

```
bash <SKILL_DIR>/scripts/bmad-init.sh <PROJECT_PATH>
```

Where:
- `<SKILL_DIR>` is the directory containing this SKILL.md (e.g., the skill's root folder as resolved by `skills_tool:load`).
- `<PROJECT_PATH>` is the active project path (e.g., `/a0/usr/projects/<project_name>`).

**Example execution:**
```bash
bash <SKILL_DIR>/scripts/bmad-init.sh <PROJECT_PATH>
```

4. Report success with the output directories and instruction files created.

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
