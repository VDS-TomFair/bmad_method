<!-- Validate mode -->

<step n="30" goal="Validate sprint-status file">
  <action>Check that {sprint_status_file} exists</action>
  <check if="missing">
    <template-output>is_valid = false</template-output>
    <template-output>error = "sprint-status.yaml missing"</template-output>
    <template-output>suggestion = "Run sprint-planning to create it"</template-output>
    <action>Return</action>
  </check>

<action>Read and parse {sprint_status_file}</action>

<action>Validate required metadata fields exist: generated, project, project_key, tracking_system, story_location</action>
<check if="any required field missing">
<template-output>is_valid = false</template-output>
<template-output>error = "Missing required field(s): {{missing_fields}}"</template-output>
<template-output>suggestion = "Re-run sprint-planning or add missing fields manually"</template-output>
<action>Return</action>
</check>

<action>Verify development_status section exists with at least one entry</action>
<check if="development_status missing or empty">
<template-output>is_valid = false</template-output>
<template-output>error = "development_status missing or empty"</template-output>
<template-output>suggestion = "Re-run sprint-planning or repair the file manually"</template-output>
<action>Return</action>
</check>

<action>Validate all status values against known valid statuses:</action>

- Stories: backlog, ready-for-dev, in-progress, review, done (legacy: drafted)
- Epics: backlog, in-progress, done (legacy: contexted)
- Retrospectives: optional, done
  <check if="any invalid status found">
  <template-output>is_valid = false</template-output>
  <template-output>error = "Invalid status values: {{invalid_entries}}"</template-output>
  <template-output>suggestion = "Fix invalid statuses in sprint-status.yaml"</template-output>
  <action>Return</action>
  </check>

<template-output>is_valid = true</template-output>
<template-output>message = "sprint-status.yaml valid: metadata complete, all statuses recognized"</template-output>
</step>

---

**HALT** — Validate mode complete. Return results to caller.
