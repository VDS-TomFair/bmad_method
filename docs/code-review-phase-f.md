# Phase F Code Review — Upstream v6.6.0 Sync

**Reviewer:** Code Reviewer (Agent Zero)  
**Date:** 2026-05-01  
**Scope:** 12 tasks, P0/P1/P2 priorities  
**Test suite:** 248 tests passed, 94 subtests passed, 1.24s  

---

## Review Summary

**Verdict:** ✅ **APPROVE**

**Overview:** Phase F is a clean, well-executed upstream sync. The 12 tasks deliver a properly adapted v6.6.0 alignment with 3 critical workflow step fixes, config migration, a new customization skill, and version polish. All upstream diffs are intentional A0 adaptations (YAML frontmatter, path variables, $A0PROJ conventions, state-write sections). No Critical issues found. Two Important findings documented below — one is a documentation gap, the other is a minor path convention nuance. Neither blocks merge.

---

## Findings

| ID | Severity | Axis | File | Description |
|----|----------|------|------|-------------|
| F-01 | Important | quality | `scripts/resolve_customization.py:14-15,62` | A0 Path Note in docstring says `$A0PROJ/_bmad/` but `find_project_root()` discovers root via `.git` or `_bmad` dir — not via `$A0PROJ`. When run against a user project this works correctly (bmad-init creates `_bmad/` at project root), but the docstring implies A0 discovers `.a0proj/` which isn't what the code does. |
| F-02 | Important | quality | `skills/bmad-customize/SKILL.md:17` | SKILL.md states "{project-root}/_bmad/ maps to $A0PROJ/_bmad/" but resolve_customization.py actually uses the upstream convention `{project-root}/_bmad/custom/`. The mapping is conceptual (A0 users invoke from plugin context), not literal (the script doesn't resolve $A0PROJ). |
| F-03 | Nit | simplification | `tests/test_resolve_customization.py` L37-52 | `TestScriptImports` imports the module twice (once per test method) via `importlib.util`. Could use `setUpClass` like `TestDeepMerge` does, but impact is negligible — test-only code. |
| F-04 | Nit | quality | `skills/bmad-customize/scripts/list_customizable_skills.py:50` | `default_skills_root()` assumes exactly 3 levels up from `__file__`. A comment explains the layout assumption, which is sufficient, but a guard assertion would make it self-documenting if the directory structure ever changes. |
| F-05 | FYI | architecture | `scripts/resolve_customization.py` | The 3-layer merge (defaults → team → user) is a faithful port of upstream with A0 path adaptation. The structural merge rules (scalars override, tables deep-merge, keyed arrays merge by code/id, others append) are clean and well-tested. No unnecessary complexity introduced in the A0 adaptation. |
| F-06 | FYI | security | `skills/bmad-bmm/workflows/.../step-04-final-validation.md:158` | The On Complete hook runs `python3 $A0PROJ/_bmad/scripts/resolve_customization.py` — this is safe because: (1) the script is a read-only TOML parser that outputs JSON to stdout, (2) it uses stdlib `tomllib` (no code execution from TOML), (3) the resolved `on_complete` value is followed as an instruction, not executed as code. |
| F-07 | FYI | performance | 30 `customize.toml` files | All 30 files are small (~30-60 lines each). Total parse time is negligible. No impact on plugin load time since customization is invoked on-demand, not at import. |

---

## Positive Observations

1. **Faithful upstream sync with clean A0 adaptation.** All 3 P0 workflow step diffs show intentional, well-reasoned A0 adaptations: YAML frontmatter for routing, `{project-root}` path variables instead of relative paths, `$A0PROJ` convention, and mandatory state-write sections. No accidental overwrites or missed upstream changes.

2. **Zero-dependency Python scripts.** Both `resolve_customization.py` and `list_customizable_skills.py` use only stdlib (`tomllib`, `json`, `pathlib`, `argparse`). No pip installs, no virtualenv needed. This is exactly right for a plugin that runs in Agent Zero's context.

3. **Robust error handling in resolve_customization.py.** The `load_toml()` function handles missing files, parse errors, and OS errors with clear stderr messages and appropriate exit codes (1 for required failures, 0 with empty dict for optional layers). The `required` parameter makes the distinction explicit.

4. **Well-structured test suite.** 48 new tests across 4 test files, all with descriptive docstrings, proper `setUp`/`setUpClass` patterns, and `subTest` usage for parameterized checks. Test names clearly map to task IDs (F-P0-1, F-P1-5, etc.).

5. **Clean TOML file design.** All 30 customize.toml files have consistent structure: header comment explaining "DO NOT EDIT", `[agent]` or `[workflow]` section, inline merge rules documentation, and proper use of arrays/tables. Spot-checked files parse cleanly.

6. **Comprehensive SKILL.md.** The bmad-customize SKILL.md defines a clear 6-step workflow (Classify → Discover → Surface → Compose → Place → Write/Verify) with proper preflight checks, fallback behaviors, and "when this skill can't help" boundaries.

7. **CHANGELOG quality.** Phase F section is well-structured with task IDs, clear descriptions of what changed, and proper Keep a Changelog format.

---

## Required Changes

**None.** No Critical or blocking Important issues found.

---

## Optional Improvements

1. **F-01/F-02 path convention clarification.** Consider adding a brief note in resolve_customization.py's docstring clarifying that `$A0PROJ` is a conceptual mapping — the script discovers the project root via `.git` or `_bmad` directory, and the actual override path is `{project-root}/_bmad/custom/`. This would prevent future confusion about whether the script should resolve `.a0proj/` literally.

2. **Test import dedup.** In `test_resolve_customization.py`, `TestScriptImports` could share the module import via `setUpClass` like `TestDeepMerge` does. Trivial improvement, test-only.

3. **Guard assertion in default_skills_root().** Adding `assert (self.parent / 'scripts' / 'list_customizable_skills.py').exists()` would make the layout assumption self-verifying, though the existing comment is sufficient.

---

## Upstream Diff Analysis

### step-07-validation.md
All differences are intentional A0 adaptations:
- L35-36: Protocol references use `{project-root}/skills/...` paths instead of upstream `Invoke the bmad-* skill` — correct for A0's file-based skill loading
- L310, L318: Same protocol path adaptation
- L328, L359: Step file references use full plugin paths instead of relative `./step-08-complete.md`
- L362-368: Added A0-specific `## ✅ Step Complete` section with frontmatter update instructions — not in upstream, intentional A0 addition

### step-02-design-epics.md
- L1-21: Added YAML frontmatter with path definitions — A0 routing pattern
- L57, L65, L214: Use `{outputFile}` variable instead of hardcoded `{planning_artifacts}/epics.md` — A0 path variable pattern
- L79: Added 🔗 emoji to Principle #5 — matches upstream visual style
- L226-228: Protocol paths use A0 convention instead of upstream skill invocations
- All other changes are path variable substitutions

### step-04-final-validation.md
- L1-20: Added YAML frontmatter — A0 routing pattern
- L113-118: File Churn Check subsection added — syncs upstream v6.6.0 addition
- L151: HALT instruction added — syncs upstream v6.6.0
- L158: Uses `$A0PROJ/_bmad/scripts/` instead of upstream `{project-root}/_bmad/scripts/` — A0 path convention
- L162-180: Added A0-specific State Write section with bash code block — not in upstream, intentional A0 addition for state management

**Verdict:** All diffs are intentional and correct. No accidental overwrites, no missing upstream content, no A0-specific sections lost.

---

## Security Assessment

| Check | Status | Notes |
|-------|--------|-------|
| Secrets in code | ✅ Pass | No secrets, API keys, or credentials in any Phase F file |
| TOML parsing safety | ✅ Pass | Uses stdlib `tomllib` (no code execution from TOML content) |
| Path traversal | ✅ Pass | `resolve_customization.py` uses `Path.resolve()` and doesn't execute paths as commands. Override files are written by the agent following SKILL.md, not by the script itself |
| Symlink risks | ✅ Pass | `list_customizable_skills.py` uses `p.is_dir()` which follows symlinks but doesn't execute anything. The scan is read-only (reads TOML + SKILL.md frontmatter) |
| On Complete hook | ✅ Pass | Step-04's hook runs resolve_customization.py which is read-only. The resolved `on_complete` value is an instruction for the agent, not shell-executed code |
| File writes | ✅ Pass | bmad-customize SKILL.md explicitly requires user confirmation before writing ("Wait for explicit yes") and shows diff before overwrite |
| Error handling | ✅ Pass | All TOML parse errors, missing files, and OS errors are caught and reported to stderr with appropriate exit codes |

---

## Performance Assessment

| Check | Status | Notes |
|-------|--------|-------|
| Directory scan efficiency | ✅ Pass | `list_customizable_skills.py` does a single `iterdir()` per skills root, filters by `customize.toml` existence. O(n) where n = number of skill directories. No recursive descent |
| TOML I/O | ✅ Pass | `resolve_customization.py` reads at most 3 TOML files (defaults + team + user). No unnecessary I/O |
| Plugin load impact | ✅ Pass | 30 customize.toml files are parsed on-demand only when bmad-customize skill is invoked, not at plugin load |
| Test suite runtime | ✅ Pass | 248 tests + 94 subtests in 1.24s. No regression from Phase F additions |
| File sizes | ✅ Pass | All new files under 233 lines. Rule of 500 satisfied with margin |

---

## Simplification Assessment

| Check | Status | Notes |
|-------|--------|-------|
| resolve_customization.py complexity | ✅ Pass | 233 lines, clean separation of concerns (load, merge, extract, main). The 3-layer merge logic is inherently the right level of abstraction — no unnecessary complexity introduced by A0 adaptation |
| list_customizable_skills.py complexity | ✅ Pass | 231 lines, single-responsibility scanner. Could theoretically be simplified but every function earns its place |
| Test redundancy | ✅ Pass | Tests are focused with clear intent. No redundant assertions observed |
| Dead code | ✅ Pass | No dead code, unused imports, or commented-out blocks in any Phase F file |

---

## Files Reviewed

### Implementation (read in full)
- `scripts/resolve_customization.py` (233 lines)
- `skills/bmad-customize/SKILL.md` (120 lines)
- `skills/bmad-customize/scripts/list_customizable_skills.py` (231 lines)
- `skills/bmad-bmm/workflows/3-solutioning/create-architecture/steps/step-07-validation.md` (368 lines)
- `skills/bmad-bmm/workflows/3-solutioning/create-epics-and-stories/steps/step-02-design-epics.md` (262 lines)
- `skills/bmad-bmm/workflows/3-solutioning/create-epics-and-stories/steps/step-04-final-validation.md` (180 lines)

### Configuration
- `plugin.yaml`
- `skills/bmad-init/core/config.yaml`
- `skills/bmad-bmm/config.yaml`
- `skills/bmad-cis/config.yaml`
- `skills/bmad-tea/config.yaml`
- `skills/bmad-bmb/config.yaml`

### Tests
- `tests/test_resolve_customization.py` (122 lines)
- `tests/test_phase_f_workflow_steps.py` (118 lines)
- `tests/test_phase_f_config.py` (87 lines)
- `tests/test_bmad_customize_skill.py` (104 lines)

### Spot-checked
- `skills/bmad-bmm/agents/pm/customize.toml` (agent surface)
- `skills/bmad-bmm/workflows/3-solutioning/create-architecture/customize.toml` (workflow surface)
- `CHANGELOG.md` (Phase F section)
- 30 customize.toml files (validated via test suite — parseable, correct sections)

### Upstream diffs
- step-07-validation.md vs upstream bmad-create-architecture
- step-02-design-epics.md vs upstream bmad-create-epics-and-stories
- step-04-final-validation.md vs upstream bmad-create-epics-and-stories

---

## Verification Story

- **Tests reviewed:** Yes — 248 tests pass (200 original + 48 Phase F). Tests cover script existence, imports, help output, deep merge semantics, A0 path conventions, config versions, workflow step content, TOML validity, and plugin metadata.
- **Build verified:** Yes — `python -m pytest tests/ -v --tb=short` completes in 1.24s with 0 failures.
- **Security checked:** Yes — no secrets, no injection vectors, safe TOML parsing, controlled file writes with user confirmation.
- **Upstream sync verified:** Yes — all 3 P0 files diffed against upstream. All differences are intentional A0 adaptations. No content lost or accidentally overwritten.
