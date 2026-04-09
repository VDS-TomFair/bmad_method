<step n="3" goal="Select next action recommendation">
  <action>Pick the next recommended workflow using priority:</action>
  <note>When selecting "first" story: sort by epic number, then story number (e.g., 1-1 before 1-2 before 2-1)</note>
  1. If any story status == in-progress → recommend `dev-story` for the first in-progress story
  2. Else if any story status == review → recommend `code-review` for the first review story
  3. Else if any story status == ready-for-dev → recommend `dev-story`
  4. Else if any story status == backlog → recommend `create-story`
  5. Else if any retrospective status == optional → recommend `retrospective`
  6. Else → All implementation items done; congratulate the user - you both did amazing work together!
  <action>Store selected recommendation as: next_story_id, next_workflow_id, next_agent (SM/DEV as appropriate)</action>
</step>

<step n="4" goal="Display summary">
  <output>
## 📊 Sprint Status

- Project: {{project}} ({{project_key}})
- Tracking: {{tracking_system}}
- Status file: {sprint_status_file}

**Stories:** backlog {{count_backlog}}, ready-for-dev {{count_ready}}, in-progress {{count_in_progress}}, review {{count_review}}, done {{count_done}}

**Epics:** backlog {{epic_backlog}}, in-progress {{epic_in_progress}}, done {{epic_done}}

**Next Recommendation:** /bmad:bmm:workflows:{{next_workflow_id}} ({{next_story_id}})

{{#if risks}}
**Risks:**
{{#each risks}}

- {{this}}
  {{/each}}
  {{/if}}

  </output>
  </step>

<step n="5" goal="Offer actions">
  <ask>Pick an option:
1) Run recommended workflow now
2) Show all stories grouped by status
3) Show raw sprint-status.yaml
4) Exit
Choice:</ask>

  <check if="choice == 1">
    <output>Run `/bmad:bmm:workflows:{{next_workflow_id}}`.
If the command targets a story, set `story_key={{next_story_id}}` when prompted.</output>
  </check>

  <check if="choice == 2">
    <output>
### Stories by Status
- In Progress: {{stories_in_progress}}
- Review: {{stories_in_review}}
- Ready for Dev: {{stories_ready_for_dev}}
- Backlog: {{stories_backlog}}
- Done: {{stories_done}}
    </output>
  </check>

  <check if="choice == 3">
    <action>Display the full contents of {sprint_status_file}</action>
  </check>

  <check if="choice == 4">
    <action>Exit workflow</action>
  </check>
</step>

---

**HALT** — Workflow complete. Await user instruction.
