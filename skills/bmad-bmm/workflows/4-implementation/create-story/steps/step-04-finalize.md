## Step 6 — Update sprint status and finalize

> **Invoke Task:** Validate against checklist at {installed_path}/checklist.md using skills/bmad-init/core/tasks/validate-workflow.md
- **Action:** Save story document unconditionally

**If** sprint status file exists:
  - **Action:** Update {{sprint_status}}
  - **Action:** Load the FULL file and read all development_status entries
  - **Action:** Find development_status key matching {{story_key}}
  - **Action:** Verify current status is "backlog" (expected previous state)
  - **Action:** Update development_status[{{story_key}}] = "ready-for-dev"
  - **Action:** Save file, preserving ALL comments and structure including STATUS DEFINITIONS
- **Action:** Report completion

**🎯 ULTIMATE BMad Method STORY CONTEXT CREATED, {user_name}!**

      **Story Details:**
      - Story ID: {{story_id}}
      - Story Key: {{story_key}}
      - File: {{story_file}}
      - Status: ready-for-dev

      **Next Steps:**
      1. Review the comprehensive story in {{story_file}}
      2. Run dev agents `dev-story` for optimized implementation
      3. Run `code-review` when complete (auto-marks done)
      4. Optional: If Test Architect module installed, run `/bmad:tea:automate` after `dev-story` to generate guardrail tests

      **The developer now has everything needed for flawless implementation!**

---

**HALT** — Workflow complete. Await user instruction.
