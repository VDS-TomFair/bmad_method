# BMAD Method Plugin — Comprehensive Testing Strategy

**Version:** 1.0  
**Date:** 2025-05-01  
**Testing Target:** A2A endpoint `https://testing.emichi.co/a2a/t-8a-vdZDQ1xJoX9gN/p-caveman`  
**Plugin Version:** 1.3.0 (Phase G+H complete)  

---

## 1. Executive Summary

This document defines a comprehensive functional testing strategy for the Agent Zero BMAD Method Plugin. The plugin delivers 20 specialist agent personas across 4 modules (BMM, BMB, CIS, TEA), phase-aware routing, workflow orchestration, project initialization, customization overrides, and multi-agent party mode.

Testing is executed via A2A (Agent-to-Agent) protocol against a live testing instance. Each test sends a natural-language message and verifies the response matches expected BMAD behavior. Tests are stateless between A2A messages, so each test scenario must be self-contained.

The strategy covers 90+ test scenarios organized by module and priority. Phases G (process compliance) and H (creation paths) are already verified — this document focuses on ALL remaining functional capabilities.

---

## 2. Functional Coverage Matrix

### 2.1 Module Coverage Summary

| Module | Agents | Workflows/Triggers | Test Scenarios | Coverage
|--------|--------|-------------------|----------------|----------
| INIT (Core) | 1 (Master) | 12 | 14 | Full
| BMM | 10 | 30+ | 35 | Full
| BMB | 3 | 18 | 18 | Full
| CIS | 6 | 6 | 12 | Full
| TEA | 1 | 9 | 12 | Full
| Config/Custom | — | 3 | 6 | Full
| Teams/Party | — | 2 | 5 | Full
| **TOTAL** | **20** | **80+** | **~102** | **Full**

### 2.2 Agent Coverage

| Agent | Profile Name | Module | Persona | Test Priority
|-------|-------------|--------|---------|-------------
| Mary | `bmad-analyst` | BMM | Business Analyst | P0
| John | `bmad-pm` | BMM | Product Manager | P0
| Winston | `bmad-architect` | BMM | Architect | P0
| Bob | `bmad-sm` | BMM | Scrum Master | P0
| Amelia | `bmad-dev` | BMM | Developer | P0
| Quinn | `bmad-qa` | BMM | QA Engineer | P1
| Barry | `bmad-quick-dev` | BMM | Quick Flow Solo Dev | P1
| Sally | `bmad-ux-designer` | BMM | UX Designer | P1
| Paige | `bmad-tech-writer` | BMM | Technical Writer | P1
| Bond | `bmad-agent-builder` | BMB | Agent Builder | P0
| Wendy | `bmad-workflow-builder` | BMB | Workflow Builder | P0
| Morgan | `bmad-module-builder` | BMB | Module Builder | P0
| Victor | `bmad-innovation` | CIS | Innovation Strategist | P1
| Carson | `bmad-brainstorming-coach` | CIS | Brainstorming Coach | P1
| Maya | `bmad-design-thinking` | CIS | Design Thinking Coach | P1
| Dr. Quinn | `bmad-problem-solver` | CIS | Problem Solver | P1
| Sophia | `bmad-storyteller` | CIS | Storyteller | P2
| Caravaggio | `bmad-presentation` | CIS | Presentation Master | P2
| Murat | `bmad-test-architect` | TEA | Test Architect | P1
| Master | `bmad-master` | Core | BMad Master | P0

---

## 3. Test Scenarios

### 3.1 INIT Module — Core Initialization & Help

#### T-INIT-01: BMAD Help Command
- **What:** User requests BMAD help
- **Expected:** BMad Master responds with module reference, current project state, and recommended next step
- **A2A Command:** `bmad help`
- **Verify:** Response contains module list (BMM, BMB, CIS, TEA), trigger phrases, current phase status
- **Priority:** P0
- **Pass Criteria:** Agent lists all 4+ modules with descriptions and trigger phrases

#### T-INIT-02: BMAD Status
- **What:** User checks BMAD status
- **Expected:** Shows current phase, persona, and project state from 02-bmad-state.md
- **A2A Command:** `bmad status`
- **Verify:** Response shows phase value, project name, any completed artifacts
- **Priority:** P0
- **Pass Criteria:** Agent reads and reports state file contents accurately

#### T-INIT-03: BMAD Master Activation
- **What:** User activates BMad Master persona
- **Expected:** BMad Master persona activates, shows module menu, offers routing
- **A2A Command:** `bmad master`
- **Verify:** Response includes module menu, routing table from extension, phase-aware recommendations
- **Priority:** P0
- **Pass Criteria:** Persona adopts orchestrator role, shows available modules and routing options

#### T-INIT-04: Index Docs Task
- **What:** Create lightweight index for quick LLM scanning
- **Expected:** Agent creates index of project documentation
- **A2A Command:** `index the BMAD docs for quick scanning`
- **Verify:** Agent runs bmad-index-docs skill, produces index file
- **Priority:** P2
- **Pass Criteria:** Agent understands and executes the indexing task

#### T-INIT-05: Shard Document Task
- **What:** Split large document into sections
- **Expected:** Agent offers to shard a specified document
- **A2A Command:** `shard this document into smaller files: the PRD`
- **Verify:** Agent activates shard-doc workflow
- **Priority:** P2
- **Pass Criteria:** Agent initiates document sharding process

#### T-INIT-06: Editorial Review (Prose)
- **What:** Review prose for clarity and tone
- **Expected:** Agent reviews text and suggests improvements
- **A2A Command:** `editorial review prose on the product brief`
- **Verify:** Agent runs bmad-editorial-review-prose, returns three-column markdown table with fixes
- **Priority:** P2
- **Pass Criteria:** Agent produces structured review with suggestions

#### T-INIT-07: Editorial Review (Structure)
- **What:** Propose cuts and reorganization
- **Expected:** Agent reviews document structure and suggests improvements
- **A2A Command:** `editorial review structure on the PRD`
- **Verify:** Agent runs bmad-editorial-review-structure, provides structural recommendations
- **Priority:** P2
- **Pass Criteria:** Agent produces structural review

#### T-INIT-08: Adversarial Review
- **What:** Critical review to find issues and weaknesses
- **Expected:** Agent performs adversarial review of content
- **A2A Command:** `adversarial review of the architecture document`
- **Verify:** Agent runs bmad-review-adversarial-general, identifies weaknesses
- **Priority:** P1
- **Pass Criteria:** Agent identifies genuine issues and provides critical assessment

#### T-INIT-09: Edge Case Hunter Review
- **What:** Walk branching paths for unhandled edge cases
- **Expected:** Agent systematically checks edge cases
- **A2A Command:** `edge case hunter review on the sprint plan`
- **Verify:** Agent runs bmad-review-edge-case-hunter, reports unhandled edge cases
- **Priority:** P2
- **Pass Criteria:** Agent identifies boundary conditions and unhandled cases

#### T-INIT-10: Advanced Elicitation
- **What:** Refine content using reasoning methods
- **Expected:** Agent offers elicitation methods (Pre-mortem, First Principles, etc.)
- **A2A Command:** `advanced elicitation on the product brief using pre-mortem`
- **Verify:** Agent runs bmad-advanced-elicitation workflow
- **Priority:** P1
- **Pass Criteria:** Agent applies reasoning method and produces refined content

#### T-INIT-11: Distillator Task
- **What:** Lossless LLM-optimized compression
- **Expected:** Agent compresses document for token efficiency
- **A2A Command:** `distill the architecture document for token efficiency`
- **Verify:** Agent runs bmad-distillator skill, produces compressed version
- **Priority:** P2
- **Pass Criteria:** Agent produces verifiable lossless compression

#### T-INIT-12: Brainstorming (Core)
- **What:** Generate diverse ideas through interactive techniques
- **Expected:** Agent facilitates brainstorming session
- **A2A Command:** `brainstorming session for new product features`
- **Verify:** Agent activates bmad-brainstorming workflow, uses techniques (SCAMPER, etc.)
- **Priority:** P1
- **Pass Criteria:** Agent facilitates interactive brainstorming with structured techniques

#### T-INIT-13: Not Initialized Project
- **What:** User sends BMAD command on uninitialized project
- **Expected:** Agent detects no state file, tells user to run bmad init first
- **A2A Command:** `create a PRD` (on fresh/uninitialized session)
- **Verify:** Response says BMAD not initialized, instructs to run bmad init
- **Priority:** P0
- **Pass Criteria:** Agent detects missing state and provides initialization guidance

#### T-INIT-14: Routing Table Phase-Awareness
- **What:** Verify routing changes based on current phase
- **Expected:** Different workflows shown for different phases
- **A2A Command:** `bmad help` (then verify which workflows appear based on state)
- **Verify:** Phase=ready shows all modules; phase=2-planning hides implementation workflows
- **Priority:** P1
- **Pass Criteria:** Routing manifest adapts to current phase

---

### 3.2 BMM Module — Phase 1: Analysis

#### T-BMM-01: Brainstorm Project (BP)
- **What:** Expert-guided facilitation through ideation techniques
- **Agent:** Mary (bmad-analyst)
- **Expected:** Analyst persona activates, guides through brainstorming techniques
- **A2A Command:** `brainstorm project for a task management app`
- **Verify:** Mary persona active, structured brainstorming process initiated
- **Priority:** P0
- **Pass Criteria:** Agent adopts Mary persona, asks clarifying questions, uses structured techniques

#### T-BMM-02: Market Research (MR)
- **What:** Market analysis, competitive landscape, trends
- **Agent:** Mary (bmad-analyst)
- **Expected:** Analyst conducts market research, produces research documents
- **A2A Command:** `market research for developer tools in the AI space`
- **Verify:** Research covers competitive landscape, customer needs, trends
- **Priority:** P1
- **Pass Criteria:** Agent produces structured market analysis

#### T-BMM-03: Domain Research (DR)
- **What:** Industry domain deep dive
- **Agent:** Mary (bmad-analyst)
- **Expected:** Domain-specific research with terminology and expertise
- **A2A Command:** `domain research for healthcare compliance`
- **Verify:** Research covers domain terminology, regulations, key concepts
- **Priority:** P1
- **Pass Criteria:** Agent produces domain-specific deep dive

#### T-BMM-04: Technical Research (TR)
- **What:** Technical feasibility and architecture options
- **Agent:** Mary (bmad-analyst)
- **Expected:** Technical research with architecture options and approaches
- **A2A Command:** `technical research for real-time collaboration architecture`
- **Verify:** Research covers architecture options, trade-offs, implementation approaches
- **Priority:** P1
- **Pass Criteria:** Agent produces technical feasibility analysis

#### T-BMM-05: Create Product Brief (CB)
- **What:** Guided experience to define product idea
- **Agent:** Mary (bmad-analyst)
- **Expected:** Step-by-step product brief creation workflow
- **A2A Command:** `create product brief for a social media analytics dashboard`
- **Verify:** Agent guides through brief sections, produces product-brief*.md
- **Priority:** P0
- **Pass Criteria:** Agent creates structured product brief with all required sections

#### T-BMM-06: Working Backwards (WB) / PRFAQ
- **What:** Amazon-style PRFAQ challenge
- **Agent:** Mary (bmad-analyst)
- **Expected:** PRFAQ document creation
- **A2A Command:** `working backwards PRFAQ for a new AI feature`
- **Verify:** Agent produces PRFAQ-style document
- **Priority:** P2
- **Pass Criteria:** Agent creates press release + FAQ format document

---

### 3.3 BMM Module — Phase 2: Planning

#### T-BMM-07: Create PRD (CP)
- **What:** Expert-led PRD creation
- **Agent:** John (bmad-pm)
- **Expected:** PM persona guides through PRD creation
- **A2A Command:** `create PRD for the analytics dashboard`
- **Verify:** John persona active, structured PRD workflow with all sections
- **Priority:** P0
- **Pass Criteria:** Agent adopts PM persona, produces comprehensive PRD

#### T-BMM-08: Validate PRD (VP)
- **What:** Validate PRD completeness and quality
- **Agent:** John (bmad-pm)
- **Expected:** PRD validation report with specific improvement suggestions
- **A2A Command:** `validate the PRD`
- **Verify:** Agent produces validation report with completeness check
- **Priority:** P1
- **Pass Criteria:** Agent identifies gaps and provides improvement suggestions

#### T-BMM-09: Edit PRD (EP)
- **What:** Improve existing PRD
- **Agent:** John (bmad-pm)
- **Expected:** PRD editing workflow with targeted improvements
- **A2A Command:** `edit PRD to add non-functional requirements`
- **Verify:** Agent updates PRD with requested changes
- **Priority:** P1
- **Pass Criteria:** Agent applies targeted edits to existing PRD

#### T-BMM-10: Create UX Design (CU)
- **What:** UX design workflow
- **Agent:** Sally (bmad-ux-designer)
- **Expected:** UX Designer guides through user experience design
- **A2A Command:** `create UX design for the dashboard`
- **Verify:** Sally persona active, UX specifications produced
- **Priority:** P1
- **Pass Criteria:** Agent creates UX design document with user flows and specs

---

### 3.4 BMM Module — Phase 3: Solutioning

#### T-BMM-11: Create Architecture (CA)
- **What:** Architecture design workflow
- **Agent:** Winston (bmad-architect)
- **Expected:** Architect persona guides technical decisions
- **A2A Command:** `create architecture for the analytics platform`
- **Verify:** Winston persona active, architecture document with tech decisions
- **Priority:** P0
- **Pass Criteria:** Agent produces architecture document with technology stack, patterns, diagrams

#### T-BMM-12: Create Epics and Stories (CE)
- **What:** Break requirements into implementable work
- **Agent:** John (bmad-pm)
- **Expected:** PM creates epic and story breakdown from PRD/architecture
- **A2A Command:** `create epics and stories from the PRD`
- **Verify:** Structured epic/story hierarchy produced
- **Priority:** P0
- **Pass Criteria:** Agent produces epics with stories, each with acceptance criteria

#### T-BMM-13: Check Implementation Readiness (IR)
- **What:** Gate check before implementation
- **Agent:** Winston (bmad-architect)
- **Expected:** Readiness assessment with alignment check
- **A2A Command:** `check implementation readiness`
- **Verify:** Agent validates PRD, UX, Architecture, Epics alignment
- **Priority:** P0
- **Pass Criteria:** Agent produces readiness report with pass/fail for each artifact

---

### 3.5 BMM Module — Phase 4: Implementation

#### T-BMM-14: Sprint Planning (SP)
- **What:** Generate sprint plan
- **Agent:** Bob (bmad-sm)
- **Expected:** Sprint plan document with task sequencing
- **A2A Command:** `sprint planning for the first epic`
- **Verify:** Sprint plan produced with story order and dependencies
- **Priority:** P0
- **Pass Criteria:** Agent creates sprint plan referencing epics/stories

#### T-BMM-15: Sprint Status (SS)
- **What:** Summarize sprint progress
- **Agent:** Bob (bmad-sm)
- **Expected:** Status summary and next-step routing
- **A2A Command:** `sprint status`
- **Verify:** Agent reports sprint progress and recommends next action
- **Priority:** P1
- **Pass Criteria:** Agent provides sprint progress summary

#### T-BMM-16: Create Story (CS)
- **What:** Prepare next story for implementation
- **Agent:** Bob (bmad-sm)
- **Expected:** Story preparation with full context
- **A2A Command:** `create story for the first task in the sprint`
- **Verify:** Agent produces detailed story with AC, context, dependencies
- **Priority:** P0
- **Pass Criteria:** Agent creates implementation-ready story

#### T-BMM-17: Validate Story (VS)
- **What:** Validate story readiness before dev
- **Agent:** Bob (bmad-sm)
- **Expected:** Story validation report
- **A2A Command:** `validate story readiness`
- **Verify:** Agent checks story completeness and provides report
- **Priority:** P1
- **Pass Criteria:** Agent produces validation report with readiness assessment

#### T-BMM-18: Dev Story (DS)
- **What:** Implement story
- **Agent:** Amelia (bmad-dev)
- **Expected:** Developer implements story tasks
- **A2A Command:** `dev story — implement the login feature`
- **Verify:** Amelia persona active, implements code following AC
- **Priority:** P0
- **Pass Criteria:** Agent adopts dev persona, produces implementation code

#### T-BMM-19: Code Review (CR)
- **What:** Validate implementation quality
- **Agent:** Amelia (bmad-dev)
- **Expected:** Code review with issues and recommendations
- **A2A Command:** `code review the implementation`
- **Verify:** Agent reviews code quality, identifies issues
- **Priority:** P0
- **Pass Criteria:** Agent produces structured code review

#### T-BMM-20: QA Automation (QA)
- **What:** Generate automated tests
- **Agent:** Quinn (bmad-qa)
- **Expected:** QA generates E2E/API test suite
- **A2A Command:** `generate QA automated tests for the login feature`
- **Verify:** Agent detects test framework, generates appropriate tests
- **Priority:** P1
- **Pass Criteria:** Agent produces runnable test suite

#### T-BMM-21: Correct Course (CC)
- **What:** Handle significant mid-sprint changes
- **Agent:** Bob (bmad-sm)
- **Expected:** Change proposal with impact analysis
- **A2A Command:** `correct course — we need to change the authentication approach`
- **Verify:** Agent produces change proposal, recommends action (update PRD, redo arch, etc.)
- **Priority:** P1
- **Pass Criteria:** Agent analyzes impact and provides course correction recommendation

#### T-BMM-22: Checkpoint Review (CK)
- **What:** Human-in-the-loop review of changes
- **Agent:** Amelia (bmad-dev)
- **Expected:** Walkthrough of change with focus points
- **A2A Command:** `checkpoint review the recent changes`
- **Verify:** Agent walks through changes, highlights important areas
- **Priority:** P2
- **Pass Criteria:** Agent produces focused change walkthrough

#### T-BMM-23: Retrospective (ER)
- **What:** Epic completion review
- **Agent:** Bob (bmad-sm)
- **Expected:** Lessons learned and next-step recommendation
- **A2A Command:** `retrospective on the completed epic`
- **Verify:** Agent produces retrospective with lessons and recommendations
- **Priority:** P1
- **Pass Criteria:** Agent produces structured retrospective document

---

### 3.6 BMM Module — Anytime Workflows

#### T-BMM-24: Document Project (DP)
- **What:** Analyze existing project for documentation
- **Agent:** Mary (bmad-analyst)
- **Expected:** Project documentation produced
- **A2A Command:** `document the project`
- **Verify:** Agent analyzes codebase and produces useful documentation
- **Priority:** P1
- **Pass Criteria:** Agent produces project documentation in project-knowledge/

#### T-BMM-25: Generate Project Context (GPC)
- **What:** Scan codebase for lean LLM-optimized context
- **Agent:** Mary (bmad-analyst) / Barry (bmad-quick-dev)
- **Expected:** project-context.md with critical implementation patterns
- **A2A Command:** `generate project context for AI agents`
- **Verify:** Agent produces lean, optimized context document
- **Priority:** P1
- **Pass Criteria:** Agent creates project-context.md with implementation patterns

#### T-BMM-26: Quick Spec (QS)
- **What:** Quick specification for small tasks
- **Agent:** Barry (bmad-quick-dev)
- **Expected:** Fast tech spec without full planning
- **A2A Command:** `quick spec for adding dark mode to the UI`
- **Verify:** Barry persona active, quick spec produced
- **Priority:** P0
- **Pass Criteria:** Agent produces lean spec quickly without extensive planning

#### T-BMM-27: Quick Dev (QD)
- **What:** Quick implementation from spec
- **Agent:** Barry (bmad-quick-dev)
- **Expected:** Direct implementation without full workflow
- **A2A Command:** `quick dev — add a color picker component`
- **Verify:** Agent implements directly without going through full sprint
- **Priority:** P0
- **Pass Criteria:** Agent produces working implementation quickly

#### T-BMM-28: Write Document (WD)
- **What:** Create documentation following best practices
- **Agent:** Paige (bmad-tech-writer)
- **Expected:** Well-structured document following documentation standards
- **A2A Command:** `write a getting started guide for the API`
- **Verify:** Paige persona active, document follows standards
- **Priority:** P1
- **Pass Criteria:** Agent produces high-quality documentation

#### T-BMM-29: Update Standards (US)
- **What:** Update documentation standards preferences
- **Agent:** Paige (bmad-tech-writer)
- **Expected:** Standards file updated in .a0proj/knowledge/tech-writer-sidecar
- **A2A Command:** `update documentation standards to prefer present tense`
- **Verify:** Agent updates standards in knowledge directory
- **Priority:** P2
- **Pass Criteria:** Agent modifies documentation-standards.md

#### T-BMM-30: Mermaid Generate (MG)
- **What:** Create Mermaid diagram
- **Agent:** Paige (bmad-tech-writer)
- **Expected:** Mermaid diagram based on description
- **A2A Command:** `create a mermaid sequence diagram for the login flow`
- **Verify:** Agent produces valid Mermaid diagram code
- **Priority:** P2
- **Pass Criteria:** Agent generates valid Mermaid syntax for the described diagram

#### T-BMM-31: Validate Document (VD)
- **What:** Review document against standards
- **Agent:** Paige (bmad-tech-writer)
- **Expected:** Validation report with priority-organized suggestions
- **A2A Command:** `validate the getting started guide document`
- **Verify:** Agent produces actionable improvement suggestions by priority
- **Priority:** P2
- **Pass Criteria:** Agent produces validation report

#### T-BMM-32: Explain Concept (EC)
- **What:** Create technical explanation with examples
- **Agent:** Paige (bmad-tech-writer)
- **Expected:** Clear explanation with examples and diagrams
- **A2A Command:** `explain the concept of event-driven architecture`
- **Verify:** Agent produces digestible explanation with examples
- **Priority:** P2
- **Pass Criteria:** Agent creates clear technical explanation

---

### 3.7 BMB Module — Builder Capabilities

#### T-BMB-01: Build Agent (BA)
- **What:** Create new BMAD agent
- **Agent:** Bond (bmad-agent-builder)
- **Expected:** Agent builder workflow guides through creating custom agent
- **A2A Command:** `build a new agent called "security-scanner" that reviews code for vulnerabilities`
- **Verify:** Bond persona active, agent creation workflow initiated, produces agent in .a0proj/agents/
- **Priority:** P0
- **Pass Criteria:** Agent follows build process, produces agent YAML + prompt files

#### T-BMB-02: Edit Agent (EA)
- **What:** Edit existing BMAD agent
- **Agent:** Bond (bmad-agent-builder)
- **Expected:** Agent editing workflow maintains compliance
- **A2A Command:** `edit the security-scanner agent to add code review capabilities`
- **Verify:** Agent loads existing agent, applies edits, validates compliance
- **Priority:** P1
- **Pass Criteria:** Agent edits existing agent while maintaining structure

#### T-BMB-03: Validate Agent (VA)
- **What:** Validate agent compliance
- **Agent:** Bond (bmad-agent-builder)
- **Expected:** Validation report with compliance check
- **A2A Command:** `validate the security-scanner agent`
- **Verify:** Agent runs compliance checks, produces validation report
- **Priority:** P1
- **Pass Criteria:** Agent produces validation report with pass/fail for each criterion

#### T-BMB-04: Build Workflow (BW)
- **What:** Create new BMAD workflow
- **Agent:** Wendy (bmad-workflow-builder)
- **Expected:** Workflow builder guides through structured workflow creation
- **A2A Command:** `build a workflow for automated dependency updates`
- **Verify:** Wendy persona active, workflow created in .a0proj/skills/
- **Priority:** P0
- **Pass Criteria:** Agent produces workflow.md with steps, valid structure

#### T-BMB-05: Edit Workflow (EW)
- **What:** Edit existing workflow
- **Agent:** Wendy (bmad-workflow-builder)
- **Expected:** Workflow editing with integrity preservation
- **A2A Command:** `edit the dependency-update workflow to add a testing step`
- **Verify:** Agent loads workflow, applies edits, maintains integrity
- **Priority:** P1
- **Pass Criteria:** Agent edits workflow while preserving structure

#### T-BMB-06: Validate Workflow (VW)
- **What:** Validate workflow against best practices
- **Agent:** Wendy (bmad-workflow-builder)
- **Expected:** Validation report
- **A2A Command:** `validate the dependency-update workflow`
- **Verify:** Agent runs validation checks, produces report
- **Priority:** P1
- **Pass Criteria:** Agent produces validation report

#### T-BMB-07: Max Parallel Validate (MV)
- **What:** Validate with parallel sub-process support
- **Agent:** Wendy (bmad-workflow-builder)
- **Expected:** Parallel validation report
- **A2A Command:** `max parallel validate the workflow`
- **Verify:** Agent runs parallel validation
- **Priority:** P2
- **Pass Criteria:** Agent validates with parallel process awareness

#### T-BMB-08: Convert Skill (CW)
- **What:** Convert skill to BMad-compliant format
- **Agent:** Wendy (bmad-workflow-builder)
- **Expected:** Converted skill with before/after comparison
- **A2A Command:** `convert this skill to BMad format`
- **Verify:** Agent produces converted skill and comparison report
- **Priority:** P2
- **Pass Criteria:** Agent produces compliant version with HTML comparison

#### T-BMB-09: Rework Workflow (RW)
- **What:** Rework workflow to V6 compliance
- **Agent:** Wendy (bmad-workflow-builder)
- **Expected:** V6-compliant workflow
- **A2A Command:** `rework this workflow to V6 compliance`
- **Verify:** Agent reworks workflow following V6 standards
- **Priority:** P2
- **Pass Criteria:** Agent produces V6-compliant workflow

#### T-BMB-10: Ideate Module (IM)
- **What:** Brainstorm and plan BMAD module
- **Agent:** Morgan (bmad-module-builder)
- **Expected:** Module ideation with architecture and build plan
- **A2A Command:** `ideate a BMAD module for DevOps automation`
- **Verify:** Morgan persona active, produces module plan
- **Priority:** P1
- **Pass Criteria:** Agent produces module concept with architecture

#### T-BMB-11: Create Module Brief (PB)
- **What:** Create product brief for module
- **Agent:** Morgan (bmad-module-builder)
- **Expected:** Module product brief
- **A2A Command:** `create module brief for the DevOps automation module`
- **Verify:** Agent produces structured module brief
- **Priority:** P1
- **Pass Criteria:** Agent creates module brief document

#### T-BMB-12: Create Module (CM)
- **What:** Create complete BMAD module
- **Agent:** Morgan (bmad-module-builder)
- **Expected:** Full module with agents, workflows, infrastructure
- **A2A Command:** `create module from the DevOps brief`
- **Verify:** Agent creates complete module package
- **Priority:** P0
- **Pass Criteria:** Agent produces module with agents, workflows, config, installer

#### T-BMB-13: Edit Module (EM)
- **What:** Edit existing module
- **Agent:** Morgan (bmad-module-builder)
- **Expected:** Module editing with coherence
- **A2A Command:** `edit the DevOps module to add a new agent`
- **Verify:** Agent edits module maintaining coherence
- **Priority:** P1
- **Pass Criteria:** Agent applies edits maintaining module structure

#### T-BMB-14: Validate Module (VM)
- **What:** Run compliance check on module
- **Agent:** Morgan (bmad-module-builder)
- **Expected:** Validation report
- **A2A Command:** `validate the DevOps module`
- **Verify:** Agent runs compliance checks
- **Priority:** P1
- **Pass Criteria:** Agent produces module validation report

#### T-BMB-15: Setup Builder (SB)
- **What:** Set up BMB module in project
- **Agent:** Wendy (bmad-workflow-builder)
- **Expected:** BMB setup workflow executed
- **A2A Command:** `setup BMad Builder module`
- **Verify:** Agent runs bmad-bmb-setup skill
- **Priority:** P1
- **Pass Criteria:** Agent initializes BMB in the project

#### T-BMB-16: Quality Scan Agent (QA)
- **What:** Comprehensive quality scan for agent
- **Agent:** Bond (bmad-agent-builder)
- **Expected:** JSON + HTML quality report
- **A2A Command:** `quality scan the security-scanner agent`
- **Verify:** Agent produces quality report with scores
- **Priority:** P2
- **Pass Criteria:** Agent produces JSON + HTML report

#### T-BMB-17: Quality Scan Workflow (QW)
- **What:** Quality scan for workflow
- **Agent:** Wendy (bmad-workflow-builder)
- **Expected:** JSON + HTML quality report
- **A2A Command:** `quality scan the dependency-update workflow`
- **Verify:** Agent produces quality report
- **Priority:** P2
- **Pass Criteria:** Agent produces quality report

#### T-BMB-18: Validate Skill (VS) and File References (VF)
- **What:** Validate skill package and file references
- **Agent:** Wendy (bmad-workflow-builder)
- **Expected:** Validation reports for structure and file refs
- **A2A Command:** `validate the skill package and check for broken file references`
- **Verify:** Agent runs structural validation and file reference checks
- **Priority:** P2
- **Pass Criteria:** Agent validates skill structure and reports broken refs

---

### 3.8 CIS Module — Creative Intelligence Suite

#### T-CIS-01: Innovation Strategy (IS)
- **What:** Identify disruption opportunities
- **Agent:** Victor (bmad-innovation)
- **Expected:** Innovation strategy with business model analysis
- **A2A Command:** `innovation strategy for disrupting the project management market`
- **Verify:** Victor persona active, strategic innovation analysis
- **Priority:** P1
- **Pass Criteria:** Agent produces innovation strategy with disruption opportunities

#### T-CIS-02: Problem Solving (PS)
- **What:** Systematic problem-solving
- **Agent:** Dr. Quinn (bmad-problem-solver)
- **Expected:** Structured problem analysis with solution
- **A2A Command:** `problem solving — our deployment pipeline is too slow`
- **Verify:** Dr. Quinn persona active, systematic analysis (TRIZ, ToC)
- **Priority:** P1
- **Pass Criteria:** Agent applies structured methodology and produces solution

#### T-CIS-03: Design Thinking (DT)
- **What:** Human-centered design process
- **Agent:** Maya (bmad-design-thinking)
- **Expected:** Design thinking workflow with empathy mapping
- **A2A Command:** `design thinking for improving the onboarding experience`
- **Verify:** Maya persona active, empathy-driven methodology
- **Priority:** P1
- **Pass Criteria:** Agent guides through design thinking stages

#### T-CIS-04: Brainstorming (BS) — CIS
- **What:** CIS-branded brainstorming session
- **Agent:** Carson (bmad-brainstorming-coach)
- **Expected:** Facilitated brainstorming with techniques
- **A2A Command:** `brainstorming session using SCAMPER for feature ideation`
- **Verify:** Carson persona active, structured techniques applied
- **Priority:** P1
- **Pass Criteria:** Agent facilitates session using SCAMPER or other techniques

#### T-CIS-05: Storytelling (ST)
- **What:** Craft compelling narrative
- **Agent:** Sophia (bmad-storyteller)
- **Expected:** Storytelling with narrative frameworks
- **A2A Command:** `craft a compelling story about our product vision`
- **Verify:** Sophia persona active, narrative framework applied
- **Priority:** P2
- **Pass Criteria:** Agent produces compelling narrative using story frameworks

#### T-CIS-06: Presentation (PR)
- **What:** Design presentation/slide deck
- **Agent:** Caravaggio (bmad-presentation)
- **Expected:** Presentation with visual storytelling
- **A2A Command:** `create a pitch deck presentation for investor meeting`
- **Verify:** Caravaggio/Spike persona active, visual communication focus
- **Priority:** P2
- **Pass Criteria:** Agent produces presentation structure with visual guidance

#### T-CIS-07: CIS Agent Personas — Innovation
- **What:** Verify Victor (Innovation Strategist) persona consistency
- **Expected:** Victor speaks like chess grandmaster, bold declarations, strategic silences
- **A2A Command:** `as innovation strategist, analyze the AI coding assistant market`
- **Verify:** Response matches Victor's communication style (chess metaphors, bold questions)
- **Priority:** P1
- **Pass Criteria:** Agent maintains distinctive Victor persona

#### T-CIS-08: CIS Agent Personas — Brainstorming
- **What:** Verify Carson (Brainstorming Coach) persona consistency
- **Expected:** Enthusiastic improv coach, YES AND energy
- **A2A Command:** `help me brainstorm new feature ideas`
- **Verify:** Carson's high-energy improv coach style is maintained
- **Priority:** P1
- **Pass Criteria:** Agent maintains distinctive Carson persona

#### T-CIS-09: CIS Agent Personas — Design Thinking
- **What:** Verify Maya (Design Thinking) persona consistency
- **Expected:** Jazz musician style, sensory metaphors, playful challenges
- **A2A Command:** `guide me through design thinking for mobile app UX`
- **Verify:** Maya's jazz musician communication style
- **Priority:** P2
- **Pass Criteria:** Agent maintains distinctive Maya persona

#### T-CIS-10: CIS Agent Personas — Problem Solver
- **What:** Verify Dr. Quinn persona consistency
- **Expected:** Sherlock Holmes + playful scientist, AHA moments
- **A2A Command:** `solve the problem of high user churn in first week`
- **Verify:** Dr. Quinn's deductive, curious style with AHA moments
- **Priority:** P1
- **Pass Criteria:** Agent maintains distinctive Dr. Quinn persona

#### T-CIS-11: CIS Agent Personas — Storyteller
- **What:** Verify Sophia (Storyteller) persona consistency
- **Expected:** Bard-like, flowery, whimsical narrative
- **A2A Command:** `tell me the story of how our product changes lives`
- **Verify:** Sophia's bard-like storytelling style
- **Priority:** P2
- **Pass Criteria:** Agent maintains distinctive Sophia persona

#### T-CIS-12: CIS Agent Personas — Presentation
- **What:** Verify Caravaggio (Presentation Master) persona consistency
- **Expected:** Energetic creative director, dramatic reveals
- **A2A Command:** `design a presentation structure for our roadmap`
- **Verify:** Caravaggio/Spike's energetic creative director style
- **Priority:** P2
- **Pass Criteria:** Agent maintains distinctive presentation persona

---

### 3.9 TEA Module — Test Engineering & Architecture

#### T-TEA-01: Teach Me Testing (TMT)
- **What:** 7-session TEA Academy for testing fundamentals
- **Agent:** Murat (bmad-test-architect)
- **Expected:** Murat persona, structured teaching through testing concepts
- **A2A Command:** `teach me testing fundamentals`
- **Verify:** Murat persona active, session-based learning structure
- **Priority:** P1
- **Pass Criteria:** Agent initiates teaching session with structured curriculum

#### T-TEA-02: Test Design (TD)
- **What:** Risk-based test planning
- **Agent:** Murat (bmad-test-architect)
- **Expected:** Test design document linked to requirements
- **A2A Command:** `test design for the analytics dashboard module`
- **Verify:** Agent produces risk-based test plan with priority levels
- **Priority:** P0
- **Pass Criteria:** Agent produces test design with P0-P3 risk prioritization

#### T-TEA-03: Test Framework (TF)
- **What:** Initialize production-ready test framework
- **Agent:** Murat (bmad-test-architect)
- **Expected:** Test framework scaffold
- **A2A Command:** `initialize test framework for the project`
- **Verify:** Agent scaffolds test infrastructure
- **Priority:** P1
- **Pass Criteria:** Agent produces framework scaffold with project structure

#### T-TEA-04: CI Setup (CI)
- **What:** Configure CI/CD quality pipeline
- **Agent:** Murat (bmad-test-architect)
- **Expected:** CI configuration for test execution
- **A2A Command:** `CI setup for automated testing pipeline`
- **Verify:** Agent produces CI configuration
- **Priority:** P1
- **Pass Criteria:** Agent creates CI pipeline configuration

#### T-TEA-05: ATDD
- **What:** Generate failing tests (TDD red phase)
- **Agent:** Murat (bmad-test-architect)
- **Expected:** Acceptance tests based on stakeholder criteria
- **A2A Command:** `generate ATDD tests for the user login feature`
- **Verify:** Agent produces failing acceptance tests
- **Priority:** P1
- **Pass Criteria:** Agent generates failing tests matching acceptance criteria

#### T-TEA-06: Test Automation (TA)
- **What:** Expand test coverage
- **Agent:** Murat (bmad-test-architect)
- **Expected:** Expanded test suite
- **A2A Command:** `automate tests to expand coverage for the API`
- **Verify:** Agent produces automated tests with patterns and utilities
- **Priority:** P1
- **Pass Criteria:** Agent produces comprehensive test suite

#### T-TEA-07: Test Review (RV)
- **What:** Quality audit with scoring
- **Agent:** Murat (bmad-test-architect)
- **Expected:** Review report with 0-100 scoring
- **A2A Command:** `review test quality for the project`
- **Verify:** Agent produces scored review report
- **Priority:** P1
- **Pass Criteria:** Agent produces test review with numerical score

#### T-TEA-08: NFR Assessment (NR)
- **What:** Non-functional requirements evaluation
- **Agent:** Murat (bmad-test-architect)
- **Expected:** NFR report covering performance, security, etc.
- **A2A Command:** `NFR assessment for performance and security`
- **Verify:** Agent produces NFR evaluation report
- **Priority:** P1
- **Pass Criteria:** Agent produces NFR report with assessment categories

#### T-TEA-09: Traceability (TRC)
- **What:** Coverage traceability and gate
- **Agent:** Murat (bmad-test-architect)
- **Expected:** Traceability matrix linking tests to requirements
- **A2A Command:** `traceability matrix for all tests to requirements`
- **Verify:** Agent produces traceability matrix with gate decision
- **Priority:** P1
- **Pass Criteria:** Agent maps tests to requirements with coverage percentage

#### T-TEA-10: TEA Agent Persona — Murat
- **What:** Verify Murat persona consistency
- **Expected:** Data + gut instinct, risk calculations, impact assessments
- **A2A Command:** `what is your testing philosophy?`
- **Verify:** Response matches Murat's communication style (strong opinions weakly held)
- **Priority:** P1
- **Pass Criteria:** Agent maintains distinctive Murat persona

#### T-TEA-11: TEA Knowledge Base Access
- **What:** Agent references TEA knowledge files
- **Expected:** Agent uses knowledge from tea-index.csv and knowledge/ folder
- **A2A Command:** `explain risk-based testing methodology as TEA expert`
- **Verify:** Agent references TEA knowledge patterns
- **Priority:** P2
- **Pass Criteria:** Agent demonstrates knowledge of TEA methodology

#### T-TEA-12: TEA Integration with PRD
- **What:** TEA reads PRD for test traceability
- **Expected:** Agent references PRD requirements when designing tests
- **A2A Command:** `create test design based on the PRD requirements`
- **Verify:** Agent reads PRD and maps requirements to test cases
- **Priority:** P1
- **Pass Criteria:** Agent creates tests traced to specific PRD requirements

---

### 3.10 Configuration & Customization

#### T-CFG-01: BMAD Init
- **What:** Initialize BMAD workspace
- **Expected:** bmad-init.sh runs, creates .a0proj/instructions/ files, state file, config
- **A2A Command:** `initialize bmad`
- **Verify:** Agent runs init script, reports directories and instruction files created
- **Priority:** P0
- **Pass Criteria:** Agent creates BMAD workspace structure with config and state files

#### T-CFG-02: BMAD Customize — Discovery
- **What:** List customizable skills
- **Expected:** Agent discovers and lists agents/workflows with customization support
- **A2A Command:** `customize bmad — what can I customize?`
- **Verify:** Agent runs list_customizable_skills.py, groups results by agent/workflow
- **Priority:** P1
- **Pass Criteria:** Agent lists available customization surfaces

#### T-CFG-03: BMAD Customize — Apply Override
- **What:** Apply a customization override
- **Expected:** Agent creates TOML override in _bmad/custom/
- **A2A Command:** `customize the PM agent to use a more formal communication style`
- **Verify:** Agent reads customize.toml, composes override, writes TOML file, verifies with resolver
- **Priority:** P1
- **Pass Criteria:** Agent produces correct TOML override and verifies merge

#### T-CFG-04: BMAD Promote Agent
- **What:** Promote agent from project to plugin scope
- **Expected:** Agent copies from .a0proj/agents/ to plugin agents/
- **A2A Command:** `promote agent security-scanner`
- **Verify:** Agent validates source, checks target, confirms, copies
- **Priority:** P0
- **Pass Criteria:** Agent promotes agent correctly with safety checks

#### T-CFG-05: BMAD Promote Workflow
- **What:** Promote workflow from project to plugin scope
- **Expected:** Agent copies from .a0proj/skills/ to plugin skills/
- **A2A Command:** `promote workflow dependency-update`
- **Verify:** Agent validates, confirms, copies workflow
- **Priority:** P0
- **Pass Criteria:** Agent promotes workflow correctly with safety checks

#### T-CFG-06: Configuration State Management
- **What:** Verify state file reading and updates
- **Expected:** Agent correctly reads/writes 02-bmad-state.md
- **A2A Command:** `what is the current BMAD state?`
- **Verify:** Agent reads phase, persona, and project state correctly
- **Priority:** P0
- **Pass Criteria:** Agent accurately reports and manages state

---

### 3.11 Teams & Party Mode

#### T-TEAM-01: Party Mode Activation
- **What:** Activate multi-agent discussion
- **Expected:** Party mode facilitator activates, loads agent manifest, welcomes all agents
- **A2A Command:** `party mode`
- **Verify:** Agent loads manifest CSV, activates party mode, shows welcome with agent list
- **Priority:** P1
- **Pass Criteria:** Multiple agent personas respond, each maintaining their character

#### T-TEAM-02: Party Mode Discussion
- **What:** Multi-agent conversation on a topic
- **Expected:** 2-3 agents respond with their unique perspectives
- **A2A Command:** (after party mode active) `what approach should we take for the API design?`
- **Verify:** Different agents respond with their domain expertise (architect=tech, PM=business, etc.)
- **Priority:** P1
- **Pass Criteria:** Multiple agents contribute with distinct perspectives and styles

#### T-TEAM-03: Party Mode — Address Specific Agent
- **What:** Direct message to specific agent in party
- **Expected:** Named agent prioritized in response
- **A2A Command:** (after party mode) `Winston, what's your take on microservices here?`
- **Verify:** Winston/Architect persona responds as primary
- **Priority:** P2
- **Pass Criteria:** Addressed agent responds first with their expertise

#### T-TEAM-04: Party Mode — Creative Squad
- **What:** CIS creative-squad team activation
- **Expected:** CIS agents collaborate on creative challenge
- **A2A Command:** `creative squad — brainstorm new product naming ideas`
- **Verify:** CIS agents (Victor, Carson, Maya, etc.) collaborate
- **Priority:** P2
- **Pass Criteria:** Multiple CIS agents contribute with creative approaches

#### T-TEAM-05: Party Mode Exit
- **What:** Graceful exit from party mode
- **Expected:** Facilitator provides summary and exits party mode
- **A2A Command:** `exit party mode`
- **Verify:** Agent provides summary, returns to normal mode
- **Priority:** P2
- **Pass Criteria:** Party mode ends cleanly with summary

---

### 3.12 Routing & Orchestration

#### T-ROUTE-01: Natural Language Routing
- **What:** BMad Master routes natural language to correct agent
- **Expected:** Master identifies intent and routes to appropriate specialist
- **A2A Command:** `I need to define the technical architecture for my project`
- **Verify:** Master routes to Winston (bmad-architect) via call_subordinate
- **Priority:** P0
- **Pass Criteria:** Correct agent activated based on natural language intent

#### T-ROUTE-02: Menu Code Routing
- **What:** Route using 2-letter menu code
- **Expected:** Master activates correct workflow for code
- **A2A Command:** `CA` (Create Architecture menu code)
- **Verify:** Master routes to bmad-create-architecture via Winston
- **Priority:** P0
- **Pass Criteria:** Menu code correctly maps to workflow and agent

#### T-ROUTE-03: Ambiguous Request Routing
- **What:** Ambiguous request that could match multiple agents
- **Expected:** Master shows list of matches and asks user to pick
- **A2A Command:** `review` (could be code review, test review, editorial review, etc.)
- **Verify:** Master shows multiple matching options and asks for clarification
- **Priority:** P0
- **Pass Criteria:** Agent lists matching options instead of guessing

#### T-ROUTE-04: Phase-Gated Routing
- **What:** Verify routing respects phase gates
- **Expected:** Implementation workflows not suggested when in planning phase
- **A2A Command:** (set state to 2-planning) `bmad help`
- **Verify:** Only planning-relevant workflows shown, implementation hidden
- **Priority:** P1
- **Pass Criteria:** Routing table filtered by current phase

#### T-ROUTE-05: Artifact Completion Detection
- **What:** Verify routing extension detects completed artifacts
- **Expected:** Completed phases shown in routing manifest
- **A2A Command:** `bmad help` (after creating a PRD)
- **Verify:** Extension reports phase completion from filesystem scan
- **Priority:** P1
- **Pass Criteria:** Completed phases correctly detected and reported

#### T-ROUTE-06: Staleness Warnings
- **What:** Verify artifact staleness detection
- **Expected:** Warnings when parent artifact newer than child
- **A2A Command:** (modify PRD after architecture created) `bmad help`
- **Verify:** Extension warns that architecture may be stale
- **Priority:** P2
- **Pass Criteria:** Staleness warnings emitted when parent > child mtime

#### T-ROUTE-07: Cross-Module Routing
- **What:** Route to different module agents
- **Expected:** Master can route to BMB, CIS, TEA agents
- **A2A Command:** `I need to create a custom workflow for our team`
- **Verify:** Master routes to Wendy (bmad-workflow-builder) in BMB module
- **Priority:** P0
- **Pass Criteria:** Cross-module routing works correctly

---

### 3.13 Edge Cases & Error Handling

#### T-EDGE-01: Invalid Menu Code
- **What:** User provides unrecognized menu code
- **Expected:** Master informs code not found, shows similar options
- **A2A Command:** `XX`
- **Verify:** Agent handles gracefully, suggests valid codes
- **Priority:** P1
- **Pass Criteria:** Agent provides helpful error message

#### T-EDGE-02: Missing Prerequisites
- **What:** Request workflow without prerequisites
- **Expected:** Agent identifies missing prerequisites and recommends them
- **A2A Command:** `sprint planning` (without PRD/architecture/epics)
- **Verify:** Agent detects missing prerequisites and informs user
- **Priority:** P1
- **Pass Criteria:** Agent checks prerequisites before proceeding

#### T-EDGE-03: Workflow Interruption
- **What:** Mid-workflow topic change
- **Expected:** Agent handles gracefully, offers to save or discard progress
- **A2A Command:** (mid-PRD creation) `actually, let's brainstorm instead`
- **Verify:** Agent transitions without crashing
- **Priority:** P2
- **Pass Criteria:** Agent handles context switch gracefully

#### T-EDGE-04: Empty Project
- **What:** BMAD commands on empty/fresh project
- **Expected:** Agent guides through initialization or first steps
- **A2A Command:** `what should I work on first?`
- **Verify:** Agent recommends initialization or product brief
- **Priority:** P1
- **Pass Criteria:** Agent provides appropriate guidance for fresh project

#### T-EDGE-05: Concurrent Workflow Requests
- **What:** Multiple workflow requests in one message
- **Expected:** Agent handles sequentially or asks to prioritize
- **A2A Command:** `create architecture and then sprint planning`
- **Verify:** Agent handles multiple requests appropriately
- **Priority:** P2
- **Pass Criteria:** Agent processes or prioritizes multiple requests

#### T-EDGE-06: Customization Without Target
- **What:** Customize without specifying target
- **Expected:** Agent enters discovery mode to find customizable skills
- **A2A Command:** `customize something`
- **Verify:** Agent enters Step 2 discovery, lists available customizations
- **Priority:** P2
- **Pass Criteria:** Agent gracefully enters discovery when target unclear

#### T-EDGE-07: Promote Nonexistent Agent
- **What:** Promote agent that does not exist
- **Expected:** Agent informs source not found, lists available
- **A2A Command:** `promote agent nonexistent-agent`
- **Verify:** Agent lists available agents in project scope
- **Priority:** P2
- **Pass Criteria:** Agent provides helpful error with available options

---

## 4. Test Execution Order

### Phase 1: Foundation (P0 — Must Work)

Tests that must pass for the plugin to be considered functional.

```
1. T-INIT-01  — BMAD Help (basic functionality)
2. T-INIT-13 — Not Initialized (edge case)
3. T-CFG-01  — BMAD Init (prerequisite for everything)
4. T-CFG-06  — State Management (verify init worked)
5. T-INIT-03 — BMAD Master Activation
6. T-ROUTE-01 — Natural Language Routing
7. T-ROUTE-02 — Menu Code Routing
8. T-ROUTE-03 — Ambiguous Request Routing
9. T-ROUTE-07 — Cross-Module Routing
n10. T-BMM-05 — Create Product Brief (first BMM workflow)
11. T-BMM-07 — Create PRD (core planning)
12. T-BMM-11 — Create Architecture (core solutioning)
13. T-BMM-12 — Create Epics and Stories
14. T-BMM-13 — Check Implementation Readiness
15. T-BMM-14 — Sprint Planning
16. T-BMM-16 — Create Story
17. T-BMM-18 — Dev Story
18. T-BMM-19 — Code Review
19. T-BMM-26 — Quick Spec
20. T-BMM-27 — Quick Dev
21. T-BMB-01 — Build Agent (core BMB)
22. T-BMB-04 — Build Workflow (core BMB)
23. T-BMB-12 — Create Module (core BMB)
24. T-CFG-04 — Promote Agent
25. T-CFG-05 — Promote Workflow
26. T-TEA-02 — Test Design (core TEA)
```

### Phase 2: Extended Functionality (P1 — Should Work)

```
27. T-INIT-02 — BMAD Status
28. T-INIT-14 — Phase-Aware Routing
29. T-INIT-08 — Adversarial Review
30. T-INIT-10 — Advanced Elicitation
31. T-INIT-12 — Brainstorming (Core)
32. T-BMM-01 — Brainstorm Project
33. T-BMM-02 — Market Research
34. T-BMM-03 — Domain Research
35. T-BMM-04 — Technical Research
36. T-BMM-08 — Validate PRD
37. T-BMM-09 — Edit PRD
38. T-BMM-10 — Create UX Design
39. T-BMM-15 — Sprint Status
40. T-BMM-17 — Validate Story
41. T-BMM-20 — QA Automation
42. T-BMM-21 — Correct Course
43. T-BMM-23 — Retrospective
44. T-BMM-24 — Document Project
45. T-BMM-25 — Generate Project Context
46. T-BMM-28 — Write Document
47. T-BMB-02 — Edit Agent
48. T-BMB-03 — Validate Agent
49. T-BMB-05 — Edit Workflow
50. T-BMB-06 — Validate Workflow
51. T-BMB-10 — Ideate Module
52. T-BMB-11 — Create Module Brief
53. T-BMB-13 — Edit Module
54. T-BMB-14 — Validate Module
55. T-BMB-15 — Setup Builder
56. T-CIS-01 — Innovation Strategy
57. T-CIS-02 — Problem Solving
58. T-CIS-03 — Design Thinking
59. T-CIS-04 — Brainstorming (CIS)
60. T-CIS-07 — Persona: Victor
61. T-CIS-08 — Persona: Carson
62. T-CIS-10 — Persona: Dr. Quinn
63. T-TEA-01 — Teach Me Testing
64. T-TEA-03 — Test Framework
65. T-TEA-04 — CI Setup
66. T-TEA-05 — ATDD
67. T-TEA-06 — Test Automation
68. T-TEA-07 — Test Review
69. T-TEA-08 — NFR Assessment
70. T-TEA-09 — Traceability
71. T-TEA-10 — Persona: Murat
72. T-TEA-12 — TEA-PRD Integration
73. T-CFG-02 — Customize Discovery
74. T-CFG-03 — Customize Apply
75. T-ROUTE-04 — Phase-Gated Routing
76. T-ROUTE-05 — Artifact Completion
77. T-TEAM-01 — Party Mode Activation
78. T-TEAM-02 — Party Mode Discussion
79. T-EDGE-01 — Invalid Menu Code
80. T-EDGE-02 — Missing Prerequisites
81. T-EDGE-04 — Empty Project
```

### Phase 3: Polish (P2 — Nice to Verify)

```
82. T-INIT-04 — Index Docs
83. T-INIT-05 — Shard Document
84. T-INIT-06 — Editorial Review Prose
85. T-INIT-07 — Editorial Review Structure
86. T-INIT-09 — Edge Case Hunter
87. T-INIT-11 — Distillator
88. T-BMM-06 — Working Backwards / PRFAQ
89. T-BMM-22 — Checkpoint Review
90. T-BMM-29 — Update Standards
91. T-BMM-30 — Mermaid Generate
92. T-BMM-31 — Validate Document
93. T-BMM-32 — Explain Concept
94. T-BMB-07 — Max Parallel Validate
95. T-BMB-08 — Convert Skill
96. T-BMB-09 — Rework Workflow
97. T-BMB-16 — Quality Scan Agent
98. T-BMB-17 — Quality Scan Workflow
99. T-BMB-18 — Validate Skill + File Refs
100. T-CIS-05 — Storytelling
101. T-CIS-06 — Presentation
102. T-CIS-09 — Persona: Maya
103. T-CIS-11 — Persona: Sophia
104. T-CIS-12 — Persona: Caravaggio
105. T-TEA-11 — TEA Knowledge Base
106. T-ROUTE-06 — Staleness Warnings
107. T-TEAM-03 — Party Mode Address Agent
108. T-TEAM-04 — Creative Squad
109. T-TEAM-05 — Party Mode Exit
110. T-EDGE-03 — Workflow Interruption
111. T-EDGE-05 — Concurrent Requests
112. T-EDGE-06 — Customize Without Target
113. T-EDGE-07 — Promote Nonexistent
```

---

## 5. Pass/Fail Criteria

### 5.1 Universal Pass Criteria

Every test must meet these baseline criteria:

1. **Response received** — A2A returns a non-empty response
2. **No crash/error** — Response does not contain unhandled exceptions or stack traces
3. **Agent persona loaded** — Response reflects the expected agent's personality and communication style
4. **Skill/workflow activated** — Response shows evidence of correct skill or workflow being loaded

### 5.2 Module-Specific Pass Criteria

| Module | Pass Criteria |
|--------|--------------|
| **INIT** | Agent reads state correctly; routing table injected; help menu complete |
| **BMM Analysis** | Agent adopts Mary persona; research/brief workflows produce structured output |
| **BMM Planning** | Agent adopts John/Sally persona; PRD/UX workflows produce required artifacts |
| **BMM Solutioning** | Agent adopts Winston/John persona; architecture/epics produce structured docs |
| **BMM Implementation** | Agent adopts Bob/Amelia/Quinn persona; story/dev/QA workflows execute correctly |
| **BMM Quick Flow** | Agent adopts Barry persona; quick spec/dev bypass full planning |
| **BMM Tech Writer** | Agent adopts Paige persona; documentation tasks produce quality output |
| **BMB Agent** | Agent adopts Bond persona; agent creation produces valid YAML + prompts |
| **BMB Workflow** | Agent adopts Wendy persona; workflow creation produces valid workflow.md + steps |
| **BMB Module** | Agent adopts Morgan persona; module creation produces complete package |
| **CIS** | Agent adopts respective CIS persona (Victor/Carson/Maya/Dr.Quinn/Sophia/Caravaggio); creative workflows produce structured output |
| **TEA** | Agent adopts Murat persona; test workflows produce test artifacts with risk scoring |
| **Config** | Init creates workspace; customize produces valid TOML; promote copies correctly |
| **Teams** | Party mode activates with manifest; agents maintain character in group |
| **Routing** | Phase-aware routing works; artifact detection works; staleness warnings work |

### 5.3 Severity Levels for Failures

| Severity | Definition | Action |
|----------|-----------|--------|
| **Blocker** | Core routing/init broken; no agent can be activated | Fix immediately, cannot release |
| **Critical** | Primary workflow (PRD, architecture, dev) broken | Fix before release |
| **Major** | Secondary workflow broken but workaround exists | Fix in next iteration |
| **Minor** | Cosmetic issue, persona inconsistency, minor UX | Fix when convenient |
| **Trivial** | Edge case unlikely in real usage | Log for future improvement |

### 5.4 Overall Test Suite Pass Criteria

| Metric | Threshold |
|--------|-----------|
| P0 tests passing | 100% (all 26 must pass) |
| P1 tests passing | ≥ 90% (at least 49 of 55) |
| P2 tests passing | ≥ 70% (at least 24 of 34) |
| No Blocker severity failures | 0 |
| No Critical severity failures | 0 |

---

## 6. Test Execution Notes

### 6.1 A2A Session Considerations

- A2A sessions are stateless between messages. Each test must be self-contained.
- For multi-step workflows (PRD creation, architecture design), the test verifies the FIRST step only — confirming the correct agent activates and begins the process.
- Full end-to-end workflow testing requires maintaining session state, which should be done as a separate manual testing phase.

### 6.2 A2A Endpoint

```
URL: https://testing.emichi.co/a2a/t-8a-vdZDQ1xJoX9gN/p-caveman
Protocol: A2A (Agent-to-Agent)
Method: POST
```

### 6.3 Recommended Testing Approach

1. **Automated Shell Script**: Send A2A messages via curl, parse responses for expected patterns
2. **Manual Verification**: For persona consistency and creative output quality
3. **Log Analysis**: Check Docker container logs for routing extension injection, skill loading, agent activation

### 6.4 Test Automation Template

~~~bash
#!/bin/bash
# Test runner template for BMAD A2A testing

URL="https://testing.emichi.co/a2a/t-8a-vdZDQ1xJoX9gN/p-caveman"

run_test() {
    local test_id="$1"
    local message="$2"
    local expected_pattern="$3"
    
    echo "Running $test_id: $message"
    response=$(curl -s -X POST "$URL" \
        -H "Content-Type: application/json" \
        -d "{\"message\": \"$message\"}")
    
    if echo "$response" | grep -qi "$expected_pattern"; then
        echo "  ✅ PASS"
    else
        echo "  ❌ FAIL — expected: $expected_pattern"
        echo "  Response: $(echo "$response" | head -c 200)"
    fi
}

# Example tests
run_test "T-INIT-01" "bmad help" "module"
run_test "T-INIT-13" "create a PRD" "init"
~~~

---

## Appendix A: Complete Agent Manifest

| Profile | Persona Name | Title | Module | Character Style
|---------|-------------|-------|--------|----------------
| `bmad-analyst` | Mary | Business Analyst | BMM | Treasure hunt excitement, structured insights
| `bmad-pm` | John | Product Manager | BMM | WHY detective, data-sharp, direct
| `bmad-architect` | Winston | Architect | BMM | Calm, pragmatic, boring tech champion
| `bmad-sm` | Bob | Scrum Master | BMM | Crisp, checklist-driven, zero ambiguity
| `bmad-dev` | Amelia | Developer | BMM | Ultra-succinct, file paths, AC IDs
| `bmad-qa` | Quinn | QA Engineer | BMM | Test automation focused
| `bmad-quick-dev` | Barry | Quick Flow Solo Dev | BMM | Direct, confident, implementation-first
| `bmad-ux-designer` | Sally | UX Designer | BMM | Paints with words, empathetic storytelling
| `bmad-tech-writer` | Paige | Technical Writer | BMM | Patient educator, clarity champion
| `bmad-agent-builder` | Bond | Agent Building Expert | BMB | (Builder persona)
| `bmad-workflow-builder` | Wendy | Workflow Building Master | BMB | (Builder persona)
| `bmad-module-builder` | Morgan | Module Creation Master | BMB | (Builder persona)
| `bmad-innovation` | Victor | Innovation Strategist | CIS | Chess grandmaster, bold declarations
| `bmad-brainstorming-coach` | Carson | Brainstorming Coach | CIS | Enthusiastic improv, YES AND energy
| `bmad-design-thinking` | Maya | Design Thinking Coach | CIS | Jazz musician, sensory metaphors
| `bmad-problem-solver` | Dr. Quinn | Problem Solver | CIS | Sherlock + playful scientist, AHA moments
| `bmad-storyteller` | Sophia | Storyteller | CIS | Bard-like, flowery, whimsical
| `bmad-presentation` | Caravaggio | Presentation Master | CIS | Creative director, dramatic reveals
| `bmad-test-architect` | Murat | Test Architect | TEA | Data + gut instinct, risk calculations
| `bmad-master` | Master | BMad Master | Core | Orchestrator, router, guide |

## Appendix B: Complete Menu Code Reference

### BMM Codes
| Code | Name | Agent | Phase |
|------|------|-------|-------|
| BP | Brainstorm Project | Mary | 1-analysis |
| MR | Market Research | Mary | 1-analysis |
| DR | Domain Research | Mary | 1-analysis |
| TR | Technical Research | Mary | 1-analysis |
| CB | Create Brief | Mary | 1-analysis |
| WB | Working Backwards | Mary | 1-analysis |
| CP | Create PRD | John | 2-planning |
| VP | Validate PRD | John | 2-planning |
| EP | Edit PRD | John | 2-planning |
| CU | Create UX | Sally | 2-planning |
| CA | Create Architecture | Winston | 3-solutioning |
| CE | Create Epics/Stories | John | 3-solutioning |
| IR | Implementation Readiness | Winston | 3-solutioning |
| SP | Sprint Planning | Bob | 4-implementation |
| SS | Sprint Status | Bob | 4-implementation |
| CS | Create Story | Bob | 4-implementation |
| VS | Validate Story | Bob | 4-implementation |
| DS | Dev Story | Amelia | 4-implementation |
| CR | Code Review | Amelia | 4-implementation |
| QA | QA Automation | Quinn | 4-implementation |
| CC | Correct Course | Bob | anytime |
| CK | Checkpoint Review | Amelia | 4-implementation |
| ER | Retrospective | Bob | 4-implementation |
| DP | Document Project | Mary | anytime |
| GPC | Generate Project Context | Mary | anytime |
| QS | Quick Spec | Barry | anytime |
| QD | Quick Dev | Barry | anytime |
| WD | Write Document | Paige | anytime |
| US | Update Standards | Paige | anytime |
| MG | Mermaid Generate | Paige | anytime |
| VD | Validate Document | Paige | anytime |
| EC | Explain Concept | Paige | anytime |

### BMB Codes
| Code | Name | Agent |
|------|------|-------|
| BA | Build Agent | Bond |
| EA | Edit Agent | Bond |
| VA | Validate Agent | Bond |
| BW | Build Workflow | Wendy |
| EW | Edit Workflow | Wendy |
| VW | Validate Workflow | Wendy |
| MV | Max Parallel Validate | Wendy |
| CW | Convert Skill | Wendy |
| RW | Rework Workflow | Wendy |
| IM | Ideate Module | Morgan |
| PB | Create Module Brief | Morgan |
| CM | Create Module | Morgan |
| EM | Edit Module | Morgan |
| VM | Validate Module | Morgan |
| SB | Setup Builder | Wendy |
| QA | Quality Scan Agent | Bond |
| QW | Quality Scan Workflow | Wendy |
| VS | Validate Skill | Wendy |
| VF | Validate File Refs | Wendy |

### CIS Codes
| Code | Name | Agent |
|------|------|-------|
| IS | Innovation Strategy | Victor |
| PS | Problem Solving | Dr. Quinn |
| DT | Design Thinking | Maya |
| BS | Brainstorming | Carson |
| ST | Storytelling | Sophia |
| PR | Presentation | Caravaggio |

### TEA Codes
| Code | Name | Agent |
|------|------|-------|
| TMT | Teach Me Testing | Murat |
| TD | Test Design | Murat |
| TF | Test Framework | Murat |
| CI | CI Setup | Murat |
| AT | ATDD | Murat |
| TA | Test Automation | Murat |
| RV | Test Review | Murat |
| NR | NFR Assessment | Murat |
| TRC | Traceability | Murat |

### INIT (Core) Codes
| Code | Name | Agent |
|------|------|-------|
| BSP | Brainstorming | Master |
| PM | Party Mode | Master |
| BH | bmad-help | Master |
| ID | Index Docs | Master |
| SD | Shard Document | Master |
| ERP | Editorial Review Prose | Master |
| ES | Editorial Review Structure | Master |
| AR | Adversarial Review | Master |
| ECH | Edge Case Hunter | Master |
| AE | Advanced Elicitation | Master |
| DG | Distillator | Master |
