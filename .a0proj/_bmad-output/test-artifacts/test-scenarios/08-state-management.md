# Test Scenarios: State Management (02-bmad-state.md)

**Priority:** HIGH  
**State file:** `.a0proj/instructions/02-bmad-state.md`  
**Risk:** State corruption causes phase confusion, wrong workflow routing, and lost work context  

---

## Scenario STATE-01: Initial State File Structure

**Objective:** Verify 02-bmad-state.md has correct initial state post-init  
**Risk Level:** CRITICAL  

### Steps
```bash
cat /a0/usr/projects/a0_bmad_method/.a0proj/instructions/02-bmad-state.md
```

### Expected Structure
```markdown
## BMAD Active State
- Phase: ready
- Persona: BMad Master (Orchestrator)
- Active Artifact: none

### Session Context
...
```

### Required Fields
| Field | Required Values | Notes |
|-------|----------------|-------|
| Phase | ready / analysis / planning / solutioning / implementation | Must be one of these |
| Persona | Agent name from the 20 BMAD agents | Must match active agent |
| Active Artifact | none / filename.md | "none" when no workflow active |

### Pass Criteria
- [ ] `Phase: ready` on fresh init
- [ ] `Persona: BMad Master` on fresh init
- [ ] `Active Artifact: none` on fresh init
- [ ] File is valid Markdown (no syntax errors)
- [ ] File is auto-injected into agent system prompt (appears in EXTRAS)

---

## Scenario STATE-02: Phase Transition — Ready → Analysis

**Objective:** Verify state updates when Phase 1 analysis workflow starts  
**Risk Level:** HIGH  

### Steps
1. Start with `Phase: ready`
2. Trigger brainstorm workflow ("brainstorm project [idea]")
3. Execute through first step of brainstorm
4. Read 02-bmad-state.md

### Expected State After
```markdown
- Phase: analysis
- Persona: Mary (Business Analyst)  
- Active Artifact: brainstorm-[name]-[date].md
```

### Pass Criteria
- [ ] Phase updated from `ready` to `analysis`
- [ ] Persona updated to the active analyst agent
- [ ] Active Artifact set to the in-progress brainstorm file
- [ ] State update happens BEFORE workflow completion (not just at end)

---

## Scenario STATE-03: Phase Transition — Analysis → Planning

**Objective:** Verify state updates when Phase 2 planning workflow starts  
**Risk Level:** HIGH  

### Steps
1. Start with `Phase: analysis`
2. Trigger PRD creation workflow
3. Execute through first step
4. Read 02-bmad-state.md

### Expected State After
```markdown
- Phase: planning
- Persona: John (Product Manager)
- Active Artifact: prd.md
```

### Pass Criteria
- [ ] Phase updated to `planning`
- [ ] Persona updated to John (PM)
- [ ] Active Artifact = `prd.md`
- [ ] Previous analysis phase context preserved in Session Context section

---

## Scenario STATE-04: Phase Transition — Planning → Solutioning

**Objective:** Verify state updates when Phase 3 solutioning workflow starts  
**Risk Level:** HIGH  

### Steps
1. Start with `Phase: planning`
2. Trigger architecture creation
3. Execute through first step
4. Read 02-bmad-state.md

### Expected State After
```markdown
- Phase: solutioning
- Persona: Winston (Architect)
- Active Artifact: architecture.md
```

### Pass Criteria
- [ ] Phase updated to `solutioning`
- [ ] Persona updated to Winston (Architect)
- [ ] Previous phases not erased from state history

---

## Scenario STATE-05: Phase Transition — Solutioning → Implementation

**Objective:** Verify state updates when Phase 4 implementation workflow starts  
**Risk Level:** HIGH  

### Steps
1. Start with `Phase: solutioning`
2. Trigger dev story workflow
3. Execute through first step
4. Read 02-bmad-state.md

### Expected State After
```markdown
- Phase: implementation
- Persona: Amelia (Developer Agent)
- Active Artifact: epic-1-1-story.md
```

### Pass Criteria
- [ ] Phase updated to `implementation`
- [ ] Artifact points to specific story file (not generic)
- [ ] Implementation artifacts path used (not planning_artifacts)

---

## Scenario STATE-06: Quick Flow State Path

**Objective:** Verify Quick Flow track sets appropriate state (skips analysis/planning/solutioning)  
**Risk Level:** HIGH  

### Steps
1. Start with `Phase: ready`
2. Trigger Quick Flow: "quick flow [feature]"
3. Read state after quick-spec step

### Expected State After Quick Spec
```markdown
- Phase: implementation  
- Persona: Barry (Quick Flow Solo Dev)
- Active Artifact: tech-spec-[name].md
```

### Pass Criteria
- [ ] Phase jumps directly to `implementation` (skips analysis, planning, solutioning)
- [ ] Barry persona active (not John/Winston)
- [ ] No artificial phase history for skipped phases

---

## Scenario STATE-07: Persona Field Updates Correctly Per Agent

**Objective:** Verify Persona field accurately reflects which specialist is active  
**Risk Level:** HIGH  

### Test Matrix

| Activated Agent Profile | Expected Persona Value |
|------------------------|------------------------|
| bmad-master | BMad Master (Orchestrator) |
| bmad-analyst | Mary (Business Analyst) |
| bmad-pm | John (Product Manager) |
| bmad-ux-designer | Sally (UX Designer) |
| bmad-architect | Winston (Architect) |
| bmad-sm | Bob (Scrum Master) |
| bmad-dev | Amelia (Developer Agent) |
| bmad-quick-dev | Barry (Quick Flow Solo Dev) |
| bmad-test-architect | Murat (Master Test Architect) |
| bmad-innovation | Victor (Disruptive Innovation Oracle) |
| bmad-agent-builder | Bond (Agent Building Expert) |

### Steps
For each agent:
1. Activate agent profile
2. Trigger a workflow that updates state
3. Verify Persona field in 02-bmad-state.md

### Pass Criteria
- [ ] Persona field matches expected value for each agent
- [ ] No persona bleeds between agents (Mary never shows when Winston should be active)
- [ ] Persona cleared to BMad Master on DA (Dismiss Agent)

---

## Scenario STATE-08: Active Artifact Field Lifecycle

**Objective:** Verify Active Artifact set on start, persists during, clears on completion  
**Risk Level:** HIGH  

### Steps
1. Note initial state: `Active Artifact: none`
2. Start PRD creation workflow
3. Mid-workflow: verify Active Artifact = `prd.md` (or in-progress marker)
4. Complete PRD workflow
5. Verify Active Artifact = `prd.md` (completed artifact reference)
6. Start new architecture workflow
7. Verify Active Artifact updates to `architecture.md`

### Expected Lifecycle
```
none → [workflow starts] → in-progress artifact name → [workflow completes] → completed artifact name
```

### Pass Criteria
- [ ] Active Artifact updates when workflow starts
- [ ] Active Artifact NOT cleared to `none` mid-workflow
- [ ] Active Artifact updates to new artifact when next workflow begins
- [ ] Artifact path (not just filename) usable to locate the file

---

## Scenario STATE-09: State Persistence Across Sessions

**Objective:** Verify 02-bmad-state.md persists phase/persona across Agent Zero restarts  
**Risk Level:** CRITICAL  

### Steps
1. Set state to `Phase: planning`, `Active Artifact: prd.md` by running PRD workflow
2. Simulate session end (new conversation / agent restart)
3. Activate BMad Master in new session
4. Verify BMad Master reads and reports correct phase

### Expected Behavior
- New session reads 02-bmad-state.md (auto-injected via EXTRAS)
- BMad Master reports: "Project is currently in planning phase with prd.md as active artifact"
- Workflows offered are appropriate for planning phase

### Pass Criteria
- [ ] Phase preserved across sessions
- [ ] Active Artifact preserved across sessions
- [ ] BMad Master reads and uses state in opening message
- [ ] No reset to `phase: ready` on new session

---

## Scenario STATE-10: State File Format Validation

**Objective:** Verify state file is always valid Markdown that can be parsed by agents  
**Risk Level:** HIGH  

### Steps
After each workflow run, execute:
```bash
cat /a0/usr/projects/a0_bmad_method/.a0proj/instructions/02-bmad-state.md
```
Verify:
1. Markdown heading structure intact
2. Phase field: exactly one value, valid phase name
3. Persona field: not empty, not "undefined"
4. Active Artifact field: present
5. Session Context section: present and non-empty

### Pass Criteria
- [ ] Phase is ALWAYS one of: ready, analysis, planning, solutioning, implementation
- [ ] Persona is ALWAYS a recognized BMAD agent name
- [ ] No raw JSON/YAML artifacts written to state file
- [ ] File remains valid Markdown after 10+ state updates

---

## Scenario STATE-11: State-Aware Workflow Routing

**Objective:** Verify agents use state to provide context-appropriate guidance  
**Risk Level:** HIGH  

### Steps
1. Set state to `Phase: solutioning`
2. Ask BMad Master: "What should I do next?"
3. Set state to `Phase: analysis`
4. Ask BMad Master: "What should I do next?"

### Expected Behavior
- Solutioning phase: suggests architecture completion, epics creation, readiness check
- Analysis phase: suggests completing analysis, moving to PRD
- Responses are phase-specific — not generic

### Pass Criteria
- [ ] BMad Master reads phase from state before answering
- [ ] Phase-appropriate next steps recommended
- [ ] No Phase 4 suggestions when in Phase 1
- [ ] No Phase 1 re-work suggestions when in Phase 3
