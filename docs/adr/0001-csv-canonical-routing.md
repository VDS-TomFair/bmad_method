# ADR-0001: CSV as Canonical Routing Mechanism

**Status:** Accepted
**Date:** 2026-04-26
**Phase:** C (Routing Consolidation)

## Context

The BMAD Method plugin uses `module-help.csv` files to route user inputs (menu codes, keywords) to the correct workflow. During alignment analysis, we evaluated replacing CSV with SKILL.md frontmatter routing (Agent Zero native pattern).

## Decision

**Keep CSV as the canonical routing mechanism**, aligned with upstream BMAD-METHOD 13-column schema.

## Rationale

- Upstream BMAD-METHOD also uses `module-help.csv` as its routing mechanism — not SKILL.md frontmatter
- CSV is designed for IDE integrations (Cursor, Claude Code, Windsurf) that parse it directly
- Replacing CSV would break upstream compatibility and create a maintenance fork
- Agent Zero discoverability is addressed separately via `trigger_patterns` in SKILL.md

## Consequences

- **Positive:** Full upstream compatibility; IDE integrations work unchanged
- **Positive:** Separation of concerns — CSV for BMAD routing, SKILL.md for A0 discovery
- **Negative:** Two metadata sources per skill (CSV + SKILL.md) — mitigated by single source of truth for routing (CSV)

## Alternatives Considered

1. **SKILL.md frontmatter routing** — would break upstream compatibility
2. **YAML routing config** — unnecessary abstraction layer over CSV
3. **Dual-read compatibility** — removed in C1; adds complexity without benefit
