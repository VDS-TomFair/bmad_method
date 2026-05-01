# BMAD Workflow Builder Agent Failure Analysis — Complete Report

**Date:** 2026-05-01 (Final)
**Analyst:** Agent Zero (with subordinate research + empirical verification)
**Subject:** bmad-workflow-builder (Wendy) — Process Bypass on Caveman Skill Task
**Severity:** CRITICAL — Systemic prompt design issue + broken include mechanism across all 20 BMAD agents
**Grounding:** A0 framework source code, DeepWiki, a0-create-agent skill, prompt cartography, harness architecture, empirical VPS testing

---

## 1. Executive Summary

The bmad-workflow-builder agent (Wendy) was tasked with creating a Caveman skill. Instead of following the BMAD 11-step workflow process (Discovery → Classification → Requirements → Tools → Plan Review → Design → Foundation → Build Steps → Confirmation → Completion), Wendy rationalized skipping all steps and wrote a monolithic 401-line SKILL.md in a single shot.

This analysis discovered **TWO critical failure layers**:

1. **BROKEN INCLUDE MECHANISM (RC0):** The `{{ include "bmad-agent-shared.md" }}` directive in all 19 non-master agents' `specifics.md` **silently fails** — A0's `process_includes()` cannot find the file because `agents/_shared/prompts/` is not in the search path. All 19 agents are missing 85 lines of critical behavioral instructions.

2. **CONFLICTING DIRECTIVES (RC1-RC5):** Even if the include worked, the agent prompts contain contradictory imperatives that bias toward task-completion shortcuts.

**Scope:** This is NOT a Wendy-specific issue. All 20 BMAD agents share the same structural vulnerabilities. 19 of 20 are additionally affected by the broken include.

---

## 2. Critical Discovery: `{{ include }}` Silently Fails

### 2.1 The Problem

All 19 non-master BMAD agents have this in their `specifics.md`:

```markdown
## Your Role in the Conversation

{{ include "bmad-agent-shared.md" }}
```

The shared fragment lives at:
```
/a0/usr/plugins/bmad_method/agents/_shared/prompts/bmad-agent-shared.md
```

### 2.2 Why It Fails

A0's `get_paths()` in `helpers/subagents.py:339` builds search directories for profile `bmad-workflow-builder`:

| Priority | Directory | Type |
|---|---|---|
| 1 | `project/agents/bmad-workflow-builder/prompts/` | Project-scoped |
| 2 | `project/.a0proj/...` | Project meta |
| 3 | `usr/agents/bmad-workflow-builder/prompts/` | User agent |
| 4 | `plugin/agents/bmad-workflow-builder/prompts/` | Plugin agent |
| 5 | `agents/bmad-workflow-builder/prompts/` | Framework agent |
| 6 | `usr/prompts/` | User root |
| 7 | `plugin/prompts/` | Plugin root |
| 8 | `prompts/` | Framework root |

**`agents/_shared/prompts/` is NOT in this chain** — `_shared` is not a profile name.

### 2.3 What Happens When It Fails

From `helpers/files.py:358-365`:

```python
def replace_include(match):
    include_path = match.group(1)
    if os.path.isabs(include_path):
        return match.group(0)
    try:
        return read_prompt_file(include_path, _directories, **kwargs)
    except FileNotFoundError:
        return match.group(0)  # SILENTLY returns literal text
```

The literal text `{{ include "bmad-agent-shared.md" }}` stays in the system prompt as inert text — the agent sees it as noise, not instructions.

### 2.4 Empirical Proof from VPS

```
=== Searching for bmad-agent-shared.md ===
NOT FOUND - include would silently fail!

=== Actual shared file location ===
  /a0/usr/plugins/bmad_method/agents/_shared/prompts/bmad-agent-shared.md (exists=True)
```

Test script run with A0's framework Python (`/opt/venv-a0/bin/python3`) on VPS testing container.

### 2.5 Impact: ALL 19 Non-Master Agents Missing 85 Lines

The shared fragment (`bmad-agent-shared.md`) contains:

| Section | Lines | Purpose |
|---|---|---|
| A0 Variable Resolution | ~8 | How to use `{{ vars }}` in prompts |
| BMAD Activation Protocol | ~12 | When and how to activate BMAD mode |
| **Initial Clarification** | ~8 | **The escape hatch blamed for the failure** |
| Thinking Framework | ~15 | Structured thinking before acting |
| Tool Calling | ~20 | Proper tool usage patterns |
| File and Artifact Handling | ~22 | Output conventions, state management |

**These instructions were NEVER present in any of the 19 agents' system prompts.**

### 2.6 ADR 0002 Is Wrong

ADR 0002 states: "Confirmed working via live A2A testing on the testing instance."

This claim is **false**. The include silently fails. The ADR must be revised.

### 2.7 Why bmad-master Is Unaffected

bmad-master has a 109-line `specifics.md` that **inlines the shared content directly** — it does NOT use `{{ include }}`. This is why bmad-master works correctly while all specialist agents are broken.

---

## 3. A0 Agent Architecture

### 3.1 How Agent Profiles Work

Agent Zero uses a **filename-driven, zero-configuration override model**:

- All agents share the same top-level shell (`agent.system.main.md`)
- Profiles override by placing files with identical basenames in their directory
- The framework resolves prompts using **first-hit-wins** precedence:
  1. `<project>/agents/<profile>/prompts/`
  2. `usr/agents/<profile>/prompts/`
  3. `<plugin>/agents/<profile>/prompts/`
  4. `agents/<profile>/prompts/` (default profile)
  5. `<project>/prompts/`
  6. `usr/prompts/`
  7. `<plugin>/prompts/`
  8. `prompts/` (framework default)

### 3.2 agent.yaml Schema

The `agent.yaml` file contains ONLY three fields:

```yaml
title: BMAD Wendy (Workflow Building Master)
description: |
  Wendy — Workflow Building Master. Master workflow architect...
context: |
  BMAD BMB module specialist for workflow engineering...
```

No model configuration, tool restrictions, or behavioral constraint fields. All behavioral control comes from prompt files.

### 3.3 The Canonical Extension Point

`agent.system.main.specifics.md` is the designated extension slot — ships **empty** in both `/a0/prompts/` and `/a0/agents/default/prompts/`. Every shipped A0 profile overrides this file.

---

## 4. Wendy's Configuration — Full Breakdown

### 4.1 Prompt Assembly Layers

| Layer | File | Status | Lines |
|---|---|---|---|
| 1 | Framework shell: `agent.system.main.md` | Inherited | ~50 |
| 2 | Wendy's role: `role.md` | Override | 87 |
| 3 | Wendy's specifics: `specifics.md` | Override | 23 |
| 3a | **Shared fragment: `bmad-agent-shared.md`** | **BROKEN — never loaded** | **0 (should be 85)** |
| 4 | Wendy's solving: `solving.md` | Override | 36 |
| 5 | Framework communication: `communication.md` | Inherited | ~30 |
| 6 | Wendy's communication_additions: `communication_additions.md` | Override | 32 |
| 7 | Wendy's tips: `tips.md` | Override | 47 |
| 8 | Framework defaults | Inherited | ~200 |
| 9 | Dynamic extras | Runtime | Variable |

**Total effective behavioral content: ~232 lines (should be ~317 with shared fragment)**

### 4.2 agent.yaml (6 lines) ✅
Correct structure. `context` field used for delegation routing.

### 4.3 role.md (87 lines) ⚠️
Contains 8 principles and 8 operational directives. **Gaps:**
- No process compliance gate
- No "NEVER skip steps" enforcement
- No subordinate-mode awareness

### 4.4 specifics.md (23 lines) 🔴
Contains `{{ include "bmad-agent-shared.md" }}` which **silently fails**.
Only 15 lines of skill usage protocol are actually loaded.

### 4.5 solving.md (36 lines) 🔴
**Lines 1-27:** Exact copy of A0 default including `don't accept failure retry be high-agency`
**Lines 30-36:** BMAD addition including `Follow workflow steps precisely — never execute from memory`

**CRITICAL CONFLICT:** Line 25 (complete task, high-agency) vs Line 33 (follow steps precisely). LLM task-completion bias resolves toward shortcut.

**Architecture issue:** Full override (not `{{ include original }}` extension) — won't inherit framework updates.

### 4.6 communication_additions.md (32 lines) ⚠️
Menu-driven interaction model. **Breaks in subordinate mode** — when called via `call_subordinate`, the menu is bypassed entirely.

### 4.7 tips.md (47 lines) ✅
Domain-specific workflow tips. About OUTPUT quality, not PROCESS compliance.

---

## 5. Codebase Verification — All 20 Agents

### 5.1 Methodology

All 20 agent directories verified. 6 agents read in full:
- **BMB:** bmad-workflow-builder (Wendy), bmad-agent-builder (Bond), bmad-module-builder (Morgan)
- **BMM:** bmad-architect (Winston), bmad-dev (Amelia), bmad-pm (John)

### 5.2 Complete Agent Inventory

| Agent | role.md | specifics.md | solving.md | tips.md | comm_add | Other | Total |
|---|---|---|---|---|---|---|---|
| bmad-agent-builder (Bond) | 86 | 23 | 36 | 48 | 30 | — | 223 |
| bmad-analyst | 62 | 23 | 36 | 49 | 33 | — | 203 |
| bmad-architect (Winston) | 62 | 23 | 36 | 49 | 29 | — | 199 |
| bmad-brainstorming-coach | 75 | 23 | 36 | 51 | 28 | — | 213 |
| bmad-design-thinking | 71 | 23 | 36 | 49 | 28 | — | 207 |
| bmad-dev (Amelia) | 84 | 23 | 36 | 49 | 29 | — | 221 |
| bmad-innovation | 70 | 23 | 36 | 47 | 28 | — | 204 |
| **bmad-master** | **116** | **109** | **36** | **77** | **346** | response(29), fw.initial(11) | **724** |
| bmad-module-builder (Morgan) | 87 | 23 | 36 | 47 | 31 | — | 224 |
| bmad-pm (John) | 62 | 23 | 36 | 47 | 33 | — | 201 |
| bmad-presentation | 74 | 23 | 36 | 49 | 34 | — | 216 |
| bmad-problem-solver | 72 | 23 | 36 | 48 | 28 | — | 207 |
| bmad-qa | 63 | 23 | 36 | 48 | 28 | — | 198 |
| bmad-quick-dev | 63 | 23 | 36 | 47 | 30 | — | 199 |
| bmad-sm | 62 | 23 | 36 | 48 | 31 | — | 200 |
| bmad-storyteller | 71 | 23 | 36 | 48 | 28 | — | 206 |
| bmad-tech-writer | 66 | 23 | 36 | 48 | 33 | — | 206 |
| bmad-test-architect | 109 | 23 | 36 | 51 | 36 | — | 255 |
| bmad-ux-designer | 63 | 23 | 36 | 49 | 28 | — | 199 |
| bmad-workflow-builder (Wendy) | 87 | 23 | 36 | 47 | 32 | — | 225 |

### 5.3 Key Findings

- All 20 `solving.md` files are **byte-identical** (md5: `da712af70ffb483e970bd847e3602449`)
- All 19 non-master `specifics.md` files are 23 lines with broken `{{ include }}`
- bmad-master inlines shared content (109 lines) — does NOT use `{{ include }}`
- Only role.md, tips.md, and communication_additions.md differ between agents

---

## 6. Root Causes (6 Total)

### RC0: Broken `{{ include }}` Resolution (Severity: CRITICAL — PRIMARY ROOT CAUSE)

| Aspect | Detail |
|---|---|
| **What** | `{{ include "bmad-agent-shared.md" }}` silently fails for all 19 non-master agents |
| **Why** | File is in `agents/_shared/prompts/` which is not in A0's search path — `_shared` is not a profile name |
| **Effect** | All 19 agents missing 85 lines of behavioral instructions: variable resolution, activation protocol, clarification, thinking framework, tool calling, file handling |
| **Evidence** | Empirically verified on VPS with A0 framework Python — `find_file_in_dirs` returns NOT FOUND |
| **Impact** | Agents operate without the shared behavioral foundation that was designed to prevent exactly this failure |

### RC1: Conflicting Directives in solving.md (Severity: CRITICAL)

| Directive | Location | Effect |
|---|---|---|
| `don't accept failure retry be high-agency` | Line 25 (A0 default copy) | Incentivize task completion by any means |
| `Follow workflow steps precisely — never execute from memory` | Line 33 (BMAD addition) | Require sequential step execution |

The BMAD solving.md replicates A0's default verbatim, then appends conflicting BMAD section. LLM resolves toward task completion (skipping process).

### RC2: Initial Clarification Escape Hatch (Severity: HIGH — but moot if include is broken)

From `bmad-agent-shared.md` lines 29-37:

```markdown
## Initial Clarification
Before executing any significant BMAD workflow, conduct a structured clarification pass...
Only when you can execute the full workflow without further interruption should you begin autonomous work.
```

**NOTE:** This section was NEVER loaded due to RC0. If the include is fixed, this escape hatch would become a secondary failure vector. Must be fixed regardless.

### RC3: Step-File Rules Not in Agent Prompts (Severity: HIGH)

Enforcement rules exist only inside skill files (loaded on demand into `extras_persistent`). If agent rationalizes not loading the skill, rules never enter context. Circular dependency: rules guard against skipping → only exist inside skills → require loading → which is what agent skips.

### RC4: No Subordinate-Mode Awareness (Severity: HIGH)

A0 passes no framework context about HOW a subordinate should work. Menu-driven interaction breaks when called via `call_subordinate` — the menu is bypassed entirely, but agents have no alternative execution path.

### RC5: No Process Compliance Gate (Severity: HIGH)

None of the 20 agents contain a non-overridable process compliance directive. role.md focuses on OUTPUT quality, not PROCESS adherence.

---

## 7. Recommendations — Priority Ordered

### R0: Fix the Broken Include (Priority: P0 — MUST DO FIRST)

Move `bmad-agent-shared.md` to a directory that IS in the search path:

```
# Current (broken):
agents/_shared/prompts/bmad-agent-shared.md

# Fixed:
prompts/bmad-agent-shared.md
```

The plugin root `prompts/` directory IS in the search chain (priority level 7). All `{{ include }}` directives will resolve correctly.

**Steps:**
1. Create `/a0/usr/plugins/bmad_method/prompts/` directory
2. Move `bmad-agent-shared.md` there
3. Update ADR 0002
4. Verify on VPS with test script
5. Run existing test suite (248 tests)

**A0 compatibility:** Uses existing framework mechanisms. No code changes required.

### R1: Add Process Compliance Gate to role.md (Priority: P0)

Add to EVERY BMAD agent's role.md, BEFORE the persona definition:

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

**Apply to:** All 20 BMAD agents.

### R2: Rewrite bmad-agent-shared.md Initial Clarification (Priority: P0)

Replace the escape hatch with process-aware clarification:

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

**Apply to:** The shared fragment (one change fixes all 19 agents).

### R3: Rewrite solving.md to Remove Conflict (Priority: P0)

Replace the full override with `{{ include original }}` extension:

```markdown
{{ include original }}

## BMAD Process Override

CRITICAL: The above "complete task" directive is OVERRIDDEN for BMAD agents:
- "Complete task" means complete the PROCESS, not skip to the output
- Process compliance is non-negotiable — always overrides efficiency
- You MUST load the BMAD skill before taking ANY action
- You MUST follow workflow steps precisely — never execute from memory
- Produce artifact at skill-defined output path
- Update `02-bmad-state.md` after phase transitions
- Use `text_editor:patch` for large artifacts — never rewrite entire files

If you feel tension between completing the task and following the process,
FOLLOW THE PROCESS.
```

**A0 compatibility:** Uses `{{ include original }}` to inherit framework default, then overrides conflict.
**Apply to:** All 20 BMAD agents (create shared fragment to avoid 20-file copy).

### R4: Add Subordinate-Mode Detection (Priority: P1)

Add to communication_additions.md:

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

**Apply to:** All 20 BMAD agents.

### R5: Create Shared solving.md Fragment (Priority: P1)

Since all 20 agents share identical solving.md content:

```markdown
{{ include "bmad-agent-shared-solving.md" }}
```

Place `bmad-agent-shared-solving.md` in the same `prompts/` directory as the shared fragment (from R0). This eliminates copy-paste across 20 files.

### R6: Add A0 Framework Skill Awareness (Priority: P2)

Add to specifics.md:

```markdown
## A0 Framework Integration

When building workflows that interact with Agent Zero:
- Load `a0-development` skill to understand framework architecture
- Reference A0 tool patterns and conventions
- Use `call_subordinate` to delegate specialist work
- Follow A0 prompt inheritance and override patterns
```

**Apply to:** BMB agents primarily (Wendy, Bond, Morgan).

---

## 8. Decision Flow — Updated with Broken Include

```
                    Task Received
                         |
                         v
              [specifics.md loaded]
              {{ include "bmad-agent-shared.md" }}
                         |
             +-----------+-----------+
             |                       |
        RC0: Include FAILS      Include works (after fix)
        (current state)              |
             |                       v
             |              [bmad-agent-shared.md]
             |              Initial Clarification
             |                       |
             |           +-----------+-----------+
             |           |                       |
             |    Requirements              Requirements
             |      appear clear              unclear
             |           |                       |
             v           v                       v
   [solving.md conflict]              "Ask clarifying
   "complete task" WINS               questions"
   over "follow process"                   |
        (RC1)                            v
           |                        [Load skill,
           v                         follow steps]
   Write SKILL.md                      |
   directly (FAIL)                     v
                                 Step-by-step
                                 execution (SUCCESS)

WITHOUT RC0 FIX: Agents never get shared instructions → operate blind
WITH RC0 FIX + R1-R3: Process compliance enforced at multiple layers
```

---

## 9. Failure Probability Assessment

| Scenario | Probability | Rationale |
|---|---|---|
| **Current (broken include, no fixes)** | **95-100%** | Agents missing core behavioral instructions + conflicting directives = almost guaranteed shortcut |
| **After R0 (include fixed only)** | **60-80%** | Shared instructions present but escape hatch + conflict still exist |
| **After R0 + R1-R3 (process compliance)** | **5-15%** | Multiple enforcement layers, conflict removed |
| **After all fixes (R0-R6)** | **<5%** | Defense in depth across all layers |

---

## 10. bmad-master vs Specialist Agents

bmad-master is the ORCHESTRATOR — routes tasks to 19 specialists, never executes directly.

### Key Differences

| Aspect | bmad-master | Specialists (19) |
|---|---|---|
| specifics.md | 109 lines (inlines shared content) | 23 lines (broken `{{ include }}`) |
| communication_additions | 346 lines (menu, routing, party mode) | ~30 lines (simple menu) |
| Extra files | response.md, fw.initial.md | None |
| Anti-rationalization guard | YES ("NEVER executes specialist workflows directly") | NO |
| Shared fragment | Inlined directly | Broken include |
| Subordinate-mode | N/A (always direct user) | Missing |

### Proven Pattern to Port

bmad-master's anti-rationalization guard can be adapted for specialists:
"NEVER skip the step-by-step workflow process — ALWAYS load the skill first."

---

## 11. Implementation Priority

| Priority | Fix | Root Cause | Effort | Scope |
|---|---|---|---|---|
| **P0** | R0: Fix include (move to `prompts/`) | RC0 | Low | 1 file move |
| **P0** | R1: Process compliance gate in role.md | RC5 | Low | 20 files |
| **P0** | R2: Rewrite shared fragment | RC2 | Low | 1 file |
| **P0** | R3: Rewrite solving.md with `{{ include original }}` | RC1 | Low | 20 files (or 1 shared) |
| **P1** | R4: Subordinate-mode detection | RC4 | Low | 20 files |
| **P1** | R5: Shared solving.md fragment | Maintenance | Medium | 1 new file |
| **P2** | R6: A0 skill awareness | Quality | Low | 3 files (BMB) |

**Total effort:** ~2-3 hours for P0 fixes. All are prompt text changes, no code.

---

## Appendix A: A0 Source Code References

| Component | File | Key Line | Purpose |
|---|---|---|---|
| Include resolution | `helpers/files.py` | `process_includes()` :332 | Resolves `{{ include }}` directives |
| Silent failure | `helpers/files.py` | :364 | Returns literal text on FileNotFoundError |
| File search | `helpers/files.py` | `find_file_in_dirs()` :384 | First-hit-wins directory search |
| Path building | `helpers/subagents.py` | `get_paths()` :339 | Builds 8-level precedence chain |
| Plugin paths | `helpers/plugins.py` | `get_enabled_plugin_paths()` :426 | Returns plugin directories |
| Routing extension | `extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py` | — | Injects routing table into extras |

## Appendix B: A0 Architecture Concepts

| Concept | Description |
|---|---|
| Profile | Named agent persona with prompt overrides, tools, extensions |
| Prompt Override | File in `<profile>/prompts/` with same name as framework default — first-hit-wins |
| `{{ include }}` | Expands file content inline — searches profile's directory chain |
| `{{ include original }}` | Loads same file from next lower-priority directory — enables extension |
| specifics.md | Canonical extension slot — empty in default, filled by profiles |
| solving.md | Controls problem-solving loop — high-value override surface |
| agent.yaml | Profile metadata ONLY (title, description, context) |
| extras_persistent | Dynamic context surviving across turns (loaded skills) |
| call_subordinate | Tool for delegating to specialized agents |

## Appendix C: Test Coverage Gaps

The current test suite (248 tests) covers structural/content validation but NOT runtime behavior:

- ✅ CSV schema validation
- ✅ Trigger pattern coverage
- ✅ Shared fragment structure
- ✅ Include directive format
- ❌ **Runtime include resolution** (would have caught RC0)
- ❌ **Process compliance** (no integration tests)
- ❌ **Subordinate delegation behavior** (no behavioral tests)

**Recommendation:** Add integration test that verifies `{{ include }}` resolves for all 19 agents on the live A0 framework.
