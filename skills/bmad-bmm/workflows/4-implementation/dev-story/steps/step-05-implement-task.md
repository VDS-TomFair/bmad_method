## Step 5 — Implement task following red-green-refactor cycle

> ⚠️ **CRITICAL:** FOLLOW THE STORY FILE TASKS/SUBTASKS SEQUENCE EXACTLY AS WRITTEN - NO DEVIATION
  - **Action:** Review the current task/subtask from the story file - this is your authoritative implementation guide
  - **Action:** Plan implementation following red-green-refactor cycle
  - **Action:** Write FAILING tests first for the task/subtask functionality
  - **Action:** Confirm tests fail before implementation - this validates test correctness
  - **Action:** Implement MINIMAL code to make tests pass
  - **Action:** Run tests to confirm they now pass
  - **Action:** Handle error conditions and edge cases as specified in task/subtask
  - **Action:** Improve code structure while keeping tests green
  - **Action:** Ensure code follows architecture patterns and coding standards from Dev Notes
  - **Action:** Document technical approach and decisions in Dev Agent Record → Implementation Plan
  - **Action (if** *new dependencies required beyond story specifications***): HALT: "Additional dependencies need user approval"
  - **Action (if** *3 consecutive implementation failures occur***): HALT and request guidance
  - **Action (if** *required configuration is missing***): HALT: "Cannot proceed without necessary configuration files"
> ⚠️ **CRITICAL:** NEVER implement anything not mapped to a specific task/subtask in the story file
> ⚠️ **CRITICAL:** NEVER proceed to next task until current task/subtask is complete AND tests pass
> ⚠️ **CRITICAL:** Execute continuously without pausing until all tasks/subtasks are complete or explicit HALT condition
> ⚠️ **CRITICAL:** Do NOT propose to pause for review until Step 9 completion gates are satisfied

---

Append `step-05-implement-task` to the `stepsCompleted` array in the story file's frontmatter.
Update `lastUpdatedAt` with current ISO timestamp.

**HALT** — Await user response or explicit 'continue' before loading next step.

Next step: {installed_path}/steps/step-06-author-tests.md
