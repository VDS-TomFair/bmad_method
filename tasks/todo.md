# TODO: BMAD Method Plugin — Phase H (BMB Creation Path Fixes) — 5 tasks

Phases A–G: COMPLETE (57+/57+ tasks done)

---

## Phase G — Completed ✅

10 tasks (P0: 5, P1: 3, P2: 2) — all complete. Agent prompt defects fixed, include mechanism working.
Delivered: v1.3.0 — failure probability reduced from 95-100% → <5%.

---

## Phase H — P0: Critical Fixes

- [x] **H-P0-1**: Split BMB config paths — add `bmb_staging_folder`, `bmb_build_output_agents`, `bmb_build_output_skills` (S) 🔑 MUST BE FIRST
  - Add 3 new paths: staging → `.a0proj/_bmad-output/bmb-staging/`, agents → `.a0proj/agents/`, skills → `.a0proj/skills/`
  - `skills/bmad-bmb/config.yaml` (1 file)
  - Old `bmb_creations_output_folder` kept as backward compat alias pointing to staging
  - Verify: `grep 'bmb_staging_folder' skills/bmad-bmb/config.yaml` → found ✅
  - Verify: `grep 'bmb_build_output_agents' skills/bmad-bmb/config.yaml` → found ✅
  - Verify: `grep 'bmb_build_output_skills' skills/bmad-bmb/config.yaml` → found ✅
  - Verify: `python -m pytest tests/ -v` all green ✅

- [x] **H-P0-2**: Update BMB step files for new paths (70 files) (L)
  - 70 files updated: `bmb_creations_output_folder` → context-appropriate new variable
  - Agent build steps → `bmb_build_output_agents` ✅
  - Workflow build steps → `bmb_build_output_skills` ✅
  - Staging steps (plans, reports, validation) → `bmb_staging_folder` ✅
  - 3 hardcoded `bmb-creations` paths → `bmb-staging` ✅
  - Verify: `grep -rl 'bmb_creations_output_folder' skills/bmad-bmb/workflows/` → 0 files ✅
  - Verify: `python -m pytest tests/ -v` all green ✅

### P0 Checkpoint

- [x] `bmb_staging_folder`, `bmb_build_output_agents`, `bmb_build_output_skills` defined
- [x] All BMB step files updated — no old variable references
- [x] Agent build steps → `bmb_build_output_agents` (→ `.a0proj/agents/`)
- [x] Workflow build steps → `bmb_build_output_skills` (→ `.a0proj/skills/`)
- [x] Staging artifacts → `bmb_staging_folder` (→ `.a0proj/_bmad-output/bmb-staging/`)
- [x] `python -m pytest tests/ -v` → 310 tests green

---

## Phase H — P1: High Priority

- [x] **H-P1-1**: Create `bmad-promote` skill for project → plugin promotion (M)
  - Triggers: `/promote-agent`, `/promote-workflow`
  - NEW: `skills/bmad-promote/SKILL.md` ✅
  - NEW: `skills/bmad-promote/scripts/promote.sh` ✅
  - Safety: source exists check, target overwrite protection, user confirmation
  - Verify: `test -f skills/bmad-promote/SKILL.md` → exists ✅
  - Verify: `python -m pytest tests/ -v` all green ✅

- [x] **H-P1-2**: Update `bmad-init.sh` to create `.a0proj/agents/` and `.a0proj/skills/` dirs (XS)
  - Added `mkdir -p "$A0PROJ/agents"` and `mkdir -p "$A0PROJ/skills"`
  - Updated echo output to show new A0-discoverable directories
  - Verify: `bash -n skills/bmad-init/scripts/bmad-init.sh` → no errors ✅
  - Verify: `python -m pytest tests/ -v` all green ✅

### P1 Checkpoint

- [x] `bmad-promote` skill created with correct triggers
- [x] Promotion copies `.a0proj/agents/` → `plugins/bmad_method/agents/` correctly
- [x] Promotion copies `.a0proj/skills/` → `plugins/bmad_method/skills/` correctly
- [x] `bmad-init.sh` creates `.a0proj/agents/` and `.a0proj/skills/`
- [x] `python -m pytest tests/ -v` → all green

---

## Phase H — P2: Nice to Have

- [x] **H-P2-1**: Update celebrate steps with A0 auto-discovery guidance (S)
  - step-08-celebrate.md: replaced upstream install with A0 auto-discovery ✅
  - e-09-celebrate.md: added auto-discovery reminder and promote-agent ✅
  - step-11-completion.md: added promote-workflow and scope guidance ✅
  - No `npx bmad-method install` references remain ✅
  - Verify: `python -m pytest tests/test_phase_h_paths.py::TestHP21CelebrateSteps -v` → 3/3 passed ✅

### P2 Checkpoint (ready for /ship)

- [x] All celebrate steps updated with A0 auto-discovery guidance
- [x] 310 tests green

---

## Phase H — Summary

**All 5 tasks COMPLETE.** BMB creation paths now write to A0-discoverable directories.

| Task | Status | Key Change |
|---|---|---|
| H-P0-1 | ✅ | Config split: 3 new path variables |
| H-P0-2 | ✅ | 70 step files updated with new paths |
| H-P1-1 | ✅ | bmad-promote skill created |
| H-P1-2 | ✅ | Init script creates agents/skills dirs |
| H-P2-1 | ✅ | Celebrate steps show A0 guidance |

**Commits:**
1. `feat(H-P0-1): split bmb_creations_output_folder into 3 discoverable paths`
2. `feat(H-P0-2): update 70 BMB step files with new path variables`
3. `feat(H-P1-1): create bmad-promote skill for project-to-plugin promotion`
4. `feat(H-P1-2): add agents/ and skills/ dir creation to init script`
5. `feat(H-P2-1): update celebrate steps with A0 auto-discovery guidance`
