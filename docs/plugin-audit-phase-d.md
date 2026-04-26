# Plugin Audit — Phase D

**Date:** 2026-04-26
**Branch:** develop
**Test Suite:** 169 tests, all passing (0.95s)

## Phase D Tasks Completed

| Task | Description | Status |
|------|-------------|--------|
| D1 | Create `agents/_shared/prompts/bmad-agent-shared.md` — 6 shared sections | ✅ |
| D2 | Audit 20 agent specifics — confirm 6 sections identical, skills table varies by module | ✅ |
| D3 | Update 19 non-master specifics to use `{{ include "bmad-agent-shared.md" }}` | ✅ |
| D4 | Remove static 19-agent table from bmad-master role.md, use `{{agent_profiles}}` | ✅ |
| D5 | Fix `_recommend()` caching — accept pre-computed state/agents/skills/tests | ✅ |
| D6 | Dashboard error display — store-gated, `x-text` only, no `x-html` | ✅ |
| D7 | `project-context.md` stub — idempotent empty file creation | ✅ |
| D8 | Party mode — all 8 ACs verified, known divergence documented | ✅ |
| D9 | Plugin audit — this document | ✅ |

## Test Coverage Summary

### Phase A Tests (8 files, 51 tests)
- `test_bmad_init_sh.py` — init script paths, strict mode, idempotency
- `test_bmad_dashboard_html.py` — HTML tag balance
- `test_bmad_routing_logging.py` — bare except logging
- `test_bmad_status_api.py` — None-guard on spec
- `test_bmad_status_core.py` — shared state parser, compiled regex
- `test_mtime_fallback.py` — mtime fallback removal/gating
- `test_dead_code.py` — dead code removal
- `test_extension_80.py` — routing extension baseline

### Phase B Tests (8 files, 37 tests)
- `test_plugin_yaml.py` — per_project_config
- `test_bmad_init_skill.py` — trigger patterns
- `test_api_dead_imports.py` — dead imports
- `test_dashboard_store.py` — error state
- `test_user_prefs.py` — user prefs migration
- `test_bash_hardening.py` — rsync fallback, stderr
- `test_constants_consolidation.py` — AGENT_NAMES/PHASE_ACTIONS
- `test_mtime_caching.py` — mtime-keyed cache

### Phase C Tests (8 files, 42 tests)
- `test_core_csv_schema.py` — 13-col CSV migration
- `test_c1_dual_read.py` — dual-read removal
- `test_c6_core_triggers.py` — core trigger patterns
- `test_c3_cis_triggers.py` — CIS trigger patterns
- `test_c5_bmb_triggers.py` — BMB trigger patterns
- `test_c4_tea_triggers.py` — TEA trigger patterns
- `test_c2_bmm_triggers.py` — BMM trigger patterns
- `test_c7_verification.py` — schema + coverage verification

### Phase D Tests (9 files, 39 tests)
- `test_d7_project_context.py` — project-context.md stub
- `test_d4_master_table.py` — static table removal
- `test_d6_error_display.py` — error display strategy
- `test_d5_recommend_caching.py` — _recommend() caching
- `test_d1_shared_fragment.py` — shared fragment creation
- `test_d2_audit_specifics.py` — agent specifics audit
- `test_d3_include_directive.py` — include directive migration
- `test_d8_party_mode.py` — party mode 8 ACs

## Key Findings

### Architecture Improvements
1. **Shared prompt fragment** reduces 19× duplicated sections to 1 include file (~1662 lines removed)
2. **Dynamic agent table** via `{{agent_profiles}}` auto-updates when agents change
3. **Pre-computed recommendation** eliminates double I/O on each dashboard refresh
4. **Store-gated error display** prevents XSS via `x-text` only
5. **Party mode** verified against all 8 acceptance criteria with known divergences documented

### No Regressions
- All 169 tests pass with zero failures
- No `x-html` usage in dashboard
- No bare `except: pass` without logging
- No cross-project mtime fallback in production code
- All CSV files use unified 13-column schema

## Files Modified (Phase D)

### New Files
- `agents/_shared/prompts/bmad-agent-shared.md`
- `docs/plugin-audit-phase-d.md`

### Modified Files
- `agents/bmad-*/prompts/agent.system.main.specifics.md` (19 files)
- `agents/bmad-master/prompts/agent.system.main.role.md`
- `api/_bmad_status.py`
- `webui/bmad-dashboard.html`
- `webui/bmad-dashboard-store.js`
- `skills/bmad-init/scripts/bmad-init.sh`
- `skills/bmad-init/core/workflows/party-mode/workflow.md`
- 9 test files created

## Conclusion

Phase D completes the BMAD-A0 alignment implementation. All 9 tasks (D1–D9) completed with full TDD coverage. The plugin is in a clean, working state with 169 passing tests and no known regressions.
