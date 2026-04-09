## Step 9 — Story completion gate and mark for review `[sprint-status]`

  - **Action:** Verify ALL tasks and subtasks are marked [x] (re-scan the story document now)
  - **Action:** Run the full regression suite (do not skip)
  - **Action:** Confirm File List includes every changed file
  - **Action:** Execute enhanced definition-of-done validation
  - **Action:** Update the story Status to: "review"
  - **Action:** Validate definition-of-done checklist with essential requirements:
      - All tasks/subtasks marked complete with [x]
      - Implementation satisfies every Acceptance Criterion
      - Unit tests for core functionality added/updated
      - Integration tests for component interactions added when required
      - End-to-end tests for critical flows added when story demands them
      - All tests pass (no regressions, new tests successful)
      - Code quality checks pass (linting, static analysis if configured)
      - File List includes every new/modified/deleted file (relative paths)
      - Dev Agent Record contains implementation notes
      - Change Log includes summary of changes
      - Only permitted story sections were modified

  **If** *{sprint_status} file exists AND {{current_sprint_status}} != 'no-sprint-tracking'*:
      - **Action:** Load the FULL file: {sprint_status}
      - **Action:** Find development_status key matching {{story_key}}
      - **Action:** Verify current status is "in-progress" (expected previous state)
      - **Action:** Update development_status[{{story_key}}] = "review"
      - **Action:** Save file, preserving ALL comments and structure including STATUS DEFINITIONS

  ✅ Story status updated to "review" in sprint-status.yaml

  **If** *{sprint_status} file does NOT exist OR {{current_sprint_status}} == 'no-sprint-tracking'*:

  ℹ️ Story status updated to "review" in story file (no sprint tracking configured)

  **If** *story key not found in sprint status*:

  ⚠️ Story file updated, but sprint-status update failed: {{story_key}} not found

        Story status is set to "review" in file, but sprint-status.yaml may be out of sync.
  - **Action (if** *any task is incomplete***): HALT - Complete remaining tasks before marking ready for review
  - **Action (if** *regression failures exist***): HALT - Fix regression issues before completing
  - **Action (if** *File List is incomplete***): HALT - Update File List with all changed files
  - **Action (if** *definition-of-done validation fails***): HALT - Address DoD failures before completing

---

Append `step-09-completion-gate` to the `stepsCompleted` array in the story file's frontmatter.
Update `lastUpdatedAt` with current ISO timestamp.

**HALT** — Await user response or explicit 'continue' before loading next step.

Next step: {installed_path}/steps/step-10-communication.md
