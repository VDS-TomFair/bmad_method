# TODO: BMAD Method Plugin — Phase F (Upstream v6.6.0 Sync) — 12 tasks

Phases A–D: COMPLETE (35/35 tasks done)

---

## Phase F — P0: Critical Workflow Step Sync

- [x] **F-P0-1**: Fix pre-checked architecture checklist in step-07-validation.md (M) ✅
  - Change all `[x]` → `[ ]`, remove ✅ emoji from headers, add 3-tier conditional status
  - Verify: Step Complete section preserved at file bottom
  - Verify: `python -m pytest tests/ -v` all green

- [x] **F-P0-2**: Add file churn detection to epic design in step-02-design-epics.md (M) ✅
  - Add Principle #6 (Implementation Efficiency), rename Step A, add Step C (File Overlap Review), add examples
  - `skills/bmad-bmm/workflows/3-solutioning/create-epics-and-stories/steps/step-02-design-epics.md`
  - Verify: `grep 'Implementation Efficiency' .../step-02-design-epics.md` → found
  - Verify: `grep 'Review for File Overlap' .../step-02-design-epics.md` → found
  - Verify: YAML frontmatter + Step Complete section preserved
  - Verify: `python -m pytest tests/ -v` all green

- [x] **F-P0-3**: Add file churn check + HALT + on_complete hook in step-04-final-validation.md (M) ✅
  - Add File Churn Check subsection, HALT instruction, On Complete hook (resolve_customization.py)
  - On Complete path adapted: `$A0PROJ/_bmad/scripts/resolve_customization.py`
  - `skills/bmad-bmm/workflows/3-solutioning/create-epics-and-stories/steps/step-04-final-validation.md`
  - Verify: `grep 'File Churn Check' .../step-04-final-validation.md` → found
  - Verify: `grep 'HALT' .../step-04-final-validation.md` → found
  - Verify: `grep 'resolve_customization' .../step-04-final-validation.md` → found
  - Verify: Workflow Completion — State Write section + YAML frontmatter preserved
  - Verify: `python -m pytest tests/ -v` all green

### P0 Checkpoint

- [ ] All 3 workflow step files synced with upstream v6.6.0 content
- [ ] All A0-specific sections preserved (YAML frontmatter, Step Complete, State Write)
- [ ] `python -m pytest tests/ -v` → all 200+ tests green

---

## Phase F — P1: Config Migration + Customization

- [x] **F-P1-1**: Move `project_name` to core config (XS) ✅
  - Add `project_name: ""` to core config, update version 6.0.3 → 6.6.0
  - `skills/bmad-init/core/config.yaml`
  - Verify: `grep 'project_name' skills/bmad-init/core/config.yaml` → found
  - Verify: `grep 'Version: 6.6.0' skills/bmad-init/core/config.yaml` → found

- [x] **F-P1-2**: Remove `project_name` from bmm config (XS) ✅
  - Remove `project_name: ""`, update version 6.0.3 → 6.6.0
  - `skills/bmad-bmm/config.yaml`
  - Verify: `grep 'project_name' skills/bmad-bmm/config.yaml` → empty
  - Verify: `python -m pytest tests/ -v` all green

- [x] **F-P1-3**: Update remaining config versions to 6.6.0 (XS) ✅
  - Update version headers in cis, tea, bmb configs
  - `skills/bmad-cis/config.yaml`, `skills/bmad-tea/config.yaml`, `skills/bmad-bmb/config.yaml`
  - Verify: `grep -r 'Version: 6.0.3' skills/*/config.yaml` → empty
  - Verify: `grep -r 'Version: 6.6.0' skills/*/config.yaml` → 5 hits

- [x] **F-P1-4**: Verify CSV row coverage post-migration (S) ✅
  - Quick sanity check — confirmed upstream: no CSV rows reference `project_name`
  - All 5 `skills/*/module-help.csv` files
  - Verify: `grep -r 'project_name' skills/*/module-help.csv` → empty
  - Verify: `python -m pytest tests/test_extension_80.py tests/test_core_csv_schema.py -v` green

- [x] **F-P1-5**: Include `resolve_customization.py` in plugin (S) ✅
  - Copy from upstream `src/scripts/resolve_customization.py`, adapt paths `{project-root}/_bmad/` → `$A0PROJ/_bmad/`
  - NEW: `$A0PROJ/_bmad/scripts/resolve_customization.py`
  - Upstream source: `.a0proj/upstream/BMAD-METHOD/src/scripts/resolve_customization.py`
  - Verify: `python3 $A0PROJ/_bmad/scripts/resolve_customization.py --help` runs without error
  - Verify: All path references adapted to A0 conventions
  - Verify: `python -m pytest tests/ -v` all green

- [x] **F-P1-6**: Create bmad-customize skill (M) ✅
  - Port upstream core skill with A0 path adaptations
  - Port: SKILL.md, `list_customizable_skills.py`, test, 31 customize.toml files
  - Upstream: `.a0proj/upstream/BMAD-METHOD/src/core-skills/bmad-customize/`
  - Verify: bmad-customize skill loads via SKILL.md
  - Verify: `list_customizable_skills.py` runs and discovers customizable skills
  - Verify: All customize.toml files ported and valid TOML
  - Verify: `python -m pytest tests/ -v` all green

### P1 Checkpoint

- [ ] `project_name` in core config only (not in bmm)
- [ ] All 5 config.yaml versions read 6.6.0
- [ ] CSV routing unaffected
- [ ] `resolve_customization.py` included at `$A0PROJ/_bmad/scripts/`
- [ ] `bmad-customize` skill created with all supporting files
- [ ] `python -m pytest tests/ -v` → all green

---

## Phase F — P2: Polish

- [x] **F-P2-1**: Update CHANGELOG (XS) ✅
  - Add `[1.1.0]` section with Phase F entries
  - `CHANGELOG.md`
  - Verify: `grep '\[1.1.0\]' CHANGELOG.md` → found
  - Verify: All Phase F task IDs referenced

- [x] **F-P2-2**: Plugin version bump to 1.1.0 (XS) ✅
  - Update `version: 1.0.8` → `version: 1.1.0`
  - `plugin.yaml`
  - Verify: `grep 'version: 1.1.0' plugin.yaml` → found
  - Verify: `python -m pytest tests/ -v` all green

### P2 Checkpoint (ready for /ship)

- [ ] CHANGELOG updated
- [ ] Plugin version 1.1.0
- [ ] All 20 BMAD agents functional on VPS testing instance
- [ ] BMAD initializable from any path
- [ ] Tagged v1.1.0; merged to main
