## Step 7 — Run validations and tests

  - **Action:** Determine how to run tests for this repo (infer test framework from project structure)
  - **Action:** Run all existing tests to ensure no regressions
  - **Action:** Run the new tests to verify implementation correctness
  - **Action:** Run linting and code quality checks if configured in project
  - **Action:** Validate implementation meets ALL story acceptance criteria; enforce quantitative thresholds explicitly
  - **Action (if** *regression tests fail***): STOP and fix before continuing - identify breaking changes immediately
  - **Action (if** *new tests fail***): STOP and fix before continuing - ensure implementation correctness

---

Append `step-07-run-validations` to the `stepsCompleted` array in the story file's frontmatter.
Update `lastUpdatedAt` with current ISO timestamp.

**HALT** — Await user response or explicit 'continue' before loading next step.

Next step: {installed_path}/steps/step-08-validate-complete.md
