# BMAD Method for Agent Zero

**Structured AI-assisted software development — from idea to shipped code.**

BMAD (Business Method for Agile Development) is a structured AI-first product development framework. This plugin provides a full drop-in integration: 20 specialized agent personas, 5 global skills, and the complete workflow library — ready to use inside Agent Zero.

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

## How It Works

BMAD organizes software development into phases — Ideation → Planning → Architecture → Implementation → Testing. Each phase has one or more specialist agents who own it.

You start every session by talking to **BMad Master**, the orchestrator. It reads your project state and routes you to the right specialist. Specialists produce artifacts — briefs, PRDs, architecture docs, user stories, test plans — that the next phase consumes.

Project state is tracked across sessions. Decisions made by the architect are visible to the developer. The sprint board survives restarts.

~~~
User → BMad Master → [routes to specialist] → artifact produced → state updated → next phase
~~~

---

## Modules

| Module | Skill | Purpose |
|--------|-------|----------|
| **BMM** — Business Method Module | `bmad-bmm` | Full product lifecycle: discovery → planning → architecture → implementation |
| **BMB** — Builder Module | `bmad-bmb` | Meta-module for creating and extending BMAD agents, workflows, and modules |
| **TEA** — Testing Excellence Accelerator | `bmad-tea` | Test architecture, ATDD, automation, CI, NFR assessment |
| **CIS** — Creative Intelligence Suite | `bmad-cis` | Innovation strategy, design thinking, storytelling, structured problem solving |

---

## Agent Roster

| Agent | Persona | Commands | Module |
|-------|---------|----------|--------|
| bmad-master | BMad Master 🧙 | `LT` `LW` `AE` `DG` `PM` | Core |
| bmad-analyst | Mary 📊 | `BP` `MR` `DR` `TR` `CB` `WB` `DP` `GPC` | BMM |
| bmad-pm | John 📋 | `CP` `VP` `EP` `CE` `IR` `CC` | BMM |
| bmad-ux-designer | Sally 🎨 | `CU` | BMM |
| bmad-architect | Winston 🏗️ | `CA` `IR` | BMM |
| bmad-dev | Amelia 💻 | `DS` `CR` `CHK` | BMM |
| bmad-qa | Quinn 🧪 | `QA` | BMM |
| bmad-sm | Bob 🏃 | `SP` `CS` `VS` `SS` `ER` `CC` | BMM |
| bmad-quick-dev | Barry 🚀 | `QS` `QD` `CR` | BMM |
| bmad-tech-writer | Paige 📚 | `DP` `WD` `US` `MG` `VD` `EC` | BMM |
| bmad-test-architect | Murat 🔬 | `TMT` `TF` `AT` `TA` `TD` `TRC` `NR` `CI` `RV` | TEA |
| bmad-brainstorming-coach | Carson 🧠 | `BS` | CIS |
| bmad-design-thinking | Maya 🎭 | `DT` | CIS |
| bmad-innovation | Victor ⚡ | `IS` | CIS |
| bmad-storyteller | Sophia 📖 | `ST` | CIS |
| bmad-problem-solver | Dr. Quinn 🔬 | `PS` | CIS |
| bmad-presentation | Caravaggio 🎨 | `SD` `EX` `PD` `CT` `IN` `VM` `CV` | CIS |
| bmad-agent-builder | Bond 🤖 | `CA` `EA` `VA` | BMB |
| bmad-workflow-builder | Wendy 🔄 | `CW` `EW` `VW` `MV` `RW` | BMB |
| bmad-module-builder | Morgan 🏗️ | `PB` `CM` `EM` `VM` | BMB |

---

## Prompt Architecture

Each BMAD agent is built from a clean 3-layer boundary:

~~~
┌─────────────────────────────────────────────────────────┐
│  Agent Prompts  (WHO the agent is)                      │
│  role.md · communication.md · tips.md ·                 │
│  communication_additions.md                             │
├─────────────────────────────────────────────────────────┤
│  Skills  (WHAT to execute)                              │
│  SKILL.md — workflow routing, paths, execution protocol │
├─────────────────────────────────────────────────────────┤
│  Project Instructions  (WHERE the project is)           │
│  .a0proj/instructions/ — state, config, paths           │
└─────────────────────────────────────────────────────────┘
~~~

**Agent prompts** define persona, communication style, and menu presentation.
**Skills** are loaded on-demand and contain all workflow execution logic.
**Project instructions** are written by `bmad init` and contain project-specific state and configuration.

---

## Extension Pipeline

| Extension | Hook | Purpose |
|-----------|------|----------|
| `_80_bmad_routing_manifest.py` | `message_loop_prompts_after` | Dynamically builds routing manifest from `skills/*/module-help.csv`, filesystem artifact detection, and staleness warnings |

---

## Memory Architecture

- **Project-level FAISS store** — `.a0proj/memory/` — single vector database shared by all agents (structural isolation)
- **Knowledge preload** — `.a0proj/knowledge/main/` — recursive FAISS scan on agent init
- **No per-agent stores** — project-level isolation with cross-agent recall by design

---

## Dashboard

BMAD ships a live project status dashboard. After installation, the BMAD button appears in Agent Zero's sidebar.

The dashboard is **read-only** — it observes agent state without writing to it.

---

## Version

**Plugin:** 1.0.4
**Upstream versions:** Core 6.2.2 · BMB 1.5.0 · TEA 1.9.1 · CIS 0.1.9

See [CHANGELOG.md](./CHANGELOG.md) for full version history.

---

## Documentation

- [Architecture Alignment Report v1.0.3](/.a0proj/_bmad-output/planning-artifacts/architecture-bmad-a0-alignment.md) — canonical system architecture reference
- [Document Lifecycle Framework](./docs/document-lifecycle.md) — artifact staleness detection and consistency checks
- [Memory Architecture](/.a0proj/knowledge/main/memory-architecture.md) — FAISS-native reference

---

## Links

- [BMAD-METHOD Core](https://github.com/bmad-code-org/BMAD-METHOD)
- [bmad-builder (BMB)](https://github.com/bmad-code-org/bmad-builder)
- [bmad-method-test-architecture-enterprise (TEA)](https://github.com/bmad-code-org/bmad-method-test-architecture-enterprise)
- [bmad-module-creative-intelligence-suite (CIS)](https://github.com/bmad-code-org/bmad-module-creative-intelligence-suite)

---

## Requirements

- [Agent Zero](https://github.com/frdel/agent-zero) (latest stable release)
- An LLM with large context window recommended (Claude Sonnet or better)
