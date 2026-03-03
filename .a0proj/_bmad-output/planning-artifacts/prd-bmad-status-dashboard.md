---
stepsCompleted: [step-01-init, step-02-discovery, step-03-success, step-04-journeys, step-05-domain, step-06-innovation, step-07-project-type, step-08-scoping, step-09-functional, step-10-nonfunctional, step-11-polish, step-12-complete, step-e-01-discovery, step-e-02-review, step-e-03-edit, step-v2-party-mode-overhaul]
inputDocuments: [brainstorm-session-1, brainstorm-session-2, brainstorm-session-3, brainstorm-session-4]
workflowType: prd
project: BMAD Status Dashboard
author: Vanja
date: 2026-03-01
lastEdited: 2026-03-01
editHistory:
  - date: 2026-03-01
    changes: v2.0 major overhaul — Party Mode brainstorm integration, scope expanded to Framework Status Intelligence System
  - date: 2026-03-01
    changes: v1.2 — Dark mode re-added as ADR-004 after removal experiment
  - date: 2026-03-01
    changes: v1.1 — Dark mode FR-07 added per stakeholder request
  - date: 2026-03-01
    changes: v1.0 — Initial PRD, agent health checker
status: draft-v2
---

# Product Requirements Document — BMAD Status Dashboard

**Author:** Vanja  
**PM:** John (BMAD Product Manager)  
**Date:** 2026-03-01  
**Version:** 2.0  
**Status:** Draft v2.0 — Pending Vanja Review  

---

## 1. Executive Summary

The BMAD Status Dashboard is a **Framework Status Intelligence System** — a Python-powered tool that provides at-a-glance visibility into the health, context, and next-action guidance for a BMAD-powered Agent Zero project.

V2.0 represents a complete scope expansion beyond the original agent health checker. The system now addresses **five live data sources**, delivers **two output formats** (rich HTML dashboard + concise markdown STATUS command), and is designed around a single governing principle established by Vanja across four Party Mode brainstorm sessions:

> **"Understand it first, then fix it."**

The dashboard's primary job is **legibility before action**. Every screen, every message, and every diagnostic follows the sequence: **WHAT → WHY → NEXT**. Never mixed, never reversed.

**Design North Star:** *"No surprises, only clarity."*

---

## 2. Problem Statement

The v1.2 dashboard solved one problem well: checking whether agent prompt files exist. But a BMAD session involves far more complexity than file presence:

- **Orientation failure:** Opening a conversation after hours away with no context on where you left off, what phase youâre in, or what the next action is
- **Silent staleness:** Dashboards showing data from hours ago with no freshness signal erode trust and cause bad decisions
- **Path-first language:** Error messages showing file paths instead of persona names create distance instead of urgency
- **Missing guidance:** Red status shown with no explanation of why it happened or how to fix it
- **Invisible telemetry:** No visibility into which agents are burning tokens, where failures are occurring, or what the session cost looks like
- **No continuity:** No way to recover from accidental state overwrites; no shift handoff when returning after inactivity

**The result:** A developer spends the first 5-15 minutes of every session reconstructing context that the system should have preserved.

**The core need:** A Framework Status Intelligence System that answers three questions instantly:
1. **Where am I?** (current phase, active artifact, active persona)
2. **Is everything healthy?** (agents, skills, tests, state, telemetry)
3. **What should I do next?** (single recommended action, always visible)

---

## 3. Design Principles

Established across four Party Mode brainstorm sessions (Sessions 1-4, 2026-03-01). These are not guidelines — they are constraints that all design and implementation decisions must satisfy.

| # | Principle | Meaning |
|---|-----------|--------|
| DP-01 | **Understand it first, then fix it** | Lead with WHAT before NEXT. Show the full picture before suggesting action. |
| DP-02 | **No surprises, only clarity** | Every data point is either actionable or anxiety-eliminating. Nothing in between. |
| DP-03 | **Persona-first, path-never** | Agents are people. "Bob is missing his role definition" — never a file path. |
| DP-04 | **Freshness builds trust** | Every data point has a timestamp. Stale data is worse than no data. |
| DP-05 | **One action wins** | The dashboard always knows what you should do next. One recommendation, never a menu. |
| DP-06 | **Orientation before action** | Answer "where am I?" before "what do I do?" Disoriented users make bad decisions. |
| DP-07 | **Context-aware mode** | After 2+ hours away: full orientation mode. Under 2 hours: compact heartbeat mode. |
| DP-08 | **WHAT/WHY/NEXT always** | Never show a problem without explaining the probable cause and offering explicit options. |

---

## 4. Goals and Non-Goals

### Goals
- Provide instant orientation: phase, active artifact, active persona, health summary, next action
- Surface health status for all five data sources with freshness timestamps
- Deliver WHAT/WHY/NEXT diagnostics — never a red light without a path forward
- Support two output modes: rich HTML dashboard and concise markdown STATUS command
- Integrate LLM telemetry from Langfuse (token cost, latency, error traces)
- Enable one-click state rollback from the last 5 state snapshots
- Require zero dependencies to run — single Python script, single HTML file
- Use persona-first language throughout — agents are people, not file paths

### Non-Goals
- Real-time auto-refresh or file watching
- Agent configuration editing from the dashboard
- Mobile / responsive design (developer tool, desktop only)
- Authentication or access control
- Supporting non-BMAD Agent Zero agents
- Editing or repairing agent files from within the dashboard

---

## 5. Users and Stakeholders

### Primary User: Vanja (Framework Developer)
- Builds and extends the BMAD framework
- Needs fast context recovery at session start after any absence duration
- Needs cost/performance visibility to optimize agent prompts
- Comfort level: technical, CLI-fluent
- **Jobs-to-be-done:**
  - "When I start a session, I want to know exactly where I left off without reconstructing it from memory"
  - "When something is broken, I want to know what broke, why, and the exact steps to fix it"
  - "When Iâm mid-session, I want a quick status check without leaving my workflow"

### Secondary User: BMAD Power User
- Uses BMAD heavily for product work
- Needs assurance the framework is intact before a session
- Comfort level: intermediate, prefers GUI over CLI

### Tertiary User: BMad Master (Orchestrator Agent)
- Activates at conversation start and needs structured session context
- Consumes the markdown STATUS output to orient itself
- **Job:** "Inject framework state into my context before responding to any user request"

---

## 6. Five Data Sources

All data is **live, never cached** except where explicitly noted. Each source has a required freshness indicator.

| # | Source | Path | Data Retrieved | Freshness Signal |
|---|--------|------|---------------|------------------|
| DS-01 | BMAD State File | `.a0proj/instructions/02-bmad-state.md` | Phase, active artifact, active persona, open defects, session context | File modification timestamp |
| DS-02 | Agent Manifest | `agents/*/agent.yaml` + `agents/*/prompts/` | 20-agent health check — all required prompt files present? | Scan timestamp (live per run) |
| DS-03 | Skill Symlinks | `skills/bmad-*/SKILL.md` | 5 skill symlinks alive and resolving? | Scan timestamp (live per run) |
| DS-04 | Test Reports | `test-artifacts/behavioral-test-report*.md` | Last test report filename, timestamp, pass/fail summary | File modification timestamp |
| DS-05 | Langfuse API | Langfuse REST API (via `langfuse` A0 skill) | Trace count, token usage per agent, avg latency, error traces, estimated cost | API response timestamp; fetched at HTML generation time |

---

## 7. Functional Requirements

### Core Health Check (Preserved from v1.x)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | Display health status (🟢/🔴) for all 20 BMAD agents using persona names, not directory paths | Must Have |
| FR-02 | Show agent persona name and role alongside health indicator | Must Have |
| FR-03 | List missing files in WHAT/WHY/NEXT format when an agent is unhealthy | Must Have |
| FR-04 | Display overall health score (X/20 agents ready) with freshness timestamp | Must Have |
| FR-05 | Support configurable base path for agent directory via Python CLI `--base-path` arg | Must Have |
| FR-06 | Generate dashboard via Python CLI with `--base-path` and `--output` args | Must Have |

### STATUS Command

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-07 | Provide a `STATUS` command: `python bmad-status.py --format markdown` that queries all 5 live data sources and returns a concise markdown summary | Must Have |
| FR-08 | STATUS output must include: phase, active artifact, active persona, agent health score, skill health, last test result — each with a freshness timestamp | Must Have |
| FR-09 | STATUS output must not exceed 30 lines; designed for injection into agent context at session start | Must Have |
| FR-10 | STATUS command must complete in under 5 seconds including all data source reads | Must Have |

### Auto-Brief on Session Start

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-11 | BMad Master must run the STATUS command at the start of each new conversation and surface the output as the first response element | Must Have |
| FR-12 | Auto-brief is a session-start pattern only — not triggered on every tool call or agent action | Must Have |

### Three-Layer Dashboard Layout

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-13 | Dashboard renders in three named layers: **NOW** (current orientation), **NEXT** (actionable guidance), **HEALTH** (deep diagnostics) | Must Have |
| FR-14 | The NOW layer must be visible without scrolling — first thing seen on dashboard open | Must Have |
| FR-15 | HEALTH layer details are collapsed by default; expand on demand | Must Have |

### Vital Signs Panel (NOW Layer)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-16 | Always-visible panel showing 6 critical metrics: Phase, Active Artifact, Active Persona, Agent Health (X/20), Skill Health (X/5), Last Test Result | Must Have |
| FR-17 | Each vital sign metric displays a freshness timestamp in human-relative format ("3 min ago", not ISO timestamp) | Must Have |
| FR-18 | Each metric uses 🟢/🟡/🔴 color coding with a text label (not color-only) | Must Have |

### Next Action Recommendation Engine (NEXT Layer)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-19 | Always display exactly one recommended next action — never empty, never a menu | Must Have |
| FR-20 | Recommendation is derived from a decision table mapping (current phase × artifact presence × defect count) → recommended action | Must Have |
| FR-21 | Action must be expressed as an imperative directive: "Start implementing Story-001" not "Implementation phase detected" | Must Have |
| FR-22 | Decision table must cover all BMAD phases and common transition states (see Section 10) | Must Have |

### WHAT/WHY/NEXT Diagnostic Framework

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-23 | Every 🔴 or 🟡 health indicator must expand to show a WHAT/WHY/NEXT panel | Must Have |
| FR-24 | WHAT: exact symptom in persona-first language — "Bob (Scrum Master) is missing his role definition" | Must Have |
| FR-25 | WHY: probable cause from a failure pattern knowledge base (3-5 common causes per failure type) | Must Have |
| FR-26 | NEXT: numbered list of 2-4 concrete, immediately-actionable options — no further investigation required | Must Have |
| FR-27 | Knowledge base must cover known failure patterns for: agents, skills, state file, test reports | Must Have |

### Persona-First Language

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-28 | All agent references use persona name + role: "Bob (Scrum Master)" not "bmad-sm" | Must Have |
| FR-29 | All health messages use human language: "3 agents need attention" not "CRITICAL: 3 FAILED" | Must Have |
| FR-30 | Tone throughout: informative, calm, confident — never alarming, never hedging | Must Have |

### Context-Aware Mode

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-31 | Detect elapsed time since last project activity using file modification timestamps | Should Have |
| FR-32 | If elapsed > 2 hours: display **Orientation Mode** — full context panel with session resume narrative | Should Have |
| FR-33 | If elapsed < 2 hours: display **Heartbeat Mode** — compact delta view showing only changes and critical alerts | Should Have |
| FR-34 | Mode switch is automatic — no manual toggle required | Should Have |

### Shift Handoff Summary

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-35 | When orientation mode triggers, display a Session Resume narrative: what was active → what happened → where to go | Should Have |
| FR-36 | Resume narrative reads state file, computes time-since-activity, shows last active story and recommended first action | Should Have |

### State Rollback

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-37 | Maintain rolling history of last 5 state file snapshots in `.state-history/` directory | Should Have |
| FR-38 | Dashboard shows snapshot list with timestamp and diff summary | Should Have |
| FR-39 | Restore action copies selected snapshot back to `02-bmad-state.md` with a confirmation prompt | Should Have |
| FR-40 | Post-restore: dashboard refreshes to reflect restored state | Should Have |

### Langfuse LLM Telemetry Panel

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-41 | Display LLM telemetry panel showing: trace count, token usage per agent, average latency per workflow, error traces, estimated session/project cost | Must Have |
| FR-42 | Langfuse data fetched at HTML generation time by the Python script via the `langfuse` A0 skill; embedded as static JSON payload in HTML | Must Have |
| FR-43 | Telemetry panel shows data generation timestamp prominently — user must know when data was fetched | Must Have |
| FR-44 | Token usage per agent sorted descending — most expensive agents surfaced first | Must Have |
| FR-45 | Error traces shown with agent name, workflow, timestamp, and error summary | Must Have |
| FR-46 | If Langfuse is unreachable: show a graceful fallback message with timestamp of last successful fetch | Must Have |

### Dark Mode (Preserved from v1.x)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-47 | Dashboard renders correctly in dark mode via `prefers-color-scheme: dark` — no manual toggle | Should Have |

