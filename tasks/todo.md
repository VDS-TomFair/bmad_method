# TODO: BMAD Method A0 Alignment — 35 tasks (A: 7 · B: 11 · C: 8 · D: 9)

## Phase A — Critical Bug Fixes

- [x] A1: Fix hardcoded `/a0/usr/projects/` paths in `bmad-init.sh` (S) — Replace 5 path-table literals with `$A0PROJ`-derived vars; add `set -euo pipefail`
- [x] A2: Consolidate `read_state()` into `helpers/bmad_status_core.py` (M) — Add MULTILINE+IGNORECASE regex, lowercase output, delete scripts/bmad_status_core.py, update bmad-status.py + routing ext
- [x] A3: Remove/gate cross-project mtime fallback — split treatment (M) — `api/_bmad_status.py` + routing ext: hard remove, return `None`; `bmad-status.py`: gate behind `BMAD_DEV_MODE` with `log.warning()`
- [x] A4: Fix malformed HTML in `bmad-dashboard.html` (XS) — Remove 4 stray `</div>` and 1 stray `</template>` at lines 255–263
- [x] A5: Add `log.warning()` to bare `except` blocks in routing extension (XS) — Top-level `execute()` except + `_build_staleness_warnings()` except
- [x] A6: None-guard on `spec_from_file_location` in `api/_bmad_status.py` (XS) — Add `if _spec is None: raise ImportError(...)`
- [x] A7: Write `tests/test_bmad_status_core.py` (S) — 6+ `read_state()` format variants, exports, check_agents/check_modules fixtures

## Phase B — Structural Alignment

- [x] B1: Set `per_project_config: true` in `plugin.yaml` (XS) — One-line change enables per-project toggle UI
- [x] B2: Move user prefs to `bmad-user-prefs.promptinclude.md` (S) — Write file on init (no-clobber), remove User Settings block from 01-bmad-config.md template
- [x] B3: Add slash-style `trigger_patterns` to `skills/bmad-init/SKILL.md` (XS) — `/bmad`, `/bmad-init`, `/bmad-help`, `/bmad-status` + natural-language variants
- [x] B4: Remove dead `SKILL_TO_MODULE` constant from routing extension (XS) — Lines 30–36, verify no importers
- [x] B5: Fix orphaned `this.error` field in `bmad-dashboard-store.js` (XS) — Remove assignment or add state declaration to match
- [x] B6: Full bash hardening of `bmad-init.sh` (S) — `set -euo pipefail`, rsync fallback, warnings to stderr
- [x] B7: Consolidate `AGENT_NAMES`, `PHASE_ACTIONS`, `PHASE_BUCKET_PREFIXES` into `helpers/bmad_status_core.py` (M) — Remove duplicates from api + bmad-status.py; import via importlib
- [x] B8: Remove dead imports from `api/_bmad_status.py` (XS) — Delete `re, json`; remove duplicate `Path as _Path`
- [x] B9: Implement mtime-keyed caching for alias + CSV reads (M) — `(path_str, mtime_ns)` cache keys for `_alias_cache` and new `_csv_cache`
- [x] B10: Git branch setup + VPS deploy confirm (XS) — Verify `develop` branch, tag `v1.0.8-pre-align`, confirm VPS symlink + git pull
- [x] B11: Write `tests/test_bmad_init_sh.py` (S) — Subprocess tests: directories created, no hardcoded paths, idempotency, strict-mode header

## Phase C — Routing Consolidation

- [ ] C0: Migrate `skills/bmad-init/core/module-help.csv` to upstream 13-col schema (S) — Sole CSV on old schema; migrate before C1 removes dual-read; no dependencies
- [ ] C1: Align remaining 4 `module-help.csv` files to upstream 13-column schema (L) — Depends on C0; normalize columns; remove old-name fallbacks from routing extension
- [ ] C2: Add `trigger_patterns` to all `bmad-bmm` workflow SKILL.md files (L) — ~20 files; slash-style + natural-language triggers; no `bmad:` block
- [ ] C3: Add `trigger_patterns` to all `bmad-cis` workflow SKILL.md files (M) — ~5 files; same pattern as C2
- [ ] C4: Add `trigger_patterns` to all `bmad-tea` workflow SKILL.md files (M) — ~9 files; same pattern as C2
- [ ] C5: Add `trigger_patterns` to all `bmad-bmb` workflow SKILL.md files (M) — ~5 files; same pattern as C2
- [ ] C6: Add `trigger_patterns` to `bmad-init/core` workflow SKILL.md files (S) — ~3 files; same pattern as C2
- [ ] C7: Verify routing + discoverability, expand tests (S) — VPS A2A smoke tests; pytest for CSV schema + trigger_patterns coverage

## Phase D — UX Surface

- [ ] D1: Create `prompts/bmad.methodology.shared.md` (S) — Activation Protocol + Thinking Framework sections shared across all 20 agents
- [ ] D2: Audit all 20 `main.specifics.md` to determine shared fragment scope (S) — OQ-D2 resolved: 7 sections byte-identical across 19 non-master agents; findings confirmed; target: `agents/_shared/prompts/bmad-agent-shared.md`
- [ ] D3: Update 19 non-master `main.specifics.md` to use shared include (L) — OQ-D3 confirmed: `{{ include "bmad-agent-shared.md" }}` works; replace 7 shared sections; bmad-master excluded
- [ ] D4: Remove static 19-agent table from `bmad-master/role.md` (XS) — Replace with routing guidance prose referencing `{{agent_profiles}}`
- [ ] D5: Fix `_recommend()` caching in `api/_bmad_status.py` (S) — Accept pre-computed state/agents/skills/tests; no double I/O per refresh
- [ ] D6: Dashboard error display (S) — Decide error UI strategy; ensure `x-text` only, store-gated; no `x-html`
- [ ] D7: `project-context.md` stub in `bmad-init.sh` (XS) — Idempotent empty file creation at `$A0PROJ/knowledge/main/project-context.md`
- [ ] D8: Party mode — solo implementation (M) — 8 ACs (AC-PM-01–08): roster display, agent selection, communicationStyle per agent, named-agent addressing, graceful exit, rotation, language config; document divergence from upstream (no subagent spawning, no `--model` flag)
- [ ] D9: Plugin audit via `a0-review-plugin` (S) — Run audit; fix any Critical findings; save output to `docs/plugin-audit-v1.1.md`; depends on D4, D5, D6, D7, D8

## Checkpoints

- [ ] ✅ Phase A checkpoint — init paths clean, HTML tidy errors=0, all tests green, phase values consistent, no silent except
- [ ] ✅ Phase B checkpoint — per_project_config true, promptinclude written, constants in core, develop branch live, flake8 F401 clean
- [ ] ✅ Phase C checkpoint — 13-col CSV, all SKILL.md have trigger_patterns, skills_tool:search correct on VPS, tests green
- [ ] ✅ Phase D checkpoint (= ready for VERIFY phase) — no static table, 20 agents include shared fragment, audit clean, all tests green
