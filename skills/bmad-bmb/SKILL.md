---
name: "bmad-bmb"
description: "BMAD Builder Module — create and extend BMAD agents, workflows, and modules. Triggers: create agent, new agent, edit agent, validate agent, create workflow, new workflow, edit workflow, validate workflow, rework workflow, create module, new module, edit module, validate module, create module brief, bmad builder."
version: "1.0.0"
author: "BMAD"
tags: ["bmad", "bmb", "builder", "meta", "agents", "workflows"]
trigger_patterns:
  - "create agent"
  - "new agent"
  - "edit agent"
  - "validate agent"
  - "create workflow"
  - "new workflow"
  - "edit workflow"
  - "validate workflow"
  - "rework workflow"
  - "create module"
  - "new module"
  - "edit module"
  - "validate module"
  - "create module brief"
  - "bmad builder"
---

# BMAD Builder Module (BMB) — Create and Extend BMAD Agents, Workflows, and Modules

BMB is the meta-module for building and extending BMAD itself. Use it to author new BMAD agents, design and validate workflows, and create new BMAD modules.

All paths use `{project-root}` which resolves to `.a0proj/` as defined in `01-bmad-config.md`.

When any BMB workflow is triggered, read the full workflow file at the path shown and follow it exactly.

---

## Agent Workflows

### Create Agent
**Triggers:** "create agent", "new agent", "build agent", "author agent"
**Output artifact:** New agent definition file
**Workflow:** `{skill-dir}/workflows/agent/workflow-create-agent.md`

### Edit Agent
**Triggers:** "edit agent", "update agent", "modify agent", "revise agent"
**Output artifact:** Updated agent definition file
**Workflow:** `{skill-dir}/workflows/agent/workflow-edit-agent.md`

### Validate Agent
**Triggers:** "validate agent", "review agent", "check agent", "audit agent"
**Output artifact:** Validation report inline
**Workflow:** `{skill-dir}/workflows/agent/workflow-validate-agent.md`

---

## Workflow Workflows

### Create Workflow
**Triggers:** "create workflow", "new workflow", "build workflow", "author workflow"
**Output artifact:** New workflow file
**Workflow:** `{skill-dir}/workflows/workflow/workflow-create-workflow.md`

### Edit Workflow
**Triggers:** "edit workflow", "update workflow", "modify workflow", "revise workflow"
**Output artifact:** Updated workflow file
**Workflow:** `{skill-dir}/workflows/workflow/workflow-edit-workflow.md`

### Rework Workflow
**Triggers:** "rework workflow", "refactor workflow", "restructure workflow"
**Output artifact:** Reworked workflow file
**Workflow:** `{skill-dir}/workflows/workflow/workflow-rework-workflow.md`

### Validate Workflow
**Triggers:** "validate workflow", "review workflow", "check workflow", "audit workflow"
**Output artifact:** Validation report inline
**Workflow:** `{skill-dir}/workflows/workflow/workflow-validate-workflow.md`

### Validate Max Parallel Workflow
**Triggers:** "validate max parallel workflow", "parallel workflow validation", "concurrency audit"
**Output artifact:** Parallel validation report inline
**Workflow:** `{skill-dir}/workflows/workflow/workflow-validate-max-parallel-workflow.md`

---

## Module Workflows

### Create Module
**Triggers:** "create module", "new module", "build module", "author module"
**Output artifact:** New module directory and files
**Workflow:** `{skill-dir}/workflows/module/workflow-create-module.md`

### Edit Module
**Triggers:** "edit module", "update module", "modify module", "revise module"
**Output artifact:** Updated module files
**Workflow:** `{skill-dir}/workflows/module/workflow-edit-module.md`

### Validate Module
**Triggers:** "validate module", "review module", "check module", "audit module"
**Output artifact:** Module validation report inline
**Workflow:** `{skill-dir}/workflows/module/workflow-validate-module.md`

### Create Module Brief
**Triggers:** "create module brief", "module brief", "new module brief"
**Output artifact:** Module brief document
**Workflow:** `{skill-dir}/workflows/module/workflow-create-module-brief.md`

---

## Execution Instructions

When any BMB workflow is triggered:
1. Identify the workflow from the trigger phrase.
2. Read the full workflow file at the path shown above using `code_execution_tool` (bash cat).
3. Follow the workflow instructions exactly — do not summarize or skip steps.
4. Write output artifacts using `code_execution_tool` (bash write).
5. Update `{project-root}/instructions/02-bmad-state.md` to reflect the active BMB workflow.
