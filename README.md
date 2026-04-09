# BMAD Method for Agent Zero

**Structured AI-assisted software development — from idea to shipped code.**

BMAD Method brings a proven product development framework to Agent Zero. Instead of a single general-purpose agent, you get 20 specialist personas, each owning a specific phase of the development lifecycle. They coordinate through structured workflows, maintain project state, and hand off cleanly between phases.

---

## What's New in v1.0.4

- **Party Mode Persona Guard** — FM-019 resolved: 8 prescriptive rules ensuring agents maintain distinct voices and never break character
- **prfaq (Working Backwards) workflow** — Amazon Working Backwards methodology ported from upstream with 5-step architecture
- **TEA extended knowledge** — 28 additional knowledge files for Murat (43 total), covering Pact, Playwright, NFR, and more
- **BMM Phase 2 validation** — FM-006/007/008 CLOSED: PM + UX Designer routing verified end-to-end (6/6 PASS)
- **5 consecutive zero-regression sprints** — Behavioral test suite: 69/69 PASS · Grade A+ (100/100)

---

## What's New in v1.0.3

- **Workflow sharding** — 38 step files across 6 BMM workflows, each with HALT compliance and resume capability
- **Live artifact detection** — the routing extension scans the filesystem for existing artifacts; staleness warnings surface in EXTRAS when parent artifacts are newer than children
- **Agent enrichment** — all 19 specialist agents updated with 7+ guiding principles and startup orientation
- **TEA knowledge fragments** — 14 domain-specific knowledge files for Murat, dynamically loaded across all 9 TEA workflows
- **CIS Presentation workflow** — Caravaggio (Presentation Expert) fully operational with complete CIS workflow coverage
- **Document Lifecycle Framework** — [`docs/document-lifecycle.md`](./docs/document-lifecycle.md) defines authoring, review, and staleness rules for all project artifacts
- **Behavioral test suite** — 54/54 PASS · Grade A (96/100) · 0 regressions

---

## Quick Start

**1. Install the plugin**

Install via the Agent Zero Plugin Hub, or clone directly into your Agent Zero plugins folder:

~~~bash
git clone https://github.com/vanja-emichi/bmad_method.git usr/plugins/bmad-method
~~~

**2. Initialize a BMAD project**

Select the **BMad Master** profile in Agent Zero, then run:

~~~
bmad init
~~~

This sets up the project workspace, creates the `.a0proj/` configuration directory, and initializes project-scoped memory.

**3. Start building**

Tell BMad Master what you want to build. It routes you to the right specialist for your current phase — no manual agent selection needed.

---

## What's Included

| Component | Count | Description |
|-----------|-------|-------------|
| Agent personas | 20 | Specialist agents, each with a defined role and communication style |
| Modules | 4 | BMM · BMB · TEA · CIS |
| Workflow skills | 40+ | Bundled, phase-aware workflow definitions loaded on demand |
| Routing extension | 1 | Phase-aware routing with live artifact detection and staleness warnings |

---

## How It Works

BMAD organizes software development into phases — Ideation → Planning → Architecture → Implementation → Testing. Each phase has one or more specialist agents who own it.

You start every session by talking to **BMad Master**, the orchestrator. It reads your project state and routes you to the right specialist. Specialists produce artifacts — briefs, PRDs, architecture docs, user stories, test plans — that the next phase consumes.

Project state is tracked across sessions. Decisions made by the architect are visible to the developer. The sprint board survives restarts.

~~~
User → BMad Master → [routes to specialist] → artifact produced → state updated → next phase
~~~

---

## Modules

### BMM — Business Method Module
*The full product development lifecycle.*

Covers everything from initial idea to shipped stories: market research, product briefs, PRDs, UX design, architecture, sprint planning, story writing, implementation, and code review. Eight specialist agents, each owning their phase.

**Upstream:** [BMAD-METHOD Core 6.2.2](https://github.com/bmad-code-org/BMAD-METHOD)

---

### BMB — Builder Module
*Build BMAD tooling: agents, workflows, and modules.*

For teams that want to extend BMAD itself. Three specialists — Bond (agents), Morgan (modules), Wendy (workflows) — guide you through creating, editing, and validating BMAD components that follow all framework conventions.

**Upstream:** [bmad-builder 1.5.0](https://github.com/bmad-code-org/bmad-builder)

---

### TEA — Testing Excellence Accelerator
*Enterprise-grade test architecture and automation.*

Murat, the Master Test Architect, covers risk-based test planning, ATDD, API and E2E automation, CI/CD quality gates, and test framework setup across Playwright, Cypress, pytest, JUnit, and Go test.

**Upstream:** [bmad-method-test-architecture-enterprise 1.9.1](https://github.com/bmad-code-org/bmad-method-test-architecture-enterprise)

---

### CIS — Creative Intelligence Suite
*Ideation, innovation, and strategic thinking.*

Five specialists for the creative and strategic side of product work: brainstorming, design thinking, disruptive innovation, storytelling, and visual communication and presentations.

**Upstream:** [bmad-module-creative-intelligence-suite 0.1.9](https://github.com/bmad-code-org/bmad-module-creative-intelligence-suite)

---

## Agent Roster

### BMM — Business Method Module

| Persona | Name | Role |
|---------|------|------|
| Mary | Business Analyst | Market research, competitive analysis, product briefs |
| John | Product Manager | PRD creation, requirements discovery, stakeholder alignment |
| Sally | UX Designer | User research, interaction design, UX specifications |
| Winston | Architect | System architecture, technical design decisions |
| Bob | Scrum Master | Sprint planning, story preparation, agile ceremonies |
| Amelia | Developer | Story implementation, TDD, code execution |
| Barry | Quick Dev | Rapid solo development, minimal ceremony |
| Quinn | QA Engineer | API and E2E test generation, coverage |

### BMB — Builder Module

| Persona | Name | Role |
|---------|------|------|
| Bond | Agent Builder | Create, edit, and validate BMAD agents |
| Morgan | Module Builder | Create complete BMAD modules |
| Wendy | Workflow Builder | Design, validate, and convert BMAD workflows |

### TEA — Testing Excellence Accelerator

| Persona | Name | Role |
|---------|------|------|
| Murat | Master Test Architect | Risk-based testing, ATDD, CI/CD quality gates |

### CIS — Creative Intelligence Suite

| Persona | Name | Role |
|---------|------|------|
| Carson | Brainstorming Coach | Creative facilitation, ideation techniques |
| Maya | Design Thinking Maestro | Human-centered design, empathy mapping |
| Victor | Innovation Oracle | Disruptive strategy, business model innovation |
| Sophia | Master Storyteller | Narrative craft, brand and persuasive writing |
| Caravaggio | Presentation Expert | Visual communication, slide decks, Excalidraw |

### Cross-Module

| Persona | Name | Role |
|---------|------|------|
| BMad Master | Orchestrator | Phase routing, workflow orchestration, project state |
| Paige | Technical Writer | Documentation, Mermaid diagrams, OpenAPI specs |
| Dr. Quinn | Problem Solver | TRIZ, systems thinking, root cause analysis |

---

## Status Dashboard

The plugin includes an interactive WebUI panel — accessible from the Agent Zero sidebar — that displays current project phase, sprint status, story progress, and recent decisions.

The dashboard is read-only: it observes agent state without writing to it.

---

## Quality

The plugin ships with a behavioral test suite covering all routing, phase-transition, and specialist-handoff paths.

**Latest results:** 54/54 PASS · Grade A (96/100) · 0 regressions

Test artifacts: `.a0proj/_bmad-output/test-artifacts/`

---

## Version

**Plugin:** 1.0.4  
**Upstream versions:** Core 6.2.2 · BMB 1.5.0 · TEA 1.9.1 · CIS 0.1.9

See [CHANGELOG.md](./CHANGELOG.md) for full version history.

---

## Links

- [BMAD-METHOD Core](https://github.com/bmad-code-org/BMAD-METHOD)
- [bmad-builder (BMB)](https://github.com/bmad-code-org/bmad-builder)
- [bmad-method-test-architecture-enterprise (TEA)](https://github.com/bmad-code-org/bmad-method-test-architecture-enterprise)
- [bmad-module-creative-intelligence-suite (CIS)](https://github.com/bmad-code-org/bmad-module-creative-intelligence-suite)
- [Document Lifecycle Framework](./docs/document-lifecycle.md)
