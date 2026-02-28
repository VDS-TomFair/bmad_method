# a0-bmad-method

**BMAD Method Framework v6** integration for [Agent Zero](https://github.com/frdel/agent-zero).

BMAD (Business Method for Agile Development) is a structured AI-first product development framework. This repo provides a full drop-in integration: 20 specialized agent personas, 5 global skills, and the complete workflow library — ready to use inside Agent Zero.

---

## What's included

| Path | Contents |
|---|---|
| `agents/bmad-*/` | 20 BMAD agent profiles (personas) |
| `skills/bmad-*/` | 5 BMAD skills (init, bmm, bmb, cis, tea) |
| `docs/bmad/` | Full BMAD framework template library |

### Agent personas (20)
`bmad-master` · `bmad-pm` · `bmad-analyst` · `bmad-architect` · `bmad-dev` · `bmad-sm` · `bmad-qa` · `bmad-ux-designer` · `bmad-tech-writer` · `bmad-quick-dev` · `bmad-agent-builder` · `bmad-workflow-builder` · `bmad-module-builder` · `bmad-test-architect` · `bmad-brainstorming-coach` · `bmad-design-thinking` · `bmad-innovation` · `bmad-storyteller` · `bmad-problem-solver` · `bmad-presentation`

### Skills
- **bmad-init** — bootstrap script that sets up a BMAD workspace in any Agent Zero project
- **bmad-bmm** — Business Method Module: PRD, architecture, epics, stories, dev, sprint workflows
- **bmad-bmb** — Builder Module: create/edit/validate BMAD agents, workflows, and modules
- **bmad-cis** — Creative Intelligence Suite: innovation strategy, design thinking, storytelling, problem solving
- **bmad-tea** — Testing Excellence Accelerator: ATDD, test automation, CI integration, NFR assessment

---

## Installation

Copy the three directories into your Agent Zero installation (`/a0/`):

```bash
# From inside your Agent Zero directory
cp -r agents/bmad-* agents/
cp -r skills/bmad-* skills/
cp -r docs/bmad docs/
```

Then restart Agent Zero. The 5 BMAD skills appear immediately in the skill list. Select the **BMad Master** profile to start.

### First run

In Agent Zero, trigger the bootstrap skill to initialize a project workspace:

> *"bmad init"*

This creates `.a0proj/` in the current project directory with the full framework, config files, and state tracking.

---

## Modules

| Module | Purpose |
|---|---|
| **BMM** — Business Method Module | Full product lifecycle: discovery → planning → architecture → implementation |
| **BMB** — Builder Module | Meta-module for creating and extending BMAD agents, workflows, and modules |
| **TEA** — Testing Excellence Accelerator | Test architecture, ATDD, automation, CI, NFR assessment |
| **CIS** — Creative Intelligence Suite | Innovation strategy, design thinking, storytelling, structured problem solving |

---

## Requirements

- [Agent Zero](https://github.com/frdel/agent-zero) (testing branch or latest)
- An LLM with large context window recommended (Claude Sonnet or better)
