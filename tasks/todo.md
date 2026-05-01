# TODO: BMAD Method Plugin — Phase H (BMB Creation Path Fixes) — 5 tasks

Phases A–G: COMPLETE (57+/57+ tasks done)

---

## Phase G — Completed ✅

10 tasks (P0: 5, P1: 3, P2: 2) — all complete. Agent prompt defects fixed, include mechanism working.
Delivered: v1.3.0 — failure probability reduced from 95-100% → <5%.

---

## Phase H — P0: Critical Fixes

- [ ] **H-P0-1**: Split BMB config paths — add `bmb_staging_folder`, `bmb_build_output_agents`, `bmb_build_output_skills` (S) 🔑 MUST BE FIRST
  - Remove `bmb_creations_output_folder` from `skills/bmad-bmb/config.yaml`
  - Add 3 new paths: staging → `.a0proj/_bmad-output/bmb-staging/`, agents → `.a0proj/agents/`, skills → `.a0proj/skills/`
  - `skills/bmad-bmb/config.yaml` (1 file)
  - Verify: `grep 'bmb_staging_folder' skills/bmad-bmb/config.yaml` → found
  - Verify: `grep 'bmb_build_output_agents' skills/bmad-bmb/config.yaml` → found
  - Verify: `grep 'bmb_build_output_skills' skills/bmad-bmb/config.yaml` → found
  - Verify: `grep 'bmb_creations_output_folder' skills/bmad-bmb/config.yaml` → NOT found
  - Verify: BMB reads new path variables correctly
  - Verify: `python -m pytest tests/ -v` all green

- [ ] **H-P0-2**: Update BMB step files for new paths (~80 files) (L)
  - Find all refs: `grep -rl 'bmb_creations_output_folder\|bmb-creations' skills/bmad-bmb/workflows/`
  - Agent build steps → `bmb_build_output_agents`
  - Workflow build steps → `bmb_build_output_skills`
  - Staging steps (plans, reports, validation) → `bmb_staging_folder`
  - Module build steps → clarify destination (Q13)
  - Key files:
    - `skills/bmad-bmb/workflows/agent/steps-c/step-07-build-agent.md`
    - `skills/bmad-bmb/workflows/agent/steps-c/step-08-celebrate.md`
    - `skills/bmad-bmb/workflows/workflow/steps-c/step-09-build-next-step.md`
    - `skills/bmad-bmb/workflows/workflow/steps-c/step-11-completion.md`
    - `skills/bmad-bmb/workflows/module/steps-c/step-07-complete.md`
  - ~75 additional step files in `skills/bmad-bmb/workflows/`
  - Verify: `grep -rl 'bmb_creations_output_folder' skills/bmad-bmb/workflows/` → 0 files
  - Verify: Agent build steps reference `bmb_build_output_agents`
  - Verify: Workflow build steps reference `bmb_build_output_skills`
  - Verify: Staging steps reference `bmb_staging_folder`
  - Verify: `python -m pytest tests/ -v` all green

### P0 Checkpoint

- [ ] `bmb_creations_output_folder` removed from config.yaml
- [ ] `bmb_staging_folder`, `bmb_build_output_agents`, `bmb_build_output_skills` defined
- [ ] All BMB step files updated — no old variable references
- [ ] Agent build steps → `bmb_build_output_agents` (→ `.a0proj/agents/`)
- [ ] Workflow build steps → `bmb_build_output_skills` (→ `.a0proj/skills/`)
- [ ] Staging artifacts → `bmb_staging_folder` (→ `.a0proj/_bmad-output/bmb-staging/`)
- [ ] `python -m pytest tests/ -v` → 292+ tests green

---

## Phase H — P1: High Priority

- [ ] **H-P1-1**: Create `bmad-promote` skill for project → plugin promotion (M)
  - Triggers: `/promote-agent`, `/promote-workflow`, `/promote-skill`
  - Validate source exists (`.a0proj/agents/{name}/` or `.a0proj/skills/{name}/`)
  - Validate structure (`agent.yaml` for agents, `SKILL.md` for skills)
  - Copy to plugin dir: `plugins/bmad_method/agents/{name}/` or `plugins/bmad_method/skills/{name}/`
  - Overwrite protection (Q14)
  - NEW: `skills/bmad-promote/SKILL.md`
  - NEW: `skills/bmad-promote/module-help.csv`
  - NEW: `tests/test_bmad_promote_skill.py`
  - Verify: `test -f skills/bmad-promote/SKILL.md` → exists
  - Verify: `/promote-agent {name}` copies correctly
  - Verify: `/promote-skill {name}` copies correctly
  - Verify: `python -m pytest tests/ -v` all green

- [ ] **H-P1-2**: Update `bmad-init.sh` to create `.a0proj/agents/` and `.a0proj/skills/` dirs (XS)
  - Add `mkdir -p "$A0PROJ/agents"` and `mkdir -p "$A0PROJ/skills"`
  - `skills/bmad-init/scripts/bmad-init.sh` (add 2 lines)
  - Verify: `bash -n skills/bmad-init/scripts/bmad-init.sh` → no errors
  - Verify: Smoke test creates both directories
  - Verify: `python -m pytest tests/ -v` all green

### P1 Checkpoint

- [ ] `bmad-promote` skill created with correct triggers
- [ ] Promotion copies `.a0proj/agents/` → `plugins/bmad_method/agents/` correctly
- [ ] Promotion copies `.a0proj/skills/` → `plugins/bmad_method/skills/` correctly
- [ ] `bmad-init.sh` creates `.a0proj/agents/` and `.a0proj/skills/`
- [ ] `python -m pytest tests/ -v` → all green

---

## Phase H — P2: Nice to Have

- [ ] **H-P2-1**: Update celebrate steps with A0 auto-discovery guidance (S)
  - Replace manual install instructions with A0 auto-discovery:
    - Agent auto-discovered in `.a0proj/agents/`
    - Use via `call_subordinate` with profile `bmad-{name}`
    - Promote globally via `/promote-agent {name}`
  - `skills/bmad-bmb/workflows/agent/steps-c/step-08-celebrate.md`
  - Additional celebrate steps in workflow/module flows
  - Verify: Celebrate steps contain `A0 Auto-Discovery` section
  - Verify: No manual install instructions remain
  - Verify: `python -m pytest tests/ -v` all green

### P2 Checkpoint (ready for /ship)

- [ ] All celebrate steps updated with A0 auto-discovery guidance
- [ ] CHANGELOG updated with Phase H entries
- [ ] Plugin version `1.4.0`
- [ ] All 292+ tests green
- [ ] BMB agent creation end-to-end — agent in `call_subordinate` profile list
- [ ] BMB workflow creation end-to-end — skill in `skills_tool:list`
- [ ] Promotion tested — project → plugin scope works
- [ ] Tagged `v1.4.0`; merged to `main`
