## Pre-step: Project Context

Before starting, check for `{output_folder}/project-context.md`.
If it exists, read it and apply its conventions throughout this workflow.

## Resume Check

Before starting: read the `stepsCompleted` array in the story file's frontmatter.
- If empty or field absent → this is a fresh run. Set `startedAt` to current ISO timestamp. Continue.
- If non-empty → this workflow was previously interrupted.
  - List completed steps to the user: "Steps already completed: [list]"
  - Ask: "Resume from the next step, or start over?"
  - HALT and await user response before proceeding.

---

> ⚠️ **CRITICAL:** The workflow execution engine is governed by: {project-root}/skills/bmad-init/core/tasks/workflow.md
> ⚠️ **CRITICAL:** You MUST have already loaded and processed: {installed_path}/workflow.yaml
> ⚠️ **CRITICAL:** Communicate all responses in {communication_language} and language MUST be tailored to {user_skill_level}
> ⚠️ **CRITICAL:** Generate all documents in {document_output_language}
> ⚠️ **CRITICAL:** Only modify the story file in these areas: Tasks/Subtasks checkboxes, Dev Agent Record (Debug Log, Completion Notes), File List,
    Change Log, and Status
> ⚠️ **CRITICAL:** Execute ALL steps in exact order; do NOT skip steps
> ⚠️ **CRITICAL:** Absolutely DO NOT stop because of "milestones", "significant progress", or "session boundaries". Continue in a single execution
    until the story is COMPLETE (all ACs satisfied and all tasks/subtasks checked) UNLESS a HALT condition is triggered or the USER gives
    other instruction.
> ⚠️ **CRITICAL:** Do NOT schedule a "next session" or request review pauses unless a HALT condition applies. Only Step 6 decides completion.
> ⚠️ **CRITICAL:** User skill level ({user_skill_level}) affects conversation style ONLY, not code updates.

## Step 1 — Find next ready story and load it `[sprint-status]`

  **If** *{{story_path}} is provided*:
      - **Action:** Use {{story_path}} directly
      - **Action:** Read COMPLETE story file
      - **Action:** Extract story_key from filename or metadata
      > **Goto** step task_check

  **If** *{{sprint_status}} file exists*:
  > ⚠️ **CRITICAL:** MUST read COMPLETE sprint-status.yaml file from start to end to preserve order
      - **Action:** Load the FULL file: {{sprint_status}}
      - **Action:** Read ALL lines from beginning to end - do not skip any content
      - **Action:** Parse the development_status section completely to understand story order
      - **Action:** Find the FIRST story (by reading in order from top to bottom) where:
        - Key matches pattern: number-number-name (e.g., "1-2-user-auth")
        - NOT an epic key (epic-X) or retrospective (epic-X-retrospective)
        - Status value equals "ready-for-dev"

      **If** *no ready-for-dev or in-progress story found*:

    📋 No ready-for-dev stories found in sprint-status.yaml

          **Current Sprint Status:** {{sprint_status_summary}}

          **What would you like to do?**
          1. Run `create-story` to create next story from epics with comprehensive context
          2. Run `*validate-create-story` to improve existing stories before development (recommended quality check)
          3. Specify a particular story file to develop (provide full path)
          4. Check {{sprint_status}} file to see current sprint status

          💡 **Tip:** Stories in `ready-for-dev` may not have been validated. Consider running `validate-create-story` first for a quality
          check.

          **❓ Ask user:**
          Choose option [1], [2], [3], or [4], or specify story file path:

          **If** *user chooses '1'*:
              - **Action:** HALT - Run create-story to create next story

          **If** *user chooses '2'*:
              - **Action:** HALT - Run validate-create-story to improve existing stories

          **If** *user chooses '3'*:

              **❓ Ask user:**
              Provide the story file path to develop:
              - **Action:** Store user-provided story path as {{story_path}}
              > **Goto** step task_check

          **If** *user chooses '4'*:

      Loading {{sprint_status}} for detailed status review...
              - **Action:** Display detailed sprint status analysis
              - **Action:** HALT - User can review sprint status and provide story path

          **If** *user provides story file path*:
              - **Action:** Store user-provided story path as {{story_path}}
              > **Goto** step task_check

  **If** *{{sprint_status}} file does NOT exist*:
      - **Action:** Search {implementation_artifacts} for stories directly
      - **Action:** Find stories with "ready-for-dev" status in files
      - **Action:** Look for story files matching pattern: *-*-*.md
      - **Action:** Read each candidate story file to check Status section

      **If** *no ready-for-dev stories found in story files*:

    📋 No ready-for-dev stories found

          **Available Options:**
          1. Run `create-story` to create next story from epics with comprehensive context
          2. Run `*validate-create-story` to improve existing stories
          3. Specify which story to develop

          **❓ Ask user:**
          What would you like to do? Choose option [1], [2], or [3]:

          **If** *user chooses '1'*:
              - **Action:** HALT - Run create-story to create next story

          **If** *user chooses '2'*:
              - **Action:** HALT - Run validate-create-story to improve existing stories

          **If** *user chooses '3'*:

              **❓ Ask user:**
              It's unclear what story you want developed. Please provide the full path to the story file:
              - **Action:** Store user-provided story path as {{story_path}}
              - **Action:** Continue with provided story file

      **If** *ready-for-dev story found in files*:
          - **Action:** Use discovered story file and extract story_key
  - **Action:** Store the found story_key (e.g., "1-2-user-authentication") for later status updates
  - **Action:** Find matching story file in {implementation_artifacts} using story_key pattern: {{story_key}}.md
  - **Action:** Read COMPLETE story file from discovered path
  <!-- anchor: task_check -->
  - **Action:** Parse sections: Story, Acceptance Criteria, Tasks/Subtasks, Dev Notes, Dev Agent Record, File List, Change Log, Status
  - **Action:** Load comprehensive context from story file's Dev Notes section
  - **Action:** Extract developer guidance from Dev Notes: architecture requirements, previous learnings, technical specifications
  - **Action:** Use enhanced story context to inform implementation decisions and approaches
  - **Action:** Identify first incomplete task (unchecked [ ]) in Tasks/Subtasks
  - **Action (if** *no incomplete tasks***): 
    - Completion sequence
  - **Action (if** *story file inaccessible***): HALT: "Cannot develop story without access to story file"
  - **Action (if** *incomplete task or subtask requirements ambiguous***): ASK user to clarify or HALT

---

Append `step-01-find-story` to the `stepsCompleted` array in the story file's frontmatter.
Update `lastUpdatedAt` with current ISO timestamp.

**HALT** — Await user response or explicit 'continue' before loading next step.

Next step: {installed_path}/steps/step-02-load-context.md
