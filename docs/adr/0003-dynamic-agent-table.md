# ADR-0003: Dynamic Agent Table via `{{agent_profiles}}`

**Status:** Accepted
**Date:** 2026-04-26
**Phase:** D (UX Surface)

## Context

The bmad-master agent maintained a static table of all 19 specialist agents in `role.md`. Every time an agent was added, removed, or renamed, this table required manual updating. This was error-prone and already out of date.

## Decision

Replace the static table with Agent Zero's built-in `{{agent_profiles}}` template variable, which dynamically generates the agent list from the plugin's `agents/` directory.

## Rationale

- `{{agent_profiles}}` is populated by `subagents.get_available_agents_dict()` which scans all `agents/*/agent.yaml` files, including from plugins
- Always accurate — no manual maintenance
- Confirmed working via live A2A testing
- Reduces prompt size and eliminates a maintenance chore

## Consequences

- **Positive:** Agent list is always current
- **Positive:** No manual sync needed when agents change
- **Negative:** Agent descriptions come from `agent.yaml` `description` field, which may differ from the previous hand-written summaries
- **Mitigation:** Updated all `agent.yaml` descriptions to be informative

## Alternatives Considered

1. **Keep static table** — high maintenance, drift risk
2. **Python extension to inject table** — over-engineered, `{{agent_profiles}}` already exists
3. **CSV-based agent list** — redundant with `agent.yaml` data
