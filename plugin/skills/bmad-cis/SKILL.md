---
name: "bmad-cis"
description: "BMAD Creative Intelligence Suite — innovation, design thinking, storytelling, problem solving, brainstorming. Triggers: innovation strategy, disruption opportunities, design thinking, empathy driven design, storytelling, narrative, problem solving, structured problem solving, brainstorming, ideate, creative session, cis module."
version: "1.0.0"
author: "BMAD"
tags: ["bmad", "cis", "creative", "innovation", "design"]
trigger_patterns:
  - "innovation strategy"
  - "disruption opportunities"
  - "design thinking"
  - "empathy driven design"
  - "storytelling"
  - "narrative"
  - "problem solving"
  - "structured problem solving"
  - "brainstorming"
  - "ideate"
  - "creative session"
  - "cis module"
---

# BMAD Creative Intelligence Suite (CIS) — Innovation and Design Thinking

CIS provides structured creative methodologies: innovation strategy, design thinking, storytelling, and problem solving. Use CIS when you need creative rigor applied to product discovery, user research, or strategic challenges.

All paths use `{project-root}` which resolves to `.a0proj/` as defined in `01-bmad-config.md`.

When any CIS workflow is triggered, read the full workflow file at the path shown and follow it exactly.

---

## CIS Workflows

### Innovation Strategy
**Triggers:** "innovation strategy", "disruption opportunities", "strategic innovation", "innovation roadmap"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/innovation-strategy-<date>.md`
**Workflow:** `{skill-dir}/workflows/innovation-strategy/workflow.yaml`

### Design Thinking
**Triggers:** "design thinking", "empathy driven design", "user centered design", "design sprint"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/design-thinking-<date>.md`
**Workflow:** `{skill-dir}/workflows/design-thinking/workflow.yaml`

### Storytelling
**Triggers:** "storytelling", "narrative", "craft narrative", "story framework", "communication strategy"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/storytelling-<date>.md`
**Workflow:** `{skill-dir}/workflows/storytelling/workflow.yaml`

### Problem Solving
**Triggers:** "problem solving", "structured problem solving", "brainstorming", "ideate", "creative session", "root cause analysis"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/problem-solving-<date>.md`
**Workflow:** `{skill-dir}/workflows/problem-solving/workflow.yaml`

---

## Execution Instructions

When any CIS workflow is triggered:
1. Identify the workflow from the trigger phrase.
2. Read the full workflow file at the path shown above using `code_execution_tool` (bash cat).
3. Follow the workflow instructions exactly — do not summarize or skip steps.
4. Write output artifacts using `code_execution_tool` (bash write).
5. Update `{project-root}/instructions/02-bmad-state.md` to reflect the active CIS workflow.
