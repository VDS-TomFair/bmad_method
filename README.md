# BMAD Method for Agent Zero

[![Version](https://img.shields.io/badge/version-1.1.0-blue)]() [![License: MIT](https://img.shields.io/badge/license-MIT-green)]() [![Agent Zero](https://img.shields.io/badge/A0-compatible-brightgreen)]()

**Structured AI-assisted software development — from idea to shipped code.**

BMAD (Business Method for Agile Development) is a structured AI-first product development framework. This plugin provides a full drop-in Agent Zero integration: 23 specialized agent personas, 6 global skills, and the complete workflow library.

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
| **BMK** — Marketing Module | `bmad-mkt` | Market strategy, content marketing, growth engineering, community, and analytics |

> **Note:** BMK is a default-install module. To exclude it, remove `skills/bmad-mkt/` and the 3 agent directories (`agents/bmad-marketing-strategist/`, `agents/bmad-content-manager/`, `agents/bmad-growth-engineer/`).

---

## Agent Roster

| Agent | Persona | Commands | Module |
|-------|---------|----------|--------|
| bmad-master | BMad Master 🧙 | `LT` `LW` `AE` `DG` `PM` | Core |
| bmad-analyst | Mary 📊 | `BP` `MR` `DR` `TR` `CB` `WB` `DP` `GPC` | BMM |
| bmad-pm | John 📋 | `CP` `VP` `EP` `CE` `IR` `CC` | BMM |
| bmad-ux-designer | Sally 🎨 | `CU` | BMM |
| bmad-architect | Winston 🏗️ | `CA` `IR` | BMM |
| bmad-dev | Amelia 💻 | `DS` `CR` `CK` | BMM |
| bmad-qa | Quinn 🧪 | `QA` | BMM |
| bmad-sm | Bob 🏃 | `SP` `CS` `VS` `SS` `ER` `CC` | BMM |
| bmad-quick-dev | Barry 🚀 | `QS` `QQ` `CR` | BMM |
| bmad-tech-writer | Paige 📚 | `DP` `WD` `US` `MG` `VD` `EC` | BMM |
| bmad-test-architect | Murat 🔬 | `TMT` `TF` `AT` `TA` `TD` `TR` `NR` `CI` `RV` | TEA |
| bmad-brainstorming-coach | Carson 🧠 | `BS` | CIS |
| bmad-design-thinking | Maya 🎭 | `DT` | CIS |
| bmad-innovation | Victor ⚡ | `IS` | CIS |
| bmad-storyteller | Sophia 📖 | `ST` | CIS |
| bmad-problem-solver | Dr. Quinn 🔬 | `PS` | CIS |
| bmad-presentation | Caravaggio 🎨 | `SD` `EX` `PD` `CT` `IN` `VM` `CV` | CIS |
| bmad-agent-builder | Bond 🤖 | `BA` `EA` `VA` `VS` `VF` | BMB |
| bmad-workflow-builder | Wendy 🔄 | `BW` `EW` `VW` `MV` `RW` `CW` | BMB |
| bmad-module-builder | Morgan 🏗️ | `PB` `CM` `EM` `VM` `IM` | BMB |
| bmad-marketing-strategist | Elara 📈 | `MP` `MY` `MPS` `MCS` `LS` `LM` `MI` `GP` `CRE` | BMK |
| bmad-content-manager | Mia ✍️ | `MSP` `MAT` `SA` `MST` `SM` `SH` `MCW` `MCE` `MES` `CL` `SC` `PA` `AC` `AU` `AI` `PG` `CN` `IM` `MSS` `GE` `MPR` `SF` `FC` `OC` `PC` `PU` `MCP` `MCM` `CMM` | BMK |
| bmad-growth-engineer | Kai 📊 | `MCR` `AB` `RP` `FT` `RO` `SE` `CH` `GA` | BMK |

---

## Skills Architecture

Each BMAD module ships as an Agent Zero skill containing a `SKILL.md` manifest, a `module-help.csv` routing table, and a `workflows/` directory with step files. Skills are loaded on-demand — agents call `skills_tool:load` to get workflow instructions, then execute them exactly as defined. No workflow logic lives in agent prompts.

---

## Prompt Architecture

Each agent uses A0's native prompt slot system for clean separation of concerns:

~~~
┌─────────────────────────────────────────────────────────┐
│  role.md + tips.md     (WHO — persona, principles)      │
├─────────────────────────────────────────────────────────┤
│  specifics.md          (HOW — BMAD framework rules)      │
├─────────────────────────────────────────────────────────┤
│  solving.md            (WHEN — workflow execution pattern)│
├─────────────────────────────────────────────────────────┤
│  communication.md      (FORMAT — JSON output rules)      │
├─────────────────────────────────────────────────────────┤
│  SKILL.md              (WHAT — workflow routing + steps) │
├─────────────────────────────────────────────────────────┤
│  .a0proj/instructions/ (WHERE — project config + state)  │
└─────────────────────────────────────────────────────────┘
~~~

**role.md** defines persona and principles. **specifics.md** carries the BMAD operational framework (moved from communication.md to use A0's dedicated slot). **solving.md** overrides the default problem-solving pattern with BMAD's workflow-first execution model. **communication.md** handles JSON format rules only. **SKILL.md** contains workflow routing. **Project instructions** provide config and state.

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

**Plugin:** 1.1.0 | **Upstream:** Core 6.2.2 · BMB 1.5.0 · TEA 1.9.1 · CIS 0.1.9 · BMK 1.0.0

**Upstream parity: ~98%** — full coverage across BMM, BMB, TEA, CIS, BMK modules. Only BMGD (game dev) module deferred. Verified against [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD).

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
- [bmad-marketing (BMK)](https://github.com/bmad-code-org/bmad-marketing)
- [bmad-module-creative-intelligence-suite (CIS)](https://github.com/bmad-code-org/bmad-module-creative-intelligence-suite)

---

## License

MIT
