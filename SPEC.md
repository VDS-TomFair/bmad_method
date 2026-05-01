# Spec: BMAD Method Plugin — Upstream v6.6.0 Sync (v1.2)

**Date:** 2026-05-01  
**Status:** Draft — pending user approval  
**Branch:** `develop` (merge to `main` on `/ship`)  
**Scope:** Phase F (upstream v6.6.0 sync) — Phases A–D ✅ COMPLETE  
**Upstream sync:** `88b9a1c` → `9debc16` (v6.6.0, 37 files changed)

---

## Objective

Sync the BMAD Method A0 plugin (v1.0.8) with upstream BMAD-METHOD v6.6.0, incorporating critical workflow step improvements, config migration, and evaluating new upstream features for A0 compatibility.

**Prior work (COMPLETE):** Phases A–D delivered 35 tasks, 200 tests, 49 commits — full A0 alignment migration fixing all Critical bugs, aligning structural conventions, consolidating routing, and polishing UX surface. See [CHANGELOG.md](CHANGELOG.md) for details.

**This phase targets:**

- **P0 (Critical):** Sync 3 workflow step files with upstream v6.6.0 content (architecture checklist fix, design epics file churn, final validation hook)
- **P1 (High):** Migrate `project_name` from bmm config to core config, update version headers
- **P2 (Nice to have):** Evaluate `bmad-customize` skill for A0, update CHANGELOG

**Target user:** Individual developer using Agent Zero for personal software projects. BMAD is **project-scoped** — each project gets independent BMAD state, initialization, and knowledge. BMAD must work in any A0 project (`.a0proj/` present) or A0 workdir. Not limited to `/a0/usr/projects/`.

**What success looks like:**
- All 3 critical workflow steps match upstream v6.6.0 content
- Config migration complete (`project_name` in core config, versions updated to 6.6.0)
- Plugin version bumped to v1.1.0 (feature addition from upstream sync)
- All A0-specific additions (Step Complete sections, YAML frontmatter, trigger_patterns) preserved
- All 200+ existing tests continue to pass

---

## Tech Stack

| Layer | Technology | Notes |
|---|---|---|
| Runtime | Python 3.10+ | A0 plugin conventions |
| Init scripts | Bash | `set -euo pipefail` required |
| WebUI | Alpine.js + vanilla JS | Store-gated, `x-text` only (no `x-html`) |
| A0 version | `agent0ai/agent-zero:latest` ≥ 0.9.0 | Per `min_a0_version` in plugin.yaml |
| Key A0 imports | `helpers.api`, `helpers.projects`, `helpers.extension`, `agent.AgentContext`, `agent.LoopData` | Never re-implement these |
| Testing | `pytest` | Existing `tests/test_extension_80.py` pattern |
| VCS | Git | `develop` branch → `main` on /ship |
| Deployment | VPS `162.19.152.199` | Plugin dir mapped to testing instance |
| Upstream | BMAD-METHOD v6.6.0 | `.a0proj/upstream/BMAD-METHOD/` local clone |

---

## Commands

```bash
# Run all tests
cd /a0/usr/projects/a0_bmad_method && python -m pytest tests/ -v

# Check HTML validity
tidy -e webui/bmad-dashboard.html 2>&1 | grep -E "^(Error|Warning)"

# Validate bash syntax
bash -n skills/bmad-init/scripts/bmad-init.sh

# Lint Python (max 100 chars)
python -m flake8 api/ helpers/ extensions/ --max-line-length 100

# Test BMAD init on arbitrary path (smoke test)
bash skills/bmad-init/scripts/bmad-init.sh /tmp/test-bmad-project
grep 'A0PROJ' /tmp/test-bmad-project/.a0proj/instructions/01-bmad-config.md  # must NOT contain /a0/usr/projects

# Diff workflow step against upstream
diff skills/bmad-bmm/workflows/3-solutioning/create-epics-and-stories/steps/step-02-design-epics.md \
     .a0proj/upstream/BMAD-METHOD/src/bmm-skills/create-epics-and-stories/steps/step-02-design-epics.md

# Git: create dev branch
git -C /a0/usr/projects/a0_bmad_method checkout -b develop
git -C /a0/usr/projects/a0_bmad_method push origin develop

# Deploy to VPS testing instance
# Architecture:
#   Dev container:     /a0 (= /home/debian/agent-zero/development on VPS host)
#   Testing container: mounts /home/debian/agent-zero/testing as /a0 (SEPARATE container)
#   Plugin symlink:    testing/usr/plugins/bmad_method -> ../projects/a0_bmad_method (RELATIVE)
#   Plugin source:     testing/usr/projects/a0_bmad_method (git clone of github.com/vanja-emichi/bmad_method)
#
# Deploy workflow: commit + push here → git pull on testing
git -C /a0/usr/projects/a0_bmad_method add -A
git -C /a0/usr/projects/a0_bmad_method commit -m "<message>"
git -C /a0/usr/projects/a0_bmad_method push origin develop

# Pull changes into testing instance
ssh -i /a0/usr/.ssh/id_ed25519 -o StrictHostKeyChecking=no root@162.19.152.199 \
  'docker exec agent-zero-testing bash -c "cd /a0/usr/projects/a0_bmad_method && git pull origin develop"'

# Optional: restart testing container to fully reload plugin
ssh -i /a0/usr/.ssh/id_ed25519 -o StrictHostKeyChecking=no root@162.19.152.199 \
  'docker restart agent-zero-testing'

# Live testing via A2A protocol (testing instance)
# Endpoint: https://testing.emichi.co/a2a/t-uFypjRGDwc2M2NtW/p-test
# Use a2a_chat tool:
#   tool_name: a2a_chat
#   tool_args:
#     agent_url: "https://testing.emichi.co/a2a/t-uFypjRGDwc2M2NtW/p-test"
#     message: "<test prompt>"
#     reset: true   ← start fresh session
#     reset: false  ← continue session

# Docker logs — inspect what the testing agent actually did
ssh -i /a0/usr/.ssh/id_ed25519 -o StrictHostKeyChecking=no root@162.19.152.199 \
  'docker logs agent-zero-testing --tail 100'

# Follow logs in real time during A2A test
ssh -i /a0/usr/.ssh/id_ed25519 -o StrictHostKeyChecking=no root@162.19.152.199 \
  'docker logs agent-zero-testing --follow --tail 50'

# Container name discovery (if name differs)
ssh -i /a0/usr/.ssh/id_ed25519 -o StrictHostKeyChecking=no root@162.19.152.199 \
  'docker ps --format "{{.Names}}\t{{.Image}}\t{{.Status}}"'
```

---

## Project Structure

```
/a0/usr/projects/a0_bmad_method/
│
├── plugin.yaml                          ← per_project_config: true ✅
├── SPEC.md                              ← this file
├── CHANGELOG.md
├── README.md
├── .gitignore                           ← ✅ DONE: .kilo/ .cursor/ .claude/ .windsurf/ added
│
├── api/
│   └── _bmad_status.py                  ← ✅ DONE: None-guard, _recommend() caching
│
├── helpers/
│   ├── __init__.py
│   └── bmad_status_core.py              ← ✅ DONE: read_state(), AGENT_NAMES, PHASE_ACTIONS, PHASE_BUCKET_PREFIXES
│
├── extensions/
│   ├── python/
│   │   └── message_loop_prompts_after/
│   │       └── _80_bmad_routing_manifest.py  ← ✅ DONE: mtime caching, log.warning, dead code removed
│   └── webui/
│       └── sidebar-quick-actions-main-start/
│           └── _bmad_dashboard_btn.html
│
├── agents/                              ← 20 bmad-* profiles (idiomatic ✅)
│   ├── _shared/
│   │   └── prompts/
│   │       └── bmad-agent-shared.md     ← ✅ DONE: shared fragment (85 lines)
│   ├── bmad-master/
│   │   └── prompts/
│   │       ├── agent.system.main.role.md      ← ✅ DONE: dynamic via {{agent_profiles}}
│   │       ├── agent.system.main.specifics.md ← ✅ DONE: includes shared fragment
│   │       └── ...
│   └── bmad-pm/ ... (19 more — same shared include ✅)
│
├── skills/
│   ├── bmad-init/
│   │   ├── SKILL.md                    ← ✅ DONE: trigger_patterns added
│   │   ├── module-help.csv             ← ✅ DONE: upstream 13-col schema
│   │   ├── core/
│   │   │   └── config.yaml             ← Phase F: add project_name, update version
│   │   └── scripts/
│   │       ├── bmad-init.sh            ← ✅ DONE: $A0PROJ paths, set -euo pipefail
│   │       └── bmad-status.py          ← ✅ DONE: importlib, BMAD_DEV_MODE gate
│   ├── bmad-bmm/
│   │   ├── config.yaml                 ← Phase F: remove project_name, update version
│   │   ├── module-help.csv             ← ✅ DONE: upstream 13-col schema
│   │   └── workflows/
│   │       └── 3-solutioning/create-epics-and-stories/steps/
│   │           ├── step-02-design-epics.md      ← Phase F P0: sync with upstream v6.6.0
│   │           └── step-04-final-validation.md  ← Phase F P0: sync with upstream v6.6.0
│   │       └── 3-solutioning/create-architecture/steps/
│   │           └── step-07-validation.md        ← Phase F P0: sync with upstream v6.6.0
│   ├── bmad-tea/                        ← ✅ DONE: trigger_patterns, CSV aligned
│   ├── bmad-cis/                        ← ✅ DONE: trigger_patterns, CSV aligned
│   └── bmad-bmb/                        ← ✅ DONE: trigger_patterns, CSV aligned
│
├── webui/
│   ├── bmad-dashboard.html             ← ✅ DONE: HTML fixed
│   └── bmad-dashboard-store.js         ← ✅ DONE: orphan removed
│
├── prompts/                            ← ✅ DONE
│   └── bmad.methodology.shared.md      ← shared fragment (85 lines)
│
├── tests/                              ← 200+ tests ✅
│   ├── test_extension_80.py            ← routing extension tests
│   ├── test_bmad_status_core.py        ← read_state() variants
│   ├── test_bmad_init_sh.py            ← shell integration tests
│   └── ... (27+ more test files)
│
├── docs/
│   ├── upstream-sync-report-6.6.0.md   ← Phase F source of truth for sync
│   ├── alignment-analysis.md
│   ├── document-lifecycle.md
│   └── adr/                            ← 6 architecture decision records
│
└── .a0proj/
    └── upstream/BMAD-METHOD/           ← upstream repo clone (v6.6.0)
```

---

## Code Style

### Python — canonical example (helpers/bmad_status_core.py style)

```python
import re
import logging
from pathlib import Path

log = logging.getLogger(__name__)

# Module-level compiled regexes — UPPER_CASE with _RE suffix
_PHASE_RE = re.compile(
    r"^\s*[-*]?\s*Phase\s*:\s*(.+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)
_ARTIFACT_RE = re.compile(
    r"^\s*[-*]?\s*Active Artifact\s*:\s*(.+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)

# Shared constants — single source of truth, imported by API + CLI + extension
PHASE_BUCKET_PREFIXES: dict[str, str] = {
    "1-": "1-analysis",
    "2-": "2-planning",
    "3-": "3-solutioning",
    "4-": "4-implementation",
}

AGENT_NAMES: dict[str, str] = {
    "bmad-master": "BMad Master",
    "bmad-analyst": "Mary (Analyst)",
    # ... 18 more
}


def read_state(state_file: Path) -> dict:
    """Parse 02-bmad-state.md — single source of truth for phase/artifact/issues.

    Returns lowercase phase, artifact string, and list of open ARCH/DEFECT items.
    Never raises — caller should handle None state_file before calling.
    """
    if not state_file.exists():
        return {"phase": "unknown", "artifact": "none", "issues": []}
    text = state_file.read_text(encoding="utf-8")
    phase_m = _PHASE_RE.search(text)
    artifact_m = _ARTIFACT_RE.search(text)
    issues = [
        line.strip().lstrip("-# ")
        for line in text.splitlines()
        if re.search(r"(ARCH-|DEFECT-)\d+", line) and "PENDING" in line
    ]
    return {
        "phase": phase_m.group(1).strip().lower() if phase_m else "unknown",
        "artifact": artifact_m.group(1).strip() if artifact_m else "none",
        "issues": issues,
    }
```

**Key conventions:**
- `logging.getLogger(__name__)` — never `print()` in production paths
- Unquoted `Path | None` type annotations (Python 3.10+)
- `Path` objects throughout — never `str` for filesystem paths
- `encoding="utf-8"` explicit on all `read_text()` / `open()` calls
- Bare `except Exception:` **only** on per-item graceful degradation (per AC-05); always call `log.warning()` at top-level try/except
- All shared constants live in `helpers/bmad_status_core.py`, imported by extension + API + CLI
- No dead imports

### Bash — canonical style

```bash
#!/bin/bash
set -euo pipefail

PROJECT_PATH="${1:-$(pwd)}"
A0PROJ="$PROJECT_PATH/.a0proj"
PROJECT_NAME=$(basename "$PROJECT_PATH")

# All paths derived from computed vars — NEVER hardcode /a0/usr/projects/
cat > "$A0PROJ/instructions/01-bmad-config.md" << CONFIG
| \`{project-root}\`          | \`$A0PROJ/\` |
| \`{planning_artifacts}\`   | \`$A0PROJ/_bmad-output/planning-artifacts/\` |
CONFIG

# Warnings always to stderr
echo "Warning: seed-knowledge not found" >&2

# Idempotent copy via rsync (portable) or cp -Rn fallback
if command -v rsync >/dev/null 2>&1; then
    rsync -a --ignore-existing "$SEED_DIR/" "$A0PROJ/knowledge/main/"
else
    cp -Rn "$SEED_DIR/." "$A0PROJ/knowledge/main/" 2>/dev/null || true
fi
```

### SKILL.md frontmatter — established format

```yaml
---
name: "bmad-dev-story"
description: "Create a developer story for the next sprint. Use when: dev story, next story, implement story."
version: "1.0.0"
author: "BMAD"
tags: ["bmad", "bmm", "phase-4", "implementation"]
trigger_patterns:
  - "dev story"
  - "developer story"
  - "next story"
  - "/bmad dev-story"
bmad:
  module: "bmm"
  phase: "4-implementation"
  menu-code: "DS"
  agent: "bmad-dev"
  required: false
  output-location: "{implementation_artifacts}"
  outputs: "story-*.md"
---
```

### Alpine.js / WebUI

- `x-text` for all dynamic content (never `x-html` — XSS)
- Store-gating: `<template x-if="$store.bmadDashboard">` before any store access
- `@click` directives for event handling (no inline `onclick`)
- All API-derived values treated as untrusted (escaped via `x-text`)

---

## Testing Strategy

**Framework:** `pytest` (Python 3.10+)

**Locations:**

| File | Covers |
|---|---|
| `tests/test_extension_80.py` | Routing extension helpers |
| `tests/test_bmad_status_core.py` | `read_state()`, `_parse_alias_map()`, `AGENT_NAMES`, `PHASE_ACTIONS`, `PHASE_BUCKET_PREFIXES` |
| `tests/test_bmad_init_sh.py` | `bmad-init.sh` on `/tmp/test-*` dirs — idempotency, path correctness |
| `tests/test_core_csv_schema.py` | CSV column schema validation |
| `tests/test_c*_triggers.py` (4 files) | trigger_patterns presence per module |
| `tests/test_d*.py` (9 files) | Phase D: shared fragment, includes, table removal, caching, party mode |
| + 16 more | Dead code, constants, dashboard, routing vars, etc. |

**Coverage targets:**
- `helpers/bmad_status_core.py` — 100% (pure functions)
- `extensions/.../_80_bmad_routing_manifest.py` pure helpers — ≥ 80%
- `api/_bmad_status.py` — integration test per response key
- `skills/bmad-init/scripts/bmad-init.sh` — smoke test via subprocess

**CI gate:**
```bash
python -m pytest tests/ -v --tb=short          # all green (200+ tests)
tidy -e webui/bmad-dashboard.html 2>&1 | grep -c "^Error" | grep -q "^0$"  # zero HTML errors
bash -n skills/bmad-init/scripts/bmad-init.sh  # bash syntax
```

**Test naming convention:**
```python
def test_read_state_phase_with_dash_prefix():   # test_<func>_<scenario>
def test_read_state_no_file_returns_unknown():
def test_init_sh_paths_not_hardcoded():
```

---

## Boundaries

### Always Do
- Run `python -m pytest tests/ -v` before any commit
- Preserve all 20 BMAD agent profiles and their prompt files
- Use `$A0PROJ` (computed from `$PROJECT_PATH`) for all paths in init scripts — never hardcode `/a0/usr/projects/`
- Import `helpers.api`, `helpers.projects`, `helpers.extension` from A0 core — never re-implement
- Use `logging.getLogger(__name__)` for errors in extension hooks — no bare `pass` at top-level
- Keep SPEC.md updated before implementing spec changes
- Work on `develop` branch; merge to `main` only on confirmed `/ship`
- Verify tests pass on VPS testing instance before merge
- **When syncing upstream content:** Preserve all A0-specific additions (YAML frontmatter, Step Complete sections, trigger_patterns, `bmad:` blocks in SKILL.md)
- **When merging upstream diffs:** Read our file fully first, identify A0-only sections, merge upstream content around them

### Ask First
- Any change to `02-bmad-state.md` field names or format (breaks existing initialized projects)
- Any change to routing manifest `extras_temporary` key names (`bmad_routing_manifest`, `bmad_paths`, `bmad_not_initialized`) — these are the bmad-master prompt surface
- Adding Python dependencies (must not require `pip install` beyond A0's own venv)
- Removing any `module-help.csv` file before Phase C SKILL.md frontmatter migration is complete for that module
- Changing `bmad-init.sh` output file format or instruction file names (backward-compat risk)
- Any change to the VPS testing instance outside the plugin folder
- Removing the static 19-agent table from bmad-master/role.md before confirming `{{agent_profiles}}` delivers BMAD profiles
- **Adding the `bmad-customize` skill** — upstream-only feature that may need A0 adaptation

### Never Do
- Modify A0 core files (`/a0/agent.py`, core `/a0/helpers/*.py`, `/a0/prompts/`, core `/a0/extensions/`)
- Commit `.kilo/`, `.cursor/`, `.claude/`, `.windsurf/` AI-tool scratch directories
- Commit credentials, API keys, or SSH key material
- Use bare `except Exception: pass` at a top-level scope — always `log.warning()` at minimum
- Reduce the 20-agent BMAD persona surface (no agent removal or profile deletion)
- Hard-code the string `/a0/usr/projects/` in any new code
- Use `x-html` in Alpine templates (XSS risk)
- Fabricate CHANGELOG entries for changes not in the diff (PR #5 class mistake)
- **Overwrite A0-specific additions** (Step Complete sections, YAML frontmatter, trigger_patterns) when merging upstream content
- **Delete our plugin-specific sections** without explicit confirmation they're no longer needed

---

## Migration Phases

### Phase A — Critical Bug Fixes ✅ COMPLETE
**Effort:** ~6–8 hours | **Delivered:** v1.0.8  
**7 tasks:** C1 (hardcoded paths), C2+I3+N1+N3 (shared `read_state()`), C3 (mtime fallback), C4 (HTML fix), I1 (log warning), I2 (None-guard), Tests  
*See [CHANGELOG § Phase A](CHANGELOG.md) for details.*

### Phase B — Structural Alignment ✅ COMPLETE
**Effort:** ~2–3 days | **Delivered:** v1.0.8  
**11 tasks:** per_project_config, promptinclude, trigger_patterns, dead code removal, bash hardening, constants consolidation, mtime caching, git setup, shell tests  
*See [CHANGELOG § Phase B](CHANGELOG.md) for details.*

### Phase C — Routing Consolidation ✅ COMPLETE
**Effort:** ~1 week | **Delivered:** v1.0.8  
**8 tasks:** CSV 13-col migration (all 5 files), trigger_patterns on 57 SKILL.md files, routing verification  
*See [CHANGELOG § Phase C](CHANGELOG.md) for details.*

### Phase D — UX Surface ✅ COMPLETE
**Effort:** ~3–5 days | **Delivered:** v1.0.8  
**9 tasks:** shared fragment (85 lines), 19 specifics.md updated, dynamic agent table, _recommend() caching, dashboard errors, project-context stub, party mode, plugin audit  
*See [CHANGELOG § Phase D](CHANGELOG.md) for details.*

---

### Phase F — Upstream v6.6.0 Sync
**Effort:** ~1–2 days | **Risk:** Low–Medium | **Prereq:** Phases A–D complete ✅  
**Upstream:** `88b9a1c` → `9debc16` (v6.6.0) | **Files changed upstream:** 37 (3422 insertions, 312 deletions)  
**Reference:** `docs/upstream-sync-report-6.6.0.md`

This phase syncs our plugin with upstream BMAD-METHOD v6.6.0. The upstream release improves epic design quality (file churn detection), architecture validation rigor (unchecked checklists with conditional status), and workflow completion hooks. A config migration moves `project_name` to the canonical location.

#### P0 — Critical Workflow Step Sync (3 files)

| ID | Task | File | Detail |
|---|---|---|---|
| F-P0-1 | Fix pre-checked architecture checklist | `skills/bmad-bmm/workflows/3-solutioning/create-architecture/steps/step-07-validation.md` | Change all checklist items from `[x]` to `[ ]` (unchecked); remove ✅ emoji from section headers; add 3-tier conditional status (READY FOR IMPLEMENTATION / READY WITH MINOR GAPS / NOT READY) with evaluation rules; **preserve our Step Complete section** |
| F-P0-2 | Add file churn detection to epic design | `skills/bmad-bmm/workflows/3-solutioning/create-epics-and-stories/steps/step-02-design-epics.md` | Add Implementation Efficiency principle (#6); rename Step A to "Assess Context and Identify Themes" with brownfield context assessment; update Step B to consider file overlap per epic; add new Step C: Review for File Overlap; add wrong/correct examples for file churn; **preserve our YAML frontmatter and Step Complete section** |
| F-P0-3 | Add file churn check + HALT + on_complete hook | `skills/bmad-bmm/workflows/3-solutioning/create-epics-and-stories/steps/step-04-final-validation.md` | Add File Churn Check subsection to Epic Structure Validation; add HALT instruction to Final Menu; add On Complete hook (`resolve_customization.py`); **preserve our Workflow Completion — State Write section** |

**Critical sync rules for P0 tasks:**
1. Read our file fully before any changes
2. Identify all A0-specific sections (YAML frontmatter, Step Complete, State Write)
3. Merge upstream content into the appropriate locations
4. Verify A0-specific sections remain intact after merge
5. Run `python -m pytest tests/ -v` to verify no regressions

#### P1 — Config Migration (HIGH)

| ID | Task | File | Detail |
|---|---|---|---|
| F-P1-1 | Move `project_name` to core config | `skills/bmad-init/core/config.yaml` | Add `project_name` field (moved from bmm config); update version header to `6.6.0` |
| F-P1-2 | Remove `project_name` from bmm config | `skills/bmad-bmm/config.yaml` | Remove `project_name` field; update version header to `6.6.0` |
| F-P1-3 | Update remaining config versions | `skills/bmad-cis/config.yaml`, `skills/bmad-tea/config.yaml`, `skills/bmad-bmb/config.yaml` | Update version headers to `6.6.0` if present |
| F-P1-4 | Verify CSV row coverage | All 5 `module-help.csv` files | Verify no CSV rows reference config fields that moved; ensure routing still works |

#### P2 — Nice to Have

| ID | Task | Detail |
|---|---|---|
| F-P2-1 | Evaluate `bmad-customize` skill | Upstream added `bmad-customize` core skill. Assess whether it applies to A0 (where customization uses SKILL.md frontmatter + `.promptinclude.md`), or if it should be adapted/skipped |
| F-P2-2 | Update CHANGELOG | Add Phase F entries to CHANGELOG.md |
| F-P2-3 | Plugin version bump | Bump `plugin.yaml` version to `1.1.0` (feature addition from upstream sync) |

#### Phase F acceptance criteria:

**P0 (merge gate):**
- [ ] `step-07-validation.md` checklist items are all `[ ]` (unchecked), section headers have no ✅ emoji, Overall Status has 3-tier conditional logic
- [ ] `step-02-design-epics.md` has 6 principles (including #6 Implementation Efficiency), Step C (File Overlap Review) exists, wrong/correct file churn examples present
- [ ] `step-04-final-validation.md` has File Churn Check in validation, HALT instruction in Final Menu, On Complete hook section
- [ ] All 3 files retain their YAML frontmatter and Step Complete sections (A0-specific)
- [ ] `python -m pytest tests/ -v` → all 200+ tests green (no regressions)

**P1:**
- [ ] `skills/bmad-init/core/config.yaml` has `project_name` field
- [ ] `skills/bmad-bmm/config.yaml` no longer has `project_name` field
- [ ] All config.yaml files have version `6.6.0` in headers
- [ ] Routing manifest still reads CSV correctly after config migration

**P2:**
- [ ] `bmad-customize` evaluation documented (adopt / adapt / skip with rationale)
- [ ] CHANGELOG.md has Phase F entries
- [ ] `plugin.yaml` version is `1.1.0`

---

## Success Criteria (Phase F — Upstream v6.6.0 Sync)

**P0 (merge gate — no P1/P2 work until these pass):**
- [ ] All 3 critical workflow steps match upstream v6.6.0 content
- [ ] No A0-specific sections lost during sync (YAML frontmatter, Step Complete, State Write)
- [ ] All 200+ existing tests pass without modification

**P1 (config migration):**
- [ ] `project_name` lives in core config only (not duplicated in bmm)
- [ ] All config.yaml version headers read `6.6.0`
- [ ] CSV row routing unaffected by config migration

**P2 (polish):**
- [ ] `bmad-customize` evaluation documented
- [ ] CHANGELOG updated
- [ ] Plugin version `1.1.0`

**Overall (pre-`main` merge):**
- [ ] All 20 BMAD agents functional end-to-end on VPS testing instance
- [ ] BMAD initializable from workdir, `/a0/usr/projects/`, `/tmp/`, any arbitrary path
- [ ] Tagged as `v1.1.0`; merged to `main`

---

## Open Questions

1. ~~**VPS mapping type**~~ ✅ **RESOLVED** — `/home/debian/agent-zero/testing` is Docker volume-mounted to `/a0` (the dev container). Symlink established on VPS host: `testing/usr/plugins/bmad_method → development/usr/projects/a0_bmad_method`. Changes in `/a0/usr/projects/a0_bmad_method` are instantly live on the testing instance. `git push develop` is the record.

2. ~~**`{{agent_profiles}}` covers BMAD profiles?**~~ ✅ **RESOLVED** — `agent.system.tool.call_sub.py` calls `subagents.get_available_agents_dict(project)` which walks all `agents/*/` dirs including from plugins. All 20 BMAD profiles are auto-included. Phase D static table removal is safe to proceed.

3. ~~**CSV vs SKILL.md routing**~~ ✅ **RESOLVED** — `module-help.csv` is upstream BMAD-METHOD's canonical routing mechanism (confirmed in `bmad-code-org/BMAD-METHOD` source). Upstream SKILL.md carries only `name`+`description`. Phase C revised: keep CSV as routing source, add `trigger_patterns` to SKILL.md for A0 discoverability only.

4. ~~**`bmad.methodology.shared.md` exact scope**~~ ✅ **RESOLVED** — Phase D audit identified 7 shared sections; extracted to `agents/_shared/prompts/bmad-agent-shared.md` (85 lines). BMB/CIS agents use role-specific sections alongside shared fragment.

5. ~~**Party Mode requirements**~~ ✅ **RESOLVED** — Phase D delivered solo party mode with 8 ACs (AC-PM-01–08). Divergence from upstream documented: no subagent spawning, no `--model` flag.

6. ~~**`02-bmad-state.md` backward compat**~~ ✅ **RESOLVED** — Phase C kept existing format; `read_state()` handles all variants. No YAML migration needed.

7. ~~**`resolve_customization.py` in On Complete hook**~~ ✅ **RESOLVED** — Upstream script exists at `src/scripts/resolve_customization.py` (Python 3.11+, we have 3.13 ✅). Decision: **INCLUDE** in our plugin, adapting paths to A0 conventions (`$A0PROJ/_bmad/scripts/`). The script does 3-layer TOML merge for skill customization. Added as new task F-P1-5.

8. ~~**`bmad-customize` skill applicability**~~ ✅ **RESOLVED** — Decision: **CREATE** the skill. Port upstream `bmad-customize` core skill with A0 adaptations. Includes SKILL.md, `scripts/list_customizable_skills.py`, and porting `customize.toml` files from bmm skills. Upgraded from P2 evaluation to P1 creation task F-P1-6.

9. ~~**CSV row coverage post-config-migration**~~ ✅ **RESOLVED** — Verified: no CSV rows reference `project_name` at all. Config migration is safe with zero CSV changes needed. F-P1-4 reduced to a quick sanity check (no longer a blocker).
