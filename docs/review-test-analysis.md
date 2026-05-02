# Test Quality Analysis Report

**Project:** A0 BMAD Method  
**Date:** 2026-05-02  
**Files Analyzed:** 56  
**Total Test Methods:** 446  
**Total Test Classes:** 132  
**Total Lines of Test Code:** 5,269

---

## Executive Summary

The BMAD Method test suite contains 56 test files with 446 test methods across 132 classes. The suite is predominantly a **structural validation suite** rather than a behavioral test suite. Tests verify file existence, YAML parsability, string inclusion in source files, and configuration correctness. While this is appropriate for a configuration-heavy plugin project, the suite has significant gaps in behavioral testing, error-path coverage, and isolation practices.

**Overall Test Quality Score: 6.0/10**

---

## Per-File Analysis

### test_activation_sequence.py
- **Classes:** 4 | **Methods:** 25 | **LOC:** 135
- **Tests:** Validates the activation sequence steps in bmad-agent-shared.md
- **Framework:** pytest
- **Quality:** Good structure with dedicated classes per concern (sequence, sidecar, fallback, existing sections). Tests behavior of activation step ordering and content. Edge case for resolver failure is present. No mocks needed - reads actual files.

### test_activation_step_order.py
- **Classes:** 4 | **Methods:** 15 | **LOC:** 121
- **Tests:** Verifies the 8-step activation sequence appears in correct order
- **Framework:** plain asserts
- **Quality:** Tests ordering relationships (step N before step N+1) which is meaningful behavioral testing. Good coverage of sidecar instructions and resolve_customization references.

### test_agent_consolidation.py
- **Classes:** 4 | **Methods:** 13 | **LOC:** 106
- **Tests:** Validates consolidated agent directories and menu mappings
- **Framework:** unittest
- **Quality:** Checks removed directories (bmad-sm, bmad-qa, bmad-quick-dev) and menu code mappings. Mix of existence and content checks. No module docstring.

### test_agent_menu_completeness.py
- **Classes:** 8 | **Methods:** 10 | **LOC:** 116
- **Tests:** Verifies each agent customize.toml has valid menu codes
- **Framework:** plain asserts
- **Quality:** Good breadth across 8 agent types. Tests menu count and code validity. Lightweight assertions (file exists + content checks). No behavioral testing.

### test_api_dead_imports.py
- **Classes:** 1 | **Methods:** 4 | **LOC:** 51
- **Tests:** Ensures no dead imports remain in the API module
- **Framework:** unittest
- **Quality:** Implementation-detail heavy (checks specific import patterns in source text). Useful as a lint guard but fragile to refactoring. No module docstring.

### test_bash_hardening.py
- **Classes:** 1 | **Methods:** 4 | **LOC:** 45
- **Tests:** Validates bmad-init.sh uses safe bash patterns
- **Framework:** unittest
- **Quality:** Good static analysis of bash script (set -euo pipefail, rsync pattern, stderr redirects). No runtime execution testing. No module docstring.

### test_bmad_customize_skill.py
- **Classes:** 3 | **Methods:** 11 | **LOC:** 104
- **Tests:** Validates bmad-customize skill structure and TOML files
- **Framework:** unittest
- **Quality:** Good coverage of skill.md, list_customizable_skills script, and TOML files. Has module docstring. Tests script execution (test_script_runs) which is behavioral.

### test_bmad_dashboard_html.py
- **Classes:** 1 | **Methods:** 2 | **LOC:** 52
- **Tests:** Checks dashboard HTML has balanced tags
- **Framework:** unittest
- **Quality:** Minimal - only checks div and template tag balance. Does not test dashboard functionality, data loading, or rendering. Significantly under-tested.

### test_bmad_init_sh.py
- **Classes:** 1 | **Methods:** 10 | **LOC:** 183
- **Tests:** Validates bmad-init.sh script structure and generated config
- **Framework:** unittest
- **Quality:** Thorough static analysis (syntax check, strict mode, no hardcoded paths, config path rows). Does not execute the script. Good for its scope.

### test_bmad_init_skill.py
- **Classes:** 1 | **Methods:** 5 | **LOC:** 37
- **Tests:** Verifies bmad-init SKILL.md has expected trigger patterns
- **Framework:** unittest
- **Quality:** Simple content inclusion checks for slash commands. Adequate for trigger pattern validation.

### test_bmad_routing_logging.py
- **Classes:** 1 | **Methods:** 5 | **LOC:** 120
- **Tests:** Validates routing extension has proper logging and error handling
- **Framework:** unittest
- **Quality:** Checks for import patterns, no bare except/pass, and proper log.warning calls. Source-text scanning - implementation-detail focused.

### test_bmad_status_api.py
- **Classes:** 1 | **Methods:** 2 | **LOC:** 40
- **Tests:** Checks spec None handling in status API
- **Framework:** unittest
- **Quality:** Very thin - only 2 tests checking source text for None guards. Does not actually call the API functions.

### test_bmad_status_core.py
- **Classes:** 2 | **Methods:** 10 | **LOC:** 92
- **Tests:** Validates status core regex patterns and imports
- **Framework:** unittest
- **Quality:** Mix of behavioral (regex compilation flags, read_state return values) and implementation checks. One of few files testing return values.

### test_c1_dual_read.py
- **Classes:** 1 | **Methods:** 7 | **LOC:** 54
- **Tests:** Ensures no dual-read (fallback) patterns remain in code
- **Framework:** unittest
- **Quality:** Regression guard - checks source text for removed fallback patterns. Effective for preventing regression but implementation-detail focused.

### test_c2_bmm_triggers.py
- **Classes:** 1 | **Methods:** 4 | **LOC:** 83
- **Tests:** Validates BMM skill trigger patterns
- **Framework:** unittest
- **Quality:** Checks SKILL.md files have trigger_patterns with slash commands. Appropriate validation for discoverability.

### test_c3_cis_triggers.py
- **Classes:** 1 | **Methods:** 4 | **LOC:** 63
- **Tests:** Validates CIS skill trigger patterns
- **Framework:** unittest
- **Quality:** Same pattern as C2. Consistent approach across modules.

### test_c4_tea_triggers.py
- **Classes:** 1 | **Methods:** 4 | **LOC:** 68
- **Tests:** Validates TEA skill trigger patterns
- **Framework:** unittest
- **Quality:** Same pattern as C2/C3. Uniform.

### test_c5_bmb_triggers.py
- **Classes:** 1 | **Methods:** 4 | **LOC:** 62
- **Tests:** Validates BMB skill trigger patterns
- **Framework:** unittest
- **Quality:** Same pattern as C2-C4.

### test_c6_core_triggers.py
- **Classes:** 1 | **Methods:** 4 | **LOC:** 78
- **Tests:** Validates core skill trigger patterns
- **Framework:** unittest
- **Quality:** Same consistent trigger pattern validation.

### test_c7_verification.py
- **Classes:** 3 | **Methods:** 10 | **LOC:** 157
- **Tests:** Comprehensive YAML schema, trigger, and routing extension verification
- **Framework:** unittest
- **Quality:** Well-structured with 3 test classes covering schemas, triggers, and routing. Good error handling tests (3 tests). One of the better files.

### test_cis_personas.py
- **Classes:** 3 | **Methods:** 7 | **LOC:** 125
- **Tests:** Validates CIS agent titles are generic (no persona names) and icons are unique
- **Framework:** unittest
- **Quality:** Good behavioral testing for persona removal and icon uniqueness. Positive.

### test_constants_consolidation.py
- **Classes:** 1 | **Methods:** 7 | **LOC:** 59
- **Tests:** Ensures constants are centralized in core module
- **Framework:** unittest
- **Quality:** Regression guard checking no literal constants in API/CLI modules. Implementation-detail but valuable.

### test_core_csv_schema.py
- **Classes:** 1 | **Methods:** 4 | **LOC:** 51
- **Tests:** Validates core module YAML schema correctness
- **Framework:** unittest
- **Quality:** Good YAML schema validation. Checks parsing, required fields, and no old field names.

### test_d1_shared_fragment.py
- **Classes:** 1 | **Methods:** 4 | **LOC:** 41
- **Tests:** Validates shared prompt fragment structure
- **Framework:** unittest
- **Quality:** Checks existence, sections, and absence of role/skills in shared fragment. Appropriate structural test.

### test_d2_audit_specifics.py
- **Classes:** 1 | **Methods:** 4 | **LOC:** 79
- **Tests:** Validates agent-specific sections across agents
- **Framework:** unittest
- **Quality:** Tests that master agent differs from non-master and sections are identical across non-master. Good behavioral check.

### test_d3_include_directive.py
- **Classes:** 1 | **Methods:** 5 | **LOC:** 67
- **Tests:** Validates include directive usage across agent prompts
- **Framework:** unittest
- **Quality:** Tests that non-master agents use include while retaining role section and skills table. Good.

### test_d4_master_table.py
- **Classes:** 1 | **Methods:** 4 | **LOC:** 43
- **Tests:** Validates static agent table removal and dynamic replacement
- **Framework:** unittest
- **Quality:** Checks placeholder exists and static table removed. Appropriate regression guard.

### test_d5_recommend_caching.py
- **Classes:** 1 | **Methods:** 3 | **LOC:** 51
- **Tests:** Validates recommend function accepts precomputed params
- **Framework:** unittest
- **Quality:** Source-text checks for caching optimization. Implementation-detail focused.

### test_d6_error_display.py
- **Classes:** 1 | **Methods:** 3 | **LOC:** 49
- **Tests:** Validates error display uses text format (not raw HTML)
- **Framework:** unittest
- **Quality:** Good - tests both absence of raw HTML and presence of text-based error display.

### test_d7_project_context.py
- **Classes:** 1 | **Methods:** 3 | **LOC:** 40
- **Tests:** Validates project-context.md creation stub
- **Framework:** unittest
- **Quality:** Tests creation and idempotency of project context. Thin but functional.

### test_d8_party_mode.py
- **Classes:** 2 | **Methods:** 13 | **LOC:** 146
- **Tests:** Validates party mode acceptance criteria and manifest data
- **Framework:** unittest
- **Quality:** One of the better test files. Tests 10 acceptance criteria (AC01-AC10) covering manifest fields, roster display, agent selection, communication style. Behavioral focus.

### test_dashboard_store.py
- **Classes:** 1 | **Methods:** 2 | **LOC:** 37
- **Tests:** Validates dashboard store error state initialization
- **Framework:** unittest
- **Quality:** Minimal - only 2 tests checking error in initial state. Store.js has many more functions untested.

### test_dead_code.py
- **Classes:** 2 | **Methods:** 4 | **LOC:** 46
- **Tests:** Ensures dead code constants are removed
- **Framework:** unittest
- **Quality:** Regression guard for removed constants and duplicate phase maps. Effective.

### test_edge_cases_verify.py
- **Classes:** 6 | **Methods:** 21 | **LOC:** 236
- **Tests:** Edge cases for VERIFY phase (read_state, routing, dashboard, init)
- **Framework:** pytest
- **Quality:** One of the best files. Tests malformed files, empty files, partial state, nonexistent files, uppercase normalization. 11 read_state edge cases. Good behavioral testing with return value checks.

### test_extension_80.py
- **Classes:** 4 | **Methods:** 15 | **LOC:** 280
- **Tests:** Unit tests for routing manifest artifact-detection helpers
- **Framework:** unittest
- **Quality:** Best test file in the suite. Tests parse_alias_map, resolve_dir, scan_artifact_existence with actual function calls and return value assertions. 5 edge cases including invalid paths and missing configs. Has module docstring.

### test_fix1_routing_vars.py
- **Classes:** 1 | **Methods:** 4 | **LOC:** 66
- **Tests:** Validates routing extension has _SKILLS_DIR and _BMAD_CONFIG_DIR
- **Framework:** unittest
- **Quality:** Source-text checks for variable existence. Appropriate regression guard for a specific fix.

### test_fix2_loading_state.py
- **Classes:** 1 | **Methods:** 3 | **LOC:** 79
- **Tests:** Validates dashboard store resets loading on both success and error
- **Framework:** unittest
- **Quality:** Good - tests both happy and error paths for loading state reset. Behavioral intent.

### test_fix3_csv_cache.py
- **Classes:** 1 | **Methods:** 3 | **LOC:** 66
- **Tests:** Validates artifact scan uses cached YAML reads
- **Framework:** unittest
- **Quality:** Source-text checks for caching pattern. Implementation-detail but targets a specific performance fix.

### test_integration.py
- **Classes:** 2 | **Methods:** 6 | **LOC:** 114
- **Tests:** Integration tests for init script and YAML routing
- **Framework:** unittest
- **Quality:** Tests init creates directories and config files, verifies idempotency. YAML routing tests check all modules parse. Good integration coverage for init.

### test_module_yaml_schema.py
- **Classes:** 4 | **Methods:** 11 | **LOC:** 231
- **Tests:** Validates all module.yaml files follow schema conventions
- **Framework:** unittest
- **Quality:** Thorough schema validation across 4 test classes. Checks files exist, parse, have required fields, code matches module name, workflow count, menu code uniqueness. Good.

### test_mtime_caching.py
- **Classes:** 1 | **Methods:** 4 | **LOC:** 45
- **Tests:** Validates mtime-based caching in routing extension
- **Framework:** unittest
- **Quality:** Source-text checks for mtime key usage. Implementation-detail focused.

### test_mtime_fallback.py
- **Classes:** 4 | **Methods:** 8 | **LOC:** 90
- **Tests:** Validates mtime fallback patterns are removed or gated
- **Framework:** unittest
- **Quality:** Tests that fallback scans are removed from API and routing, and dev-mode is gated. Good behavioral intent.

### test_phase_f_config.py
- **Classes:** 4 | **Methods:** 8 | **LOC:** 87
- **Tests:** Validates Phase F config migration (versions, project name, changelog)
- **Framework:** unittest
- **Quality:** Good phase-specific validation. Checks config versions, project name location, and changelog entries.

### test_phase_f_workflow_steps.py
- **Classes:** 3 | **Methods:** 17 | **LOC:** 118
- **Tests:** Validates Phase F workflow step content synchronization
- **Framework:** unittest
- **Quality:** Tests specific workflow step content (checklists, conditional status, frontmatter). Content-heavy checks but validates important business rules.

### test_phase_g_compliance.py
- **Classes:** 1 | **Methods:** 3 | **LOC:** 67
- **Tests:** Validates MANDATORY PROCESS COMPLIANCE section in agent files
- **Framework:** unittest
- **Quality:** Checks all 20 agents have compliance section before persona. Good structural validation.

### test_phase_g_full.py
- **Classes:** 8 | **Methods:** 29 | **LOC:** 206
- **Tests:** Comprehensive Phase G verification (10 agent prompt fixes)
- **Framework:** unittest
- **Quality:** Largest test file. 8 classes covering solving include, fragment content, clarification, master specifics, subordinate mode, A0 integration, edge cases, and failure analysis. Thorough.

### test_phase_g_include.py
- **Classes:** 4 | **Methods:** 12 | **LOC:** 109
- **Tests:** Validates shared fragment include resolution for non-master agents
- **Framework:** unittest
- **Quality:** Tests include directive usage, agent counts, and shared content sections. Good.

### test_phase_h_paths.py
- **Classes:** 4 | **Methods:** 18 | **LOC:** 142
- **Tests:** Validates Phase H BMB creation path fixes and config split
- **Framework:** pytest
- **Quality:** Tests config file split, step file paths, init script, and celebrate steps. Good coverage of path migration.

### test_phase_h_promote.py
- **Classes:** 4 | **Methods:** 17 | **LOC:** 137
- **Tests:** Validates promote skill NAME validation, TYPE routing, and error handling
- **Framework:** pytest
- **Quality:** One of the best files. Tests input validation (reject slashes, double dots, path traversal), type routing, and error handling. Good edge cases.

### test_plugin_yaml.py
- **Classes:** 1 | **Methods:** 2 | **LOC:** 24
- **Tests:** Validates plugin.yaml has per-project config enabled
- **Framework:** unittest
- **Quality:** Minimal - only 2 assertions. Does not validate other plugin.yaml fields.

### test_project_context_loading.py
- **Classes:** 4 | **Methods:** 9 | **LOC:** 93
- **Tests:** Validates project context loading across workflows and customize.toml
- **Framework:** pytest
- **Quality:** Good coverage of persistent facts, file prefix handling, glob patterns, and workflow pre-steps.

### test_project_context_workflows.py
- **Classes:** 3 | **Methods:** 4 | **LOC:** 96
- **Tests:** Validates all implementation workflows reference project-context.md
- **Framework:** plain asserts
- **Quality:** Cross-references workflow steps with project context. Structural validation.

### test_resolve_customization.py
- **Classes:** 5 | **Methods:** 12 | **LOC:** 121
- **Tests:** Validates resolve_customization.py script and deep_merge function
- **Framework:** unittest
- **Quality:** One of the best files. Tests script existence, help output, imports, deep_merge behavior (4 test cases), and A0 path conventions. Actual behavioral testing.

### test_sidecar_memory.py
- **Classes:** 4 | **Methods:** 10 | **LOC:** 99
- **Tests:** Validates sidecar memory directories and import skill
- **Framework:** pytest
- **Quality:** Tests 16 sidecar directories, idempotency, import skill existence, and shared prompt reference. Good.

### test_user_prefs.py
- **Classes:** 1 | **Methods:** 4 | **LOC:** 52
- **Tests:** Validates user preferences file creation and no-clobber behavior
- **Framework:** unittest
- **Quality:** Tests that init creates user prefs and does not clobber existing. Good idempotency testing.

### test_yaml_routing_completeness.py
- **Classes:** 4 | **Methods:** 10 | **LOC:** 110
- **Tests:** Validates all module.yaml workflow codes are present and unique
- **Framework:** pytest
- **Quality:** Good coverage of YAML routing: discovery, code completeness (75+ codes), module-scoping, no CSV in production, and extension YAML imports.

---

## Test Coverage by Area

| Area | Test Count | Files | Assessment |
|------|-----------|-------|------------|
| Init / Activation | 55 | 4 | Good coverage of init scripts and activation sequence |
| Routing | 45 | 5 | Good coverage of routing extension, YAML routing, artifact detection |
| Phase G | 44 | 3 | Excellent coverage of agent prompt architecture changes |
| D-Series (Shared Fragments) | 39 | 8 | Good coverage of include directives, audit specifics, party mode |
| C-Series (Triggers/Schema) | 37 | 7 | Consistent trigger pattern and schema validation |
| Phase H | 35 | 2 | Good coverage of path fixes and promote validation |
| Agents | 30 | 3 | Good agent consolidation and menu validation |
| YAML Schema | 27 | 4 | Good module YAML and core schema validation |
| Phase F | 25 | 4 | Good config migration and workflow step validation |
| Edge Cases | 21 | 1 | Good edge case coverage for VERIFY phase |
| Triggers | 20 | 5 | Consistent trigger pattern validation across modules |
| Status / Dashboard | 16 | 4 | Thin - dashboard HTML and store are under-tested |
| Project Context | 16 | 2 | Good coverage of loading and workflow integration |
| Sidecar | 10 | 1 | Adequate for directory structure and import |
| Fixes | 10 | 3 | Targeted regression guards for specific bugs |
| Integration | 6 | 1 | Minimal - only tests init script and YAML parsing |

---

## Overall Assessment

### Test Count

- **Actual:** 446 test methods across 56 files
- **Expected:** ~503 (per user specification)
- **Gap:** 57 methods (11.3% shortfall)
- **Note:** The gap may come from methods counted differently (e.g., helper methods vs test methods, or methods in __init__ files)

### Test Quality Score: 6.0 / 10

| Dimension | Score | Notes |
|-----------|-------|-------|
| Coverage Breadth | 7/10 | Good coverage of configs, schemas, triggers, agents |
| Coverage Depth | 5/10 | Mostly surface-level checks, few deep behavioral tests |
| Behavioral Testing | 4/10 | 44% of tests are string-inclusion checks on source text |
| Edge Case Coverage | 5/10 | 31 edge-case methods (7%), concentrated in 2-3 files |
| Error Path Testing | 3/10 | Only 10 tests check error handling |
| Mock Usage | 2/10 | Zero mocks - all tests read actual files |
| Assertion Quality | 6/10 | Mix of self.assert* (396) and bare assert (187) |
| Documentation | 4/10 | 37/56 files missing module docstrings |
| Anti-patterns | 8/10 | No flaky patterns, no sleep, no network calls |
| Maintainability | 6/10 | Consistent structure but many tests would break on refactoring |

---

## Anti-Patterns Detected

### 1. Source-Text Scanning (MAJOR)
- **198 tests** (44%) check string inclusion in source files rather than testing behavior
- Pattern: `assert "some_string" in source.read_text()`
- Risk: Tests break on variable renaming, comment changes, or whitespace modifications
- Files most affected: test_c2-c6_triggers (all 20 tests), test_api_dead_imports, test_bmad_routing_logging, test_constants_consolidation

### 2. Zero Mock Usage (MAJOR)
- No test uses unittest.mock, pytest.mock, or any test double
- All tests read actual production files from disk
- No isolation between tests - all share the same file system state
- Risk: Tests depend on specific project directory structure; cannot test error paths easily

### 3. Implementation-Detail Coupling (MODERATE)
- 52 tests check file existence paths rather than functional outcomes
- Many tests verify internal variable names (_SKILLS_DIR, _BMAD_CONFIG_DIR) rather than behavior
- Tests for removed code (dead code, dual-read, fallbacks) are regression guards tied to specific text patterns

### 4. Missing Module Docstrings (MODERATE)
- 37 of 56 files (66%) have no module-level docstring
- Makes it harder to understand test purpose without reading all test names

### 5. No Parametrized Tests (MINOR)
- No test uses @pytest.mark.parametrize despite 7 files using pytest
- Leads to repetitive test patterns (especially in c2-c6 trigger tests)

### 6. Dashboard Under-Testing (MINOR)
- bmad-dashboard-store.js has 1 test file with 2-4 tests
- bmad-dashboard.html has 1 test file with 2 tests
- No tests for actual store functionality (state management, API calls, rendering)

---

## Gaps: What is NOT Tested

### Critical Gaps

1. **Runtime Script Execution**
   - bmad-init.sh is only statically analyzed, never executed
   - bmad-state-write.sh has zero tests
   - promote.sh has validation tests but no execution tests
   - import-sidecars.sh has no tests

2. **Python Script Execution**
   - resolve_customization.py: tests imports and deep_merge but not actual execution with arguments
   - list_customizable_skills.py: only tests that it runs, not output correctness
   - bmad-status.py: zero tests for the status CLI script
   - All bmad-bmb scripts (validate-file-refs.py, generate-html-report.py, etc.): zero tests

3. **API Endpoint Testing**
   - _bmad_status.py: only 2 tests checking source text for None guards
   - No tests actually call the API functions with inputs
   - No HTTP-level testing

4. **Routing Extension Execution**
   - _80_bmad_routing_manifest.py: test_extension_80.py tests helper functions but not the main execute() flow
   - No tests for end-to-end routing with actual user messages

### Moderate Gaps

5. **Dashboard JavaScript**
   - store.js: only loading state and error initialization tested
   - No tests for: create_store, state mutations, event handlers, API refresh cycle

6. **Agent YAML Configuration**
   - No tests for agent.yaml files in agents/ directories
   - No validation of agent prompt file structure consistency

7. **WebUI Extensions**
   - sidebar-quick-actions-main-start: zero tests

8. **Error Paths**
   - Only 10 tests across the entire suite check error handling
   - No tests for: corrupt YAML files, permission errors, missing directories at runtime, disk full scenarios

9. **Concurrent / Race Conditions**
   - mtime-caching has no tests for concurrent file access
   - No tests for parallel init script execution

10. **Performance**
    - No benchmarks for routing extension latency
    - No tests for large YAML file handling
    - No memory usage tests

---

## Recommendations

### Priority 1: Add Behavioral Tests for Python Functions
- Test resolve_customization.py with actual temp directories and real file merges
- Test bmad_status_core.read_state() with temp files containing various states
- Test _80_bmad_routing_manifest functions with isolated fixtures

### Priority 2: Add Runtime Script Tests
- Execute bmad-init.sh in a temp directory and verify output
- Execute promote.sh with valid and invalid inputs
- Test bmad-state-write.sh state transitions

### Priority 3: Introduce Mocking for Isolation
- Mock file system operations for error-path testing
- Use pytest fixtures with tmp_path for isolated tests
- Add pytest.mark.parametrize to reduce duplication in trigger tests

### Priority 4: Expand Dashboard and API Coverage
- Test store.js functions (create_store, refresh, state management)
- Test _bmad_status.py API functions with real inputs
- Add HTML rendering validation

### Priority 5: Add Module Docstrings
- Add purpose descriptions to all 37 files missing docstrings
- Follow pattern from well-documented files (test_extension_80.py, test_phase_f_config.py)

---

## Test Method Count Reconciliation

| Source | Count |
|--------|-------|
| AST-parsed test methods | 446 |
| Expected total | ~503 |
| Discrepancy | 57 |

The discrepancy likely stems from:
- Helper methods (setUp, class methods) counted differently
- Possible count from a different test runner output including fixtures
- Some test files may have been added/removed since the ~503 count was established
- Nested test functions or parametrized expansions not captured by AST

---

## Top 5 Best Test Files

1. **test_extension_80.py** (15 tests, 280 LOC) - Tests actual function behavior with return values and edge cases
2. **test_edge_cases_verify.py** (21 tests, 236 LOC) - Comprehensive edge case coverage for read_state
3. **test_resolve_customization.py** (12 tests, 121 LOC) - Behavioral testing of deep_merge function
4. **test_phase_h_promote.py** (17 tests, 137 LOC) - Input validation and error handling testing
5. **test_d8_party_mode.py** (13 tests, 146 LOC) - Acceptance criteria validation with behavioral focus

## Top 5 Weakest Test Files

1. **test_plugin_yaml.py** (2 tests, 24 LOC) - Only checks one boolean field
2. **test_dashboard_store.py** (2 tests, 37 LOC) - Only checks initial state
3. **test_bmad_status_api.py** (2 tests, 40 LOC) - Only checks source text
4. **test_bmad_dashboard_html.py** (2 tests, 52 LOC) - Only checks tag balance
5. **test_d7_project_context.py** (3 tests, 40 LOC) - Minimal creation check only
