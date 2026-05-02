# Spec: BMAD Method Plugin — Alignment Fix Sprint (v2.0)

**Date:** 2026-05-02  
**Status:** Draft — pending user approval  
**Branch:** `develop` (merge to `main` on `/ship`)  
**Grounding:** `docs/bmad-alignment-audit.md` (87/100 score), `docs/alignment-analysis.md`, `docs/bmad-method-research.md`, `docs/docs-website-research.md`  
**Upstream Version:** v6.6.0

---

## Objective

Fix all alignment issues identified in the comprehensive alignment audit (87/100) plus three user-directed changes beyond the audit scope. The plugin has excellent workflow coverage (79/79 = 100%) and correct customization engine, but needs structural cleanup to match upstream v6.6.0 conventions.

**What we're fixing:**

- **A1:** Revert CSV routing to upstream YAML format (module.yaml) — Agent Zero can parse YAML natively
- **A2:** Remove CIS named personas (Victor, Dr. Quinn, Maya, Carson, Sophia, Caravaggio) — revert to upstream generic titles
- **A3:** Remove bmad-quick-dev agent — Quick Dev is a menu item under Amelia, not a separate agent
- **P1 fixes:** Consolidate SM/QA into Amelia, fix Morgan icon, fix Quick Dev menu code, add missing menus
- **P2 fixes:** Resolve icon collisions, update Sally's filmmaker style, address menu code collisions
- **P3 fixes:** Init script _bmad/custom/ creation, static agent table removal, 8-step activation sequence, project-context.md auto-loading, file-based sidecar memory

**Prior work (COMPLETE):** Phases A–H delivered 292+ tests, 60+ commits — full A0 alignment, upstream v6.6.0 sync, config migration, prompt architecture fixes, BMB path fixes. See [CHANGELOG.md](CHANGELOG.md).

**Target user:** Individual developer using Agent Zero for personal software projects. BMAD is **project-scoped** — each project gets independent BMAD state, initialization, and knowledge.

**What success looks like:**
- All CSV routing files converted to YAML module.yaml format
- Routing extension parses YAML instead of CSV
- SM/QA/Quick-dev agents removed; all their workflows in Amelia
- CIS agents use upstream generic titles with no named personas
- Morgan icon is 📦, Quick Dev code is QD, Sally uses filmmaker metaphor
- All 292+ existing tests continue to pass (updated for YAML)
- New tests cover YAML routing and agent consolidation
- ADR-0001 superseded by new ADR for YAML routing
- 8-step activation sequence matches upstream (resolve customization, hooks, persistent facts)
- project-context.md auto-loaded via persistent_facts processing
- File-based sidecar memory directories created and loaded per agent

---

## Tech Stack

| Layer | Technology | Notes |
|---|---|---|
| Runtime | Python 3.10+ | A0 plugin conventions; YAML parsing needs PyYAML or ruamel.yaml |
| YAML parsing | `yaml` (PyYAML) | stdlib `csv` replaced with `yaml.safe_load` |
| Init scripts | Bash | `set -euo pipefail` required |
| WebUI | Alpine.js + vanilla JS | Store-gated, `x-text` only (no `x-html`) |
| A0 version | `agent0ai/agent-zero:latest` ≥ 0.9.0 | Per `min_a0_version` in plugin.yaml |
| Key A0 imports | `helpers.api`, `helpers.projects`, `helpers.extension`, `agent.AgentContext`, `agent.LoopData` | Never re-implement these |
| Testing | `pytest` | Existing `tests/test_extension_80.py` pattern |
| VCS | Git | `develop` branch → `main` on `/ship` |
| Deployment | VPS `162.19.152.199` | Plugin dir mapped to testing instance |
| Upstream | BMAD-METHOD v6.6.0 | `.a0proj/upstream/BMAD-METHOD/` local clone |

---

## Commands

```bash
# Run all tests
cd /a0/usr/projects/a0_bmad_method && python -m pytest tests/ -v

# Run routing-specific tests
python -m pytest tests/test_extension_80.py tests/test_core_csv_schema.py -v

# Validate YAML syntax of all module.yaml files
for f in skills/*/module.yaml skills/bmad-init/core/module.yaml; do
  python -c "import yaml; yaml.safe_load(open('$f'))" && echo "✅ $f" || echo "❌ $f"
done

# Validate bash syntax
bash -n skills/bmad-init/scripts/bmad-init.sh

# Lint Python (max 100 chars)
python -m flake8 api/ helpers/ extensions/ --max-line-length 100

# Check HTML validity
tidy -e webui/bmad-dashboard.html 2>&1 | grep -E "^(Error|Warning)"

# Test BMAD init on arbitrary path (smoke test)
bash skills/bmad-init/scripts/bmad-init.sh /tmp/test-bmad-project
grep 'A0PROJ' /tmp/test-bmad-project/.a0proj/instructions/01-bmad-config.md
ls -la /tmp/test-bmad-project/.a0proj/_bmad/custom/  # must exist

# Verify agent directories removed
ls agents/bmad-sm agents/bmad-qa agents/bmad-quick-dev 2>&1 | grep 'No such file'

# Verify CIS personas removed (should output nothing)
grep -r 'Victor\|Dr. Quinn\|Maya\|Carson\|Sophia\|Caravaggio' agents/bmad-innovation/ agents/bmad-problem-solver/ agents/bmad-design-thinking/ agents/bmad-brainstorming-coach/ agents/bmad-storyteller/ agents/bmad-presentation/ || echo '✅ All CIS personas removed'

# Verify Morgan icon is 📦
grep '📦' agents/bmad-module-builder/agent.yaml

# Verify Quick Dev code is QD (not QQ)
grep -r 'QQ' skills/bmad-bmm/module.yaml && echo '❌ QQ still present' || echo '✅ QQ removed'

# Git workflow
git -C /a0/usr/projects/a0_bmad_method checkout -b develop

# Deploy to VPS testing instance
ssh -i /a0/usr/.ssh/id_ed25519 -o StrictHostKeyChecking=no root@162.19.152.199 \
  'docker exec agent-zero-testing bash -c "cd /a0/usr/projects/a0_bmad_method && git pull origin develop"'

# Live testing via A2A protocol
# a2a_chat → https://testing.emichi.co/a2a/t-uFypjRGDwc2M2NtW/p-test

# Docker logs
ssh -i /a0/usr/.ssh/id_ed25519 -o StrictHostKeyChecking=no root@162.19.152.199 \
  'docker logs agent-zero-testing --tail 100'
```

---

## Project Structure

```
/a0/usr/projects/a0_bmad_method/
├── plugin.yaml                          ← per_project_config: true
├── SPEC.md                              ← this file
├── CHANGELOG.md
├── README.md
├── .gitignore
│
├── api/
│   └── _bmad_status.py                  ← None-guard, _recommend() caching
│
├── helpers/
│   ├── __init__.py
│   └── bmad_status_core.py              ← read_state(), AGENT_NAMES, PHASE_ACTIONS
│
├── extensions/
│   ├── python/
│   │   └── message_loop_prompts_after/
│   │       └── _80_bmad_routing_manifest.py  ← ★ REWRITE: CSV → YAML parsing
│   └── webui/
│       └── sidebar-quick-actions-main-start/
│           └── _bmad_dashboard_btn.html
│
├── agents/                              ← ★ CONSOLIDATION: 21 → 18 profiles
│   ├── bmad-master/                     ← ★ Update: remove static agent table
│   ├── bmad-analyst/                    (Mary)
│   ├── bmad-pm/                         (John)
│   ├── bmad-architect/                  (Winston)
│   ├── bmad-dev/                        (Amelia) ← ★ Add: SS,VS,CC,QD menus
│   ├── bmad-ux-designer/                (Sally) ← ★ Fix: filmmaker style
│   ├── bmad-tech-writer/                (Paige) ← ★ Fix: add US menu
│   ├── bmad-module-builder/             (Morgan) ← ★ Fix: icon 📦
│   ├── bmad-agent-builder/              (Bond)
│   ├── bmad-workflow-builder/           (Wendy)
│   ├── bmad-test-architect/             (Murat)
│   ├── bmad-innovation/                 ← ★ Remove persona: Victor → Innovation Strategist
│   ├── bmad-problem-solver/             ← ★ Remove persona: Dr. Quinn → Creative Problem Solver
│   ├── bmad-design-thinking/            ← ★ Remove persona: Maya → Design Thinking Coach
│   ├── bmad-brainstorming-coach/        ← ★ Remove persona: Carson → Brainstorming Coach
│   ├── bmad-storyteller/                ← ★ Remove persona: Sophia → Storyteller
│   ├── bmad-presentation/               ← ★ Remove persona: Caravaggio → Presentation Master
│   ├── bmad-sm/                         ← ★ REMOVE ENTIRELY
│   ├── bmad-qa/                         ← ★ REMOVE ENTIRELY
│   └── bmad-quick-dev/                  ← ★ REMOVE ENTIRELY
│
├── skills/
│   ├── bmad-init/
│   │   ├── SKILL.md
│   │   ├── module-help.csv             ← ★ DELETE (replaced by module.yaml)
│   │   ├── core/
│   │   │   ├── config.yaml
│   │   │   └── module.yaml             ← ★ NEW: init module routing in YAML
│   │   └── scripts/
│   │       ├── bmad-init.sh            ← ★ Add _bmad/custom/ dir creation
│   │       └── bmad-status.py
│   ├── bmad-bmm/
│   │   ├── config.yaml
│   │   ├── module-help.csv             ← ★ DELETE (replaced by module.yaml)
│   │   ├── module.yaml                 ← ★ NEW: BMM routing in YAML
│   │   └── workflows/                  ← ✅ synced with upstream v6.6.0
│   ├── bmad-tea/
│   │   ├── config.yaml
│   │   ├── module-help.csv             ← ★ DELETE (replaced by module.yaml)
│   │   ├── module.yaml                 ← ★ NEW: TEA routing in YAML
│   │   └── workflows/
│   ├── bmad-cis/
│   │   ├── config.yaml
│   │   ├── module-help.csv             ← ★ DELETE (replaced by module.yaml)
│   │   ├── module.yaml                 ← ★ NEW: CIS routing in YAML
│   │   └── workflows/
│   ├── bmad-bmb/
│   │   ├── config.yaml
│   │   ├── module-help.csv             ← ★ DELETE (replaced by module.yaml)
│   │   ├── module.yaml                 ← ★ NEW: BMB routing in YAML
│   │   └── workflows/
│   ├── bmad-promote/
│   └── bmad-customize/
│
├── webui/
│   ├── bmad-dashboard.html
│   └── bmad-dashboard-store.js
│
├── prompts/
│   ├── bmad-agent-shared.md          ← ★ REWRITE: 8-step activation sequence
│   └── bmad-agent-shared-solving.md
│
├── _bmad/                              ← Created by init script in target project
│   ├── custom/                         ← Override TOML files
│   └── _memory/                        ← ★ NEW: sidecar memory directories
│       ├── analyst-sidecar/            ← Mary's persistent memory
│       ├── pm-sidecar/                 ← John's persistent memory
│       ├── architect-sidecar/          ← Winston's persistent memory
│       ├── dev-sidecar/                ← Amelia's persistent memory
│       ├── ux-designer-sidecar/        ← Sally's persistent memory
│       ├── tech-writer-sidecar/        ← Paige's persistent memory
│       ├── module-builder-sidecar/     ← Morgan's persistent memory
│       ├── agent-builder-sidecar/      ← Bond's persistent memory
│       ├── workflow-builder-sidecar/   ← Wendy's persistent memory
│       ├── test-architect-sidecar/     ← Murat's persistent memory
│       ├── innovation-sidecar/
│       ├── problem-solver-sidecar/
│       ├── design-thinking-sidecar/
│       ├── brainstorming-coach-sidecar/
│       ├── storyteller-sidecar/
│       └── presentation-sidecar/
│
├── scripts/
│   └── resolve_customization.py
│
├── docs/
│   └── adr/
│       ├── 0001-csv-canonical-routing.md   ← ★ SUPERSEDED by new ADR
│       └── 0010-yaml-canonical-routing.md   ← ★ NEW ADR
│
└── tests/                              ← Update existing + add new
    ├── test_extension_80.py            ← ★ UPDATE: YAML parsing tests
    ├── test_core_csv_schema.py         ← ★ RENAME → test_core_yaml_schema.py
    └── ... (292+ existing tests)
```

---

## Code Style

- **Python:** PEP 8, max 100 chars, `flake8` clean
- **YAML:** 2-space indent, quoted strings with special chars, consistent key ordering
- **Bash:** `set -euo pipefail`, shellcheck-clean where possible
- **Agent prompts:** Markdown with consistent header hierarchy (## for sections, ### for subsections)
- **Follow existing patterns:** The plugin has established conventions in `helpers/`, `extensions/`, `api/` — match them
- **No reimplementation:** Use A0 framework imports (`helpers.api`, `helpers.projects`, etc.) never rewrite them

---

## Testing Strategy

### Existing Tests (must continue to pass)
- 292+ tests from Phases A–H
- All routing tests in `test_extension_80.py`
- Customization merge tests in `test_resolve_customization.py`
- Config tests in `test_phase_f_config.py`
- Dashboard tests

### New Tests Required

| Test File | What It Tests |
|---|---|
| `test_yaml_routing.py` | YAML parsing, module loading, phase filtering, menu code lookup |
| `test_agent_consolidation.py` | SM/QA/Quick-dev removed; Amelia has all menus |
| `test_cis_personas.py` | No named personas in CIS agent files |
| `test_module_yaml_schema.py` | All 5 module.yaml files pass schema validation |
| `test_migration_csv_to_yaml.py` | CSV→YAML data equivalence (row count, fields preserved) |

### Verification Approach

1. **Unit tests:** Each task bundle has corresponding test coverage
2. **Integration test:** Full routing manifest generated from YAML matches expected output
3. **Smoke test:** `bmad-init.sh` on temp directory produces correct state
4. **A2A live test:** Send messages to testing instance, verify routing works
5. **Diff verification:** Compare routing manifest output before/after — must be functionally identical

---

## Boundaries

### Always
- Run full test suite before committing
- Preserve all 79+ workflow coverage
- Keep A0-specific adaptations (profile system, skills, webui extensions)
- Match upstream module.yaml format from `.a0proj/upstream/BMAD-METHOD/src/bmm-skills/module.yaml`
- Use `yaml.safe_load()` for parsing (no custom constructors)
- Update tests alongside code changes
- Keep `customize.toml` files untouched (customization system is correct)
- Preserve per-project isolation

### Ask First
- Changing any workflow step content (`.md` workflow files)
- Modifying the customization engine (`resolve_customization.py`)
- Changes to the dashboard WebUI
- Any modification to `plugin.yaml` beyond what's specified
- Adding new dependencies

### Never
- Modify A0 framework files (`/a0/` outside plugin)
- Remove or modify workflow step files unless explicitly part of a task
- Change the customization merge rules (they're correct)
- Reintroduce CSV files once removed
- Add new named personas to CIS agents
- Create new standalone agent directories for functionality that belongs in Amelia

---

## Success Criteria

### Functional Correctness
- [ ] Routing extension generates identical routing manifest from YAML as from CSV
- [ ] Phase filtering works correctly for all 4 phases + anytime + quick-flow
- [ ] Menu code lookup returns correct workflow for all 79+ codes
- [ ] Artifact detection (staleness warnings) works with YAML paths
- [ ] Dashboard displays correct phase status
- [ ] CLI `bmad-status.py` reports correct state
- [ ] `bmad-init.sh` creates `_bmad/custom/` directory

### Agent Consolidation
- [ ] `agents/bmad-sm/` directory does not exist
- [ ] `agents/bmad-qa/` directory does not exist
- [ ] `agents/bmad-quick-dev/` directory does not exist
- [ ] Amelia's customize.toml includes: SP, SS, VS, CS, CC, DS, CR, QA, CK, QD menus
- [ ] Quick Dev code is QD (not QQ)
- [ ] All SM/QA/Quick-dev workflows accessible through Amelia

### CIS Persona Removal
- [ ] No CIS agent.yaml contains named personas (Victor, Dr. Quinn, Maya, Carson, Sophia, Caravaggio)
- [ ] CIS agents use upstream generic titles: Innovation Strategist, Creative Problem Solver, Design Thinking Coach, Brainstorming Coach, Storyteller, Presentation Master
- [ ] CIS icon collisions resolved (🎨 no longer shared across Sally + CIS)
- [ ] CIS prompt files updated to match generic styling

### CSV→YAML Migration
- [ ] All 5 module-help.csv files replaced by module.yaml
- [ ] Routing extension uses `yaml.safe_load()` instead of `csv.DictReader`
- [ ] No code references `module-help.csv` or `module-help` pattern
- [ ] All tests updated to use YAML fixtures
- [ ] ADR-0001 superseded by ADR-0010

### Specific Fixes
- [ ] Morgan icon: 📦 (was 🏗️)
- [ ] Sally communication_style: filmmaker metaphor
- [ ] Paige customize.toml: includes US menu
- [ ] bmad-master role.md: no static 19-row agent table (uses `{{agent_profiles}}`)
- [ ] Init script: creates `_bmad/custom/` directory


### P3 Structural
- [ ] bmad-agent-shared.md follows full 8-step activation sequence
- [ ] resolve_customization.py called as first tool call during activation
- [ ] activation_steps_prepend and activation_steps_append hooks processed
- [ ] persistent_facts loaded from customize.toml (including project-context.md)
- [ ] File-based sidecar directories created for all 16 non-master agents
- [ ] Sidecar files loaded during activation, written at natural breakpoints
- [ ] project-context.md auto-loaded via persistent_facts in all implementation workflows
- [ ] Sidecar import skill available for upstream migration
- [ ] New tests cover activation sequence, sidecar read/write, project-context loading

### Test Suite
- [ ] All 292+ existing tests pass (updated for YAML)
- [ ] New YAML routing tests pass
- [ ] New agent consolidation tests pass
- [ ] New CIS persona tests pass
- [ ] Total test count ≥ 300

---

## Implementation Tasks

### Task Bundle 1: CSV → YAML Migration (A1)
**Priority:** P0 — foundational change, everything else depends on routing working  
**Effort:** M (1-2 days)  
**Depends on:** Nothing (start first)

#### 1.1 Define module.yaml schema
Create a consistent YAML schema that covers all 13 CSV columns. The upstream BMM `module.yaml` uses a different structure (agent-focused, not workflow-row-focused). Our YAML must be A0-adapted while maintaining upstream compatibility.

**Schema (per-workflow entries):**
```yaml
code: bmm
name: "BMad Method Agile-AI Driven-Development"
version: "6.6.0"

workflows:
  - module: bmm
    skill: analyst
    display-name: Brainstorm Project
    menu-code: BP
    description: "Expert Guided Facilitation through a single or multiple techniques"
    action: bmad-brainstorming
    args: "skills/bmad-bmm/workflows/1-analysis/brainstorming/workflow.md"
    phase: 1-analysis
    required: false
    output-location: planning_artifacts
    outputs: "brainstorming session"
```

**Verification:** Schema validates against all 5 existing CSVs with zero data loss.

#### 1.2 Convert all 5 module-help.csv files to module.yaml
Convert CSV rows to YAML workflow entries. Files to convert:

| CSV Source | YAML Target | Row Count |
|---|---|---|
| `skills/bmad-init/module-help.csv` | `skills/bmad-init/core/module.yaml` (init section) | ~5 |
| `skills/bmad-bmm/module-help.csv` | `skills/bmad-bmm/module.yaml` | 33 |
| `skills/bmad-tea/module-help.csv` | `skills/bmad-tea/module.yaml` | 9 |
| `skills/bmad-cis/module-help.csv` | `skills/bmad-cis/module.yaml` | 6 |
| `skills/bmad-bmb/module-help.csv` | `skills/bmad-bmb/module.yaml` | 19 |

**Important:** The init CSV is special — it contains core/anytime workflows that span modules. Its entries should be merged into the appropriate module.yaml files, with any init-specific entries going into `skills/bmad-init/core/module.yaml` under a separate key.

**Conversion script approach:** Write a one-time Python conversion script (`scripts/archive/csv_to_yaml_converter.py`) that:
1. Reads each CSV with `csv.DictReader`
2. Outputs YAML with `yaml.dump()` (default_flow_style=False)
3. Validates output round-trips correctly
4. Reports any data that doesn't map cleanly

**Acceptance criteria:**
- [ ] All 5 module.yaml files created
- [ ] Row counts match between CSV and YAML
- [ ] All 13 columns preserved as YAML fields
- [ ] `yaml.safe_load()` on each file succeeds without error
- [ ] Conversion script committed for documentation/reproducibility

#### 1.3 Rewrite routing extension for YAML
Update `_80_bmad_routing_manifest.py` to parse YAML instead of CSV.

**Key changes:**
- Replace `_read_csv_cached()` with `_read_yaml_cached()` using `yaml.safe_load()`
- Replace `_collect_routing_rows()` CSV reader with YAML workflow iterator
- Replace `_scan_artifact_existence()` CSV reader with YAML iterator
- Update `_csv_cache` → `_yaml_cache` (mtime-keyed caching preserved)
- Update glob from `*/module-help.csv` → `*/module.yaml`
- Phase filtering logic stays the same (filter by `phase` field)

**The routing manifest output format must NOT change.** The YAML is an input-side change only. The text block injected into `extras_temporary["bmad_routing_manifest"]` must be identical in structure.

**Acceptance criteria:**
- [ ] `_80_bmad_routing_manifest.py` contains zero `import csv` or `csv.` references
- [ ] `yaml.safe_load()` used for all module file parsing
- [ ] Routing manifest output is byte-identical to CSV-based output (verified by test)
- [ ] Mtime caching works for YAML files
- [ ] Error handling preserves structured logging (no bare `except: pass`)

#### 1.4 Update and add tests
- Update `test_extension_80.py` — replace CSV fixtures with YAML fixtures
- Update `test_core_csv_schema.py` → rename to `test_core_yaml_schema.py`, validate YAML schema
- Add `test_yaml_routing.py` — YAML parsing, phase filtering, menu lookup
- Add `test_migration_csv_to_yaml.py` — verify CSV→YAML data equivalence

**Acceptance criteria:**
- [ ] All existing routing tests pass with YAML
- [ ] New YAML-specific tests cover parsing, caching, error handling
- [ ] Test count ≥ 300

#### 1.5 Delete CSV files and clean up references
After YAML migration is verified:
- Delete all 5 `module-help.csv` files
- Remove any `module-help` references in SKILL.md, init script, tests
- Remove CSV-related test fixtures

**Acceptance criteria:**
- [ ] `grep -r 'module-help' . --include='*.py' --include='*.md' --include='*.sh'` returns zero results
- [ ] No `import csv` in routing extension

#### 1.6 Write ADR-0010 and supersede ADR-0001
Create `docs/adr/0010-yaml-canonical-routing.md`:
- Status: Accepted
- Decision: Use YAML as canonical routing format
- Rationale: Agent Zero can parse YAML natively; no need for CSV workaround
- Supersedes: ADR-0001

Update ADR-0001 header: `**Status:** Superseded by ADR-0010`

---

### Task Bundle 2: Agent Consolidation (P1 + A3)
**Priority:** P1 — structural alignment  
**Effort:** M (1 day)  
**Depends on:** Task Bundle 1 (YAML migration must be in progress or complete so module.yaml has correct routing)

#### 2.1 Remove bmad-sm agent directory
- Delete `agents/bmad-sm/` entirely
- Update `agents/bmad-dev/` (Amelia) customize.toml to include SM menus:
  - SP (Sprint Planning)
  - SS (Sprint Status)
  - CS (Create Story)
  - ER (Retrospective)
- Update `skills/bmad-bmm/module.yaml` — change `skill: sm` → `skill: dev` for SP, SS, CS, ER entries
- Update `agents/bmad-dev/prompts/agent.system.main.specifics.md` to reference SM workflows
- Update `bmad_status_core.py` AGENT_NAMES to remove `bmad-sm`

#### 2.2 Remove bmad-qa agent directory
- Delete `agents/bmad-qa/` entirely
- Update `agents/bmad-dev/` (Amelia) customize.toml to include QA menu:
  - QA (QA Automation Test)
- Update `skills/bmad-bmm/module.yaml` — change `skill: qa` → `skill: dev` for QA entry
- Update `bmad_status_core.py` AGENT_NAMES to remove `bmad-qa`
- This also resolves the 🧪 icon collision between Quinn and Murat

#### 2.3 Remove bmad-quick-dev agent directory
- Delete `agents/bmad-quick-dev/` entirely
- Update `agents/bmad-dev/` (Amelia) customize.toml to include QD menu:
  - QD (Quick Dev) — note the code change from QQ → QD
- Update `skills/bmad-bmm/module.yaml` — change Quick Dev entry:
  - `menu-code: QQ` → `menu-code: QD`
  - `skill: quick-flow-solo-dev` → `skill: dev`
- Verify Quick Spec (QS) is also accessible through Amelia
- Update `bmad_status_core.py` AGENT_NAMES to remove `bmad-quick-dev`

#### 2.4 Add missing menus to Amelia's customize.toml
Amelia's customize.toml should have a complete menu covering ALL implementation + quick-flow workflows:

```toml
[[agent.menu]]
code = "SP"
description = "Sprint Planning"
skill = "bmad-sprint-planning"

[[agent.menu]]
code = "SS"
description = "Sprint Status"
skill = "bmad-sprint-status"

[[agent.menu]]
code = "VS"
description = "Validate Story"
skill = "bmad-create-story"

[[agent.menu]]
code = "CS"
description = "Create Story"
skill = "bmad-create-story"

[[agent.menu]]
code = "DS"
description = "Dev Story"
skill = "bmad-dev-story"

[[agent.menu]]
code = "CR"
description = "Code Review"
skill = "bmad-code-review"

[[agent.menu]]
code = "QA"
description = "QA Automation Test"
skill = "bmad-qa-automate"

[[agent.menu]]
code = "CC"
description = "Correct Course"
skill = "bmad-correct-course"

[[agent.menu]]
code = "ER"
description = "Retrospective"
skill = "bmad-retrospective"

[[agent.menu]]
code = "CK"
description = "Checkpoint Review"
skill = "bmad-checkpoint-preview"

[[agent.menu]]
code = "QD"
description = "Quick Dev"
skill = "bmad-quick-dev"

[[agent.menu]]
code = "QS"
description = "Quick Spec"
skill = "bmad-quick-spec"
```

#### 2.5 Update bmad-master role.md
- Remove static 19-row agent table from `agents/bmad-master/prompts/agent.system.main.role.md`
- Replace with condensed routing guidance prose that references `{{agent_profiles}}` dynamic list
- Update agent count references (21 → 18 agents, or 17 non-master)

#### 2.6 Update agent roster in knowledge/config files
- Update any `teams/default-party.csv` references to remove bmad-sm, bmad-qa, bmad-quick-dev
- Update `skills/bmad-bmm/agents/sm.md` — this file should be removed or its content merged into `skills/bmad-bmm/agents/dev/` reference

**Acceptance criteria:**
- [ ] `ls agents/bmad-sm agents/bmad-qa agents/bmad-quick-dev` all fail with "No such file or directory"
- [ ] Amelia's customize.toml has SP, SS, VS, CS, DS, CR, QA, CC, ER, CK, QD, QS menus
- [ ] Quick Dev code is QD (not QQ) in module.yaml
- [ ] bmad-master role.md has no static agent table
- [ ] `bmad_status_core.py` AGENT_NAMES has no bmad-sm, bmad-qa, bmad-quick-dev
- [ ] All routing tests pass

---

### Task Bundle 3: CIS Persona Removal (A2)
**Priority:** P1 — upstream alignment  
**Effort:** S-M (0.5-1 day)  
**Depends on:** Nothing (can run in parallel with Bundle 1)

#### 3.1 Update CIS agent.yaml files
Replace named personas with upstream generic titles. For each CIS agent:

| Agent Directory | Current Title | Upstream Title | Current Icon | Upstream Icon |
|---|---|---|---|---|
| bmad-innovation | "BMAD Victor (Disruptive Innovation Oracle)" | "Innovation Strategist" | ⚡ | ⚡ (keep) |
| bmad-problem-solver | "BMAD Dr. Quinn (Master Problem Solver)" | "Creative Problem Solver" | 🔬 | 🔬 (keep) |
| bmad-design-thinking | "BMAD Maya (Design Thinking Maestro)" | "Design Thinking Coach" | 🎨 | 🎯 (was 🎨, collision with Sally) |
| bmad-brainstorming-coach | "BMAD Carson (Elite Brainstorming Specialist)" | "Brainstorming Coach" | 🧠 | 🧠 (keep) |
| bmad-storyteller | "BMAD Sophia (Master Storyteller)" | "Storyteller" | 📖 | 📖 (keep) |
| bmad-presentation | "BMAD Caravaggio (Visual Communication + Presentation Expert)" | "Presentation Master" | 🎨 | 🖼️ (was 🎨, collision with Sally) |

For each agent.yaml:
- Remove persona name from title (use generic title only)
- Remove persona-specific description paragraphs
- Replace with upstream-style functional description
- Update icon if it collided (Maya→🎯, Caravaggio→🖼️)

#### 3.2 Update CIS prompt files
For each of the 6 CIS agents, update their prompt files:
- `agent.system.main.role.md` — remove persona narrative, use functional description
- `agent.system.main.specifics.md` — remove persona name references, keep methodology
- `agent.system.main.communication_additions.md` — adjust style to generic (not persona-specific)

#### 3.3 Update CIS agent references in other files
- `skills/bmad-cis/agents/` — update agent reference .md files
- `skills/bmad-cis/module.yaml` — update skill/agent names if they reference personas
- `skills/bmad-cis/teams/` — update team rosters
- Knowledge files in `skills/bmad-init/seed-knowledge/` — update any persona references

**Acceptance criteria:**
- [ ] `grep -r 'Victor\|Dr\. Quinn\|Maya\|Carson\|Sophia\|Caravaggio' agents/bmad-*/` returns zero results
- [ ] All CIS agent.yaml titles match upstream generic titles
- [ ] Icon 🎨 is only used by Sally (bmad-ux-designer)
- [ ] bmad-design-thinking uses 🎯, bmad-presentation uses 🖼️
- [ ] CIS workflows still function correctly (menu codes IS, PS, DT, BS, ST, PR)

---

### Task Bundle 4: Quick Fixes (P1/P2/P3)
**Priority:** P1-P2  
**Effort:** S (2-4 hours)  
**Depends on:** Bundle 2 (agent consolidation) for icon conflict resolution

#### 4.1 Fix Morgan icon (🏗️ → 📦)
- Update `agents/bmad-module-builder/agent.yaml` — change icon to 📦
- Update `agents/bmad-module-builder/prompts/agent.system.main.role.md` if icon appears in text
- Verify no collision with Winston (🏗️ is now Winston-only)

#### 4.2 Fix Sally communication style (filmmaker metaphor)
- Update `agents/bmad-ux-designer/prompts/agent.system.main.role.md` — change from "painter" to "filmmaker pitching the scene"
- Upstream description: "Speaks like a filmmaker pitching the scene before the code exists, painting user stories that make you feel the problem"
- Update `agents/bmad-ux-designer/agent.yaml` description if needed

#### 4.3 Add US menu to Paige's customize.toml
- Add to `agents/bmad-tech-writer/customize.toml` or the appropriate customize location:
```toml
[[agent.menu]]
code = "US"
description = "Update Standards"
skill = "bmad-update-standards"
```
- Verify US workflow is accessible from Paige's menu

#### 4.4 Add _bmad/custom/ directory creation to init script
- Update `skills/bmad-init/scripts/bmad-init.sh` to add:
```bash
mkdir -p "${A0PROJ}/_bmad/custom/"
```
- This ensures the customization override directory exists from the start

#### 4.5 Address QA/VS menu code collisions (P2)
- **QA code:** Used in both BMM (QA Automation Test) and BMB (Quality Scan Agent)
- **VS code:** Used in both BMM (Validate Story) and BMB (Validate Skill)
- **Resolution:** Accept as module-scoped — each agent only sees its own module's codes through the routing manifest's phase/module filtering. Add a comment in module.yaml documenting the intentional duplication.
- **Verification:** Confirm routing manifest correctly filters by module when both modules are active

**Acceptance criteria:**
- [ ] Morgan icon is 📦 in agent.yaml
- [ ] Sally role.md uses "filmmaker" metaphor, not "painter"
- [ ] Paige's menu includes US code
- [ ] Init script creates `_bmad/custom/` directory
- [ ] Menu code collisions documented as intentional module-scoping

---

### Task Bundle 5: Test Updates and Final Verification
**Priority:** P1  
**Effort:** M (0.5-1 day)  
**Depends on:** All previous bundles

#### 5.1 Update existing tests for YAML
- `test_extension_80.py` — replace CSV test fixtures with YAML, update assertions
- `test_core_csv_schema.py` → `test_core_yaml_schema.py` — validate YAML schema instead
- `test_constants_consolidation.py` — update agent name lists
- `test_dead_code.py` — remove CSV-related dead code checks

#### 5.2 Add new tests
- `test_yaml_routing.py`:
  - YAML file parsing (valid YAML, invalid YAML, missing file)
  - Phase filtering with YAML data
  - Menu code lookup with YAML data
  - Mtime caching for YAML files
  - All 5 module.yaml files parse correctly

- `test_agent_consolidation.py`:
  - SM/QA/Quick-dev directories don't exist
  - Amelia has all expected menus
  - QD code (not QQ) in module.yaml
  - Routing manifest includes SM/QA/QD workflows under dev agent

- `test_cis_personas.py`:
  - No named personas in CIS agent.yaml files
  - Generic titles match upstream
  - No icon collisions (🎨 unique to Sally)

#### 5.3 Full integration test
- Run `bmad-init.sh` on temp directory
- Verify all directories created including `_bmad/custom/`
- Verify routing manifest generates correctly from YAML
- Verify phase transitions work
- Verify A2A live test on VPS

**Acceptance criteria:**
- [ ] `python -m pytest tests/ -v` — all tests pass, count ≥ 300
- [ ] `python -m flake8 api/ helpers/ extensions/ --max-line-length 100` — clean
- [ ] A2A live test passes


### Task Bundle 6: P3 Structural Alignment (8-Step Activation, Sidecar Memory, project-context.md)
**Priority:** P3 — structural alignment with upstream activation model  
**Effort:** L (4-6 days total: 2-3 days activation + 0.5-1 day project-context + 1-2 days sidecar)  
**Depends on:** Bundle 4 (init script must already create `_bmad/custom/`)

This bundle implements three interconnected P3 items identified in `docs/p3-implementation-research.md`. The 8-step activation sequence (Item 1) is the prerequisite — it unlocks persistent_facts processing (which solves Item 2) and provides the framework for sidecar memory loading (Item 3).

**Implementation order:** 6.1–6.4 (activation) → 6.5 (project-context) → 6.6–6.9 (sidecar) → 6.10 (tests)

**Design decision — Sidecar Memory (Option B):** The P3 research recommended A0 native memory with area scoping (Option A). After verification, we found FAISS filter is post-filter (not pre-filter), meaning per-agent sidecar entries (5-20 items) may not surface in top-k results. The user approved **Option B: file-based sidecar** instead:
- Match upstream exactly with `_bmad/_memory/*-sidecar/*.md` files
- Each agent gets its own directory: `_bmad/_memory/analyst-sidecar/`, `_bmad/_memory/pm-sidecar/`, etc.
- Content stored as human-readable markdown files (memories.md, instructions.md, etc.)
- Agents read/write sidecar files using `text_editor` or `code_execution_tool`
- More predictable than FAISS post-filter, human-readable, matches upstream
- Init script creates sidecar directories

#### 6.1 Rewrite bmad-agent-shared.md activation section (8-step sequence)
Replace the current 5-step activation sequence with the full upstream 8-step sequence.

**Current (5 steps):**
1. Review project state
2. Review project config
3. Greet as persona
4. Present menu
5. Wait for direction

**New (8 steps):**
1. **Resolve customization** — Run `resolve_customization.py` as first tool call, parse JSON output
2. **Execute prepend steps** — Process `activation_steps_prepend` array (default: empty)
3. **Review project state** — Use auto-injected project state from system prompt
4. **Review project config** — Use auto-injected config from system prompt
5. **Load persistent facts** — Process `persistent_facts` array; load `file:` references, adopt literal entries
6. **Greet as persona** — Introduce in character, prefix with resolved icon emoji
7. **Execute append steps** — Process `activation_steps_append` array (default: empty)
8. **Present menu or dispatch** — Use resolved menu merged with defaults; dispatch if intent is clear

The activation section in `prompts/bmad-agent-shared.md` must be rewritten to follow this exact sequence, with clear prompt instructions for each step.

**Acceptance criteria:**
- [ ] `bmad-agent-shared.md` activation section lists all 8 steps in order
- [ ] Steps 1, 2, 5, 7 are new (previously missing)
- [ ] Steps 3, 4, 6, 8 are preserved from current sequence
- [ ] Step numbering and descriptions match upstream documentation

#### 6.2 Add resolve_customization first-call instructions per agent
Each agent's activation must begin with a call to `resolve_customization.py`. Add template instructions to `bmad-agent-shared.md` that guide the agent to:

1. Determine its `{skill-root}` path from its agent directory
2. Execute: `python3 {project-root}/scripts/resolve_customization.py --skill {skill-root} --key agent`
3. Parse the JSON output for resolved values
4. Use resolved `agent.icon`, `agent.role`, `agent.communication_style`, `agent.principles`, `agent.menu` throughout the session

This makes the resolver the agent's first action, producing resolved values that inform all subsequent steps. It preserves upstream behavior where customization changes take effect on next activation without re-initialization.

**Acceptance criteria:**
- [ ] Shared prompt instructs agent to run resolve_customization.py as first tool call
- [ ] Template includes `{skill-root}` variable that resolves to each agent's directory
- [ ] Agent uses resolved icon, role, communication_style from JSON output
- [ ] Test: agent with custom override in `_bmad/custom/` picks up customized values

#### 6.3 Add persistent_facts processing instructions
After resolving customization, agents must process the `persistent_facts` array. Add instructions to `bmad-agent-shared.md`:

1. Extract `persistent_facts` from resolved customization JSON
2. For each entry:
   - If prefixed `file:`, resolve the path (replacing `{project-root}`) and read matching files
   - Glob patterns (`**/project-context.md`) should search for matching files
   - Otherwise, treat the entry as a literal fact
3. Carry all loaded facts as foundational context for the entire session

This automatically loads `project-context.md` since it's in the default `persistent_facts` array in all agent customize.toml files.

**Acceptance criteria:**
- [ ] Shared prompt includes step for processing `persistent_facts` array
- [ ] `file:` prefix handling documented with glob pattern support
- [ ] Literal facts (non-file entries) are adopted as context
- [ ] Default `persistent_facts` from customize.toml are processed (including project-context.md)

#### 6.4 Add prepend/append hooks processing instructions
Add instructions for processing `activation_steps_prepend` and `activation_steps_append` arrays:

- **Prepend steps** execute BEFORE persona adoption — used for compliance checks, context loading
- **Append steps** execute AFTER greeting but BEFORE menu presentation — used for heavy setup
- Both default to empty arrays in all customize.toml files
- The mechanism must exist even if defaults are empty (for user customization)

For each entry in these arrays:
- If it's a file reference, load and process it
- If it's an instruction, execute it

**Acceptance criteria:**
- [ ] Prepend step processing occurs before persona adoption (step 2 in sequence)
- [ ] Append step processing occurs after greeting, before menu (step 7 in sequence)
- [ ] Empty arrays result in no-op (correct behavior)
- [ ] Custom override with prepend/append entries is processed correctly

#### 6.5 Standardize project-context.md loading in implementation workflows
While Item 3 (activation sequence) handles project-context.md via persistent_facts, add a safety net in implementation workflow step files. For each implementation workflow that references `project-context`:

| Workflow | File to Update |
|---|---|
| dev-story | `workflows/dev-story/steps/step-01-init.md` |
| create-story | `workflows/create-story/steps/step-01-init.md` |
| code-review | `workflows/code-review/steps/step-01-init.md` |
| sprint-planning | `workflows/sprint-planning/steps/step-01-init.md` |
| correct-course | `workflows/correct-course/steps/step-01-init.md` |
| quick-dev | `workflows/quick-dev/steps/step-01-init.md` |
| quick-spec | `workflows/quick-spec/steps/step-01-init.md` |
| create-architecture | `workflows/create-architecture/steps/step-01-init.md` |

Add to each step file:
```markdown
## Pre-step: Project Context
Before starting, check for `{output_folder}/project-context.md`.
If it exists, read it and apply its conventions throughout this workflow.
```

**Acceptance criteria:**
- [ ] All 8 implementation workflow step-01 files include project-context.md pre-step
- [ ] Pre-step is idempotent (safe even if project-context.md doesn't exist)
- [ ] project-context.md conventions applied throughout workflow execution

#### 6.6 Add file-based sidecar memory directories to init script
Update `skills/bmad-init/scripts/bmad-init.sh` to create sidecar directories for all agents:

```bash
# Create sidecar memory directories for all agents
for agent in analyst pm architect dev ux-designer tech-writer module-builder \
             agent-builder workflow-builder test-architect innovation \
             problem-solver design-thinking brainstorming-coach \
             storyteller presentation; do
    mkdir -p "${BMM_OUTPUT}/_memory/${agent}-sidecar"
    # Create initial memories.md if it doesn't exist
    touch "${BMM_OUTPUT}/_memory/${agent}-sidecar/memories.md"
done
```

Note: Sidecar directories live under `_bmad/_memory/` (not `_bmad-output/`), matching upstream.

**Acceptance criteria:**
- [ ] Init script creates `_bmad/_memory/` directory
- [ ] All 16 non-master agent sidecar directories created
- [ ] Each sidecar directory has a `memories.md` file (empty or template)
- [ ] Init script idempotent (safe to re-run)

#### 6.7 Add sidecar loading to activation sequence
Extend the 8-step activation sequence (from 6.1) to load sidecar files during activation. Add a sub-step between persistent facts (step 5) and greeting (step 6):

```markdown
### Step 5.5: Load Sidecar Memory

Read your agent's sidecar memory directory: `_bmad/_memory/{your-agent-name}-sidecar/`
Load all .md files in this directory as persistent context for this session.
- `memories.md` — running memory of past decisions and preferences
- `instructions.md` — agent-specific behavioral instructions (if exists)
- Any other .md files — load as additional context
```

The agent determines its sidecar directory from its agent profile name.

**Acceptance criteria:**
- [ ] Shared prompt includes sidecar loading instruction between facts and greeting
- [ ] Agent reads all .md files from its sidecar directory
- [ ] Missing sidecar files are handled gracefully (no error, skip)
- [ ] Sidecar content carried as context for entire session

#### 6.8 Add sidecar writing instructions to agent prompts
Add instructions to `bmad-agent-shared.md` for writing to sidecar at natural breakpoints:

```markdown
## Sidecar Memory Writing

At natural breakpoints during your session, save important context to your sidecar memory:

- **End of workflow execution** — write key decisions and outcomes to `memories.md`
- **User preference discovered** — append to `memories.md`
- **Important architectural decision** — append to `memories.md`
- **Behavioral instruction learned** — append to `instructions.md`

Use `text_editor` to append to your sidecar files:
- Path: `_bmad/_memory/{your-agent-name}-sidecar/memories.md`
- Format: `### [Date] - [Topic]\n[Content]\n`
- Keep entries concise and focused on reusable knowledge
```

**Acceptance criteria:**
- [ ] Shared prompt includes sidecar writing instructions
- [ ] Writing triggers defined at natural breakpoints
- [ ] File format documented (markdown with date/topic headers)
- [ ] Agents append (not overwrite) to preserve existing memories

#### 6.9 Create sidecar import skill for upstream migration
Create a new skill `skills/bmad-sidecar-import/` for users migrating from upstream BMAD who have existing `_bmad/_memory/*-sidecar/` content:

- `SKILL.md` — skill description and usage instructions
- `scripts/import-sidecars.sh` — copies sidecar files from upstream location to A0-compatible location
- The skill reads upstream sidecar markdown files and copies them to the correct A0 paths

This is a one-time migration tool for users coming from IDE-based BMAD installations.

**Acceptance criteria:**
- [ ] `skills/bmad-sidecar-import/SKILL.md` exists with usage instructions
- [ ] Import script copies `.md` files from upstream sidecar directories
- [ ] Import is idempotent (safe to run multiple times)
- [ ] Imported content is readable by A0 agents on next activation

#### 6.10 Add tests for activation sequence, sidecar, project-context loading
Add comprehensive tests for all P3 structural changes:

- `test_activation_sequence.py`:
  - Verify bmad-agent-shared.md lists all 8 activation steps
  - Verify resolve_customization.py is referenced as first tool call
  - Verify persistent_facts processing instructions exist
  - Verify prepend/append hook instructions exist
  - Verify sidecar loading instructions exist between facts and greeting

- `test_sidecar_memory.py`:
  - Init script creates all 16 sidecar directories
  - Each directory has `memories.md`
  - Sidecar files are readable markdown
  - Agent prompts reference sidecar paths correctly

- `test_project_context_loading.py`:
  - Shared prompt includes persistent_facts processing step
  - Implementation workflow step-01 files include project-context pre-step
  - customize.toml files reference project-context.md in persistent_facts

**Acceptance criteria:**
- [ ] All new test files pass
- [ ] Test count ≥ 310 (previous 300+ + 10+ new P3 tests)
- [ ] Tests verify end-to-end activation with customization resolution

**Bundle 6 overall acceptance criteria:**
- [ ] Agent activation follows full 8-step upstream sequence
- [ ] resolve_customization.py produces merged values used throughout session
- [ ] persistent_facts (including project-context.md) loaded automatically
- [ ] Prepend/append hooks processed at correct points
- [ ] Sidecar memory directories exist for all 16 agents
- [ ] Agents read sidecar on activation, write at natural breakpoints
- [ ] Implementation workflows explicitly check project-context.md
- [ ] All existing tests continue to pass

---

## Migration Guide: CSV → YAML

### Why This Migration

**Original decision (ADR-0001):** CSV was chosen because upstream BMAD-METHOD IDE integrations parse CSV directly, and CSV felt like a safe, human-readable format.

**Why it's changing:** Agent Zero can parse YAML natively. The upstream `module.yaml` format is YAML. Maintaining a separate CSV format creates a divergence that must be manually synced. YAML is the upstream canonical format and A0 can use it directly.

### Data Mapping: CSV Columns → YAML Fields

| CSV Column | YAML Field | Notes |
|---|---|---|
| `module` | `module` | Module code (bmm, tea, cis, bmb) |
| `skill` | `skill` | Agent skill reference |
| `display-name` | `display-name` | Human-readable workflow name |
| `menu-code` | `menu-code` | Short code for menu selection |
| `description` | `description` | Workflow description |
| `action` | `action` | Skill name to load |
| `args` | `args` | Path to workflow file |
| `phase` | `phase` | Phase assignment |
| `after` | `after` | Post-workflow action (empty in most rows) |
| `before` | `before` | Pre-workflow action (empty in most rows) |
| `required` | `required` | Boolean, whether artifact is required |
| `output-location` | `output-location` | Artifact output location alias |
| `outputs` | `outputs` | Expected output file pattern |

### Conversion Process

1. **Automated conversion:** Run `scripts/archive/csv_to_yaml_converter.py` — reads each CSV, outputs YAML
2. **Manual verification:** Diff CSV row count against YAML entry count for each module
3. **Routing test:** Run routing extension with YAML, compare output to CSV-based output
4. **Delete CSVs:** After verification, remove all module-help.csv files

### Breaking Changes

- **Routing extension API:** Internal only — `_collect_routing_rows()` changes from CSV to YAML. No external API change.
- **Routing manifest format:** UNCHANGED — the text block injected into extras_temporary is identical
- **Dashboard:** UNCHANGED — reads from routing manifest, not directly from CSV/YAML
- **CLI status:** UNCHANGED — reads from state file and routing manifest

### Rollback Plan

If YAML migration causes issues:
1. Restore module-help.csv files from git history
2. Revert routing extension to CSV parsing
3. YAML files can coexist with CSV during transition

---

## Dependency Order

```
Bundle 1 (CSV→YAML) ─────────┐
                               ├──→ Bundle 5 (Test Updates P1/P2)
Bundle 2 (Agent Consolidation) ┤                    │
                               │                    │
Bundle 3 (CIS Personas) ───────┤                    │
                               │                    ▼
Bundle 4 (Quick Fixes) ────────┘          Bundle 6 (P3 Structural)
                                                │
                                                ▼
                                       Bundle 6 Tests (6.10)
```

- **Bundle 1 and 3** can run in parallel (independent changes)
- **Bundle 2** should wait for Bundle 1 (module.yaml needs correct skill assignments)
- **Bundle 4** can partially overlap with Bundle 2 (Morgan icon fix is independent)
- **Bundle 5** runs after Bundles 1-4 are in place
- **Bundle 6** runs after Bundle 4 (needs init script's `_bmad/custom/` creation) and Bundle 5 (P1/P2 tests must pass first)
- **Bundle 6 tests (6.10)** run last to verify all P3 structural changes

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| YAML parsing regression in routing | Low | High | Automated equivalence test: YAML output == CSV output |
| Missing workflows after consolidation | Low | High | Test all 79+ workflow codes resolve correctly |
| CIS persona removal breaks user expectations | Low | Medium | Generic titles still functional; A0 handles routing |
| Init script _bmad/custom/ causes permission issue | Very Low | Low | Uses `mkdir -p`, same as other directory creation |
| PyYAML not available in A0 container | Very Low | High | Verify PyYAML is installed; add to requirements if needed |
| 8-step activation confuses existing agents | Medium | Medium | Activation is prompt-based; test each agent's first response |
| resolve_customization.py fails at activation | Low | High | Graceful fallback: agent proceeds with hardcoded customize.toml defaults |
| Sidecar files grow unbounded over time | Medium | Low | Markdown is lightweight; agents append concisely; manual cleanup possible |
| File-based sidecar not loaded (missing dir) | Low | Medium | Init script creates dirs; activation handles missing files gracefully |
| project-context.md stale after codebase changes | Medium | Low | GPC workflow regenerates it; workflows warn if stale |

---

## Upstream Reference

### BMM Agent Roster (from upstream module.yaml)

| Code | Name | Title | Icon |
|---|---|---|---|
| bmad-agent-analyst | Mary | Business Analyst | 📊 |
| bmad-agent-tech-writer | Paige | Technical Writer | 📚 |
| bmad-agent-pm | John | Product Manager | 📋 |
| bmad-agent-ux-designer | Sally | UX Designer | 🎨 |
| bmad-agent-architect | Winston | System Architect | 🏗️ |
| bmad-agent-dev | Amelia | Senior Software Engineer | 💻 |

### CIS Agent Upstream Titles

| Code | Title | Menu Code |
|---|---|---|
| bmad-innovation | Innovation Strategist | IS |
| bmad-problem-solver | Creative Problem Solver | PS |
| bmad-design-thinking | Design Thinking Coach | DT |
| bmad-brainstorming-coach | Brainstorming Coach | BS |
| bmad-storyteller | Storyteller | ST |
| bmad-presentation | Presentation Master | PR |

### BMB Agent Roster

| Code | Name | Title | Icon |
|---|---|---|---|
| bmad-agent-builder | Bond | Agent Builder | 🤖 |
| bmad-workflow-builder | Wendy | Workflow Builder | 🔄 |
| bmad-module-builder | Morgan | Module Builder | 📦 |

---

*End of alignment fix spec. All changes grounded in bmad-alignment-audit.md (485 lines), alignment-analysis.md (782 lines), bmad-method-research.md (1,012 lines), docs-website-research.md (1,527 lines), and direct file inspection. Source material analyzed: ~3,800+ lines.*
