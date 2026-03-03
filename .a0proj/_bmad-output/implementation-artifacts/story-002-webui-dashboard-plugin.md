---
id: "002"
title: "BMAD WebUI Dashboard Plugin"
status: done
phase: 4-implementation
author: Bob (bmad-sm)
date: 2026-03-01
source-prd: planning-artifacts/prd-bmad-status-dashboard.md
source-arch: planning-artifacts/architecture-bmad-status-dashboard.md
supersedes: story-001-agent-health-check.md
---

# Story 002 — BMAD WebUI Dashboard Plugin

## User Story

As a **BMAD framework developer**,
I want **a native Agent Zero WebUI plugin that shows BMAD framework health in a sidebar-accessible modal dashboard**,
So that **I can monitor agent health, skill status, project state, and Langfuse telemetry without leaving the Agent Zero interface and without the `file://` CORS limitations of a standalone HTML file**.

---

## Background

Story 001 delivered `dashboard.html` — a standalone prototype that met all ACs in isolation. However, Chrome (and all Chromium-based browsers) block `fetch()` requests over the `file://` protocol due to CORS security restrictions. This causes the health checks to silently fail when the file is opened locally, making the artifact non-functional in practice.

This story documents the production solution: a native Agent Zero WebUI plugin that performs health checks server-side via a Python API handler, eliminating the CORS limitation entirely.

---

## Acceptance Criteria

### AC-002-01 — Sidebar Button Present
- A dashboard icon button (Material Design `dashboard` icon) is present in the Agent Zero WebUI sidebar
- Button is accessible on all pages of the Agent Zero UI
- Button renders via the Agent Zero extension system (`sidebar-quick-actions-main-start`)

### AC-002-02 — Modal Dashboard Opens on Click
- Clicking the sidebar button opens a modal dashboard overlay
- Modal is rendered via the Agent Zero WebUI extension system
- Modal can be closed/dismissed

### AC-002-03 — All 20 BMAD Agents Shown with Health Status
- Dashboard displays all 20 BMAD agents by name
- Each agent row shows visual health status: green (healthy) or red (broken)
- Status indicator uses icon + color (never color alone)
- Agent list: bmad-analyst, bmad-architect, bmad-agent-builder, bmad-brainstorming-coach, bmad-design-thinking, bmad-dev, bmad-innovation, bmad-master, bmad-module-builder, bmad-pm, bmad-presentation, bmad-problem-solver, bmad-qa, bmad-quick-dev, bmad-sm, bmad-storyteller, bmad-tech-writer, bmad-test-architect, bmad-ux-designer, bmad-workflow-builder

### AC-002-04 — Server-Side Health Check Logic
- Health determined server-side by the Python API handler
- Health check verifies presence of exactly 4 required prompt files per agent:
  - `agent.system.main.role.md`
  - `agent.system.main.communication.md`
  - `agent.system.main.communication_additions.md`
  - `agent.system.main.tips.md`
- Agent is healthy only when ALL 4 files are present
- No client-side `fetch()` calls to local filesystem

### AC-002-05 — All 5 BMAD Skills Shown with Health Status
- Dashboard displays all 5 BMAD skills: bmad-bmm, bmad-bmb, bmad-cis, bmad-tea, bmad-init
- Each skill shows health status based on presence of `SKILL.md`
- Visual indicator consistent with agent health display

### AC-002-06 — Project State Panel
- Dashboard shows current project phase from BMAD state file
- Dashboard shows active artifact from BMAD state file
- State read from `.a0proj/instructions/02-bmad-state.md`

### AC-002-07 — Langfuse Telemetry Panel
- Dashboard includes a Langfuse telemetry panel
- Panel renders when Langfuse is configured (LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY present)
- Panel gracefully degrades when Langfuse is not configured (shows "not configured" state)

### AC-002-08 — API Endpoint Available
- API endpoint `/api/plugins/bmad-dashboard/_bmad_status` is registered and responds
- Endpoint returns valid JSON health data structure
- JSON includes: agents array, skills array, project state object, langfuse object
- HTTP 200 on success; appropriate error codes on failure

### AC-002-09 — Agent Zero Plugin Architecture Compliance
- Plugin follows the Agent Zero plugin architecture exactly:
  - `plugin.yaml` at plugin root
  - `api/` subdirectory for API handlers
  - `webui/` subdirectory for frontend assets
  - `extensions/` subdirectory for UI injection points
- Plugin is loadable by the Agent Zero plugin loader without modification

### AC-002-10 — Zero Client-Side External Dependencies
- No CDN references in any plugin file
- No npm build step required
- No external JavaScript libraries loaded at runtime
- AlpineJS store pattern used for reactive UI (AlpineJS already bundled in Agent Zero WebUI)

### AC-002-11 — Accessible from All Agent Zero UI Pages
- Sidebar extension point (`sidebar-quick-actions-main-start`) ensures button renders on every page
- No page-specific routing required
- Dashboard accessible during any Agent Zero session state

---

## Technical Tasks

### Task 1 — Plugin Scaffold

Create plugin directory and manifest:
- Directory: `/a0/usr/plugins/bmad-dashboard/`
- `plugin.yaml` — plugin metadata, name, description, version, entry points
- Subdirectory structure: `api/`, `webui/`, `extensions/webui/sidebar-quick-actions-main-start/`

**Acceptance:** Plugin loads without error. Plugin appears in Agent Zero plugin registry.

---

### Task 2 — API Handler (`_bmad_status.py`)

Create server-side Python API handler:
- File: `/a0/usr/plugins/bmad-dashboard/api/_bmad_status.py`
- Reads agent directories from A0 agents path
- Checks presence of 4 required prompt files per agent (filesystem stat — no HTTP)
- Reads skill directories, checks `SKILL.md` presence
- Reads BMAD state file for project phase and active artifact
- Queries Langfuse REST API if credentials present in environment
- Returns structured JSON response

**Response schema:**
~~~json
{
  "agents": [
    {"name": "bmad-analyst", "healthy": true, "missing": []}
  ],
  "skills": [
    {"name": "bmad-bmm", "healthy": true}
  ],
  "state": {
    "phase": "ready",
    "active_artifact": "architecture-bmad-status-dashboard.md"
  },
  "langfuse": {
    "configured": true,
    "traces_count": 42
  }
}
~~~

**Acceptance:** `GET /api/plugins/bmad-dashboard/_bmad_status` returns HTTP 200 with valid JSON.

---

### Task 3 — AlpineJS Store (`bmad-dashboard-store.js`)

Create reactive frontend data store:
- File: `/a0/usr/plugins/bmad-dashboard/webui/bmad-dashboard-store.js`
- Alpine.js store registered as `bmadDashboard`
- Fetches `/api/plugins/bmad-dashboard/_bmad_status` on dashboard open
- Exposes reactive state: `agents`, `skills`, `projectState`, `langfuse`, `loading`, `error`
- Handles fetch errors gracefully — sets `error` state, does not throw

**Acceptance:** Store data flows to modal HTML without page reload. Loading and error states render correctly.

---

### Task 4 — Modal Dashboard HTML (`bmad-dashboard.html`)

Create dashboard modal UI:
- File: `/a0/usr/plugins/bmad-dashboard/webui/bmad-dashboard.html`
- Full modal overlay with close button
- Agent health grid: icon (✅/❌), agent name, status
- Summary banner: `X / 20 agents healthy` with color class
- Skills panel: 5 skill rows with health indicators
- Project state panel: phase + active artifact
- Langfuse panel: telemetry data or "not configured" message
- Inline CSS only — no external stylesheet
- Uses Alpine.js `x-data`, `x-show`, `x-for` directives bound to `bmadDashboard` store

**Acceptance:** All panels render. Data updates reactively from store. Modal opens/closes correctly.

---

### Task 5 — Sidebar Extension Button (`_bmad_dashboard_btn.html`)

Create sidebar icon button:
- File: `/a0/usr/plugins/bmad-dashboard/extensions/webui/sidebar-quick-actions-main-start/_bmad_dashboard_btn.html`
- Material Design `dashboard` icon button
- Click handler opens bmad-dashboard modal
- Consistent with existing Agent Zero sidebar action button styling
- Renders on every page via extension injection point

**Acceptance:** Button visible in sidebar. Click opens dashboard modal.

---

## Definition of Done

- [x] Plugin directory structure follows A0 plugin conventions (`plugin.yaml`, `api/`, `webui/`, `extensions/`)
- [x] API endpoint `/api/plugins/bmad-dashboard/_bmad_status` responds with valid JSON
- [x] Sidebar button appears in Agent Zero WebUI sidebar
- [x] All 20 BMAD agents checked server-side with correct health logic
- [x] All 5 BMAD skills checked server-side
- [x] Project state (phase + active artifact) readable from state file
- [x] Langfuse telemetry panel present and degrades gracefully when not configured
- [x] Zero CDN or npm dependencies — AlpineJS from Agent Zero bundle only
- [x] Dashboard accessible from all Agent Zero UI pages
- [x] AC-002-01 through AC-002-11 all verified
- [x] All plugin files present and verified at correct paths

---

## Dev Agent Record

### Implementation Notes

- **Task 1**: Plugin scaffold created. `plugin.yaml` defines name, version, description, and registers the API handler and WebUI extension points. Directory structure follows A0 plugin conventions exactly.
- **Task 2**: `_bmad_status.py` implements server-side health checks via Python `os.path.exists()` — no HTTP fetch, no CORS. Langfuse telemetry via REST API using `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` env vars with graceful fallback. Returns structured JSON.
- **Task 3**: `bmad-dashboard-store.js` registers Alpine.js store `bmadDashboard`. Fetches API on modal open. Exposes reactive `agents`, `skills`, `projectState`, `langfuse`, `loading`, `error` state. Error handling prevents silent failures.
- **Task 4**: `bmad-dashboard.html` modal uses Alpine.js directives bound to `bmadDashboard` store. Four panels: agents grid, skills list, project state, Langfuse. Inline CSS. Summary banner with `all-green`/`partial`/`critical` class logic mirrors Story 001 reference implementation.
- **Task 5**: `_bmad_dashboard_btn.html` injects via `sidebar-quick-actions-main-start` extension point — renders on all pages. Material `dashboard` icon. Click triggers store fetch + modal open.
- **Key architectural decision**: Server-side Python handler eliminates the `file://` CORS limitation that rendered Story 001 non-functional in practice. Health checks are now reliable regardless of browser security policy.

### Completion Notes

- All 5 plugin files verified present at correct paths.
- Plugin accessible via sidebar dashboard icon in Agent Zero WebUI.
- Server-side health checks confirmed functional — no browser CORS interference.
- All 11 ACs verified.

---

## File List

| File | Action | Task |
|------|--------|------|
| `/a0/usr/plugins/bmad-dashboard/plugin.yaml` | Created | 1 |
| `/a0/usr/plugins/bmad-dashboard/api/_bmad_status.py` | Created | 2 |
| `/a0/usr/plugins/bmad-dashboard/webui/bmad-dashboard-store.js` | Created | 3 |
| `/a0/usr/plugins/bmad-dashboard/webui/bmad-dashboard.html` | Created | 4 |
| `/a0/usr/plugins/bmad-dashboard/extensions/webui/sidebar-quick-actions-main-start/_bmad_dashboard_btn.html` | Created | 5 |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-03-01 | Story created — documents existing WebUI plugin implementation | Bob (bmad-sm) |
