# BMAD Method Framework — Test Strategy

**Version:** 1.0.0  
**Author:** Murat (BMAD Master Test Architect, TEA Module)  
**Date:** 2026-02-28  
**Scope:** A0 BMAD Method implementation validation against official BMAD-METHOD v6 spec  
**Project Root:** `/a0/usr/projects/a0_bmad_method/`

---

## 1. Testing Philosophy

This test strategy applies **risk-based testing** calibrated to the BMAD implementation's business impact. The A0 BMAD implementation is a platform that every downstream BMAD user depends on — persona fidelity, workflow correctness, and routing reliability are **P0 risks**.

We are NOT testing the official npm toolchain. We ARE testing **behavioral equivalence**: does the A0 implementation deliver the same BMAD METHOD outcomes via Agent Zero's skill/agent/subordinate architecture?

**Testing North Star:** A tester using official BMAD in Cursor and a user using A0 BMAD should reach equivalent artifacts, following equivalent phases, guided by equivalent specialist personas.

---

## 2. Architecture Delta: Official vs A0 Implementation

| Concern | Official BMAD-METHOD v6 | A0 BMAD Implementation |
|---------|------------------------|------------------------|
| Delivery | npm package → compiled markdown agents | skills/ + agents/ directories |
| Agent format | YAML → compiled XML/MD per IDE | A0 agent.yaml + prompt files |
| Workflow engine | Step-file sharding, HALT commands | Skill workflows loaded via skills_tool |
| Orchestration | Agent commands in IDE | call_subordinate + profile routing |
| State tracking | bmm-workflow-status.yaml + frontmatter | 02-bmad-state.md |
| Memory | _bmad/_memory/ sidecar folders | Agent Zero memory system |
| Module system | module.yaml + dependency resolver | Skills with SKILL.md routing |
| Multi-IDE | 20+ platform-specific command files | Single A0 runtime |
| Config | config.yaml per module | 01-bmad-config.md |

**Key equivalence requirements:**
- Phase gating (Analysis → Planning → Solutioning → Implementation) must be enforced
- Specialist personas must match official agent definitions
- Workflow triggers must route to correct skill workflows
- Artifacts must be written to config-defined output paths
- State transitions must update 02-bmad-state.md

---

## 3. Risk Assessment

### Risk Matrix

| Area | Business Impact | Change Frequency | Test Depth |
|------|----------------|-----------------|------------|
| BMM Phase Workflows (1-4) | CRITICAL | HIGH | Deep — all phases, all workflows |
| Quick Flow Track | CRITICAL | MEDIUM | Deep — solo dev primary path |
| Agent Persona Adherence (19 agents) | HIGH | MEDIUM | Structured sampling + key agents full |
| Skill Routing (trigger→workflow) | HIGH | HIGH | All triggers, negative cases |
| State Management (02-bmad-state.md) | HIGH | MEDIUM | All phase transitions |
| bmad-init Initialization | HIGH | LOW | Happy path + error cases |
| BMB Module (builder workflows) | MEDIUM | MEDIUM | Core workflows: agent, workflow, module |
| TEA Module (test workflows) | MEDIUM | MEDIUM | Core workflows: TF, AT, TD, RV |
| CIS Module (creative workflows) | MEDIUM | LOW | Representative sampling |
| Orchestration + Delegation | HIGH | LOW | BMad Master routing patterns |
| Config Path Resolution | HIGH | LOW | All alias resolutions |

### Risk Definitions
- **CRITICAL:** Failure blocks all BMAD users from core value delivery
- **HIGH:** Failure significantly degrades quality or user experience
- **MEDIUM:** Failure impacts specific module users or edge cases

---

## 4. Test Scope

### In Scope

1. **BMAD Initialization** (`bmad-init` skill)
   - Project workspace creation
   - Config file generation (01-bmad-config.md, 02-bmad-state.md)
   - Output directory structure

2. **BMM Module** (`bmad-bmm` skill + BMM agents)
   - Phase 1: Analysis (brainstorm, domain-research, market-research)
   - Phase 2: Planning (create-prd, create-ux-design)
   - Phase 3: Solutioning (create-architecture, create-epics, check-implementation-readiness)
   - Phase 4: Implementation (dev-story, code-review, sprint-planning, retrospective)
   - Quick Flow track (quick-spec → dev-quick-flow)
   - Document project workflow
   - Generate project context workflow

3. **BMB Module** (`bmad-bmb` skill + builder agents)
   - Create agent workflow
   - Create workflow workflow
   - Create module workflow
   - Edit/validate variants

4. **TEA Module** (`bmad-tea` skill + test architect agent)
   - All 9 TEA workflows (TF, AT, ATDD, TD, TR, NR, CI, RV, TMT)
   - Trigger phrase routing
   - Artifact output paths

5. **CIS Module** (`bmad-cis` skill + creative agents)
   - Innovation strategy workflow
   - Design thinking workflow
   - Storytelling workflow
   - Problem solving workflow
   - Brainstorming (Party Mode entry point)

6. **Agent Personas** (all 19 agents)
   - Identity: correct name, title, icon
   - Menu display: all numbered items present
   - Communication style: characteristic tone and framing
   - Workflow routing: menu selection → correct workflow load
   - Activation: correct skill loaded on startup

7. **Skill Routing**
   - All trigger phrases → correct workflow paths
   - Negative: unrecognized triggers handled gracefully
   - Multi-match disambiguation

8. **State Management**
   - 02-bmad-state.md updated after phase transitions
   - Persona field reflects active agent
   - Active artifact field reflects in-progress deliverable
   - Phase field advances correctly

9. **Orchestration Patterns**
   - BMad Master delegates to correct specialist profiles
   - Subordinate receives role description and task details
   - Party Mode (PM) activates multi-agent collaboration
   - `/bmad-help` responds contextually without skill load

10. **Path Resolution**
    - `{project-root}` resolves to `.a0proj/`
    - `{planning_artifacts}` resolves to correct absolute path
    - `{implementation_artifacts}` resolves to correct absolute path
    - `{output_folder}` resolves to correct absolute path
    - Artifacts saved to resolved paths, not relative paths

### Out of Scope
- npm CLI toolchain
- IDE-specific command file generation
- YAML compilation pipeline
- Agent Zero core framework internals
- External BMAD modules (game-dev, etc.)

---

## 5. Test Types and Layers

### Layer 1: Static Analysis (Structural)
Verify file existence, YAML validity, required fields, path references.
- **Tool:** bash/cat/python
- **Who:** Automated pre-merge checks
- **Coverage target:** 100% of agent and skill SKILL.md files

### Layer 2: Behavioral Spot Checks (Manual/Exploratory)
Activate agents, observe persona, trigger workflows, verify routing and artifact output.
- **Tool:** Agent Zero interactive session
- **Who:** Tester executing scenario scripts
- **Coverage target:** All P0/P1 scenarios, sampled P2

### Layer 3: End-to-End Workflow Runs (Integration)
Complete phase-to-phase BMAD project run — from `bmad init` through implementation artifacts.
- **Tool:** Agent Zero with test project fixture
- **Who:** Full regression runs
- **Coverage target:** BMM Method track + Quick Flow track

---

## 6. Test Execution Approach

### Setup Requirements
- Active A0 BMAD project (initialized with `bmad init`)
- 01-bmad-config.md present with valid path aliases
- 02-bmad-state.md present with phase: ready
- All skills symlinked or copied to /a0/skills/bmad-*/
- All agents symlinked or copied to /a0/agents/bmad-*/

### Execution Protocol
For each scenario:
1. Record **preconditions** (state before test)
2. Execute **steps** exactly as written
3. Capture **actual behavior** (agent response, files created, state changes)
4. Compare against **expected behavior**
5. Record **PASS / FAIL / PARTIAL** with evidence
6. For failures: capture full agent response for triage

### Regression Strategy
After any change to agents/ or skills/: re-run all CRITICAL and HIGH scenarios.
After config changes only: re-run path resolution and state management scenarios.

---

## 7. Test Artifacts Structure

```
test-artifacts/
├── test-strategy.md              ← This file
├── test-checklist.md             ← Quick pass/fail verification matrix
└── test-scenarios/
    ├── 01-bmad-init.md           ← Initialization scenarios
    ├── 02-bmm-module.md          ← BMM phase workflows
    ├── 03-bmb-module.md          ← Builder module scenarios
    ├── 04-tea-module.md          ← Testing module scenarios
    ├── 05-cis-module.md          ← Creative suite scenarios
    ├── 06-agent-personas.md      ← All 19 agent persona tests
    ├── 07-skill-routing.md       ← Trigger → workflow routing
    ├── 08-state-management.md    ← 02-bmad-state.md transitions
    └── 09-orchestration.md       ← Delegation and party mode
```

---

## 8. Definition of Done

The A0 BMAD implementation is **ready for production** when:

- [ ] All CRITICAL scenarios: 100% PASS
- [ ] All HIGH scenarios: ≥ 90% PASS
- [ ] All MEDIUM scenarios: ≥ 75% PASS
- [ ] Zero persona identity failures (wrong name, wrong role, wrong module)
- [ ] Zero skill routing failures on documented trigger phrases
- [ ] Zero path resolution failures (artifacts in wrong locations)
- [ ] State management: all phase transitions update 02-bmad-state.md
- [ ] Full BMM Method track E2E run completes without blocking failures
- [ ] Quick Flow track E2E run completes without blocking failures

---

## 9. Known Risks and Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| LLM non-determinism in persona tests | HIGH | Test 3 runs, accept 2/3 PASS |
| Workflow step content changes invalidate tests | MEDIUM | Test behavior/outcome, not exact text |
| Skill load failure (symlink issues) | LOW | Pre-flight: verify all skills load via skills_tool:list |
| State file not updated after workflow | MEDIUM | Explicit state check step in every workflow scenario |
| Path alias resolution regression | LOW | Static analysis check on every config change |

---

*Murat, BMAD TEA — Test artifacts generated 2026-02-28*
