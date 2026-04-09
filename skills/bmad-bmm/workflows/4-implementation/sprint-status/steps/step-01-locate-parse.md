# Sprint Status - Multi-Mode Service

<critical>The workflow execution engine is governed by: {project-root}/skills/bmad-init/core/tasks/workflow.md</critical>
<critical>You MUST have already loaded and processed: {project-root}/skills/bmad-bmm/workflows/4-implementation/sprint-status/workflow.yaml</critical>
<critical>Modes: interactive (default), validate, data</critical>
<critical>⚠️ ABSOLUTELY NO TIME ESTIMATES. Do NOT mention hours, days, weeks, or timelines.</critical>

<step n="0" goal="Determine execution mode">
  <action>Set mode = {{mode}} if provided by caller; otherwise mode = "interactive"</action>

  <check if="mode == data">
    <action>Load: {installed_path}/steps/step-03-data-mode.md</action>
  </check>

  <check if="mode == validate">
    <action>Load: {installed_path}/steps/step-04-validate-mode.md</action>
  </check>

  <check if="mode == interactive">
    <action>Continue to Step 1 below</action>
  </check>
</step>

<step n="1" goal="Locate sprint status file">
  <action>Load {project_context} for project-wide patterns and conventions (if exists)</action>
  <action>Try {sprint_status_file}</action>
  <check if="file not found">
    <output>❌ sprint-status.yaml not found.
Run `/bmad:bmm:workflows:sprint-planning` to generate it, then rerun sprint-status.</output>
    <action>Exit workflow</action>
  </check>
  <action>Continue to Step 2</action>
</step>

<step n="2" goal="Read and parse sprint-status.yaml">
  <action>Read the FULL file: {sprint_status_file}</action>
  <action>Parse fields: generated, project, project_key, tracking_system, story_location</action>
  <action>Parse development_status map. Classify keys:</action>
  - Epics: keys starting with "epic-" (and not ending with "-retrospective")
  - Retrospectives: keys ending with "-retrospective"
  - Stories: everything else (e.g., 1-2-login-form)
  <action>Map legacy story status "drafted" → "ready-for-dev"</action>
  <action>Count story statuses: backlog, ready-for-dev, in-progress, review, done</action>
  <action>Map legacy epic status "contexted" → "in-progress"</action>
  <action>Count epic statuses: backlog, in-progress, done</action>
  <action>Count retrospective statuses: optional, done</action>

<action>Validate all statuses against known values:</action>

- Valid story statuses: backlog, ready-for-dev, in-progress, review, done, drafted (legacy)
- Valid epic statuses: backlog, in-progress, done, contexted (legacy)
- Valid retrospective statuses: optional, done

  <check if="any status is unrecognized">
    <output>
⚠️ **Unknown status detected:**
{{#each invalid_entries}}

- `{{key}}`: "{{status}}" (not recognized)
  {{/each}}

**Valid statuses:**

- Stories: backlog, ready-for-dev, in-progress, review, done
- Epics: backlog, in-progress, done
- Retrospectives: optional, done
  </output>
  <ask>How should these be corrected?
  {{#each invalid_entries}}
  {{@index}}. {{key}}: "{{status}}" → [select valid status]
  {{/each}}

Enter corrections (e.g., "1=in-progress, 2=backlog") or "skip" to continue without fixing:</ask>
<check if="user provided corrections">
<action>Update sprint-status.yaml with corrected values</action>
<action>Re-parse the file with corrected statuses</action>
</check>
</check>

<action>Detect risks:</action>

- IF any story has status "review": suggest `/bmad:bmm:workflows:code-review`
- IF any story has status "in-progress" AND no stories have status "ready-for-dev": recommend staying focused on active story
- IF all epics have status "backlog" AND no stories have status "ready-for-dev": prompt `/bmad:bmm:workflows:create-story`
- IF `generated` timestamp is more than 7 days old: warn "sprint-status.yaml may be stale"
- IF any story key doesn't match an epic pattern (e.g., story "5-1-..." but no "epic-5"): warn "orphaned story detected"
- IF any epic has status in-progress but has no associated stories: warn "in-progress epic has no stories"
</step>

---

**HALT** — Await user response or explicit 'continue' before loading next step.

Next step: {installed_path}/steps/step-02-recommend-display.md
