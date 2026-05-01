# ADR-0002: Shared Agent Prompts via `{{ include }}` Directive

**Status:** Revised (Phase G)
**Date:** 2026-04-26 (revised 2026-05-01)
**Phase:** D → G revision

## Context

19 of 20 BMAD agents had ~90 lines of identical content in `main.specifics.md` (methodology overview, workflow patterns, tool usage). This created a maintenance burden — any methodology change required editing 19 files identically.

## Decision

Extract shared content to a shared fragment and reference it via `{{ include }}` directive in each agent's `main.specifics.md`.

## Original Implementation (Phase D)

Shared fragment placed at `agents/_shared/prompts/bmad-agent-shared.md`.

**Claimed:** "Confirmed working via live A2A testing on the testing instance."

**Reality:** This was never verified. The include silently failed for all 19 non-master agents because `agents/_shared/prompts/` is NOT in A0's search path (`_shared` is not a profile name). A0's `helpers/files.py:process_includes()` silently returns the literal include text on `FileNotFoundError`. All 19 agents were missing 85 lines of critical behavioral instructions.

## Revision (Phase G — G-P0-1)

Moved shared fragment from `agents/_shared/prompts/bmad-agent-shared.md` → `prompts/bmad-agent-shared.md`.

The plugin root `prompts/` directory IS in A0's search chain (priority level 7). All `{{ include }}` directives now resolve correctly.

**Verified:** 259 tests pass, including new `test_phase_g_include.py` that validates include resolution for all 19 non-master agents.

## Rationale

- Agent Zero's `helpers/files.py:process_includes()` natively supports `{{ include }}` for prompt files
- Reduces ~1,662 lines of duplication to a single 85-line shared file
- Future methodology changes touch one file instead of 19
- Plugin root `prompts/` directory is in A0's search chain — include resolves correctly

## Consequences

- **Positive:** Single source of truth for shared methodology content
- **Positive:** ~1,580 lines removed, easier maintenance
- **Positive:** Include now actually resolves — all 19 agents receive shared instructions
- **Negative:** Agents depend on shared fragment — if deleted, all 19 agents break
- **Mitigation:** Fragment is in `prompts/` directory (standard A0 convention) with test coverage

## Alternatives Considered

1. **Keep duplicated content** — maintenance nightmare, drift risk
2. **Symlinks** — A0 doesn't resolve symlinks in prompt paths
3. **Python extension to inject content** — over-engineered for static text
4. **Keep in `agents/_shared/prompts/`** — NOT in A0 search path, include silently fails

## Lessons Learned

- Never assume `{{ include }}` works without empirical verification
- A0 silently fails on include resolution — no error, no warning
- `_shared` is not a valid A0 profile name — files there are invisible to include resolution
- Test coverage must include runtime include resolution, not just file existence
