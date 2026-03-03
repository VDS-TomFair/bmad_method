# Test Scenarios: CIS Module (Creative Intelligence Suite)

**Priority:** MEDIUM  
**Skill:** `bmad-cis`  
**Agents:** bmad-innovation (Victor), bmad-design-thinking (Maya), bmad-storyteller (Sophia), bmad-brainstorming-coach (Carson), bmad-presentation (Caravaggio)  
**Workflows:** innovation-strategy/, storytelling/, problem-solving/, design-thinking/  
**Risk:** CIS serves creative users — persona fidelity and workflow completeness are primary concerns  

---

## Scenario CIS-01: Skill Load and Routing Table

**Objective:** Verify bmad-cis skill loads and all 4 workflow triggers are enumerated  
**Risk Level:** HIGH  

### Steps
1. Trigger: "innovation strategy" or "creative session"
2. Observe `skills_tool:load` for `bmad-cis`
3. Verify SKILL.md routing table

### Expected: All 4 workflows present
| Trigger | Workflow Path |
|---------|---------------|
| "innovation strategy", "disruption opportunities" | `workflows/innovation-strategy/` |
| "storytelling", "narrative", "brand story" | `workflows/storytelling/` |
| "problem solving", "structured problem solving" | `workflows/problem-solving/` |
| "design thinking", "empathy driven design" | `workflows/design-thinking/` |

### Pass Criteria
- [ ] Skill loads without error
- [ ] All 4 workflow trigger groups present
- [ ] CIS agents enumerated with profile names
- [ ] Output paths use `{output_folder}` or `{project-root}` aliases

---

## Scenario CIS-02: Innovation Strategy Workflow (Victor)

**Objective:** Verify innovation strategy workflow delivers Blue Ocean / Jobs-to-be-Done analysis  
**Risk Level:** HIGH  
**Workflow path:** `skills/bmad-cis/workflows/innovation-strategy/`  
**Agent:** bmad-innovation (Victor — Disruptive Innovation Oracle)

### Steps
1. Trigger: "innovation strategy" or "disruption opportunities"
2. Victor persona activates
3. Provide: industry context = "traditional retail banking"
4. Execute workflow to completion

### Expected Behavior
- Victor persona: "legendary strategist, billion-dollar pivots, JTBD + Blue Ocean + business model innovation"
- Victor's characteristic framing: "Markets reward genuine new value — incremental thinking means obsolete"
- Workflow produces:
  - Current state analysis (what exists, what's broken)
  - Jobs-to-be-Done mapping
  - Blue Ocean opportunity canvas
  - Disruption vectors (technology, regulation, behavior shifts)
  - Strategic recommendation with confidence rating
- Output saved to `{output_folder}/` or inline

### Pass Criteria
- [ ] Victor persona active with disruptive framing (not conservative)
- [ ] JTBD framework explicitly applied
- [ ] Blue Ocean canvas or equivalent structure present
- [ ] Recommendations go beyond incremental improvements
- [ ] Risk/confidence assessment included

---

## Scenario CIS-03: Design Thinking Workflow (Maya)

**Objective:** Verify design thinking workflow applies human-centered process correctly  
**Risk Level:** HIGH  
**Workflow path:** `skills/bmad-cis/workflows/design-thinking/`  
**Agent:** bmad-design-thinking (Maya — Design Thinking Maestro)

### Steps
1. Trigger: "design thinking" or "empathy driven design"
2. Maya persona activates
3. Provide: problem = "elderly users struggling with mobile banking apps"
4. Execute workflow through empathy → define → ideate → prototype phases

### Expected Behavior
- Maya persona: "virtuoso with 15+ years at Fortune 500s, empathy mapping expert"
- Maya's characteristic framing: "Design is about THEM not us — validate through real human interaction"
- Workflow stages:
  1. Empathy: user interviews structure, empathy map template
  2. Define: problem statement (HMW format)
  3. Ideate: divergent idea generation (10+ ideas)
  4. Prototype: prototype brief
  5. Test: validation plan
- Output: design thinking report with all 5 stages

### Pass Criteria
- [ ] Maya persona active with empathy-first framing
- [ ] All 5 design thinking stages present
- [ ] HMW (How Might We) problem statement generated
- [ ] Ideation produces multiple options (not single solution)
- [ ] Prototype and validation approach included

---

## Scenario CIS-04: Storytelling Workflow (Sophia)

**Objective:** Verify storytelling workflow produces compelling narrative structure  
**Risk Level:** MEDIUM  
**Workflow path:** `skills/bmad-cis/workflows/storytelling/`  
**Agent:** bmad-storyteller (Sophia — Master Storyteller)

### Steps
1. Trigger: "storytelling" or "narrative" or "brand story"
2. Sophia persona activates
3. Provide: subject = "a fintech startup disrupting remittances for migrant workers"
4. Execute workflow to completion

### Expected Behavior
- Sophia persona: "50+ years across journalism, screenwriting, brand narratives, emotional psychology"
- Sophia's framing: "Find the authentic story — make the abstract concrete through vivid details"
- Workflow produces:
  - Story framework selection (Hero's Journey, Problem/Solution, Before/After, etc.)
  - Core narrative arc with opening hook
  - Character/audience empathy elements
  - Emotional beats mapped
  - Call to action
- Output: story brief or full narrative draft

### Pass Criteria
- [ ] Sophia persona active with storytelling craft language
- [ ] Named storytelling framework applied (not generic structure)
- [ ] Emotional beats explicitly mapped
- [ ] Concrete details used (not abstractions)
- [ ] Authentic angle identified beyond marketing speak

---

## Scenario CIS-05: Problem Solving Workflow (Dr. Quinn)

**Objective:** Verify problem solving workflow applies TRIZ/Systems Thinking methodology  
**Risk Level:** HIGH  
**Workflow path:** `skills/bmad-cis/workflows/problem-solving/`  
**Agent:** bmad-problem-solver (Dr. Quinn — Master Problem Solver)

### Steps
1. Trigger: "problem solving" or "structured problem solving"
2. Dr. Quinn persona activates
3. Provide: problem = "our deployment pipeline takes 45 minutes and blocks the whole team"
4. Execute workflow to root cause and solution

### Expected Behavior
- Dr. Quinn persona: "TRIZ + Theory of Constraints + Systems Thinking, aerospace background"
- Dr. Quinn's framing: "Hunts root causes relentlessly — the right question beats a fast answer"
- Workflow stages:
  1. Problem framing (restate problem precisely)
  2. Root cause analysis (5 Whys or Fishbone)
  3. Constraint identification (Theory of Constraints)
  4. Solution generation (TRIZ principles applied)
  5. Recommendation with implementation path
- Output: structured problem analysis report

### Pass Criteria
- [ ] Dr. Quinn persona active with systematic analysis framing
- [ ] Root cause identified (not just symptoms treated)
- [ ] Named methodology applied (TRIZ / ToC / Systems Thinking)
- [ ] Multiple solution options generated
- [ ] Implementation path included

---

## Scenario CIS-06: Brainstorming Coach (Carson) via Party Mode

**Objective:** Verify Carson activates via brainstorming trigger and facilitates structured session  
**Risk Level:** MEDIUM  
**Agent:** bmad-brainstorming-coach (Carson — Elite Brainstorming Specialist)

### Steps
1. Trigger: "brainstorm" or "ideate" or "creative session"
2. Carson persona activates
3. Provide: topic = "new revenue streams for a legacy newspaper"
4. Observe facilitation technique used
5. Complete brainstorm session

### Expected Behavior
- Carson persona: "20+ years leading breakthrough sessions, group dynamics, psychological safety"
- Carson's framing: "Psychological safety unlocks breakthroughs"
- Session applies named technique: SCAMPER, Random Input, Reverse Brainstorming, Brainwriting, etc.
- Diverge → Converge structure maintained (no premature evaluation)
- Output: idea catalog with promising concepts highlighted

### Pass Criteria
- [ ] Carson persona active with facilitation language
- [ ] Named creative technique applied
- [ ] Diverge/converge structure maintained
- [ ] Psychological safety framing present ("no bad ideas" equivalent)
- [ ] Ideas cataloged and top candidates identified

---

## Scenario CIS-07: Presentation Master (Caravaggio)

**Objective:** Verify Caravaggio creates visual communication with frame-by-frame purposeful design  
**Risk Level:** MEDIUM  
**Agent:** bmad-presentation (Caravaggio — Visual Communication Expert)

### Steps
1. Trigger: "presentation" or "slide deck" or "pitch deck"
2. Caravaggio persona activates
3. Provide: context = "investor pitch for Series A, B2B SaaS product"
4. Execute presentation structure workflow

### Expected Behavior
- Caravaggio persona: "master presentation designer, visual hierarchy, audience psychology, Excalidraw"
- Caravaggio's framing: "Every frame needs a job — inform, persuade, transition, or cut it"
- Output: slide-by-slide structure with:
  - Frame purpose (inform/persuade/transition)
  - Visual hierarchy notes
  - Speaker notes
  - Narrative arc across deck
  - CTA slide

### Pass Criteria
- [ ] Caravaggio persona active with design craft language
- [ ] Each frame has explicit stated purpose
- [ ] Visual hierarchy guidance present
- [ ] Investor pitch conventions honored (problem/solution/market/traction/ask)
- [ ] Frame count appropriate for context

---

## Scenario CIS-08: CIS Team Config (creative-squad.yaml)

**Objective:** Verify CIS team configuration file is valid and enables Party Mode  
**Risk Level:** MEDIUM  

### Steps
```bash
cat /a0/skills/bmad-cis/teams/creative-squad.yaml
cat /a0/skills/bmad-cis/teams/default-party.csv
```

### Expected Behavior
- `creative-squad.yaml` defines a team composition for collaborative CIS sessions
- `default-party.csv` lists agent profiles for party mode
- Agent profile names match existing `agents/bmad-*/` directories
- No orphaned profile references

### Pass Criteria
- [ ] creative-squad.yaml is valid YAML
- [ ] default-party.csv references valid agent profile names
- [ ] At least Victor, Maya, Carson in team config
