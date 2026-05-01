# Implementation Plan: BMAD Method Plugin — Phase G (Agent Prompt Fixes, v1.3)

## Overview

Fix critical agent prompt defects discovered during bmad-workflow-builder failure analysis. The analysis revealed two systemic failure layers affecting all 20 BMAD agents: a broken `{{ include }}` mechanism (silently failing for 19/20 agents) and conflicting behavioral directives that bias agents toward shortcutting process steps. All changes are prompt text only — no code changes needed.

**Prereq:** Phases A–F COMPLETE (47+ tasks, 250+ tests, 50+ commits).
**Reference:** `docs/workflow-builder-failure-analysis.md` (559 lines)
**Branch:** `develop` → `main` on /ship.
**Version target:** v1.2.0 → v1.3.0
**Test command:** `cd /a0/usr/projects/a0_bmad_method && python -m pytest tests/ -v`

---

## Architecture Decisions

- **R3 uses clean full override for solving.md** — NOT `{{ include original }}` or `{{ extend }}`. BMAD agents need fundamentally different problem-solving behavior (process-driven vs task-driven). The A0 default solving.md contains `"don't accept failure retry be high-agency"` which directly conflicts with BMAD's process requirements. Clean override eliminates conflict entirely.
- **G-P0-1 MUST be done first** — the broken `{{ include }}` prevents verification of all other prompt changes. After moving the shared fragment to `prompts/`, include resolution can be tested empirically on VPS.
- **G-P0-5 depends on G-P0-1** — bmad-master's specifics.md can only be converted from 109-line inline to `{{ include }}` after the include mechanism is verified working.
- **G-P1-2 depends on G-P0-4** — shared solving.md fragment is created from the clean override content written in G-P0-4.
- **All changes are prompt text only** — no Python code, no bash scripts, no HTML. Low risk, fast implementation.
- **`agents/_shared/` directory removed entirely** after G-P0-1 — `_shared` is not a valid A0 profile name, its existence is misleading.
- **ADR 0002 must be revised** — it falsely claims "Confirmed working via live A2A testing." The include silently fails.

---

## Dependency Graph

```
[G-P0-1: Fix broken {{ include }}] ← MUST BE FIRST
         │
         ▼
[VERIFY: Include resolves for all 19 agents on VPS]
         │
    ┌────┼────────────┐
    │    │            │
    ▼    ▼            ▼
[G-P0-2: Compliance gate]  [G-P0-3: Rewrite shared]  [G-P0-4: Rewrite solving.md]
    │    │            │
    │    │            ▼
    │    │    [G-P0-5: Master inline→include] ← depends on G-P0-1
    │    │            │
    ▼    ▼            ▼
[CHECKPOINT P0 — all 5 critical fixes done, tests green]
         │
    ┌────┼────────────┐
    │    │            │
    ▼    ▼            ▼
[G-P1-1: Subordinate mode]  [G-P1-2: Shared solving fragment]  [G-P1-3: Verify master response]
                              ← depends on G-P0-4
         │
         ▼
[CHECKPOINT P1 — high-priority fixes done]
    ┌────┴──────────────────────────┐
    │ G-P2-1: A0 skill awareness    │
    │ G-P2-2: Update failure report │
    └──────────────┬────────────────┘
                   │
          [CHECKPOINT P2 — ready for /ship]
```

**Parallelization:**
- G-P0-2, G-P0-3, G-P0-4 can run in parallel (different files) after G-P0-1
- G-P1-1, G-P1-3 can run in parallel (independent) after P0 checkpoint
- G-P2-1, G-P2-2 can run in parallel (different files) after P1 checkpoint

---

## Phase G — P0: Critical Fixes (5 tasks)

**Gate: G-P0-1 MUST pass before any other P0 work begins. All P0 tasks must pass before P1.**

---

### Task G-P0-1: Fix broken `{{ include }}` — move shared fragment [Size: S]

**SPEC ref:** G-P0-1 (R0)
**Root cause:** RC0 — broken include resolution

**Description:** `{{ include "bmad-agent-shared.md" }}` silently fails for all 19 non-master agents. The file lives in `agents/_shared/prompts/` which is NOT in A0's search path (`_shared` is not a profile name). A0's `helpers/files.py:364` silently returns the literal text on `FileNotFoundError`. All 19 agents are missing 85 lines of behavioral instructions. Move the file to `prompts/` which IS in A0's search chain (priority level 7).

**Changes required:**
1. Move `agents/_shared/prompts/bmad-agent-shared.md` → `prompts/bmad-agent-shared.md`
2. Remove empty `agents/_shared/prompts/` directory
3. Remove empty `agents/_shared/` directory entirely
4. Verify on VPS: A0 framework Python must find `bmad-agent-shared.md` via `find_file_in_dirs()`
5. Test `{{ include "bmad-agent-shared.md" }}` resolves in all 19 non-master agents
6. Update ADR 0002 status to "Revised" with corrected claims
7. Run `python -m pytest tests/ -v` — all 250+ tests green

**Files affected:**
- `agents/_shared/prompts/bmad-agent-shared.md` → MOVE to `prompts/bmad-agent-shared.md`
- `agents/_shared/` → REMOVE (becomes empty after move)
- `docs/adr/0002-shared-fragments-include.md` → UPDATE

**Dependencies:** None (MUST be first task)

**Verification steps:**
- [ ] `prompts/bmad-agent-shared.md` exists with correct content (85 lines)
- [ ] `agents/_shared/` directory removed entirely
- [ ] ADR 0002 revised — status updated, false claims corrected
- [ ] Runtime include resolution verified for all 19 non-master agents on VPS
- [ ] `python -m pytest tests/ -v` — all 250+ tests green

**Risk notes:** Low risk — file move only, no content changes. The `agents/_shared/` directory serves no other purpose. ADR 0002 revision is documentation-only.

**Estimated complexity:** Small — file move + directory cleanup + ADR revision

---

### Task G-P0-2: Add process compliance gate to all 20 role.md files [Size: M]

**SPEC ref:** G-P0-2 (R1)
**Root cause:** RC5 — no process compliance gate

**Description:** None of the 20 BMAD agents contain a non-overridable process compliance directive. `role.md` focuses on OUTPUT quality, not PROCESS adherence. Add `MANDATORY PROCESS COMPLIANCE` section BEFORE the persona definition to every agent's `role.md`.

**Changes required:**
1. Add the following section to ALL 20 agents' `role.md`, BEFORE the persona definition:

```markdown
## MANDATORY PROCESS COMPLIANCE

You are a PROCESS-DRIVEN agent. This means:

1. You MUST load the appropriate BMAD skill before ANY workflow execution
2. You MUST follow the step-file architecture loaded from the skill
3. You MUST execute steps sequentially — NEVER skip or optimize the sequence
4. You MUST read each step file completely before taking action
5. You MUST halt at checkpoints and wait for user input
6. You MUST NOT produce workflow artifacts except through the step-by-step process

Even if you believe you have all requirements, you MUST still follow the step-by-step process.
"Complete task" means complete the PROCESS, not skip to the output.
```

**Files affected (20 files):**
- `agents/bmad-master/prompts/agent.system.main.role.md`
- `agents/bmad-analyst/prompts/agent.system.main.role.md`
- `agents/bmad-architect/prompts/agent.system.main.role.md`
- `agents/bmad-pm/prompts/agent.system.main.role.md`
- `agents/bmad-dev/prompts/agent.system.main.role.md`
- `agents/bmad-ux-designer/prompts/agent.system.main.role.md`
- `agents/bmad-qa/prompts/agent.system.main.role.md`
- `agents/bmad-sm/prompts/agent.system.main.role.md`
- `agents/bmad-tech-writer/prompts/agent.system.main.role.md`
- `agents/bmad-test-architect/prompts/agent.system.main.role.md`
- `agents/bmad-innovation/prompts/agent.system.main.role.md`
- `agents/bmad-design-thinking/prompts/agent.system.main.role.md`
- `agents/bmad-presentation/prompts/agent.system.main.role.md`
- `agents/bmad-storyteller/prompts/agent.system.main.role.md`
- `agents/bmad-brainstorming-coach/prompts/agent.system.main.role.md`
- `agents/bmad-problem-solver/prompts/agent.system.main.role.md`
- `agents/bmad-quick-dev/prompts/agent.system.main.role.md`
- `agents/bmad-workflow-builder/prompts/agent.system.main.role.md`
- `agents/bmad-agent-builder/prompts/agent.system.main.role.md`
- `agents/bmad-module-builder/prompts/agent.system.main.role.md`

**Dependencies:** None (can run in parallel with G-P0-3, G-P0-4 after G-P0-1)

**Verification steps:**
- [ ] `grep -rl 'MANDATORY PROCESS COMPLIANCE' agents/*/prompts/agent.system.main.role.md` → 20 files
- [ ] Compliance section appears BEFORE persona definition in each file
- [ ] `python -m pytest tests/ -v` — all 250+ tests green

**Risk notes:** Low risk — additive text insertion only, no existing content modified.

**Estimated complexity:** Medium — 20 files, but identical content insertion at predictable location

---

### Task G-P0-3: Rewrite shared fragment Initial Clarification (escape hatch removal) [Size: S]

**SPEC ref:** G-P0-3 (R2)
**Root cause:** RC2 — escape hatch in shared fragment

**Description:** The `Initial Clarification` section in `bmad-agent-shared.md` allows agents to rationalize skipping steps if they believe requirements are clear. This escape hatch is moot while RC0 exists (section never loaded), but becomes active after the include fix in G-P0-1. Replace with process-aware clarification.

**Changes required:**
1. Replace the `Initial Clarification` section in `prompts/bmad-agent-shared.md` (now at new location after G-P0-1) with:

```markdown
## Initial Clarification

Before executing any BMAD workflow, confirm understanding of:
- What artifact is being created or modified
- Current project phase alignment
- Output format expectations
- Acceptance criteria
- Constraints to honor

Clarification determines WHICH workflow step to START at, not WHETHER to follow the process.
You ALWAYS follow the step-by-step process — clarification only affects where you begin.

NEVER interpret "I have all requirements" as permission to skip the process.
```

**Files affected:**
- `prompts/bmad-agent-shared.md` (the shared fragment — one change fixes all 19 agents)

**Dependencies:** None (can run in parallel with G-P0-2, G-P0-4 after G-P0-1)

**Verification steps:**
- [ ] `grep 'NEVER interpret' prompts/bmad-agent-shared.md` → found
- [ ] No escape hatch language remains (no "if you have all requirements, you may proceed directly")
- [ ] Clarification section is process-aware
- [ ] `python -m pytest tests/ -v` — all 250+ tests green

**Risk notes:** Low risk — single file edit, content replacement in one section.

**Estimated complexity:** Small — one section replacement in one file

---

### Task G-P0-4: Rewrite solving.md — clean full override (remove high-agency conflict) [Size: M]

**SPEC ref:** G-P0-4 (R3)
**Root cause:** RC1 — conflicting directives in solving.md

**Description:** Line 25 of the current solving.md (`don't accept failure retry be high-agency`) directly conflicts with line 33 (`Follow workflow steps precisely`). LLM task-completion bias resolves toward shortcut. Replace with clean BMAD-specific solving.md — no `{{ include original }}` or `{{ extend }}`. Clean full override eliminates conflict entirely.

**Changes required:**
1. Replace the content of ALL 20 agents' `solving.md` files with the clean BMAD-specific override:

```markdown
## Problem solving

You are a PROCESS-DRIVEN BMAD agent. Process compliance overrides efficiency.

0. Load the appropriate BMAD skill FIRST — no exceptions
1. Follow the step-file architecture loaded from the skill
2. Execute steps sequentially — never skip or optimize the sequence
3. Read each step file completely before taking action
4. Halt at checkpoints and wait for user input
5. Produce artifacts only through the step-by-step process
6. Use `text_editor:patch` for large artifacts
7. Update `02-bmad-state.md` after phase transitions

CRITICAL: "Complete task" means complete the PROCESS, not skip to the output.
If you feel tension between completing the task and following the process,
FOLLOW THE PROCESS.
```

**Files affected (20 files):**
- `agents/bmad-master/prompts/agent.system.main.solving.md`
- `agents/bmad-analyst/prompts/agent.system.main.solving.md`
- ... (all 20 agents' `solving.md` files)

**Dependencies:** None (can run in parallel with G-P0-2, G-P0-3 after G-P0-1)

**Verification steps:**
- [ ] `grep -rl 'PROCESS-DRIVEN BMAD agent' agents/*/prompts/agent.system.main.solving.md` → 20 files
- [ ] No conflicting "high-agency" or "don't accept failure" directive in any solving.md
- [ ] All 20 files have identical content
- [ ] `python -m pytest tests/ -v` — all 250+ tests green

**Risk notes:** Low risk — content replacement only. The clean override is self-contained and does not inherit from A0 framework defaults.

**Estimated complexity:** Medium — 20 files, but identical content replacement

---

### Task G-P0-5: Convert bmad-master specifics.md from 109-line inline to `{{ include }}` [Size: S]

**SPEC ref:** G-P0-5 (R7)
**Root cause:** RC0 + divergence risk

**Description:** bmad-master's `specifics.md` is 109 lines because it inlines all shared content directly — it does NOT use `{{ include }}`. This was the right call when the include was broken (RC0), but creates a divergence risk after G-P0-1+G-P0-3. After those fixes, 19 agents get new process-aware shared content via the rewritten `bmad-agent-shared.md`, but bmad-master keeps its stale 109-line inline version. The two copies will silently diverge.

**Changes required:**
1. Read current `agents/bmad-master/prompts/agent.system.main.specifics.md` (109 lines)
2. Extract master-specific content (persona preamble, master-specific extras)
3. Replace with: persona preamble + `{{ include "bmad-agent-shared.md" }}` + master-specific extras
4. Verify on VPS that include resolves correctly for bmad-master

**Files affected:**
- `agents/bmad-master/prompts/agent.system.main.specifics.md`

**Dependencies:** G-P0-1 (include mechanism must be verified working before master can use it)

**Verification steps:**
- [ ] `grep '{{ include "bmad-agent-shared.md" }}' agents/bmad-master/prompts/agent.system.main.specifics.md` → found
- [ ] File is significantly shorter than 109 lines (inline content removed)
- [ ] Master-specific content preserved (persona preamble, extras)
- [ ] Include resolves on VPS for bmad-master
- [ ] `python -m pytest tests/ -v` — all 250+ tests green

**Risk notes:** Medium risk — must carefully extract master-specific content from the 109-line file without losing anything. The inline content should match the shared fragment (after G-P0-3 rewrite), but may have master-only additions.

**Estimated complexity:** Small — content extraction + include directive in one file

---

## Checkpoint: P0

**Pass criteria (ALL must be green before P1 starts):**
- [ ] `bmad-agent-shared.md` moved to `prompts/` — `agents/_shared/` removed
- [ ] Runtime include resolution test passes for all 19 non-master agents on VPS
- [ ] All 20 `role.md` files contain `MANDATORY PROCESS COMPLIANCE` section before persona
- [ ] `bmad-agent-shared.md` Initial Clarification is process-aware (no escape hatch)
- [ ] All 20 `solving.md` files use clean BMAD-specific full override (no conflicting directive)
- [ ] bmad-master specifics.md converted from 109-line inline to `{{ include }}`
- [ ] ADR 0002 revised to reflect actual state
- [ ] `python -m pytest tests/ -v` → all 250+ tests green

---

## Phase G — P1: High Priority (3 tasks)

**Prereq:** P0 checkpoint passed.

---

### Task G-P1-1: Add subordinate-mode detection to all 20 communication_additions.md [Size: M]

**SPEC ref:** G-P1-1 (R4)
**Root cause:** RC4 — no subordinate-mode awareness

**Description:** Menu-driven interaction breaks when agents are called via `call_subordinate`. Agents have no alternative execution path for subordinate mode. Add `Subordinate Mode Detection` section to all 20 agents' `communication_additions.md`.

**Changes required:**
1. Add the following section to ALL 20 agents' `communication_additions.md`:

```markdown
## Subordinate Mode Detection

When you receive a direct task instruction (not a menu selection from the user),
you are in SUBORDINATE MODE:

1. Recognize you are being called by a superior agent
2. Load the appropriate BMAD skill IMMEDIATELY
3. Route to the matching workflow based on the task
4. Execute the workflow step-by-step — do NOT skip the process
5. Return results via the `response` tool when complete

Do NOT display the menu in subordinate mode — proceed directly to workflow execution.
```

**Files affected (20 files):**
- `agents/bmad-master/prompts/agent.system.main.communication_additions.md`
- `agents/bmad-analyst/prompts/agent.system.main.communication_additions.md`
- ... (all 20 agents' `communication_additions.md` files)

**Dependencies:** None (independent after P0 checkpoint)

**Verification steps:**
- [ ] `grep -rl 'Subordinate Mode Detection' agents/*/prompts/agent.system.main.communication_additions.md` → 20 files
- [ ] Section contains all 5 numbered items + the menu suppression instruction
- [ ] `python -m pytest tests/ -v` — all 250+ tests green

**Risk notes:** Low risk — additive text insertion only.

**Estimated complexity:** Medium — 20 files, but identical content insertion

---

### Task G-P1-2: Create shared solving.md fragment in `prompts/bmad-agent-shared-solving.md` [Size: S]

**SPEC ref:** G-P1-2 (R5)
**Root cause:** Maintenance optimization

**Description:** After G-P0-4, all 20 agents have identical solving.md content. Extract to a shared fragment to eliminate copy-paste across 20 files. Replace each `solving.md` with a single `{{ include }}` directive.

**Changes required:**
1. Create `prompts/bmad-agent-shared-solving.md` with the clean BMAD-specific content from G-P0-4
2. Replace all 20 `solving.md` files with: `{{ include "bmad-agent-shared-solving.md" }}`

**Files affected:**
- NEW: `prompts/bmad-agent-shared-solving.md` (shared fragment)
- `agents/bmad-master/prompts/agent.system.main.solving.md` → reduce to include
- ... (all 20 agents' `solving.md` files)

**Dependencies:** G-P0-4 (shared fragment created from the clean override content)

**Verification steps:**
- [ ] `prompts/bmad-agent-shared-solving.md` exists with BMAD solving content
- [ ] `grep -rl '{{ include "bmad-agent-shared-solving.md" }}' agents/*/prompts/agent.system.main.solving.md` → 20 files
- [ ] Include resolves on VPS for all 20 agents
- [ ] `python -m pytest tests/ -v` — all 250+ tests green

**Risk notes:** Low risk — content extraction + include directive. Same content as G-P0-4, just centralized.

**Estimated complexity:** Small — one new file + 20 files reduced to single-line include

---

### Task G-P1-3: Verify bmad-master response.md include resolves on VPS [Size: XS]

**SPEC ref:** G-P1-3 (R8)
**Root cause:** Quality assurance

**Description:** bmad-master has `{{ include "agent.system.response_tool_tips.md" }}` in its `response.md`. This references the A0 framework file at `/a0/prompts/agent.system.response_tool_tips.md`. It should work (framework files are in the search path), but this has never been empirically verified.

**Changes required:** None expected — verification only.

**Action:**
1. Run verification script on VPS testing instance to confirm the include resolves correctly in bmad-master's context
2. If include does NOT resolve, investigate and fix

**Files affected:**
- Potentially `agents/bmad-master/prompts/agent.system.main.response.md` if fix needed

**Dependencies:** None (independent after P0 checkpoint)

**Verification steps:**
- [ ] Include resolves on VPS — bmad-master response contains expected tooltips content
- [ ] If fix needed: commit and re-verify

**Risk notes:** Low risk — verification-only task. Framework files should be in the search path.

**Estimated complexity:** Extra-small — verification script run on VPS

---

## Checkpoint: P1

**Pass criteria:**
- [ ] All 20 `communication_additions.md` files contain `Subordinate Mode Detection` section
- [ ] Shared solving.md fragment exists in `prompts/bmad-agent-shared-solving.md`
- [ ] All 20 `solving.md` files reduced to `{{ include "bmad-agent-shared-solving.md" }}`
- [ ] bmad-master response.md include verified resolving on VPS
- [ ] `python -m pytest tests/ -v` → all 250+ tests green

---

## Phase G — P2: Nice to Have (2 tasks)

**Prereq:** P1 checkpoint passed.

---

### Task G-P2-1: Add A0 framework skill awareness to BMB specifics.md [Size: XS]

**SPEC ref:** G-P2-1 (R6)
**Root cause:** Quality improvement

**Description:** Add `A0 Framework Integration` section to BMB agent specifics.md files (Wendy/bmad-workflow-builder, Bond/bmad-agent-builder, Morgan/bmad-module-builder) so they understand A0 tool patterns when building BMAD artifacts.

**Changes required:**
1. Add the following section to 3 BMB agent specifics.md files:

```markdown
## A0 Framework Integration

When building workflows that interact with Agent Zero:
- Load `a0-development` skill to understand framework architecture
- Reference A0 tool patterns and conventions
- Use `call_subordinate` to delegate specialist work
- Follow A0 prompt inheritance and override patterns
```

**Files affected (3 files):**
- `agents/bmad-workflow-builder/prompts/agent.system.main.specifics.md`
- `agents/bmad-agent-builder/prompts/agent.system.main.specifics.md`
- `agents/bmad-module-builder/prompts/agent.system.main.specifics.md`

**Dependencies:** None

**Verification steps:**
- [ ] `grep -rl 'A0 Framework Integration' agents/bmad-workflow-builder/prompts/ agents/bmad-agent-builder/prompts/ agents/bmad-module-builder/prompts/` → 3 files
- [ ] `python -m pytest tests/ -v` — all 250+ tests green

**Risk notes:** None — additive text only.

**Estimated complexity:** Extra-small — identical section added to 3 files

---

### Task G-P2-2: Update failure analysis report to reflect clean full override decision [Size: XS]

**SPEC ref:** G-P2-2 (R9)
**Root cause:** Documentation accuracy

**Description:** `docs/workflow-builder-failure-analysis.md` still references the old `{{ extend }}` approach in its recommendations. The decision was made to use a clean full override instead (R3). Update the report to reflect the actual implementation.

**Changes required:**
1. Update failure analysis report recommendations to reflect clean full override decision
2. Remove or update references to `{{ extend }}` approach
3. Add note about why clean override was chosen over extend

**Files affected:**
- `docs/workflow-builder-failure-analysis.md`

**Dependencies:** None

**Verification steps:**
- [ ] Report references clean full override, not `{{ extend }}`
- [ ] Rationale for decision documented

**Risk notes:** None — documentation only.

**Estimated complexity:** Extra-small — single file text update

---

## Checkpoint: P2 (ready for /ship)

**Pass criteria — all required for `/ship`:**
- [ ] BMB agent specifics.md contain `A0 Framework Integration` section
- [ ] Failure analysis report updated to reflect clean full override
- [ ] CHANGELOG updated with Phase G entries
- [ ] Plugin version `1.3.0`
- [ ] All 20 BMAD agents functional end-to-end on VPS testing instance
- [ ] Include resolution empirically verified on VPS for all 19 non-master agents
- [ ] Failure probability reduced from 95-100% → <5%
- [ ] Tagged as `v1.3.0`; merged to `main`

---

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| G-P0-1 file move breaks include resolution for agents that already had it working | Medium — bmad-master uses specifics.md not include | Low | bmad-master does NOT use `{{ include }}` for shared fragment; it inlines. Move only affects 19 agents that were already broken |
| 20-file changes introduce typos or inconsistencies | Medium — agents get different prompts | Low | Use scripted/text-editor batch approach; verify with `grep` counts |
| G-P0-5 content extraction loses master-specific content | High — bmad-master loses unique behavior | Medium | Read 109-line file fully before extraction; verify master-specific extras survive |
| ADR 0002 revision exposes past incorrect claims | Low — documentation accuracy | High | Transparent revision is better than leaving false claims; add revision date and corrected status |
| Test suite doesn't cover prompt content | Medium — prompt defects not caught | High | Phase G adds `test_phase_g_include.py` and `test_phase_g_compliance.py` for runtime and content verification |
| Clean full override loses future A0 framework solving.md improvements | Medium — BMAD agents don't benefit from framework updates | Low | BMAD needs fundamentally different behavior; shared fragment in `prompts/` can be updated independently |

---

## Task Summary

| ID | Task | Priority | Size | Dependencies | Status |
|----|------|----------|------|-------------|--------|
| G-P0-1 | Fix broken `{{ include }}` — move shared fragment | P0 | S | None (MUST BE FIRST) | Ready |
| G-P0-2 | Add process compliance gate to all 20 role.md | P0 | M | None (after G-P0-1) | Ready |
| G-P0-3 | Rewrite shared fragment Initial Clarification | P0 | S | None (after G-P0-1) | Ready |
| G-P0-4 | Rewrite solving.md — clean full override | P0 | M | None (after G-P0-1) | Ready |
| G-P0-5 | Convert bmad-master inline to `{{ include }}` | P0 | S | G-P0-1 | Ready |
| G-P1-1 | Add subordinate-mode detection to 20 agents | P1 | M | P0 checkpoint | Ready |
| G-P1-2 | Create shared solving.md fragment | P1 | S | G-P0-4 | Ready |
| G-P1-3 | Verify bmad-master response include on VPS | P1 | XS | P0 checkpoint | Ready |
| G-P2-1 | Add A0 framework skill awareness to BMB | P2 | XS | P1 checkpoint | Ready |
| G-P2-2 | Update failure analysis report | P2 | XS | P1 checkpoint | Ready |

**Totals:** 10 tasks (P0: 5 · P1: 3 · P2: 2)
**Estimated effort:** 3–4 hours for P0, 5–6 hours total
