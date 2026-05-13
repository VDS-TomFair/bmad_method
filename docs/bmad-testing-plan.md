# BMAD Method A2A Testing Plan

Based on upstream BMAD-METHOD v6.6.0 behavior research via DeepWiki.

## Testing Approach

Each test sends a single A2A message and verifies the response against expected upstream behavior.
A2A URL: `https://testing.emichi.co/a2a/t-8a-vdZDQ1xJoX9gN/p-caveman`

---

## Phase 1: Core Routing & Activation (P0)

### T01: bmad-help
- **Send:** `bmad-help`
- **Expected:** Analyzes project state, shows prioritized list of recommended next steps with skill commands
- **Verify:** Response contains skill recommendations, project analysis

### T02: bmad-master greeting
- **Send:** `hello`
- **Expected:** BMad Master greets user, describes BMAD capabilities, offers to load modules
- **Verify:** Warm greeting, capability overview, menu or guidance

### T03: Analyst activation (Mary)
- **Send:** `bmad-analyst`
- **Expected:** 📊 Mary greets by name, presents menu with codes: BP, MR, DR, TR, CB, WB, DP
- **Verify:** Icon 📊, name "Mary", menu table with codes

### T04: Architect activation (Winston)
- **Send:** `bmad-architect`
- **Expected:** 🏗️ Winston greets, presents menu: CA, IR
- **Verify:** Icon 🏗️, name "Winston", menu with CA and IR

### T05: PM activation (John)
- **Send:** `bmad-pm`
- **Expected:** 📋 John greets, presents menu: CP, VP, EP, CE, IR, CC
- **Verify:** Icon 📋, name "John", menu with codes

### T06: Dev activation (Amelia)
- **Send:** `bmad-agent-dev`
- **Expected:** 💻 Amelia greets, presents menu: DS, QD, QA, CR, SP, CS, ER
- **Verify:** Icon 💻, name "Amelia", menu with codes

### T07: UX Designer activation (Sally)
- **Send:** `bmad-ux-designer`
- **Expected:** 🎨 Sally greets, presents menu: CU
- **Verify:** Icon 🎨, name "Sally", menu with CU

### T08: Tech Writer activation (Paige)
- **Send:** `bmad-tech-writer`
- **Expected:** 📚 Paige greets, presents menu: DP, WD, US, MG, VD, EC
- **Verify:** Icon 📚, name "Paige", menu with codes

---

## Phase 2: BMB Builder Activation (P0)

### T09: Workflow Builder (Wendy)
- **Send:** `/BW`
- **Expected:** Wendy loads BMB skill, presents Create Mode menu: [F]rom scratch / [C]onvert existing
- **Verify:** Menu with F and C options, WAITS for input (Phase G compliance)

### T10: Agent Builder (Bond)
- **Send:** `/BA`
- **Expected:** Bond loads BMB skill, presents Create Mode menu: [F]rom scratch / [C]onvert existing
- **Verify:** Menu with F and C options, WAITS for input

### T11: Module Builder (Morgan)
- **Send:** `/BM`
- **Expected:** Morgan loads BMB skill, presents brief or creation menu
- **Verify:** Agent activates, presents menu, WAITS for input

---

## Phase 3: Menu Navigation (P1)

### T12: Analyst menu code
- **Send:** `bmad-analyst` then (in same session) `BP`
- **Expected:** Mary activates brainstorming workflow
- **Verify:** Brainstorming session starts (not just menu redisplayed)

### T13: Natural language routing
- **Send:** `I want to brainstorm`
- **Expected:** BMad Master routes to Analyst/brainstorming
- **Verify:** Brainstorming starts or analyst activates with BP dispatched

### T14: Fuzzy menu match
- **Send:** `bmad-pm` then `create prd`
- **Expected:** John activates Create PRD workflow (CP code fuzzy matched)
- **Verify:** PRD creation starts

---

## Phase 4: Workflow First Steps (P1)

### T15: Product Brief workflow start
- **Send:** `bmad-analyst` then `CB`
- **Expected:** Mary guides product brief creation, asks clarifying questions
- **Verify:** Workflow starts, interactive questioning begins

### T16: Create Architecture start
- **Send:** `bmad-architect` then `CA`
- **Expected:** Winston guides architecture creation
- **Verify:** Architecture workflow starts

### T17: Create PRD start
- **Send:** `bmad-pm` then `CP`
- **Expected:** John guides PRD creation
- **Verify:** PRD workflow starts

### T18: Dev Story start
- **Send:** `bmad-agent-dev` then `DS`
- **Expected:** Amelia asks which story to implement
- **Verify:** Story selection/implementation starts

---

## Phase 5: Core Skills (P1)

### T19: bmad-party-mode
- **Send:** `bmad-party-mode`
- **Expected:** Shows agent roster, asks what to discuss, offers solo/multi modes
- **Verify:** Agent list displayed, user prompted for topic

### T20: bmad-customize
- **Send:** `bmad-customize`
- **Expected:** Offers customization options (agent persona, workflow logic, global config)
- **Verify:** Customization menu presented

### T21: bmad-brainstorming
- **Send:** `bmad-brainstorming`
- **Expected:** Starts brainstorming session, asks for topic
- **Verify:** Brainstorming session starts interactively

### T22: bmad-distillator
- **Send:** `bmad-distillator`
- **Expected:** Asks for document to compress
- **Verify:** Compression workflow ready

---

## Phase 6: BMB Step-File Compliance (P1)

### T23: Wendy process compliance
- **Send:** `/BW` then `F`
- **Expected:** Wendy loads step-01-discovery, asks questions about workflow idea
- **Verify:** Step-by-step process starts (NOT skipping to output)
- **Check Docker logs:** "PROCESS RULE" or step-file loading evidence

### T24: Wendy path resolution
- **Send:** `/BW` (check Docker logs)
- **Expected:** Config resolves to:
  - bmb_staging_folder: .a0proj/_bmad-output/bmb-staging
  - bmb_build_output_agents: .a0proj/agents
  - bmb_build_output_skills: .a0proj/skills
- **Verify:** Docker logs show correct path resolution (Phase H)

---

## Phase 7: TEA & CIS Activation (P2)

### T25: TEA activation (Murat)
- **Send:** `bmad-tea`
- **Expected:** Murat greets, presents test architecture workflows
- **Verify:** TEA agent activates with test workflows

### T26: CIS Design Thinking
- **Send:** `bmad-design-thinking`
- **Expected:** Design Thinking Coach greets, starts design thinking session
- **Verify:** Design thinking workflow begins

### T27: CIS Innovation Strategy
- **Send:** `bmad-innovation`
- **Expected:** Innovation Strategist greets, starts strategy session
- **Verify:** Innovation workflow begins

### T28: CIS Storyteller
- **Send:** `bmad-storyteller`
- **Expected:** Storyteller greets, offers storytelling guidance
- **Verify:** Storytelling workflow begins

### T29: CIS Problem Solver
- **Send:** `bmad-problem-solver`
- **Expected:** Creative Problem Solver greets, starts problem-solving session
- **Verify:** Problem-solving workflow begins

### T30: CIS Presentation Master
- **Send:** `bmad-presentation`
- **Expected:** Presentation Master greets, offers presentation help
- **Verify:** Presentation workflow begins

---

## Phase 8: Edge Cases (P2)

### T31: Invalid command
- **Send:** `bmad-nonexistent`
- **Expected:** Graceful error or routing to help
- **Verify:** No crash, helpful guidance

### T32: Unknown natural language
- **Send:** `xyzzy foo bar baz`
- **Expected:** BMad Master handles gracefully, offers guidance
- **Verify:** No crash, redirect to help or menu

### T33: Quick Dev Track
- **Send:** `bmad-quick-dev`
- **Expected:** Quick dev agent activates, offers fast dev flow
- **Verify:** Quick dev workflow available

---

## Test Execution Order

```
Phase 1 (P0): T01-T08    → Core routing & activation (MUST PASS)
Phase 2 (P0): T09-T11    → BMB builder activation (MUST PASS)
Phase 3 (P1): T12-T14    → Menu navigation
Phase 4 (P1): T15-T18    → Workflow first steps
Phase 5 (P1): T19-T22    → Core skills
Phase 6 (P1): T23-T24    → BMB process compliance
Phase 7 (P2): T25-T30    → TEA & CIS activation
Phase 8 (P2): T31-T33    → Edge cases
```

## Pass Criteria

- **P0 (T01-T11):** 100% must pass — routing and activation are fundamental
- **P1 (T12-T24):** ≥80% should pass — navigation and workflows
- **P2 (T25-T33):** ≥60% should pass — extended modules and edge cases

## Agent Expected Behaviors Summary

| Agent | Icon | Name | Communication Style | Key Menu Codes |
|---|---|---|---|---|
| Analyst | 📊 | Mary | Treasure hunter narrating the find | BP, MR, DR, TR, CB, WB, DP |
| Architect | 🏗️ | Winston | Seasoned engineer at the whiteboard | CA, IR |
| PM | 📋 | John | Detective interrogating a cold case | CP, VP, EP, CE, IR, CC |
| Dev | 💻 | Amelia | Terminal prompt: exact file paths, commit-message brevity | DS, QD, QA, CR, SP, CS, ER |
| UX Designer | 🎨 | Sally | Filmmaker pitching the scene | CU |
| Tech Writer | 📚 | Paige | Patient teacher with analogies | DP, WD, US, MG, VD, EC |
| Workflow Builder | 🔄 | Wendy | Workflow architect | F, C |
| Agent Builder | 🛠️ | Bond | Agent specialist | F, C |
| Module Builder | 📦 | Morgan | Module packager | Brief/Creation |
| TEA | 🧪 | Murat | Test architect expert | Test workflows |
