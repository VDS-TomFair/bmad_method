# ADR 0009: Phase H — BMB Creation Path Fixes

**Date:** 2026-05-01
**Status:** Accepted
**Phase:** H

## Context

BMB (BMAD Module Builder) agents and workflows were created by the workflow-builder and agent-builder into `.a0proj/_bmad-output/bmb-creations/`, a directory that Agent Zero does **not** scan for agents or skills. This meant every created agent/workflow was invisible to A0's discovery system and could not be used without manual file moves.

The root cause was a single config variable `bmb_creations_output_folder` that pointed to a non-discoverable path, and no mechanism to promote creations from project scope to plugin scope.

## Decision

### 1. Split config into staging vs build output paths

Replace the single `bmb_creations_output_folder` with three distinct variables:

| Variable | Path | Purpose |
|---|---|---|
| `bmb_staging_folder` | `.a0proj/_bmad-output/bmb-staging/` | Intermediate build artifacts, validation output |
| `bmb_build_output_agents` | `.a0proj/agents/` | Final agent output — directly in A0 discovery path |
| `bmb_build_output_skills` | `.a0proj/skills/` | Final skill/workflow output — directly in A0 discovery path |

**Rationale:** Separating staging from final output prevents half-built artifacts from being discovered by A0. Staging is for intermediate files; build output is the final, A0-visible location.

### 2. BMB creations go to A0-discoverable directories

Agent Zero discovers agents from `.a0proj/agents/` and skills from `.a0proj/skills/` automatically. By writing final build output directly to these paths, created agents and workflows are immediately usable after the BMB workflow completes — no manual steps required.

**Rationale:** Aligns with A0's built-in discovery mechanism. Users should not need to understand file system layout to use agents they just built.

### 3. Two-phase approach: create in project, promote to plugin

Phase 1 (automatic): BMB writes to `.a0proj/agents/` and `.a0proj/skills/` — available in the current project.

Phase 2 (manual): `bmad-promote` skill copies from project scope to plugin scope (`plugins/bmad_method/agents/` or `plugins/bmad_method/skills/`) making creations available across all projects.

**Rationale:** Not every creation deserves plugin-level distribution. The two-phase model lets users test locally before promoting to shared scope. Promotion is explicit and intentional.

### 4. bmad-init.sh creates discovery directories

The init script now creates `.a0proj/agents/` and `.a0proj/skills/` directories during project initialization.

**Rationale:** Prevents "directory not found" errors when BMB writes its first artifact. Directories exist from the start.

### 5. Security: path traversal validation in promote.sh

The promote script validates names to prevent path traversal attacks:
- Rejects names containing `/` or `..`
- Rejects names starting with `-` (flag injection)
- Only allows alphanumeric names with dots and hyphens

**Rationale:** Promotion copies files between directories. Without validation, a crafted name like `../../etc/passwd` could write outside intended boundaries.

## Consequences

### Positive
- BMB-created agents and skills are immediately discoverable by A0
- Clear separation between staging artifacts and final output
- Users can test creations locally before promoting to plugin scope
- No manual file moves required for basic usage
- Security-hardened promotion script

### Negative
- Slightly more complex config (3 variables vs 1)
- ~70 step files updated with new variable references
- Promotion to plugin scope still requires explicit user action

### Neutral
- `.a0proj/_bmad-output/` remains for staging and intermediate artifacts
- Module creations still go to staging (A0 has no `modules` discovery path)

## Test Coverage

- `tests/test_phase_h_paths.py`: Config split verification, step file path updates, celebrate step content
- `tests/test_phase_h_promote.py`: 17 tests — name validation, type routing, error handling, trigger phrases
- Total: 327 tests pass, 94 subtests, 0 failures
