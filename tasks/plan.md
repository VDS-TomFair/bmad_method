# Implementation Plan: BMAD Method A0 Alignment (Phases A–D)

## Overview

Migrate BMAD Method plugin (v1.0.8) from partially-aligned state to fully A0-idiomatic implementation across four phases. Phase A unblocks all subsequent work; phases B–D build on each other sequentially.

**Total tasks:** 35 (A: 7 · B: 11 · C: 8 · D: 9)  
**Branch:** `develop` → `main` on /ship  
**Test command:** `cd /a0/usr/projects/a0_bmad_method && python -m pytest tests/ -v`

---

## Architecture Decisions

- **Single source of truth for shared state:** `helpers/bmad_status_core.py` is the canonical module. `api/_bmad_status.py` uses importlib to load it. `scripts/bmad-status.py` must be updated to use the same importlib pattern once `scripts/bmad_status_core.py` is deleted (A2 scope).
- **CSV stays, SKILL.md gets triggers:** `module-help.csv` remains the routing source. SKILL.md carries only `name`, `description`, `trigger_patterns` for A0 discoverability (Phase C).
- **Mtime fallback — split treatment per file:** `api/_bmad_status.py` and `_80_bmad_routing_manifest.py` — mtime scan hard-removed, both return `None`. `skills/bmad-init/scripts/bmad-status.py` — gated behind `BMAD_DEV_MODE` env var with `log.warning()`. All three return `None` when context absent and `BMAD_DEV_MODE` unset. (A3 scope)
- **Regex correctness:** `_PHASE_RE` and `_ARTIFACT_RE` must be `re.MULTILINE | re.IGNORECASE`; output always `.lower()` (A2).
- **Constants live once:** `AGENT_NAMES`, `PHASE_ACTIONS`, `PHASE_BUCKET_PREFIXES` move to `helpers/bmad_status_core.py` in Phase B, imported by all three consumers.
- **`{{ include }}` mechanism confirmed:** `{{ include "filename.md" }}` fully works in A0 agent prompt contexts via `helpers/files.py:process_includes()`. D3 approach committed — 7 shared sections extracted into `agents/_shared/prompts/bmad-agent-shared.md`; each non-master agent's specifics file becomes: role section + `{{ include }}` + available-skills table. `bmad-master` excluded.
- **CSV migration scope clarified:** `skills/bmad-init/core/module-help.csv` is the sole file on the old schema. All other 4 skill CSVs already use upstream 13-column schema. Task C0 migrates this outlier before C1 removes dual-read compatibility code from routing extension.

---

## Dependency Graph (ASCII)

```
[A1: init.sh paths]──────────────────────────────────────────┐
[A2: read_state() core] → [A3: mtime gate] → [A5: log warn]   │
[A4: HTML fix]                                                 │
[A6: None-guard _spec]                                         │
[A7: tests/test_bmad_status_core.py]                           │
         │                                                     │
         ▼                                                     ▼
[CHECKPOINT A] ────────────────────────────────────────────────┘
         │
    ┌────┴──────────────────────────────────────────────┐
    │ B1: plugin.yaml          B3: SKILL.md triggers    │
    │ B2: promptinclude ← A1   B4: dead constant        │
    │ B5: store.js orphan      B6: bash hardening ← A1  │
    │ B7: constants to core ← A2                        │
    │ B8: dead imports ← A6    B9: mtime caching ← A3   │
    │ B10: git/VPS setup       B11: test_bmad_init_sh   │
    └──────────────────────┬────────────────────────────┘
                           │
                  [CHECKPOINT B]
                           │
          ┌─────────────────┴──────────────────────────────┐
          │ C0: migrate bmad-init/core/module-help.csv (S) │
          │ C1: CSV column align (4 files) ← C0            │
          │ C2: trigger_patterns bmad-bmm (~20 files)       │
          │ C3: trigger_patterns bmad-cis (~5 files)        │
          │ C4: trigger_patterns bmad-tea (~9 files)        │
          │ C5: trigger_patterns bmad-bmb (~5 files)        │
          │ C6: trigger_patterns core (~3 files)            │
          │ C7: verify + tests ← C0,C1,C2,C3,C4,C5,C6     │
          └──────────────────┬──────────────────────────────┘
                             │
                    [CHECKPOINT C]
                             │
          ┌──────────────────┴──────────────────────────────┐
          │ D1: bmad.methodology.shared.md (new)            │
          │ D2: audit scope of shared fragment              │
          │ D3: update 19 main.specifics.md ← D1,D2        │
          │ D4: remove static table bmad-master ← D3       │
          │ D5: _recommend() caching                       │
          │ D6: dashboard error display                    │
          │ D7: project-context.md stub in init.sh         │
          │ D8: party mode (solo) implementation           │
          │ D9: a0-review-plugin audit                     │
          └──────────────────┬──────────────────────────────┘
                             │
                    [CHECKPOINT D = VERIFY ready]
```

---

## Phase A — Critical Bug Fixes

**Gate: All Phase A tasks must pass before any Phase B work begins.**

---

### Task A1: Fix hardcoded `/a0/usr/projects/` paths in `bmad-init.sh` [Size: S]

Phase: A  
Description: Lines 40–44 of `bmad-init.sh` embed `/a0/usr/projects/$PROJECT_NAME` literals into the generated `01-bmad-config.md`. This breaks artifact detection for any project not under that path. Replace all five path table entries with `$A0PROJ`-derived variables. Also add `set -euo pipefail` (bash strict mode, partially addressed in B6 but `pipefail` needed now for safety). Warnings to stderr.

Acceptance criteria:
- [ ] `bash skills/bmad-init/scripts/bmad-init.sh /tmp/test-a1` succeeds
- [ ] `grep '/a0/usr/projects' /tmp/test-a1/.a0proj/instructions/01-bmad-config.md` returns empty
- [ ] Generated config contains `/tmp/test-a1/.a0proj/` in all five path rows
- [ ] `bash -n skills/bmad-init/scripts/bmad-init.sh` exits 0

Verification:
- [ ] `bash skills/bmad-init/scripts/bmad-init.sh /tmp/test-a1 && grep 'a0/usr/projects' /tmp/test-a1/.a0proj/instructions/01-bmad-config.md | wc -l | grep -q '^0$'`

Dependencies: None  
Files touched: `skills/bmad-init/scripts/bmad-init.sh`

---

### Task A2: Consolidate `read_state()` into `helpers/bmad_status_core.py` [Size: M]

Phase: A  
Description: The current `helpers/bmad_status_core.py` `read_state()` uses bare `re.search()` without `re.MULTILINE` or `re.IGNORECASE`, doesn't lowercase the phase output, and has no `logging` import. Simultaneously, `skills/bmad-init/scripts/bmad_status_core.py` is a second copy imported by `bmad-status.py`. This task: (1) fixes the `helpers/` version with module-level compiled `_PHASE_RE`/`_ARTIFACT_RE` using `re.MULTILINE | re.IGNORECASE` and lowercased output; (2) adds `import logging` + `log = logging.getLogger(__name__)`; (3) deletes `scripts/bmad_status_core.py`; (4) updates `bmad-status.py` to use importlib to load from `helpers/` (matching the pattern already used in `api/_bmad_status.py`); (5) updates `_80_bmad_routing_manifest.py` to call `read_state()` from helpers instead of its inline phase-parsing loop (lines 377–382).

Acceptance criteria:
- [ ] `helpers/bmad_status_core.py` has `_PHASE_RE` and `_ARTIFACT_RE` compiled with `re.MULTILINE | re.IGNORECASE`
- [ ] `read_state()` returns lowercase `phase` always
- [ ] `skills/bmad-init/scripts/bmad_status_core.py` deleted
- [ ] `bmad-status.py` uses importlib to load helpers version (no `from bmad_status_core import`)
- [ ] Routing extension calls `read_state()` for phase, not inline loop
- [ ] `pytest tests/test_bmad_status_core.py -v` all green (new tests in A7)

Verification:
- [ ] `python -m pytest tests/ -v`
- [ ] `ls skills/bmad-init/scripts/bmad_status_core.py 2>&1 | grep 'No such file'`

Dependencies: None  
Files touched: `helpers/bmad_status_core.py`, `skills/bmad-init/scripts/bmad_status_core.py` (delete), `skills/bmad-init/scripts/bmad-status.py`, `extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py`

---

### Task A3: Remove/gate cross-project mtime fallback — split treatment [Size: M]

Phase: A  
Description: Three files contain production fallback logic that scans `/a0/usr/projects/` causing cross-project state leakage. **OQ-A3 resolved — per-file treatment:** `api/_bmad_status.py` Stage 3 mtime scan → **hard remove, return `None`**. `_80_bmad_routing_manifest.py` fallback → **hard remove, return `None`**. `skills/bmad-init/scripts/bmad-status.py` → **gate behind `BMAD_DEV_MODE` env var** with `log.warning()`. All callers must gracefully handle `None` return.

Acceptance criteria:
- [ ] `_80_bmad_routing_manifest.py:_resolve_state_file()` — mtime scan entirely removed; returns `None` when context absent; no `BMAD_DEV_MODE` gate in this file
- [ ] `api/_bmad_status.py:_resolve_project_root()` — Stage 3 mtime scan entirely removed; returns `None` when context absent; no `BMAD_DEV_MODE` gate in this file
- [ ] `skills/bmad-init/scripts/bmad-status.py:_resolve_project_root()` — mtime fallback gated behind `os.environ.get("BMAD_DEV_MODE")`; emits `log.warning()` when activated
- [ ] When context is absent and `BMAD_DEV_MODE` unset, all three return `None`
- [ ] No bare `pass` in except blocks that hide fallback failures

Verification:
- [ ] `python -m pytest tests/ -v`
- [ ] `grep -n 'a0/usr/projects' extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py api/_bmad_status.py` — zero hits (hard removed)

Dependencies: A2 (for updated `_resolve_state_file` in routing extension)  
Files touched: `extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py`, `api/_bmad_status.py`, `skills/bmad-init/scripts/bmad-status.py`

---

### Task A4: Fix malformed HTML in `bmad-dashboard.html` [Size: XS]

Phase: A  
Description: Lines 255–263 of `bmad-dashboard.html` contain 4 stray `</div>` and 1 stray `</template>` tags that are not matched by any opening tag. Remove them and verify with `tidy`.

Acceptance criteria:
- [ ] `tidy -e webui/bmad-dashboard.html 2>&1 | grep -c '^Error' | grep -q '^0$'`
- [ ] Dashboard renders without console errors in browser

Verification:
- [ ] `tidy -e webui/bmad-dashboard.html 2>&1 | grep -E '^(Error|Warning)' | head -20`

Dependencies: None  
Files touched: `webui/bmad-dashboard.html`

---

### Task A5: Add `log.warning()` to all bare `except` blocks in routing extension [Size: XS]

Phase: A  
Description: `_80_bmad_routing_manifest.py` line 423 has a bare `except: pass` at the outermost scope of `execute()`. `_build_staleness_warnings()` (line 329) also has bare `except: pass`. Add `import logging`, `log = logging.getLogger(__name__)`, and replace each bare `pass` with `log.warning("BMAD routing: %s", traceback.format_exc())`. Import `traceback` at top. Do not re-raise.

Acceptance criteria:
- [ ] Top-level `except` in `execute()` calls `log.warning()` with traceback
- [ ] `_build_staleness_warnings()` outer `except` calls `log.warning()`
- [ ] Inner per-item `except: continue` blocks in `_collect_routing_rows()` and `_scan_artifact_existence()` may remain silent (graceful degradation)
- [ ] No bare `except: pass` at top-level scope

Verification:
- [ ] `grep -n 'except' extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py`
- [ ] `python -m pytest tests/ -v`

Dependencies: A2 (logging already imported after A2)  
Files touched: `extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py`

---

### Task A6: None-guard on `spec_from_file_location` in `api/_bmad_status.py` [Size: XS]

Phase: A  
Description: Lines 12–14 of `api/_bmad_status.py` call `_spec.loader.exec_module(_core_mod)` without checking if `_spec` is `None`. If `spec_from_file_location()` fails (missing file, import error), this raises `AttributeError` on `None`. Add: `if _spec is None: raise ImportError(f"Cannot load bmad_status_core from {_core_path}")`.

Acceptance criteria:
- [ ] Line after `_spec = _ilu.spec_from_file_location(...)` has explicit `None` check
- [ ] `python -c "from api._bmad_status import BmadStatus"` succeeds (or raises ImportError with clear message)

Verification:
- [ ] `python -m pytest tests/ -v`
- [ ] Code review: `grep -n 'if _spec' api/_bmad_status.py`

Dependencies: None  
Files touched: `api/_bmad_status.py`

---

### Task A7: Write `tests/test_bmad_status_core.py` [Size: S]

Phase: A  
Description: New test file covering the canonical `read_state()` function in `helpers/bmad_status_core.py` with 6+ format variants as specified in SPEC.md: (1) `- Phase: ready` prefix; (2) no dash prefix; (3) extra whitespace; (4) uppercase `PHASE:`; (5) narrative match mid-text; (6) missing file returns `{phase: unknown, ...}`. Also test `AGENT_NAMES`, `PHASE_BUCKET_PREFIXES` exports exist, and `check_agents()` / `check_modules()` with fixture directories.

Acceptance criteria:
- [ ] `pytest tests/test_bmad_status_core.py -v` all green
- [ ] At least 6 `read_state()` scenario tests
- [ ] `read_state()` returns lowercase phase in all cases
- [ ] Missing-file case returns `{"phase": "unknown", "artifact": "none", "issues": []}`

Verification:
- [ ] `python -m pytest tests/test_bmad_status_core.py -v`

Dependencies: A2 (helpers/bmad_status_core.py fixed first)  
Files touched: `tests/test_bmad_status_core.py` (new)

---

## Checkpoint: Phase A

**Pass criteria (ALL must be green before Phase B starts):**
- [ ] `bash skills/bmad-init/scripts/bmad-init.sh /tmp/ckpt-a` → config has no `/a0/usr/projects/` literals
- [ ] `tidy -e webui/bmad-dashboard.html 2>&1 | grep -c '^Error'` → `0`
- [ ] `python -m pytest tests/ -v` → all green
- [ ] Routing extension phase value == API phase value for same state file
- [ ] No top-level silent exception swallow in routing extension (`grep 'except.*pass' _80_bmad_routing_manifest.py` → zero at outermost scope)
- [ ] `api/_bmad_status.py` line 12–14 has `if _spec is None` guard

**Fail criteria:** Any of the above failing blocks Phase B entirely.

---

## Phase B — Structural Alignment

**Prereq:** Phase A checkpoint passed.

---

### Task B1: Set `per_project_config: true` in `plugin.yaml` [Size: XS]

Phase: B  
Description: Change `per_project_config: false` to `per_project_config: true` on line 23 of `plugin.yaml`. This enables the per-project toggle UI in Agent Zero and is required for BMAD to operate as a project-scoped plugin.

Acceptance criteria:
- [ ] `grep 'per_project_config' plugin.yaml` → `per_project_config: true`

Verification:
- [ ] `grep 'per_project_config' plugin.yaml`

Dependencies: None  
Files touched: `plugin.yaml`

---

### Task B2: Move user prefs to `bmad-user-prefs.promptinclude.md` [Size: S]

Phase: B  
Description: The `User Settings` block in `01-bmad-config.md` (User Name, Language, Skill Level) should move to a separate `bmad-user-prefs.promptinclude.md` file auto-injected by A0's `_16_promptinclude` extension. Update `bmad-init.sh` to write this file (idempotent — no-clobber) and remove the settings block from the `01-bmad-config.md` template. The `.promptinclude.md` convention means A0 automatically injects it into all agent prompts.

Acceptance criteria:
- [ ] `bmad-init.sh` writes `$A0PROJ/instructions/bmad-user-prefs.promptinclude.md` on init
- [ ] `01-bmad-config.md` template no longer contains User Settings block
- [ ] File is no-clobber (existing user edits preserved on re-init)

Verification:
- [ ] `bash skills/bmad-init/scripts/bmad-init.sh /tmp/test-b2 && ls /tmp/test-b2/.a0proj/instructions/bmad-user-prefs.promptinclude.md`

Dependencies: A1 (init.sh already using $A0PROJ vars)  
Files touched: `skills/bmad-init/scripts/bmad-init.sh`

---

### Task B3: Add slash-style `trigger_patterns` to `skills/bmad-init/SKILL.md` [Size: XS]

Phase: B  
Description: Add `trigger_patterns` block to `skills/bmad-init/SKILL.md` with entries: `/bmad`, `/bmad-init`, `/bmad-help`, `/bmad-status`, `bmad init`, `bmad help`, `bmad status`. This makes the init skill discoverable via `skills_tool:search`.

Acceptance criteria:
- [ ] `skills/bmad-init/SKILL.md` has `trigger_patterns:` block with at least 4 slash-style entries

Verification:
- [ ] `grep -A 6 'trigger_patterns' skills/bmad-init/SKILL.md`

Dependencies: None  
Files touched: `skills/bmad-init/SKILL.md`

---

### Task B4: Remove dead `SKILL_TO_MODULE` constant from routing extension [Size: XS]

Phase: B  
Description: `SKILL_TO_MODULE` dict (lines 30–36 of `_80_bmad_routing_manifest.py`) is defined but never referenced. Delete it. Verify no other file imports it.

Acceptance criteria:
- [ ] `grep 'SKILL_TO_MODULE' extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py` → empty
- [ ] `python -m pytest tests/ -v` still green

Verification:
- [ ] `grep -r 'SKILL_TO_MODULE' .` → no hits

Dependencies: None  
Files touched: `extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py`

---

### Task B5: Fix orphaned `this.error` field in `bmad-dashboard-store.js` [Size: XS]

Phase: B  
Description: Line 19 of `bmad-dashboard-store.js` sets `this.error = ""` in `refresh()` but `error` is never declared in the store's initial state, and no template references it. Either: (a) add `error: ""` to the store state and wire up an error display template in the dashboard, or (b) remove the assignment. Per SPEC.md Phase D plan, error display is a Phase D task — for Phase B, simply remove the orphaned assignment or add the state key as a no-op stub.

Acceptance criteria:
- [ ] `this.error` in `refresh()` either removed or matched by a state property declaration
- [ ] No browser console errors related to `this.error`

Verification:
- [ ] `grep -n 'error' webui/bmad-dashboard-store.js`

Dependencies: None  
Files touched: `webui/bmad-dashboard-store.js`

---

### Task B6: Full bash hardening of `bmad-init.sh` [Size: S]

Phase: B  
Description: Complete bash hardening beyond A1's path fix: (1) change `set -e` to `set -euo pipefail`; (2) replace `cp -rn` with rsync-with-fallback pattern; (3) move all warning messages to stderr with `>&2`; (4) add `project-context.md` stub write (empty file, idempotent).

Acceptance criteria:
- [ ] Line 2 is `set -euo pipefail`
- [ ] Seed-knowledge copy uses rsync if available, falls back to `cp -Rn`
- [ ] All `echo "Warning:..."` use `>&2`
- [ ] `bash -n skills/bmad-init/scripts/bmad-init.sh` exits 0

Verification:
- [ ] `bash -n skills/bmad-init/scripts/bmad-init.sh`
- [ ] `head -3 skills/bmad-init/scripts/bmad-init.sh`

Dependencies: A1  
Files touched: `skills/bmad-init/scripts/bmad-init.sh`

---

### Task B7: Consolidate `AGENT_NAMES`, `PHASE_ACTIONS`, `PHASE_BUCKET_PREFIXES` into `helpers/bmad_status_core.py` [Size: M]

Phase: B  
Description: These constants are currently duplicated across `api/_bmad_status.py` and `skills/bmad-init/scripts/bmad-status.py`. Move all three to `helpers/bmad_status_core.py` as the single source of truth. Update `api/_bmad_status.py` to import them via the existing importlib `_core_mod` object. Update `bmad-status.py` to import them via its importlib load. Remove duplicate definitions.

Acceptance criteria:
- [ ] `AGENT_NAMES`, `PHASE_ACTIONS`, `PHASE_BUCKET_PREFIXES` defined once in `helpers/bmad_status_core.py`
- [ ] `api/_bmad_status.py` imports them from `_core_mod`
- [ ] `bmad-status.py` imports them from its importlib-loaded core module
- [ ] `grep -n 'AGENT_NAMES' api/_bmad_status.py` → no dict literal definition, only import reference
- [ ] `python -m pytest tests/ -v` green

Verification:
- [ ] `python -m pytest tests/ -v`
- [ ] `grep -c 'AGENT_NAMES\s*=' api/_bmad_status.py skills/bmad-init/scripts/bmad-status.py` → both `0`

Dependencies: A2 (helpers/bmad_status_core.py canonical)  
Files touched: `helpers/bmad_status_core.py`, `api/_bmad_status.py`, `skills/bmad-init/scripts/bmad-status.py`

---

### Task B8: Remove dead imports from `api/_bmad_status.py` [Size: XS]

Phase: B  
Description: Line 2 imports `re, json` — neither is used in the file. Remove. Also remove duplicate `from pathlib import Path as _Path` (line 7 duplicates line 3). Clean up.

Acceptance criteria:
- [ ] No unused imports remain in `api/_bmad_status.py`
- [ ] `python -m flake8 api/_bmad_status.py --max-line-length 100` → no F401 errors

Verification:
- [ ] `python -m flake8 api/ helpers/ extensions/ --max-line-length 100 --select=F401`

Dependencies: A6, B7  
Files touched: `api/_bmad_status.py`

---

### Task B9: Implement mtime-keyed caching for alias + CSV reads [Size: M]

Phase: B  
Description: `_parse_alias_map()` currently caches by path string only (not mtime) — a file change won't invalidate the cache within a session. `_collect_routing_rows()` re-reads all CSVs on every `execute()` call. Implement: (1) `_alias_cache` keyed on `(str(path), mtime_ns)` — invalidates on file change; (2) `_csv_cache` dict keyed on `(str(path), mtime_ns)` for each CSV's parsed rows; (3) single `_SKILLS_DIR.glob()` call per `execute()` call, result reused for both routing rows and artifact scan.

Acceptance criteria:
- [ ] `_alias_cache` key is `(path_str, mtime_ns)` tuple
- [ ] `_csv_cache` module-level dict, same key pattern
- [ ] Second call within same process with unchanged files hits cache (no re-read)
- [ ] `python -m pytest tests/ -v` green

Verification:
- [ ] `python -m pytest tests/ -v`
- [ ] Code review of `_parse_alias_map()` and `_collect_routing_rows()`

Dependencies: A3 (mtime fallback removed; C3 leakage concern gone)  
Files touched: `extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py`

---

### Task B10: Git branch setup + VPS deploy confirm [Size: XS]

Phase: B  
Description: Ensure `develop` branch exists and is pushed to remote. Tag current pre-align state as `v1.0.8-pre-align`. Confirm VPS symlink mapping is operational: `testing/usr/plugins/bmad_method → ../projects/a0_bmad_method`. Confirm git pull works on testing instance.

Acceptance criteria:
- [ ] `git -C /a0/usr/projects/a0_bmad_method branch -r | grep develop` → exists
- [ ] `git -C /a0/usr/projects/a0_bmad_method tag | grep v1.0.8-pre-align` → exists
- [ ] VPS git pull succeeds without error

Verification:
- [ ] `git -C /a0/usr/projects/a0_bmad_method log --oneline -5`
- [ ] SSH to VPS and confirm `git pull origin develop` exits 0

Dependencies: None  
Files touched: git metadata only

---

### Task B11: Write `tests/test_bmad_init_sh.py` [Size: S]

Phase: B  
Description: New test file. Shell integration tests via `subprocess.run()` against actual `bmad-init.sh`. Tests: (1) init creates all expected directories; (2) `01-bmad-config.md` has no `/a0/usr/projects/` literals; (3) idempotent — second run preserves existing config; (4) `set -euo pipefail` present; (5) rsync fallback path doesn't crash.

Acceptance criteria:
- [ ] `pytest tests/test_bmad_init_sh.py -v` all green
- [ ] Tests run against `/tmp/test-bmad-*` scratch dirs (cleaned up in teardown)
- [ ] At least 4 test functions

Verification:
- [ ] `python -m pytest tests/test_bmad_init_sh.py -v`

Dependencies: A1, B6  
Files touched: `tests/test_bmad_init_sh.py` (new)

---

## Checkpoint: Phase B

**Pass criteria:**
- [ ] `plugin.yaml` has `per_project_config: true`
- [ ] `bmad-user-prefs.promptinclude.md` written on init
- [ ] `AGENT_NAMES`, `PHASE_ACTIONS`, `PHASE_BUCKET_PREFIXES` — defined only in `helpers/bmad_status_core.py`
- [ ] `.gitignore` blocks `.kilo/`, `.cursor/`, `.claude/`, `.windsurf/`
- [ ] `develop` branch pushed; VPS deploy pipeline confirmed
- [ ] `python -m pytest tests/ -v` → all green (includes B11 shell tests)
- [ ] `python -m flake8 api/ helpers/ extensions/ --max-line-length 100` → zero F401

---

## Phase C — Routing Consolidation

**Prereq:** Phase B checkpoint passed.

### Task C0: Migrate `skills/bmad-init/core/module-help.csv` to upstream 13-column schema [Size: S]

Phase: C  
Description: **OQ-C1 resolved.** `skills/bmad-init/core/module-help.csv` is the sole CSV still on the old schema (different column names/order). Upstream and all 4 other skill CSVs already use the new 13-column schema: `module,skill,display-name,menu-code,description,action,args,phase,after,before,required,output-location,outputs`. The routing extension has dual-read compatibility code for both schemas — migrating this outlier enables C1 to safely remove that dual-read fallback. No dependencies; must complete before C1.

Acceptance criteria:
- [ ] `skills/bmad-init/core/module-help.csv` header row matches exactly: `module,skill,display-name,menu-code,description,action,args,phase,after,before,required,output-location,outputs`
- [ ] All data rows correctly re-mapped to new column positions (no data lost)
- [ ] `python -m pytest tests/ -v` green after migration

Verification:
- [ ] `head -1 skills/bmad-init/core/module-help.csv` → 13-column upstream header
- [ ] `python -m pytest tests/ -v`

Dependencies: None  
Files touched: `skills/bmad-init/core/module-help.csv`

---

### Task C1: Align `module-help.csv` columns to upstream 13-column schema [Size: L]

Phase: C  
Description: Upstream BMAD-METHOD `module-help.csv` uses this schema: `module, skill, display-name, menu-code, description, action, args, phase, after, before, required, output-location, outputs`. Our CSVs differ in column names and ordering (e.g., use `name`/`code`/`agent-name` instead of `display-name`/`menu-code`/`skill`). Normalize all 5 module-help.csv files to the upstream schema. The routing extension already handles dual-read for old/new column names (lines 104–129) — after migration, remove the old-name fallbacks from the extension.

Acceptance criteria:
- [ ] All 5 `module-help.csv` files have exactly 13 columns matching upstream schema
- [ ] `python -m pytest tests/ -v` green
- [ ] Routing manifest still produces non-empty output after normalization
- [ ] Old-column fallbacks removed from `_collect_routing_rows()`

Verification:
- [ ] `head -1 skills/*/module-help.csv` → all match 13-column header
- [ ] `python -m pytest tests/ -v`

Dependencies: C0 (bmad-init/core/module-help.csv migrated first), B9 (caching — avoid premature CSV re-reads)  
Files touched: `skills/bmad-init/module-help.csv`, `skills/bmad-bmm/module-help.csv`, `skills/bmad-bmb/module-help.csv`, `skills/bmad-tea/module-help.csv`, `skills/bmad-cis/module-help.csv`, `extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py`

---

### Task C2: Add `trigger_patterns` to `bmad-bmm` workflow SKILL.md files [Size: L]

Phase: C  
Description: BMM module has ~20 workflow directories under `skills/bmad-bmm/workflows/`. Each SKILL.md needs a `trigger_patterns` block with slash-style entries matching the workflow name and natural-language variants. Keep SKILL.md minimal — only `name`, `description`, `trigger_patterns`, `version`, `tags`. No `bmad:` routing block (that lives in CSV).

Acceptance criteria:
- [ ] Every `skills/bmad-bmm/workflows/**/SKILL.md` has `trigger_patterns:` with at least 2 entries
- [ ] All entries are slash-style (`/bmad-*`) or natural language variants
- [ ] No `bmad:` frontmatter block added (routing stays in CSV)

Verification:
- [ ] `find skills/bmad-bmm/workflows -name SKILL.md | xargs grep -L 'trigger_patterns' | wc -l` → 0

Dependencies: C1 (CSV schema locked before adding SKILL.md patterns that must match)  
Files touched: all `skills/bmad-bmm/workflows/**/SKILL.md`

---

### Task C3: Add `trigger_patterns` to `bmad-cis` workflow SKILL.md files [Size: M]

Phase: C  
Description: CIS module has ~5 workflow directories. Same pattern as C2.

Acceptance criteria:
- [ ] Every `skills/bmad-cis/workflows/**/SKILL.md` has `trigger_patterns:` block

Verification:
- [ ] `find skills/bmad-cis/workflows -name SKILL.md | xargs grep -L 'trigger_patterns' | wc -l` → 0

Dependencies: C1  
Files touched: all `skills/bmad-cis/workflows/**/SKILL.md`

---

### Task C4: Add `trigger_patterns` to `bmad-tea` workflow SKILL.md files [Size: M]

Phase: C  
Description: TEA module has ~9 workflow directories. Same pattern as C2.

Acceptance criteria:
- [ ] Every `skills/bmad-tea/workflows/**/SKILL.md` has `trigger_patterns:` block

Verification:
- [ ] `find skills/bmad-tea/workflows -name SKILL.md | xargs grep -L 'trigger_patterns' | wc -l` → 0

Dependencies: C1  
Files touched: all `skills/bmad-tea/workflows/**/SKILL.md`

---

### Task C5: Add `trigger_patterns` to `bmad-bmb` workflow SKILL.md files [Size: M]

Phase: C  
Description: BMB module has ~5 workflow directories. Same pattern as C2.

Acceptance criteria:
- [ ] Every `skills/bmad-bmb/workflows/**/SKILL.md` has `trigger_patterns:` block

Verification:
- [ ] `find skills/bmad-bmb/workflows -name SKILL.md | xargs grep -L 'trigger_patterns' | wc -l` → 0

Dependencies: C1  
Files touched: all `skills/bmad-bmb/workflows/**/SKILL.md`

---

### Task C6: Add `trigger_patterns` to `bmad-init/core` workflow SKILL.md files [Size: S]

Phase: C  
Description: Core module has ~3 workflow directories. Same pattern.

Acceptance criteria:
- [ ] Every `skills/bmad-init/core/workflows/**/SKILL.md` has `trigger_patterns:` block

Verification:
- [ ] `find skills/bmad-init/core/workflows -name SKILL.md | xargs grep -L 'trigger_patterns' | wc -l` → 0

Dependencies: C1  
Files touched: `skills/bmad-init/core/workflows/**/SKILL.md`

---

### Task C7: Verify routing + discoverability, expand tests [Size: S]

Phase: C  
Description: End-to-end verification: (1) routing extension still produces valid manifest after CSV normalization; (2) key skill searches return correct results on VPS testing instance via A2A; (3) add pytest coverage for CSV column normalization and trigger_patterns presence. Also verify caching works: routing manifest built from cache on second call in same session.

Acceptance criteria:
- [ ] `skills_tool:search "dev story"` returns `bmad-dev-story` on VPS
- [ ] `skills_tool:search "create prd"` returns correct workflow on VPS
- [ ] `python -m pytest tests/ -v` green
- [ ] New test verifies all SKILL.md files have `trigger_patterns`

Verification:
- [ ] `python -m pytest tests/ -v`
- [ ] A2A chat to testing endpoint: `skills_tool:search "product brief"`

Dependencies: C1, C2, C3, C4, C5, C6  
Files touched: `tests/test_extension_80.py` (expand), new test assertions

---

## Checkpoint: Phase C

**Pass criteria:**
- [ ] All 5 `module-help.csv` files have 13-column upstream schema
- [ ] `find skills -name SKILL.md | xargs grep -L 'trigger_patterns' | wc -l` → 0 (all have triggers)
- [ ] `skills_tool:search` returns correct workflows on VPS testing instance
- [ ] Routing extension caching confirmed in test or log inspection
- [ ] `python -m pytest tests/ -v` green

---

## Phase D — UX Surface

**Prereq:** Phase C checkpoint passed.

---

### Task D1: Create `prompts/bmad.methodology.shared.md` [Size: S]

Phase: D  
Description: Create `prompts/` directory and write the shared methodology fragment. This file should contain sections truly common across all 20 agents: Activation Protocol, BMAD Thinking Framework, Using BMAD Skills. Sections that are module-specific (BMM phase model, BMB builder patterns) must NOT be included — address in D2/D3.

Acceptance criteria:
- [ ] `prompts/bmad.methodology.shared.md` exists with at least Activation Protocol and Thinking Framework sections
- [ ] No module-specific content (BMM phases, BMB-only patterns)

Verification:
- [ ] `cat prompts/bmad.methodology.shared.md`

Dependencies: None  
Files touched: `prompts/bmad.methodology.shared.md` (new)

---

### Task D2: Audit shared scope of `main.specifics.md` — confirmed [Size: S]

Phase: D  
Description: **OQ-D2 resolved.** Audit complete. 7 sections byte-identical across all 19 non-master agents: (1) A0 Variable Resolution, (2) BMAD Activation Protocol, (3) Initial Clarification, (4) Thinking Framework, (5) Using BMAD Skills, (6) Tool Calling, (7) File and Artifact Handling. Only agent-specific part: `Available BMAD Skills` table (2-3 rows). `bmad-master` structurally different — excluded from shared fragment. Target file confirmed: `agents/_shared/prompts/bmad-agent-shared.md`. Each agent `specifics.md` → Role section (agent-specific) + `{{ include "bmad-agent-shared.md" }}` + Available Skills table (agent-specific).

Acceptance criteria:
- [ ] Findings documented in `.a0proj/run/current/findings.md` (confirmed complete)
- [ ] `agents/_shared/prompts/bmad-agent-shared.md` target path established

Verification:
- [ ] `cat .a0proj/run/current/findings.md | grep -A 5 'shared'`

Dependencies: D1  
Files touched: `.a0proj/run/current/findings.md`
---

### Task D3: Update 19 non-master `main.specifics.md` to use shared include [Size: L]

Phase: D  
Description: **OQ-D3 confirmed.** `{{ include "filename.md" }}` fully works in A0 agent prompt contexts via `helpers/files.py:process_includes()`. For each of the 19 non-master agents: replace 7 shared sections with `{{ include "bmad-agent-shared.md" }}`; retain Role section + Available Skills table (agent-specific). `bmad-master` excluded — kept as-is. Create `agents/_shared/prompts/bmad-agent-shared.md` with the 7 shared sections extracted from current specifics files.

Acceptance criteria:
- [ ] `agents/_shared/prompts/bmad-agent-shared.md` created with all 7 shared sections
- [ ] All 19 non-master `main.specifics.md` contain `{{ include "bmad-agent-shared.md" }}`; 7 shared sections removed
- [ ] `bmad-master/agent.system.main.specifics.md` unchanged; A0 resolves include on VPS without error

Verification:
- [ ] `grep -rl 'bmad-agent-shared' agents/ | grep -v bmad-master | wc -l` → 19
- [ ] A2A test: activate non-master agent; confirm full prompt loads with no missing sections

Dependencies: D1, D2  
Files touched: all 19 `agents/bmad-*/prompts/agent.system.main.specifics.md` (excl. bmad-master), `agents/_shared/prompts/bmad-agent-shared.md` (new)
---

### Task D4: Remove static 19-agent table from `bmad-master/role.md` [Size: XS]

Phase: D  
Description: Replace the static table listing all 19 subordinate agents in `agents/bmad-master/prompts/agent.system.main.role.md` with routing guidance prose. Safe to proceed — SPEC open question #2 confirmed resolved: `{{agent_profiles}}` dynamically includes all 20 BMAD profiles via `subagents.get_available_agents_dict()`.

Acceptance criteria:
- [ ] No static 19-row agent table in `bmad-master/role.md`
- [ ] Routing guidance prose references `{{agent_profiles}}` or equivalent
- [ ] bmad-master can still call all 20 subordinates on VPS testing instance

Verification:
- [ ] `grep -c '|' agents/bmad-master/prompts/agent.system.main.role.md` → significantly reduced
- [ ] A2A test: bmad-master delegates to bmad-analyst successfully

Dependencies: D3 (20 agents confirmed working with shared fragment)  
Files touched: `agents/bmad-master/prompts/agent.system.main.role.md`

---

### Task D5: Fix `_recommend()` caching in `api/_bmad_status.py` [Size: S]

Phase: D  
Description: `_recommend()` (lines 152–179) re-calls `_read_state()`, `_check_agents()`, `_check_skills()`, `_read_tests()` — all already called in `process()`. Refactor to accept pre-computed results as arguments instead of recomputing. This halves the I/O for each dashboard refresh.

Acceptance criteria:
- [ ] `_recommend(state, agents, skills, tests)` accepts cached results
- [ ] `process()` passes already-computed values
- [ ] No double filesystem reads per dashboard refresh

Verification:
- [ ] `python -m pytest tests/ -v`
- [ ] Code review: `_recommend()` signature has 4 parameters

Dependencies: B7, B8  
Files touched: `api/_bmad_status.py`

---

### Task D6: Dashboard error display [Size: S]

Phase: D  
Description: `bmad-dashboard-store.js` catches errors and calls `toastFrontendError()`, but the dashboard HTML has no inline error state display. After B5 cleanup, decide if a visible error section is needed. If yes: add `error: ""` state, populate on catch, show in template with `x-text` (never `x-html`). If no: confirm toast-only is sufficient and document the decision.

Acceptance criteria:
- [ ] Error handling strategy documented
- [ ] If error section added: uses `x-text`, store-gated with `x-if="$store.bmadDashboard"`
- [ ] No `x-html` anywhere in dashboard template

Verification:
- [ ] `grep 'x-html' webui/bmad-dashboard.html` → empty
- [ ] Dashboard loads without JS errors in browser

Dependencies: B5  
Files touched: `webui/bmad-dashboard.html`, `webui/bmad-dashboard-store.js`

---

### Task D7: `project-context.md` stub in `bmad-init.sh` [Size: XS]

Phase: D  
Description: Upstream BMAD v6 writes an empty `project-context.md` stub on init. Add idempotent creation of `$A0PROJ/knowledge/main/project-context.md` (empty file, no-clobber) to `bmad-init.sh`. This aligns with upstream v6 structure without requiring full v6 migration.

Acceptance criteria:
- [ ] `bmad-init.sh` creates `$A0PROJ/knowledge/main/project-context.md` on init (no-clobber)
- [ ] Second run does not overwrite existing file

Verification:
- [ ] `bash skills/bmad-init/scripts/bmad-init.sh /tmp/test-d7 && ls /tmp/test-d7/.a0proj/knowledge/main/project-context.md`

Dependencies: B6 (init.sh hardened)  
Files touched: `skills/bmad-init/scripts/bmad-init.sh`

### Task D8: Party mode (solo implementation) [Size: M]

Phase: D  
Description: **OQ-D-party resolved.** Implement party mode as the plugin's multi-agent conversation feature. Plugin diverges from upstream: implements upstream's `--solo` mode as its **only** mode — no real subagent spawning, no `--model` flag. **Known divergence from upstream: document explicitly; this is not a bug.** On activation, loads `agent-manifest.csv`, displays roster, selects 2-4 relevant agents per user message based on content analysis, and maintains each agent's distinct `communicationStyle` from config.

Acceptance criteria:
- [ ] AC-PM-01: On activation, load `agent-manifest.csv`, display roster with icon + name + one-liner
- [ ] AC-PM-02: For each user message, select 2–4 relevant agents based on content analysis
- [ ] AC-PM-03: Each agent response strictly from `communicationStyle` CSV field — no blending between agents
- [ ] AC-PM-04: Each agent response prefixed with `{icon} **{displayName}:**`
- [ ] AC-PM-05: Support user directing named agent: "Winston, what do you think?"
- [ ] AC-PM-06: Graceful exit on `*exit`, `goodbye`, `end party` — emit summary before closing
- [ ] AC-PM-07: Rotate agent participation — no two agents dominating consecutive rounds
- [ ] AC-PM-08: `communication_language` from config respected in all agent responses
- [ ] Known divergence documented in `docs/party-mode-divergence.md`: no parallel subagent spawning, no `--model` flag

Verification:
- [ ] Manual test: activate party mode, send 3 messages — verify ≥2 different agents respond each round
- [ ] `grep -c 'communicationStyle' skills/bmad-*/teams/default-party.csv` → non-zero across modules
- [ ] `cat docs/party-mode-divergence.md` confirms divergence documented

Dependencies: D3 (agents confirmed working with shared fragment)  
Files touched: party mode implementation file(s), `docs/party-mode-divergence.md` (new)

---

### Task D9: Plugin audit via `a0-review-plugin` [Size: S]

Phase: D  
Description: Run `a0-review-plugin` skill against the BMAD plugin. Fix any Critical findings. Document Important/Suggestion findings for future work. This is the final gate before `/ship`.

Acceptance criteria:
- [ ] `a0-review-plugin` produces output
- [ ] Zero Critical findings in output
- [ ] Any Important findings triaged and either fixed or deferred with rationale

Verification:
- [ ] Run `a0-review-plugin` skill in A0
- [ ] Output saved to `docs/plugin-audit-v1.1.md`

Dependencies: D4, D5, D6, D7, D8  
Files touched: `docs/plugin-audit-v1.1.md` (new)

## Checkpoint: Phase D (= VERIFY phase ready)

**Pass criteria — all required for `/ship`:**
- [ ] `bmad-master/role.md` has no static agent table
- [ ] `agents/_shared/prompts/bmad-agent-shared.md` included by all 19 non-master agents
- [ ] `a0-review-plugin` passes with zero Critical findings
- [ ] `python -m pytest tests/ -v` green
- [ ] All 20 BMAD agents functional end-to-end on VPS testing instance (A2A smoke test)
- [ ] `bmad init` works from `/tmp/`, `/a0/usr/projects/`, workdir (any path)
- [ ] Dashboard renders correctly, no browser console errors
- [ ] Ready to tag `v1.1.0` and merge to `main`

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| `bmad-status.py` import breaks after scripts/bmad_status_core.py deletion | High — CLI tool unusable | A2 scope explicitly includes updating bmad-status.py to importlib pattern |
| CSV column rename breaks routing extension row-parsing | High — no routing manifest | Routing extension dual-read already present; remove only after C0 migrates bmad-init/core CSV and C1 removes fallbacks |
| `{{ include }}` syntax in A0 agent prompts | **Resolved** ✅ | Confirmed working via `helpers/files.py:process_includes()`; D3 approach committed; no rollback risk |
| ~40 SKILL.md files need trigger_patterns — high volume, repetitive | Medium — time risk | C2–C6 split by module; can parallelize across subagents |
| Party Mode acceptance criteria undefined | **Resolved** ✅ | 8 AC-PM defined (D9); plugin implements upstream solo-mode only — no subagent spawning; divergence documented, not a bug |
| `02-bmad-state.md` format change for YAML frontmatter (SPEC OQ #6) | Low | Deferred; backward compat migration script needed if pursued |
| B9 mtime cache keying correctness | Medium — stale cache within session | Cache key MUST be `(path_str, mtime_ns)` tuple, not path string alone; file changes within same session would be missed with path-only key |

---

## Parallelization Opportunities

- **A4** (HTML fix) and **A6** (None-guard) can run in parallel with **A2** — no file overlap
- **C2, C3, C4, C5, C6** can all run in parallel after **C1** — different skill directories
- **D5, D6, D7** can run in parallel after their respective dependencies
- **B1, B3, B4, B5** can all run in parallel — no file overlap

---

## Open Questions

> **All open questions resolved as of OQ resolution batch — no remaining blockers before BUILD.**

| OQ | Status | Resolution |
|---|---|---|
| OQ-A3: Mtime fallback disposition | ✅ Resolved | Split treatment: `api/_bmad_status.py` + `_80_bmad_routing_manifest.py` → hard remove; `bmad-status.py` → gate behind `BMAD_DEV_MODE` with `log.warning()` |
| OQ-C1: CSV schema migration scope | ✅ Resolved | `skills/bmad-init/core/module-help.csv` is sole outlier → new **C0** task; upstream + other 4 skill CSVs already on new schema |
| OQ-D3: `{{ include }}` support in A0 agent prompts | ✅ Resolved | Confirmed working via `helpers/files.py:process_includes()`; D3 approach committed |
| OQ-D2: Shared fragment scope | ✅ Resolved | 7 sections byte-identical across 19 non-master agents; `bmad-master` excluded; target: `agents/_shared/prompts/bmad-agent-shared.md` |
| OQ-D-party: Party mode acceptance criteria | ✅ Resolved | 8 AC-PM criteria defined; plugin implements solo-mode only (no subagent spawning); divergence documented, not a bug |
