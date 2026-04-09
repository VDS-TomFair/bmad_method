## Step 4 — Mark story in-progress `[sprint-status]`

  **If** *{{sprint_status}} file exists*:
      - **Action:** Load the FULL file: {{sprint_status}}
      - **Action:** Read all development_status entries to find {{story_key}}
      - **Action:** Get current status value for development_status[{{story_key}}]

      **If** *current status == 'ready-for-dev' OR review_continuation == true*:
          - **Action:** Update the story in the sprint status report to = "in-progress"

    🚀 Starting work on story {{story_key}}
          Status updated: ready-for-dev → in-progress

      **If** *current status == 'in-progress'*:

    ⏯️ Resuming work on story {{story_key}}
          Story is already marked in-progress

      **If** *current status is neither ready-for-dev nor in-progress*:

    ⚠️ Unexpected story status: {{current_status}}
          Expected ready-for-dev or in-progress. Continuing anyway...
      - **Action:** Store {{current_sprint_status}} for later use

  **If** *{{sprint_status}} file does NOT exist*:

  ℹ️ No sprint status file exists - story progress will be tracked in story file only
      - **Action:** Set {{current_sprint_status}} = "no-sprint-tracking"

---

Append `step-04-mark-in-progress` to the `stepsCompleted` array in the story file's frontmatter.
Update `lastUpdatedAt` with current ISO timestamp.

**HALT** — Await user response or explicit 'continue' before loading next step.

Next step: {installed_path}/steps/step-05-implement-task.md
