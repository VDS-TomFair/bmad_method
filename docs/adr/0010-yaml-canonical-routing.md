# ADR-0010: YAML as Canonical Routing Mechanism

**Status:** Accepted
**Date:** 2026-05-02
**Supersedes:** ADR-0001 (CSV as Canonical Routing Mechanism)
**Phase:** Bundle 1 — CSV → YAML Migration (P0)

## Context

ADR-0001 established CSV (`module-help.csv`) as the canonical routing mechanism for the BMAD Method A0 Plugin. Since that decision, the upstream BMAD Method has migrated to YAML-based `module.yaml` files as the canonical source for module configuration and routing (source: [BMAD Method docs — How to Customize BMad](https://docs.bmad-method.org/how-to/customize-bmad/)).

The CSV format presented several issues:
- **Maintenance burden**: Two metadata sources per skill (CSV + SKILL.md) required manual synchronization
- **Schema fragility**: CSV column ordering was brittle; adding/removing columns risked data corruption
- **Upstream divergence**: ADR-0001's rationale ("upstream also uses CSV") is no longer accurate — upstream now uses YAML
- **IDE compatibility**: The 13-column CSV schema was designed for IDE integrations that the A0 plugin does not use

## Decision

**Migrate from CSV (`module-help.csv`) to YAML (`module.yaml`) as the canonical routing mechanism**, aligning with upstream BMAD Method's current format.

## Rationale

- **Upstream alignment**: BMAD Method now uses `module.yaml` with a `workflows:` array as the canonical format (source: `docs-website-research.md`, upstream module.yaml structure)
- **Single source of truth**: YAML's structured format eliminates the need for column-indexed parsing
- **Schema flexibility**: Adding new fields to YAML does not require updating every module file
- **YAML safe loading**: Using `yaml.safe_load()` from Python stdlib (3.11+) with no custom constructors
- **Routing contract preserved**: The routing manifest output format is byte-identical to the CSV version — all consumers (agents, dashboard) are unaffected

## Migration Details

| Aspect | Before (CSV) | After (YAML) |
|--------|-------------|-------------|
| File name | `module-help.csv` | `module.yaml` |
| Parsing | `csv.DictReader` | `yaml.safe_load()` |
| Schema | 13-column header row | Structured dict with `workflows:` array |
| Caching | mtime-keyed (preserved) | mtime-keyed (preserved) |
| Output format | JSON routing manifest | JSON routing manifest (unchanged) |

### Files Changed

- `skills/bmad-init/module.yaml` — new YAML routing file
- `skills/bmad-init/core/module.yaml` — new YAML routing file
- `skills/bmad-bmm/module.yaml` — new YAML routing file
- `skills/bmad-cis/module.yaml` — new YAML routing file
- `skills/bmad-tea/module.yaml` — new YAML routing file
- `skills/bmad-bmb/module.yaml` — new YAML routing file
- `extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py` — YAML parser
- All 6 `module-help.csv` files deleted

### Conversion Script

`scripts/archive/csv_to_yaml_converter.py` — one-time conversion script (now archived) that reads all CSV files and produces YAML equivalents with zero data loss.

## Consequences

- **Positive:** Full upstream alignment with BMAD Method's current format
- **Positive:** Simpler schema — no column-indexed parsing
- **Positive:** Routing manifest output unchanged — no consumer breakage
- **Positive:** All 337 tests pass after migration
- **Negative:** `yaml` module required (Python 3.11+ stdlib `tomllib` used by resolve scripts; `yaml` is already a dependency)
- **Negative:** BMB module builder templates still reference `module-help.csv` internally (these are scaffolding templates, not routing files — tracked separately)

## Alternatives Considered

1. **Keep CSV** — would maintain divergence from upstream
2. **Dual-read compatibility** — adds complexity without benefit; clean migration is simpler
3. **TOML routing** — upstream uses YAML, not TOML; TOML is used for customization overlay (resolve_customization.py) but not for routing
