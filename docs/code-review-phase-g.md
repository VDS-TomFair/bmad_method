# Phase G Code Review — Agent Prompt Fixes

**Reviewer:** Code Reviewer (Agent Zero)
**Date:** 2026-05-01
**Phase:** G — Critical Agent Prompt Fixes (10 tasks)
**Scope:** 20 agents × 4 prompt files + 2 shared fragments + docs

---

## Review Summary

**Verdict:** APPROVE — with 1 Important issue to address post-merge

**Overview:** Phase G delivers a well-executed fix for a critical systemic failure where `{{ include }}` silently failed across all 19 non-master BMAD agents. The architectural change (shared fragments in `prompts/`) is correct, the behavioral guardrails (process compliance gate, clean solving override, subordinate detection) are well-designed, and the consistency across all 20 agents is machine-verified. All 292 tests pass. One dangling skill reference needs attention.

---

## Critical Issues

None.

---

## Important Issues

### 1. Dangling `a0-development` Skill Reference in BMB Agents

**Files:**
- `agents/bmad-workflow-builder/prompts/agent.system.main.specifics.md`
- `agents/bmad-agent-builder/prompts/agent.system.main.specifics.md`
- `agents/bmad-module-builder/prompts/agent.system.main.specifics.md`

**Severity:** Important

**Problem:** All three BMB agents contain `A0 Framework Integration` sections that instruct:

```
Load `a0-development` skill to understand framework architecture
```

The `a0-development` skill does not exist in the project (`skills/` directory contains no such skill). When a BMB agent attempts `skills_tool:load a0-development`, it will fail. The agent then falls through to generic behavior — the instruction is misleading rather than dangerous, but it undermines the credibility of the A0 Framework Integration section.

**Recommended fix:** Either:
- (a) Create the `a0-development` skill with A0 framework documentation, or
- (b) Replace the reference with actionable alternatives: `Read A0 framework docs from /a0/prompts/ and /a0/helpers/ to understand architecture`

**Impact:** Low — the rest of the A0 Framework Integration section (reference patterns, call_subordinate, inheritance) is still valid. Non-blocking for merge.

---

## Nits

### 2. CHANGELOG Test Count Outdated

**File:** `CHANGELOG.md` (line ~38)

**Severity:** Nit

**Problem:** CHANGELOG states `Total: 263 tests pass (up from 248)` but the actual suite is now 292 tests. The 29 new `test_phase_g_full.py` tests were added after the CHANGELOG entry was written.

**Fix:** Update to `Total: 292 tests pass (up from 263)`.

### 3. SPEC.md Acceptance Criteria Checkboxes Unchecked

**File:** `SPEC.md` (lines 735-756)

**Severity:** Nit

**Problem:** All Phase G acceptance criteria remain `[ ]` (unchecked) despite all criteria passing per the test report. This creates ambiguity about completion status.

**Fix:** Update all passing criteria to `[x]`.

---

## FYI

### 4. communication_additions.md — 20 Unique Files (Expected)

All 20 `communication_additions.md` files have unique hashes. This is correct — each agent has persona-specific menu content. The `Subordinate Mode Detection` section (identical across all 20, verified by single md5 hash `7dc6dfe4...`) is appended below the unique content. No action needed.

### 5. specifics.md — 5 Variants (Expected)

5 unique hashes across 20 specifics.md files, corresponding to:
- Master (1): unique routing table + module-help.csv reference
- BMB agents (3): identical skill table + A0 Framework Integration
- Test Architect (1): TEA-specific skill table
- Standard module agents (8): BMM skill table
- Creative agents (6): CIS skill table

Each variant differs only in the skill table rows — the shared fragment include and mandatory protocol are identical. Correct by design.

### 6. Token Impact Analysis

Per-agent token additions from Phase G:

| Component | Words | ~Tokens |
|-----------|-------|---------|
| Compliance gate (role.md) | 107 | ~140 |
| Subordinate detection (comm_additions) | 70 | ~90 |
| Shared solving fragment (resolved) | 108 | ~140 |
| Shared fragment (resolved) | 868 | ~1,130 |
| **Total per agent** | **~1,153** | **~1,500** |

At ~1,500 tokens per agent, this is a meaningful increase but justified:
- The shared fragment (868 words) was *supposed* to be there before — it was silently missing due to the broken include
- Net new behavioral content is ~285 tokens per agent (compliance gate + subordinate detection + solving override)
- The compliance gate and solving override serve as critical guardrails against the exact failure that triggered Phase G

### 7. Redundancy Between Compliance Gate and Solving Fragment

The role.md compliance gate (6 MUST statements) and the shared solving fragment (7 numbered steps + "FOLLOW THE PROCESS") both enforce process compliance. This is **intentional layering**, not redundancy:
- **role.md**: Loaded first, sets the behavioral frame before the agent even sees its persona
- **solving.md**: Loaded in the problem-solving slot, applies when the agent is actively working

Both layers are needed because LLMs can "forget" early instructions as context grows. The dual enforcement is a feature.

---

## Detailed Axis Review

### Axis 1: Code Quality

| Check | Result | Detail |
|-------|--------|--------|
| `MANDATORY PROCESS COMPLIANCE` in all 20 role.md | ✅ 20/20 | Identical text, before persona |
| 6-point directive intact | ✅ 20/20 | All 6 MUST statements present |
| `{{ include "bmad-agent-shared.md" }}` in all 20 specifics | ✅ 20/20 | Correct include syntax |
| `{{ include "bmad-agent-shared-solving.md" }}` in all 20 solving | ✅ 20/20 | Single-line files, identical |
| `Subordinate Mode Detection` in all 20 comm_additions | ✅ 20/20 | Consistent section text |
| Skill tables correct per agent group | ✅ 5 variants | BMM, BMB, CIS, TEA, Master |
| Mandatory skill usage protocol | ✅ 20/20 | Identical 5-point protocol |
| `_shared/` directory removed | ✅ Confirmed | Does not exist |

**Prompt text quality:** Well-structured, consistent formatting, clear behavioral directives. No typos found. The `MANDATORY PROCESS COMPLIANCE` section is forceful without being verbose.

**Include usage:** Correct `{{ include "filename" }}` syntax (quoted, no path component) matching A0's `process_includes()` expected format.

**Master specifics conversion:** 109 → 29 lines is clean. The master-specific content (routing table, skill table, loading protocol) is preserved while the shared fragment is now a single include.

### Axis 2: Simplification

| Aspect | Assessment |
|--------|------------|
| Shared fragment approach (2 files in `prompts/`) | ✅ Correct abstraction — right level of sharing |
| 20 solving.md → single-line includes | ✅ Eliminates 720 lines of duplication |
| Master specifics 109→29 lines | ✅ Clean extraction, no content lost |
| Specifics variants (5 groups) | ✅ Each variant has genuine differences (skill tables) |

**Could be further simplified:** The "Mandatory skill usage protocol" (5 points) is duplicated verbatim across all 20 specifics.md files (minus master, which has a variant). This could theoretically be moved into the shared fragment. **However**, this is a Nit-level observation — the current approach keeps the protocol visible in each agent's specifics.md which aids debugging. Not recommended for action.

### Axis 3: Security

| Check | Result | Detail |
|-------|--------|--------|
| Path traversal in `{{ include }}` | ✅ Safe | Filenames only, no path components; A0 resolves via search chain |
| Prompt injection in behavioral directives | ✅ Low risk | Directives are static text, no user-controlled input |
| Secrets in prompt files | ✅ None | No credentials, tokens, or API keys |
| Error disclosure | ✅ N/A | A0 silently returns literal text on failed include — no error messages exposed |
| `!!!` directive in shared fragment | ✅ Safe | A0's native instruction marker, not executable code |

**Note on A0's silent include failure:** The original bug existed because `process_includes()` silently returns the literal `{{ include }}` text on `FileNotFoundError`. Phase G fixed the *symptom* (file not found) by moving the fragment to the correct location. The underlying framework behavior (silent failure) remains. This is an A0 framework concern, not a plugin concern — but it's worth documenting as a known risk.

### Axis 4: Performance

| Check | Result | Detail |
|-------|--------|--------|
| Include resolution efficiency | ✅ Single pass | Resolved at prompt assembly, no runtime cost |
| Unnecessary prompt verbosity | ✅ Minimal | All added content serves clear behavioral purposes |
| `!!!` compression directive in shared fragment | ✅ Good | Instructs agent to output minimal thoughts, reducing response token usage |

**Token budget impact:** ~1,500 tokens/agent increase. For context, typical A0 system prompts are 4,000-8,000 tokens. Phase G adds ~20% to the lower bound, but ~1,130 of those tokens were *supposed to be there* (shared fragment was missing). Net new tokens: ~370 per agent.

---

## What's Done Well

1. **Machine-verified consistency.** Every structural claim (20/20 agents, identical sections, correct ordering) is backed by automated tests (29 tests in `test_phase_g_full.py` alone). This is the gold standard for prompt engineering at scale.

2. **Layered defense against process bypass.** Three independent enforcement layers (role.md compliance gate, shared fragment clarification, solving.md process override) create redundancy that makes shortcut behavior unlikely even if the agent partially ignores one layer.

3. **Clean architectural fix.** Moving from `agents/_shared/prompts/` (invisible to A0) to `prompts/` (in search chain) is the minimal correct fix. No workarounds, no hacks — just putting the file where the framework expects it.

4. **Honest failure analysis and ADR revision.** The revised ADR 0002 is refreshingly candid about the original false claim ("Confirmed working via live A2A testing"). The "Lessons Learned" section turns a bug into institutional knowledge. This is exactly how ADRs should work.

5. **Master specifics conversion.** Reducing bmad-master from 109-line inline to 29-line with include eliminates the last divergence risk. All 20 agents now share the same behavioral base.

6. **Subordinate mode detection.** A practical fix for a real operational problem — agents called via `call_subordinate` would previously display interactive menus to a non-interactive caller. The 5-step detection protocol is concise and actionable.

---

## Verification Story

- **Tests reviewed:** Yes — 292/292 pass (44 Phase G-specific). Tests cover structural integrity, content correctness, edge cases, and VPS deployment. Coverage is comprehensive.
- **Build verified:** Yes — `python -m pytest tests/ -v` → 292 passed in 0.12s (Phase G suite), 292 collected (full suite).
- **Security checked:** Yes — no path traversal, injection, or secret exposure risks. Silent include failure is a framework-level concern documented in ADR 0002.
- **VPS verified:** Yes — per test report, all critical checks confirmed on remote testing instance.

---

## Acceptance Criteria Status

| Criterion | Status |
|-----------|--------|
| P0: `bmad-agent-shared.md` moved to `prompts/` | ✅ PASS |
| P0: `_shared/` directory removed | ✅ PASS |
| P0: Runtime include resolution for all 19 non-master | ✅ PASS (VPS verified) |
| P0: All 20 role.md have compliance before persona | ✅ PASS |
| P0: Initial Clarification rewritten (no escape hatch) | ✅ PASS |
| P0: All 20 solving.md clean override (no high-agency) | ✅ PASS |
| P0: ADR 0002 revised | ✅ PASS |
| P0: All 250+ tests green | ✅ PASS (292) |
| P0: Master specifics converted to include | ✅ PASS |
| P1: Subordinate mode in all 20 comm_additions | ✅ PASS |
| P1: Shared solving fragment exists | ✅ PASS |
| P1: All 20 solving.md reduced to include | ✅ PASS |
| P1: Master response.md include verified | N/A (no response.md) |
| P2: BMB A0 Framework Integration | ✅ PASS (⚠️ skill ref dangling) |
| P2: Failure analysis updated | ✅ PASS |

---

## Post-Merge Action Items

| Priority | Item | Effort |
|----------|------|--------|
| Important | Resolve `a0-development` skill reference in BMB agents | Small |
| Nit | Update CHANGELOG test count (263→292) | Trivial |
| Nit | Check SPEC.md acceptance criteria boxes | Trivial |
