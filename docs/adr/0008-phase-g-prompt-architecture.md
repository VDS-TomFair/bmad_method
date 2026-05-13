# ADR-0008: Phase G Prompt Architecture — Multi-Layer Process Compliance

**Status:** Accepted
**Date:** 2026-05-01
**Phase:** G (Agent Prompt Fixes v1.3.0)

## Context

During bmad-workflow-builder (Wendy) end-to-end testing, Wendy skipped the entire 11-step BMAD workflow and produced a monolithic SKILL.md. Root cause analysis (documented in `docs/workflow-builder-failure-analysis.md`) revealed **six systemic root causes** affecting ALL 20 BMAD agents, with compound failure probability of 95-100%:

| RC | Root Cause | Impact |
|----|-----------|--------|
| RC0 | Broken `{{ include }}` — shared fragment in `agents/_shared/prompts/` (not in A0 search path) | 19/20 agents missing 85 lines of behavioral instructions |
| RC1 | Conflicting directives — solving.md "high-agency" overrides vs BMAD "follow steps precisely" | Agents default to autonomous shortcuts |
| RC2 | Escape hatch — Initial Clarification section allowed agents to skip process entirely | 30% failure rate on its own |
| RC3 | Step rules absent from prompts — compliance only in workflow steps, not in agent prompts | Agents never see process rules |
| RC4 | No subordinate mode detection — agents don't recognize they're called by a superior | Wrong communication patterns |
| RC5 | No process compliance gate — nothing enforces process before persona | Persona overrides process |

## Decisions

### D1: Fix Include Path (G-P0-1)

Move shared fragment from `agents/_shared/prompts/bmad-agent-shared.md` → `prompts/bmad-agent-shared.md`.

**Rationale:** Plugin root `prompts/` directory IS in A0's search chain (priority level 7). `_shared` is not a valid A0 profile name — `helpers/files.py:process_includes()` silently returns literal `{{ include }}` text on `FileNotFoundError`.

### D2: MANDATORY PROCESS COMPLIANCE Gate (G-P0-2)

Add a 6-point compliance directive section to ALL 20 agent `role.md` files, positioned BEFORE the persona definition:

```markdown
## MANDATORY PROCESS COMPLIANCE

1. Load skill via skills_tool:load with the appropriate skill name
2. Follow workflow steps precisely — never execute from memory
3. Produce artifact at the skill-defined output path
4. If a step is unclear, ask for clarification — do NOT skip
5. Process compliance is non-negotiable — persona serves the process
6. When called by a superior agent: load skill, execute, report results
```

**Rationale:** Process rules must appear before persona text so they establish behavioral context first. This addresses RC3 and RC5 simultaneously.

### D3: Rewrite Initial Clarification — Remove Escape Hatch (G-P0-3)

Replace the original "Initial Clarification" section in `bmad-agent-shared.md` which contained:

> "If you determine that no clarification is needed, you may proceed directly to execution."

With a process-aware version that determines WHERE to start in the process, not WHETHER to start:

> "Determine the current phase and starting point. Clarification identifies WHERE to resume, not WHETHER to proceed."

**Rationale:** The escape hatch allowed agents to skip the entire workflow process. Removing it eliminates RC2.

### D4: Clean Solving.md Override (G-P0-4)

Replace ALL 20 `solving.md` files with a clean BMAD-specific full override that eliminates conflicting "high-agency" directives.

**Key design choice:** Use `{{ include "bmad-agent-shared-solving.md" }}` for single source of truth rather than `{{ extend }}` or per-file overrides.

**Rationale:** A0's prompt resolution uses first-match. A file named `solving.md` in the agent's `prompts/` directory completely overrides A0's default solving behavior. This eliminates RC1 by removing the conflict entirely rather than trying to reconcile two opposing philosophies.

### D5: Subordinate Mode Detection (G-P1-1)

Add `Subordinate Mode Detection` section to all 20 `communication_additions.md` files:

```markdown
## Subordinate Mode Detection

If you detect that you were called by a superior agent (via call_subordinate):
1. Load the relevant skill via skills_tool:load
2. Execute the assigned task directly — do NOT show menu or ask questions
3. Report results concisely to the superior agent
4. Suppress interactive prompts and menu displays
```

**Rationale:** Agents need to recognize when they're operating as subordinates and adapt communication accordingly. Addresses RC4.

### D6: bmad-master Include Conversion (G-P0-5)

Convert bmad-master's 109-line inline `specifics.md` to `{{ include "bmad-master-specifics.md" }}`.

**Rationale:** After rewriting the shared fragment, keeping inline content in bmad-master would cause divergence. Using `{{ include }}` ensures consistency.

## Consequences

### Positive
- Failure probability reduced from 95-100% → <5%
- Single source of truth for shared behavioral content (1 file instead of 19)
- Single source of truth for solving behavior (1 shared fragment instead of 20)
- Process compliance enforced at 4 layers: role.md gate, shared fragment, solving.md, communication_additions.md
- Future methodology changes touch 1-2 files instead of 20+

### Negative
- Shared fragment dependency — if deleted, all 19 non-master agents break
- Compliance gate adds ~16 lines to each role.md (acceptable trade-off)
- Full override of solving.md means A0 framework improvements won't auto-propagate to BMAD agents

### Mitigations
- Fragment is in standard `prompts/` directory with 292 tests covering include resolution
- Solving override is intentional — BMAD process-driven behavior differs fundamentally from A0's autonomous defaults
- bmad-master include uses same mechanism, tested identically

## Alternatives Considered

1. **`{{ extend }}` for solving.md** — A0 doesn't support this directive; not an option
2. **Prompt engineering only (no structural changes)** — Insufficient; the include was broken, structural fix required
3. **Per-agent solving.md customization** — Defeats purpose; creates 20 maintenance points
4. **Remove process compliance, let agents be autonomous** — Would abandon the entire BMAD methodology
5. **Fix include only, skip other RCs** — Would leave 40% failure probability from RC1-RC5

## Files Changed

- 20 `role.md` — compliance gate added
- 20 `solving.md` — clean override with `{{ include }}`
- 20 `communication_additions.md` — subordinate mode detection
- 1 `prompts/bmad-agent-shared.md` — moved, rewritten clarification
- 1 `prompts/bmad-agent-shared-solving.md` — new shared solving fragment
- 1 `bmad-master specifics.md` — converted to include
- 3 BMB `specifics.md` — A0 framework integration
- 1 ADR 0002 — revised to reflect broken include history
- 3 new test files — 292 total tests (up from 263)

## Lessons Learned

1. **Never assume `{{ include }}` works without empirical verification** — A0 silently fails
2. **Conflicting directives resolve to the stronger bias** — "high-agency" always wins over "follow steps"
3. **Process compliance must be structural, not advisory** — Agents optimize for what they're measured against
4. **Multi-layer defense works** — No single fix would have achieved <5%; the compound effect of 6 fixes was required
5. **Escape hatches are footguns** — Any permission to skip process WILL be used
