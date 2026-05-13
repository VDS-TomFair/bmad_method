# Code Review: BMAD Method A0 Plugin Alignment Sprint

## Review Summary

**Verdict:** APPROVE
**Reviewer:** Code Reviewer (Senior Staff Engineer)
**Date:** 2026-05-02
**Scope:** 6 bundles, 56 test files, ~50 files changed
**Test Results:** 503 passed, 0 failed, 221 subtests (4.70s)

**Overview:** The alignment sprint delivers a clean CSV→YAML migration, agent consolidation (21→18 profiles), CIS persona removal, and P3 structural improvements (8-step activation, sidecar memory, project-context auto-loading). The codebase is well-structured, follows A0 extension patterns correctly, and all 503 tests pass. No blocking issues found.

---

## Categorized Issues

### Critical Issues

None.

### Important Issues

**I-1. `bmad-init.sh` L28: `echo` without `-e` produces literal `\n` in memories.md stubs**

```bash
# Current (line 28):
[ -f "...memories.md" ] || echo "# ${agent} memories\n\n" > "...memories.md"
```

In bash, `echo` without `-e` does NOT interpret escape sequences. The resulting file contains literal `\n` characters instead of newlines. This is cosmetic (the stub is immediately overwritten on first use), but it's technically incorrect.

**Fix:** Use `printf` instead:
```bash
[ -f "...memories.md" ] || printf "# %s memories\n\n" "${agent}" > "...memories.md"
```

**I-2. `import-sidecars.sh` is effectively a no-op audit tool**

The script scans `$A0PROJ/_bmad/_memory/*-sidecar/` directories and reports what exists, but does not copy files from any upstream source. The comment on line 49 says "For A0 plugin, files are already in place via init script" — confirming it's a verification tool, not an import mechanism.

The SKILL.md title says "Import Upstream Sidecar Memory" which may mislead users expecting an actual import operation.

**Recommendation:** Rename to `verify-sidecars.sh` or update SKILL.md to clearly state it's a verification/audit tool, not an import mechanism.

**I-3. Test suite quality gaps — 44% string-inclusion, zero mocking**

198 of 446 test methods use `assert "x" in source.read_text()` pattern. These are fragile — they break on variable renaming or whitespace changes without catching actual behavioral regressions. Zero tests use mocks, patches, or test doubles. Only 10 error-path tests exist across the entire suite.

**Not a merge blocker** — the tests DO provide valuable structural coverage and caught real issues during development. But the team should invest in behavioral tests for future sprints.

### Suggestions

**S-1. CIS agent.yaml trailing whitespace cleanup**

`agents/bmad-innovation/agent.yaml`, `agents/bmad-design-thinking/agent.yaml`, and `agents/bmad-presentation/agent.yaml` have trailing whitespace in YAML multiline strings and a leading space in the `context` field (e.g., `' Innovation Strategist`). Valid YAML, but inconsistent with cleaner agent.yaml files like bmad-dev (6 lines, no trailing whitespace).

**S-2. CIS agent.yaml title fields lack agent names**

Innovation/Design-Thinking/Presentation agent.yaml files use generic titles ("BMAD Innovation Strategist") while other agents include persona names ("Amelia — Developer Agent", "Morgan — Module Creation Master"). Consider adding names for consistency, or document that CIS agents intentionally use generic titles per upstream alignment.

**S-3. Step 5.5 numbering in activation sequence**

`prompts/bmad-agent-shared.md` uses Step 5.5 for sidecar memory loading, inserted between Steps 5 and 6. Functionally correct but slightly awkward. Consider renumbering to Steps 1-9, or documenting that 5.5 is a sub-step of 5 (persistent data loading).

**S-4. Add `communication_additions.md` verification**

`helpers/bmad_status_core.py` defines `REQUIRED_PROMPTS` including `agent.system.main.communication_additions.md`. Verify all 17 agent directories contain this file. No test currently validates this.

**S-5. Consider end-to-end test for resolve_customization.py**

Currently tested for imports and deep_merge function, but not for a full CLI invocation with real TOML files. The verification report also recommends this.

### Nits

**N-1.** `_bmad_status.py` lines 60-61: Two extra blank lines (cosmetic only).

**N-2.** BMM module.yaml line 169: `output-location: planning_artifacts|project-knowledge` uses pipe separator — consistent with design but worth a comment for future readers.

---

## What's Done Well

1. **Routing extension architecture** — The `_80_bmad_routing_manifest.py` is excellent. Mtime-keyed cache invalidation prevents stale data without re-reading unchanged files. Phase-aware module filtering keeps routing relevant. Artifact staleness warnings (PRD→Architecture→Sprint chain) are a thoughtful addition.

2. **YAML migration execution** — Clean migration from CSV to YAML with zero regressions. ADR-0010 properly documents the decision. All 7 module.yaml files parse correctly with consistent schema.

3. **Agent consolidation** — Removing 3 agents (SM, QA, Quick-Dev) and consolidating menus into Amelia was done cleanly. The QD menu code fix (QQ→QD) is properly verified.

4. **8-step activation sequence** — Well-documented in `bmad-agent-shared.md`. The resolve_customization.py integration (Step 1) with three-layer TOML merge is elegant — team overrides, personal overrides, skill defaults.

5. **Sidecar memory architecture** — File-based memory per agent under `_bmad/_memory/{agent}-sidecar/memories.md` is simple and effective. Init script creates all 16 worker agent directories idempotently.

6. **Security consciousness** — `resolve_customization.py` uses `tomllib` (safe parser), walks only upward for project root discovery (no path traversal), validates all inputs. Routing extension uses `yaml.safe_load()` exclusively.

7. **Idempotent init** — `bmad-init.sh` uses no-clobber patterns throughout (`[ ! -f ]` guards, `rsync --ignore-existing`, `cp -Rn`). Re-running init preserves user data.

8. **Comprehensive verification** — The verification report at `docs/verification-report.md` covers all 6 bundles with explicit pass/fail criteria and gap analysis.

---

## Five-Axis Assessment

| Axis | Rating | Notes |
|------|--------|-------|
| Correctness | 9/10 | All 6 bundles implemented per SPEC.md. 503 tests pass. Edge cases covered (empty YAML, missing files). Deduction: echo bug in init.sh (I-1), import-sidecars.sh is a no-op (I-2). |
| Readability | 8/10 | Clear naming conventions, well-structured module.yaml files, good docstrings. Deduction: CIS agent.yaml trailing whitespace (S-1), Step 5.5 numbering (S-3). |
| Architecture | 9/10 | Follows A0 extension patterns correctly. Clean module boundaries. Mtime caching is well-designed. Phase-aware routing is elegant. No circular dependencies. |
| Security | 9/10 | yaml.safe_load(), tomllib, no injection vectors, no credential exposure, no command injection in scripts. find_project_root walks only upward. Deduction: No explicit path validation in import-sidecars.sh (but it's a no-op anyway). |
| Performance | 9/10 | Mtime-keyed cache avoids re-reading unchanged YAML. Single discovery per execute(). FIFO cache eviction. No N+1 patterns. Deduction: Cache eviction removes oldest half (could use LRU), but acceptable for 128-entry limit. |

---

## Verification Story

- **Tests reviewed:** 56 test files, 503 tests (446 methods + 57 parametrized), 221 subtests — ALL PASS
- **Build status:** PASS (4.70s execution time)
- **Security checked:** YES — yaml.safe_load(), tomllib, no shell injection, no path traversal, no credential exposure
- **Manual verification:** Init script reviewed line-by-line. Routing extension logic verified. Agent consolidation confirmed (3 directories removed, menus migrated). CIS persona removal confirmed (zero matches for Victor/Dr. Quinn/Maya/Carson/Sophia/Caravaggio).
- **Test quality:** 6.0/10 — strong structural coverage but weak behavioral testing (44% string-inclusion, zero mocking, 10 error-path tests). Adequate for this sprint but needs investment for future sprints.

---

## Bundle-by-Bundle Assessment

| Bundle | Description | Verdict | Notes |
|--------|-------------|---------|-------|
| 1 | CSV → YAML Migration | ✅ PASS | Clean migration, ADR-0010, 77 workflow codes, zero CSV imports in production |
| 2 | Agent Consolidation | ✅ PASS | 3 agents removed, 12 menus in Amelia, QD code fixed |
| 3 | CIS Persona Removal | ✅ PASS | Zero named personas, generic titles, no icon collisions |
| 4 | Quick Fixes | ✅ PASS | Morgan 📦, Sally filmmaker, Paige US menu, _bmad/custom/ created |
| 5 | Test Updates | ✅ PASS | 39 new tests, 0 regressions |
| 6 | P3 Structural | ✅ PASS | 8-step activation, sidecar memory, project-context auto-loading |

---

## Files Reviewed (Complete List)

### Plugin Core
- `plugin.yaml` — 24 lines, clean
- `SPEC.md` — 1099 lines, comprehensive spec

### Routing (Bundle 1)
- `extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py` — 449 lines, excellent
- `skills/bmad-bmm/module.yaml` — 439 lines, clean
- `skills/bmad-tea/module.yaml` — 120 lines, clean
- `skills/bmad-cis/module.yaml` — 87 lines, clean (cross-module dep noted)
- `skills/bmad-bmb/module.yaml` — 261 lines, clean
- `skills/bmad-init/core/module.yaml` — 156 lines, clean

### Activation Sequence (Bundle 6)
- `prompts/bmad-agent-shared.md` — 187 lines, clean
- `prompts/bmad-agent-shared-solving.md` — 16 lines, clean
- `scripts/resolve_customization.py` — 237 lines, clean

### Init Script (Bundles 4, 6)
- `skills/bmad-init/scripts/bmad-init.sh` — 124 lines, minor echo bug (I-1)

### Agent Changes (Bundles 2, 3, 4)
- `agents/bmad-dev/agent.yaml` — 6 lines, clean
- `agents/bmad-dev/prompts/agent.system.main.role.md` — 100 lines, excellent
- `agents/bmad-module-builder/agent.yaml` — 6 lines, clean
- `agents/bmad-ux-designer/prompts/agent.system.main.role.md` — 79 lines, clean
- `agents/bmad-tech-writer/prompts/agent.system.main.role.md` — 82 lines, clean
- `agents/bmad-innovation/agent.yaml` — 13 lines, trailing whitespace (S-1)
- `agents/bmad-design-thinking/agent.yaml` — 11 lines, trailing whitespace (S-1)
- `agents/bmad-presentation/agent.yaml` — 13 lines, trailing whitespace (S-1)
- `agents/bmad-master/prompts/agent.system.main.role.md` — 132 lines, clean
- `helpers/bmad_status_core.py` — 122 lines, clean

### API and WebUI
- `api/_bmad_status.py` — 140 lines, clean
- `webui/bmad-dashboard.html` — 269 lines, clean

### Sidecar (Bundle 6)
- `skills/bmad-sidecar-import/SKILL.md` — 57 lines, clean
- `skills/bmad-sidecar-import/scripts/import-sidecars.sh` — 63 lines, no-op concern (I-2)

### Tests
- `tests/` — 56 files, 503 tests, ALL PASS

### Documentation
- `docs/adr/0010-yaml-canonical-routing.md` — 68 lines, clean
- `docs/verification-report.md` — 159 lines, comprehensive

---

## Final Verdict

**APPROVE** — The alignment sprint is ready to merge. All 6 bundles are correctly implemented, all 503 tests pass, security is sound, and architecture follows A0 patterns. The 3 Important issues are non-blocking (cosmetic echo bug, no-op script naming, test quality investment for future sprints).
