# BMAD Alignment Fix Sprint — TODO

**Source of truth:** `SPEC.md` (1,099 lines)
**Branch:** `develop` → `main` on `/ship`
**Total subtasks:** 33 across 6 bundles

---

## Phase 1: Foundation (Parallel Tracks)

---

## Bundle 1: CSV → YAML Migration [P0] — Effort: M (1-2 days)

- [x] 1.1 Define module.yaml schema
  - Acceptance: Schema validates against all 5 CSVs with zero data loss; 13 CSV columns mapped to YAML fields
  - Verify: `python3 scripts/archive/csv_to_yaml_converter.py --dry-run`
  - Files: `scripts/archive/csv_to_yaml_converter.py` (new)

- [x] 1.2 Convert all 5 module-help.csv files to module.yaml
  - Acceptance: All 5 module.yaml files created; row counts match CSVs; yaml.safe_load() succeeds on each
  - Verify: `for f in skills/*/module.yaml skills/bmad-init/core/module.yaml; do python -c "import yaml; yaml.safe_load(open('$f'))" && echo "OK $f" || echo "FAIL $f"; done`
  - Files: `skills/bmad-init/core/module.yaml`, `skills/bmad-bmm/module.yaml`, `skills/bmad-tea/module.yaml`, `skills/bmad-cis/module.yaml`, `skills/bmad-bmb/module.yaml`
  - Note: Init CSV is special — entries merged into appropriate module.yaml files

- [x] 1.3 Rewrite routing extension for YAML
  - Acceptance: Zero import csv or csv. references; yaml.safe_load() used; routing manifest output byte-identical to CSV version; mtime caching works
  - Verify: `grep -r 'import csv' extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py && echo 'FAIL' || echo 'OK'
  - Files: `extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py` (rewrite)

- [x] 1.4 Update and add tests for YAML
  - Acceptance: All existing routing tests pass with YAML; new YAML-specific tests cover parsing, caching, error handling; test count >= 300
  - Verify: `python -m pytest tests/test_extension_80.py tests/test_core_yaml_schema.py tests/test_yaml_routing.py tests/test_migration_csv_to_yaml.py -v`
  - Files: `tests/test_extension_80.py` (update), `tests/test_core_csv_schema.py` → `tests/test_core_yaml_schema.py` (rename), `tests/test_yaml_routing.py` (new), `tests/test_migration_csv_to_yaml.py` (new)
- [x] 1.5 Delete CSV files and clean up references
  - Acceptance: grep -r 'module-help' returns zero results; no import csv in routing extension
  - Verify: `grep -r 'module-help' . --include='*.py' --include='*.md' --include='*.sh'`
  - Files: DELETE `skills/bmad-init/module-help.csv`, `skills/bmad-bmm/module-help.csv`, `skills/bmad-tea/module-help.csv`, `skills/bmad-cis/module-help.csv`, `skills/bmad-bmb/module-help.csv`

- [x] 1.6 Write ADR-0010 and supersede ADR-0001
  - Acceptance: ADR-0010 exists with status Accepted; ADR-0001 header updated to Status: Superseded by ADR-0010
  - Verify: `head -5 docs/adr/0010-yaml-canonical-routing.md && head -5 docs/adr/0001-csv-canonical-routing.md`
  - Files: `docs/adr/0010-yaml-canonical-routing.md` (new), `docs/adr/0001-csv-canonical-routing.md` (update header)

### Checkpoint A: After Bundle 1
```
python -m pytest tests/test_extension_80.py -v
for f in skills/*/module.yaml skills/bmad-init/core/module.yaml; do
  python -c "import yaml; yaml.safe_load(open('$f'))" && echo "OK $f" || echo "FAIL $f"
done
```

---

## Bundle 3: CIS Persona Removal [P1] — Effort: S-M (0.5-1 day)

- [x] 3.1 Update CIS agent.yaml files — replace named personas with upstream generic titles
  - Acceptance: No CIS agent.yaml contains named personas; titles match upstream generic titles; icons updated (design-thinking gets target, presentation gets framed-picture)
  - Verify: `grep -r 'Victor\|Dr. Quinn\|Maya\|Carson\|Sophia\|Caravaggio' agents/bmad-*/ || echo 'OK: All CIS personas removed'`
  - Files: `agents/bmad-innovation/agent.yaml`, `agents/bmad-problem-solver/agent.yaml`, `agents/bmad-design-thinking/agent.yaml`, `agents/bmad-brainstorming-coach/agent.yaml`, `agents/bmad-storyteller/agent.yaml`, `agents/bmad-presentation/agent.yaml`

- [x] 3.2 Update CIS prompt files — remove persona narrative, use functional descriptions
  - Acceptance: All 6 CIS agents role.md, specifics.md, communication_additions.md updated to generic functional style
  - Verify: `grep -r 'Victor\|Dr. Quinn\|Maya\|Carson\|Sophia\|Caravaggio' agents/bmad-innovation/ agents/bmad-problem-solver/ agents/bmad-design-thinking/ agents/bmad-brainstorming-coach/ agents/bmad-storyteller/ agents/bmad-presentation/ || echo 'OK'`
  - Files: 6x `agents/bmad-{agent}/prompts/agent.system.main.role.md`, 6x `agents/bmad-{agent}/prompts/agent.system.main.specifics.md`, 6x `agents/bmad-{agent}/prompts/agent.system.main.communication_additions.md`

- [x] 3.3 Update CIS agent references in other files
  - Acceptance: CIS agents reference files, module.yaml, teams, seed-knowledge all updated; no persona name leaks
  - Verify: `grep -r 'Victor\|Dr. Quinn\|Maya\|Carson\|Sophia\|Caravaggio' skills/bmad-cis/ skills/bmad-init/seed-knowledge/ || echo 'OK'`
  - Files: `skills/bmad-cis/agents/*.md`, `skills/bmad-cis/module.yaml`, `skills/bmad-cis/teams/`, `skills/bmad-init/seed-knowledge/`

---

## Phase 2: Consolidation + Fixes

---

## Bundle 2: Agent Consolidation [P1] — Effort: M (1 day)

- [x] 2.1 Remove bmad-sm agent directory
  - Acceptance: agents/bmad-sm/ does not exist; Amelia customize.toml includes SP, SS, CS, ER menus; module.yaml updated skill:sm to skill:dev
  - Verify: `ls agents/bmad-sm 2>&1 | grep 'No such file'`
  - Files: DELETE `agents/bmad-sm/`, UPDATE `agents/bmad-dev/customize.toml`, UPDATE `skills/bmad-bmm/module.yaml`, UPDATE `agents/bmad-dev/prompts/agent.system.main.specifics.md`, UPDATE `helpers/bmad_status_core.py`

- [x] 2.2 Remove bmad-qa agent directory
  - Acceptance: agents/bmad-qa/ does not exist; Amelia customize.toml includes QA menu; test-tube icon collision resolved
  - Verify: `ls agents/bmad-qa 2>&1 | grep 'No such file'`
  - Files: DELETE `agents/bmad-qa/`, UPDATE `agents/bmad-dev/customize.toml`, UPDATE `skills/bmad-bmm/module.yaml`, UPDATE `helpers/bmad_status_core.py`

- [x] 2.3 Remove bmad-quick-dev agent directory
  - Acceptance: agents/bmad-quick-dev/ does not exist; Amelia customize.toml includes QD menu; menu-code QQ changed to QD
  - Verify: `ls agents/bmad-quick-dev 2>&1 | grep 'No such file' && grep -r 'QQ' skills/bmad-bmm/module.yaml && echo 'FAIL: QQ still present' || echo 'OK: QQ removed'`
  - Files: DELETE `agents/bmad-quick-dev/`, UPDATE `agents/bmad-dev/customize.toml`, UPDATE `skills/bmad-bmm/module.yaml`, UPDATE `helpers/bmad_status_core.py`

- [x] 2.4 Add missing menus to Amelia customize.toml
  - Acceptance: Amelia customize.toml has SP, SS, VS, CS, DS, CR, QA, CC, ER, CK, QD, QS menus (12 total)
  - Verify: `grep -c '\[\[agent\.menu\]\]' agents/bmad-dev/customize.toml`
  - Files: `agents/bmad-dev/customize.toml`

- [x] 2.5 Update bmad-master role.md — remove static agent table
  - Acceptance: No static 19-row agent table; replaced with condensed routing guidance using dynamic list; agent count references updated to 18
  - Verify: `grep -c '|.*|.*|' agents/bmad-master/prompts/agent.system.main.role.md`
  - Files: `agents/bmad-master/prompts/agent.system.main.role.md`

- [x] 2.6 Update agent roster in knowledge/config files
  - Acceptance: bmad_status_core.py AGENT_NAMES has no bmad-sm, bmad-qa, bmad-quick-dev; teams updated; sm.md removed or merged
  - Verify: `grep -E 'bmad-sm|bmad-qa|bmad-quick-dev' helpers/bmad_status_core.py && echo 'FAIL' || echo 'OK'`
  - Files: `helpers/bmad_status_core.py`, `skills/bmad-bmm/agents/sm.md`, teams CSV files

### Checkpoint B: After Bundle 2
```
ls agents/bmad-sm agents/bmad-qa agents/bmad-quick-dev 2>&1 | grep 'No such file'
python -m pytest tests/ -v
```

---

## Bundle 4: Quick Fixes [P1/P2] — Effort: S (2-4 hours)

- [x] 4.1 Fix Morgan icon (construction → package)
  - Acceptance: agents/bmad-module-builder/agent.yaml icon is package; construction is Winston-only
  - Verify: `grep 'package-icon' agents/bmad-module-builder/agent.yaml`
  - Files: `agents/bmad-module-builder/agent.yaml`, possibly `agents/bmad-module-builder/prompts/agent.system.main.role.md`

- [x] 4.2 Fix Sally communication style (painter to filmmaker metaphor)
  - Acceptance: Sally role.md uses filmmaker pitching the scene metaphor
  - Verify: `grep -i 'filmmaker' agents/bmad-ux-designer/prompts/agent.system.main.role.md`
  - Files: `agents/bmad-ux-designer/prompts/agent.system.main.role.md`, possibly `agents/bmad-ux-designer/agent.yaml`

- [x] 4.3 Add US menu to Paige customize.toml
  - Acceptance: Paige customize.toml includes US (Update Standards) menu code
  - Verify: `grep 'code = "US"' agents/bmad-tech-writer/customize.toml`
  - Files: `agents/bmad-tech-writer/customize.toml`

- [x] 4.4 Add _bmad/custom/ directory creation to init script
  - Acceptance: Init script creates _bmad/custom/ directory; idempotent
  - Verify: `bash skills/bmad-init/scripts/bmad-init.sh /tmp/test-bmad-project && ls -la /tmp/test-bmad-project/.a0proj/_bmad/custom/`
  - Files: `skills/bmad-init/scripts/bmad-init.sh`

- [x] 4.5 Document QA/VS menu code collisions as intentional module-scoping
  - Acceptance: Comments in module.yaml documenting intentional QA/VS code duplication; routing manifest correctly filters by module
  - Verify: `grep -A2 'Module-scoped' skills/bmad-bmm/module.yaml skills/bmad-bmb/module.yaml`
  - Files: `skills/bmad-bmm/module.yaml`, `skills/bmad-bmb/module.yaml`

### Checkpoint C: After Bundles 2-4
```
python -m pytest tests/ -v
bash skills/bmad-init/scripts/bmad-init.sh /tmp/test-bmad-project
ls -la /tmp/test-bmad-project/.a0proj/_bmad/custom/
```

---

## Phase 3: Test Updates

---

## Bundle 5: Test Updates and Final Verification [P1] — Effort: M (0.5-1 day)

- [ ] 5.1 Update existing tests for YAML
  - Acceptance: test_extension_80.py uses YAML fixtures; test_core_csv_schema.py renamed to test_core_yaml_schema.py; test_constants_consolidation.py updated; test_dead_code.py CSV checks removed
  - Verify: `python -m pytest tests/test_extension_80.py tests/test_core_yaml_schema.py tests/test_constants_consolidation.py tests/test_dead_code.py -v`
  - Files: `tests/test_extension_80.py`, `tests/test_core_csv_schema.py` → `tests/test_core_yaml_schema.py`, `tests/test_constants_consolidation.py`, `tests/test_dead_code.py`

- [ ] 5.2 Add new tests (test_yaml_routing, test_agent_consolidation, test_cis_personas)
  - Acceptance: test_yaml_routing.py covers YAML parsing, phase filtering, menu lookup, mtime caching; test_agent_consolidation.py covers SM/QA/QD removal, Amelia menus, QD code; test_cis_personas.py covers no named personas, generic titles, no icon collisions
  - Verify: `python -m pytest tests/test_yaml_routing.py tests/test_agent_consolidation.py tests/test_cis_personas.py -v`
  - Files: `tests/test_yaml_routing.py` (new), `tests/test_agent_consolidation.py` (new), `tests/test_cis_personas.py` (new)

- [ ] 5.3 Full integration test — init script, routing manifest, A2A live test
  - Acceptance: bmad-init.sh on temp dir produces correct state; routing manifest generates correctly from YAML; phase transitions work; A2A live test on VPS passes; test count >= 300; flake8 clean
  - Verify: `python -m pytest tests/ -v && python -m flake8 api/ helpers/ extensions/ --max-line-length 100`
  - Files: N/A (verification only, deploying to VPS)

### Checkpoint D: After Bundle 5
```
python -m pytest tests/ -v  # count >= 300, all pass
python -m flake8 api/ helpers/ extensions/ --max-line-length 100
```

---

## Phase 4: P3 Structural Alignment

---

## Bundle 6: P3 Structural Alignment [P3] — Effort: L (4-6 days)

### 6A: 8-Step Activation Sequence

- [x] 6.1 Rewrite bmad-agent-shared.md activation section (8-step sequence)
  - Acceptance: Activation section lists all 8 steps in order; steps 1,2,5,7 are new; steps 3,4,6,8 preserved from current
  - Verify: `grep -c '### Step' prompts/bmad-agent-shared.md` (should show 8 activation steps)
  - Files: `prompts/bmad-agent-shared.md`

- [x] 6.2 Add resolve_customization first-call instructions per agent
  - Acceptance: Shared prompt instructs agent to run resolve_customization.py as first tool call; template includes skill-root variable
  - Verify: `grep 'resolve_customization' prompts/bmad-agent-shared.md`
  - Files: `prompts/bmad-agent-shared.md`

- [x] 6.3 Add persistent_facts processing instructions
  - Acceptance: Shared prompt includes step for processing persistent_facts array; file: prefix handling documented with glob support; literal facts adopted as context
  - Verify: `grep -A5 'persistent_facts' prompts/bmad-agent-shared.md`
  - Files: `prompts/bmad-agent-shared.md`

- [x] 6.4 Add prepend/append hooks processing instructions
  - Acceptance: Prepend step processing before persona adoption; append step processing after greeting before menu; empty arrays result in no-op
  - Verify: `grep 'activation_steps_prepend\|activation_steps_append' prompts/bmad-agent-shared.md`
  - Files: `prompts/bmad-agent-shared.md`

### 6B: project-context.md Loading

- [x] 6.5 Standardize project-context.md loading in implementation workflows
  - Acceptance: All 8 implementation workflow step-01 files include project-context.md pre-step; pre-step is idempotent
  - Verify: `grep -l 'project-context' skills/bmad-bmm/workflows/*/steps/step-01-init.md | wc -l`
  - Files: `skills/bmad-bmm/workflows/dev-story/steps/step-01-init.md`, `skills/bmad-bmm/workflows/create-story/steps/step-01-init.md`, `skills/bmad-bmm/workflows/code-review/steps/step-01-init.md`, `skills/bmad-bmm/workflows/sprint-planning/steps/step-01-init.md`, `skills/bmad-bmm/workflows/correct-course/steps/step-01-init.md`, `skills/bmad-bmm/workflows/quick-dev/steps/step-01-init.md`, `skills/bmad-bmm/workflows/quick-spec/steps/step-01-init.md`, `skills/bmad-bmm/workflows/create-architecture/steps/step-01-init.md`

### 6C: File-Based Sidecar Memory

- [x] 6.6 Add file-based sidecar memory directories to init script
  - Acceptance: Init script creates _bmad/_memory/ with 16 agent sidecar directories; each has memories.md; idempotent
  - Verify: `bash skills/bmad-init/scripts/bmad-init.sh /tmp/test-bmad-project && ls /tmp/test-bmad-project/.a0proj/_bmad/_memory/ | wc -l`
  - Files: `skills/bmad-init/scripts/bmad-init.sh`

- [x] 6.7 Add sidecar loading to activation sequence
  - Acceptance: Shared prompt includes sidecar loading between facts (step 5) and greeting (step 6); agent reads all .md files from sidecar directory; missing files handled gracefully
  - Verify: `grep -A5 'sidecar' prompts/bmad-agent-shared.md`
  - Files: `prompts/bmad-agent-shared.md`

- [x] 6.8 Add sidecar writing instructions to agent prompts
  - Acceptance: Shared prompt includes sidecar writing instructions; triggers at natural breakpoints; format documented (markdown with date/topic headers); agents append not overwrite
  - Verify: `grep -A5 'Sidecar Memory Writing' prompts/bmad-agent-shared.md`
  - Files: `prompts/bmad-agent-shared.md`

- [x] 6.9 Create sidecar import skill for upstream migration
  - Acceptance: skills/bmad-sidecar-import/SKILL.md exists; import script copies .md files from upstream sidecar directories; idempotent
  - Verify: `ls skills/bmad-sidecar-import/SKILL.md skills/bmad-sidecar-import/scripts/import-sidecars.sh`
  - Files: `skills/bmad-sidecar-import/SKILL.md` (new), `skills/bmad-sidecar-import/scripts/import-sidecars.sh` (new)

### 6D: P3 Tests

- [x] 6.10 Add tests for activation sequence, sidecar, project-context loading
  - Acceptance: test_activation_sequence.py verifies 8 steps, resolve_customization, persistent_facts, prepend/append, sidecar loading; test_sidecar_memory.py verifies 16 directories, memories.md, readable markdown; test_project_context_loading.py verifies persistent_facts step, workflow pre-steps, customize.toml references; test count >= 310
  - Verify: `python -m pytest tests/test_activation_sequence.py tests/test_sidecar_memory.py tests/test_project_context_loading.py -v`
  - Files: `tests/test_activation_sequence.py` (new), `tests/test_sidecar_memory.py` (new), `tests/test_project_context_loading.py` (new)

### Checkpoint E: After Bundle 6
```
python -m pytest tests/ -v  # count >= 310, all pass
bash skills/bmad-init/scripts/bmad-init.sh /tmp/test-bmad-project
ls -la /tmp/test-bmad-project/.a0proj/_bmad/custom/
ls -la /tmp/test-bmad-project/.a0proj/_bmad/_memory/
grep -c '### Step' prompts/bmad-agent-shared.md  # should be 8+
```

---

## Final Gate: A2A Live Test + Deploy

- [ ] Deploy to VPS testing instance
  - Verify: `ssh -i /a0/usr/.ssh/id_ed25519 -o StrictHostKeyChecking=no root@162.19.152.199 'docker exec agent-zero-testing bash -c "cd /a0/usr/projects/a0_bmad_method && git pull origin develop"'`

- [ ] Merge develop to main (/ship)
  - Verify: All 33 subtasks checked off; test count >= 310; A2A live test passes

---

## Summary

| Bundle | Tasks | Status |
|--------|-------|--------|
| 1: CSV to YAML [P0] | 1.1-1.6 (6) | [] |
| 2: Agent Consolidation [P1] | 2.1-2.6 (6) | [] |
| 3: CIS Persona Removal [P1] | 3.1-3.3 (3) | [] |
| 4: Quick Fixes [P1/P2] | 4.1-4.5 (5) | [] |
| 5: Test Updates [P1] | 5.1-5.3 (3) | [] |
| 6: P3 Structural [P3] | 6.1-6.10 (10) | [] |
| **Total** | **33 subtasks** | |
