## Step 3 — Detect review continuation and extract review context

> ⚠️ **CRITICAL:** Determine if this is a fresh start or continuation after code review
  - **Action:** Check if "Senior Developer Review (AI)" section exists in the story file
  - **Action:** Check if "Review Follow-ups (AI)" subsection exists under Tasks/Subtasks

  **If** *Senior Developer Review section exists*:
      - **Action:** Set review_continuation = true
      - **Action:** Extract from "Senior Developer Review (AI)" section:
        - Review outcome (Approve/Changes Requested/Blocked)
        - Review date
        - Total action items with checkboxes (count checked vs unchecked)
        - Severity breakdown (High/Med/Low counts)
      - **Action:** Count unchecked [ ] review follow-up tasks in "Review Follow-ups (AI)" subsection
      - **Action:** Store list of unchecked review items as {{pending_review_items}}

  ⏯️ **Resuming Story After Code Review** ({{review_date}})

        **Review Outcome:** {{review_outcome}}
        **Action Items:** {{unchecked_review_count}} remaining to address
        **Priorities:** {{high_count}} High, {{med_count}} Medium, {{low_count}} Low

        **Strategy:** Will prioritize review follow-up tasks (marked [AI-Review]) before continuing with regular tasks.

  **If** *Senior Developer Review section does NOT exist*:
      - **Action:** Set review_continuation = false
      - **Action:** Set {{pending_review_items}} = empty

  🚀 **Starting Fresh Implementation**

        Story: {{story_key}}
        Story Status: {{current_status}}
        First incomplete task: {{first_task_description}}

---

Append `step-03-detect-continuation` to the `stepsCompleted` array in the story file's frontmatter.
Update `lastUpdatedAt` with current ISO timestamp.

**HALT** — Await user response or explicit 'continue' before loading next step.

Next step: {installed_path}/steps/step-04-mark-in-progress.md
