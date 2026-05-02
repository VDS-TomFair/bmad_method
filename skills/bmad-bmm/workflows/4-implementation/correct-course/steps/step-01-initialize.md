# Correct Course - Sprint Change Management Instructions

## Pre-step: Project Context

Before starting, check for `{output_folder}/project-context.md`.
If it exists, read it and apply its conventions throughout this workflow.


<critical>The workflow execution engine is governed by: {project-root}/skills/bmad-init/core/tasks/workflow.md</critical>
<critical>You MUST have already loaded and processed: {project-root}/skills/bmad-bmm/workflows/4-implementation/correct-course/workflow.yaml</critical>
<critical>Communicate all responses in {communication_language} and language MUST be tailored to {user_skill_level}</critical>
<critical>Generate all documents in {document_output_language}</critical>
<critical>DOCUMENT OUTPUT: Updated epics, stories, or PRD sections. Clear, actionable changes. User skill level ({user_skill_level}) affects conversation style ONLY, not document updates.</critical>

<step n="1" goal="Initialize Change Navigation">
  <action>Load {project_context} for coding standards and project-wide patterns (if exists)</action>
  <action>Confirm change trigger and gather user description of the issue</action>
  <action>Ask: "What specific issue or change has been identified that requires navigation?"</action>
  <action>Verify access to required project documents:</action>
    - PRD (Product Requirements Document)
    - Current Epics and Stories
    - Architecture documentation
    - UI/UX specifications
  <action>Ask user for mode preference:</action>
    - **Incremental** (recommended): Refine each edit collaboratively
    - **Batch**: Present all changes at once for review
  <action>Store mode selection for use throughout workflow</action>

<action if="change trigger is unclear">HALT: "Cannot navigate change without clear understanding of the triggering issue. Please provide specific details about what needs to change and why."</action>

<action if="core documents are unavailable">HALT: "Need access to project documents (PRD, Epics, Architecture, UI/UX) to assess change impact. Please ensure these documents are accessible."</action>
</step>

<step n="0.5" goal="Discover and load project documents">
  <invoke-protocol name="discover_inputs" />
  <note>After discovery, these content variables are available: {prd_content}, {epics_content}, {architecture_content}, {ux_design_content}, {tech_spec_content}, {document_project_content}</note>
</step>

---

**HALT** — Await user response or explicit 'continue' before loading next step.

Next step: {installed_path}/steps/step-02-analyze-propose.md
