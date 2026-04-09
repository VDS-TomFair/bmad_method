# Document Lifecycle Framework

**Version:** 1.0  
**Created:** 2026-04-09 (Story 034)  
**Authors:** Winston (bmad-architect), Paige (bmad-tech-writer)  
**Addresses:** FM-024 — No cross-artifact consistency management

---

## Overview

The Document Lifecycle Framework is a lightweight set of rules, checks, and tooling that helps BMAD projects maintain consistency across their planning and implementation artifacts as the project evolves.

Without this framework, a PRD update can silently invalidate an architecture document. A new architecture component can go weeks without an epic. Stories can accumulate without tracing back to the requirements that motivated them.

This framework solves FM-024 with three mechanisms:
1. **Artifact Relationship Map** — documents which artifacts depend on which
2. **Staleness Detection** — automated mtime-based warnings injected into every bmad-master session
3. **Consistency Check Task** — on-demand semantic validation of cross-artifact coverage

---

## Artifact Hierarchy

BMAD projects produce artifacts in a defined sequence across four phases:

```
Phase 1 — Analysis
  └── Product Brief
        │
Phase 2 — Planning
        └── PRD (Product Requirements Document)
              │
Phase 3 — Solutioning
              └── Architecture Document
                    │
Phase 4 — Implementation
                    ├── Epics List
                    ├── User Stories (story-NNN-*.md)
                    └── Sprint Plans (sprint-plan-*.md)
```

Each artifact depends on the one above it. When a parent artifact changes, its children may need to be reviewed and updated.

For the complete dependency graph with staleness trigger annotations, see: `.a0proj/knowledge/main/artifact-relationships.md`

---

## Staleness Detection

### What It Does

The `_80_bmad_routing_manifest.py` extension runs on every bmad-master message loop. As part of its context injection, it performs a quick mtime comparison of key artifact pairs:

| Parent | Child | Rule |
|--------|-------|------|
| PRD | Architecture Doc | If PRD modified after Architecture → warning |
| Architecture Doc | Sprint Plan | If Architecture modified after Sprint Plan → warning |
| PRD | Sprint Plan | If PRD modified after Sprint Plan (and Architecture doesn't already cover it) → warning |

### What You'll See

When staleness is detected, the following warnings appear in the EXTRAS context visible to bmad-master:

```
## Artifact Staleness Warnings
⚠️ Architecture may be stale — PRD (prd.md) was updated after architecture (architecture-bmad-a0-alignment.md)
⚠️ Sprint plan may be stale — Architecture (architecture-bmad-a0-alignment.md) was updated after sprint plan (sprint-plan-sprint-3.md)
```

### What Triggers It

- Editing and saving the PRD
- Creating a new version of the architecture document
- Any file modification that changes the `mtime` of a tracked artifact

### What It Does NOT Do

- It does **not** block routing or workflow execution
- It does **not** prevent development from continuing
- It does **not** read file content — only filesystem timestamps
- It does **not** tell you *what* changed — only *that* something may need review

Staleness warnings are **advisory only**. They flag that a human should review the relationship between the two artifacts.

### Implementation

The detection logic lives in `_build_staleness_warnings()` inside:
```
extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py
```

It resolves artifact paths from `01-bmad-config.md` aliases (`planning_artifacts`, `implementation_artifacts`) so it works correctly regardless of project location.

Graceful degradation: if any artifact file is missing, that rule is silently skipped. The function never raises an exception.

---

## Consistency Check

### What It Is

The consistency check is a deeper, on-demand semantic validation. Unlike staleness detection (which only checks timestamps), the consistency check reads actual file content and validates coverage across artifact boundaries.

It is implemented as a BMAD task file:
```
skills/bmad-init/core/tasks/consistency-check.md
```

### Five Consistency Rules

| Rule | What It Checks |
|------|----------------|
| CC-01 | Every PRD Functional Requirement is covered in the Architecture document |
| CC-02 | Every Architecture component has at least one Epic |
| CC-03 | Every Epic has at least one Story |
| CC-04 | Every Story references a valid Epic ID (no orphan stories) |
| CC-05 | Every story referenced in a Sprint Plan actually exists as a file |

### When to Run It

Run the consistency check when:

- **A PRD update has been merged** — verify architecture still covers all requirements
- **A new architecture version is finalized** — verify epics cover all new components
- **Before starting a new sprint** — verify no orphan stories or phantom sprint references
- **A staleness warning has been active for more than one sprint** — the warning has become chronic; investigate the gap
- **Onboarding a new team member** — use the report to establish a shared understanding of project state

### How to Trigger It

Instruct bmad-master:
```
Run the consistency check for this project
```

bmad-master will load `skills/bmad-init/core/tasks/consistency-check.md` and execute it, producing a structured report listing any gaps found.

### Output Format

The check produces a consistency report:

```
# Cross-Artifact Consistency Report
Date: YYYY-MM-DD
Artifacts checked: [prd.md, architecture-*.md, epics*.md, story-*.md]

## Summary
- CC-01 gaps: 0
- CC-02 gaps: 1
- CC-03 gaps: 0
- CC-04 gaps: 0
- CC-05 gaps: 0
- OVERALL: GAPS FOUND

## CC-02 — Architecture Component Coverage Gaps
- Component: "Notification Service" — no associated epic found
  Recommended action: Create Epic covering notification delivery pipeline
```

---

## Resolving Staleness and Consistency Gaps

### Staleness Warnings

| Warning | Resolution |
|---------|------------|
| Architecture stale | Review PRD changes → update architecture sections affected → re-run CC-01 |
| Sprint plan stale | Review architecture changes → identify new/removed components → update epics/stories → re-cut sprint plan |

### Consistency Gaps

| Gap Type | Resolution |
|----------|------------|
| CC-01 — FR not in architecture | Add an architecture section or ADR entry addressing the requirement |
| CC-02 — Component without epic | Create an epic for the uncovered component before next sprint |
| CC-03 — Empty epic | Either create stories for the epic or merge it into a related epic |
| CC-04 — Orphan story | Update the story's epic reference to a valid Epic ID |
| CC-05 — Phantom sprint story | Create the missing story file or remove the reference from the sprint plan |

**Resolution priority order:** CC-05 (blocks execution) → CC-04 (story has no home) → CC-01 (requirements traceability) → CC-02 (component coverage) → CC-03 (empty epics)

---

## File Reference

| File | Purpose |
|------|---------|
| `.a0proj/knowledge/main/artifact-relationships.md` | Artifact DAG, staleness rules, consistency rules — FAISS-preloaded |
| `extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py` | Staleness detection implementation (`_build_staleness_warnings()`) |
| `skills/bmad-init/core/tasks/consistency-check.md` | On-demand consistency check task |
| `docs/document-lifecycle.md` | This document — framework overview |

---

## Design Principles

This framework is intentionally **lightweight**:

- **No blocking** — warnings and reports only; never prevents work
- **No new processes** — staleness detection piggybacks on the existing `_80` extension
- **No overhead in green state** — if no artifacts exist yet, all checks skip silently
- **Filesystem-first** — staleness uses mtime (fast, no parsing); consistency check is opt-in
- **Graceful degradation** — missing files, unresolvable aliases, and parse errors all fail silently

The goal is to surface information that a team would otherwise miss, without creating ceremony that slows them down.
