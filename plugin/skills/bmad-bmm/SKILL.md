---
name: "bmad-bmm"
description: "BMAD Method Module — complete software development lifecycle. Triggers: create product brief, product brief, product discovery, brainstorm project, domain research, market research, technical research, create PRD, product requirements, edit PRD, validate PRD, create UX design, UX specifications, create architecture, technical architecture, solution design, create epics and stories, epics and stories, check implementation readiness, sprint planning, sprint status, create story, next story, dev story, implement story, code review, QA tests, generate e2e tests, retrospective, correct course, document project, generate project context, quick spec, quick dev."
version: "1.0.0"
author: "BMAD"
tags: ["bmad", "bmm", "development", "lifecycle", "planning", "implementation"]
trigger_patterns:
  - "create product brief"
  - "product brief"
  - "product discovery"
  - "brainstorm project"
  - "domain research"
  - "market research"
  - "technical research"
  - "create prd"
  - "product requirements"
  - "edit prd"
  - "validate prd"
  - "create ux design"
  - "ux specifications"
  - "create architecture"
  - "technical architecture"
  - "solution design"
  - "create epics and stories"
  - "epics and stories"
  - "check implementation readiness"
  - "sprint planning"
  - "sprint status"
  - "create story"
  - "next story"
  - "dev story"
  - "implement story"
  - "code review"
  - "generate e2e tests"
  - "qa tests"
  - "retrospective"
  - "correct course"
  - "document project"
  - "project context"
  - "quick spec"
  - "quick dev"
---

# BMAD Method Module (BMM) — Development Lifecycle Workflows

BMM covers the complete software development lifecycle: analysis, planning, solutioning, and implementation. When a workflow is triggered, read the full workflow file at the path shown and follow it exactly.

All paths below use `{project-root}` which resolves to `.a0proj/` as defined in `01-bmad-config.md`.

---

## Phase 1 — Analysis

### Create Product Brief
**Triggers:** "create product brief", "product brief", "product discovery", "brainstorm project"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/product-brief-<project>-<date>.md`
**Workflow:** `{skill-dir}/workflows/1-analysis/create-product-brief/workflow.md`

### Technical Research
**Triggers:** "technical research", "research technology", "research stack"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/research/technical-<topic>-research-<date>.md`
**Workflow:** `{skill-dir}/workflows/1-analysis/research/workflow-technical-research.md`

### Domain Research
**Triggers:** "domain research", "research domain", "industry research"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/research/domain-<topic>-research-<date>.md`
**Workflow:** `{skill-dir}/workflows/1-analysis/research/workflow-domain-research.md`

### Market Research
**Triggers:** "market research", "research market", "competitive analysis"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/research/market-<topic>-research-<date>.md`
**Workflow:** `{skill-dir}/workflows/1-analysis/research/workflow-market-research.md`

### Document Project
**Triggers:** "document project", "generate project context", "project context"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/project-context-<date>.md`
**Workflow:** `{skill-dir}/workflows/document-project/workflow.yaml`

---

## Phase 2 — Planning

### Create PRD
**Triggers:** "create PRD", "product requirements", "create product requirements document"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/prd.md`
**Workflow:** `{skill-dir}/workflows/2-plan-workflows/create-prd/workflow-create-prd.md`

### Edit PRD
**Triggers:** "edit PRD", "update PRD", "revise PRD"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/prd.md` (updated in place)
**Workflow:** `{skill-dir}/workflows/2-plan-workflows/create-prd/workflow-edit-prd.md`

### Validate PRD
**Triggers:** "validate PRD", "review PRD", "check PRD"
**Output artifact:** Review report inline
**Workflow:** `{skill-dir}/workflows/2-plan-workflows/create-prd/workflow-validate-prd.md`

### Create UX Design
**Triggers:** "create UX design", "UX specifications", "user experience design", "UI design"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/ux-design-<date>.md`
**Workflow:** `{skill-dir}/workflows/2-plan-workflows/create-ux-design/workflow.md`

---

## Phase 3 — Solutioning

### Create Architecture
**Triggers:** "create architecture", "technical architecture", "solution design", "system design"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/architecture.md`
**Workflow:** `{skill-dir}/workflows/3-solutioning/create-architecture/workflow.md`

### Create Epics and Stories
**Triggers:** "create epics and stories", "epics and stories", "break down into stories", "epic breakdown"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/epics-and-stories.md`
**Workflow:** `{skill-dir}/workflows/3-solutioning/create-epics-and-stories/workflow.md`

### Check Implementation Readiness
**Triggers:** "check implementation readiness", "readiness check", "ready for development"
**Output artifact:** Readiness report inline
**Workflow:** `{skill-dir}/workflows/3-solutioning/check-implementation-readiness/workflow.md`

---

## Phase 4 — Implementation

### Sprint Planning
**Triggers:** "sprint planning", "plan sprint", "select stories for sprint"
**Output artifact:** `{project-root}/_bmad-output/implementation-artifacts/sprint-status.yaml`
**Workflow:** `{skill-dir}/workflows/4-implementation/sprint-planning/workflow.yaml`

### Sprint Status
**Triggers:** "sprint status", "show sprint status", "sprint progress"
**Workflow:** `{skill-dir}/workflows/4-implementation/sprint-status/workflow.yaml`

### Create Story
**Triggers:** "create story", "next story", "write story", "author story"
**Output artifact:** `{project-root}/_bmad-output/implementation-artifacts/<story-key>.md`
**Workflow:** `{skill-dir}/workflows/4-implementation/create-story/workflow.yaml`

### Dev Story
**Triggers:** "dev story", "implement story", "develop story", "code story"
**Input:** Story file at `{project-root}/_bmad-output/implementation-artifacts/<story-key>.md`
**Workflow:** `{skill-dir}/workflows/4-implementation/dev-story/workflow.yaml`

### Code Review
**Triggers:** "code review", "review code", "review implementation"
**Workflow:** `{skill-dir}/workflows/4-implementation/code-review/workflow.yaml`

### Retrospective
**Triggers:** "retrospective", "sprint retrospective", "team retrospective"
**Output artifact:** `{project-root}/_bmad-output/implementation-artifacts/retrospective-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-implementation/retrospective/workflow.yaml`

### Correct Course
**Triggers:** "correct course", "course correction", "pivot", "re-scope"
**Workflow:** `{skill-dir}/workflows/4-implementation/correct-course/workflow.yaml`

### QA Generate E2E Tests
**Triggers:** "generate e2e tests", "QA tests", "end to end tests", "automated tests"
**Output artifact:** `{project-root}/_bmad-output/test-artifacts/e2e-tests-<date>.md`
**Workflow:** `{skill-dir}/workflows/qa-generate-e2e-tests/workflow.yaml`

### Generate Project Context
**Triggers:** "generate project context", "project context document"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/project-context-<date>.md`
**Workflow:** `{skill-dir}/workflows/generate-project-context/workflow.md`

### Quick Spec
**Triggers:** "quick spec", "rapid specification", "fast spec"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/quick-spec-<date>.md`
**Workflow:** `{skill-dir}/workflows/bmad-quick-flow/quick-spec/workflow.md`

### Quick Dev
**Triggers:** "quick dev", "rapid development", "fast dev"
**Workflow:** `{skill-dir}/workflows/bmad-quick-flow/quick-dev/workflow.md`

---

## Execution Instructions

When any BMM workflow is triggered:
1. Identify the workflow from the trigger phrase.
2. Read the full workflow file at the path shown above using `code_execution_tool` (bash cat).
3. Follow the workflow instructions exactly — do not summarize or skip steps.
4. Write output artifacts to the paths specified using `code_execution_tool` (bash write).
5. Update `{project-root}/instructions/02-bmad-state.md` after significant state changes.

## Knowledge Integration

After completing major planning artifact workflows (Create Product Brief, Create PRD, Create Architecture, Create Epics and Stories), optionally index the artifact for semantic retrieval:

```bash
cp {artifact-path} {project-root}/knowledge/main/{artifact-filename}
```

This enables any BMAD persona to query project context using Agent Zero's `document_query` tool:
- Query the PRD: "what are the success criteria for this project?"
- Query the architecture: "what database technology is specified?"
- Query epics: "what stories are in epic 3?"

**When to use `document_query` vs. `code_execution_tool` cat:**
- Use `document_query` for natural-language semantic queries (finding relevant sections without reading the full document)
- Use `code_execution_tool` cat for reading entire workflow files or when you need complete file contents

**Dev Story knowledge usage:** When the Dev Story workflow is active and the story references architecture decisions or PRD requirements, use `document_query` to retrieve the relevant context rather than re-reading the full 50-100KB planning documents:
```
document_query: "what are the authentication requirements from the PRD?"
document_query: "what is the database schema for user management?"
```
