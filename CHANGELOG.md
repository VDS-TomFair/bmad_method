# Changelog

All notable changes to the BMAD Method plugin are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---
## [1.1.0] — 2026-04-11

### BMK Marketing Module — New Module

#### Added

- **BMK Marketing Module** (`skills/bmad-mkt/`) — 46 workflows across 7 categories: discovery, strategy, setup, execution, growth, retention, and orchestration
- **3 new specialist agents:**
  - `bmad-marketing-strategist` (Elara) — market positioning, competitive analysis, go-to-market planning, customer research
  - `bmad-content-manager` (Mia) — content marketing, SEO, editorial planning, multi-channel distribution, campaign management
  - `bmad-growth-engineer` (Kai) — CRO, A/B testing, analytics, revenue operations, churn prevention
- **6 module skill** — `bmad-mkt` skill with full workflow library, module-help.csv routing, and config
- **Validation:** All 46 module-help.csv entries validated with zero broken references — see `skills/bmad-mkt/VALIDATION-REPORT.md`

#### Changed

- **Agent count:** 20 → 23 specialized agents
- **Skill count:** 5 → 6 global skills
- **Version bumped:** 1.0.8 → 1.1.0 (minor version — new module capability)

#### Notes

- BMK is a default-install module. To exclude, remove `skills/bmad-mkt/` and the 3 agent directories (`agents/bmad-marketing-strategist/`, `agents/bmad-content-manager/`, `agents/bmad-growth-engineer/`)

---

## [1.0.8] — 2026-04-10

### Sprint 10 — Gap Closure Sprint

#### Added

- **Skill Validator workflow (`VS`)** — New `skills/bmad-bmb/workflows/skill/workflow-validate-skill.md` (376 lines). Ports 27 rules (14 deterministic SKILL-01 → SEQ-02 + 13 LLM-inference) from upstream `tools/skill-validator.md`. Completes the BMB validation quartet: VA + VW + VM + VS. Executor: Bond (bmad-agent-builder)
- **File Reference Validator script (`VF`)** — New `skills/bmad-bmb/scripts/validate-file-refs.py` (310 lines, Python 3 stdlib only). Scans `*.md/*.yaml/*.csv` recursively for broken file path references; `--strict` mode exits non-zero on any broken reference. Executor: Amelia (bmad-dev)

#### Closed

- **GAP-002 CLOSED** — Skill Validator rules ported to BMB (Story 059)
- **GAP-003 CLOSED** — File Reference Validator script added (Story 060)
- **GAP-004 CONFIRMED CLOSED** — Code Review 3-layer sharding already implemented: Blind Hunter + Edge Case Hunter + Acceptance Auditor in `step-02-review.md`

#### Status

- **Upstream parity: ~98%** — only BMGD game dev module deferred

---

## [1.0.7] — 2026-04-10

### FM-015 Fix — Workflow Config Path Resolution + Variable Resolution

#### Fixed

- **Workflow config path references** — 3 workflow files referenced non-existent `{project-root}/_bmad/bmm/config.yaml`. Fixed to point to `skills/bmad-bmm/config.yaml` (which exists in A0 plugin structure). Affected: `quick-dev/workflow.md`, `code-review/workflow.md`, `checkpoint-preview/SKILL.md`
- **Variable resolution guidance for all 19 specialist agents** — Added `## A0 Variable Resolution` block to every specialist agent's `specifics.md`. Agents now know to resolve `{user_name}`, `{communication_language}`, `{output_folder}`, `{planning_artifacts}`, `{implementation_artifacts}` from injected `01-bmad-config.md` instead of attempting to load a config file. Eliminates literal `{placeholder}` leakage in specialist workflow execution.

---

## [1.0.6] — 2026-04-10

### Alignment Sprint — Menu Codes + Prompt Architecture

#### Added

- **Ideate Module (IM) workflow** — Morgan (bmad-module-builder) can now ideate new modules
- **Convert Skill (CW) workflow** — Wendy (bmad-workflow-builder) can convert workflows to skills — BMB parity complete

#### Changed

- **8 menu codes aligned with upstream**: CHK→CK, QD→QQ, ERP→EP, TRC→TR, BAG→BA, BS→SB, CVS→CW, CW→BW
- **Prompt architecture refactor** — BMAD framework moved to `specifics.md` (A0 design pattern slot), `solving.md` override added with BMAD workflow execution pattern, `communication.md` simplified to JSON format rules only, `tips.md` trimmed to remove duplicated principles
- All 20 agents updated with new prompt architecture

#### Result

- **100% upstream parity across all 5 modules** — 66/66 workflows routable

---

## [1.0.5] — 2026-04-09

### Validation Sprint — End-to-End Method Verification

#### Workflow Validation (11 tests, 10 agents, all PASS)

- **BP** (Mary — Brainstorm Project): Skill loaded, 8 steps, workflow.md found
- **CP** (John — Create PRD): Skill loaded, 12 steps, workflow-create-prd.md found
- **CA** (Winston — Create Architecture): Skill loaded, 9+1 steps
- **CU** (Sally — Create UX): Skill loaded, 14 steps, template found
- **CE** (John — Create Epics): Skill loaded, 4 steps, templates found
- **QA** (Quinn — QA Automation): Skill loaded, 6 steps, instructions found
- **TMT** (Murat — Teach Me Testing): Skill loaded, 15 steps, 43 knowledge fragments
- **BS** (Carson — Brainstorming): CIS agent activated, 8 techniques available
- **AE** (Advanced Elicitation): Core skill loaded, 30+ methods
- **DG** (Distillator): Core task loaded, 4-stage architecture
- **LW** (List Workflows): 42+ workflows discoverable, phase detection correct

#### Bugs Found & Fixed

- **Story 052 — CIS Routing Gap**: `_80_bmad_routing_manifest.py` excluded `cis` module from all phase module lists. Fixed by adding `cis` to all phases in `PHASE_MODULES` map.
- **SKILL.md Format Standardization**: 21 SKILL.md files referenced `workflow.yaml` but actual execution used `instructions.md` (BMM/CIS) or `workflow.md` (TEA). All references standardized.

#### autoresearch Milestones

- **Formal LLM evaluation working**: `run_eval.py` now uses A0 native model routing
- **Baseline**: Composite 7.775/10 → **Re-evaluation: 8.45/10** (+0.675)
- **Phase A L1 rules**: 10 BMAD-specific behaviour rules applied

#### Documentation

- **README v1.0.5 rewrite**: Restored agent roster table with emojis, added badges, Skills Architecture section
- Removed internal `.a0proj` links from README

---

## [1.0.4] — 2026-04-09

### Sprint 4 — Process & Documentation (Stories 037–040)

- **Party Mode Persona Guard (FM-019)**: 8 prescriptive rules added to all BMAD agents + PERSONA GUARD section added to `workflow.md` — prevents persona drift during multi-agent collaboration
- **Upstream BMAD Sync Check**: Audited 5 suspected missing workflows; confirmed only `prfaq` was missing (ported in Sprint 5)
- **README v1.0.3 update**: Added What's New section, quality metrics summary, document lifecycle link
- **Architecture doc updated to v1.0.3**: 703 lines, 13 sections, semver-aligned with plugin version

### Sprint 5 — Upstream Parity & Validation (Stories 041–044)

- **prfaq (Working Backwards) workflow ported**: 5 step files + assets + agents + module-help.csv row added to `bmad-bmm`
- **28 TEA extended knowledge files ported**: 43 total knowledge fragments now in `knowledge/bmad-test-architect/` (was 15)
- **BMM Phase 2 Routing Validation**: 6/6 PASS — PM (John) + UX (Sally) end-to-end routing confirmed. FM-006/007/008 CLOSED.
- **Behavioral test suite**: 60/60 PASS · Grade A+ (100/100) · zero regressions vs prior baseline

### Sprint 6 — autoresearch & Housekeeping (Stories 045–047)

- **autoresearch Phase A audit**: Root cause diagnosed — capture pipeline works correctly, optimizer loop never triggered due to insufficient conversation depth
- **autoresearch per-agent profiles**: 20 config files verified DONE across all agent profiles
- **State housekeeping**: 4 story files corrected (status + metadata), state inconsistencies in `02-bmad-state.md` resolved

---

## [1.0.3] — 2026-04-09

### Major Improvements — BMAD Harness Quality Initiative

Comprehensive system-wide improvement based on DeepWiki upstream analysis (4 BMAD repos) and A0 native audit. 25 failure modes identified and addressed across orchestration, workflow execution, specialist agents, and module infrastructure.

#### 🚨 Critical Fixes

- **FM-012 FIXED**: All 10 workflow instruction files referenced `workflow.xml` (non-existent) — fixed to `workflow.md`. The workflow execution engine now loads correctly in all BMM and TEA workflows for the first time.
- **FM-021 FIXED**: `_80_bmad_routing_manifest.py` now scans the filesystem for actual artifact existence using `output-location` + `outputs` columns from module-help.csv. Phase detection is now filesystem-based, not state-file-dependent. 15 unit tests added.
- **FM-023 FIXED**: `output-location` and `outputs` columns populated for all `required=true` rows in `skills/bmad-bmm/module-help.csv`. Phase gate artifact detection now works correctly.

#### 🔧 Workflow Improvements

- **Sharding**: 6 monolithic workflow instruction files (8–60KB each) sharded into 38 focused step files across dev-story, create-story, sprint-planning, sprint-status, correct-course, retrospective. Each step = one logical task + one HALT.
- **dev-story granularity**: 6 step files refined to 10 single-phase step files (step-01 through step-10).
- **stepsCompleted tracking**: Resume capability added to 4 key workflows (Create PRD, Create Architecture, Dev Story, Sprint Planning) — 26 files updated with Resume Check blocks and Step Complete markers.
- **FM-015 FIXED**: workflow.yaml config variables (`{communication_language}`, `{user_skill_level}`, `{user_name}`) confirmed unresolved by A0 natively. Mitigated by adding Workflow Variable Resolution table to `01-bmad-config.md`.

#### 🤖 Agent Quality

- **FM-017 FIXED**: All 19 agents enriched with 7+ action-oriented principles, precise communication style, and (for BMM agents) startup orientation instruction to read project state on activation. Zero compliance violations on Bond validation pass.
- **FM-016 FIXED**: Murat (bmad-test-architect) now has 14 core-tier knowledge fragments preloaded via FAISS (`.a0proj/knowledge/bmad-test-architect/`) and dynamic fragment loading in all 9 TEA workflow entry steps.
- `skills/bmad-tea/testarch/SKILL.md` wrapper created — testarch skill now directly loadable.

#### 📦 Module & Skills

- **CIS alignment**: Presentation workflow created for Caravaggio (`skills/bmad-cis/workflows/presentation/` — 4 files). All 6 CIS agents now routable via `LW`. CIS README updated.
- **FM-024**: Document Lifecycle Framework implemented — artifact relationship DAG, staleness detection (mtime-based, live in `_80` EXTRAS), `consistency-check.md` task, `docs/document-lifecycle.md` framework guide.
- **FM-022**: TEA SKILL.md wrapper created.

#### 🤖 autoresearch

- autoresearch plugin initialized for BMAD project. Per-project workspace created.
- System-wide optimization strategy v2.0 written (25 failure modes, 5 layers, all 19 profiles).
- 20 per-agent config files created — each profile has targeted cascade levels and failure mode focus.

#### ✅ Quality

- Behavioral test suite re-run: **54/54 PASS · Grade A (96/100) · 0 regressions** vs prior baseline.
- Test score improvement: B (89) → A (96) (+7 points).
- `tests/test_extension_80.py` added: 15 automated unit tests for routing extension.

---


## [1.0.2] — 2026-04-08

### Upstream Source Updates

**Core (BMM): 6.0.4 → 6.2.2**

- `code-review` workflow: full rewrite with sharded 4-step architecture (step-01 through step-04 + workflow.md), replacing the old workflow.yaml format
- `quick-dev` workflow: overhauled with new flat step structure (step-01 through step-05 + step-oneshot.md + spec-template.md)
- `checkpoint-preview`: new Phase 4 workflow added — LLM-assisted human-in-the-loop review (5 steps)
- Source references updated in `.a0proj/bmad-source/core/`

**BMB (Builder): 1.1.0 → 1.5.0**

- `agent-builder`: sanctum memory architecture added (BOND/CREED/MEMORY/PERSONA/PULSE/INDEX templates + bootloader), 26 new reference docs, 8 updated scripts
- `workflow-builder`: 18 new reference docs added + Workflow Convert capability scripts
- `module-builder`: 10 new assets (standalone + setup-skill templates), references, scripts
- `bmb-setup`: new skill added (module setup scripts + module-help.csv)
- Source references updated in `.a0proj/bmad-source/bmb/`

**TEA (Test Architect): 1.7.2 → 1.9.1**

- 13 old `*subprocess*` step files deleted — renamed to `*subagent*` terminology across all 9 workflows
- `playwright-cli.md` knowledge fragment added to workflow knowledge directories
- All step files (steps-c / steps-e / steps-v) synced from upstream
- Source references updated in `.a0proj/bmad-source/tea/`

**CIS: 0.1.9** — no change

### CSV and Routing Fixes

- Renamed `agent` → `skill` column in all `module-help.csv` headers (8 files) to align with upstream 13-column spec
- Added `checkpoint-preview` (code: `CHK`) to `bmad-bmm/module-help.csv`
- Added `bmb-setup` (code: `BS`) to `bmad-bmb/module-help.csv`
- Fixed `code-review` CSV path: `workflow.yaml` → `workflow.md`
- Fixed `code-review` SKILL.md to reference `workflow.md`

### Tests

- Behavioral regression: 49/49 PASS (0 PARTIAL, 0 FAIL)
- Fixed test harness `load_module_help_csvs()` to use top-level CSV only, matching runtime extension behavior

### Documentation

- README fully rewritten — value-first, audience-focused, no internal implementation details
- plugin.yaml description updated to reflect current state

---

## [1.0.1] — 2026-03-27

### Routing Extension

- Implemented dynamic lightweight (LW) routing — the `LW` command now reads directly from `skills/*/module-help.csv` at runtime, eliminating the sync risk with the compiled `bmad-help.csv` aggregate
- `_80_bmad_routing_manifest.py` column priority fixed: reads the `agent` column (the original column name) with `skill` and `agent-name` retained as legacy fallbacks
- Natural language routing fallback updated to also use dynamic module CSVs instead of the compiled aggregate
- Removed `_11_bmad_autobrief.py` extension — A0 natively auto-injects all `.a0proj/instructions/` files into every agent's system prompt; the extension was redundant

### Documentation Sprint 1 (Stories 016–018)

- `project-overview.md` refreshed with current architecture and story table
- `project-context.md` generated (LLM-optimized brownfield context)
- Architecture v4.0 document written
- Retrospective PRD authored — dogfooding gap closed

### Update Sprint 1 (Stories 019–023)

- `module-help.csv` format updated to 13-column upstream spec across all modules
- `bmad-bmm` skill updated to include all Phase 4 workflows
- `bmad-bmb` skill updated to BMB v1.2.0 (major restructure)
- `bmad-tea` skill updated to TEA v1.7.2 (skills migration)
- `bmad-cis` skill updated to CIS v0.1.9 (skill format conversion)
- Per-workflow thin SKILL.md wrappers implemented (Option B)

---

## [1.0.0] — 2026-02-28

### Initial Release

- Full BMAD Method Framework integration for Agent Zero
- 20 specialist agents across 4 modules: BMM, BMB, TEA, CIS
- 5 skill packages with bundled workflow files
- Project-scoped FAISS-native shared memory store
- Phase-aware routing extension (`_80_bmad_routing_manifest.py`)
- Interactive BMAD status dashboard plugin
- Party Mode (single-LLM multi-persona simulation)
- `bmad-init` bootstrap script for workspace initialization
- Phase Gate Protocol (GATE-001) enforcement
