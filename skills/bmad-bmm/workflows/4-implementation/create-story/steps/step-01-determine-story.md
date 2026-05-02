## Pre-step: Project Context

Before starting, check for `{output_folder}/project-context.md`.
If it exists, read it and apply its conventions throughout this workflow.

> ⚠️ **CRITICAL:** The workflow execution engine is governed by: {project-root}/skills/bmad-init/core/tasks/workflow.md
> ⚠️ **CRITICAL:** You MUST have already loaded and processed: {installed_path}/workflow.yaml
> ⚠️ **CRITICAL:** Communicate all responses in {communication_language} and generate all documents in {document_output_language}
> ⚠️ **CRITICAL:** 🔥 CRITICAL MISSION: You are creating the ULTIMATE story context engine that prevents LLM developer mistakes, omissions or
    disasters! 🔥
> ⚠️ **CRITICAL:** Your purpose is NOT to copy from epics - it's to create a comprehensive, optimized story file that gives the DEV agent
    EVERYTHING needed for flawless implementation
> ⚠️ **CRITICAL:** COMMON LLM MISTAKES TO PREVENT: reinventing wheels, wrong libraries, wrong file locations, breaking regressions, ignoring UX,
    vague implementations, lying about completion, not learning from past work
> ⚠️ **CRITICAL:** 🚨 EXHAUSTIVE ANALYSIS REQUIRED: You must thoroughly analyze ALL artifacts to extract critical context - do NOT be lazy or skim!
    This is the most important function in the entire development process!
> ⚠️ **CRITICAL:** 🔬 UTILIZE SUBPROCESSES AND SUBAGENTS: Use research subagents, subprocesses or parallel processing if available to thoroughly
    analyze different artifacts simultaneously and thoroughly
> ⚠️ **CRITICAL:** ❓ SAVE QUESTIONS: If you think of questions or clarifications during analysis, save them for the end after the complete story is
    written
> ⚠️ **CRITICAL:** 🎯 ZERO USER INTERVENTION: Process should be fully automated except for initial epic/story selection or missing documents

## Step 1 — Determine target story

**If** {{story_path}} is provided by user or user provided the epic and story number such as 2-4 or 1.6 or epic 1 story 5:
  - **Action:** Parse user-provided story path: extract epic_num, story_num, story_title from format like "1-2-user-auth"
  - **Action:** Set {{epic_num}}, {{story_num}}, {{story_key}} from user input
  - **Action:** GOTO step 2a
- **Action:** Check if {{sprint_status}} file exists for auto discover

**If** sprint status file does NOT exist:

  🚫 No sprint status file found and no story specified

  **Required Options:**
        1. Run `sprint-planning` to initialize sprint tracking (recommended)
        2. Provide specific epic-story number to create (e.g., "1-2-user-auth")
        3. Provide path to story documents if sprint status doesn't exist yet

  **❓ Ask user:** Choose option [1], provide epic-story number, path to story docs, or [q] to quit:

  **If** user chooses 'q':
    - **Action:** HALT - No work needed

  **If** user chooses '1':

    Run sprint-planning workflow first to create sprint-status.yaml
    - **Action:** HALT - User needs to run sprint-planning

  **If** user provides epic-story number:
    - **Action:** Parse user input: extract epic_num, story_num, story_title
    - **Action:** Set {{epic_num}}, {{story_num}}, {{story_key}} from user input
    - **Action:** GOTO step 2a

  **If** user provides story docs path:
    - **Action:** Use user-provided path for story documents
    - **Action:** GOTO step 2a

**If** no user input provided:
  > ⚠️ **CRITICAL:** MUST read COMPLETE {sprint_status} file from start to end to preserve order
  - **Action:** Load the FULL file: {{sprint_status}}
  - **Action:** Read ALL lines from beginning to end - do not skip any content
  - **Action:** Parse the development_status section completely
  - **Action:** Find the FIRST story (by reading in order from top to bottom) where:
        - Key matches pattern: number-number-name (e.g., "1-2-user-auth")
        - NOT an epic key (epic-X) or retrospective (epic-X-retrospective)
        - Status value equals "backlog"

  **If** no backlog story found:

    📋 No backlog stories found in sprint-status.yaml

          All stories are either already created, in progress, or done.

          **Options:**
          1. Run sprint-planning to refresh story tracking
          2. Load PM agent and run correct-course to add more stories
          3. Check if current sprint is complete and run retrospective
    - **Action:** HALT
  - **Action:** Extract from found story key (e.g., "1-2-user-authentication"):
        - epic_num: first number before dash (e.g., "1")
        - story_num: second number after first dash (e.g., "2")
        - story_title: remainder after second dash (e.g., "user-authentication")
  - **Action:** Set {{story_id}} = "{{epic_num}}.{{story_num}}"
  - **Action:** Store story_key for later use (e.g., "1-2-user-authentication")
  - **Action:** Check if this is the first story in epic {{epic_num}} by looking for {{epic_num}}-1-* pattern

  **If** this is first story in epic {{epic_num}}:
    - **Action:** Load {{sprint_status}} and check epic-{{epic_num}} status
    - **Action:** If epic status is "backlog" → update to "in-progress"
    - **Action:** If epic status is "contexted" (legacy status) → update to "in-progress" (backward compatibility)
    - **Action:** If epic status is "in-progress" → no change needed

    **If** epic status is 'done':

      🚫 ERROR: Cannot create story in completed epic

      Epic {{epic_num}} is marked as 'done'. All stories are complete.

      If you need to add more work, either:

      1. Manually change epic status back to 'in-progress' in sprint-status.yaml

      2. Create a new epic for additional work
      - **Action:** HALT - Cannot proceed

    **If** epic status is not one of: backlog, contexted, in-progress, done:

      🚫 ERROR: Invalid epic status '{{epic_status}}'

      Epic {{epic_num}} has invalid status. Expected: backlog, in-progress, or done

      Please fix sprint-status.yaml manually or run sprint-planning to regenerate
      - **Action:** HALT - Cannot proceed

    📊 Epic {{epic_num}} status updated to in-progress
  - **Action:** GOTO step 2a
- **Action:** Load the FULL file: {{sprint_status}}
- **Action:** Read ALL lines from beginning to end - do not skip any content
- **Action:** Parse the development_status section completely
- **Action:** Find the FIRST story (by reading in order from top to bottom) where:
      - Key matches pattern: number-number-name (e.g., "1-2-user-auth")
      - NOT an epic key (epic-X) or retrospective (epic-X-retrospective)
      - Status value equals "backlog"

**If** no backlog story found:

  📋 No backlog stories found in sprint-status.yaml

        All stories are either already created, in progress, or done.

        **Options:**
        1. Run sprint-planning to refresh story tracking
        2. Load PM agent and run correct-course to add more stories
        3. Check if current sprint is complete and run retrospective
  - **Action:** HALT
- **Action:** Extract from found story key (e.g., "1-2-user-authentication"):
      - epic_num: first number before dash (e.g., "1")
      - story_num: second number after first dash (e.g., "2")
      - story_title: remainder after second dash (e.g., "user-authentication")
- **Action:** Set {{story_id}} = "{{epic_num}}.{{story_num}}"
- **Action:** Store story_key for later use (e.g., "1-2-user-authentication")
- **Action:** Check if this is the first story in epic {{epic_num}} by looking for {{epic_num}}-1-* pattern

**If** this is first story in epic {{epic_num}}:
  - **Action:** Load {{sprint_status}} and check epic-{{epic_num}} status
  - **Action:** If epic status is "backlog" → update to "in-progress"
  - **Action:** If epic status is "contexted" (legacy status) → update to "in-progress" (backward compatibility)
  - **Action:** If epic status is "in-progress" → no change needed

  **If** epic status is 'done':

    🚫 ERROR: Cannot create story in completed epic

    Epic {{epic_num}} is marked as 'done'. All stories are complete.

    If you need to add more work, either:

    1. Manually change epic status back to 'in-progress' in sprint-status.yaml

    2. Create a new epic for additional work
    - **Action:** HALT - Cannot proceed

  **If** epic status is not one of: backlog, contexted, in-progress, done:

    🚫 ERROR: Invalid epic status '{{epic_status}}'

    Epic {{epic_num}} has invalid status. Expected: backlog, in-progress, or done

    Please fix sprint-status.yaml manually or run sprint-planning to regenerate
    - **Action:** HALT - Cannot proceed

  📊 Epic {{epic_num}} status updated to in-progress
- **Action:** GOTO step 2a

---

**HALT** — Await user response or explicit 'continue' before loading next step.

Next step: {installed_path}/steps/step-02-load-artifacts.md
