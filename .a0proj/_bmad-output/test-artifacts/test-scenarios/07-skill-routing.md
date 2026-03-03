# Test Scenarios: Skill Routing (Trigger → Workflow Mapping)

**Priority:** HIGH  
**Risk:** Routing failures silently send users to wrong workflows — trust-destroying and hard to diagnose  
**Type:** Trigger phrase coverage + negative case testing  

---

## Scenario ROUTE-01: Static Routing Table Completeness Check

**Objective:** Verify all 5 SKILL.md files contain complete routing tables  
**Risk Level:** CRITICAL  
**Type:** Static analysis  

### Steps
```bash
for skill in /a0/skills/bmad-*/; do
  echo "=== ${skill} ==="
  grep -c "Triggers:\|\*\*Triggers\|triggers:" "${skill}SKILL.md" 2>/dev/null || echo "NO TRIGGER ENTRIES"
done
```

### Expected: Each SKILL.md contains

| Skill | Min Trigger Groups | Key Trigger Phrases |
|-------|-------------------|--------------------|
| bmad-bmm | 10+ | "create PRD", "brainstorm", "create architecture", "dev story", "sprint planning", "quick flow" |
| bmad-bmb | 6+ | "create agent", "edit agent", "validate agent", "create workflow", "create module" |
| bmad-tea | 9 | all 9 workflow triggers (see TEA-01) |
| bmad-cis | 4+ | "innovation strategy", "storytelling", "problem solving", "design thinking" |
| bmad-init | 3+ | "bmad init", "initialize bmad", "bmad help" |

### Pass Criteria
- [ ] All 5 SKILL.md files have trigger entries
- [ ] Trigger phrases are quoted strings (not vague descriptions)
- [ ] Each trigger maps to a specific workflow path (not "the workflow")
- [ ] Workflow paths use `{skill-dir}/` prefix — no hardcoded absolute paths

---

## Scenario ROUTE-02: BMM Skill Trigger Routing — Happy Paths

**Objective:** Verify all documented BMM triggers route to correct workflows  
**Risk Level:** CRITICAL  

### Test Matrix — Each row is one routing test

| Input Phrase | Expected Skill Load | Expected Workflow Path |
|-------------|--------------------|-----------------------|
| "brainstorm project" | bmad-bmm | workflows/1-analysis/brainstorm/ |
| "domain research" | bmad-bmm | workflows/1-analysis/domain-research/ |
| "market research" | bmad-bmm | workflows/1-analysis/ |
| "create PRD" | bmad-bmm | workflows/2-plan-workflows/create-prd/ |
| "product requirements" | bmad-bmm | workflows/2-plan-workflows/create-prd/ |
| "create UX design" | bmad-bmm | workflows/2-plan-workflows/ |
| "create architecture" | bmad-bmm | workflows/3-solutioning/ |
| "technical architecture" | bmad-bmm | workflows/3-solutioning/ |
| "create epics and stories" | bmad-bmm | workflows/3-solutioning/ |
| "check implementation readiness" | bmad-bmm | workflows/3-solutioning/check-implementation-readiness/ |
| "dev story" | bmad-bmm | workflows/4-implementation/dev-story/ |
| "implement story" | bmad-bmm | workflows/4-implementation/dev-story/ |
| "sprint planning" | bmad-bmm | workflows/4-implementation/ |
| "code review" | bmad-bmm | workflows/4-implementation/ |
| "quick flow" | bmad-bmm | workflows/bmad-quick-flow/ |
| "document project" | bmad-bmm | workflows/document-project/ |
| "generate project context" | bmad-bmm | workflows/generate-project-context/ |

### Pass Criteria
- [ ] Each trigger phrase produces `skills_tool:load` with `skill_name: bmad-bmm`
- [ ] Loaded skill content references correct workflow path for each trigger
- [ ] No trigger routes to wrong workflow (e.g., "dev story" → PRD workflow)

---

## Scenario ROUTE-03: TEA Skill Trigger Routing — All 9 Workflows

**Objective:** Verify all 9 TEA trigger phrases route to correct workflows  
**Risk Level:** CRITICAL  

### Test Matrix

| Input Phrase | Expected Workflow |
|-------------|------------------|
| "ATDD" | testarch/atdd/ |
| "acceptance tests" | testarch/atdd/ |
| "automate tests" | testarch/automate/ |
| "test automation" | testarch/automate/ |
| "CI integration" | testarch/ci/ |
| "continuous integration tests" | testarch/ci/ |
| "test framework" | testarch/framework/ |
| "NFR assessment" | testarch/nfr-assess/ |
| "non-functional requirements test" | testarch/nfr-assess/ |
| "test design" | testarch/test-design/ |
| "test cases" | testarch/test-design/ |
| "test review" | testarch/test-review/ |
| "review tests" | testarch/test-review/ |
| "trace tests" | testarch/trace/ |
| "traceability" | testarch/trace/ |
| "teach me testing" | testarch/teach-me-testing/ |
| "learn testing" | testarch/teach-me-testing/ |

### Pass Criteria
- [ ] All 17 trigger phrases load `bmad-tea` skill
- [ ] Each trigger maps to distinct correct workflow (no cross-routing)
- [ ] Menu item numbers (1-9) also route correctly ("1" → TMT, "2" → TF, etc.)

---

## Scenario ROUTE-04: BMB Skill Trigger Routing

**Objective:** Verify all BMB trigger phrases route correctly  
**Risk Level:** HIGH  

### Test Matrix

| Input Phrase | Expected Workflow |
|-------------|------------------|
| "create agent" | workflows/agent/ |
| "new agent" | workflows/agent/ |
| "edit agent" | workflows/agent/ |
| "validate agent" | workflows/agent/ |
| "create workflow" | workflows/workflow/ |
| "new workflow" | workflows/workflow/ |
| "edit workflow" | workflows/workflow/ |
| "validate workflow" | workflows/workflow/ |
| "create module" | workflows/module/ |
| "new module" | workflows/module/ |
| "bmad builder" | bmad-bmb skill load |

### Pass Criteria
- [ ] All triggers load `bmad-bmb` skill
- [ ] Agent triggers → agent/ workflows only
- [ ] Workflow triggers → workflow/ workflows only
- [ ] Module triggers → module/ workflows only

---

## Scenario ROUTE-05: CIS Skill Trigger Routing

**Objective:** Verify all CIS trigger phrases route to correct creative workflows  
**Risk Level:** HIGH  

### Test Matrix

| Input Phrase | Expected Workflow |
|-------------|------------------|
| "innovation strategy" | workflows/innovation-strategy/ |
| "disruption opportunities" | workflows/innovation-strategy/ |
| "storytelling" | workflows/storytelling/ |
| "narrative" | workflows/storytelling/ |
| "problem solving" | workflows/problem-solving/ |
| "structured problem solving" | workflows/problem-solving/ |
| "design thinking" | workflows/design-thinking/ |
| "empathy driven design" | workflows/design-thinking/ |
| "brainstorm" | bmad-cis skill + Carson agent |

### Pass Criteria
- [ ] All triggers load `bmad-cis` skill
- [ ] Each creative domain routes to distinct workflow

---

## Scenario ROUTE-06: bmad-init Trigger Routing

**Objective:** Verify bmad-init triggers are handled correctly  
**Risk Level:** HIGH  

### Test Matrix

| Input Phrase | Expected Behavior |
|-------------|------------------|
| "bmad init" | Load bmad-init skill → run init script |
| "initialize bmad" | Load bmad-init skill → run init script |
| "setup bmad" | Load bmad-init skill → run init script |
| "start bmad" | Load bmad-init skill |
| "bmad help" | Contextual help response |
| "bmad status" | Read + report 02-bmad-state.md |

### Pass Criteria
- [ ] Init triggers always load bmad-init skill first
- [ ] "bmad help" and "bmad status" handled without full init run
- [ ] Re-init on existing project: warns user, does not overwrite state

---

## Scenario ROUTE-07: Fuzzy Match and Disambiguation

**Objective:** Verify agents handle ambiguous trigger phrases gracefully  
**Risk Level:** HIGH  

### Steps
1. Say: "I want to do some testing" (ambiguous — could be TEA or general)
2. Say: "design" alone (matches test-design AND design-thinking)
3. Say: "review" alone (matches test-review AND code-review)

### Expected Behavior
- Single ambiguous match: agent asks for clarification with options
- Multiple possible matches: all matches listed for user selection
- No match: agent says "Not recognized" and shows menu
- Agent does NOT auto-execute on ambiguous input

### Pass Criteria
- [ ] Ambiguous triggers prompt clarification (not silent execution)
- [ ] Disambiguation options are accurate (no hallucinated options)
- [ ] No-match case shows correct menu for active agent

---

## Scenario ROUTE-08: Cross-Skill Boundary — Wrong Skill Triggers

**Objective:** Verify agents don't load wrong skills for cross-boundary triggers  
**Risk Level:** HIGH  

### Steps
1. Activate Murat (bmad-test-architect)
2. Ask: "create PRD" (BMM trigger, not TEA)
3. Observe: does Murat redirect or incorrectly attempt to handle?

4. Activate John (bmad-pm)
5. Ask: "test design" (TEA trigger, not BMM)
6. Observe: does John redirect to Murat or incorrectly attempt?

### Expected Behavior
- Each specialist agent recognizes out-of-scope requests
- Redirects to appropriate specialist agent or BMad Master
- Does NOT load wrong skill and attempt the workflow
- Framing: "That's [specialist]'s domain — let me connect you" or similar

### Pass Criteria
- [ ] No wrong skill loads on cross-boundary triggers
- [ ] Specialist agents redirect out-of-scope work correctly
- [ ] Redirect identifies correct specialist by name

---

## Scenario ROUTE-09: Workflow Path Resolution — {skill-dir} Alias

**Objective:** Verify {skill-dir} alias resolves to correct absolute path at runtime  
**Risk Level:** CRITICAL  

### Steps
For each skill, verify the runtime path resolution:
```bash
# Expected resolutions:
# bmad-tea {skill-dir} → /a0/skills/bmad-tea
# bmad-bmm {skill-dir} → /a0/skills/bmad-bmm
# bmad-bmb {skill-dir} → /a0/skills/bmad-bmb
# bmad-cis {skill-dir} → /a0/skills/bmad-cis
# bmad-init {skill-dir} → /a0/skills/bmad-init

for skill in /a0/skills/bmad-*/; do
  name=$(basename $skill)
  echo "${name}: ${skill}" 
done
```

### Pass Criteria
- [ ] {skill-dir} for each skill resolves to symlinked path `/a0/skills/bmad-*/`
- [ ] Symlinks resolve to actual project files (not broken)
- [ ] Workflow yaml/md files accessible via resolved paths
```bash
ls -la /a0/skills/ | grep bmad
for skill in bmad-tea bmad-bmm bmad-bmb bmad-cis bmad-init; do
  echo -n "$skill SKILL.md: "
  [ -f "/a0/skills/$skill/SKILL.md" ] && echo "EXISTS" || echo "MISSING"
done
```

### Pass Criteria
- [ ] All 5 skill symlinks present and not broken
- [ ] All 5 SKILL.md files accessible
- [ ] os.walk(followlinks=True) fix confirmed active in skills.py
