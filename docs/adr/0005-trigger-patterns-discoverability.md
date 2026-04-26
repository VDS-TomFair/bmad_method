# ADR-0005: trigger_patterns for Agent Zero Skill Discoverability

**Status:** Accepted
**Date:** 2026-04-26
**Phase:** C (Routing Consolidation)

## Context

BMAD skills were not discoverable via Agent Zero's `skills_tool:search` because SKILL.md files lacked `trigger_patterns` frontmatter. Users had to know exact skill names or menu codes to invoke BMAD workflows.

## Decision

Add `trigger_patterns` frontmatter to all 57 SKILL.md files with both slash-style (`/bmad-init`) and natural language (`initialize a bmad project`) triggers.

## Rationale

- `skills_tool:search` matches against SKILL.md `trigger_patterns` and description
- Slash commands (`/bmad`, `/bmad-init`, `/bmad-status`) align with A0 slash-command convention
- Natural language triggers enable intent-based discovery ("create a story" → bmad-bmm story workflow)
- No conflict with CSV routing — CSV handles BMAD-internal menu codes, trigger_patterns handle A0 discovery

## Consequences

- **Positive:** All 57 BMAD skills discoverable via `skills_tool:search`
- **Positive:** Users can type `/bmad` to find the main entry point
- **Negative:** Two metadata systems per skill (CSV + trigger_patterns) — but they serve different purposes
- **Mitigation:** CSV is authoritative for BMAD routing; trigger_patterns is supplementary for A0 discovery only

## Alternatives Considered

1. **No trigger_patterns** — skills invisible to A0 search, poor UX
2. **Trigger patterns in CSV** — would bloat CSV with A0-specific data, break upstream compatibility
3. **Single generic trigger per module** — too broad, doesn't help users find specific workflows
