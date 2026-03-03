# BMAD Method Framework — Test Checklist

**Version:** 1.0.0  
**Author:** Murat, BMAD TEA Module  
**Usage:** Run pre-merge, after any agent/skill change, and before release  
**Time to complete:** ~45 min full run / ~10 min smoke run (★ items only)  

**Legend:** ★ = Smoke test (run always) | C = Critical | H = High | M = Medium  
**Result:** ✅ PASS | ❌ FAIL | ⏭ SKIP | ⚠️ PARTIAL  

---

## 0. PRE-FLIGHT (Run Before Everything Else)

| # | Check | Risk | Result | Notes |
|---|-------|------|--------|-------|
| P01 ★ | All 5 skill symlinks exist and are not broken | C | | `ls -la /a0/skills/ \| grep bmad` |
| P02 ★ | All 5 SKILL.md files accessible | C | | `for s in bmad-tea bmad-bmm bmad-bmb bmad-cis bmad-init; do [ -f /a0/skills/$s/SKILL.md ] && echo OK; done` |
| P03 ★ | All 20 agent directories exist under /a0/agents/bmad-* | C | | `ls /a0/agents/ \| grep -c bmad` → 20 |
| P04 ★ | 01-bmad-config.md present and readable | C | | `cat .a0proj/instructions/01-bmad-config.md` |
| P05 ★ | 02-bmad-state.md present with valid phase | C | | Phase must be one of: ready/analysis/planning/solutioning/implementation |
| P06 | skills.py uses os.walk(followlinks=True) | C | | `grep -n "followlinks" /a0/python/helpers/skills.py` |
| P07 | All 20 agent.yaml files parseable | H | | No YAML syntax errors |
| P08 | All 20 agents have 4 required prompt files | H | | See PERSONA-01 verification command |

---

## 1. INITIALIZATION (bmad-init)

| # | Check | Risk | Result | Notes |
|---|-------|------|--------|-------|
| I01 ★ | `bmad init` creates .a0proj/ directory tree | C | | Scenario INIT-01 |
| I02 ★ | 01-bmad-config.md written with all 5 path aliases | C | | {project-root}, {planning_artifacts}, {implementation_artifacts}, {output_folder}, {product_knowledge} |
| I03 ★ | All path aliases are absolute paths (start with /) | C | | No relative path aliases |
| I04 ★ | 02-bmad-state.md written: phase=ready, persona=BMad Master | C | | Scenario INIT-01 |
| I05 | All output subdirs created: planning-artifacts/, implementation-artifacts/, test-artifacts/ | H | | Scenario INIT-01 |
| I06 | Re-init on existing project does NOT overwrite state | H | | Scenario INIT-03 |
| I07 | /bmad-help responds without loading any skill | M | | Scenario INIT-04 |
| I08 | agent-manifest.csv lists all 20 agents | M | | Scenario INIT-05 |
| I09 | workflow-manifest.csv covers all major workflow areas | M | | Scenario INIT-05 |

---

## 2. BMM MODULE — PHASES AND WORKFLOWS

### Phase 1 — Analysis
| # | Check | Risk | Result | Notes |
|---|-------|------|--------|-------|
| B01 ★ | bmad-bmm skill loads without error | C | | Scenario BMM-01 |
| B02 | Brainstorm workflow executes through all steps | H | | Scenario BMM-02 |
| B03 | Brainstorm artifact written to planning_artifacts/ | H | | Absolute path, not relative |
| B04 | Domain research workflow produces structured artifact | H | | Scenario BMM-03 |
| B05 | State updated to phase=analysis after Phase 1 start | H | | State file check |

### Phase 2 — Planning
| # | Check | Risk | Result | Notes |
|---|-------|------|--------|-------|
| B06 ★ | PRD workflow loads and all steps execute | C | | Scenario BMM-04 |
| B07 ★ | PRD contains all required sections (goals, requirements, NFRs, metrics) | C | | Scenario BMM-04 |
| B08 ★ | PRD saved as planning_artifacts/prd.md | C | | Absolute path |
| B09 | State updated to phase=planning, persona=John | H | | Scenario STATE-03 |
| B10 | UX design workflow produces UX spec artifact | H | | Scenario BMM-05 |

### Phase 3 — Solutioning
| # | Check | Risk | Result | Notes |
|---|-------|------|--------|-------|
| B11 ★ | Architecture workflow loads and executes | C | | Scenario BMM-06 |
| B12 ★ | Architecture document contains all required sections | C | | System overview, tech stack, ADRs |
| B13 ★ | Architecture saved to planning_artifacts/architecture.md | C | | Absolute path |
| B14 | State updated to phase=solutioning, persona=Winston | H | | |
| B15 | Epics workflow decomposes PRD into user stories | H | | Scenario BMM-07 |
| B16 | User stories in correct format (As a/I want/So that) | H | | |
| B17 | Acceptance criteria present on every story | H | | |
| B18 | Implementation readiness check validates all artifacts | H | | Scenario BMM-08 |
| B19 | Readiness report gives READY/NOT READY recommendation | H | | |

### Phase 4 — Implementation
| # | Check | Risk | Result | Notes |
|---|-------|------|--------|-------|
| B20 ★ | Dev story workflow produces implementation-ready story | C | | Scenario BMM-09 |
| B21 ★ | Story saved to implementation_artifacts/ (NOT planning_artifacts/) | C | | Path segregation critical |
| B22 | DoD checklist present in story file | H | | |
| B23 | State updated to phase=implementation, persona=Amelia | H | | |
| B24 | Sprint planning produces sprint-status.yaml | H | | Scenario BMM-10 |

### Quick Flow Track
| # | Check | Risk | Result | Notes |
|---|-------|------|--------|-------|
| B25 ★ | Quick flow bypasses Phase 1-3 ceremony | C | | Scenario BMM-11 |
| B26 ★ | Barry persona active (not John/Winston/Amelia) | C | | |
| B27 | Phase jumps directly to implementation | H | | No artificial phase history |
| B28 | Tech spec created before implementation starts | H | | |

### Utility Workflows
| # | Check | Risk | Result | Notes |
|---|-------|------|--------|-------|
| B29 | Document project workflow creates docs at output_folder | M | | Scenario BMM-12 |
| B30 | Generate project context creates project-context.md | M | | Scenario BMM-13 |
| B31 | Phase gating warns on missing prerequisites | H | | Scenario BMM-14 |
| B32 | BMad Master recommends Quick Flow for simple features | M | | Scenario BMM-15 |
| B33 | BMad Master recommends Method track for complex systems | M | | Scenario BMM-15 |

---

## 3. BMB MODULE — BUILDER

| # | Check | Risk | Result | Notes |
|---|-------|------|--------|-------|
| MB01 ★ | bmad-bmb skill loads, all 3 workflow areas present | H | | Scenario BMB-01 |
| MB02 ★ | Create agent workflow generates all required files | H | | agent.yaml + _context.md + 4 prompts |
| MB03 | Generated agent.yaml has name/title/description fields | H | | Scenario BMB-02 |
| MB04 | Generated agent follows same structure as existing bmad-* | H | | |
| MB05 | Edit agent workflow modifies only targeted fields | M | | Scenario BMB-03 |
| MB06 | Validate agent catches missing files | M | | Scenario BMB-04 |
| MB07 | Create workflow generates steps-c/steps-e/steps-v structure | H | | Scenario BMB-05 |
| MB08 | Generated workflow.yaml has triggers and step references | H | | |
| MB09 | Create module generates SKILL.md with routing table | M | | Scenario BMB-06 |

---

## 4. TEA MODULE — TESTING

| # | Check | Risk | Result | Notes |
|---|-------|------|--------|-------|
| T01 ★ | bmad-tea skill loads, all 9 workflow triggers present | C | | Scenario TEA-01 |
| T02 ★ | Murat menu shows 9 numbered items on activation | C | | Scenario TEA-02 |
| T03 ★ | Menu STOPS after display — no auto-execute | C | | Scenario TEA-02 |
| T04 ★ | ATDD workflow generates failing API + E2E tests | C | | Scenario TEA-03 |
| T05 | ATDD output includes implementation checklist | H | | |
| T06 | ATDD artifact at test-artifacts/ with date stamp | H | | |
| T07 | Test framework workflow recommends with rationale | H | | Scenario TEA-04 |
| T08 | Test automation generates risk-prioritized test suite | H | | Scenario TEA-05 |
| T09 | Test design produces risk matrix + coverage plan | H | | Scenario TEA-06 |
| T10 | Trace workflow produces SHIP/HOLD gate decision | H | | Scenario TEA-07 |
| T11 | NFR assessment covers all 4 dimensions | M | | Scenario TEA-08 |
| T12 | CI workflow generates valid pipeline YAML | H | | Scenario TEA-09 |
| T13 | Test review identifies anti-patterns with remediation | H | | Scenario TEA-10 |
| T14 | TMT shows 7-session curriculum | M | | Scenario TEA-11 |
| T15 | All step files execute sequentially (steps-c order) | H | | Scenario TEA-13 |
| T16 | Knowledge base files accessible during workflows | M | | Scenario TEA-12 |

---

## 5. CIS MODULE — CREATIVE

| # | Check | Risk | Result | Notes |
|---|-------|------|--------|-------|
| C01 ★ | bmad-cis skill loads, all 4 workflow triggers present | H | | Scenario CIS-01 |
| C02 | Victor delivers JTBD + Blue Ocean analysis | H | | Scenario CIS-02 |
| C03 | Victor framing is disruptive (not incremental) | H | | |
| C04 | Maya applies all 5 design thinking stages | H | | Scenario CIS-03 |
| C05 | Sophia applies named storytelling framework | M | | Scenario CIS-04 |
| C06 | Dr. Quinn identifies root cause (not just symptoms) | H | | Scenario CIS-05 |
| C07 | Carson applies named brainstorming technique | M | | Scenario CIS-06 |
| C08 | Caravaggio assigns purpose to each frame | M | | Scenario CIS-07 |
| C09 | creative-squad.yaml is valid YAML | M | | Scenario CIS-08 |

---

## 6. AGENT PERSONAS (20 Agents)

| # | Check | Risk | Result | Notes |
|---|-------|------|--------|-------|
| A01 ★ | All 20 agent directories have required file structure | C | | Scenario PERSONA-01 script |
| A02 ★ | All 20 agent.yaml have name/title/description | H | | Scenario PERSONA-02 |
| A03 ★ | No agent.yaml has empty or missing name field | C | | |
| A04 ★ | BMad Master self-identifies as orchestrator (not specialist) | C | | Scenario PERSONA-03 |
| A05 ★ | Mary (Analyst) self-identifies correctly | H | | Scenario PERSONA-04 |
| A06 ★ | John (PM) exhibits WHY-focused communication | H | | Scenario PERSONA-05 |
| A07 ★ | Winston (Architect) ties decisions to business value | H | | Scenario PERSONA-06 |
| A08 ★ | Amelia (Dev) exhibits TDD-first framing | H | | Scenario PERSONA-07 |
| A09 ★ | Barry (Quick Dev) exhibits efficiency/lean framing | H | | Scenario PERSONA-08 |
| A10 | Murat self-identifies with 🧪 icon, risk-calibrated framing | H | | Scenario PERSONA-10 |
| A11 | Victor uses disruptive innovation framing | M | | Scenario PERSONA-11 |
| A12 | Bond references BMAD compliance in agent building | H | | Scenario PERSONA-12 |
| A13 | All remaining 8 agents: name check passes | M | | Scenario PERSONA-13 |
| A14 | No agent uses "I am an AI assistant" identity evasion | H | | Scenario PERSONA-14 |
| A15 | Specialists redirect out-of-scope work correctly | H | | Scenario PERSONA-14 |

---

## 7. SKILL ROUTING

| # | Check | Risk | Result | Notes |
|---|-------|------|--------|-------|
| R01 ★ | All 5 SKILL.md files have trigger entries | C | | Scenario ROUTE-01 |
| R02 ★ | Workflow paths use {skill-dir}/ prefix (no hardcoded paths) | C | | |
| R03 ★ | "create PRD" → bmad-bmm + create-prd/ workflow | C | | Scenario ROUTE-02 |
| R04 ★ | "dev story" → bmad-bmm + 4-implementation/dev-story/ | C | | |
| R05 ★ | "quick flow" → bmad-bmm + bmad-quick-flow/ | C | | |
| R06 ★ | "ATDD" → bmad-tea + testarch/atdd/ | C | | Scenario ROUTE-03 |
| R07 ★ | "test review" → bmad-tea + testarch/test-review/ | C | | |
| R08 | All 9 TEA triggers route to distinct correct workflows | C | | Scenario ROUTE-03 full matrix |
| R09 | All BMB triggers route to correct builder area | H | | Scenario ROUTE-04 |
| R10 | All CIS triggers route to correct creative workflow | H | | Scenario ROUTE-05 |
| R11 | "bmad init" triggers load bmad-init skill | H | | Scenario ROUTE-06 |
| R12 | Ambiguous triggers prompt clarification (no auto-execute) | H | | Scenario ROUTE-07 |
| R13 | Murat rejects "create PRD" (cross-skill boundary) | H | | Scenario ROUTE-08 |
| R14 | John rejects "test design" (cross-skill boundary) | H | | Scenario ROUTE-08 |
| R15 | All 5 skill symlinks resolve correctly at runtime | C | | Scenario ROUTE-09 |

---

## 8. STATE MANAGEMENT

| # | Check | Risk | Result | Notes |
|---|-------|------|--------|-------|
| S01 ★ | Initial state: phase=ready, persona=BMad Master, artifact=none | C | | Scenario STATE-01 |
| S02 ★ | State file has all 3 required fields (Phase, Persona, Active Artifact) | C | | |
| S03 ★ | Phase transitions: ready→analysis when Phase 1 starts | C | | Scenario STATE-02 |
| S04 ★ | Phase transitions: analysis→planning when PRD starts | C | | Scenario STATE-03 |
| S05 ★ | Phase transitions: planning→solutioning when arch starts | C | | Scenario STATE-04 |
| S06 ★ | Phase transitions: solutioning→implementation when story starts | C | | Scenario STATE-05 |
| S07 ★ | Quick Flow: phase jumps directly to implementation | C | | Scenario STATE-06 |
| S08 | Persona field updates to correct agent on activation | H | | Scenario STATE-07 full matrix |
| S09 | Active Artifact updates when workflow starts | H | | Scenario STATE-08 |
| S10 | Active Artifact not cleared mid-workflow | H | | |
| S11 | State persists across session restarts | C | | Scenario STATE-09 |
| S12 | Phase value is ALWAYS one of 5 valid values | C | | Scenario STATE-10 |
| S13 | BMad Master reads state to provide phase-aware guidance | H | | Scenario STATE-11 |
| S14 | DA command reverts Persona to BMad Master | M | | Scenario ORCH-08 |

---

## 9. ORCHESTRATION AND DELEGATION

| # | Check | Risk | Result | Notes |
|---|-------|------|--------|-------|
| O01 ★ | BMad Master greets with phase context from state file | C | | Scenario ORCH-01 |
| O02 ★ | "create PRD" → BMad Master delegates to bmad-pm | C | | Scenario ORCH-02 |
| O03 ★ | "test strategy" → BMad Master delegates to bmad-test-architect | C | | Scenario ORCH-03 |
| O04 ★ | "create architecture" → BMad Master delegates to bmad-architect | C | | Scenario ORCH-02 |
| O05 ★ | Delegation message includes role + task + project context | C | | Scenario ORCH-06 |
| O06 ★ | No delegation message uses "wait for instructions" | C | | Anti-pattern check |
| O07 | Innovation → Victor, brainstorm → Carson (not swapped) | H | | Scenario ORCH-04 |
| O08 | Agent → Bond, Workflow → Wendy, Module → Morgan | H | | Scenario ORCH-05 |
| O09 | BMad Master does NOT execute BMM workflows directly | H | | Should always delegate |
| O10 | PM command activates Party Mode with team roster | M | | Scenario ORCH-07 |
| O11 | Team config files are valid (fullstack.yaml, creative-squad.yaml) | M | | |
| O12 | DA command handled gracefully in specialist's voice | M | | Scenario ORCH-08 |
| O13 | /bmad-help triggers NO skills_tool:load | H | | Scenario ORCH-09 |
| O14 | Multi-hop delegation preserves context (BMad→SM→Dev) | H | | Scenario ORCH-10 |
| O15 | Quinn (QA) handles qa-generate-e2e-tests workflow | M | | Scenario ORCH-11 |
| O16 | All 20 BMAD profiles present in A0 profile registry | C | | Scenario ORCH-12 |

---

## DEFINITION OF DONE — RELEASE GATE

| Gate | Threshold | Status |
|------|-----------|--------|
| All CRITICAL checks (★ + C) | 100% PASS | ☐ |
| All HIGH checks | ≥ 90% PASS | ☐ |
| All MEDIUM checks | ≥ 75% PASS | ☐ |
| Zero persona identity failures | 0 failures | ☐ |
| Zero skill routing failures | 0 failures | ☐ |
| Zero path resolution failures | 0 failures | ☐ |
| State management: all phase transitions update state | 100% | ☐ |
| Full BMM Method track E2E (Phase 1→4) completes | No blocking failures | ☐ |
| Quick Flow track E2E completes | No blocking failures | ☐ |

**RELEASE DECISION:** ☐ SHIP — all gates passed | ☐ HOLD — gate failures present

---

## REGRESSION RUN LOG

| Date | Runner | Scope | C Pass | H Pass | M Pass | Decision | Failures |
|------|--------|-------|--------|--------|--------|----------|----------|
| | | | | | | | |

---
*Murat, BMAD TEA — Checklist v1.0.0 — 2026-02-28*
