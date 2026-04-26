# ADR-0002: Shared Agent Prompts via `{{ include }}` Directive

**Status:** Accepted
**Date:** 2026-04-26
**Phase:** D (UX Surface)

## Context

19 of 20 BMAD agents had ~90 lines of identical content in `main.specifics.md` (methodology overview, workflow patterns, tool usage). This created a maintenance burden — any methodology change required editing 19 files identically.

## Decision

Extract shared content to `agents/_shared/prompts/bmad-agent-shared.md` and reference it via `{{ include }}` directive in each agent's `main.specifics.md`.

## Rationale

- Agent Zero's `helpers/files.py:process_includes()` natively supports `{{ include }}` for prompt files
- Reduces ~1,662 lines of duplication to a single 85-line shared file
- Future methodology changes touch one file instead of 19
- Confirmed working via live A2A testing on the testing instance

## Consequences

- **Positive:** Single source of truth for shared methodology content
- **Positive:** ~1,580 lines removed, easier maintenance
- **Negative:** Agents depend on shared fragment — if deleted, all 19 agents break
- **Mitigation:** Fragment is in `_shared/` directory with clear documentation

## Alternatives Considered

1. **Keep duplicated content** — maintenance nightmare, drift risk
2. **Symlinks** — A0 doesn't resolve symlinks in prompt paths
3. **Python extension to inject content** — over-engineered for static text
