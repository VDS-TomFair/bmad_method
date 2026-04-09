## Step 10 — Completion communication and user support

  - **Action:** Execute the enhanced definition-of-done checklist using the validation framework
  - **Action:** Prepare a concise summary in Dev Agent Record → Completion Notes
  - **Action:** Communicate to {user_name} that story implementation is complete and ready for review
  - **Action:** Summarize key accomplishments: story ID, story key, title, key changes made, tests added, files modified
  - **Action:** Provide the story file path and current status (now "review")
  - **Action:** Based on {user_skill_level}, ask if user needs any explanations about:
      - What was implemented and how it works
      - Why certain technical decisions were made
      - How to test or verify the changes
      - Any patterns, libraries, or approaches used
      - Anything else they'd like clarified

  **If** *user asks for explanations*:
      - **Action:** Provide clear, contextual explanations tailored to {user_skill_level}
      - **Action:** Use examples and references to specific code when helpful
  - **Action:** Once explanations are complete (or user indicates no questions), suggest logical next steps
  - **Action:** Recommended next steps (flexible based on project setup):
      - Review the implemented story and test the changes
      - Verify all acceptance criteria are met
      - Ensure deployment readiness if applicable
      - Run `code-review` workflow for peer review
      - Optional: If Test Architect module installed, run `/bmad:tea:automate` to expand guardrail tests

💡 **Tip:** For best results, run `code-review` using a **different** LLM than the one that implemented this story.

  **If** *{sprint_status} file exists*:
      - **Action:** Suggest checking {sprint_status} to see project progress
  - **Action:** Remain flexible - allow user to choose their own path or ask for other assistance

---

## ✅ Workflow Complete

Append `step-10-communication` to the `stepsCompleted` array in the story file's frontmatter.
Update `lastUpdatedAt` with current ISO timestamp.

**HALT** — Workflow complete. Await user instruction.
