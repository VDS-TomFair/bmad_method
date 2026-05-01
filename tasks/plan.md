# Implementation Plan: BMAD Method Plugin — Phase H (BMB Creation Path Fixes, v1.4)

## Overview

Fix the BMB creation path problem where agents and skills built by BMB are placed in a non-discoverable directory (`.a0proj/_bmad-output/bmb-creations/`). BMB output must land in A0-discoverable directories so that built agents are immediately callable via `call_subordinate` and built skills are immediately discoverable via `skills_tool`.

**Two-phase approach:**
1. **Create in project scope** — BMB writes final output to `.a0proj/agents/{name}/` and `.a0proj/skills/{name}/` (A0 discovers these)
2. **Promote to plugin** — Optional: copy from project to plugin for global availability

**Prereq:** Phases A–G COMPLETE (57+ tasks, 292+ tests, 60+ commits).
**Reference:** `docs/workflow-builder-failure-analysis.md`, A0 source code discovery paths
**Branch:** `develop` → `main` on /ship.
**Version target:** v1.3.0 → v1.4.0
**Test command:** `cd /a0/usr/projects/a0_bmad_method && python -m pytest tests/ -v`

---

## Phase G — Completed ✅

10 tasks (P0: 5, P1: 3, P2: 2) — all complete. Agent prompt defects fixed, include mechanism working, process compliance enforced.

**Delivered:** v1.3.0 — failure probability reduced from 95-100% → <5%.

---

## Architecture Decisions

- **Config split enables all other work** — `bmb_creations_output_folder` is a single path. Replacing with 3 separate paths (`bmb_staging_folder`, `bmb_build_output_agents`, `bmb_build_output_skills`) is the foundation for everything else. H-P0-1 MUST be first.
- **`{project-root}` in BMAD config resolves to `.a0proj/`** — So `{project-root}/agents` = `.a0proj/agents/` which IS in A0's project-scoped discovery path (`usr/projects/*/.a0proj/agents/`).
- **A0 discovery paths (verified from source code):**
  - Agents: `usr/projects/*/.a0proj/agents/` (project-scoped)
  - Skills: `usr/projects/*/.a0proj/skills/` (project-scoped)
  - Agents: `plugins/*/agents/` (global/plugin-scoped)
  - Skills: `plugins/*/skills/` (global/plugin-scoped)
- **Staging directory for intermediate artifacts** — Plans, reports, validation outputs go to `.a0proj/_bmad-output/bmb-staging/` (not discoverable, not meant to be).
- **Promotion is optional and explicit** — Users run `/promote-agent {name}` or `/promote-skill {name}` to copy from project scope to plugin scope. No auto-promotion.
- **Module creation path** — Modules may need different handling since A0 doesn't have a `modules` discovery path. Clarify during H-P0-2 implementation (Open Question Q13).
- **~80 step files need path updates** — This is the bulk of the work. Most changes are find-and-replace of `bmb_creations_output_folder` → appropriate new variable.

---

## Dependency Graph

```
[H-P0-1: Split config.yaml paths] ← MUST BE FIRST
         │
         ▼
[VERIFY: BMB reads new path variables correctly]
[VERIFY: {project-root}/agents resolves to .a0proj/agents/]
         │
         ▼
[H-P0-2: Update ~80 BMB step files for new paths]
         │
         ▼
[CHECKPOINT P0 — config split done, step files updated, tests green]
         │
    ┌────┼────────────────┐
    │    │                │
    ▼    ▼                ▼
[H-P1-1: Create bmad-promote skill]  [H-P1-2: Update bmad-init.sh dirs]
    │    │                │
    ▼    ▼                ▼
[CHECKPOINT P1 — promotion works, init creates dirs]
         │
         ▼
[H-P2-1: Update celebrate steps with A0 guidance]
         │
         ▼
[CHECKPOINT P2 — ready for /ship]
```

**Parallelization:**
- H-P1-1 and H-P1-2 can run in parallel after P0 checkpoint (independent files)
- H-P2-1 can run anytime after H-P0-2 (independent of P1)

---

## Path Mapping Reference

| Artifact | Current (Wrong) | Fixed (Phase H) |
|---|---|---|
| Agent YAML + sidecar | `.a0proj/_bmad-output/bmb-creations/{name}/` | `.a0proj/agents/{name}/` (project-scoped) |
| Workflow/skill files | `.a0proj/_bmad-output/bmb-creations/workflows/` | `.a0proj/skills/{name}/` (project-scoped) |
| Plans, reports | `.a0proj/_bmad-output/bmb-creations/` | `.a0proj/_bmad-output/bmb-staging/` (intermediate) |
| Validation reports | `.a0proj/_bmad-output/bmb-creations/validation-*.md` | `.a0proj/_bmad-output/bmb-staging/validation-*.md` |

**Promotion flow:**
`.a0proj/agents/{name}/` → `/promote-agent {name}` → `plugins/bmad_method/agents/{name}/` (global)

---

## Phase H — P0: Critical Fixes (2 tasks)

**Gate: H-P0-1 MUST pass before H-P0-2. Both P0 tasks must pass before P1.**

---

### Task H-P0-1: Split BMB config paths [Size: S]

**SPEC ref:** H-P0-1 (R10)
**Root cause:** RC6 — single output path for all artifact types

**Description:** Replace the single `bmb_creations_output_folder` with 3 separate paths for staging, agents, and skills. This is the foundation for all other Phase H work.

**Changes required:**
1. Open `skills/bmad-bmb/config.yaml`
2. Remove `bmb_creations_output_folder: "{project-root}/_bmad-output/bmb-creations"`
3. Add:
   ```yaml
   bmb_staging_folder: "{project-root}/_bmad-output/bmb-staging"
   bmb_build_output_agents: "{project-root}/agents"
   bmb_build_output_skills: "{project-root}/skills"
   ```
4. Verify BMB reads new path variables correctly
5. Confirm `{project-root}/agents` resolves to `.a0proj/agents/` (in A0's discovery path)
6. Run `python -m pytest tests/ -v` — all 292+ tests green

**Files affected:**
- `skills/bmad-bmb/config.yaml` (1 file)

**Dependencies:** None (MUST be first task)

**Verification steps:**
- [ ] `grep 'bmb_staging_folder' skills/bmad-bmb/config.yaml` → found
- [ ] `grep 'bmb_build_output_agents' skills/bmad-bmb/config.yaml` → found
- [ ] `grep 'bmb_build_output_skills' skills/bmad-bmb/config.yaml` → found
- [ ] `grep 'bmb_creations_output_folder' skills/bmad-bmb/config.yaml` → NOT found
- [ ] BMB reads new path variables correctly (manual or test verification)
- [ ] `python -m pytest tests/ -v` — all 292+ tests green

**Risk notes:** Low risk — single config file change. However, all ~80 step files reference the old variable, so BMB will break between H-P0-1 and H-P0-2. This is expected and acceptable.

**Estimated effort:** 15–30 minutes

---

### Task H-P0-2: Update BMB step files for new paths [Size: L → decomposed]

**SPEC ref:** H-P0-2 (R11)
**Root cause:** RC6 — ~80 step files reference old `bmb_creations_output_folder`

**Description:** Update all BMB step files that reference `bmb_creations_output_folder` or `bmb-creations`. Agent creation steps → `bmb_build_output_agents`, workflow creation steps → `bmb_build_output_skills`, staging/artifact steps → `bmb_staging_folder`.

**Changes required:**
1. Find all files referencing `bmb_creations_output_folder` or `bmb-creations`:
   ```bash
   grep -rl 'bmb_creations_output_folder\|bmb-creations' skills/bmad-bmb/workflows/
   ```
2. For each file, determine artifact type and replace with correct variable:
   - **Agent build steps** (step-07-build-agent.md, etc.) → `bmb_build_output_agents`
   - **Workflow build steps** (step-11-completion.md, etc.) → `bmb_build_output_skills`
   - **Module build steps** (step-07-complete.md, etc.) → clarify destination (Q13)
   - **Staging steps** (plans, reports, validation) → `bmb_staging_folder`
3. Key files (highest priority — actual build output steps):
   - `workflows/agent/steps-c/step-07-build-agent.md` — writes agent.yaml and prompts
   - `workflows/agent/steps-c/step-08-celebrate.md` — confirms output location
   - `workflows/workflow/steps-c/step-09-build-next-step.md` — redirect build output
   - `workflows/workflow/steps-c/step-11-completion.md` — finalizes workflow
   - `workflows/module/steps-c/step-07-complete.md` — finalizes module
4. Run `python -m pytest tests/ -v` — all 292+ tests green

**Files affected:**
- `skills/bmad-bmb/workflows/agent/steps-c/step-07-build-agent.md`
- `skills/bmad-bmb/workflows/agent/steps-c/step-08-celebrate.md`
- `skills/bmad-bmb/workflows/workflow/steps-c/step-09-build-next-step.md`
- `skills/bmad-bmb/workflows/workflow/steps-c/step-11-completion.md`
- `skills/bmad-bmb/workflows/module/steps-c/step-07-complete.md`
- ~75 additional step files in `skills/bmad-bmb/workflows/`

**Dependencies:** H-P0-1 (config must define the new paths first)

**Verification steps:**
- [ ] `grep -rl 'bmb_creations_output_folder' skills/bmad-bmb/workflows/` → 0 files
- [ ] `grep -rl 'bmb-creations' skills/bmad-bmb/workflows/` → 0 files (or only comments/docs)
- [ ] Agent build steps reference `bmb_build_output_agents`
- [ ] Workflow build steps reference `bmb_build_output_skills`
- [ ] Staging steps reference `bmb_staging_folder`
- [ ] `python -m pytest tests/ -v` — all 292+ tests green

**Risk notes:** Medium risk — large number of files. Mitigation: use `grep -rl` to find all references, batch-replace systematically, verify counts before/after.

**Estimated effort:** 1.5–2.5 hours (find all refs, classify, replace, verify)

---

## Checkpoint: P0

**Pass criteria (ALL must be green before P1 starts):**
- [ ] `bmb_creations_output_folder` removed from `skills/bmad-bmb/config.yaml`
- [ ] `bmb_staging_folder`, `bmb_build_output_agents`, `bmb_build_output_skills` defined in config.yaml
- [ ] All BMB step files updated — no references to old `bmb_creations_output_folder`
- [ ] Agent build steps write to `bmb_build_output_agents` (→ `.a0proj/agents/`)
- [ ] Workflow build steps write to `bmb_build_output_skills` (→ `.a0proj/skills/`)
- [ ] Staging artifacts go to `bmb_staging_folder` (→ `.a0proj/_bmad-output/bmb-staging/`)
- [ ] `python -m pytest tests/ -v` → all 292+ tests green

---

## Phase H — P1: High Priority (2 tasks)

**Prereq:** P0 checkpoint passed.

---

### Task H-P1-1: Create bmad-promote skill [Size: M]

**SPEC ref:** H-P1-1 (R12)
**Root cause:** RC7 — no mechanism to promote project-scoped artifacts to global

**Description:** New skill `bmad-promote` that copies agents/skills from project scope (`.a0proj/agents/`, `.a0proj/skills/`) to plugin scope (`plugins/bmad_method/agents/`, `plugins/bmad_method/skills/`). Makes BMB-built artifacts globally available across all projects.

**Changes required:**
1. Create `skills/bmad-promote/` directory with:
   - `SKILL.md` — skill definition with triggers: `/promote-agent`, `/promote-workflow`, `/promote-skill`
   - `module-help.csv` — routing entries for promote commands
2. SKILL.md behavior:
   - Parse command to determine artifact type (agent/skill) and name
   - Validate source exists (`.a0proj/agents/{name}/` or `.a0proj/skills/{name}/`)
   - Validate artifact structure (`agent.yaml` present for agents, `SKILL.md` present for skills)
   - Check destination doesn't exist (warn if overwriting — Q14)
   - Copy source → plugin directory
   - Confirm promoted artifact is globally discoverable
3. Add test file `tests/test_bmad_promote_skill.py`

**Files affected:**
- NEW: `skills/bmad-promote/SKILL.md`
- NEW: `skills/bmad-promote/module-help.csv`
- NEW: `tests/test_bmad_promote_skill.py`

**Dependencies:** H-P0-2 (step files must write to correct paths before promotion makes sense)

**Verification steps:**
- [ ] `skills/bmad-promote/SKILL.md` exists with correct trigger patterns
- [ ] `/promote-agent {name}` copies `.a0proj/agents/{name}/` → `plugins/bmad_method/agents/{name}/`
- [ ] `/promote-skill {name}` copies `.a0proj/skills/{name}/` → `plugins/bmad_method/skills/{name}/`
- [ ] Overwrite protection works (warns when destination exists)
- [ ] `python -m pytest tests/ -v` — all tests green

**Risk notes:** Low-medium risk — new skill, no existing code to break. Must handle edge cases (missing source, invalid structure, existing destination).

**Estimated effort:** 1–1.5 hours

---

### Task H-P1-2: Update bmad-init.sh for project-scope dirs [Size: XS]

**SPEC ref:** H-P1-2 (R13)
**Root cause:** RC6 — init script doesn't create agent/skill output directories

**Description:** Add `mkdir -p` for `.a0proj/agents/` and `.a0proj/skills/` to the init script so BMB has output directories ready.

**Changes required:**
1. Open `skills/bmad-init/scripts/bmad-init.sh`
2. Find the section where `.a0proj/` subdirectories are created
3. Add:
   ```bash
   # Ensure BMB output directories exist
   mkdir -p "$A0PROJ/agents"
   mkdir -p "$A0PROJ/skills"
   ```
4. Verify with: `bash -n skills/bmad-init/scripts/bmad-init.sh` (syntax check)
5. Run smoke test: `bash skills/bmad-init/scripts/bmad-init.sh /tmp/test-bmad-phase-h`
6. Verify: `test -d /tmp/test-bmad-phase-h/.a0proj/agents` → exists
7. Verify: `test -d /tmp/test-bmad-phase-h/.a0proj/skills` → exists

**Files affected:**
- `skills/bmad-init/scripts/bmad-init.sh` (add 2 lines)

**Dependencies:** None (independent of H-P1-1, can run in parallel after P0 checkpoint)

**Verification steps:**
- [ ] `grep 'mkdir.*\$A0PROJ/agents' skills/bmad-init/scripts/bmad-init.sh` → found
- [ ] `grep 'mkdir.*\$A0PROJ/skills' skills/bmad-init/scripts/bmad-init.sh` → found
- [ ] `bash -n skills/bmad-init/scripts/bmad-init.sh` → no syntax errors
- [ ] Smoke test creates `.a0proj/agents/` and `.a0proj/skills/` directories
- [ ] `python -m pytest tests/ -v` — all 292+ tests green

**Risk notes:** Very low risk — 2 lines added to bash script, additive only.

**Estimated effort:** 15 minutes

---

## Checkpoint: P1

**Pass criteria:**
- [ ] `bmad-promote` skill created with `/promote-agent`, `/promote-workflow`, `/promote-skill` triggers
- [ ] Promotion copies from `.a0proj/agents/` to `plugins/bmad_method/agents/` correctly
- [ ] Promotion copies from `.a0proj/skills/` to `plugins/bmad_method/skills/` correctly
- [ ] `bmad-init.sh` creates `.a0proj/agents/` and `.a0proj/skills/` directories
- [ ] `python -m pytest tests/ -v` → all tests green

---

## Phase H — P2: Nice to Have (1 task)

**Prereq:** P0 checkpoint passed (P1 not strictly required).

---

### Task H-P2-1: Update celebrate steps with A0 auto-discovery guidance [Size: S]

**SPEC ref:** H-P2-1 (R14)
**Root cause:** UX — celebrate steps give wrong install instructions

**Description:** Replace manual install instructions in celebrate step files with A0 auto-discovery guidance. After Phase H, agents/skills appear automatically — no manual install needed.

**Changes required:**
1. Update celebrate steps to show A0 auto-discovery guidance:
   ```markdown
   ## A0 Auto-Discovery

   Your new agent is now available! Agent Zero automatically discovers agents in `.a0proj/agents/`.

   **To use:** Call `call_subordinate` with profile `bmad-{agent-name}`.

   **To make globally available** (all projects): Run `/promote-agent {agent-name}`.
   ```
2. Apply to all celebrate step files across workflows:
   - `workflows/agent/steps-c/step-08-celebrate.md`
   - `workflows/agent/steps-e/step-09-celebrate.md` (if exists)
   - Similar celebrate steps in workflow/module flows

**Files affected:**
- `skills/bmad-bmb/workflows/agent/steps-c/step-08-celebrate.md`
- Additional celebrate step files (TBD — grep for celebrate steps)

**Dependencies:** H-P0-2 (paths must be correct before celebrating correct locations)

**Verification steps:**
- [ ] Celebrate steps contain `A0 Auto-Discovery` section
- [ ] No manual install instructions remain
- [ ] Promotion command mentioned for global availability
- [ ] `python -m pytest tests/ -v` — all tests green

**Risk notes:** Low risk — text changes in step files only.

**Estimated effort:** 30–45 minutes

---

## Checkpoint: P2 (ready for /ship)

**Pass criteria — all required for `/ship`:**
- [ ] All celebrate steps updated with A0 auto-discovery guidance
- [ ] CHANGELOG updated with Phase H entries
- [ ] Plugin version `1.4.0`
- [ ] All 292+ tests green
- [ ] BMB agent creation tested end-to-end — agent appears in `call_subordinate` profile list
- [ ] BMB workflow creation tested end-to-end — skill appears in `skills_tool:list`
- [ ] Promotion tested — project-scoped agent/skill becomes globally available after `/promote-*`
- [ ] Tagged as `v1.4.0`; merged to `main`

---

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| ~80 step file updates introduce wrong variable in some files | Medium — artifacts go to wrong directory | Medium | Use `grep -rl` to find ALL references; classify by artifact type before replace; verify counts match |
| Module creation path unclear (Q13) | Low — modules may not have A0 discovery path | Medium | Clarify during H-P0-2; modules may stay in staging or map to skills |
| Config variable names don't match BMB's variable resolution | High — BMB can't find paths | Low | Verify `{project-root}` resolution works for all 3 new paths |
| Promotion overwrites existing plugin artifacts (Q14) | Medium — data loss | Medium | Add overwrite protection with confirmation prompt |
| Test suite doesn't cover BMB output paths | Medium — path defects not caught | High | Add `tests/test_phase_h_paths.py` for path verification |
| Breaking change between H-P0-1 and H-P0-2 | Low — BMB unusable in intermediate state | High | Complete H-P0-1 and H-P0-2 in same session |

---

## Open Questions

| # | Question | Status | Action |
|---|----------|--------|--------|
| Q12 | BMB step file count — exact scope of changes per file | 🔄 Phase H | Verify during H-P0-2 with `grep -rl` |
| Q13 | Module creation path — A0 has no `modules` discovery path | 🔄 Phase H | Clarify during H-P0-2; may map to skills or stay in staging |
| Q14 | Promotion safety — overwrite behavior for existing artifacts | 🔄 Phase H | Define during H-P1-1; add confirmation prompt |

---

## Task Summary

| ID | Task | Priority | Size | Dependencies | Status |
|----|------|----------|------|-------------|--------|
| H-P0-1 | Split BMB config paths | P0 | S | None (MUST BE FIRST) | Ready |
| H-P0-2 | Update BMB step files for new paths | P0 | L | H-P0-1 | Ready |
| H-P1-1 | Create bmad-promote skill | P1 | M | H-P0-2 | Ready |
| H-P1-2 | Update bmad-init.sh for project-scope dirs | P1 | XS | P0 checkpoint | Ready |
| H-P2-1 | Update celebrate steps with A0 guidance | P2 | S | H-P0-2 | Ready |

**Totals:** 5 tasks (P0: 2 · P1: 2 · P2: 1)
**Estimated effort:** 3–4.5 hours total (P0: 2–3h · P1: 1.25h · P2: 0.5h)
