---
name: bmad-module-builder-workflow
description: 'Plan, create, edit, and validate complete BMAD modules with agents, workflows, and infrastructure.'
trigger_patterns:
  - /bmad-module-builder-workflow
  - /build-module
  - /CM
  - build module
  - create module
  - edit module
  - validate module
  - /EM
  - /VM
  - /IM
  - ideate module
  - /PB
  - module brief
---

# Module Builder Routing

Detect user intent and route to the appropriate workflow:

| Intent | Route To |
|--------|----------|
| **Ideate / Brainstorm / Plan** — "I have an idea for a module" | `workflow-ideate-module.md` |
| **Create Brief** — structured module brief through creative discovery | `workflow-create-module-brief.md` |
| **Create / Scaffold** — package built skills as a module | `workflow-create-module.md` |
| **Edit** — modify existing module | `workflow-edit-module.md` |
| **Validate** — check module completeness | `workflow-validate-module.md` |
| **Unclear** | Present options above |
