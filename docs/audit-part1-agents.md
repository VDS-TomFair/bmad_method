# BMAD Alignment Audit — Part 1: Agent Profiles Comparison

**Date**: 2026-05-02  
**Auditor**: Deep Research Agent  
**Scope**: All 21 agent directories vs upstream specification

---

## Executive Summary

The BMAD A0 plugin contains **21 agent directories** against an upstream roster of **19 agents**. Overall alignment is strong for core BMM agents (names, icons, menus, communication styles). Key deviations include: (1) SM and QA agents exist separately despite upstream consolidating them into Amelia v6.3+, (2) an extra quick-dev agent (Barry) not in the upstream roster, (3) one icon mismatch (Morgan), (4) multiple icon collisions across CIS agents, and (5) a simplified activation sequence (5 steps vs upstream 8 steps).

---

## Agent-by-Agent Comparison Table

| # | Agent Dir | Persona Name | Icon | Title Match | Style Match | Menu Codes | Phase | Module | Status |
|---|-----------|-------------|------|-------------|-------------|------------|-------|--------|--------|
| 1 | bmad-analyst | Mary | 📊 | ✅ Business Analyst | ✅ treasure hunter | BP,MR,DR,TR,CB,WB,DP | Phase 1 | BMM | ✅ ALIGNED |
| 2 | bmad-pm | John | 📋 | ✅ Product Manager | ✅ detective/WHY | CP,VP,EP,CE,IR,CC | Phase 2 | BMM | ✅ ALIGNED |
| 3 | bmad-architect | Winston | 🏗️ | ✅ System Architect | ✅ calm/whiteboard | CA,IR | Phase 3 | BMM | ✅ ALIGNED |
| 4 | bmad-dev | Amelia | 💻 | ✅ Senior SW Eng | ✅ terminal/exact paths | DS,QD,QA,CR,SP,CS,ER | Phase 4 | BMM | ⚠️ PARTIAL |
| 5 | bmad-ux-designer | Sally | 🎨 | ✅ UX Designer | ⚠️ painter≠filmmaker | CU | Phase 2 | BMM | ⚠️ PARTIAL |
| 6 | bmad-tech-writer | Paige | 📚 | ✅ Technical Writer | ✅ patient teacher | DP,WD,MG,VD,EC | Anytime | BMM | ⚠️ PARTIAL |
| 7 | bmad-sm | Bob | 🏃 | N/A (legacy) | — | SP,SS,VS,CS,ER | Phase 4 | BMM | ❌ LEGACY |
| 8 | bmad-qa | Quinn | 🧪 | N/A (legacy) | — | QA | Phase 4 | BMM | ❌ LEGACY |
| 9 | bmad-agent-builder | Bond | 🤖 | ✅ Agent Builder | ✅ precise/technical | BA,EA,VA,QA | Anytime | BMB | ✅ ALIGNED |
| 10 | bmad-workflow-builder | Wendy | 🔄 | ✅ Workflow Builder | ✅ systematic | BW,EW,VW,CW,RW,QW,VS,VF,MV | Anytime | BMB | ✅ ALIGNED |
| 11 | bmad-module-builder | Morgan | ❌ 🏗️→📦 | ✅ Module Builder | ✅ strategic | IM,PB,CM,EM,VM,SB | Anytime | BMB | ⚠️ ICON MISMATCH |
| 12 | bmad-test-architect | Murat | 🧪 | ✅ Master Test Architect | ✅ data-driven/risk | TMT,TD,TF,CI,AT,TA,RV,NR,TRC | Anytime | TEA | ✅ ALIGNED |
| 13 | bmad-innovation | Victor | ⚡ | ⚠️ Plugin persona | ✅ strategic/bold | IS | Anytime | CIS | ⚠️ ENRICHED |
| 14 | bmad-problem-solver | Dr. Quinn | 🔬 | ⚠️ Plugin persona | ✅ systematic | PS | Anytime | CIS | ⚠️ ENRICHED |
| 15 | bmad-design-thinking | Maya | 🎨* | ⚠️ Plugin persona | ✅ empathy/jazz | DT | Anytime | CIS | ⚠️ ENRICHED |
| 16 | bmad-brainstorming-coach | Carson | 🧠 | ⚠️ Plugin persona | ✅ improv/enthusiastic | BS | Anytime | CIS | ⚠️ ENRICHED |
| 17 | bmad-storyteller | Sophia | 📖 | ⚠️ Plugin persona | ✅ bard/poet | ST | Anytime | CIS | ⚠️ ENRICHED |
| 18 | bmad-presentation | Caravaggio | 🎨* | ⚠️ Plugin persona | ✅ creative director | PR | Anytime | CIS | ⚠️ ENRICHED |
| 19 | bmad-master | BMad Master | 🧙 | ✅ orchestrator | ✅ direct/comprehensive | (routes to agents) | All | Core | ✅ ALIGNED |
| 20 | bmad-quick-dev | Barry | 🚀 | ❓ Not in upstream | — | QS,QQ | Quick Flow | BMM | ❓ EXTRA |

*🎨 = icon collision — shared by Sally (UX), Maya (Design Thinking), and Caravaggio (Presentation)

---

## Detailed Findings per Agent

### 1. bmad-analyst — Mary (Business Analyst) ✅ ALIGNED

| Criterion | Upstream | Plugin | Match |
|-----------|----------|--------|-------|
| Name | Mary | Mary | ✅ |
| Icon | 📊 | 📊 | ✅ |
| Title | Business Analyst | Business Analyst | ✅ |
| Skill name | bmad-analyst | bmad-analyst | ✅ |
| Phase | Phase 1 | Phase 1 — Analysis | ✅ |
| Communication style | treasure hunter narrating finds | "Treasure hunter's excitement for patterns, McKinsey memo's structure for findings" | ✅ |
| Menu codes | BP,MR,DR,TR,CB,WB,DP | BP,MR,DR,TR,CB,WB,DP | ✅ |

**Verdict**: Fully aligned. All criteria match upstream specification.

---

### 2. bmad-pm — John (Product Manager) ✅ ALIGNED

| Criterion | Upstream | Plugin | Match |
|-----------|----------|--------|-------|
| Name | John | John | ✅ |
| Icon | 📋 | 📋 | ✅ |
| Title | Product Manager | Product Manager | ✅ |
| Skill name | bmad-pm | bmad-pm | ✅ |
| Phase | Phase 2-3 | Phase 2 — Planning | ⚠️ Minor |
| Communication style | detective interrogating cold case | "Detective's 'why?' relentless. Direct, data-sharp, cuts through fluff to what matters." | ✅ |
| Menu codes | CP,VP,EP,CE,IR,CC | CP,VP,EP,CE,IR,CC | ✅ |

**Note**: Upstream says Phase 2-3; plugin says Phase 2 only. However, module-help.csv correctly routes CE and IR to Phase 3-solutioning. The customize.toml includes Phase 3 menu items (CE, IR, CC). This is a documentation label difference, not a functional one.

**Verdict**: Aligned with minor phase label discrepancy.

---

### 3. bmad-architect — Winston (System Architect) ✅ ALIGNED

| Criterion | Upstream | Plugin | Match |
|-----------|----------|--------|-------|
| Name | Winston | Winston | ✅ |
| Icon | 🏗️ | 🏗️ | ✅ |
| Title | System Architect | System Architect | ✅ |
| Skill name | bmad-architect | bmad-architect | ✅ |
| Phase | Phase 3 | Phase 3 — Solutioning | ✅ |
| Communication style | seasoned engineer at whiteboard | "Calm and pragmatic. Balances 'what could be' with 'what should be'" | ✅ |
| Menu codes | CA,IR | CA,IR | ✅ |

**Verdict**: Fully aligned.

---

### 4. bmad-dev — Amelia (Developer) ⚠️ PARTIAL

| Criterion | Upstream | Plugin | Match |
|-----------|----------|--------|-------|
| Name | Amelia | Amelia | ✅ |
| Icon | 💻 | 💻 | ✅ |
| Title | Senior Software Engineer | Senior Software Engineer | ✅ |
| Skill name | bmad-agent-dev | bmad-dev | ❌ MISMATCH |
| Phase | Phase 4 + Quick | Phase 4 — Implementation | ⚠️ |
| Communication style | terminal prompt, exact paths | "Ultra-succinct. Speaks in file paths and AC IDs — every statement citable" | ✅ |
| Menu codes | DS,QD,QA,CR,SP,CS,ER | DS,QD,QA,CR,SP,CS,ER | ✅ |

**Deviations**:

1. **Skill name**: Upstream uses `bmad-agent-dev`; plugin uses `bmad-dev`. This is the A0 profile/directory naming convention — the upstream name uses the Claude/Cursor skill name pattern.

2. **Consolidation incomplete**: Upstream says SM (SP,SS,VS,CS,CC,ER) and QA (QA) are consolidated into Amelia v6.3+. Plugin has separate bmad-sm and bmad-qa agents. However, Amelia's customize.toml DOES include SP, CS, ER, and QA menu codes, suggesting partial consolidation at the menu level while keeping separate agent profiles.

3. **Missing from customize.toml**: SS (Sprint Status), VS (Validate Story), CC (Correct Course) are in module-help.csv under `sm` skill but NOT in Amelia's customize.toml menu.

**Verdict**: Partially aligned. Menu codes partially consolidated; separate SM/QA agents remain.

---

### 5. bmad-ux-designer — Sally (UX Designer) ⚠️ PARTIAL

| Criterion | Upstream | Plugin | Match |
|-----------|----------|--------|-------|
| Name | Sally | Sally | ✅ |
| Icon | 🎨 | 🎨 | ✅ |
| Title | UX Designer | UX Designer | ✅ |
| Skill name | bmad-ux-designer | bmad-ux-designer | ✅ |
| Phase | Phase 2 | Phase 2 — Planning | ✅ |
| Communication style | filmmaker pitching scene | "Paints pictures with words. User stories that make you feel the problem" | ⚠️ |
| Menu codes | CU | CU | ✅ |

**Deviation**: Communication style wording differs. Upstream says "filmmaker pitching scene" while plugin uses a "painter" metaphor. The role.md says "Sally paints pictures with words" and "storytelling flair" — related but distinct from the filmmaker metaphor.

**Verdict**: Mostly aligned with style wording difference.

---

### 6. bmad-tech-writer — Paige (Technical Writer) ⚠️ PARTIAL

| Criterion | Upstream | Plugin | Match |
|-----------|----------|--------|-------|
| Name | Paige | Paige | ✅ |
| Icon | 📚 | 📚 | ✅ |
| Title | Technical Writer | Technical Writer | ✅ |
| Skill name | bmad-tech-writer | bmad-tech-writer | ✅ |
| Phase | Anytime | Cross-Phase (Documentation) | ✅ |
| Communication style | patient teacher | "Patient educator — explains like teaching a friend" | ✅ |
| Menu codes | DP,WD,US,MG,VD,EC | DP,WD,**~~US~~**,MG,VD,EC | ❌ MISSING US |

**Deviation**: US (Update Standards) is listed in module-help.csv for tech-writer but is NOT in customize.toml menu. This means Paige's in-agent menu does not show the Update Standards option, though the workflow exists.

**Verdict**: Missing US menu code from customize.toml.

---

### 7. bmad-sm — Bob (Scrum Master) ❌ LEGACY

| Criterion | Upstream | Plugin | Match |
|-----------|----------|--------|-------|
| Name | (consolidated into Amelia) | Bob | ❌ |
| Icon | (consolidated) | 🏃 | N/A |
| Title | (consolidated) | Scrum Master | N/A |
| Menu codes | SP,SS,VS,CS,CC,ER (merged to Amelia) | Exists separately in module-help.csv | ❌ |

**Deviation**: Upstream v6.3+ consolidates SM into Amelia. Plugin retains a separate bmad-sm agent with persona "Bob". Module-help.csv assigns SP,SS,VS,CS menu codes to the `sm` skill. The SM menus (SP, CS, ER) also appear in Amelia's customize.toml, creating a dual-routing situation.

**Verdict**: Legacy agent that should be consolidated per upstream v6.3+.

---

### 8. bmad-qa — Quinn (QA Engineer) ❌ LEGACY

| Criterion | Upstream | Plugin | Match |
|-----------|----------|--------|-------|
| Name | (consolidated into Amelia) | Quinn | ❌ |
| Icon | (consolidated) | 🧪 | N/A |
| Title | (consolidated) | QA Engineer | N/A |
| Menu codes | QA (merged to Amelia) | QA exists separately | ❌ |

**Deviation**: Upstream v6.3+ consolidates QA into Amelia. Plugin retains separate bmad-qa agent with persona "Quinn". QA also appears in Amelia's customize.toml menu.

**Icon collision**: Quinn (bmad-qa) and Murat (bmad-test-architect) both use 🧪.

**Verdict**: Legacy agent that should be consolidated per upstream v6.3+.

---

### 9. bmad-agent-builder — Bond (Agent Builder) ✅ ALIGNED

| Criterion | Upstream | Plugin | Match |
|-----------|----------|--------|-------|
| Name | Bond | Bond | ✅ |
| Icon | 🤖 | 🤖 | ✅ |
| Title | Agent Builder | Agent Building Expert | ✅ |
| Module | BMB | BMB | ✅ |
| Communication style | precise, technical | "precision of a senior software architect conducting a code review" | ✅ |
| Menu codes | BA,EA,VA,QA | BA,EA,VA,QA (from module-help.csv) | ✅ |

**Note**: No customize.toml in the agents directory for BMB agents; menu codes are defined via module-help.csv routing.

**Verdict**: Fully aligned.

---

### 10. bmad-workflow-builder — Wendy (Workflow Builder) ✅ ALIGNED

| Criterion | Upstream | Plugin | Match |
|-----------|----------|--------|-------|
| Name | Wendy | Wendy | ✅ |
| Icon | 🔄 | 🔄 | ✅ |
| Title | Workflow Builder | Workflow Building Master | ✅ |
| Module | BMB | BMB | ✅ |
| Communication style | systematic | "methodical precision of a systems engineer" | ✅ |
| Menu codes | BW,EW,VW,CW,RW,QW,VS,VF,MV | BW,EW,VW,CW,RW,QW,VS,VF,MV | ✅ |

**Verdict**: Fully aligned.

---

### 11. bmad-module-builder — Morgan (Module Builder) ⚠️ ICON MISMATCH

| Criterion | Upstream | Plugin | Match |
|-----------|----------|--------|-------|
| Name | Morgan | Morgan | ✅ |
| Icon | 📦 | 🏗️ | ❌ MISMATCH |
| Title | Module Builder | Module Creation Master | ✅ |
| Module | BMB | BMB | ✅ |
| Communication style | strategic | "strategic perspective of a systems architect" | ✅ |
| Menu codes | IM,PB,CM,EM,VM,SB | IM,PB,CM,EM,VM,SB | ✅ |

**Deviation**: Icon is 🏗️ in plugin but upstream specifies 📦. Additionally, 🏗️ collides with Winston (bmad-architect).

**Verdict**: Icon mismatch — should be 📦 per upstream.

---

### 12. bmad-test-architect — Murat (Master Test Architect) ✅ ALIGNED

| Criterion | Upstream | Plugin | Match |
|-----------|----------|--------|-------|
| Name | Murat | Murat | ✅ |
| Icon | 🧪 | 🧪 | ✅ |
| Title | Master Test Architect | Master Test Architect and Quality Advisor | ✅ |
| Module | TEA | TEA | ✅ |
| Communication style | (not specified upstream) | "blending hard data with seasoned instinct" | ✅ |
| Menu codes | TMT,TD,TF,CI,AT,TA,RV,NR,TRC | TMT,TD,TF,CI,AT,TA,RV,NR,TRC | ✅ |

**Icon collision**: Murat shares 🧪 with Quinn (bmad-qa). If QA is consolidated into Amelia, this resolves.

**Verdict**: Fully aligned.

---

### 13-18. CIS Agents ⚠️ ENRICHED (Plugin-Specific Personas)

The upstream CIS specification provides only functional role names (Innovation Strategist, Creative Problem Solver, etc.) without specific persona names or icons. The plugin enriches these with detailed personas:

| Agent Dir | Plugin Persona | Plugin Icon | Upstream Role Name | Menu Code | Style Match |
|-----------|---------------|-------------|-------------------|-----------|-------------|
| bmad-innovation | Victor (Disruptive Innovation Oracle) | ⚡ | Innovation Strategist | IS | ✅ strategic/bold |
| bmad-problem-solver | Dr. Quinn (Master Problem Solver) | 🔬 | Creative Problem Solver | PS | ✅ systematic/scientific |
| bmad-design-thinking | Maya (Design Thinking Maestro) | 🎨* | Design Thinking Coach | DT | ✅ empathy/jazz |
| bmad-brainstorming-coach | Carson (Elite Brainstorming Specialist) | 🧠 | Brainstorming Coach | BS | ✅ improv/enthusiastic |
| bmad-storyteller | Sophia (Master Storyteller) | 📖 | Storyteller | ST | ✅ bard/poet |
| bmad-presentation | Caravaggio (Visual Communication Expert) | 🎨* | Presentation Master | PR | ✅ creative director |

*🎨 = icon collision

**Key observations**:

- All menu codes match upstream exactly
- Persona names (Victor, Dr. Quinn, Maya, Carson, Sophia, Caravaggio) are plugin-specific enrichments
- Title variations are minor (e.g., "Creative Problem Solver" → "Master Problem Solver")
- Communication styles are well-matched to upstream role descriptions

**Icon collisions within CIS**:
- 🎨 used by 3 agents: Maya (design-thinking), Caravaggio (presentation), and Sally (ux-designer)
- No unique icons for design-thinking vs presentation vs ux-designer

**Verdict**: Functionally aligned (all menu codes correct). Persona names and some titles are plugin-specific enhancements not present in upstream. Icon collisions need resolution.

---

### 19. bmad-master — BMad Master (Orchestrator) ✅ ALIGNED

| Criterion | Upstream | Plugin | Match |
|-----------|----------|--------|-------|
| Name | (bmad-master) | BMad Master | ✅ |
| Icon | (not specified) | 🧙 | ✅ |
| Title | orchestrator | BMad Master Executor, Knowledge Custodian, Workflow Orchestrator | ✅ |
| Module | Core | Core | ✅ |
| Delegates to | 19 specialized agents | All 20 subordinates (incl. extra Barry) | ⚠️ |

**Verdict**: Aligned. Role as orchestrator correctly implemented.

---

### 20. bmad-quick-dev — Barry (Quick Flow Solo Dev) ❓ EXTRA

| Criterion | Upstream | Plugin | Match |
|-----------|----------|--------|-------|
| Name | (not in upstream roster) | Barry | N/A |
| Icon | (not in upstream) | 🚀 | N/A |
| Title | (not in upstream) | Quick Flow Solo Dev | N/A |
| Module | — | BMM | N/A |
| Menu codes | — | QS, QQ (via module-help.csv) | N/A |

**Analysis**: Barry does not appear in the upstream agent roster. However, the upstream Amelia listing mentions "Phase 4 + Quick" and QD appears in Amelia's customize.toml ("Unified quick flow — clarify intent, plan, implement, review, present"). The module-help.csv also has a `quick-flow-solo-dev` skill with QS and QQ codes. This suggests Quick Flow is an upstream concept but was split into a separate agent in the plugin.

**Verdict**: Extra agent not in upstream roster. Quick Flow is an upstream concept but handled differently.

---

## Activation Sequence Analysis

### Upstream Specification (8 steps)

1. Resolve customization (base → team → user merge)
2. Execute `activation_steps_prepend`
3. Load persona (identity, communication style)
4. Load `persistent_facts`
5. Load config and resolve variables
6. Greet the user
7. Execute `activation_steps_append`
8. Present menu

### Plugin Implementation (5 steps — from bmad-agent-shared.md)

1. Review project state (auto-injected in system prompt)
2. Review project config (auto-injected in system prompt)
3. Greet as persona
4. Present menu
5. Wait for direction

### Gap Analysis

| Upstream Step | Plugin Equivalent | Gap |
|--------------|-------------------|-----|
| 1. Resolve customization | Not in activation flow | ❌ Missing |
| 2. activation_steps_prepend | Not in activation flow | ❌ Missing |
| 3. Load persona | Step 3 (greet as persona) | ⚠️ Implicit |
| 4. Load persistent_facts | Not in activation flow | ❌ Missing |
| 5. Load config + resolve vars | Steps 1-2 (auto-injected) | ⚠️ Different mechanism |
| 6. Greet user | Step 3 | ✅ Present |
| 7. activation_steps_append | Not in activation flow | ❌ Missing |
| 8. Present menu | Step 4 | ✅ Present |

The customize.toml files for BMM agents DO define `activation_steps_prepend`, `activation_steps_append`, and `persistent_facts`, but the shared activation protocol does not orchestrate them.

---

## Team Assignment Analysis

### Upstream Specification
- BMM agents: team = `software-development`
- BMB agents: team = (builder)
- TEA agent: team = (testing)
- CIS agents: team = (creative)

### Plugin Implementation
- No `team` field in agent.yaml files
- Teams are implicitly defined via module-help.csv `skill` column
- The `customize.toml` files have `name` and `title` as read-only but no team field

**Verdict**: Team assignment is handled differently (module routing vs explicit team field) but functionally equivalent.

---

## Key Findings Summary

### ✅ Correctly Aligned Agents (11/20)

1. **Mary** (bmad-analyst) — Perfect match
2. **John** (bmad-pm) — Match (minor phase label)
3. **Winston** (bmad-architect) — Perfect match
4. **Bond** (bmad-agent-builder) — Perfect match
5. **Wendy** (bmad-workflow-builder) — Perfect match
6. **Murat** (bmad-test-architect) — Perfect match
7. **BMad Master** (bmad-master) — Match
8. **Victor** (bmad-innovation) — Menu aligned, persona is plugin enrichment
9. **Dr. Quinn** (bmad-problem-solver) — Menu aligned, persona is plugin enrichment
10. **Carson** (bmad-brainstorming-coach) — Menu aligned, persona is plugin enrichment
11. **Sophia** (bmad-storyteller) — Menu aligned, persona is plugin enrichment

### ⚠️ Partially Aligned Agents (6/20)

1. **Amelia** (bmad-dev) — Skill name mismatch (bmad-dev vs bmad-agent-dev), incomplete SM/QA consolidation
2. **Sally** (bmad-ux-designer) — Style wording differs (painter vs filmmaker)
3. **Paige** (bmad-tech-writer) — Missing US menu code from customize.toml
4. **Morgan** (bmad-module-builder) — Icon mismatch (🏗️ vs 📦)
5. **Maya** (bmad-design-thinking) — Icon collision (🎨 shared with Sally and Caravaggio)
6. **Caravaggio** (bmad-presentation) — Icon collision (🎨 shared with Sally and Maya)

### ❌ Legacy Agents (2/20)

1. **Bob** (bmad-sm) — Should be consolidated into Amelia per v6.3+
2. **Quinn** (bmad-qa) — Should be consolidated into Amelia per v6.3+

### ❓ Extra Agents (1/20)

1. **Barry** (bmad-quick-dev) — Not in upstream roster; Quick Flow concept exists upstream but handled differently

### Missing from Upstream

None. All 19 upstream agents have corresponding plugin directories.

---

## Critical Issues Requiring Resolution

### Priority 1: SM/QA Consolidation Decision

**bmad-sm** and **bmad-qa** exist separately despite upstream v6.3+ consolidating them into Amelia. Current state:
- Amelia's customize.toml has: SP, CS, ER, QA (partial SM/QA menus)
- Missing from Amelia: SS (Sprint Status), VS (Validate Story), CC (Correct Course)
- Separate bmad-sm and bmad-qa agents exist with full menu codes

**Options**:
- A) Full consolidation: Add SS, VS, CC to Amelia's customize.toml, deprecate bmad-sm and bmad-qa
- B) Keep separate: Document as intentional A0-specific design decision
- C) Hybrid (current): Maintain both but ensure no routing conflicts

### Priority 2: Icon Collisions

| Icon | Agents Sharing | Recommended Fix |
|------|---------------|----------------|
| 🎨 | Sally (UX), Maya (Design Thinking), Caravaggio (Presentation) | Assign unique: 🎨 Sally, 🎯 Maya, 🖼️ Caravaggio |
| 🏗️ | Winston (Architect), Morgan (Module Builder) | Morgan → 📦 (upstream spec) |
| 🧪 | Quinn (QA), Murat (Test Architect) | Resolved if QA consolidated to Amelia |

### Priority 3: Missing Menu Code

- **Paige** (bmad-tech-writer): Add US (Update Standards) to customize.toml `[[agent.menu]]`

### Priority 4: Activation Sequence Enhancement

The 5-step plugin activation should be enhanced to include the full 8-step upstream sequence, particularly:
- Explicit customization resolution step
- activation_steps_prepend/append execution
- persistent_facts loading

### Priority 5: Communication Style Alignment

- **Sally**: Consider updating style reference from "painter" to "filmmaker" to match upstream

---

## Skill Name Mapping

| Upstream Skill Name | Plugin Profile Name | Match |
|--------------------|--------------------|-------|
| bmad-analyst | bmad-analyst | ✅ |
| bmad-pm | bmad-pm | ✅ |
| bmad-architect | bmad-architect | ✅ |
| bmad-agent-dev | bmad-dev | ❌ |
| bmad-ux-designer | bmad-ux-designer | ✅ |
| bmad-tech-writer | bmad-tech-writer | ✅ |
| bmad-master | bmad-master | ✅ |
| bmad-test-architect | bmad-test-architect | ✅ |

---

*End of Part 1: Agent Profiles Comparison*
