## Step 2 — Load project context and story information

> ⚠️ **CRITICAL:** Load all available context to inform implementation
  - **Action:** Load {project_context} for coding standards and project-wide patterns (if exists)
  - **Action:** Parse sections: Story, Acceptance Criteria, Tasks/Subtasks, Dev Notes, Dev Agent Record, File List, Change Log, Status
  - **Action:** Load comprehensive context from story file's Dev Notes section
  - **Action:** Extract developer guidance from Dev Notes: architecture requirements, previous learnings, technical specifications
  - **Action:** Use enhanced story context to inform implementation decisions and approaches

✅ **Context Loaded**
      Story and project context available for implementation

---

Append `step-02-load-context` to the `stepsCompleted` array in the story file's frontmatter.
Update `lastUpdatedAt` with current ISO timestamp.

**HALT** — Await user response or explicit 'continue' before loading next step.

Next step: {installed_path}/steps/step-03-detect-continuation.md
