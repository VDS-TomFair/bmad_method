# ADR-0007: Upstream BMAD-METHOD v6.6.0 Sync (Phase F)

## Status
Accepted

## Date
2026-05-01

## Context

The upstream BMAD-METHOD repository advanced from commit 88b9a1c to 9debc16 (v6.6.0), introducing 37 files changed with +3422/-312 lines. Our A0 BMAD Method plugin had diverged from upstream in several workflow steps and lacked new customization infrastructure added upstream.

Key upstream changes requiring sync:
1. **Pre-checked checklists** in architecture validation (step-07) — upstream fixed this, our copy still had them
2. **File churn detection** missing from epic design (step-02) and final validation (step-04)
3. **Config migration** — `project_name` moved from bmm config to core config
4. **Customization infrastructure** — upstream added 30 `customize.toml` files and a resolve script
5. **Version alignment** — all config Version fields needed updating to 6.6.0

## Decision

Sync with upstream v6.6.0 using a 5-step merge protocol for each file:
1. Read our current file (preserving A0-specific sections)
2. Read upstream file
3. Merge: accept upstream workflow logic, preserve A0 path conventions (`$P/{skill}/...`)
4. Verify YAML frontmatter and A0 sections intact
5. Test with pytest

12 tasks organized by priority:
- **P0 (3 tasks)**: Critical workflow fixes — pre-checked checklists, file churn detection in epics and validation
- **P1 (6 tasks)**: Config migration, version updates, resolve_customization.py, bmad-customize skill, 30 customize.toml files
- **P2 (2 tasks)**: CHANGELOG update, version bump to 1.1.0

### What We Adapted for A0

- **Path conventions**: All file references use `$P/{skill}/...` A0 variable syntax instead of upstream's hardcoded paths
- **resolve_customization.py**: Adapted to use `$A0PROJ` environment variable for project root detection
- **bmad-customize skill**: Discovery script uses A0 skill layout conventions
- **Config migration**: `project_name` moved to `bmad-init/core/config.yaml` (A0's core config) rather than upstream's location
- **No CSV changes**: Upstream CSV files verified safe — no `project_name` references found

## Alternatives Considered

### Full upstream overlay (replace everything)
- Pros: Simplest to execute, guaranteed exact match
- Cons: Loses A0-specific customizations, path conventions, and agent adaptations
- Rejected: Would break A0 integration points

### Cherry-pick only P0 fixes
- Pros: Minimal risk, smallest change surface
- Cons: Misses customization infrastructure (30+ toml files, resolve script), config alignment drifts further
- Rejected: Technical debt accumulates, customization story incomplete

### Defer to next release
- Pros: More testing time
- Cons: Pre-checked checklist bug remains live, file churn gap unfixed
- Rejected: P0 fixes are user-facing bugs that should ship now

## Consequences

### Positive
- **3 critical workflow bugs fixed**: Pre-checked checklists, missing file churn detection in epics and validation
- **Customization infrastructure**: 30 customize.toml files + resolve_customization.py enable 3-layer TOML merge (base → project → user)
- **New bmad-customize skill**: Users can discover and customize any BMAD skill
- **48 new tests**: Test coverage increased from 200 to 248 (24% increase)
- **Config alignment**: All 4 skill configs at Version 6.6.0, plugin at 1.1.0

### Negative
- **Migration required**: Existing projects referencing `project_name` in bmm config must update to core config
- **Behavior change**: step-07 validation no longer has pre-checked items — users must actively validate each item
- **Larger diff**: 37 files changed in a single sync, harder to bisect if issues arise

### Risks Mitigated
- **Test coverage**: 248 tests provide regression safety net
- **Code review approved**: 0 blocking issues found in docs/code-review-phase-f.md
- **Atomic commit**: Single commit on develop with detailed message for easy revert if needed

## Deprecation Notices

### project_name config migration (Advisory)
- **What changed**: `project_name` moved from `skills/bmad-bmm/config.yaml` to `skills/bmad-init/core/config.yaml`
- **Who is affected**: Existing projects that reference bmm config for project_name
- **Migration**: Update config references from bmm to core config location
- **Timeline**: Advisory — bmm config still works as fallback during transition

### Pre-checked checklists replaced (Advisory)
- **What changed**: step-07-validation.md no longer has pre-checked `[x]` items
- **Who is affected**: Users relying on pre-populated validation results
- **Migration**: Users must actively validate each checklist item
- **Timeline**: Immediate — conditional validation is the correct behavior
