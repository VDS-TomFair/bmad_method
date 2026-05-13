# Phase H Code Review — BMB Creation Path Fixes

**Reviewer:** Code Reviewer (Agent Zero)
**Date:** 2026-05-01
**Phase:** H — BMB Creation Path Fixes (5 tasks, 6 commits)
**Scope:** config.yaml split, 70 step files, promote skill, init script, celebrate updates

---

## Review Summary

**Verdict:** REQUEST CHANGES — 2 Important issues must be addressed before merge

**Overview:** Phase H delivers a well-architected fix for the BMB creation path problem. The config split (staging vs build output) is clean, the 70 step file updates are comprehensive and consistent, A0 path alignment is verified correct, and the celebrate step rewrite replaces confusing installation instructions with clear auto-discovery guidance. However, `promote.sh` has a path traversal vulnerability — the `NAME` parameter is unsanitized before path construction and `rm -rf`, allowing an attacker or misconfigured agent to write/delete outside intended directories. A second issue is a spec compliance gap: SPEC.md requires a `/promote-skill` trigger that is not implemented.

---

## Critical Issues

None.

---

## Important Issues

### 1. Path Traversal Vulnerability in promote.sh

**File:** `skills/bmad-promote/scripts/promote.sh` (lines 29-31, 49-50, 67)
**Severity:** Important

**Problem:** The `NAME` parameter (`$2`) is used directly in path construction without validation:

```bash
NAME="$2"                              # Unvalidated user input
SOURCE="${PROJECT_ROOT}/.a0proj/${SUBDIR}/${NAME}"    # Line 49
TARGET="/a0/usr/plugins/bmad_method/${SUBDIR}/${NAME}" # Line 50
```

If `NAME="../../../etc/cron.d/malicious"`, the constructed paths traverse out of the intended directories. Combined with line 67 (`rm -rf "$TARGET"`), this becomes a destructive path traversal — an agent or user invoking `promote.sh agent "../../somewhere"` could delete arbitrary directories and write to arbitrary locations.

**Attack vector:**
```
NAME="../../../tmp/evil"
SOURCE → /project/.a0proj/agents/../../../tmp/evil → /tmp/evil (may not exist, exits 2)
NAME="../../usr/share/doc"
SOURCE → /project/.a0proj/agents/../../usr/share/doc → /usr/share/doc (exists on many systems)
TARGET → /a0/usr/plugins/bmad_method/agents/../../usr/share/doc → /a0/usr/share/doc
With PROMOTE_FORCE=true: rm -rf /a0/usr/share/doc, then cp -R /usr/share/doc /a0/usr/share/doc
```

**Recommended fix:** Add NAME validation immediately after line 31:

```bash
# --- Validate name (prevent path traversal) ---
if [[ "$NAME" =~ / ]] || [[ "$NAME" =~ \.\. ]] || [[ "$NAME" =~ ^- ]]; then
    echo "ERROR: Invalid name '$NAME'. Must not contain '/', '..', or start with '-'."
    exit 1
fi
```

**Impact:** In practice, A0 agents are the primary callers and NAME comes from directory listings. The SKILL.md instructs agents to validate source existence before calling the script. Risk is mitigated but not eliminated — defense in depth requires the script itself to validate.

---

### 2. Missing `/promote-skill` Trigger — SPEC Compliance Gap

**Files:** `skills/bmad-promote/SKILL.md`, `skills/bmad-promote/scripts/promote.sh`
**Severity:** Important

**Problem:** SPEC.md (lines 749, 920) specifies the promote skill must have these triggers:

> **Triggers:** `/promote-agent`, `/promote-workflow`, `/promote-skill`

The implementation only supports two:
- SKILL.md trigger_patterns: `/promote-agent`, `/promote-workflow` (and text aliases)
- promote.sh case statement: `agent` or `workflow` only
- No `/promote-skill` trigger, no `skill` type handling

**Resolution options:**
- (a) Add `skill` as an alias for `workflow` in promote.sh and SKILL.md (simplest — skills and workflows share the same output path)
- (b) Update SPEC.md to remove `/promote-skill` if it was intentionally omitted

**Recommended:** Option (a) — add `skill) SUBDIR="skills";;` to the case statement and `/promote-skill` to trigger patterns. This is a 2-line change in each file.

---

## Nits

### 3. SPEC Acceptance Criteria Unchecked

**File:** `SPEC.md` (lines 911-927)

All Phase H acceptance criteria remain `[ ]` despite all criteria passing per the test report. Same issue was flagged in Phase G review (finding #3). Update all passing criteria to `[x]`.

### 4. Missing `test_phase_h_promote.py`

**File:** Referenced in SPEC.md (line 367) and test report (note 1)

SPEC lists `tests/test_phase_h_promote.py` as a Phase H deliverable. The file does not exist. The test report notes promote functionality is "partially covered" by `test_phase_h_paths.py` (18 tests). Consider either:
- (a) Creating the file with dedicated promote tests (script execution, error cases, force mode, invalid name rejection)
- (b) Removing the reference from SPEC.md

Tests for the path traversal fix from finding #1 should go here regardless.

### 5. module-help.csv Old Variable Reference

**File:** `skills/bmad-bmb/module-help.csv`

Still references `bmb_creations_output_folder` in the data column. Cosmetic — the CSV maps module commands to config variables. Update to reference new variable names for consistency with the Phase H changes.

---

## FYI

### 6. Config Backward Compatibility Alias

`config.yaml` line 12 keeps `bmb_creations_output_folder` aliased to `bmb_staging_folder`. This is intentional — provides backward compat for any external tooling referencing the old variable. The test suite verifies this alias. Correct design decision.

### 7. Hardcoded Plugin Path in promote.sh

Line 50 hardcodes `TARGET="/a0/usr/plugins/bmad_method/${SUBDIR}/${NAME}"`. This is container-specific. If A0 deployment changes or the plugin directory moves, this breaks. Acceptable for now (matches A0's architecture), but consider making this configurable via environment variable or config lookup in a future iteration.

### 8. TEA Sample File Has Old Path

`skills/bmad-tea/workflows/testarch/teach-me-testing/workflow-plan-teach-me-testing.md` contains hardcoded user paths with `bmb-creations`. This is an out-of-scope sample artifact, not BMB infrastructure. No action needed.

---

## Detailed Axis Review

### Axis 1: Correctness

| Check | Result | Detail |
|-------|--------|--------|
| `bmb_staging_folder` defined | ✅ | `{project-root}/_bmad-output/bmb-staging` |
| `bmb_build_output_agents` defined | ✅ | `{project-root}/agents` |
| `bmb_build_output_skills` defined | ✅ | `{project-root}/skills` |
| Old variable aliased | ✅ | Points to staging for backward compat |
| Agent build → agents path | ✅ | step-07-build-agent.md uses `bmb_build_output_agents` |
| Workflow build → skills path | ✅ | step-11-completion.md uses `bmb_build_output_skills` |
| Staging used for plans/reports | ✅ | discovery, plan, validation steps use `bmb_staging_folder` |
| Old variable purged from step files | ✅ | 0 matches in `workflows/` directory |
| `bmb-creations` purged from step files | ✅ | 0 matches in `workflows/` directory |
| Init creates discoverable dirs | ✅ | `mkdir -p "$A0PROJ/agents"` and `"$A0PROJ/skills"` |
| Celebrate steps updated | ✅ | Auto-discovery guidance, no `npx install` references |

**Path resolution correctness:**
- `{project-root}` in BMAD config → `.a0proj/`
- `{project-root}/agents` → `.a0proj/agents/` → A0 discovers via `usr/projects/*/.a0proj/agents` ✅
- `{project-root}/skills` → `.a0proj/skills/` → A0 discovers via `usr/projects/*/.a0proj/skills` ✅

### Axis 2: Readability & Simplification

| Aspect | Assessment |
|--------|------------|
| Config split (4 variables) | ✅ Clean — each has one clear purpose |
| 70 step file updates | ✅ Mechanical replacement, no logic changes |
| Celebrate step rewrite | ✅ Significantly simpler — removed 30+ lines of installation boilerplate |
| promote.sh (86 lines) | ✅ Well-structured, clear exit codes, good comments |
| promote SKILL.md (142 lines) | ✅ Thorough step-by-step guide with safety checks |

**Chesterton's Fence analysis:** The backward compat alias for `bmb_creations_output_folder` is justified — removing it would break any external tooling or uncommitted BMB sessions. The alias points to staging (not agents/skills), which is semantically correct since the old variable was used for all output including intermediate artifacts.

**Rule of 500 check:** 78 files changed, ~1092 insertions. The bulk is mechanical find-replace across 70 step files (each ~2-line change). The meaningful new code is ~280 lines (promote.sh 86 + SKILL.md 142 + init changes 4 + config changes 8 + celebrate rewrites ~40). Under the 500-line threshold for meaningful code.

### Axis 3: Architecture

| Aspect | Assessment |
|--------|------------|
| Path hierarchy (staging → build output) | ✅ Correct separation of concerns |
| Promote skill (project → plugin scope) | ✅ Clean two-tier scope model |
| Init script dir creation | ✅ Idempotent, follows existing mkdir -p pattern |
| Celebrate step information architecture | ✅ Scopes table is clear and actionable |

**Scope model is well-designed:**

```
BMB Build → .a0proj/agents/{name}/ (project scope, auto-discovered)
         → .a0proj/skills/{name}/ (project scope, auto-discovered)

Promote   → plugins/bmad_method/agents/{name}/ (plugin scope, global)
         → plugins/bmad_method/skills/{name}/ (plugin scope, global)
```

This matches A0's discovery hierarchy exactly. Agents discover project-scope first, plugin-scope as fallback.

### Axis 4: Security

| Check | Result | Detail |
|-------|--------|--------|
| Path traversal in promote.sh | 🟡 See finding #1 | NAME not validated before path construction + rm -rf |
| Secrets in code | ✅ None | No credentials, tokens, or API keys |
| Input validation in promote.sh | 🟡 Partial | TYPE validated via case, NAME not validated |
| Target overwrite protection | ✅ Good | PROMOTE_FORCE required, explicit warning |
| Safe quoting | ✅ All variables quoted | No unquoted expansions |
| No `eval` or `$(...)` injection | ✅ Clean | Only `$(pwd)` and `$(dirname ...)` |

**Severity of finding #1 is moderated by:**
- A0 agents are the primary callers (not end users directly)
- SKILL.md instructs agents to validate source before calling
- Containerized environment limits blast radius
- But defense in depth requires script-level validation

### Axis 5: Performance

| Check | Result | Detail |
|-------|--------|--------|
| Path changes affect runtime | ✅ No | Paths are config strings resolved by BMB engine |
| promote.sh efficiency | ✅ Good | Single cp -R, no loops |
| Init script overhead | ✅ None | Two additional mkdir -p calls |
| Celebrate step size | ✅ Reduced | Net deletion of ~30 lines |

No performance concerns. This is purely a path routing change with no runtime cost impact.

---

## What's Done Well

1. **Comprehensive mechanical update.** 70 step files updated with zero orphan references. The test suite verifies this with two independent grep checks (`bmb_creations_output_folder` and `bmb-creations`). This is exactly how a large-scale find-replace should be executed and verified.

2. **Clean architectural model.** The staging vs build output split is the right abstraction. Intermediate artifacts (plans, reports, validation results) go to staging. Final build artifacts go to A0-discoverable paths. The backward compat alias prevents breaking existing sessions.

3. **Celebrate step rewrite.** Replacing 30+ lines of BMAD installation boilerplate with a concise auto-discovery explanation is a significant improvement. The scope table (project vs plugin) is immediately understandable. The `/promote-agent` call-to-action is clear and actionable.

4. **Promote skill design.** The SKILL.md is thorough — preflight checks, step-by-step execution, safety checks, error handling, and explicit "when this skill can't help" section. The script has clear exit codes and proper overwrite protection. Well-documented for agent consumption.

5. **Test coverage.** 18 Phase H tests covering config split, step file path correctness, init script, and celebrate content. The `test_no_old_variable_in_step_files` and `test_no_bmb_creations_hardcoded_path` tests are particularly valuable — they catch regressions if any step file is reverted or a new file is added with old paths.

6. **Zero regressions.** 310 tests pass, 94 subtests, 0 failures. Every test from Phases A-G continues to pass after the 70-file update.

---

## Verification Story

- **Tests reviewed:** Yes — 310/310 pass (18 Phase H-specific). Tests cover config structure, path variable correctness, orphan reference detection, init script content, and celebrate step content. Coverage is good for config/step-file changes. Missing: dedicated promote.sh execution tests.
- **Build verified:** Yes — `python -m pytest tests/test_phase_h_paths.py -v` → 18 passed in 0.10s.
- **Security checked:** Yes — path traversal vulnerability identified in promote.sh (finding #1). No secrets exposure. Input validation gap for NAME parameter. Safe quoting throughout.

---

## Post-Merge Action Items

| # | Item | Priority | Issue |
|---|------|----------|-------|
| 1 | Add NAME validation to promote.sh | **Pre-merge** | Finding #1 — path traversal |
| 2 | Add `/promote-skill` trigger or update SPEC | **Pre-merge** | Finding #2 — spec compliance |
| 3 | Update SPEC acceptance criteria to `[x]` | Post-merge | Finding #3 |
| 4 | Create `test_phase_h_promote.py` with execution tests | Post-merge | Finding #4 |
| 5 | Update `module-help.csv` variable references | Post-merge | Finding #5 |
