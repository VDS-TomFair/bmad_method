# Test Scenarios: BMM Module (BMAD Method Module)

**Priority:** CRITICAL  
**Skill:** `bmad-bmm`  
**Agents:** bmad-analyst, bmad-pm, bmad-ux-designer, bmad-architect, bmad-sm, bmad-dev, bmad-quick-dev, bmad-qa, bmad-tech-writer  
**Risk:** BMM is the core value delivery engine — phase failures block all downstream planning and implementation  

---

## Scenario BMM-01: Skill Load and Menu Display

**Objective:** Verify bmad-bmm skill loads without error and routing table is accessible  
**Risk Level:** CRITICAL  

### Steps
1. Trigger bmad-bmm load: say "create PRD" or activate any BMM agent
2. Observe skills_tool:load call for `bmad-bmm`
3. Verify SKILL.md content is returned
4. Confirm workflow routing table is present

### Expected Behavior
- `skills_tool:load` with `skill_name: bmad-bmm` succeeds
- SKILL.md body returned with workflow trigger table
- All 4 phase workflow groups present: `1-analysis/`, `2-plan-workflows/`, `3-solutioning/`, `4-implementation/`
- Quick Flow entries present: `bmad-quick-flow/`
- Document Project and Generate Project Context entries present

### Pass Criteria
- [ ] Skill loads without error
- [ ] Workflow triggers enumerated in SKILL.md
- [ ] Phase organization matches official BMAD phases 1-4

---

## Scenario BMM-02: Phase 1 Analysis — Brainstorm Workflow

**Objective:** Verify brainstorm workflow loads and executes through steps  
**Risk Level:** HIGH  
**Workflow path:** `skills/bmad-bmm/workflows/1-analysis/brainstorm/`  

### Preconditions
- Project initialized, 02-bmad-state.md: `phase: ready`
- Analyst agent active (bmad-analyst profile)

### Steps
1. Trigger: say "brainstorm project" or "brainstorm [idea]"
2. Verify skill loads `bmad-bmm`
3. Verify workflow path resolved: `{skill-dir}/workflows/1-analysis/brainstorm/`
4. Observe step-file execution sequence
5. Provide sample brainstorm inputs at each step
6. Verify artifact output location

### Expected Behavior
- Analyst persona active: Mary, strategic analyst, WHY-focused
- Workflow steps execute sequentially (step-01, step-02, etc.)
- Brainstorm artifact written to `{planning_artifacts}/` 
- 02-bmad-state.md updated: `phase: analysis`, `active artifact: brainstorm output`

### Pass Criteria
- [ ] Analyst persona characteristics present (Mary, strategic analyst)
- [ ] Steps execute in correct sequence
- [ ] Output artifact written to planning_artifacts/ (absolute path)
- [ ] State file updated after completion

---

## Scenario BMM-03: Phase 1 Analysis — Domain Research Workflow

**Objective:** Verify domain research workflow produces structured research artifact  
**Risk Level:** HIGH  
**Workflow path:** `skills/bmad-bmm/workflows/1-analysis/domain-research/`  

### Steps
1. Trigger: "domain research" or "research [domain]"
2. Execute workflow to completion with sample domain (e.g., "e-commerce payment processing")
3. Verify artifact structure and output path

### Expected Behavior
- Analyst (Mary) persona active
- Research artifact produced with: market context, domain terminology, key players, risk factors
- Artifact saved to `{planning_artifacts}/research/` or `{planning_artifacts}/`
- State updated to reflect analysis phase progress

### Pass Criteria
- [ ] Research artifact created at correct path
- [ ] Artifact contains structured research sections
- [ ] State reflects analysis phase

---

## Scenario BMM-04: Phase 2 Planning — Create PRD Workflow

**Objective:** Verify PRD creation workflow produces spec-compliant PRD artifact  
**Risk Level:** CRITICAL  
**Workflow path:** `skills/bmad-bmm/workflows/2-plan-workflows/create-prd/`  

### Preconditions
- Phase 1 analysis artifacts exist (or can proceed directly for greenfield)
- PM agent active (bmad-pm profile)

### Steps
1. Trigger: "create PRD" or "product requirements"
2. Execute full workflow with sample product concept ("task management SaaS")
3. Accept or provide inputs at each interactive step
4. Verify final PRD artifact

### Expected Behavior
- PM persona active: John, 8+ years experience, asks WHY relentlessly
- PRD workflow loads from `skills/bmad-bmm/workflows/2-plan-workflows/create-prd/`
- Step files execute sequentially with HALT/user interaction points
- Final PRD artifact contains:
  - Product overview and goals
  - User personas or target users
  - Functional requirements (epics/stories level)
  - Non-functional requirements
  - Success metrics
  - Out of scope items
- PRD saved as `{planning_artifacts}/prd.md`
- State updated: `phase: planning`, `active artifact: prd.md`

### Pass Criteria
- [ ] PM (John) persona active with correct communication style
- [ ] All required PRD sections present
- [ ] Artifact at `{planning_artifacts}/prd.md` (absolute path)
- [ ] State file updated

---

## Scenario BMM-05: Phase 2 Planning — Create UX Design Workflow

**Objective:** Verify UX design workflow produces structured UX specification  
**Risk Level:** HIGH  
**Workflow path:** `skills/bmad-bmm/workflows/2-plan-workflows/`  

### Preconditions
- PRD exists at `{planning_artifacts}/prd.md`
- UX Designer agent active (bmad-ux-designer profile)

### Steps
1. Trigger: "create UX design" or "UX specifications"
2. Reference PRD as input context
3. Execute workflow to completion

### Expected Behavior
- Sally (UX Designer) persona active: empathy-driven, 7+ years
- UX spec references PRD requirements
- Output contains: user flows, key screens/interactions, design principles
- Artifact saved to `{planning_artifacts}/ux-design.md` or equivalent
- State updated

### Pass Criteria
- [ ] UX Designer (Sally) persona active
- [ ] PRD referenced as context
- [ ] UX artifact created at planning_artifacts path

---

## Scenario BMM-06: Phase 3 Solutioning — Create Architecture Workflow

**Objective:** Verify architecture workflow produces technical architecture document  
**Risk Level:** CRITICAL  
**Workflow path:** `skills/bmad-bmm/workflows/3-solutioning/`  

### Preconditions
- PRD at `{planning_artifacts}/prd.md`
- Architect agent active (bmad-architect profile)

### Steps
1. Trigger: "create architecture" or "technical architecture"
2. Execute workflow using sample system requirements from PRD
3. Verify output artifact

### Expected Behavior
- Winston (Architect) persona: distributed systems expert, connects to business value
- Architecture document contains:
  - System overview and component diagram
  - Technology stack choices with rationale
  - API design patterns
  - Data model overview
  - Infrastructure and deployment approach
  - Key architectural decisions (ADRs or equivalent)
- Artifact saved to `{planning_artifacts}/architecture.md`
- State updated: `phase: solutioning`

### Pass Criteria
- [ ] Architect (Winston) persona active
- [ ] All required architecture sections present
- [ ] Technology choices include rationale (not just selections)
- [ ] Artifact at planning_artifacts path
- [ ] State updated to solutioning phase

---

## Scenario BMM-07: Phase 3 Solutioning — Create Epics and Stories

**Objective:** Verify epics creation workflow decomposes PRD into actionable epics/stories  
**Risk Level:** HIGH  
**Workflow path:** `skills/bmad-bmm/workflows/3-solutioning/`  

### Preconditions
- PRD and architecture artifacts exist

### Steps
1. Trigger: "create epics and stories" or "epics and stories"
2. Provide PRD reference
3. Execute workflow to completion

### Expected Behavior
- Epics file contains structured epics with user stories
- Each story has: title, user story format (As a... I want... So that...), acceptance criteria
- Stories are implementation-ready (specific, testable)
- Output at `{planning_artifacts}/epics.md` or equivalent

### Pass Criteria
- [ ] Epics/stories in correct user story format
- [ ] Acceptance criteria present on each story
- [ ] Stories traceable to PRD requirements
- [ ] Artifact at planning_artifacts path

---

## Scenario BMM-08: Phase 3 — Check Implementation Readiness

**Objective:** Verify implementation readiness check validates all phase 1-3 artifacts  
**Risk Level:** HIGH  
**Workflow path:** `skills/bmad-bmm/workflows/3-solutioning/check-implementation-readiness/`  

### Steps
1. Trigger: "check implementation readiness"
2. Execute workflow — should discover and validate: PRD, architecture, UX, epics
3. Observe readiness report

### Expected Behavior
- Workflow discovers artifacts in `{planning_artifacts}/`
- Validates each artifact for completeness
- Generates readiness report with: coverage status, gaps, recommendation (READY / NOT READY)
- Report saved to `{planning_artifacts}/implementation-readiness-report-{date}.md`

### Pass Criteria
- [ ] All artifacts checked against completeness criteria
- [ ] Report contains clear READY/NOT READY recommendation
- [ ] Missing artifacts listed with remediation guidance
- [ ] Report saved with date stamp in filename

---

## Scenario BMM-09: Phase 4 Implementation — Dev Story Workflow

**Objective:** Verify dev-story workflow produces implementation-ready story with tasks  
**Risk Level:** CRITICAL  
**Workflow path:** `skills/bmad-bmm/workflows/4-implementation/dev-story/`  

### Preconditions
- Epics and architecture artifacts exist
- Developer agent active (bmad-dev profile)

### Steps
1. Trigger: "dev story" or "implement story [story-id]"
2. Reference an epic story as input
3. Execute workflow to completion

### Expected Behavior
- Amelia (Dev Agent) persona: TDD-focused, strict story adherence
- Story file contains:
  - Story context from epics/PRD
  - Implementation tasks (numbered, specific)
  - Technical notes and constraints
  - Testing requirements
  - Definition of Done checklist
- Story saved to `{implementation_artifacts}/epic-X-Y-story.md`
- State updated: `phase: implementation`, `active artifact: story file`

### Pass Criteria
- [ ] Dev (Amelia) persona active
- [ ] Story file contains implementation tasks
- [ ] DoD checklist present
- [ ] Artifact at implementation_artifacts path (not planning_artifacts)
- [ ] State updated to implementation phase

---

## Scenario BMM-10: Phase 4 — Sprint Planning

**Objective:** Verify sprint planning workflow produces structured sprint plan  
**Risk Level:** HIGH  
**Workflow path:** `skills/bmad-bmm/workflows/4-implementation/`  

### Preconditions
- Epics and stories available
- Scrum Master agent active (bmad-sm profile)

### Steps
1. Trigger: "sprint planning" or "plan sprint"
2. Provide available stories as input
3. Execute workflow to completion

### Expected Behavior
- Bob (Scrum Master) persona: certified SM, zero tolerance for ambiguity
- Sprint plan contains: sprint goal, selected stories, capacity allocation
- Sprint status file created: `{implementation_artifacts}/sprint-status.yaml`

### Pass Criteria
- [ ] SM (Bob) persona active
- [ ] Sprint status file created at implementation_artifacts
- [ ] Sprint plan contains goal and selected stories

---

## Scenario BMM-11: Quick Flow Track — Quick Spec to Implementation

**Objective:** Verify Quick Flow delivers spec + implementation without full Phase 1-3  
**Risk Level:** CRITICAL  
**Workflow path:** `skills/bmad-bmm/workflows/bmad-quick-flow/`  

### Preconditions
- Simple project scope (< 500 LOC equivalent)
- Quick Dev agent active (bmad-quick-dev profile)

### Steps
1. Trigger: "quick flow" or activate bmad-quick-dev agent
2. Provide simple feature description
3. Execute quick-spec workflow
4. Execute dev-quick-flow implementation workflow
5. Verify artifacts

### Expected Behavior
- Barry (Quick Dev) persona: "minimum ceremony, lean artifacts, ruthless efficiency"
- Quick spec created: lean tech spec, skips PRD/architecture formality
- Implementation begins directly from tech spec
- No Phase 1-3 gates enforced
- Output: tech-spec.md + implementation

### Pass Criteria
- [ ] Quick Dev (Barry) persona active with efficiency-focused framing
- [ ] Quick spec created without full PRD/architecture ceremony
- [ ] Implementation follows spec without extra planning steps
- [ ] Time from trigger to first implementation is substantially faster than Method track

---

## Scenario BMM-12: Document Project Workflow

**Objective:** Verify document-project workflow generates comprehensive project documentation  
**Risk Level:** MEDIUM  
**Workflow path:** `skills/bmad-bmm/workflows/document-project/`  

### Steps
1. Trigger: "document project" or via Tech Writer agent
2. Execute workflow on a project with existing artifacts
3. Verify documentation output

### Expected Behavior
- Tech Writer (Paige) persona: CommonMark/DITA expert, clarity-focused
- Documentation generated from existing artifacts
- Output includes: README, API docs structure, deployment notes
- Docs written to `{output_folder}/` (permanent docs location)

### Pass Criteria
- [ ] Tech Writer (Paige) persona active
- [ ] Documentation references existing artifacts
- [ ] Output written to output_folder (not planning or implementation artifacts)

---

## Scenario BMM-13: Generate Project Context Workflow

**Objective:** Verify project context file is generated and usable as workflow input  
**Risk Level:** MEDIUM  
**Workflow path:** `skills/bmad-bmm/workflows/generate-project-context/`  

### Steps
1. Trigger: "generate project context" or equivalent
2. Execute workflow
3. Verify context file output and format

### Expected Behavior
- project-context.md generated by assembling existing artifacts
- File serves as single discovery document for agent workflows
- Content includes: project description, key decisions, phase status, artifact index
- Saved to `{project-root}/` or `{planning_artifacts}/`

### Pass Criteria
- [ ] project-context.md created
- [ ] Contains structured project overview
- [ ] References all existing planning artifacts

---

## Scenario BMM-14: Phase Gating Enforcement

**Objective:** Verify that workflows respect phase prerequisites and warn when skipped  
**Risk Level:** HIGH  

### Steps
1. Start fresh project (no planning artifacts)
2. Attempt to trigger Phase 4 workflow directly: "dev story" without PRD/architecture
3. Observe agent response

### Expected Behavior
- Agent warns that prerequisite artifacts are missing
- Either: refuses to proceed (strict gating) OR proceeds with explicit user override
- Does NOT silently produce incomplete stories without context

### Pass Criteria
- [ ] Missing prerequisites identified and communicated
- [ ] User informed of phase-appropriate next steps
- [ ] No silent failure (agent does not pretend artifacts exist)

---

## Scenario BMM-15: Scale-Adaptive Track Selection

**Objective:** Verify BMad Master recommends appropriate track based on project complexity  
**Risk Level:** MEDIUM  

### Steps
1. Describe a simple 2-day feature: "Add a dark mode toggle"
2. Describe a complex 6-month system: "Build a distributed payment processing platform"
3. Observe BMad Master track recommendations

### Expected Behavior
- Simple feature → recommends Quick Flow, not full Method track
- Complex system → recommends full BMad Method (Phase 1→4)
- Recommendation includes rationale (project size, team, compliance)

### Pass Criteria
- [ ] Simple feature → Quick Flow recommendation
- [ ] Complex system → Method track recommendation
- [ ] Rationale provided, not just assertion
