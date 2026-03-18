# a0-bmad-method

**BMAD Method Framework v6** integration for [Agent Zero](https://github.com/frdel/agent-zero).

BMAD (Business Method for Agile Development) is a structured AI-first product development framework. This repo provides a full drop-in integration: 20 specialized agent personas, 5 global skills, and the complete workflow library — ready to use inside Agent Zero.

---

## What's included

| Path | Contents |
|---|---|
| `agents/bmad-*/` | 20 BMAD agent profiles, each with a complete prompt system (4 files for subordinates, 5 files for bmad-master) |
| `skills/bmad-*/` | 5 BMAD skills (init, bmm, bmb, cis, tea) — installed globally, not per-project |

### Agent personas (20)

`bmad-master` · `bmad-analyst` · `bmad-pm` · `bmad-architect` · `bmad-dev` · `bmad-sm` · `bmad-qa` · `bmad-ux-designer` · `bmad-tech-writer` · `bmad-quick-dev` · `bmad-agent-builder` · `bmad-workflow-builder` · `bmad-module-builder` · `bmad-test-architect` · `bmad-brainstorming-coach` · `bmad-design-thinking` · `bmad-innovation` · `bmad-storyteller` · `bmad-problem-solver` · `bmad-presentation`

### Skills

- **bmad-init** — bootstrap script that sets up a BMAD workspace in any Agent Zero project
- **bmad-bmm** — Business Method Module: PRD, architecture, epics, stories, dev, sprint workflows
- **bmad-bmb** — Builder Module: create/edit/validate BMAD agents, workflows, and modules
- **bmad-cis** — Creative Intelligence Suite: innovation strategy, design thinking, storytelling, problem solving
- **bmad-tea** — Testing Excellence Accelerator: ATDD, test automation, CI integration, NFR assessment

---

## Agent Prompt Architecture

Each BMAD agent is built from a clean 3-layer boundary:

```
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
```

**Agent prompts** define persona, communication style, and menu presentation — they are static and live in the repo.  
**Skills** are loaded on-demand and contain all workflow execution logic and routing instructions.  
**Project instructions** are written by `bmad init` and contain project-specific state and configuration — they are never stored in the repo.

This boundary keeps the agents lightweight, the skills composable, and project state cleanly separated.

---

## Prompt Files Per Agent

### Standard agents (19 subordinates) — 4 files each

| File | Purpose |
|---|---|
| `agent.system.main.role.md` | Full inline persona definition — name, background, expertise, personality. No lazy-loading from external docs; the complete persona is embedded here. |
| `agent.system.main.communication.md` | BMAD Activation Protocol, JSON output format, thinking framework, skill routing instructions, and the `§§include` file-inclusion hook. |
| `agent.system.main.tips.md` | Standard Agent Zero operational guidance (tool use, file handling, problem-solving steps) plus BMAD-specific behavioral guidelines. |
| `agent.system.main.communication_additions.md` | Agent-specific numbered workflow menu — the list of commands this agent can execute, routing rules, and menu handling logic. |

### bmad-master — 6 files (superset)

All 4 files above, plus:

| File | Purpose |
|---|---|
| `agent.system.tool.response.md` | Rich output formatting rules — how bmad-master structures final responses, markdown conventions, and section layout. |
| `fw.initial_message.md` | The greeting message displayed when the bmad-master profile is first activated in a new session. |

---

## Menu System

Every BMAD agent presents a **numbered workflow menu** when activated. This is the primary interaction model.

### How it works

1. Agent activates → greets user as their persona → displays numbered menu
2. User selects by **number** (e.g. `1`), **command code** (e.g. `BP`), or **natural language** (fuzzy matched)
3. Agent routes to the appropriate BMAD skill and executes the workflow
4. For chat and help commands, agent responds directly without loading a skill

### Menu definition

Each agent's menu is defined in `communication_additions.md`. The file specifies:
- The numbered command list with descriptions and type (Guided / Workflow / Task)
- Always-available commands (`CH`, `PM`, `MH`, `DA`, `/bmad-help`)
- Menu handling rules (ambiguity, no-match, stop-and-wait behavior)
- Skill routing: which `skills_tool:load` call maps to which workflow section

### Agent menu reference

| Agent | Persona | Commands | Module |
|---|---|---|---|
| bmad-analyst | Mary 📊 | `BP` `MR` `DR` `TR` `CB` `DP` | BMM |
| bmad-pm | John 📋 | `CP` `VP` `EP` `CE` `IR` `CC` | BMM |
| bmad-architect | Winston 🏗️ | `CA` `IR` | BMM |
| bmad-dev | Amelia 💻 | `DS` `CR` | BMM |
| bmad-qa | Quinn 🧪 | `QA` | BMM |
| bmad-sm | Bob 🏃 | `SP` `CS` `ER` `CC` | BMM |
| bmad-ux-designer | Sally 🎨 | `CU` | BMM |
| bmad-quick-dev | Barry 🚀 | `QS` `QD` `CR` | BMM |
| bmad-tech-writer | Paige 📚 | `DP` `WD` `US` `MG` `VD` `EC` | BMM |
| bmad-brainstorming-coach | Carson 🧠 | `BS` | CIS |
| bmad-design-thinking | Maya 🎨 | `DT` | CIS |
| bmad-innovation | Victor ⚡ | `IS` | CIS |
| bmad-storyteller | Sophia 📖 | `ST` | CIS |
| bmad-problem-solver | Dr. Quinn 🔬 | `PS` | CIS |
| bmad-presentation | Caravaggio 🎨 | `SD` `EX` `PD` `CT` `IN` `VM` `CV` | CIS |
| bmad-agent-builder | Bond 🤖 | `CA` `EA` `VA` | BMB |
| bmad-workflow-builder | Wendy 🔄 | `CW` `EW` `VW` `MV` `RW` | BMB |
| bmad-module-builder | Morgan 🏗️ | `PB` `CM` `EM` `VM` | BMB |
| bmad-test-architect | Murat 🧪 | `TMT` `TF` `AT` `TA` `TD` `TR` `NR` `CI` `RV` | TEA |
| bmad-master | BMad 🧙 | `LT` `LW` + delegates to all 19 agents | Core |

---

## Installation

This repo is an **Agent Zero plugin**. The plugin folder **must be named `bmad`** — the dashboard and extensions reference `/usr/plugins/bmad/` internally.

### Option A — Clone directly into Agent Zero

```bash
git clone https://github.com/vanja-emichi/bmad_method.git /path/to/agent-zero/usr/plugins/bmad
```

### Option B — Copy from an existing clone

```bash
cp -r /path/to/a0-bmad-method /path/to/agent-zero/usr/plugins/bmad
```

> ⚠️ **The folder must be named `bmad`** — not `a0-bmad-method` or anything else.

The `.toggle-1` file is included in the repo, so the plugin ships **pre-enabled**. Restart Agent Zero after installation — the **BMAD Method** plugin and dashboard icon will appear immediately.

For detailed installation steps, verification, developer setup, and upgrade instructions: see [README-install.md](README-install.md).


## First Run

Select the **BMad Master** profile in Agent Zero, then trigger the bootstrap skill:

> *"bmad init"*

### What `bmad init` creates

Running `bmad init` in a project sets up the BMAD workspace inside `.a0proj/`:

| Path | Description |
|---|---|
| `.a0proj/_bmad-output/` | Output directory for generated artifacts |
| `.a0proj/knowledge/` | Project knowledge base directory |
| `.a0proj/instructions/` | Project instruction files (read by Agent Zero on every session) |
| `.a0proj/instructions/01-bmad-config.md` | Path aliases and user settings for this project |
| `.a0proj/instructions/02-bmad-state.md` | Current BMAD phase, active persona, and artifact tracking |

The two instruction files are loaded automatically by Agent Zero and used by the **BMAD Activation Protocol** in each agent's `communication.md`: on session start, the agent reads project state from `02-bmad-state.md`, reads config from `01-bmad-config.md`, greets the user as the appropriate BMAD persona, and waits for direction before executing any workflow.

> Skills are **not** copied into the project — they are bundled in the plugin at `skills/` and loaded on-demand via `skills_tool`.

---

## Modules

| Module | Skill | Purpose |
|---|---|---|
| **BMM** — Business Method Module | `bmad-bmm` | Full product lifecycle: discovery → planning → architecture → implementation |
| **BMB** — Builder Module | `bmad-bmb` | Meta-module for creating and extending BMAD agents, workflows, and modules |
| **TEA** — Testing Excellence Accelerator | `bmad-tea` | Test architecture, ATDD, automation, CI, NFR assessment |
| **CIS** — Creative Intelligence Suite | `bmad-cis` | Innovation strategy, design thinking, storytelling, structured problem solving |

---

## Dashboard

BMAD ships a live project status dashboard. After installation, the BMAD button appears in Agent Zero's sidebar.

| Component | Location | Purpose |
|---|---|---|
| Dashboard SPA | `webui/bmad-dashboard.html` | Real-time phase, active artifact, story tracking |
| REST API | `api/_bmad_status.py` | Reads `02-bmad-state.md` and serves structured status |
| Sidebar button | `extensions/webui/sidebar-quick-actions-main-start/` | Opens dashboard in one click |

The dashboard is **read-only** — it observes agent state without writing to it.

---

## Memory Architecture (ARCH-006)

Each BMAD agent maintains isolated persistent memory across sessions:

- **Per-agent FAISS stores** — `.a0proj/memory/bmad-{name}/` — vector databases isolated by agent and project ID
- **Constitutional knowledge layer** — `.a0proj/knowledge/main/bmad-{name}/` — static standards and seeds, preloaded into FAISS at session start via native A0 `agent_knowledge_subdir` mechanism
- **Project knowledge** — `.a0proj/knowledge/main/` — shared FAISS-loaded documents available to all agents


---

## Extension Pipeline

Two Python extensions hook into Agent Zero's lifecycle:

| Extension | Hook Point | Purpose |
|---|---|---|
| `_11_bmad_autobrief.py` | `agent_init` | Auto-generates project brief for BMad Master on fresh sessions |
| `_80_bmad_routing_manifest.py` | `message_loop_prompts_after` | Dynamically builds routing manifest from `skills/*/module-help.csv` for BMad Master orchestration |


---

## Documentation

- **Architecture Alignment Report v3.0** — canonical system architecture reference (internal dev doc, see `.a0proj/_bmad-output/planning-artifacts/` after `bmad init`)
- [Detailed Install Guide](README-install.md) — installation, verification, upgrade, and developer setup
- **Memory Architecture** — ARCH-006 FAISS-native reference (see `.a0proj/knowledge/main/memory-architecture.md` after `bmad init`)
---

## Requirements

- [Agent Zero](https://github.com/frdel/agent-zero) (latest stable release)
- An LLM with large context window recommended (Claude Sonnet or better)
