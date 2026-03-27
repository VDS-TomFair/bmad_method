# Changelog

All notable changes to the BMAD Method plugin are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.1] — 2026-03-27

### Fixed
- **`module-help.csv` column naming** — Renamed ambiguous `skill` column to `agent` in all 5 module CSV files (`bmad-bmb`, `bmad-bmm`, `bmad-cis`, `bmad-init`, `bmad-tea`). The column contains agent identifiers, not A0 skill names — the old name caused confusion with the `skills_tool` system.
- **Routing extension column priority** — `_80_bmad_routing_manifest.py` now reads `agent` column first, with `skill` and `agent-name` retained as legacy fallbacks for backward compatibility.

### Improved
- **LW (List Workflows) now reads dynamically** — The `LW` command now reads directly from `skills/*/module-help.csv` at runtime (same as the routing extension), eliminating the sync risk with the compiled `bmad-help.csv` aggregate.
- **Natural language routing fallback updated** — Fallback CSV read (when routing extension is unavailable) now also uses dynamic module CSVs instead of the compiled aggregate.
- **Column name consistency** — All prompt references updated: `skill-name` → `action`, `workflow-file` → `args`, `agent-name` → `agent` throughout BMad Master prompt files.
- **Manifest table clarified** — `bmad-help.csv` now labelled as "compiled aggregate" with a note explaining it is a snapshot only, not the routing source of truth.

---

## [1.0.0] — 2026-02-28

### Initial Release
- Full BMAD Method Framework integration for Agent Zero
- 20 specialist agents across 4 modules: BMM, BMB, TEA, CIS
- 5 skill packages with bundled workflow files
- Project-scoped FAISS-native shared memory store
- Phase-aware routing extension (`_80_bmad_routing_manifest.py`)
- Interactive BMAD status dashboard plugin
- Party Mode (single-LLM multi-persona simulation)
- `bmad-init` bootstrap script for workspace initialization
- Phase Gate Protocol (GATE-001) enforcement
