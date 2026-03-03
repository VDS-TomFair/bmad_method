# Test Scenarios: TEA Module (Testing Excellence Accelerator)

**Priority:** HIGH (dogfooding — TEA tests itself)  
**Skill:** `bmad-tea`  
**Agent:** Murat (bmad-test-architect)  
**Workflow paths:** `skills/bmad-tea/workflows/testarch/`  
**9 Workflows:** atdd, automate, ci, framework, nfr-assess, teach-me-testing, test-design, test-review, trace  
**Risk:** TEA is the BMAD quality gate — failures undermine all other module quality  

---

## Scenario TEA-01: Skill Load and Routing Table Completeness

**Objective:** Verify bmad-tea SKILL.md loads and exposes all 9 workflow trigger mappings  
**Risk Level:** CRITICAL  

### Steps
1. Trigger: "test architecture" or "testing strategy"
2. Observe `skills_tool:load` for `bmad-tea`
3. Verify SKILL.md routing table entries

### Expected: All 9 triggers present
| Trigger | Workflow Path |
|---------|---------------|
| "ATDD", "acceptance test driven" | `testarch/atdd/workflow.yaml` |
| "automate tests", "test automation" | `testarch/automate/workflow.yaml` |
| "CI integration", "continuous integration tests" | `testarch/ci/workflow.yaml` |
| "test framework", "testing framework" | `testarch/framework/workflow.yaml` |
| "NFR assessment", "non-functional requirements test" | `testarch/nfr-assess/workflow.yaml` |
| "test design", "test cases" | `testarch/test-design/workflow.yaml` |
| "test review", "review tests" | `testarch/test-review/workflow.yaml` |
| "trace tests", "traceability" | `testarch/trace/workflow.yaml` |
| "teach me testing", "learn testing" | `testarch/teach-me-testing/workflow.md` |

### Pass Criteria
- [ ] All 9 workflow triggers present in SKILL.md
- [ ] Workflow paths all use `{skill-dir}/` prefix (not hardcoded absolute paths)
- [ ] Output artifact patterns include `{project-root}/_bmad-output/test-artifacts/`
- [ ] Murat persona active on skill load

---

## Scenario TEA-02: Menu Display — Murat's 9-Item Workflow Menu

**Objective:** Verify Murat presents correct numbered menu on activation  
**Risk Level:** HIGH  

### Steps
1. Activate bmad-test-architect agent profile
2. Observe initial greeting and menu

### Expected Menu
```
| 1 | TMT  | Teach Me Testing |
| 2 | TF   | Test Framework   |
| 3 | AT   | ATDD             |
| 4 | TA   | Test Automation  |
| 5 | TD   | Test Design      |
| 6 | TR   | Trace Requirements |
| 7 | NR   | NFR Assessment   |
| 8 | CI   | Continuous Integration |
| 9 | RV   | Review Tests     |
```

### Pass Criteria
- [ ] Greeting uses name "Murat" and title "Master Test Architect and Quality Advisor"
- [ ] Icon 🧪 present
- [ ] All 9 numbered items present
- [ ] CH, PM, MH, DA, /bmad-help always-available items listed
- [ ] Menu STOPS and waits — does NOT auto-execute any item

---

## Scenario TEA-03: ATDD Workflow (AT / Menu Item 3)

**Objective:** Verify ATDD generates failing acceptance tests before implementation  
**Risk Level:** CRITICAL  
**Workflow:** `skills/bmad-tea/workflows/testarch/atdd/`  
**Step structure:** steps-c/ (preflight, mode, strategy, generate-tests, validate) + steps-e/ + steps-v/

### Steps
1. Select menu item 3 (AT) or say "ATDD"
2. Provide sample story: "As a user, I can reset my password via email link"
3. Execute workflow through all steps-c stages
4. Verify output artifact

### Expected Behavior
- Workflow loads `atdd/workflow.yaml` via skills_tool read
- Steps execute: preflight-and-context → generation-mode → test-strategy → generate-tests (api + e2e) → validate
- ATDD output contains:
  - Failing API tests (not yet passing)
  - Failing E2E tests (not yet passing)
  - Implementation checklist derived from acceptance criteria
  - Clear test IDs for traceability
- Artifact saved to: `{project-root}/_bmad-output/test-artifacts/atdd-<story>-<date>.md`

### Pass Criteria
- [ ] Workflow reads step files sequentially (step-01 → step-02 → ...)
- [ ] Failing tests generated (not placeholder stubs)
- [ ] Implementation checklist present
- [ ] Output at correct test-artifacts path with date stamp
- [ ] State updated: active artifact = atdd output file

---

## Scenario TEA-04: Test Framework Workflow (TF / Menu Item 2)

**Objective:** Verify framework workflow selects appropriate framework and scaffolds it  
**Risk Level:** HIGH  
**Workflow:** `skills/bmad-tea/workflows/testarch/framework/`  
**Steps:** preflight → select-framework → scaffold-framework → docs-and-scripts → validate-and-summary

### Steps
1. Select menu item 2 (TF) or say "test framework"
2. Provide: tech stack = "Python FastAPI backend"
3. Execute all 5 steps
4. Verify output

### Expected Behavior
- Framework selection step presents options with risk-calibrated recommendations
- For Python/FastAPI: recommends pytest as primary framework
- Scaffold step generates: `conftest.py`, `pytest.ini`/`pyproject.toml`, fixture hierarchy
- Docs-and-scripts step generates README and helper scripts
- Output artifact: `test-framework-<date>.md` with setup instructions

### Pass Criteria
- [ ] Framework recommendation includes rationale (not just tool name)
- [ ] Scaffold files generated (not just described)
- [ ] Fixture hierarchy matches team's risk profile
- [ ] Output at test-artifacts path

---

## Scenario TEA-05: Test Automation Workflow (TA / Menu Item 4)

**Objective:** Verify automation workflow generates prioritized test suite for existing feature  
**Risk Level:** HIGH  
**Workflow:** `skills/bmad-tea/workflows/testarch/automate/`  
**Steps:** preflight-and-context → identify-targets → generate-tests (api + e2e + backend) → validate-and-summarize

### Steps
1. Select menu item 4 (TA) or say "automate tests"
2. Provide feature context: "User authentication API with JWT"
3. Execute workflow

### Expected Behavior
- Target identification step produces risk-prioritized test list
- Test generation branches: api subprocess + e2e subprocess + backend subprocess
- Tests mirror actual usage (consumer patterns, real user journeys)
- DoD summary confirms coverage
- Output: `automation-<date>.md` with test suite

### Pass Criteria
- [ ] Tests prioritized by risk (not alphabetical or arbitrary order)
- [ ] API tests and E2E tests generated as separate concerns
- [ ] DoD checklist present at end
- [ ] Tests reference actual endpoints/selectors (not abstract pseudocode)

---

## Scenario TEA-06: Test Design Workflow (TD / Menu Item 5)

**Objective:** Verify test design produces risk assessment and coverage strategy  
**Risk Level:** HIGH  
**Workflow:** `skills/bmad-tea/workflows/testarch/test-design/`  
**Steps:** detect-mode → load-context → risk-and-testability → coverage-plan → generate-output

### Steps
1. Select menu item 5 (TD) or say "test design"
2. Provide: system scope = "Payment processing microservice"
3. Execute workflow

### Expected Behavior
- Risk assessment identifies: high-risk areas, change frequency, business impact
- Coverage plan calibrated to risk (deep on payment paths, lighter on logging)
- Multiple test design templates available (architecture, QA, handoff)
- Output: `test-design-<date>.md` with risk matrix and coverage plan

### Pass Criteria
- [ ] Risk matrix present with business impact ratings
- [ ] Coverage depth explicitly calibrated to risk level
- [ ] Equivalence partitioning / boundary analysis mentioned for applicable areas
- [ ] Pyramid proportions recommended (unit > integration > E2E rationale)

---

## Scenario TEA-07: Trace Requirements Workflow (TR / Menu Item 6)

**Objective:** Verify traceability workflow maps requirements to tests and makes gate decision  
**Risk Level:** HIGH  
**Workflow:** `skills/bmad-tea/workflows/testarch/trace/`  
**Steps:** load-context → discover-tests → map-criteria → analyze-gaps → gate-decision

### Steps
1. Select menu item 6 (TR) or say "trace tests"
2. Provide requirements source (e.g., PRD or stories)
3. Provide existing test suite location
4. Execute workflow through Phase 1 (traceability) and Phase 2 (gate decision)

### Expected Behavior
- Phase 1: Requirements → test case matrix generated
- Phase 2: Coverage completeness → SHIP / HOLD recommendation
- Gaps identified: untested requirements listed
- Orphaned tests identified: tests with no requirement link
- Output: `traceability-matrix-<date>.md`

### Pass Criteria
- [ ] Bidirectional traceability (requirements→tests AND tests→requirements)
- [ ] Clear SHIP / HOLD gate decision with justification
- [ ] Untested requirements enumerated
- [ ] Orphaned tests enumerated

---

## Scenario TEA-08: NFR Assessment Workflow (NR / Menu Item 7)

**Objective:** Verify NFR assessment covers all 4 NFR dimensions  
**Risk Level:** MEDIUM  
**Workflow:** `skills/bmad-tea/workflows/testarch/nfr-assess/`  
**Steps:** load-context → define-thresholds → gather-evidence → evaluate-and-score (security/performance/reliability/scalability subprocesses + aggregate) → generate-report

### Steps
1. Select menu item 7 (NR) or say "NFR assessment"
2. Provide system context
3. Execute workflow through all subprocess stages

### Expected Behavior
- Four NFR dimensions assessed: security, performance, reliability, scalability
- Each dimension: evidence gathered → scored → remediation recommended
- Aggregate NFR score produced
- Output: `nfr-assessment-<date>.md` using nfr-report-template.md structure

### Pass Criteria
- [ ] All 4 NFR dimensions present in report
- [ ] Measurable thresholds defined (not just "should be fast")
- [ ] Specific tools recommended per dimension (e.g., k6 for load, OWASP ZAP for security)
- [ ] Aggregate readiness recommendation

---

## Scenario TEA-09: CI Integration Workflow (CI / Menu Item 8)

**Objective:** Verify CI workflow scaffolds a complete quality pipeline  
**Risk Level:** HIGH  
**Workflow:** `skills/bmad-tea/workflows/testarch/ci/`  
**Templates available:** github-actions, gitlab-ci, azure-pipelines, jenkins, harness  
**Steps:** preflight → generate-pipeline → configure-quality-gates → validate-and-summary

### Steps
1. Select menu item 8 (CI) or say "CI integration"
2. Specify: platform = "GitHub Actions", stack = "Python pytest + Playwright"
3. Execute workflow

### Expected Behavior
- Pipeline generated from `github-actions-template.yaml` template
- Quality gates configured with data-backed thresholds:
  - Coverage threshold (e.g., 80% line coverage)
  - Test pass rate (100% required)
  - Flakiness detection step included
- Output: working GitHub Actions YAML (not pseudocode)

### Pass Criteria
- [ ] Valid YAML generated (parseable)
- [ ] Quality gate thresholds present with justification
- [ ] Parallel test execution strategy included
- [ ] Platform matches requested target

---

## Scenario TEA-10: Test Review Workflow (RV / Menu Item 9)

**Objective:** Verify review workflow catches testing anti-patterns  
**Risk Level:** HIGH  
**Workflow:** `skills/bmad-tea/workflows/testarch/test-review/`  
**Steps:** load-context → discover-tests → quality-evaluation (determinism/isolation/maintainability/performance subprocesses + aggregate) → generate-report

### Steps
1. Select menu item 9 (RV) or say "review tests"
2. Point to a test file with known issues (e.g., hardcoded waits, poor selectors)
3. Execute workflow

### Expected Behavior
- Tests evaluated on 4 quality dimensions: determinism, isolation, maintainability, performance
- Anti-patterns identified:
  - Hardcoded `sleep()` waits → flag as determinism issue
  - `//div[1]` XPath selectors → flag as brittle selector
  - Test that modifies shared global state → flag as isolation issue
  - Test file with 500+ lines → flag as maintainability issue
- Improvement plan prioritized by impact

### Pass Criteria
- [ ] All 4 quality dimensions scored
- [ ] Specific anti-patterns named with line references
- [ ] Remediation prioritized (not just listed)
- [ ] Flakiness explicitly addressed

---

## Scenario TEA-11: Teach Me Testing (TMT / Menu Item 1)

**Objective:** Verify TMT presents 7-session progressive curriculum  
**Risk Level:** MEDIUM  
**Workflow:** `skills/bmad-tea/workflows/testarch/teach-me-testing/`  
**Data:** curriculum.yaml, role-paths.yaml, session-content-map.yaml, quiz-questions.yaml

### Steps
1. Select menu item 1 (TMT) or say "teach me testing"
2. Execute init step
3. Complete assessment step
4. Navigate to session menu
5. Select Session 1 and complete it

### Expected Behavior
- Init step asks about learner background
- Assessment determines starting point
- Session menu shows 7 sessions with role-based paths
- Session 1 delivers foundational testing concepts
- Progress tracking via progress-template.yaml
- Certificate generated upon completion (certificate-template.md)

### Pass Criteria
- [ ] 7 sessions enumerable from session menu
- [ ] Curriculum follows testing fundamentals → advanced progression
- [ ] Quiz questions present at session end
- [ ] Session notes saved using session-notes-template.md

---

## Scenario TEA-12: Knowledge Base Accessibility

**Objective:** Verify Murat can access and apply TEA knowledge base during workflows  
**Risk Level:** MEDIUM  
**Knowledge base:** `skills/bmad-tea/testarch/knowledge/` (35 files)

### Steps
1. Ask Murat: "What is the recommended fixture architecture for Playwright?"
2. Ask Murat: "How should I handle authentication in test fixtures?"
3. Ask Murat: "What is the selector resilience approach?"

### Expected Behavior
- Murat reads from `testarch/knowledge/fixture-architecture.md`
- Murat reads from `testarch/knowledge/auth-session.md`
- Murat reads from `testarch/knowledge/selector-resilience.md`
- Responses are grounded in knowledge base content, not generic advice

### Pass Criteria
- [ ] Knowledge base files accessible via skills_tool or code_execution_tool
- [ ] Responses reflect specific knowledge file content
- [ ] tea-index.csv used for knowledge base discovery

---

## Scenario TEA-13: Workflow Step File Sequential Execution

**Objective:** Verify all TEA workflows follow step-file sequential execution (steps-c → steps-e → steps-v)  
**Risk Level:** HIGH  

### Steps
For any TEA workflow (e.g., test-design):
1. Observe which files are loaded
2. Verify steps-c/ files load in numbered order (step-01, step-02, ...)
3. Verify steps-e/ (edit/refine) only loaded if revision needed
4. Verify steps-v/ (validate) loaded at end

### Expected Behavior
- Create steps (steps-c/) execute in sequence for happy path
- Edit steps (steps-e/) available for revision cycle
- Validate step (steps-v/) always runs at end
- workflow.yaml references all steps correctly

### Pass Criteria
- [ ] Step files load in correct numeric order
- [ ] No skipped steps in happy path
- [ ] Validate step always executes
- [ ] workflow.yaml and workflow.md are consistent
