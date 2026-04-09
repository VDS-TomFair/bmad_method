# Changelog

All notable changes to the BMAD Method plugin are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
