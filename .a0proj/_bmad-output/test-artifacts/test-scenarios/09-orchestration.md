# Test Scenarios: Orchestration and Delegation

**Priority:** HIGH  
**Agent:** bmad-master (BMad Master Orchestrator)  
**Risk:** Orchestration failures mis-route users to wrong specialists or block delegation entirely  

---

## Scenario ORCH-01: BMad Master Activation and State Reading

**Objective:** Verify BMad Master reads project state on activation and presents phase-aware context  
**Risk Level:** CRITICAL  

### Steps
1. Ensure 02-bmad-state.md has `Phase: planning`
2. Activate bmad-master agent profile
3. Observe opening response

### Expected Behavior
- BMad Master reads 02-bmad-state.md from EXTRAS (auto-injected)
- Opening message references current phase: "Your project is in **planning** phase"
- Offers phase-appropriate next steps (PRD completion, UX design, readiness for solutioning)
- Does NOT default to generic welcome without phase context

### Pass Criteria
- [ ] Phase from state file mentioned in opening message
- [ ] Next steps are phase-appropriate (not generic)
- [ ] Active artifact (if any) acknowledged
- [ ] User name from 01-bmad-config.md used in greeting

---

## Scenario ORCH-02: BMad Master Routes BMM Workflows to Correct Specialists

**Objective:** Verify BMad Master delegates to correct specialist profiles for BMM work  
**Risk Level:** CRITICAL  

### Test Matrix

| User Request | Expected Delegation | Expected Profile |
|-------------|--------------------|-----------------|
| "I need to brainstorm a product idea" | call_subordinate | bmad-analyst |
| "Create a PRD for my product" | call_subordinate | bmad-pm |
| "Design the UX for this feature" | call_subordinate | bmad-ux-designer |
| "Create the technical architecture" | call_subordinate | bmad-architect |
| "Plan my next sprint" | call_subordinate | bmad-sm |
| "Implement story epic-1-1" | call_subordinate | bmad-dev |
| "I want quick flow, simple feature" | call_subordinate | bmad-quick-dev |

### Steps
For each request:
1. Ask BMad Master the request phrase
2. Observe: does BMad Master call_subordinate with correct profile?
3. Verify the subordinate receives: role description + task details

### Expected Delegation Pattern
```json
{
  "tool_name": "call_subordinate",
  "tool_args": {
    "profile": "bmad-[specialist]",
    "message": "You are [Name], [role]. [Task description with context]",
    "reset": "true"
  }
}
```

### Pass Criteria
- [ ] All 7 delegations use correct profile
- [ ] Message includes role description (not just task)
- [ ] Message includes project context (phase, existing artifacts)
- [ ] BMad Master does NOT attempt to execute BMM workflows directly
- [ ] `reset: true` on first delegation to specialist

---

## Scenario ORCH-03: BMad Master Routes TEA Workflows to Murat

**Objective:** Verify BMad Master delegates testing work to bmad-test-architect  
**Risk Level:** HIGH  

### Steps
1. Ask BMad Master: "I need to design a test strategy for my API"
2. Ask BMad Master: "Set up ATDD for my current sprint stories"
3. Ask BMad Master: "Review my existing test suite"

### Expected Behavior
- All testing requests → call_subordinate with `profile: bmad-test-architect`
- Murat persona activates in subordinate
- Murat loads bmad-tea skill and presents TEA workflow menu

### Pass Criteria
- [ ] All testing triggers delegate to `bmad-test-architect`
- [ ] No testing triggers handled directly by BMad Master
- [ ] Subordinate receives role framing: "You are Murat, Master Test Architect"

---

## Scenario ORCH-04: BMad Master Routes CIS Workflows to Correct Creatives

**Objective:** Verify BMad Master delegates creative work to correct CIS specialists  
**Risk Level:** HIGH  

### Test Matrix

| User Request | Expected Profile |
|-------------|------------------|
| "Help me brainstorm innovation opportunities" | bmad-innovation |
| "Facilitate a brainstorming session" | bmad-brainstorming-coach |
| "Apply design thinking to this problem" | bmad-design-thinking |
| "Help me tell my product's story" | bmad-storyteller |
| "Solve this complex technical problem" | bmad-problem-solver |
| "Create a pitch deck" | bmad-presentation |

### Pass Criteria
- [ ] Each creative request routes to correct specialist profile
- [ ] Victor receives innovation work (not Carson)
- [ ] Carson receives brainstorming facilitation (not Victor)
- [ ] No CIS work handled directly by BMad Master

---

## Scenario ORCH-05: BMad Master Routes BMB Work to Builders

**Objective:** Verify BMad Master delegates builder work to correct BMB specialists  
**Risk Level:** HIGH  

### Test Matrix

| User Request | Expected Profile |
|-------------|------------------|
| "Create a new BMAD agent" | bmad-agent-builder |
| "Build a new BMAD workflow" | bmad-workflow-builder |
| "Create a new BMAD module" | bmad-module-builder |

### Pass Criteria
- [ ] Bond receives agent creation requests
- [ ] Wendy receives workflow creation requests
- [ ] Morgan receives module creation requests
- [ ] No cross-routing between builders

---

## Scenario ORCH-06: call_subordinate Message Quality

**Objective:** Verify delegation messages contain all required context for subordinates  
**Risk Level:** HIGH  

### Steps
1. Ask BMad Master: "I need a PRD for a task management mobile app"
2. Capture the exact call_subordinate message argument
3. Evaluate message quality

### Message Quality Checklist

A well-formed delegation message must include:
- [ ] **Role description:** "You are John, Product Manager..."
- [ ] **Task:** What to produce and for what purpose
- [ ] **Context:** Current project phase, existing artifacts
- [ ] **Input reference:** Any relevant existing artifacts to build on
- [ ] **Output expectation:** What the artifact should be/contain
- [ ] **Project config reference:** Point to 01-bmad-config.md for paths

### Anti-patterns to Flag
- Message is only 1 sentence (insufficient context)
- No role description (subordinate will be generic AI, not specialist)
- No project context (subordinate won't know phase/existing work)
- Message tells subordinate to "wait for instructions" (prohibited)

### Pass Criteria
- [ ] Message > 3 sentences minimum
- [ ] Role + task + context all present
- [ ] No "wait for instructions" phrase
- [ ] Subordinate successfully activates correct persona

---

## Scenario ORCH-07: Party Mode Activation (PM)

**Objective:** Verify Party Mode activates multi-agent collaboration correctly  
**Risk Level:** MEDIUM  

### Steps
1. Type `PM` to any active BMAD agent
2. Observe Party Mode activation behavior
3. Verify team composition loaded
4. Trigger a collaborative task

### Expected Behavior
- Party Mode loads team config (e.g., `teams/default-party.csv` for BMM or `teams/creative-squad.yaml` for CIS)
- Multiple agent perspectives offered on the task
- Each agent responds in their own persona voice
- BMad Master coordinates the collaboration

### Team Configs to Test
| Context | Team Config File |
|---------|------------------|
| BMM context | `skills/bmad-bmm/teams/team-fullstack.yaml` |
| BMM default | `skills/bmad-bmm/teams/default-party.csv` |
| CIS creative | `skills/bmad-cis/teams/creative-squad.yaml` |
| TEA default | `skills/bmad-tea/teams/default-party.csv` |

### Pass Criteria
- [ ] Party Mode activates on `PM` command
- [ ] Team members listed with their personas
- [ ] Each team member's response is in-character
- [ ] Collaboration produces richer output than single agent

---

## Scenario ORCH-08: Dismiss Agent (DA) Behavior

**Objective:** Verify DA command returns control to BMad Master or caller  
**Risk Level:** MEDIUM  

### Steps
1. Activate specialist (e.g., bmad-pm/John)
2. Type `DA` (Dismiss Agent)
3. Observe behavior

### Expected Behavior
- Specialist acknowledges dismissal in persona voice
- Control returns to caller (BMad Master or user)
- 02-bmad-state.md Persona reverts to BMad Master (Orchestrator) or calling agent
- Active artifact preserved (not cleared)

### Pass Criteria
- [ ] DA acknowledged in specialist's voice
- [ ] Persona field in state reverts
- [ ] Active artifact preserved
- [ ] No abrupt/silent exit

---

## Scenario ORCH-09: /bmad-help Contextual Response (No Skill Load)

**Objective:** Verify /bmad-help provides contextual guidance without triggering skill load  
**Risk Level:** MEDIUM  

### Steps
1. Type `/bmad-help where do I start?` (fresh project)
2. Type `/bmad-help I have a PRD, what's next?` (planning phase)
3. Type `/bmad-help how do I create an agent?` (builder question)
4. Observe: no skills_tool:load call in any case

### Expected Behavior
- Response is immediate (no skill load delay)
- Answer references current phase from 02-bmad-state.md
- For "where do I start" → explains BMAD phases, recommends Phase 1 analysis
- For "what's next" with PRD → recommends UX design or architecture
- For agent building → references BMB module and Bond

### Pass Criteria
- [ ] Zero skills_tool:load calls for /bmad-help
- [ ] Contextually accurate phase-aware answers
- [ ] Correct next-step recommendations per phase
- [ ] Response time notably faster than workflow execution

---

## Scenario ORCH-10: Multi-Hop Delegation Chain

**Objective:** Verify BMad Master → Specialist → Sub-specialist chains work without context loss  
**Risk Level:** HIGH  

### Steps
1. Ask BMad Master: "I need a full sprint plan including stories for epic 1"
2. Observe: BMad Master delegates to Bob (SM)
3. Bob creates sprint plan
4. Bob needs story details → requests dev story from Amelia
5. Verify context preserved across 3-agent chain

### Expected Behavior
- BMad Master → Bob: sprint planning context passed
- Bob → Amelia: story specification with epic context passed
- Amelia returns story to Bob
- Bob returns sprint plan to BMad Master
- Final output coherent across all 3 agents

### Pass Criteria
- [ ] Context from original request preserved in final output
- [ ] Epic reference maintained across delegation hops
- [ ] No redundant clarification requests between agents
- [ ] Artifacts written to correct paths (implementation_artifacts not planning_artifacts)

---

## Scenario ORCH-11: BMM QA E2E Tests Workflow

**Objective:** Verify bmad-bmm qa-generate-e2e-tests workflow generates usable E2E test suite  
**Risk Level:** MEDIUM  
**Workflow path:** `skills/bmad-bmm/workflows/qa-generate-e2e-tests/`  
**Agent:** Quinn (bmad-qa)

### Steps
1. Trigger: "generate E2E tests" or via bmad-qa profile
2. Provide: feature description or user story reference
3. Execute workflow
4. Verify test output

### Expected Behavior
- Quinn (QA) persona: "pragmatic test automation, rapid coverage, ship and iterate"
- E2E tests generated in real test framework syntax (Playwright/Cypress)
- Tests follow actual user journeys (not internal implementation)
- Output to `{output_folder}/` or test-artifacts/

### Pass Criteria
- [ ] Quinn persona active (not Murat — different agents for different depths)
- [ ] E2E tests in executable syntax (not pseudocode)
- [ ] User journey tested end-to-end
- [ ] Pragmatic/quick framing (not enterprise ATDD process)

---

## Scenario ORCH-12: Agent Profile Resolution (A0 Profile Registry)

**Objective:** Verify all 20 BMAD agent profiles are registered in Agent Zero's profile registry  
**Risk Level:** CRITICAL  
**Type:** Static analysis  

### Steps
```bash
# Check Agent Zero profile registry
ls /a0/prompts/ | grep bmad
# Or check profile descriptions in agent config
cat /a0/python/helpers/call_subordinate.py 2>/dev/null | grep -A3 "bmad" | head -50
# Check prompts directory for bmad profiles
ls /a0/prompts/default/ | grep bmad 2>/dev/null
```

### Expected: All profiles present in system prompt profile list
```
bmad-master
bmad-analyst
bmad-pm
bmad-ux-designer
bmad-architect
bmad-sm
bmad-dev
bmad-quick-dev
bmad-test-architect
bmad-qa
bmad-tech-writer
bmad-innovation
bmad-design-thinking
bmad-storyteller
bmad-brainstorming-coach
bmad-presentation
bmad-problem-solver
bmad-agent-builder
bmad-workflow-builder
bmad-module-builder
```

### Pass Criteria
- [ ] All 20 profiles listed in A0 profile registry
- [ ] Profile names match directory names in agents/
- [ ] Profile descriptions accurate to agent roles
- [ ] No profiles listed that don't have corresponding agent directories
