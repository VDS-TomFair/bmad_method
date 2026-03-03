# Test Scenarios: BMB Module (BMAD Builder Module)

**Priority:** MEDIUM-HIGH  
**Skill:** `bmad-bmb`  
**Agents:** bmad-agent-builder (Bond), bmad-workflow-builder (Wendy), bmad-module-builder (Morgan)  
**Workflow paths:** `skills/bmad-bmb/workflows/agent/`, `workflows/workflow/`, `workflows/module/`  
**Risk:** BMB is the BMAD meta-layer — failures here block framework extensibility  

---

## Scenario BMB-01: Skill Load and Workflow Menu

**Objective:** Verify bmad-bmb skill loads and exposes all 3 builder workflow areas  
**Risk Level:** HIGH  

### Steps
1. Trigger: "create agent" or "bmad builder"
2. Observe `skills_tool:load` for `bmad-bmb`
3. Verify SKILL.md exposes: agent/, workflow/, module/ workflow groups

### Expected Behavior
- Skill loads without error
- Three builder domains visible: Agent Building, Workflow Building, Module Creation
- Trigger phrases enumerated for each domain

### Pass Criteria
- [ ] Skill loads cleanly
- [ ] All 3 workflow areas present in SKILL.md routing table
- [ ] Bond, Wendy, Morgan agent profiles listed

---

## Scenario BMB-02: Create Agent Workflow

**Objective:** Verify new BMAD agent creation workflow produces a valid agent definition  
**Risk Level:** HIGH  
**Workflow path:** `skills/bmad-bmb/workflows/agent/`  
**Agent:** Bond (bmad-agent-builder)

### Steps
1. Trigger: "create agent" or "new agent"
2. Bond (agent builder) persona activates
3. Provide sample agent spec: name="Legal Analyst", role="Contract review specialist", module="Custom"
4. Execute workflow to completion
5. Verify output artifact

### Expected Behavior
- Bond persona: "master agent architect, BMAD Core compliance, best practices"
- Workflow collects: agent name, title, role description, communication style, menu items, workflow triggers
- Output artifact is a valid A0 BMAD agent structure:
  ```
  agents/legal-analyst/
  ├── agent.yaml
  ├── _context.md
  └── prompts/
      ├── agent.system.main.role.md
      ├── agent.system.main.communication.md
      ├── agent.system.main.communication_additions.md
      └── agent.system.main.tips.md
  ```
- agent.yaml contains required fields: name, title, description
- role.md defines specialist identity
- Output saved to `{output_folder}/` or specified path

### Pass Criteria
- [ ] Bond persona characteristics present
- [ ] All required agent files generated (agent.yaml + 4 prompt files)
- [ ] agent.yaml is valid YAML with required fields
- [ ] Generated agent follows same structure as existing bmad-* agents
- [ ] DoD checklist provided at workflow end

---

## Scenario BMB-03: Edit Existing Agent Workflow

**Objective:** Verify agent edit workflow modifies only specified fields without breaking structure  
**Risk Level:** MEDIUM  
**Workflow path:** `skills/bmad-bmb/workflows/agent/`  

### Steps
1. Trigger: "edit agent" with an existing agent as target (e.g., bmad-analyst)
2. Request: update communication style
3. Execute edit workflow
4. Verify only targeted changes applied

### Expected Behavior
- Bond asks which fields to modify
- Targeted edit applied (deep-merge style)
- Untouched fields preserved
- Validation confirms BMAD compliance post-edit

### Pass Criteria
- [ ] Only modified fields changed
- [ ] Agent structure still valid after edit
- [ ] Bond validates BMAD compliance

---

## Scenario BMB-04: Validate Agent Workflow

**Objective:** Verify agent validation catches compliance issues  
**Risk Level:** MEDIUM  
**Workflow path:** `skills/bmad-bmb/workflows/agent/`  

### Steps
1. Trigger: "validate agent" pointing to an agent directory
2. Execute validation on `agents/bmad-pm/`
3. Also test with a deliberately incomplete agent (missing prompts/ files)

### Expected Behavior
- Valid agent: passes all checks, summary confirms compliance
- Invalid agent: specific failures identified:
  - Missing agent.yaml fields
  - Missing prompt files
  - Incorrect BMAD naming conventions
  - Missing `_context.md`

### Pass Criteria
- [ ] Valid agent passes without false positives
- [ ] Invalid agent: all issues enumerated with remediation guidance
- [ ] Validation references BMAD agent standards

---

## Scenario BMB-05: Create Workflow Workflow

**Objective:** Verify workflow creation produces BMAD-compliant step-file workflow structure  
**Risk Level:** HIGH  
**Workflow path:** `skills/bmad-bmb/workflows/workflow/`  
**Agent:** Wendy (bmad-workflow-builder)

### Steps
1. Trigger: "create workflow" or "new workflow"
2. Provide: workflow name="legal-review", purpose="Review contracts for compliance issues", steps=3
3. Execute workflow
4. Verify output

### Expected Behavior
- Wendy persona: "master workflow architect, process design, state management"
- Generated workflow structure matches TEA/BMM pattern:
  ```
  workflow-name/
  ├── workflow.yaml
  ├── workflow.md
  ├── workflow-plan.md
  ├── instructions.md
  ├── checklist.md
  ├── steps-c/
  │   ├── step-01-*.md
  │   ├── step-02-*.md
  │   └── step-0N-*.md
  ├── steps-e/
  │   ├── step-01-assess.md
  │   └── step-02-apply-edit.md
  └── steps-v/
      └── step-01-validate.md
  ```
- workflow.yaml contains: triggers, output artifact path, step references
- Steps include HALT enforcement and sequential progression

### Pass Criteria
- [ ] Wendy persona active
- [ ] Three-tier step structure generated (steps-c, steps-e, steps-v)
- [ ] workflow.yaml valid with trigger phrases
- [ ] Steps reference next step for chaining
- [ ] HALT pattern present in step files

---

## Scenario BMB-06: Create Module Workflow

**Objective:** Verify module creation produces a complete BMAD module with agents and workflows  
**Risk Level:** MEDIUM  
**Workflow path:** `skills/bmad-bmb/workflows/module/`  
**Agent:** Morgan (bmad-module-builder)

### Steps
1. Trigger: "create module" or "new module"
2. Provide: module name="legal", domain="Legal tech for contract analysis"
3. Execute workflow (may be multi-step)
4. Verify output structure

### Expected Behavior
- Morgan persona: "comprehensive BMAD Core knowledge, cohesive scalable modules"
- Module output contains:
  - SKILL.md with trigger routing
  - config.yaml with module settings
  - agents/ with at least one specialist agent
  - workflows/ with at least one workflow
  - module-help.csv
- Module follows same structure as `skills/bmad-bmm/`, `skills/bmad-tea/`

### Pass Criteria
- [ ] Morgan persona active
- [ ] Complete module scaffold generated
- [ ] SKILL.md present with routing table
- [ ] At least one agent definition generated
- [ ] Module installable into Agent Zero skills/ directory
