# Task: Cross-Artifact Consistency Check

**Task ID:** consistency-check  
**Version:** 1.0  
**Created:** 2026-04-09 (Story 034)  
**Owner:** bmad-master (orchestrator), bmad-architect (reviewer)  
**Trigger:** On demand — run when staleness warnings have been active, before sprint planning, or after PRD/architecture updates.

---

## Purpose

Perform a systematic cross-artifact consistency check across PRD, architecture document, epics, and stories. Identify gaps where requirements are untraced, components are uncovered, or stories are orphaned.

This task produces a **consistency report** — a structured gap list with recommended resolution actions.

---

## Prerequisites

Before running this task, ensure the following artifacts exist in the project:

| Artifact | Expected Location | Required |
|----------|------------------|----------|
| PRD | `planning_artifacts/prd.md` or `prd-*.md` | Yes |
| Architecture Doc | `planning_artifacts/architecture-*.md` | Yes |
| Epics listing | `implementation_artifacts/epics*.md` or in sprint plans | Yes |
| Story files | `implementation_artifacts/story-*.md` | Yes |

If PRD or Architecture are missing, stop and report `CONSISTENCY-CHECK: Cannot run — required artifacts missing.`

---

## Execution Steps

### Step 1 — Load artifacts

1. Read the PRD. Extract all **Functional Requirements (FRs)** — look for sections titled `Functional Requirements`, `Features`, `User Stories`, or numbered FR-NNN items.
2. Read the Architecture document. Extract all **components** — look for section headers, system topology descriptions, and service/module names.
3. Read the Epics listing. Extract all **Epic IDs and titles** — look for Epic-NNN or `## Epic N` patterns.
4. Scan implementation-artifacts for all `story-*.md` files. For each, extract the **Epic reference** (usually in frontmatter or `**Epic:**` field).

### Step 2 — Run consistency rules

Apply each rule in sequence. Record all gaps found.

#### CC-01: PRD Functional Requirements → Architecture Coverage

For each FR identified in the PRD:
- Search the architecture document for any reference to that requirement (by FR ID, feature name, or capability description)
- **Gap flag:** FR present in PRD but not mentioned or addressed in architecture

#### CC-02: Architecture Components → Epic Coverage  

For each major component or service in the architecture:
- Check that at least one Epic references or covers that component
- **Gap flag:** Architecture component with no associated Epic

#### CC-03: Epics → Story Coverage

For each Epic in the epics listing:
- Count the story files that reference that Epic ID
- **Gap flag:** Epic with zero associated stories

#### CC-04: Stories → Valid Epic Reference

For each story file:
- Check that its Epic reference matches an Epic ID in the epics listing
- **Gap flag:** Story with an Epic reference that does not exist in the epics listing (orphan story)

#### CC-05: Sprint Plan → Story File Existence

For each story referenced in any sprint-plan*.md:
- Check that the corresponding `story-NNN-*.md` file exists in implementation-artifacts
- **Gap flag:** Sprint plan references a story file that does not exist

### Step 3 — Produce consistency report

Output the following report structure:

```
# Cross-Artifact Consistency Report
Date: [YYYY-MM-DD]
Artifacts checked: [list files and their mtimes]

## Summary
- CC-01 gaps: N
- CC-02 gaps: N
- CC-03 gaps: N
- CC-04 gaps: N
- CC-05 gaps: N
- OVERALL: CONSISTENT | GAPS FOUND

## CC-01 — PRD FR Coverage Gaps
[List each uncovered FR with: FR ID, description, recommended architecture section to add]

## CC-02 — Architecture Component Coverage Gaps
[List each uncovered component with: component name, recommended epic to create]

## CC-03 — Empty Epics
[List each epic with no stories: Epic ID, title, recommended stories to create]

## CC-04 — Orphan Stories
[List each orphan story: story file, referenced Epic ID, valid Epic IDs available]

## CC-05 — Phantom Sprint Stories
[List each phantom: sprint plan file, story reference, resolution action]

## Recommended Resolution Order
1. Fix CC-05 phantom stories (sprint plan risk — blocks execution)
2. Fix CC-04 orphan stories (story has no home — assign to correct epic)
3. Resolve CC-01 FR gaps (architecture completeness)
4. Resolve CC-02 component gaps (create missing epics)
5. Resolve CC-03 empty epics (create stories or remove empty epic)
```

---

## Escalation

If the consistency check reveals **more than 3 CC-01 gaps**, flag for architecture review session before the next sprint begins. Untraced functional requirements represent implementation risk.

If any CC-05 phantom stories are found, halt sprint planning until resolved — phantom stories indicate a planning document out of sync with the actual story backlog.

---

## Related

- Artifact relationship rules: `.a0proj/knowledge/main/artifact-relationships.md`
- Staleness detection: `extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py`
- Framework overview: `docs/document-lifecycle.md`
