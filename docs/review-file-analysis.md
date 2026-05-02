# BMAD Method A0 Plugin — File Review Analysis

**Date:** 2026-05-02
**Reviewer:** Deep Research Agent (automated)
**Files Reviewed:** 24

---

## Summary

All 24 requested files were read and analyzed. The codebase is well-structured with consistent patterns across module definitions, agent prompts, and infrastructure code. A few minor issues were identified (trailing whitespace, a no-op import script, cross-module path dependencies) — none are blockers.

---

## File-by-File Analysis

### 1. `skills/bmad-tea/module.yaml`

- **Line count:** 120
- **Key content:** Defines the TEA (Test Engineering Architecture) module with 9 workflows covering the full testing lifecycle: Teach Me Testing (Phase 0), Test Design (Phase 3), Test Framework (Phase 3), CI Setup (Phase 3), ATDD (Phase 4), Test Automation (Phase 4), Test Review (Phase 4), NFR Assessment (Phase 4), and Traceability (Phase 4). Each workflow has consistent structure: module, skill, display-name, menu-code, description, action, args, phase, after, before, required, output-location, outputs.
- **Issues:** Clean. Consistent structure, all fields populated.

---

### 2. `skills/bmad-cis/module.yaml`

- **Line count:** 87
- **Key content:** Defines the CIS (Creative Innovation Suite) module with 6 workflows: Innovation Strategy, Problem Solving, Design Thinking, Brainstorming, Storytelling, Presentation. All workflows are phase `anytime`. Uses varied skill names (innovation-strategist, creative-problem-solver, design-thinking-coach, brainstorming-coach, storyteller, presentation).
- **Issues:** Cross-module dependency — the Brainstorming workflow (line 53) points to `skills/bmad-init/core/workflows/brainstorming/workflow.md` rather than a path under `bmad-cis`. This is intentional (core owns brainstorming), but creates a hidden coupling.

---

### 3. `skills/bmad-bmb/module.yaml`

- **Line count:** 261
- **Key content:** Defines the BMB (BMad Builder) module with 17 workflows covering agent CRUD (Build/Edit/Validate Agent), module CRUD (Ideate/Create Brief/Create/Edit/Validate Module), workflow CRUD (Build/Edit/Validate/Rework Workflow, Max Parallel Validate, Convert Skill), quality scanning (Quality Scan Agent/Workflow), setup (Setup Builder), and validation (Validate Skill, Validate File References). Includes a documentation header explaining that CSV files in BMB are intentional data/templates, not routing CSVs.
- **Issues:** Clean. Intentional menu-code duplicates documented with inline comments (QA on lines 196-197, VS on lines 237-238). Module-scoped routing means these are not collisions.

---

### 4. `skills/bmad-init/core/module.yaml`

- **Line count:** 156
- **Key content:** Defines the Core Utilities module with 11 workflows: Brainstorming, Party Mode, bmad-help, Index Docs, Shard Document, Editorial Review (Prose), Editorial Review (Structure), Adversarial Review (General), Edge Case Hunter Review, Advanced Elicitation, and Distillator. All are phase `anytime`. Skills are assigned to `analyst`, `party-mode facilitator`, and `bmad-master`.
- **Issues:** Clean. The brainstorming workflow path `skills/bmad-init/core/workflows/brainstorming/workflow.md` is the same path referenced by CIS module.yaml — confirming the cross-module dependency is by design.

---

### 5. `prompts/bmad-agent-shared.md`

- **Line count:** 187
- **Key content:** The shared activation protocol for all BMAD agents. Defines an 8-step activation sequence: (1) Resolve Customization via Python script, (2) Execute Prepend Steps, (3) Review Project State, (4) Review Project Config, (5) Load Persistent Facts, (5.5) Load Sidecar Memory, (6) Greet as Persona, (7) Execute Append Steps, (8) Present Menu or Dispatch. Also defines sidecar memory writing rules, initial clarification protocol, thinking framework, tool calling guidelines, and file/artifact handling rules.
- **Issues:** Clean. Well-structured with clear step numbering and detailed instructions. The Step 5.5 insertion is slightly awkward (between 5 and 6) but functionally correct.

---

### 6. `prompts/bmad-agent-shared-solving.md`

- **Line count:** 16
- **Key content:** Short process-compliance rules for BMAD agents. Seven rules emphasizing process-driven behavior: load skill first, follow step-file architecture, execute sequentially, read each step, halt at checkpoints, produce artifacts only through process, use text_editor:patch for large artifacts, update state after phase transitions.
- **Issues:** Clean. Concise and focused.

---

### 7. `scripts/resolve_customization.py`

- **Line count:** 237
- **Key content:** Three-layer TOML merge script for BMAD skill customization. Layers (highest priority first): (1) `{project}/_bmad/custom/{name}.user.toml` (personal, gitignored), (2) `{project}/_bmad/custom/{name}.toml` (team/org), (3) `{skill-root}/customize.toml` (defaults). Implements deep merge with structural rules: scalars override, tables deep merge, arrays use keyed merge (by `code` or `id` field) or append fallback. Supports dotted key extraction via `--key` flag. Requires Python 3.11+ (stdlib `tomllib`).
- **Issues:** Clean. Well-documented with comprehensive docstring. Error handling is thorough (missing files, parse errors, Python version checks). Project root discovery walks upward looking for `_bmad` or `.git`.

---

### 8. `skills/bmad-init/scripts/bmad-init.sh`

- **Line count:** 124
- **Key content:** Project initialization script. Creates directory structure (output, knowledge, instructions, agents, skills, sidecar memory), seeds knowledge from `seed-knowledge/` (no-clobber), writes `01-bmad-config.md` (path aliases), `bmad-user-prefs.promptinclude.md` (user settings), and `02-bmad-state.md` (initial state). Creates sidecar memory directories for 16 agents with initial `memories.md` stubs. Uses `rsync` when available, falls back to `cp -Rn`.
- **Issues:** Minor — line 28 uses `echo` with `\n` escape sequences, but without `echo -e` these will be literal `\n` characters instead of newlines in some shells. The `echo` builtin in bash without `-e` does not interpret escape sequences. Should be `echo -e` or use `printf`.

---

### 9. `agents/bmad-dev/agent.yaml`

- **Line count:** 6
- **Key content:** Agent definition for Amelia (Developer Agent). Contains title, description (Senior Software Engineer, test-driven implementation specialist), and context (Phase 4 Implementation specialist).
- **Issues:** Clean. Concise agent definition following standard 3-field pattern.

---

### 10. `agents/bmad-dev/prompts/agent.system.main.role.md`

- **Line count:** 100
- **Key content:** Full role prompt for Amelia (Developer Agent). Defines identity (name, icon, module, phase, profile), role description, 9 capabilities, communication style (ultra-succinct), 8 principles (TDD-focused), specialization, and operational directives. Includes two critical behavioral rules: Rule 1 (TDD Contract Rule — pre-written tests are sacred, never modify them) and Rule 2 (AC Traceability Protocol — every AC must be traceable to implementing code with inline comments).
- **Issues:** Clean. Well-structured with clear section hierarchy. The two behavioral rules are well-defined and non-negotiable.

---

### 11. `agents/bmad-module-builder/agent.yaml`

- **Line count:** 6
- **Key content:** Agent definition for Morgan (Module Creation Master). Expert module architect with BMAD Core systems knowledge, creates complete modules with agents, workflows, and infrastructure.
- **Issues:** Clean.

---

### 12. `agents/bmad-ux-designer/prompts/agent.system.main.role.md`

- **Line count:** 79
- **Key content:** Full role prompt for Sally (UX Designer). Identity (icon: palette emoji, Phase 2 Planning), role as empathy layer bridging PRD and Architecture, 10 capabilities (UX Design, User Research, Interaction Design, UI Patterns, Journey Mapping, Personas, Accessibility, Mobile/Responsive, Design Systems, Empathy Mapping). Communication style: filmmaker pitching the scene. 7 principles.
- **Issues:** Clean.

---

### 13. `agents/bmad-tech-writer/prompts/agent.system.main.role.md`

- **Line count:** 82
- **Key content:** Full role prompt for Paige (Technical Writer). Cross-phase documentation specialist. 9 capabilities (Project Documentation, Document Authoring, Standards Management, Mermaid Diagrams, Documentation Validation, Concept Explanation, API Documentation, Architecture Documentation, Standards Compliance). Communication style: patient educator. 7 principles emphasizing clarity and diagrams.
- **Issues:** Clean.

---

### 14. `agents/bmad-innovation/agent.yaml`

- **Line count:** 13
- **Key content:** Agent definition for Innovation Strategist (CIS module). Expert in Jobs-to-be-Done, Blue Ocean Strategy, and business model innovation.
- **Issues:** **Trailing whitespace** — the YAML multiline strings in `description` and `context` fields end with trailing newlines and leading spaces. The `context` field starts with a leading space (`' Innovation Strategist`). This is valid YAML but aesthetically inconsistent with the cleaner agent.yaml files (e.g., bmad-dev which is 6 lines). Also, the `title` field lacks the agent's name (just says "BMAD Innovation Strategist" unlike Amelia/Morgan which include names).

---

### 15. `agents/bmad-design-thinking/agent.yaml`

- **Line count:** 11
- **Key content:** Agent definition for Design Thinking Coach (CIS module). Expert in empathy mapping, prototyping, and user insights.
- **Issues:** **Same trailing whitespace pattern** as file 14. Leading space in `context` field. Title lacks agent name. Slightly different line count (11 vs 13) due to shorter description.

---

### 16. `agents/bmad-presentation/agent.yaml`

- **Line count:** 13
- **Key content:** Agent definition for Presentation Master (CIS module). Expert in visual hierarchy, audience psychology, and information design.
- **Issues:** **Same trailing whitespace pattern** as files 14-15. Leading space in `context` field. Title lacks agent name.

---

### 17. `agents/bmad-master/prompts/agent.system.main.role.md`

- **Line count:** 132
- **Key content:** Full role prompt for BMad Master (orchestrator agent). Defines BMAD identity, 4 modules (BMM, BMB, TEA, CIS), BMM phases table, available subordinates (dynamic via `{{agent_profiles}}`), orchestration behavior (initialization, routing, state management, help), and Phase Gate Protocol (GATE-001) enforcing strict phase prerequisites with hard rules.
- **Issues:** Clean. The Phase Gate Protocol is well-defined with explicit handling for phase skips and non-BMAD artifacts. Uses `{{agent_profiles}}` template variable for dynamic agent discovery.

---

### 18. `helpers/bmad_status_core.py`

- **Line count:** 122
- **Key content:** Shared data functions with zero A0 framework imports. Exports: `SKILL_NAMES` (5 canonical module names), `REQUIRED_PROMPTS` (2 agent prompt files), `AGENT_NAMES` (17 agent name mappings), `PHASE_ACTIONS` (phase-to-action mappings), and 4 functions: `read_state()`, `check_agents()`, `check_modules()`, `read_tests()`. Uses compiled regexes for state parsing.
- **Issues:** Clean. The `REQUIRED_PROMPTS` set includes `agent.system.main.communication_additions.md` — worth verifying all 17 agents have this file present.

---

### 19. `api/_bmad_status.py`

- **Line count:** 140
- **Key content:** API handler for BMAD status dashboard. Uses `importlib` to load `bmad_status_core.py` (avoiding name collision with A0's own `helpers` package). Resolves project root from A0 chat context (preferred) or symlink fallback. The `BmadStatus` handler returns state, agent health, skill status, test results, and recommendations.
- **Issues:** Clean. The importlib workaround is well-documented. Two extra blank lines on lines 60-61 are cosmetic only.

---

### 20. `webui/bmad-dashboard.html`

- **Line count:** 269
- **Key content:** Alpine.js dashboard with dark theme (Catppuccin-inspired CSS variables). Displays: recommended next action, project state (phase + artifact), agent health (health bar + chips for healthy/broken), modules status (skill badges), test results (pass/fail counts). References external `bmad-dashboard-store.js` for Alpine store logic.
- **Issues:** Clean. Inline CSS is dense but well-organized by section. Alpine.js directives are properly structured with `x-data`, `x-if`, `x-for`, `x-text`, `x-show`.

---

### 21. `skills/bmad-sidecar-import/SKILL.md`

- **Line count:** 57
- **Key content:** Skill definition for importing upstream BMAD Method sidecar memory files into A0 plugin. Has YAML frontmatter with trigger patterns. Documents when to use (migration from IDE-based BMAD), how it works (scans _bmad/_memory/), usage commands, and import details.
- **Issues:** Clean. The `/load-skill bmad-sidecar-import` usage example references an A0-specific command pattern.

---

### 22. `skills/bmad-sidecar-import/scripts/import-sidecars.sh`

- **Line count:** 63
- **Key content:** Bash script for sidecar import. Scans `$A0PROJ/_bmad/_memory/*-sidecar/` directories, iterates over `.md` files, reports found vs skipped. Uses no-clobber logic to preserve existing content.
- **Issues:** **Functional concern** — the script scans `$SOURCE_DIR` for sidecars and then checks files in the same `$sidecar_dir` for both source and target. It does not actually copy files from an upstream location. The script essentially just audits what already exists. The comment on line 49 says "For A0 plugin, files are already in place via init script" which means this script is a verification/reporting tool rather than an actual import mechanism. This may confuse users expecting a real import operation.

---

### 23. `docs/adr/0010-yaml-canonical-routing.md`

- **Line count:** 68
- **Key content:** Architecture Decision Record for migrating from CSV to YAML as the canonical routing mechanism. Documents context (upstream moved to YAML, CSV issues), decision (migrate to module.yaml), rationale (upstream alignment, single source of truth, schema flexibility), migration details (before/after comparison), files changed, and consequences.
- **Issues:** Clean. Well-structured ADR following standard format. Date is 2026-05-02, supersedes ADR-0001.

---

### 24. `docs/verification-report.md`

- **Line count:** 159
- **Key content:** Comprehensive verification report for 6 bundles of alignment fixes. Bundle 1 (CSV to YAML), Bundle 2 (Agent Consolidation — removed bmad-sm/bmad-qa/bmad-quick-dev), Bundle 3 (CIS Persona Removal — generic titles), Bundle 4 (Quick Fixes — icons, menu codes), Bundle 5 (Test Updates), Bundle 6 (P3 Structural — activation sequence, sidecar, project-context). 503 tests pass, 39 new tests added.
- **Issues:** Clean. Gaps section clearly documents false positives and acceptable exceptions.

---

## Cross-File Observations

### Pattern Consistency

- All 4 `module.yaml` files follow identical schema: `code`, `name`, `workflows[]` with consistent fields
- All agent role prompts (files 10, 12, 13, 17) follow the same structure: Mandatory Process Compliance, BMAD Persona (Identity, Role, Capabilities, Communication Style, Principles, Specialization, Operational Directives)
- Agent.yaml files have two patterns: 6-line (bmad-dev, bmad-module-builder) and 11-13 line (CIS agents) — the CIS agents have trailing whitespace

### Agent Health Note

`REQUIRED_PROMPTS` in `bmad_status_core.py` (file 18) requires `agent.system.main.communication_additions.md` in every agent's `prompts/` directory. This file was not in the review list — worth verifying its existence across all 17 agents.

### Sidecar Memory Coverage

The init script (file 8) creates sidecar directories for 16 agents, but `AGENT_NAMES` in file 18 lists 17 agents (including `bmad-storyteller`). The storyteller is missing from the init loop (line 22-26), though it is listed in `AGENT_NAMES`.

---

## Issue Summary

| # | File | Issue | Severity |
|---|------|-------|----------|
| 1 | `skills/bmad-init/scripts/bmad-init.sh` | `echo` with `\n` escapes but no `-e` flag on line 28 — may produce literal `\n` instead of newlines | Low |
| 2 | `agents/bmad-innovation/agent.yaml` | Trailing whitespace in YAML multiline strings, leading space in context | Low |
| 3 | `agents/bmad-design-thinking/agent.yaml` | Same trailing whitespace pattern as file 14 | Low |
| 4 | `agents/bmad-presentation/agent.yaml` | Same trailing whitespace pattern as file 14 | Low |
| 5 | `skills/bmad-cis/module.yaml` | Brainstorming workflow points to bmad-init/core path (cross-module dependency) | Info |
| 6 | `skills/bmad-sidecar-import/scripts/import-sidecars.sh` | Script is effectively a no-op audit tool — does not import from upstream | Medium |
| 7 | `skills/bmad-init/scripts/bmad-init.sh` | `bmad-storyteller` missing from sidecar creation loop (16 agents vs 17 in AGENT_NAMES) | Low |
| 8 | `agents/bmad-innovation/agent.yaml` (and 15, 16) | Title field lacks agent name (unlike bmad-dev "Amelia", bmad-module-builder "Morgan") | Low |

**No blockers found. All issues are low-severity or informational.**
