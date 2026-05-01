# Implementation Plan: BMAD Method Plugin — Phase F (Upstream v6.6.0 Sync)

## Overview

Sync the BMAD Method A0 plugin (v1.0.8) with upstream BMAD-METHOD v6.6.0, incorporating critical workflow step improvements, config migration, and evaluating new upstream features for A0 compatibility. This phase targets 12 tasks across 3 priority tiers.

**Prereq:** Phases A–D COMPLETE (35 tasks, 200 tests, 49 commits).
**Upstream:** `88b9a1c` → `9debc16` (v6.6.0, 37 files changed, 3422 insertions, 312 deletions).
**Branch:** `develop` → `main` on /ship.
**Test command:** `cd /a0/usr/projects/a0_bmad_method && python -m pytest tests/ -v`

---

## Architecture Decisions

- **5-step merge protocol for all P0 workflow step syncs:** (1) Read our file fully, (2) Identify all A0-specific sections, (3) Merge upstream content around them, (4) Verify A0 sections intact, (5) Run full test suite. Never overwrite A0 additions.
- **A0-specific sections to preserve in all 3 workflow steps:** YAML frontmatter (step-02, step-04), Step Complete sections, Workflow Completion — State Write section (step-04).
- **Config migration is atomic:** `project_name` moves from bmm → core in one commit; version bumps applied to all 5 config files simultaneously.
- **Plugin version bump to 1.1.0:** Feature addition from upstream sync warrants minor version bump (not patch).
- **`bmad-customize` skill to be ported from upstream:** Decision: CREATE — port upstream core skill with A0 path adaptations. Uses `resolve_customization.py` for 3-layer TOML merge customization.
- **`resolve_customization.py` included in plugin:** Upstream script at `src/scripts/resolve_customization.py` is a Python 3.11+ script (we have 3.13) that does 3-layer TOML merge for skill customization. Include at `$A0PROJ/_bmad/scripts/` with A0 path conventions.

---

## Dependency Graph

```
[F-P0-1: step-07 validation fix]     ← independent
[F-P0-2: step-02 design epics fix]   ← independent
[F-P0-3: step-04 final validation]    ← independent
         │
         ▼
[CHECKPOINT P0 — all 3 synced, tests green]
         │
         ▼
[F-P1-1: project_name → core config] ─── [F-P1-2: remove project_name from bmm]
         │                                      │
         ▼                                      ▼
[F-P1-3: update config versions to 6.6.0] ← depends on F-P1-1 + F-P1-2
         │
         ▼
[F-P1-4: verify CSV row coverage]     ← depends on F-P1-3
[F-P1-5: include resolve_customization.py] ← independent
         │
         ▼
[F-P1-6: create bmad-customize skill]  ← depends on F-P1-5
         │
         ▼
[CHECKPOINT P1 — config migrated, customization in place]
    ┌────┴──────────────────────────┐
    │ F-P2-1: update CHANGELOG      │
    │ F-P2-2: version bump 1.1.0    │
    └──────────────┬────────────────┘
                   │
          [CHECKPOINT P2 — ready for /ship]
```

**Parallelization:**
- F-P0-1, F-P0-2, F-P0-3 can run in parallel (different files)
- F-P1-1 and F-P1-2 can run in parallel (different files)
- F-P1-4 and F-P1-5 can run in parallel (independent)
- F-P2-1, F-P2-2 can run in parallel (different files)

---

## 5-Step Merge Protocol (applies to all P0 tasks)

All P0 tasks involve merging upstream v6.6.0 content into our workflow step files while preserving A0-specific additions.

1. **Read our file fully** — Load the complete file content; note all sections, structure, and line numbers
2. **Identify A0-specific sections** — Mark YAML frontmatter blocks, Step Complete sections, State Write sections, any A0-only content not present in upstream
3. **Merge upstream content** — Apply upstream v6.6.0 changes (new sections, modified text, restructured checklists) while keeping A0-specific sections in their correct positions
4. **Verify A0 sections intact** — Diff check that all A0-specific sections survive the merge unchanged
5. **Run test suite** — `python -m pytest tests/ -v` must pass with zero failures

**Upstream source files** (for diff reference):
- step-07: `.a0proj/upstream/BMAD-METHOD/src/bmm-skills/3-solutioning/bmad-create-architecture/steps/step-07-validation.md`
- step-02: `.a0proj/upstream/BMAD-METHOD/src/bmm-skills/3-solutioning/bmad-create-epics-and-stories/steps/step-02-design-epics.md`
- step-04: `.a0proj/upstream/BMAD-METHOD/src/bmm-skills/3-solutioning/bmad-create-epics-and-stories/steps/step-04-final-validation.md`

---

## Phase F — P0: Critical Workflow Step Sync (3 tasks)

**Gate: All P0 tasks must pass before any P1 work begins.**

---

### Task F-P0-1: Fix pre-checked architecture checklist in step-07-validation.md [Size: M]

**SPEC ref:** F-P0-1

**Description:** The architecture validation checklist in `step-07-validation.md` currently has all items pre-checked `[x]` with hard-coded `READY FOR IMPLEMENTATION` status. Upstream v6.6.0 changed all items to unchecked `[ ]` with conditional 3-tier status logic. This is a critical quality improvement — the checklist is meaningless if every item is pre-checked.

**Changes required:**
1. Change all checklist items from `[x]` to `[ ]` (unchecked)
2. Remove ✅ emoji from section headers (e.g., `**✅ Requirements Analysis**` → `**Requirements Analysis**`)
3. Add instruction: "Mark each item `[x]` only if validation confirms it; leave `[ ]` if missing, partial, or unverified."
4. Replace hard-coded `Overall Status: READY FOR IMPLEMENTATION` with conditional 3-tier logic:
   - `READY FOR IMPLEMENTATION` — all 16 items `[x]`, no Critical Gaps
   - `READY WITH MINOR GAPS` — some items unchecked but no Critical Gaps open
   - `NOT READY` — any Critical Gap open or any Requirements Analysis / Architectural Decisions item unchecked
5. Add "Architecture Readiness Assessment" section with the conditional rules
6. **Preserve our Step Complete section** at bottom of file (A0-specific, not in upstream)

**Files affected:**
- `skills/bmad-bmm/workflows/3-solutioning/create-architecture/steps/step-07-validation.md`

**Upstream reference:** `.a0proj/upstream/BMAD-METHOD/src/bmm-skills/3-solutioning/bmad-create-architecture/steps/step-07-validation.md` (361 lines)

**Dependencies:** None

**Verification steps:**
- [ ] All checklist items are `[ ]` (unchecked)
- [ ] No ✅ emoji in any section header
- [ ] Overall Status has 3-tier conditional instruction
- [ ] Step Complete section preserved at file bottom
- [ ] `python -m pytest tests/ -v` — all green

**Risk notes:** Our file (366 lines) vs upstream (361 lines) — 5 extra lines likely from Step Complete section. Low risk merge. No YAML frontmatter in our version to preserve.

**Estimated complexity:** Medium — multiple checklist changes + new conditional section, but straightforward search-and-replace pattern

---

### Task F-P0-2: Add file churn detection to epic design in step-02-design-epics.md [Size: M]

**SPEC ref:** F-P0-2

**Description:** Upstream v6.6.0 added Implementation Efficiency principle (#6), renamed Step A to include brownfield context assessment, updated Step B to consider file overlap, added new Step C (Review for File Overlap), and added wrong/correct file churn examples. These changes significantly improve epic design quality by detecting when multiple epics target the same core files.

**Changes required:**
1. Add Principle #6: "Implementation Efficiency" — consider consolidating epics that modify the same core files
2. Add wrong/correct file churn examples after principles (❌ WRONG: 3 epics touching same model/controller/web; ✅ CORRECT: single consolidated epic)
3. Rename Step A from "Identify User Value Themes" to "Assess Context and Identify Themes" — add brownfield context assessment paragraph
4. Update Step B instruction to include "considering whether epics share the same core files"
5. Add new Step C: "Review for File Overlap" — detect when multiple epics target same core files, recommend consolidation
6. **Preserve our YAML frontmatter** at top of file
7. **Preserve our Step Complete section** at bottom of file

**Files affected:**
- `skills/bmad-bmm/workflows/3-solutioning/create-epics-and-stories/steps/step-02-design-epics.md`

**Upstream reference:** `.a0proj/upstream/BMAD-METHOD/src/bmm-skills/3-solutioning/bmad-create-epics-and-stories/steps/step-02-design-epics.md` (242 lines)

**Dependencies:** None

**Verification steps:**
- [ ] 6 principles present (including #6 Implementation Efficiency)
- [ ] Wrong/correct file churn examples present
- [ ] Step A renamed to "Assess Context and Identify Themes" with brownfield paragraph
- [ ] Step B mentions file overlap consideration
- [ ] Step C (Review for File Overlap) exists
- [ ] YAML frontmatter preserved at file top
- [ ] Step Complete section preserved at file bottom
- [ ] `python -m pytest tests/ -v` — all green

**Risk notes:** Our file (233 lines) vs upstream (242 lines) — upstream has +9 lines (new content). Our file has YAML frontmatter that upstream may not. Medium merge complexity due to structural changes (new Step C shifts numbering).

**Estimated complexity:** Medium — structural changes to step flow + new content sections + two preserved A0 sections

---

### Task F-P0-3: Add file churn check + HALT + on_complete hook in step-04-final-validation.md [Size: M]

**SPEC ref:** F-P0-3

**Description:** Upstream v6.6.0 added three changes to the final validation step: (1) File Churn Check subsection in Epic Structure Validation, (2) HALT instruction in Final Menu, (3) On Complete hook running `resolve_customization.py`. These changes improve validation rigor and add workflow completion extensibility.

**Changes required:**
1. Add File Churn Check subsection to Epic Structure Validation:
   - "Do multiple epics repeatedly modify the same core files?"
   - Assess overlap pattern: unnecessary churn vs incidental
   - If significant: validate splitting provides genuine value
   - If no justification: recommend consolidation
   - Wrong example: multiple epics each modifying same files with no feedback loop
   - Right example: distinct files/components, or consolidation explicitly considered
2. Add HALT instruction to Final Menu:
   - `HALT — wait for user input before proceeding.`
3. Add On Complete section:
   - `Run: python3 $A0PROJ/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow.on_complete`
   - If resolved `workflow.on_complete` is non-empty, follow it as final terminal instruction
   - Note: `resolve_customization.py` is included in F-P1-5
4. **Preserve our Workflow Completion — State Write section** (A0-specific, not in upstream)
5. **Preserve our YAML frontmatter** at top of file

**Files affected:**
- `skills/bmad-bmm/workflows/3-solutioning/create-epics-and-stories/steps/step-04-final-validation.md`

**Upstream reference:** `.a0proj/upstream/BMAD-METHOD/src/bmm-skills/3-solutioning/bmad-create-epics-and-stories/steps/step-04-final-validation.md` (143 lines)

**Dependencies:** None (On Complete hook references `resolve_customization.py` which will be included in F-P1-5, but the step file can reference it before it exists)

**Verification steps:**
- [ ] File Churn Check subsection exists in Epic Structure Validation
- [ ] HALT instruction present in Final Menu
- [ ] On Complete hook section present with resolve_customization.py reference
- [ ] Workflow Completion — State Write section preserved
- [ ] YAML frontmatter preserved at file top
- [ ] `python -m pytest tests/ -v` — all green

**Risk notes:** Our file (167 lines) vs upstream (143 lines) — our +24 lines are the State Write section. On Complete hook path adapted from upstream's `{project-root}/_bmad/scripts/` to A0's `$A0PROJ/_bmad/scripts/`.

**Estimated complexity:** Medium — multiple additions + one preserved A0 section

---

## Checkpoint: P0

**Pass criteria (ALL must be green before P1 starts):**
- [ ] `step-07-validation.md` — all `[ ]` unchecked, no ✅ emoji, 3-tier conditional status
- [ ] `step-02-design-epics.md` — 6 principles, Step C exists, file churn examples
- [ ] `step-04-final-validation.md` — File Churn Check, HALT, On Complete hook
- [ ] All 3 files retain their A0-specific sections (YAML frontmatter, Step Complete, State Write)
- [ ] `python -m pytest tests/ -v` → all 200+ tests green

---

## Phase F — P1: Config Migration + Customization (6 tasks)

**Prereq:** P0 checkpoint passed.

---

### Task F-P1-1: Move `project_name` to core config [Size: XS]

**SPEC ref:** F-P1-1

**Description:** `project_name` currently lives in `skills/bmad-bmm/config.yaml` but upstream v6.6.0 moved it to the core config as it's a project-level value, not BMM-specific. Add `project_name` field to `skills/bmad-init/core/config.yaml` and update the version header from `6.0.3` to `6.6.0`.

**Changes required:**
1. Add `project_name: ""` to `skills/bmad-init/core/config.yaml`
2. Update version comment from `6.0.3` to `6.6.0`

**Current core config state:**
~~~yaml
# CORE Module Configuration
# Version: 6.0.3

user_name: ""
communication_language: English
document_output_language: English
output_folder: "{project-root}/_bmad-output"
~~~

**Target state:**
~~~yaml
# CORE Module Configuration
# Version: 6.6.0

project_name: ""
user_name: ""
communication_language: English
document_output_language: English
output_folder: "{project-root}/_bmad-output"
~~~

**Files affected:**
- `skills/bmad-init/core/config.yaml`

**Dependencies:** None

**Verification steps:**
- [ ] `grep 'project_name' skills/bmad-init/core/config.yaml` → found
- [ ] `grep 'Version: 6.6.0' skills/bmad-init/core/config.yaml` → found

**Risk notes:** Low risk. `project_name` may be referenced by CSV routing rows or workflow templates — verify in F-P1-4.

**Estimated complexity:** Small — add one field, change version string

---

### Task F-P1-2: Remove `project_name` from bmm config [Size: XS]

**SPEC ref:** F-P1-2

**Description:** Remove `project_name` from `skills/bmad-bmm/config.yaml` now that it lives in core config. Update version header from `6.0.3` to `6.6.0`.

**Changes required:**
1. Remove `project_name: ""` line from `skills/bmad-bmm/config.yaml`
2. Update version comment from `6.0.3` to `6.6.0`

**Current bmm config state:**
~~~yaml
# BMM Module Configuration
# Version: 6.0.3

project_name: ""
user_skill_level: intermediate
...
~~~

**Target state:**
~~~yaml
# BMM Module Configuration
# Version: 6.6.0

user_skill_level: intermediate
...
~~~

**Files affected:**
- `skills/bmad-bmm/config.yaml`

**Dependencies:** F-P1-1 (project_name must exist in core config before removing from bmm)

**Verification steps:**
- [ ] `grep 'project_name' skills/bmad-bmm/config.yaml` → empty
- [ ] `grep 'Version: 6.6.0' skills/bmad-bmm/config.yaml` → found
- [ ] `python -m pytest tests/ -v` — all green

**Risk notes:** Any code or workflow that reads `project_name` from bmm config will break. Need to verify all consumers in F-P1-4.

**Estimated complexity:** Small — remove one line, change version string

---

### Task F-P1-3: Update remaining config versions to 6.6.0 [Size: XS]

**SPEC ref:** F-P1-3

**Description:** Update version headers in the 3 remaining config files from `6.0.3` to `6.6.0`. No content changes needed — these files don't have `project_name`.

**Changes required:**
1. `skills/bmad-cis/config.yaml` — change `Version: 6.0.3` to `Version: 6.6.0`
2. `skills/bmad-tea/config.yaml` — change `Version: 6.0.3` to `Version: 6.6.0`
3. `skills/bmad-bmb/config.yaml` — change `Version: 6.0.3` to `Version: 6.6.0`

**Files affected:**
- `skills/bmad-cis/config.yaml`
- `skills/bmad-tea/config.yaml`
- `skills/bmad-bmb/config.yaml`

**Dependencies:** F-P1-1, F-P1-2 (config migration should be atomic)

**Verification steps:**
- [ ] `grep -r 'Version: 6.0.3' skills/*/config.yaml` → empty
- [ ] `grep -r 'Version: 6.6.0' skills/*/config.yaml` → 5 hits (all 5 configs)
- [ ] `python -m pytest tests/ -v` — all green

**Risk notes:** Minimal — version string change only, no functional impact.

**Estimated complexity:** Small — version string update in 3 files

---

### Task F-P1-4: Verify CSV row coverage post-migration [Size: S]

**SPEC ref:** F-P1-4

**Description:** After moving `project_name` from bmm to core config, verify that all 5 `module-help.csv` files still route correctly. Verified upstream: no CSV rows reference `project_name` at all, so this is a quick sanity check confirming the migration is safe.

**Changes required:** None (verification-only task, but may require fixes if issues found)

**Verification steps:**
- [ ] `grep -r 'project_name' skills/*/module-help.csv` — confirm no CSV references project_name
- [ ] `python -m pytest tests/test_extension_80.py -v` — routing tests pass
- [ ] `python -m pytest tests/test_core_csv_schema.py -v` — CSV schema tests pass
- [ ] Manual: load a bmm workflow via routing manifest and verify config resolution

**Files affected:**
- Potentially any `module-help.csv` if references need updating (unlikely)

**Dependencies:** F-P1-3 (all config changes complete)

**Risk notes:** Low risk — verified upstream that no CSV rows reference `project_name`. Config migration is safe.

**Estimated complexity:** Small — quick sanity check, no longer a blocker

---

### Task F-P1-5: Include `resolve_customization.py` in plugin [Size: S]

**SPEC ref:** F-P1-5

**Description:** Upstream's `resolve_customization.py` is a Python 3.11+ script (we have 3.13) that performs 3-layer TOML merge for skill customization. Include it in our plugin, adapting paths from upstream's `{project-root}/_bmad/` to A0's `$A0PROJ/_bmad/` conventions.

**Changes required:**
1. Copy `src/scripts/resolve_customization.py` from upstream to `$A0PROJ/_bmad/scripts/resolve_customization.py`
2. Adapt all path references from `{project-root}/_bmad/` to `$A0PROJ/_bmad/`
3. Verify script runs with our Python 3.13 environment
4. Add any missing dependencies (e.g., `tomllib` or `tomli` for TOML parsing)

**Files affected:**
- NEW: `$A0PROJ/_bmad/scripts/resolve_customization.py` (adapted from upstream)

**Upstream reference:** `.a0proj/upstream/BMAD-METHOD/src/scripts/resolve_customization.py`

**Dependencies:** None (can run in parallel with F-P1-4)

**Verification steps:**
- [ ] Script exists at `$A0PROJ/_bmad/scripts/resolve_customization.py`
- [ ] `python3 $A0PROJ/_bmad/scripts/resolve_customization.py --help` runs without error
- [ ] All path references adapted from upstream format to A0 format
- [ ] `python -m pytest tests/ -v` — all green

**Risk notes:** Low risk — straightforward port with path adaptation. Python 3.13 has `tomllib` built-in for TOML reading (3.11+ feature).

**Estimated complexity:** Small — copy + path adaptation

---

### Task F-P1-6: Create bmad-customize skill [Size: M]

**SPEC ref:** F-P1-6

**Description:** Port the upstream `bmad-customize` core skill to our plugin with A0 path adaptations. This skill enables project-level customization (adjusting agent personas, workflow parameters, etc.) using the `resolve_customization.py` script for 3-layer TOML merge.

**Changes required:**
1. Port upstream SKILL.md with A0 path adaptations:
   - `src/core-skills/bmad-customize/SKILL.md` → adapt with A0 paths
2. Port supporting scripts:
   - `src/core-skills/bmad-customize/scripts/list_customizable_skills.py`
   - `src/core-skills/bmad-customize/scripts/tests/test_list_customizable_skills.py`
3. Port `customize.toml` files from bmm skills (31 files found upstream)
4. Adapt all path references from upstream conventions to A0 conventions

**Files affected:**
- NEW: Skill directory with SKILL.md, scripts, and customize.toml files

**Upstream references:**
- `.a0proj/upstream/BMAD-METHOD/src/core-skills/bmad-customize/SKILL.md`
- `.a0proj/upstream/BMAD-METHOD/src/core-skills/bmad-customize/scripts/list_customizable_skills.py`
- `.a0proj/upstream/BMAD-METHOD/src/core-skills/bmad-customize/scripts/tests/test_list_customizable_skills.py`
- 31 `customize.toml` files across bmm skills

**Dependencies:** F-P1-5 (resolve_customization.py must be in place for the skill to function)

**Verification steps:**
- [ ] bmad-customize skill loads via SKILL.md
- [ ] `list_customizable_skills.py` runs and discovers customizable skills
- [ ] Test for `list_customizable_skills.py` passes
- [ ] All customize.toml files ported and valid TOML
- [ ] All path references adapted to A0 conventions
- [ ] `python -m pytest tests/ -v` — all green

**Risk notes:** Medium complexity — 31 customize.toml files to port, but they're likely simple config files. The SKILL.md needs careful path adaptation. Test file needs to work in A0's test environment.

**Estimated complexity:** Medium — multiple files to port with path adaptations

---

## Checkpoint: P1

**Pass criteria:**
- [ ] `project_name` in core config only (not duplicated in bmm)
- [ ] All 5 config.yaml version headers read `6.6.0`
- [ ] CSV row routing unaffected by config migration
- [ ] `resolve_customization.py` included at `$A0PROJ/_bmad/scripts/`
- [ ] `bmad-customize` skill created with all supporting files
- [ ] `python -m pytest tests/ -v` → all 200+ tests green

---

## Phase F — P2: Polish (2 tasks)

**Prereq:** P1 checkpoint passed.

---

### Task F-P2-1: Update CHANGELOG [Size: XS]

**SPEC ref:** F-P2-1

**Description:** Add Phase F entries to CHANGELOG.md documenting all changes from the upstream v6.6.0 sync.

**Changes required:**
Add new section at top of CHANGELOG:

~~~markdown
## [1.1.0] — 2026-05-XX

### Phase F — Upstream v6.6.0 Sync

#### P0 — Critical Workflow Step Sync
- **F-P0-1**: Architecture validation checklist unchecked with 3-tier conditional status
- **F-P0-2**: File churn detection in epic design (Principle #6, Step C, examples)
- **F-P0-3**: File churn validation + HALT instruction + on_complete hook in final validation

#### P1 — Config Migration + Customization
- **F-P1-1**: `project_name` moved to core config
- **F-P1-2**: `project_name` removed from bmm config
- **F-P1-3**: All config version headers updated to 6.6.0
- **F-P1-4**: CSV row coverage verified post-migration
- **F-P1-5**: `resolve_customization.py` included in plugin
- **F-P1-6**: `bmad-customize` skill created from upstream

#### P2 — Polish
- **F-P2-1**: CHANGELOG updated
- **F-P2-2**: Plugin version bumped to 1.1.0
~~~

**Files affected:**
- `CHANGELOG.md`

**Dependencies:** F-P0-1, F-P0-2, F-P0-3, F-P1-1 through F-P1-6 (all changes documented)

**Verification steps:**
- [ ] CHANGELOG has `[1.1.0]` section at top
- [ ] All Phase F task IDs referenced
- [ ] No fabricated entries

**Risk notes:** None

**Estimated complexity:** Small — documentation only

---

### Task F-P2-2: Plugin version bump to 1.1.0 [Size: XS]

**SPEC ref:** F-P2-2

**Description:** Bump plugin version from `1.0.8` to `1.1.0` in `plugin.yaml`. This is a minor version bump (feature addition from upstream sync), not a patch bump.

**Changes required:**
1. Update `version: 1.0.8` to `version: 1.1.0` in `plugin.yaml` line 3

**Files affected:**
- `plugin.yaml`

**Dependencies:** All P0 and P1 tasks complete (version bump is the final gate)

**Verification steps:**
- [ ] `grep 'version: 1.1.0' plugin.yaml` → found
- [ ] `python -m pytest tests/ -v` — all green

**Risk notes:** None

**Estimated complexity:** Small — single line change

---

## Checkpoint: P2 (ready for /ship)

**Pass criteria — all required for `/ship`:**
- [ ] CHANGELOG updated with Phase F entries
- [ ] Plugin version `1.1.0`
- [ ] All 20 BMAD agents functional end-to-end on VPS testing instance
- [ ] BMAD initializable from any path
- [ ] Tagged as `v1.1.0`; merged to `main`

---

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| A0-specific sections lost during merge | High — breaks Step Complete / State Write | Low | 5-step merge protocol; explicit diff check after each merge |
| Upstream structural changes conflict with our YAML frontmatter | Medium — frontmatter parsing breaks | Low | Read file fully before merge; frontmatter is delimited by `---` fences |
| Config migration breaks routing | High — CSV rows can't find `project_name` | Low | F-P1-4 dedicated verification task; upstream confirms no CSV references `project_name` |
| Test regressions from workflow step content changes | Medium — tests may validate step structure | Low | No existing tests parse step file internals; all 200+ tests should pass unchanged |
| Upstream step-04 has fewer lines than ours | Low — content removed upstream that we need | Low | Our +24 lines are A0-specific (State Write); upstream content is additive |
| customize.toml files have upstream-specific paths | Medium — customization won't resolve correctly | Low | Careful path adaptation during F-P1-6; test with list_customizable_skills.py |

---

## Task Summary

| ID | Task | Priority | Size | Dependencies | Status |
|----|------|----------|------|-------------|--------|
| F-P0-1 | Fix pre-checked architecture checklist | P0 | M | None | Ready |
| F-P0-2 | Add file churn detection to epic design | P0 | M | None | Ready |
| F-P0-3 | Add file churn check + HALT + on_complete | P0 | M | None | Ready |
| F-P1-1 | Move project_name to core config | P1 | XS | None | Ready |
| F-P1-2 | Remove project_name from bmm config | P1 | XS | F-P1-1 | Ready |
| F-P1-3 | Update config versions to 6.6.0 | P1 | XS | F-P1-1, F-P1-2 | Ready |
| F-P1-4 | Verify CSV row coverage | P1 | S | F-P1-3 | Ready |
| F-P1-5 | Include resolve_customization.py | P1 | S | None | Ready |
| F-P1-6 | Create bmad-customize skill | P1 | M | F-P1-5 | Ready |
| F-P2-1 | Update CHANGELOG | P2 | XS | All P0+P1 | Ready |
| F-P2-2 | Plugin version bump to 1.1.0 | P2 | XS | All P0+P1 | Ready |

**Totals:** 12 tasks (P0: 3 · P1: 6 · P2: 2)
**Estimated effort:** 1–2 days
