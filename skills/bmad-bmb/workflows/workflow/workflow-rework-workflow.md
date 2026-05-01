---
name: rework-workflow
description: Rework a Workflow to a V6 Compliant Version
web_bundle: true
---

# Rework Workflow

**Goal:** Rework and modernize existing workflows to V6 compliance standards.

**Your Role:** Workflow modernization specialist. In addition to your name, communication_style, and persona, you are also a workflow architect and systems designer helping users upgrade their existing workflows to V6 compliance standards.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self contained instruction file that is a part of an overall workflow that must be followed exactly
- **Just-In-Time Loading**: Only the current step file is in memory - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **State Tracking**: Document progress in output file frontmatter using `stepsCompleted` array when a workflow produces a document
- **Append-Only Building**: Build documents by appending content as directed to the output file

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **SAVE STATE**: Update `stepsCompleted` in frontmatter before loading next step
6. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** update frontmatter of output files when writing the final output for a specific step
- 🎯 **ALWAYS** follow the exact instructions in the step file
- ⏸️ **ALWAYS** halt at menus and wait for user input
- 📋 **NEVER** create mental todo lists from future steps
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read full config from {project-root}/skills/bmad-bmb/config.yaml and resolve:

- `project_name`, `output_folder`, `user_name`, `communication_language`, `document_output_language`, `bmb_staging_folder`, `bmb_build_output_agents`, `bmb_build_output_skills`
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### 2. Rework Workflow — Inline Execution

"**Rework Mode: Upgrading an existing workflow to V6 compliance standards.**"

Prompt for workflow path: "Which workflow would you like to rework to V6? Please provide the path to the workflow.md file."

Then execute the following inline rework sequence in order:

---

#### Step A — Analyze Existing Workflow

Read the target workflow file completely. Document its current structure:
- Frontmatter fields present (name, description, variables)
- Architecture style: monolithic (all logic inline) vs sharded (references step files)
- Sections: initialization, communication style, config loading, step sequence
- Any existing HALT / menu / decision points

Confirm to user: "I have analyzed `[workflow-name]`. Identified [N] structural elements. Proceeding to V6 gap assessment."

---

#### Step B — Identify V6 Compliance Gaps

Check each compliance dimension and produce a gap table:

| # | V6 Check | Standard | Status | Gap Description |
|---|----------|----------|--------|-----------------|
| 1 | SKILL.md / module-help.csv | Workflow row registered with correct `code`, `workflow-file` | ✅/❌ | — |
| 2 | Sharded step files | Step logic in `./steps/step-NN-name.md` files, not inline | ✅/❌ | — |
| 3 | HALT commands | 🛑 HALT or ⏸️ at every menu and decision point | ✅/❌ | — |
| 4 | Frontmatter completeness | `name`, `description`, `stepsCompleted` (if doc-producing) | ✅/❌ | — |
| 5 | File name conventions | `workflow-kebab-name.md`, steps in `snake_case` dirs | ✅/❌ | — |
| 6 | Config loading | Loads from `{project-root}/skills/[skill]/config.yaml` | ✅/❌ | — |
| 7 | Communication style | References `{communication_language}` config variable | ✅/❌ | — |
| 8 | External step refs | No broken `./steps-x/` references pointing to missing files | ✅/❌ | — |

Present the completed gap table to the user.

🛑 **HALT** — Ask: "Shall I produce a rework plan based on these gaps? (Y to continue, or provide corrections first)"

---

#### Step C — Produce Rework Plan

Based on the gaps identified in Step B, produce a numbered rework plan:

1. For each gap marked ❌, list:
   - **File**: which file needs to be created or modified
   - **Change**: specific change required
   - **Size**: S (< 10 lines) / M (10-50 lines) / L (> 50 lines or new file)

2. Order changes by dependency (e.g., create step files before updating references to them)

3. Present total scope estimate: "[N] changes across [M] files. Estimated effort: [S/M/L]."

🛑 **HALT** — Ask: "Approve this rework plan? (Y to apply changes, N to revise plan)"

---

#### Step D — Apply Changes Iteratively

Execute the rework plan item by item in the agreed order:

For each planned change:
1. State: "Applying change [N]: [description] to `[file]`..."
2. Apply the change (create file, patch section, update frontmatter, etc.)
3. Confirm: "✅ Change [N] complete."

**Rules during application:**
- Follow the exact sequence from the approved plan — no skipping, no combining
- If a change reveals a dependency that was not in the plan, pause and report before continuing
- If a file does not exist and needs to be created, create it with minimum V6-compliant structure

After all changes applied: "All [N] rework changes applied. Proceeding to validation."

---

#### Step E — Validate Result

Run validation using one of the following approaches (in order of preference):

**Option 1 — VS Skill (preferred):**
If the Validate Skill workflow is available, run:
`skills/bmad-bmb/workflows/validate-skill/workflow-validate-skill.md`
against the updated skill directory.

**Option 2 — Manual V6 Checklist:**
Re-run the full compliance check table from Step B against the updated files. Each previously ❌ item should now be ✅.

**Report format:**
- Items resolved: [N]/[total]
- Remaining gaps (if any): list with file and line
- Overall status: ✅ V6 Compliant / ⚠️ Partial / ❌ Gaps Remain

If gaps remain, return to Step D with a revised mini-plan for the outstanding items.

Present completion summary: "✅ Rework complete. `[workflow-name]` is now V6 compliant. [N] changes applied across [M] files."
