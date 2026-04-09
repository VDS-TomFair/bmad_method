## Step 8 — Validate and mark task complete ONLY when fully done

> ⚠️ **CRITICAL:** NEVER mark a task complete unless ALL conditions are met - NO LYING OR CHEATING
  - **Action:** Verify ALL tests for this task/subtask ACTUALLY EXIST and PASS 100%
  - **Action:** Confirm implementation matches EXACTLY what the task/subtask specifies - no extra features
  - **Action:** Validate that ALL acceptance criteria related to this task are satisfied
  - **Action:** Run full test suite to ensure NO regressions introduced

  **If** *task is review follow-up (has [AI-Review] prefix)*:
      - **Action:** Extract review item details (severity, description, related AC/file)
      - **Action:** Add to resolution tracking list: {{resolved_review_items}}
      - **Action:** Mark task checkbox [x] in "Tasks/Subtasks → Review Follow-ups (AI)" section
      - **Action:** Find matching action item in "Senior Developer Review (AI) → Action Items" section by matching description
      - **Action:** Mark that action item checkbox [x] as resolved
      - **Action:** Add to Dev Agent Record → Completion Notes: "✅ Resolved review finding [{{severity}}]: {{description}}"

  **If** *ALL validation gates pass AND tests ACTUALLY exist and pass*:
      - **Action:** ONLY THEN mark the task (and subtasks) checkbox with [x]
      - **Action:** Update File List section with ALL new, modified, or deleted files (paths relative to repo root)
      - **Action:** Add completion notes to Dev Agent Record summarizing what was ACTUALLY implemented and tested

  **If** *ANY validation fails*:
      - **Action:** DO NOT mark task complete - fix issues first
      - **Action:** HALT if unable to fix validation failures

  **If** *review_continuation == true and {{resolved_review_items}} is not empty*:
      - **Action:** Count total resolved review items in this session
      - **Action:** Add Change Log entry: "Addressed code review findings - {{resolved_count}} items resolved (Date: {{date}})"
  - **Action:** Save the story file
  - **Action:** Determine if more incomplete tasks remain
  - **Action (if** *more tasks remain***):
    - Return to step-05-implement-task.md for next task
  - **Action (if** *no tasks remain***):
    - Proceed to completion

---

Append `step-08-validate-complete` to the `stepsCompleted` array in the story file's frontmatter.
Update `lastUpdatedAt` with current ISO timestamp.

**HALT** — Await user response or explicit 'continue' before loading next step.

Next step: {installed_path}/steps/step-09-completion-gate.md
