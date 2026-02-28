---
name: "bmad-tea"
description: "BMAD Testing Excellence Accelerator — test architecture, ATDD, automation, CI integration, test design, trace, NFR assessment, test review, teach me testing. Triggers: test architecture, testing strategy, ATDD, acceptance test driven, automate tests, test automation, CI integration, continuous integration tests, test framework, test design, test cases, trace tests, traceability, NFR assessment, non-functional requirements test, test review, review tests, teach me testing, learn testing, tea module."
version: "1.0.0"
author: "BMAD"
tags: ["bmad", "tea", "testing", "quality", "automation"]
trigger_patterns:
  - "test architecture"
  - "testing strategy"
  - "ATDD"
  - "acceptance test driven"
  - "automate tests"
  - "test automation"
  - "CI integration"
  - "test framework"
  - "test design"
  - "test cases"
  - "trace tests"
  - "traceability"
  - "NFR assessment"
  - "test review"
  - "review tests"
  - "teach me testing"
  - "learn testing"
  - "tea module"
---

# BMAD Testing Excellence Accelerator (TEA) — Test Architecture and Automation

TEA provides structured testing workflows: test architecture design, ATDD, test automation, CI integration, traceability, NFR assessment, and test review. Use TEA to build comprehensive, traceable, and automated test coverage.

All paths use `{project-root}` which resolves to `.a0proj/` as defined in `01-bmad-config.md`.

When any TEA workflow is triggered, read the full workflow file at the path shown and follow it exactly.

---

## TEA Workflows

### ATDD — Acceptance Test Driven Development
**Triggers:** "ATDD", "acceptance test driven", "acceptance tests", "BDD", "behavior driven"
**Output artifact:** `{project-root}/_bmad-output/test-artifacts/atdd-<story>-<date>.md`
**Workflow:** `{project-root}/_bmad/tea/workflows/testarch/atdd/workflow.yaml`

### Automate Tests
**Triggers:** "automate tests", "test automation", "automated test suite", "automation scripts"
**Output artifact:** `{project-root}/_bmad-output/test-artifacts/automation-<date>.md`
**Workflow:** `{project-root}/_bmad/tea/workflows/testarch/automate/workflow.yaml`

### CI Integration
**Triggers:** "CI integration", "continuous integration tests", "pipeline tests", "CI/CD testing"
**Output artifact:** `{project-root}/_bmad-output/test-artifacts/ci-integration-<date>.md`
**Workflow:** `{project-root}/_bmad/tea/workflows/testarch/ci/workflow.yaml`

### Test Framework
**Triggers:** "test framework", "testing framework", "set up test framework", "choose test framework"
**Output artifact:** `{project-root}/_bmad-output/test-artifacts/test-framework-<date>.md`
**Workflow:** `{project-root}/_bmad/tea/workflows/testarch/framework/workflow.yaml`

### NFR Assessment
**Triggers:** "NFR assessment", "non-functional requirements test", "performance testing", "security testing", "scalability testing"
**Output artifact:** `{project-root}/_bmad-output/test-artifacts/nfr-assessment-<date>.md`
**Workflow:** `{project-root}/_bmad/tea/workflows/testarch/nfr-assess/workflow.yaml`

### Test Design
**Triggers:** "test design", "test cases", "design test cases", "test plan", "test strategy"
**Output artifact:** `{project-root}/_bmad-output/test-artifacts/test-design-<date>.md`
**Workflow:** `{project-root}/_bmad/tea/workflows/testarch/test-design/workflow.yaml`

### Test Review
**Triggers:** "test review", "review tests", "audit tests", "test quality review"
**Output artifact:** Test review report inline
**Workflow:** `{project-root}/_bmad/tea/workflows/testarch/test-review/workflow.yaml`

### Trace Tests
**Triggers:** "trace tests", "traceability", "test traceability matrix", "requirements coverage"
**Output artifact:** `{project-root}/_bmad-output/test-artifacts/traceability-matrix-<date>.md`
**Workflow:** `{project-root}/_bmad/tea/workflows/testarch/trace/workflow.yaml`

### Teach Me Testing
**Triggers:** "teach me testing", "learn testing", "testing tutorial", "testing concepts"
**Output artifact:** Educational content inline
**Workflow:** `{project-root}/_bmad/tea/workflows/testarch/teach-me-testing/workflow.md`

---

## Execution Instructions

When any TEA workflow is triggered:
1. Identify the workflow from the trigger phrase.
2. Read the full workflow file at the path shown above using `code_execution_tool` (bash cat).
3. Follow the workflow instructions exactly — do not summarize or skip steps.
4. Write output artifacts using `code_execution_tool` (bash write).
5. Update `{project-root}/instructions/02-bmad-state.md` to reflect the active TEA workflow.
