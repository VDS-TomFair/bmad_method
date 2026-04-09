# BMAD Method for Agent Zero

[![Version](https://img.shields.io/badge/version-1.0.5-blue)]() [![License: MIT](https://img.shields.io/badge/license-MIT-green)]() [![Agent Zero](https://img.shields.io/badge/A0-compatible-brightgreen)]()

**Structured AI-assisted software development — from idea to shipped code.**

BMAD (Business Method for Agile Development) is a structured AI-first product development framework. This plugin provides a full drop-in Agent Zero integration: 20 specialized agent personas, 5 global skills, and the complete workflow library.

---

## Quick Start

**1. Install the plugin**

~~~bash
git clone https://github.com/vanja-emichi/bmad_method.git usr/plugins/bmad-method
~~~

**2. Initialize a BMAD project**

Select the **BMad Master** profile in Agent Zero, then run:

~~~
bmad init
~~~

This creates the project workspace and initializes project-scoped memory.

**3. Start building**

Tell BMad Master what you want to build. It routes you to the right specialist for your current phase — no manual agent selection needed.

---

## How It Works

BMAD organizes development into phases — Ideation → Planning → Architecture → Implementation → Testing. Each phase has specialist agents who own it.

You talk to **BMad Master**, the orchestrator. It reads project state and routes you to the right specialist. Specialists produce artifacts that the next phase consumes. State persists across sessions.

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

## Skills Architecture

Each BMAD module ships as an Agent Zero skill containing a `SKILL.md` manifest, a `module-help.csv` routing table, and a `workflows/` directory with step files. Skills are loaded on-demand — agents call `skills_tool:load` to get workflow instructions, then execute them exactly as defined. No workflow logic lives in agent prompts.

---

## Prompt Architecture

Each agent is built from a clean 3-layer boundary:

~~~
┌─────────────────────────────────────────────────────────┐
│  Agent Prompts  (WHO the agent is)                      │
│  role.md · communication.md · tips.md                   │
├─────────────────────────────────────────────────────────┤
│  Skills  (WHAT to execute)                              │
│  SKILL.md — workflow routing, paths, execution protocol │
├─────────────────────────────────────────────────────────┤
│  Project Instructions  (WHERE the project is)           │
│  Project config + state                                 │
└─────────────────────────────────────────────────────────┘
~~~

**Agent prompts** define persona, communication style, and menu presentation. **Skills** contain all workflow execution logic. **Project instructions** are written by `bmad init` and contain project-specific state and configuration.

---

## Extension Pipeline

| Extension | Hook | Purpose |
|-----------|------|----------|
| `_80_bmad_routing_manifest.py` | `message_loop_prompts_after` | Dynamically builds routing manifest from skill routing tables with artifact detection and staleness warnings |

---

## Memory Architecture

- **Project-level FAISS store** — single vector database shared by all agents (structural isolation)
- **Knowledge preload** — recursive FAISS scan on agent init
- **No per-agent stores** — cross-agent recall by design

---

## Dashboard

BMAD ships a live project status dashboard. After installation, the BMAD button appears in Agent Zero's sidebar. The dashboard is **read-only** — it observes agent state without writing to it.

---

## Documentation

| Document | Description |
|----------|-------------|
| [Quick Start](#quick-start) | Clone and initialize a BMAD project |
| [Document Lifecycle](./docs/document-lifecycle.md) | Artifact staleness detection and consistency checks |
| [CHANGELOG](./CHANGELOG.md) | Full version history |
| [BMAD-METHOD Core](https://github.com/bmad-code-org/BMAD-METHOD) | Upstream framework architecture reference |
| [Agent Zero](https://github.com/frdel/agent-zero) | Host platform |

---

## Version

**Plugin:** 1.0.4 | **Upstream:** Core 6.2.2 · BMB 1.5.0 · TEA 1.9.1 · CIS 0.1.9

See [CHANGELOG.md](./CHANGELOG.md) for full version history.

---

## Requirements

- [Agent Zero](https://github.com/frdel/agent-zero) (latest stable release)
- An LLM with large context window recommended (Claude Sonnet or better)

---

## Links

- [BMAD-METHOD Core](https://github.com/bmad-code-org/BMAD-METHOD)
- [bmad-builder (BMB)](https://github.com/bmad-code-org/bmad-builder)
- [bmad-method-test-architecture-enterprise (TEA)](https://github.com/bmad-code-org/bmad-method-test-architecture-enterprise)
- [bmad-module-creative-intelligence-suite (CIS)](https://github.com/bmad-code-org/bmad-module-creative-intelligence-suite)

---

## License

MIT
