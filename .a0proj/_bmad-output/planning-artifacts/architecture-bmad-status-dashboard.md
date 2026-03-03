---
version: 2.0
date: 2026-03-01
prd-version: 2.0
author: Winston (BMAD Architect)
changelog:
  - version: "2.0"
    date: 2026-03-01
    changes: >
      Full overhaul to match PRD v2.0. Scope expanded from single-file HTML agent
      health checker to Framework Status Intelligence System. Five data sources,
      STATUS command, auto-brief, three-layer HTML layout (NOW/NEXT/HEALTH),
      WHAT/WHY/NEXT diagnostic engine, next-action recommendation engine,
      context-aware mode, state rollback, Langfuse telemetry. ADR-009 through
      ADR-014 added. Mermaid system architecture diagram added. PERSONA_MAP
      architecture section added. All 8 design principles incorporated as
      architectural constraints.
  - version: "1.1"
    date: 2026-03-01
    changes: >
      Full rewrite to align with PRD v1.2. Previous architecture assumed Agent Zero
      plugin. PRD mandates zero-dependency single-file HTML with no frameworks.
  - version: "1.0"
    date: 2026-03-01
    changes: Initial architecture draft
---

# Architecture Document — BMAD Status Dashboard

**Author:** Winston (BMAD Architect)  
**Date:** 2026-03-01  
**Version:** 2.0  
**PRD Version:** 2.0  
**Status:** Updated

---

## Architecture Upgrade Notice — v1.1 to v2.0

> **What changed and why:**  
> PRD v2.0 expanded scope from a single-file HTML agent health checker to a
> **Framework Status Intelligence System**. This architecture has been fully
> rewritten to match. Nothing from v1.1 has been silently dropped — where v1.1
> decisions are preserved, the relevant ADR notes continuity explicitly.
>
> **Design constraint from PRD:** The eight Design Principles (DP-01..DP-08)
> established across four Party Mode brainstorm sessions are **architectural
> constraints**, not guidelines. Every design decision in this document must
> satisfy them. The governing principle: *"Understand it first, then fix it."*

---

## 1. Executive Summary

The BMAD Status Dashboard is a **Framework Status Intelligence System** — a
Python-powered, zero-dependency tool that answers three questions at any moment:

1. **Where am I?** Phase, active artifact, active persona — without reconstruction
2. **Is everything healthy?** Five live data sources, freshness-stamped, persona-first
3. **What should I do next?** One recommended action, always present, never a menu

The system delivers two output surfaces:

- **STATUS command**: Python CLI invoked by BMad Master at session start and on demand
  — concise markdown, max 30 lines, all 5 sources live
- **HTML Dashboard**: Single-file visual explorer — three-layer layout
  (NOW / NEXT / HEALTH), generated artifact, static at generation time

Both surfaces enforce persona-first language via a shared `PERSONA_MAP`.
All health messages follow the **WHAT -> WHY -> NEXT** sequence mandated by DP-08.
Freshness timestamps are present on every data point per DP-04.

The system requires zero external dependencies for DS-01..DS-04. DS-05 (Langfuse
telemetry) requires the `requests` library and valid Langfuse credentials — both
optional; all other sources degrade independently.

---

## 2. Design Principles as Architectural Constraints

Established in PRD v2.0 Section 3. These are not preferences — every architectural
decision must satisfy them.

| ID | Principle | Architectural Implication |
|----|-----------|--------------------------|
| DP-01 | **Understand it first, then fix it** | WHAT must always render before NEXT. No action card without a diagnostic card. |
| DP-02 | **No surprises, only clarity** | Every data point is actionable or anxiety-eliminating. Nothing rendered without purpose. |
| DP-03 | **Persona-first, path-never** | `PERSONA_MAP` enforced at data layer — no file paths in any user-facing output surface. |
| DP-04 | **Freshness builds trust** | Every DS result carries a freshness timestamp. Stale HTML must show generation time prominently. |
| DP-05 | **One action wins** | Recommendation engine always returns exactly one action. Empty state architecturally forbidden. |
| DP-06 | **Orientation before action** | NOW layer renders before NEXT layer. Auto-brief runs before any agent response. |
| DP-07 | **Context-aware mode** | 2-hour boundary: orientation (full) vs heartbeat (compact). Automatic, no toggle. |
| DP-08 | **WHAT/WHY/NEXT always** | Every red/yellow indicator expands to a three-layer diagnostic. No red light without a path forward. |

---

## 3. System Architecture Diagram

~~~mermaid
flowchart TD
    subgraph TRIGGERS["Trigger Surface"]
        CMD["User: STATUS command"]
        SESSION["New conversation start"]
        HTMLGEN["HTML generation request"]
    end

    subgraph BMAD_MASTER["BMad Master Agent"]
        COMM["communication_additions.md\nSTATUS hook + auto-brief hook"]
        CET["code_execution_tool\nterminal runtime"]
    end

    subgraph CLI["bmad-status.py - Python CLI"]
        ARGS["ArgParser\n--base-path --output --mode --sources"]
        CTX["ContextModeController\norientation | heartbeat"]
        ORCH["SourceOrchestrator\nparallel DS reads"]
        PM["PERSONA_MAP\ndir-name to display-name + icon"]
        DIAG["DiagnosticEngine\nWHAT / WHY / NEXT"]
        REC["RecommendationEngine\nDecision table, first-match"]
        SNAP["SnapshotWriter\n.state-history/ max 5"]
        REND["Renderer\nmarkdown | html | json | brief"]
    end

    subgraph DS["Five Data Sources"]
        DS01["DS-01 - State File\n02-bmad-state.md\nPhase / Artifact / Defects / ADRs"]
        DS02["DS-02 - Agent Manifest\nagents/*/agent.yaml\nagents/*/prompts/ x 4 files\n20 agents"]
        DS03["DS-03 - Skill Symlinks\nskills/bmad-*/SKILL.md\n5 skills"]
        DS04["DS-04 - Test Reports\ntest-artifacts/behavioral-test-report*.md\nLatest by mtime"]
        DS05["DS-05 - Langfuse API\nREST API v2 via requests\nTraces / Tokens / Latency / Cost"]
    end

    subgraph OUT["Output Surfaces"]
        MD["Markdown STATUS block\n30 lines max / freshness-stamped"]
        BRIEF["5-line auto-brief\nsession-start orientation"]
        HTML["bmad-status.html\nNOW / NEXT / HEALTH layers"]
        HIST[".state-history/\nJSON snapshots / max 5"]
    end

    CMD --> COMM
    SESSION --> COMM
    HTMLGEN --> COMM
    COMM --> CET
    CET --> ARGS
    ARGS --> CTX
    CTX --> ORCH
    ORCH --> DS01 & DS02 & DS03 & DS04 & DS05
    DS01 & DS02 --> PM
    PM --> ORCH
    ORCH --> DIAG
    ORCH --> REC
    ORCH --> SNAP
    DIAG --> REND
    REC --> REND
    ORCH --> REND
    REND --> MD & BRIEF & HTML & HIST
~~~

---
## 4. Component Architecture

### 4.1 bmad-status.py — Python CLI

**Path:** `/a0/skills/bmad-init/scripts/bmad-status.py`
(Symlinked into project at `/a0/usr/projects/a0_bmad_method/skills/bmad-init/scripts/`)

**CLI interface:**

~~~
usage: bmad-status.py [-h]
                      [--base-path PATH]
                      [--output PATH]
                      [--mode {status,brief,html,json}]
                      [--sources {ds01,ds02,ds03,ds04,ds05} [...]]
                      [--restore SNAPSHOT]

arguments:
  --base-path PATH    BMAD project root (default: auto-detect)
  --output PATH       Write output to file; default: stdout
  --mode MODE         Output format: status (default), brief, html, json
  --sources SRC ...   Subset of DS to query; default: all
  --restore SNAPSHOT  Restore named snapshot to 02-bmad-state.md
~~~

**Internal class structure** (all inline — single-artifact principle):

| Class | Responsibility |
|-------|----------------|
| `PersonaMap` | `PERSONA_MAP` dict + `persona()` lookup with icon fallback |
| `ContextModeController` | Read `.state-history/`, determine orientation vs heartbeat |
| `SourceOrchestrator` | Coordinate DS-01..DS-05 reads with timeout + error isolation |
| `SourceReader` | One method per DS: `read_ds01()` through `read_ds05()` |
| `DiagnosticEngine` | WHAT/WHY/NEXT three-layer analysis per issue |
| `RecommendationEngine` | `DECISION_TABLE` ordered tuples, first-match wins |
| `SnapshotWriter` | Write `.state-history/snapshot-{ts}.json`, prune to max 5 |
| `Renderer` | Format output: markdown / html / json / brief |

**Dependencies:**
- Python 3.8+ stdlib: `os`, `sys`, `re`, `json`, `glob`, `argparse`, `pathlib`, `datetime`, `urllib.request`
- Optional: `requests` (pip) for DS-05 — falls back to `urllib.request` if unavailable
- **No Node.js, no npm, no npx** required for any DS

---

### 4.2 Auto-Brief Component

**Trigger:** BMad Master `communication_additions.md` — session-start only (FR-12)
**Execution:** `python bmad-status.py --mode brief --sources ds01`

**5-line output contract (FR-11):**

~~~
📍 Phase: {phase} | Artifact: {active_artifact} | Persona: {active_persona}
🏥 Agents: {healthy}/20 healthy | Skills: {skill_count}/5 live
🔬 Last test: {test_result} ({test_age} ago)
⚠️  Open: {defect_count} defect(s) / {adr_count} ADR(s) pending
➡️  Recommended: {top_recommendation} -> {recommended_agent}
~~~

**Shift Handoff Summary** (orientation mode — FR-35, FR-36):
When elapsed time >= 2 hours, prepended before the 5-line brief:

~~~
🔄 Session Resume — last active {age} ago
   Was: {previous_phase} / {previous_artifact}
   Now: {current_phase} / {current_artifact}
   Recommended first action: {top_recommendation}
~~~

---

### 4.3 Three-Layer HTML Dashboard

The HTML dashboard renders in three named, ordered layers (FR-13..FR-15):

~~~
bmad-status.html
+-- Layer 1: NOW — Vital Signs Panel (always visible, no scroll — FR-14)
|   +-- 6 metric cards:
|   |     Phase / Active Artifact / Active Persona
|   |     Agent Health (X/20) / Skill Health (X/5) / Last Test Result
|   +-- Each card: green/yellow/red indicator + text label + "N min ago" timestamp
|
+-- Layer 2: NEXT — Action Panel (always visible, below NOW)
|   +-- Single recommended action card (FR-19) — imperative language (FR-21)
|   +-- Agent attribution: "-> Amelia (Developer)"
|   +-- Never empty — catch-all entry always fires (FR-19)
|
+-- Layer 3: HEALTH — Diagnostics (collapsed by default — FR-15)
    +-- Agent health grid (20 cards, CSS Grid 4-col)
    |     Each broken agent -> <details> WHAT/WHY/NEXT panel
    +-- Skill health list (5 entries + symlink status)
    +-- Test report summary (pass/fail counts, age)
    +-- Langfuse telemetry panel
    |     Trace count / Token usage per agent (sorted desc — FR-44)
    |     Avg latency p50/p95 / Error traces / Estimated cost
    |     Data generation timestamp prominently displayed (FR-43)
    +-- State Rollback panel (FR-37..FR-40)
          Last 5 snapshots: timestamp + diff summary
          Restore action with confirmation prompt
~~~

---

### 4.4 WHAT/WHY/NEXT Diagnostic Engine

Activated for every red or yellow indicator (FR-23). Output contract per issue:

~~~
WHAT: Bob (Scrum Master) is missing his role definition
WHY:  The agent directory was re-created without re-running bmad-init;
      the prompts/ folder is present but agent.system.main.role.md is absent.
NEXT:
  1. Re-run bmad-init for bmad-sm to restore default prompts
  2. Copy role prompt from /a0/skills/bmad-init/core/agents/bmad-sm/prompts/
  3. Investigate git history for unintentional deletion
~~~

**Failure pattern knowledge base (FR-27):**

| Failure Type | Known Patterns (WHY candidates) |
|-------------|--------------------------------|
| Agent missing / broken | Empty prompts/, symlink broken, partial init, agent.yaml absent, wrong base-path |
| Skill symlink broken | Symlink target moved, skills/ not symlinked, SKILL.md deleted |
| State file corrupt / missing | Manual edit error, failed heredoc write, file never initialized |
| No test report | Tests never run, report in wrong directory, wrong glob pattern |
| Langfuse unavailable | Env vars unset, API key expired, network unreachable, quota exceeded |

---

### 4.5 Next-Action Recommendation Engine

Pure deterministic if-statement logic. No AI. Input: aggregated state struct.

~~~python
# DECISION_TABLE — ordered list, first-match wins (ADR-011)
# Tuple: (condition_fn, action_template, agent_key, priority)
DECISION_TABLE = [
    (lambda s: s["open_defects"] > 0,
         "Resolve {n} open defect(s) before proceeding",
         "bmad-dev", 1),
    (lambda s: s["broken_agents"] > 0,
         "Restore {n} broken agent(s) — run bmad-init",
         "bmad-master", 2),
    (lambda s: s["broken_skills"] > 0,
         "Fix {n} broken skill symlink(s)",
         "bmad-master", 3),
    (lambda s: s["open_adrs"] > 0,
         "Elaborate {n} pending ADR(s)",
         "bmad-architect", 4),
    (lambda s: s["last_test_age_hrs"] > 24,
         "Run behavioral test suite — last run {age} ago",
         "bmad-test-architect", 5),
    (lambda s: s["langfuse_error_rate"] > 0.05,
         "Review LLM error traces — {pct}% error rate",
         "bmad-master", 6),
    (lambda s: s["phase"] == "Phase 4" and s["active_story"],
         "Continue implementing {story}",
         "bmad-dev", 7),
    (lambda s: True,
         "Framework healthy — continue current sprint",
         None, 99),  # catch-all: never empty
]
~~~

---

### 4.6 Context-Aware Mode Controller

~~~python
HEARTBEAT_THRESHOLD_HOURS = float(
    os.environ.get("BMAD_HEARTBEAT_HOURS", "2.0")
)  # ADR-010

def detect_mode(state_history_dir: Path) -> str:
    snapshots = sorted(state_history_dir.glob("snapshot-*.json"))
    if not snapshots:
        return "orientation"  # First run ever
    last = json.loads(snapshots[-1].read_text())
    age_hrs = (time.time() - last["captured_at"]) / 3600
    return "heartbeat" if age_hrs < HEARTBEAT_THRESHOLD_HOURS else "orientation"
~~~

| Mode | Sources | Max Lines | Triggers |
|------|---------|-----------|----------|
| `orientation` | DS-01..DS-05 | 30 | First run, or >= 2hrs since last snapshot |
| `heartbeat` | DS-01, DS-02 | 10 | Active session, < 2hrs since last snapshot |

---

### 4.7 State Rollback Component

**Snapshot format** (`.a0proj/.state-history/snapshot-{ISO}.json`):

~~~json
{
  "captured_at": 1740000000,
  "captured_at_iso": "2026-03-01T04:00:00Z",
  "phase": "Phase 4",
  "active_artifact": "story-001.md",
  "active_persona": "bmad-dev",
  "open_defects": 0,
  "open_adrs": 2,
  "source_hash": "sha256:abc123"
}
~~~

**Pruning:** After every write, sort snapshots lexicographically, delete all but
the 5 newest. Write is atomic: write `.tmp` then `os.rename()` on Linux.

**Restore flow:** HTML restore button -> JS confirm dialog -> on confirm:
`python bmad-status.py --restore snapshot-{ts}.json` -> script copies snapshot
state fields back to `02-bmad-state.md` -> page refresh shows restored state.

---

## 5. Data Source Specifications

### DS-01 — BMAD State File

| Attribute | Value |
|-----------|-------|
| **Path** | `{base_path}/.a0proj/instructions/02-bmad-state.md` |
| **Read mechanism** | `pathlib.Path.read_text()` + regex line extraction |
| **Fields** | `phase`, `active_artifact`, `active_persona`, `open_defects[]`, `open_adrs[]`, `session_context` |
| **Freshness signal** | `os.path.getmtime()` -> human-relative string ("3 min ago") |
| **Failure** | `FileNotFoundError` -> `Warning: State file missing` |
| **Parse strategy** | Regex per line: `Phase:`, `Active Artifact:`, `Persona:`, defect items (`- DEFECT-`) |

### DS-02 — Agent Manifest

| Attribute | Value |
|-----------|-------|
| **Paths** | `{base_path}/agents/{id}/agent.yaml` AND `{base_path}/agents/{id}/prompts/*.md` |
| **Read mechanism** | `Path.exists()` for agent.yaml; `glob()` for required prompt files |
| **Healthy definition** | `agent.yaml` present **AND** all 4 required prompt files present |
| **Required prompt files** | `agent.system.main.role.md`, `agent.system.main.communication.md`, `agent.system.main.communication_additions.md`, `agent.system.main.tips.md` |
| **Freshness** | Directory scan timestamp (live per run) |
| **Failure states** | Missing `prompts/` -> MISSING; any required file absent -> BROKEN; broken symlink -> SYMLINK_BROKEN |
| **Persona mapping** | Directory `id` -> display name via `PERSONA_MAP` |
| **Expected count** | 20 agents |

### DS-03 — Skill Symlinks

| Attribute | Value |
|-----------|-------|
| **Path** | `{base_path}/skills/bmad-*/SKILL.md` |
| **Read mechanism** | `Path.exists()` + `os.path.islink()` + `os.path.isfile()` (resolves through symlink) |
| **Fields** | Skill name, SKILL.md present, symlink target valid, version from front-matter |
| **Freshness** | Scan timestamp (live per run) |
| **Failure states** | Missing SKILL.md -> BROKEN; broken symlink target -> SYMLINK_BROKEN |
| **Expected count** | 5 skills (bmad-bmm, bmad-bmb, bmad-cis, bmad-tea, bmad-init) |

### DS-04 — Test Reports

| Attribute | Value |
|-----------|-------|
| **Path** | `{base_path}/.a0proj/_bmad-output/test-artifacts/behavioral-test-report*.md` |
| **Read mechanism** | `max(glob(...), key=os.path.getmtime)` -> regex parse of summary line |
| **Fields** | `total_checks`, `pass_count`, `fail_count`, `partial_count`, `overall_result`, `age_hrs` |
| **Freshness** | File `mtime` -> human-relative string |
| **Failure** | No files found -> `No test report available` (not an error state) |
| **Staleness threshold** | `age_hrs > 24` -> triggers recommendation to re-run tests |

### DS-05 — Langfuse LLM Telemetry

| Attribute | Value |
|-----------|-------|
| **Source** | Langfuse REST API v2 |
| **Host** | `LANGFUSE_HOST` env var (default: `https://cloud.langfuse.com`) |
| **Auth** | HTTP Basic Auth: `LANGFUSE_PUBLIC_KEY` (user) + `LANGFUSE_SECRET_KEY` (password) |
| **HTTP client** | `requests.Session` if available; stdlib `urllib.request` as fallback |
| **Timeout** | 5 seconds per request |
| **Freshness in STATUS** | Fetched live at execution time — never cached |
| **Freshness in HTML** | Fetched once at generation time; embedded as static JSON |
| **Failure states** | `unconfigured` (env vars absent), `unavailable` (network/API error), `ok` |
| **Security** | Keys never written to output; output scrubbed for `pk-lf-*`/`sk-lf-*` patterns |

**Endpoints queried:**

| Metric | Endpoint | Notes |
|--------|----------|-------|
| Trace count (7d) | `GET /api/public/traces?limit=1` | Use `meta.totalItems` |
| Daily token usage | `GET /api/public/metrics/daily?fromTimestamp={7d_ago}` | Sum `inputUsage` + `outputUsage` per model |
| Error traces | `GET /api/public/traces?tags=error&limit=50` | Extract name, timestamp, latency |
| Estimated cost | Daily metrics `totalCost` field | Only if model pricing configured in Langfuse |

Latency: fetch up to 200 traces (paginated), extract `latency`, compute p50/p95 client-side.

---

## 6. Langfuse Integration Architecture

### 6.1 Access Pattern Decision (see ADR-013)

The `langfuse` A0 skill recommends `npx langfuse-cli` for interactive agent use.
For `bmad-status.py`, `npx` introduces a Node.js dependency the PRD prohibits.
Resolution: `bmad-status.py` uses the Langfuse REST API directly via Python HTTP
(`requests` or `urllib.request`). The langfuse skill CLI remains available for
BMad Master when interactively querying Langfuse data outside the STATUS workflow.

### 6.2 LangfuseConnector Class Structure

The connector implements three public methods:

- `connect()` -> returns dict with `status: ok | unconfigured | unavailable`
- `_check_credentials()` -> reads env vars, returns (pk, sk, host) or raises
- `_fetch_all(host, pk, sk)` -> queries traces + daily metrics, computes p50/p95

Auth: HTTP Basic Auth with `LANGFUSE_PUBLIC_KEY` as user and `LANGFUSE_SECRET_KEY`
as password. Timeout: 5 seconds per request. No retry logic — fail fast and degrade.

### 6.3 Embedding Strategy for HTML Dashboard

Generated HTML embeds Langfuse data as an inline JavaScript constant at generation
time. The HTML never makes live API calls (ADR-013, ADR-003). The constant structure:

- `status`: `"ok"` / `"unavailable"` / `"unconfigured"`
- `fetched_at_iso`: ISO timestamp of when data was fetched
- `fetched_at_relative`: human-relative string ("2 hours ago")
- `trace_count_7d`: integer
- `top_agents_by_tokens`: array sorted descending by token count (FR-44)
- `avg_latency_p50_ms` / `avg_latency_p95_ms`: integers
- `error_count_7d`: integer
- `error_traces`: array of `{name, timestamp, latency}` objects
- `estimated_cost_usd`: float (null if pricing not configured)

When `status` is not `"ok"`, the Langfuse panel renders a graceful placeholder
with the status message. It never breaks the dashboard layout or throws JS errors.

### 6.4 Security Enforcement

- API keys read from environment only — never hardcoded, never written to output
- Renderer scrubs any string matching `pk-lf-[a-zA-Z0-9-]+` or `sk-lf-[a-zA-Z0-9-]+`
- `LANGFUSE_HOST` URL included in output (non-sensitive); keys are not
- Empty string env var -> skip DS-05 silently (no format hints revealing key pattern)
- LANGFUSE_DATA JS constant never contains auth material of any kind

---

## 7. Persona-First Language Architecture

### 7.1 PERSONA_MAP Definition

Defined at the top of `bmad-status.py`. All output surfaces reference this dict.
Unknown agent IDs fall back to `(id, "?")` — a visible signal to update the map.

| Directory Name | Display Name | Icon |
|----------------|-------------|------|
| bmad-agent-builder | Bond (Agent Builder) | 🔧 |
| bmad-analyst | Mary (Analyst) | 📊 |
| bmad-architect | Winston (Architect) | 🏗️ |
| bmad-brainstorming-coach | Carson (Brainstorming) | 💡 |
| bmad-design-thinking | Maya (Design Thinking) | 🌀 |
| bmad-dev | Amelia (Developer) | 💻 |
| bmad-innovation | Victor (Innovation) | 🚀 |
| bmad-master | BMad Master | 🎯 |
| bmad-module-builder | Morgan (Module Builder) | 📦 |
| bmad-pm | John (PM) | 📋 |
| bmad-presentation | Caravaggio (Presentation) | 🖼️ |
| bmad-problem-solver | Dr. Quinn (Problem Solver) | 🔍 |
| bmad-qa | Quinn (QA Engineer) | 🔬 |
| bmad-quick-dev | Barry (Quick Dev) | ⚡ |
| bmad-sm | Bob (Scrum Master) | 🏃 |
| bmad-storyteller | Sophia (Storyteller) | 📖 |
| bmad-tech-writer | Paige (Tech Writer) | 📝 |
| bmad-test-architect | Murat (Test Architect) | 🧪 |
| bmad-ux-designer | Sally (UX Designer) | 🎨 |
| bmad-workflow-builder | Wendy (Workflow Builder) | ⚙️ |

The `persona(agent_id)` helper is the single call site — no renderer formats
agent names directly. All 20 agents listed; unknown IDs produce a warning icon.

### 7.2 Enforcement Points

| Surface | Enforcement |
|---------|-------------|
| STATUS markdown output | All agent refs passed through `persona()` before formatting |
| Auto-brief | `persona()` used for active-persona and recommendation fields |
| WHAT/WHY/NEXT text | `DiagnosticEngine` resolves all agent IDs through `persona()` |
| Recommendation card | `agent_key` resolved through `persona()` for attribution line |
| HTML dashboard | JavaScript PERSONA_MAP const mirrors Python dict exactly |
| Langfuse telemetry panel | Trace names matched against PERSONA_MAP; display names substituted |
| Status messages | Human language: "3 agents need attention" not "CRITICAL: 3 FAILED" |

---

## 8. Delivery Architecture (v0.1 to v0.6)

### v0.1 — STATUS Command (Highest Priority)

**Delivers:** Python CLI with DS-01..DS-05, markdown STATUS output (max 30 lines)

**New components:**
- `bmad-status.py` with `SourceReader`, `PersonaMap`, `Renderer` (markdown mode)
- `RecommendationEngine` with initial `DECISION_TABLE`
- `SnapshotWriter` basic — captures DS-01 fields on every STATUS run

**BMad Master integration** added to `communication_additions.md`:

    When user types STATUS:
      Execute code_execution_tool (terminal runtime):
      python /a0/skills/bmad-init/scripts/bmad-status.py \
             --base-path /a0/usr/projects/a0_bmad_method
      Display result verbatim.

**File changes:**

    [NEW]  /a0/skills/bmad-init/scripts/bmad-status.py
    [MOD]  agents/bmad-master/prompts/communication_additions.md

---

### v0.2 — Auto-Brief on Session Start

**Delivers:** 5-line orientation summary prepended to every new BMad Master conversation

**New components:**
- `--mode brief` flag + `BriefRenderer` class
- DS-01 only in brief mode (lightweight, < 1s)
- `ContextModeController` (reads snapshot age, selects orientation vs heartbeat)
- Shift Handoff Summary for orientation mode (elapsed >= 2hrs)

**File changes:**

    [MOD]  /a0/skills/bmad-init/scripts/bmad-status.py
    [MOD]  agents/bmad-master/prompts/communication_additions.md
           (session-start hook: python bmad-status.py --mode brief --sources ds01)

---

### v0.3 — WHAT/WHY/NEXT Diagnostic Engine

**Delivers:** Three-layer issue analysis for every red/yellow indicator in STATUS

**New components:**
- `DiagnosticEngine` class
- Failure pattern knowledge base (5 failure categories, 3-5 WHY patterns each)
- WHAT/WHY/NEXT markdown renderer

**File changes:**

    [MOD]  /a0/skills/bmad-init/scripts/bmad-status.py  (DiagnosticEngine)

---

### v0.4 — Three-Layer HTML Dashboard

**Delivers:** `bmad-status.html` with NOW / NEXT / HEALTH layers

**New components:**
- `--mode html` flag + `HtmlRenderer` class
- `AGENT_CONFIG` + JavaScript PERSONA_MAP as inline constants (ADR-005)
- NOW layer: Vital Signs Panel (6 metrics, freshness timestamps)
- NEXT layer: Recommendation card with agent attribution
- HEALTH layer: Agent grid, skill list, test summary — collapsed (ADR-007)
- XHR + static-config fallback for DS-02 browser check (ADR-003)
- Dark mode via prefers-color-scheme (ADR-004, FR-47)

**File changes:**

    [MOD]  /a0/skills/bmad-init/scripts/bmad-status.py  (HtmlRenderer)
    [NEW]  /a0/usr/projects/a0_bmad_method/bmad-status.html

---

### v0.5 — Context-Aware Mode + State Rollback

**Delivers:** Orientation vs heartbeat mode; snapshot history with restore

**New components:**
- `ContextModeController` full version (all DS-01 fields captured)
- `SnapshotWriter` full (atomic write, max-5 pruning)
- State Rollback panel in HTML (snapshot list + restore + confirm dialog)
- `--restore {snapshot}` CLI flag

**File changes:**

    [MOD]  /a0/skills/bmad-init/scripts/bmad-status.py
    [NEW]  /a0/usr/projects/a0_bmad_method/.a0proj/.state-history/  (runtime)
    [MOD]  /a0/usr/projects/a0_bmad_method/bmad-status.html

---

### v0.6 — Langfuse LLM Telemetry

**Delivers:** DS-05 live in STATUS; Langfuse panel in HTML dashboard

**New components:**
- `LangfuseConnector` class (REST API v2, three failure states, 5s timeout)
- DS-05 markdown renderer (tokens/cost/latency/errors sorted desc — FR-44)
- HTML Langfuse panel with LANGFUSE_DATA static JSON constant (FR-41..FR-46)
- `--sources ds05` flag for Langfuse-only queries

**File changes:**

    [MOD]  /a0/skills/bmad-init/scripts/bmad-status.py
    [MOD]  /a0/usr/projects/a0_bmad_method/bmad-status.html

---

## 9. Architecture Decision Records

### ADR-001: Single-File HTML Architecture

| | |
|---|---|
| **Status** | Accepted — preserved from v1.1 |
| **Decision** | HTML dashboard is a single .html file with all CSS and JS inline. Runs via file:// protocol. Target size: under 50KB. |
| **Rationale** | Zero deployment friction (PRD goal G2). Any split creates a distribution problem. Vanilla CSS and JS at this scale needs no build step. |
| **Consequences** | All logic inline. No external assets. Generated by bmad-status.py --mode html. Editing requires only a text editor. |

### ADR-002: No JavaScript Framework

| | |
|---|---|
| **Status** | Accepted — preserved from v1.1 |
| **Decision** | Vanilla ES6+ and vanilla CSS only. No React, Vue, Alpine, jQuery, or CDN imports of any kind. |
| **Rationale** | PRD NFR-05 explicit prohibition. At target scale (20 agents, static render), framework overhead violates the 50KB constraint. |
| **Consequences** | DOM manipulation via native APIs. CSS Grid for agent health grid. details/summary for expand/collapse without JS. |

### ADR-003: Browser Filesystem Access — XHR + Static-Config Fallback

| | |
|---|---|
| **Status** | Accepted — preserved from v1.1, extended for v2.0 data model |
| **Decision** | HTML attempts XHR HEAD against file:// paths for live DS-02 agent check. If blocked (Chrome default), falls back to embedded AGENT_CONFIG with degradation banner. Python CLI is the authoritative live-check tool for all 5 DS. |
| **Rationale** | Browser file:// XHR policies are inconsistent across browsers and OS. Fallback ensures the tool never breaks — it degrades to a known-good display rather than an error page. |
| **Consequences** | Two JS code paths (live + static). DS-01, DS-03, DS-04, DS-05 always static in HTML (embedded at generation time). Python script covers live-check in restricted environments. |

### ADR-004: Dark Mode via prefers-color-scheme Only

| | |
|---|---|
| **Status** | Accepted — re-included in PRD v2.0 as FR-47 |
| **Decision** | Dark/light mode via CSS media query prefers-color-scheme: dark only. No manual toggle UI. |
| **Rationale** | Respects OS-level preference without JS or state management. Re-added in PRD v2.0 after brief removal in v1.2. |
| **Consequences** | No manual override. Acceptable trade-off for zero added complexity. |

### ADR-005: AGENT_CONFIG as Single Source of Truth

| | |
|---|---|
| **Status** | Accepted — preserved from v1.1 |
| **Decision** | A single AGENT_CONFIG JavaScript constant in the HTML defines all 20 expected agents. Python bmad-status.py maintains a matching list. Both derived from the canonical 20-agent roster. |
| **Rationale** | Prevents agent list from diverging between generator and consumer. Single edit point per roster change. |
| **Consequences** | HTML regeneration required when agent roster changes. PERSONA_MAP must also be updated simultaneously. |

### ADR-006: Agent Health Definition — agent.yaml + 4 Required Prompt Files

| | |
|---|---|
| **Status** | Accepted — updated from v1.1 |
| **Decision** | An agent is HEALTHY if agent.yaml exists AND all 4 required prompt files are present: agent.system.main.role.md, agent.system.main.communication.md, agent.system.main.communication_additions.md, agent.system.main.tips.md. |
| **Rationale** | PRD v2.0 DS-02 specifies agents/*/agent.yaml as a required health signal alongside prompt files. The v1.1 file-count thresholds (HEALTHY>=20, WARNING>=15) are replaced by the exact 5-artifact requirement for precision. |
| **Consequences** | Missing agent.yaml marks agent as BROKEN even if all prompts are present. More precise health signal than file count. |

### ADR-007: details/summary for Expandable Diagnostics

| | |
|---|---|
| **Status** | Accepted — preserved from v1.1, extended |
| **Decision** | HEALTH layer content (per-agent WHAT/WHY/NEXT panels, skill details, snapshot list) uses native HTML details/summary elements. Collapsed by default per FR-15. |
| **Rationale** | Native progressive disclosure. Accessible by default. Zero JS required for expand/collapse. |
| **Consequences** | Expand state does not persist on page refresh. Acceptable for a diagnostic tool. |

### ADR-008: Python CLI with --base-path, --output, --mode, --sources, --restore Args

| | |
|---|---|
| **Status** | Accepted — extended from v1.1 |
| **Decision** | bmad-status.py accepts --base-path (project root), --output (file vs stdout), --mode (status/brief/html/json), --sources (DS subset), and --restore (snapshot name). |
| **Rationale** | Enables use across project contexts and both interactive and automated modes. --mode brief enables lightweight auto-brief without full diagnostics. --restore enables state rollback from CLI. |
| **Consequences** | --base-path must be passed explicitly from BMad Master to avoid CWD ambiguity. All args have sensible defaults so bare invocation still works. |

### ADR-009: State Snapshot Storage

| | |
|---|---|
| **Status** | Accepted |
| **Decision** | State snapshots written to .a0proj/.state-history/snapshot-{ISO-timestamp}.json. Maximum 5 snapshots — oldest pruned atomically (os.rename) on each new write. Format: JSON. |
| **Rationale** | Context-aware mode (ADR-010) and state rollback (FR-37..FR-40) both require snapshot history. JSON is human-readable and trivially parseable. Max-5 balances history depth with storage discipline. Atomic rename prevents partial writes on Linux. |
| **Consequences** | .state-history/ created on first run. Directory must be gitignored. Pruning uses write-temp-then-rename sequence. |

### ADR-010: Context Mode Threshold — 2-Hour Boundary

| | |
|---|---|
| **Status** | Accepted |
| **Decision** | If last snapshot is under 2 hours old: heartbeat mode (DS-01+DS-02, max 10 lines). If 2 hours or older, or no snapshot exists: orientation mode (all DS, max 30 lines). |
| **Rationale** | 2 hours is a natural working-session boundary (PRD DP-07). Within a session, full re-orientation adds noise. Across sessions it is mandatory. First STATUS of any day is always orientation mode. |
| **Consequences** | HEARTBEAT_THRESHOLD_HOURS = 2.0 is a named constant. Overridable via BMAD_HEARTBEAT_HOURS env var without code change. |

### ADR-011: Next-Action Decision Table — Ordered Tuples, First-Match Wins

| | |
|---|---|
| **Status** | Accepted |
| **Decision** | Recommendation engine uses an ordered list of (condition_fn, action_template, agent_key, priority) tuples. First matching condition wins. Pure if-statement logic — no AI, no scoring. Must have a catch-all final entry so the engine never returns empty (FR-19). |
| **Rationale** | Deterministic, testable, auditable. Priority is explicit in ordering. No model changes needed to add conditions. Matches PRD FR-20 decision table requirement exactly. |
| **Consequences** | Condition ordering is critical — wrong order produces wrong recommendations. Catch-all entry is mandatory. Table must be reviewed when new BMAD phases or failure modes are added. |

### ADR-012: STATUS Command as Python CLI, HTML as Separate Generated Artifact

| | |
|---|---|
| **Status** | Accepted |
| **Decision** | The STATUS command is bmad-status.py --mode status (markdown, live, all 5 DS). The HTML dashboard is bmad-status.py --mode html (generated file, static at generation time). They share data model and PERSONA_MAP but are distinct outputs with different freshness guarantees. |
| **Rationale** | Python CLI runs in Agent Zero code_execution_tool with full filesystem access. HTML runs in a browser sandbox. Different execution contexts require different delivery surfaces. |
| **Consequences** | HTML Langfuse data is static at generation time; STATUS always fetches live. Explicit regeneration step required for fresh HTML data. Both surfaces must stay in sync when data model changes. |

### ADR-013: Langfuse Integration — REST API Directly, Not langfuse-cli

| | |
|---|---|
| **Status** | Accepted |
| **Decision** | bmad-status.py queries Langfuse via Python HTTP (requests or urllib.request). It does NOT use npx langfuse-cli subprocess. The langfuse A0 skill (npx CLI) is used for interactive agent use only, outside the STATUS workflow. |
| **Rationale** | npx langfuse-cli requires Node.js runtime — a dependency the PRD prohibits (zero external deps for DS-01..04; HTTP only for DS-05). The REST API provides the same data. |
| **Consequences** | requests pip install recommended for DS-05 (better timeout/error handling). urllib.request fallback ensures DS-05 works without requests. langfuse-cli remains available for BMad Master interactive use. |

### ADR-014: Persona-First Language Enforced at Data Layer

| | |
|---|---|
| **Status** | Accepted |
| **Decision** | PERSONA_MAP is the single source of truth for agent display names across all output surfaces. All agent references pass through persona() before any rendering. File paths and directory names never appear in user-facing output. |
| **Rationale** | PRD DP-03 and FR-28 are absolute constraints: agents are people, not file paths. Enforcing at the data layer prevents any renderer from accidentally exposing implementation details. |
| **Consequences** | Unknown agents fall back to directory name with warning icon — a visible signal to update the map. JavaScript PERSONA_MAP in HTML must be kept in sync with Python definition whenever agents are added or renamed. |

---

## 10. File Structure (Complete by Version)

    # v0.1 introduces:
    /a0/skills/bmad-init/scripts/
      bmad-status.py                          [NEW] Primary Python CLI

    /a0/usr/projects/a0_bmad_method/
      agents/bmad-master/prompts/
        communication_additions.md           [MOD] STATUS command hook

    # v0.2 modifies:
      agents/bmad-master/prompts/
        communication_additions.md           [MOD] Session-start auto-brief hook

    # v0.4 adds:
      bmad-status.html                       [NEW] Three-layer HTML dashboard (generated artifact)

    # v0.5 adds at runtime:
      .a0proj/
        .state-history/                      [NEW dir, gitignored]
          snapshot-{ISO}.json               [RUNTIME] Max 5, oldest pruned automatically

    # Source-of-truth references (read-only by CLI):
      .a0proj/instructions/02-bmad-state.md      DS-01
      agents/*/agent.yaml                        DS-02
      agents/*/prompts/*.md                      DS-02
      skills/bmad-*/SKILL.md                     DS-03
      .a0proj/_bmad-output/test-artifacts/
        behavioral-test-report*.md              DS-04

    # Planning artifacts (this document):
      .a0proj/_bmad-output/planning-artifacts/
        architecture-bmad-status-dashboard.md   This document (v2.0)
        prd-bmad-status-dashboard.md            PRD v2.0

---

## 11. Non-Functional Requirements

### 11.1 Performance

| Requirement | Target | Notes |
|-------------|--------|-------|
| STATUS (DS-01..04 only) | Under 3 seconds | Filesystem reads only — no network |
| STATUS (all DS including Langfuse) | Under 8 seconds | DS-05 HTTP timeout capped at 5s |
| Auto-brief (DS-01 only) | Under 1 second | Single file read + regex |
| Heartbeat mode | Under 1.5 seconds | DS-01 + DS-02 only |
| HTML generation (with Langfuse) | Under 10 seconds | Includes DS-05 fetch + file write |
| STATUS output length | 30 lines maximum | FR-09 hard constraint |
| HTML file size | Under 50KB | ADR-001, PRD NFR-03 |

### 11.2 Reliability and Graceful Degradation

| Failure Scenario | Behavior |
|-----------------|----------|
| DS-05 Langfuse unavailable | Section shows Langfuse unavailable — all other sections unaffected |
| DS-05 not configured | Message: set LANGFUSE_PUBLIC_KEY + LANGFUSE_SECRET_KEY |
| DS-04 no test report found | No test report available — not an error state |
| DS-02 agent directory missing | Agent shown as MISSING with WHAT/WHY/NEXT panel (v0.3+) |
| DS-01 state file missing | Warning: State file missing — project may not be initialized |
| DS-01 state file corrupt | Parse error caught — Warning: State file unreadable |
| .state-history/ unwritable | Context mode defaults to orientation — no crash, snapshot skipped |
| requests not installed | DS-05 falls back to urllib.request — no failure |
| Python under 3.8 | Explicit check at startup with human-readable error message |

### 11.3 Security

| Constraint | Implementation |
|------------|---------------|
| No API keys in output | Keys read from env only — output scrubbed for pk-lf-* and sk-lf-* patterns |
| No live network calls in HTML | Langfuse data embedded at generation time — HTML makes zero outbound requests |
| No file paths in user output | All agent refs mapped through PERSONA_MAP — absolute paths suppressed |
| Env var safety | Missing env vars cause graceful skip, not exception with env dump |
| Snapshot content | Snapshots contain only state metadata — no secrets, no prompt content |

### 11.4 Maintainability

- Single Python file — all logic inline, no external imports beyond stdlib + optional requests
- PERSONA_MAP and DECISION_TABLE at the top of the file — easy to update without reading implementation
- Each data source isolated in its own method (read_ds01 through read_ds05) — failures in one do not cascade
- All threshold constants named at module level: HEARTBEAT_THRESHOLD_HOURS, SNAPSHOT_MAX_COUNT
- Comprehensive --help output documents all flags and required env vars

---

## 12. Implementation Readiness Checklist

Before development of v0.1 begins, verify:

- [x] PRD v2.0 reviewed — all 47 FRs accounted for in architecture
- [x] All 8 Design Principles confirmed as architectural constraints (Section 2)
- [x] Dark mode (FR-47) re-included via prefers-color-scheme (ADR-004)
- [x] Agent canonical list (20 agents) confirmed against project agents/ directory
- [x] DS-02 health definition updated: agent.yaml + 4 prompt files (ADR-006)
- [x] Langfuse access pattern decided: REST API direct, not npx CLI (ADR-013)
- [x] Browser XHR fallback strategy preserved and extended (ADR-003)
- [x] Size budget confirmed feasible — approximately 18KB vs 50KB limit
- [x] Python stdlib-only for DS-01..DS-04 confirmed feasible
- [x] WCAG 2.1 AA approach: emoji + text labels, not color-only (Section 4.3)
- [x] State rollback architecture designed (FR-37..FR-40, ADR-009)
- [x] PERSONA_MAP complete — all 20 agents mapped (Section 7.1)
- [x] Three-layer HTML layout specified: NOW / NEXT / HEALTH (Section 4.3)
- [x] DECISION_TABLE structure defined with mandatory catch-all entry (Section 4.5)
- [x] Langfuse embedding strategy for HTML defined (Section 6.3)
- [ ] v0.1 dev story drafted for Amelia (Developer)
- [ ] ATDD scenarios covering orientation mode and heartbeat mode
- [ ] ATDD scenarios covering all 3 DS-05 failure states (ok / unavailable / unconfigured)
- [ ] ATDD scenarios covering WHAT/WHY/NEXT output for each failure category

---

*Architecture document maintained by Winston — BMAD Architect*
*Last updated: 2026-03-01 | Version: 2.0*
