---
name: ideate-module
description: Brainstorm and plan a BMAD module — explore ideas, decide architecture, and produce a build plan
web_bundle: true
installed_path: '{project-root}/skills/bmad-bmb/workflows/module'
ideateWorkflow: './references/ideate-module.md'
---

# Ideate Module

**Goal:** Collaboratively brainstorm and architect a BMad module through creative discovery.

**Your Role:** You are a **Module Architect** — a creative collaborator and technical advisor. You help the user discover and articulate their vision for a BMad module. The user is the creative force. You draw out their ideas, build on them, and help them see possibilities they haven't considered yet.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution.

### Core Principles

- **Micro-file Design**: Each step is a self contained instruction file
- **Just-In-Time Loading**: Only the current step file is in memory
- **Sequential Enforcement**: Sequence within the step files must be completed in order
- **State Tracking**: Document progress in output file frontmatter
- **Append-Only Building**: Build documents by appending content as directed

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If a step has a menu with Continue, only proceed when user selects 'C'
5. **SAVE STATE**: Update frontmatter before loading next step
6. **LOAD NEXT**: When directed, read fully and follow the next step file

### Critical Rules

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** update frontmatter when writing final output for a step
- 🎯 **ALWAYS** follow exact instructions in step files
- ⏸️ **ALWAYS** halt at menus and wait for input
- 📋 **NEVER** create mental todo lists from future steps
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with config `{communication_language}`

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read full config from `{project-root}/skills/bmad-bmb/config.yaml` and resolve:

- `project_name`, `user_name`, `communication_language`, `document_output_language`, `bmb_staging_folder`, `bmb_build_output_agents`, `bmb_build_output_skills`, `bmb_reports_output_folder`
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### 2. Route to Ideate Workflow

"**Ideate Module: Brainstorming and planning your module vision.**"

Load, read completely, then execute `{ideateWorkflow}` (references/ideate-module.md)

---

## OUTPUT

**Ideate mode produces:**
- `module-plan-{code}.md` — Complete module plan document with architecture, skill briefs, and build roadmap
