# BMAD Alignment Fix Sprint — Implementation Plan v2.0

**Source of truth:** `SPEC.md` (1,099 lines)  
**Date:** 2026-05-02  
**Branch:** `develop` → `main` on `/ship`  
**Upstream:** BMAD-METHOD v6.6.0  

---

## 1. Overview

The BMAD A0 plugin scored 87/100 on the alignment audit. It has excellent workflow coverage (79/79 = 100%) and a correct customization engine, but needs structural cleanup to match upstream v6.6.0 conventions. This sprint fixes all alignment issues plus three user-directed changes beyond audit scope.

**What we're fixing (6 bundles, 33 subtasks):**

- **A1:** CSV routing → YAML `module.yaml` (Agent Zero parses YAML natively)
- **A2:** Remove CIS named personas → upstream generic titles
- **A3:** Remove bmad-quick-dev agent → Quick Dev is a menu item under Amelia
- **P1:** Consolidate SM/QA into Amelia, fix Morgan icon, fix Quick Dev menu code, add missing menus
- **P2:** Resolve icon collisions, update Sally's filmmaker style, address menu code collisions
- **P3:** 8-step activation sequence, file-based sidecar memory, project-context.md auto-loading

**Prior work (COMPLETE):** Phases A–H delivered 292+ tests, 60+ commits. This sprint builds on that foundation.

---

## 2. Dependency Graph

```
Bundle 1: CSV → YAML (P0)
    │
    ├──→ Bundle 2: Agent Consolidation (P1) ──┐
    │         needs module.yaml with           │
    │         correct skill assignments          │
    │                                           ├──→ Bundle 5: Test Updates (P1)
    Bundle 3: CIS Personas (P1) ──────────────┤         after Bundles 1-4
    (independent, parallel with 1)             │              │
    │                                          │              │
    └──→ Bundle 4: Quick Fixes (P1/P2) ───────┘              │
          Morgan icon independent;                            │
          init script needed by Bundle 6                      │
                                                               │
                                        Bundle 6: P3 Structural (P3)
                                        needs Bundle 4 init script
                                        + Bundle 5 tests passing
                                               │
                                               └──→ 6.10: P3 Tests (last)
```

---

## 3. Execution Strategy

### Parallel Tracks (Phase 1)

| Track A | Track B | Track C |
|---------|----------|---------|
| **Bundle 1: CSV → YAML** (P0) | **Bundle 3: CIS Personas** (P1) | **Bundle 4 partial** (Morgan icon, Sally fix) |
| Start first — foundational | Independent of YAML | Independent of everything |
| 1.1 → 1.2 → 1.3 → 1.4 → 1.5 → 1.6 | 3.1 → 3.2 → 3.3 | 4.1, 4.2, 4.3 |

### Sequential (Phase 2)

| Step | Bundle | Why Sequential |
|------|--------|----------------|
| 1 | **Bundle 2: Agent Consolidation** | Needs Bundle 1 YAML files with correct skill assignments |
| 2 | **Bundle 4 remaining** (4.4 init script, 4.5 collisions) | 4.4 is independent; 4.5 needs Bundle 2 agent consolidation |

### Sequential (Phase 3)

| Step | Bundle | Why Sequential |
|------|--------|----------------|
| 1 | **Bundle 5: Test Updates** | All Bundles 1-4 must be complete |
| 2 | **Bundle 6: P3 Structural** | Needs Bundle 4's init script `_bmad/custom/` creation |
| 3 | **Bundle 6.10: P3 Tests** | All P3 structural changes must be in place |

### Recommended Execution Order

```
Week 1 Day 1-2: Bundle 1 (1.1→1.6) + Bundle 3 (3.1→3.3) in parallel
Week 1 Day 3:   Bundle 2 (2.1→2.6) sequential
Week 1 Day 3:   Bundle 4 (4.1→4.5) mixed
Week 1 Day 4:   Bundle 5 (5.1→5.3) + integration verification
Week 2 Day 1-3: Bundle 6 (6.1→6.10) structural alignment
Week 2 Day 4:   Final integration, A2A live test, archive
```

---

## 4. Bundle Breakdown

### Bundle 1: CSV → YAML Migration (A1)

| Field | Value |
|-------|-------|
| **Priority** | P0 — foundational |
| **Effort** | M (1-2 days) |
| **Depends on** | Nothing (start first) |
| **Subtasks** | 1.1, 1.2, 1.3, 1.4, 1.5, 1.6 |

**Summary:** Replace all CSV routing files with upstream-compatible YAML `module.yaml` format. Agent Zero parses YAML natively; the CSV workaround was a divergence from upstream v6.6.0.

**Key files affected:**
- `skills/bmad-init/module-help.csv` → `skills/bmad-init/core/module.yaml`
- `skills/bmad-bmm/module-help.csv` → `skills/bmad-bmm/module.yaml`
- `skills/bmad-tea/module-help.csv` → `skills/bmad-tea/module.yaml`
- `skills/bmad-cis/module-help.csv` → `skills/bmad-cis/module.yaml`
- `skills/bmad-bmb/module-help.csv` → `skills/bmad-bmb/module.yaml`
- `extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py` (rewrite CSV→YAML parsing)
- `scripts/csv_to_yaml_converter.py` (new conversion script)
- `docs/adr/0010-yaml-canonical-routing.md` (new ADR)
- `docs/adr/0001-csv-canonical-routing.md` (supersede)

**Risks:**
- YAML parsing regression → Mitigation: automated equivalence test (YAML output == CSV output)
- PyYAML not available → Mitigation: verify in A0 container; add to requirements if needed
- Data loss during conversion → Mitigation: conversion script with round-trip validation

---

### Bundle 2: Agent Consolidation (P1 + A3)

| Field | Value |
|-------|-------|
| **Priority** | P1 — structural alignment |
| **Effort** | M (1 day) |
| **Depends on** | Bundle 1 (module.yaml needs correct skill assignments) |
| **Subtasks** | 2.1, 2.2, 2.3, 2.4, 2.5, 2.6 |

**Summary:** Remove bmad-sm, bmad-qa, bmad-quick-dev agent directories. Consolidate all their workflows into Amelia (bmad-dev). Quick Dev is a menu item, not a standalone agent per upstream.

**Key files affected:**
- `agents/bmad-sm/` (DELETE)
- `agents/bmad-qa/` (DELETE)
- `agents/bmad-quick-dev/` (DELETE)
- `agents/bmad-dev/customize.toml` (add SP, SS, VS, CS, DS, CR, QA, CC, ER, CK, QD, QS menus)
- `skills/bmad-bmm/module.yaml` (update skill assignments)
- `agents/bmad-master/prompts/agent.system.main.role.md` (remove static table)
- `helpers/bmad_status_core.py` (update AGENT_NAMES)

**Risks:**
- Missing workflows after consolidation → Mitigation: test all 79+ workflow codes resolve correctly
- Menu code collisions (QA, VS) → Mitigation: module-scoped, documented as intentional

---

### Bundle 3: CIS Persona Removal (A2)

| Field | Value |
|-------|-------|
| **Priority** | P1 — upstream alignment |
| **Effort** | S-M (0.5-1 day) |
| **Depends on** | Nothing (can run in parallel with Bundle 1) |
| **Subtasks** | 3.1, 3.2, 3.3 |

**Summary:** Remove named personas (Victor, Dr. Quinn, Maya, Carson, Sophia, Caravaggio) from CIS agents. Replace with upstream generic titles (Innovation Strategist, Creative Problem Solver, etc.). Resolve icon collisions (🎨 no longer shared across Sally + CIS).

**Key files affected:**
- `agents/bmad-innovation/agent.yaml` + prompts/
- `agents/bmad-problem-solver/agent.yaml` + prompts/
- `agents/bmad-design-thinking/agent.yaml` + prompts/
- `agents/bmad-brainstorming-coach/agent.yaml` + prompts/
- `agents/bmad-storyteller/agent.yaml` + prompts/
- `agents/bmad-presentation/agent.yaml` + prompts/
- `skills/bmad-cis/agents/`, `skills/bmad-cis/teams/`, `skills/bmad-cis/module.yaml`

**Risks:**
- CIS persona removal breaks user expectations → Mitigation: generic titles still functional
- Icon collision resolution incomplete → Mitigation: verify 🎨 unique to Sally after changes

---

### Bundle 4: Quick Fixes (P1/P2/P3)

| Field | Value |
|-------|-------|
| **Priority** | P1-P2 |
| **Effort** | S (2-4 hours) |
| **Depends on** | Bundle 2 (for icon conflict resolution) |
| **Subtasks** | 4.1, 4.2, 4.3, 4.4, 4.5 |

**Summary:** Collection of small fixes: Morgan icon 🏗️→📦, Sally filmmaker style, Paige US menu, init script `_bmad/custom/` creation, menu code collision documentation.

**Key files affected:**
- `agents/bmad-module-builder/agent.yaml` (icon fix)
- `agents/bmad-ux-designer/prompts/agent.system.main.role.md` (filmmaker)
- `agents/bmad-tech-writer/customize.toml` (US menu)
- `skills/bmad-init/scripts/bmad-init.sh` (`_bmad/custom/` creation)

**Risks:**
- Init script permission issue → Mitigation: uses `mkdir -p`, same as other directory creation

---

### Bundle 5: Test Updates and Final Verification

| Field | Value |
|-------|-------|
| **Priority** | P1 |
| **Effort** | M (0.5-1 day) |
| **Depends on** | All previous bundles (1-4) |
| **Subtasks** | 5.1, 5.2, 5.3 |

**Summary:** Update existing tests for YAML, add new tests for routing/consolidation/personas, run full integration verification including A2A live test on VPS.

**Key files affected:**
- `tests/test_extension_80.py` (update fixtures)
- `tests/test_core_csv_schema.py` → `tests/test_core_yaml_schema.py` (rename)
- New: `tests/test_yaml_routing.py`, `tests/test_agent_consolidation.py`, `tests/test_cis_personas.py`

**Risks:**
- Test count regression → Mitigation: target ≥ 300, verify before proceeding to Bundle 6

---

### Bundle 6: P3 Structural Alignment

| Field | Value |
|-------|-------|
| **Priority** | P3 — structural alignment |
| **Effort** | L (4-6 days total) |
| **Depends on** | Bundle 4 (init script) + Bundle 5 (P1/P2 tests pass) |
| **Subtasks** | 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 6.10 |

**Summary:** Implement full upstream 8-step activation sequence, file-based sidecar memory directories, and project-context.md auto-loading. This is the largest bundle with three interconnected P3 items.

**Implementation order:** 6.1–6.4 (activation) → 6.5 (project-context) → 6.6–6.9 (sidecar) → 6.10 (tests)

**Key files affected:**
- `prompts/bmad-agent-shared.md` (8-step activation rewrite)
- `skills/bmad-init/scripts/bmad-init.sh` (sidecar directory creation)
- `skills/bmad-sidecar-import/` (new skill for upstream migration)
- `tests/test_activation_sequence.py`, `tests/test_sidecar_memory.py`, `tests/test_project_context_loading.py` (new tests)
- 8 implementation workflow `step-01-init.md` files (project-context pre-step)

**Risks:**
- 8-step activation confuses existing agents → Mitigation: activation is prompt-based; test each agent's first response
- Sidecar files grow unbounded → Mitigation: markdown is lightweight; agents append concisely
- resolve_customization.py fails at activation → Mitigation: graceful fallback to hardcoded defaults

---

## 5. Architecture Decisions

| Decision | Rationale | Reference |
|----------|-----------|----------|
| **CSV → YAML routing** | Agent Zero parses YAML natively; upstream uses YAML; CSV was a divergence | ADR-0010 (new), supersedes ADR-0001 |
| **File-based sidecar memory (Option B)** | FAISS filter is post-filter, not pre-filter; file-based matches upstream exactly; human-readable | SPEC §6, P3 research |
| **Agent consolidation (SM/QA/QD → Amelia)** | Upstream: Quick Dev is a menu item under dev agent, not standalone | Upstream module.yaml |
| **CIS generic titles** | Upstream uses functional titles, not named personas; A0 routing works with any title | Upstream agent roster |
| **Module-scoped menu codes** | QA and VS codes intentionally duplicated across modules; routing manifest filters by module | SPEC §4.5 |
| **8-step activation sequence** | Matches upstream exactly: resolve customization → prepend → state → config → facts → greet → append → menu | Upstream docs |
| **Routing manifest format unchanged** | Internal YAML parsing change only; output text block injected into extras_temporary is identical | SPEC §1.3 |

---

## 6. Testing Checkpoints

### Checkpoint A: After Bundle 1 (CSV → YAML)
```
python -m pytest tests/test_extension_80.py tests/test_core_csv_schema.py -v
# All routing tests pass with YAML
for f in skills/*/module.yaml skills/bmad-init/core/module.yaml; do
  python -c "import yaml; yaml.safe_load(open('$f'))" && echo "✅ $f" || echo "❌ $f"
done
```

### Checkpoint B: After Bundles 2-4 (Consolidation + Personas + Fixes)
```
ls agents/bmad-sm agents/bmad-qa agents/bmad-quick-dev 2>&1 | grep 'No such file'
grep -r 'Victor\|Dr. Quinn\|Maya\|Carson\|Sophia\|Caravaggio' agents/bmad-*/ || echo '✅ All CIS personas removed'
grep '📦' agents/bmad-module-builder/agent.yaml
python -m pytest tests/ -v
```

### Checkpoint C: After Bundle 5 (Test Updates)
```
python -m pytest tests/ -v  # count ≥ 300, all pass
python -m flake8 api/ helpers/ extensions/ --max-line-length 100
```

### Checkpoint D: After Bundle 6 (P3 Structural)
```
python -m pytest tests/ -v  # count ≥ 310
bash skills/bmad-init/scripts/bmad-init.sh /tmp/test-bmad-project
ls -la /tmp/test-bmad-project/.a0proj/_bmad/custom/  # must exist
ls -la /tmp/test-bmad-project/.a0proj/_bmad/_memory/  # 16 sidecar dirs
```

### Final Gate: A2A Live Test
```
ssh -i /a0/usr/.ssh/id_ed25519 -o StrictHostKeyChecking=no root@162.19.152.199 \
  'docker exec agent-zero-testing bash -c "cd /a0/usr/projects/a0_bmad_method && git pull origin develop"'
# Send test messages via A2A protocol
# Verify routing, activation, sidecar loading
```

---

## 7. Rollback Plan

### Per-Bundle Rollback

| Bundle | Rollback Strategy |
|--------|-------------------|
| **1: CSV → YAML** | `git revert` restores CSV files; YAML files can coexist with CSV during transition. Revert routing extension to CSV parsing. |
| **2: Consolidation** | `git revert` restores agent directories. Restore Amelia's customize.toml to pre-consolidation state. |
| **3: CIS Personas** | `git revert` restores persona YAML and prompt files. |
| **4: Quick Fixes** | Individual `git revert` per subtask (each is independent). |
| **5: Test Updates** | `git revert` restores test files; no production code affected. |
| **6: P3 Structural** | `git revert` restores shared prompt and init script. Sidecar directories are empty on init, safe to remove. |

### Nuclear Option
```bash
git checkout main -- .  # Reset everything to last known good state
python -m pytest tests/ -v  # Verify
```

---

## 8. Effort Summary

| Bundle | Priority | Effort | Subtasks | Depends On |
|--------|----------|--------|----------|------------|
| 1: CSV → YAML | P0 | M (1-2d) | 6 | Nothing |
| 2: Consolidation | P1 | M (1d) | 6 | Bundle 1 |
| 3: CIS Personas | P1 | S-M (0.5-1d) | 3 | Nothing |
| 4: Quick Fixes | P1-P2 | S (2-4h) | 5 | Bundle 2 |
| 5: Test Updates | P1 | M (0.5-1d) | 3 | Bundles 1-4 |
| 6: P3 Structural | P3 | L (4-6d) | 10 | Bundles 4+5 |
| **Total** | | **~8-12 days** | **33** | |
