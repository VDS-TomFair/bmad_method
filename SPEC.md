# Spec: BMAD Method Plugin — Phase G: Agent Prompt Fixes (v1.3)

**Date:** 2026-05-01  
**Status:** Draft — pending user approval  
**Branch:** `develop` (merge to `main` on `/ship`)  
**Scope:** Phase G (agent prompt fixes) — Phases A–F ✅ COMPLETE  
**Grounding:** `docs/workflow-builder-failure-analysis.md` — empirical VPS verification + A0 framework source

---

## Objective

Fix critical agent prompt defects discovered during bmad-workflow-builder failure analysis. The analysis revealed **two systemic failure layers** affecting all 20 BMAD agents: a broken `{{ include }}` mechanism (silently failing for 19/20 agents) and conflicting behavioral directives that bias agents toward shortcutting process steps.

**Prior work (COMPLETE):** Phases A–F delivered 250+ tests, 50+ commits — full A0 alignment, upstream v6.6.0 sync, config migration. See [CHANGELOG.md](CHANGELOG.md) for details.

**This phase targets:**

- **P0 (Critical):** Fix broken include (RC0), add process compliance gate (R1), rewrite shared fragment (R2), rewrite solving.md (R3)
- **P1 (High):** Add subordinate-mode detection (R4), create shared solving.md fragment (R5)
- **P2 (Nice to have):** Add A0 framework skill awareness (R6)

**Target user:** Individual developer using Agent Zero for personal software projects. BMAD is **project-scoped** — each project gets independent BMAD state, initialization, and knowledge. BMAD must work in any A0 project (`.a0proj/` present) or A0 workdir. Not limited to `/a0/usr/projects/`.

**What success looks like:**
- All 19 non-master agents successfully load shared behavioral fragment (85 lines)
- No conflicting directives between A0 framework defaults and BMAD process requirements
- Process compliance enforced at multiple layers (role.md, shared fragment, solving.md)
- Failure probability drops from 95-100% → <5%
- All 250+ existing tests continue to pass
- ADR 0002 revised to reflect actual state

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
| VCS | Git | `develop` branch → `main` on `/ship` |
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
│   ├── _shared/                         ← ⚠️ Phase G: REMOVE prompts/ dir after migration
│   │   └── prompts/
│   │       └── bmad-agent-shared.md     ← ⚠️ Phase G G-P0-1: MOVE to prompts/
│   ├── bmad-master/
│   │   └── prompts/
│   │       ├── agent.system.main.role.md      ← Phase G G-P0-2: add process compliance gate
│       │       ├── agent.system.main.specifics.md ← Phase G G-P0-5: convert from 109-line inline to {{ include }}
│   │       └── ...
│   └── bmad-pm/ ... (19 more — Phase G fixes apply to all)
│
├── skills/
│   ├── bmad-init/
│   │   ├── SKILL.md                    ← ✅ DONE: trigger_patterns added
│   │   ├── module-help.csv             ← ✅ DONE: upstream 13-col schema
│   │   ├── core/
│   │   │   └── config.yaml             ← ✅ DONE: project_name added, version 6.6.0
│   │   └── scripts/
│   │       ├── bmad-init.sh            ← ✅ DONE: $A0PROJ paths, set -euo pipefail
│   │       └── bmad-status.py          ← ✅ DONE: importlib, BMAD_DEV_MODE gate
│   ├── bmad-bmm/
│   │   ├── config.yaml                 ← ✅ DONE: project_name removed, version 6.6.0
│   │   ├── module-help.csv             ← ✅ DONE: upstream 13-col schema
│   │   └── workflows/                  ← ✅ DONE: synced with upstream v6.6.0
│   ├── bmad-tea/                        ← ✅ DONE: trigger_patterns, CSV aligned
│   ├── bmad-cis/                        ← ✅ DONE: trigger_patterns, CSV aligned
│   ├── bmad-bmb/                        ← ✅ DONE: trigger_patterns, CSV aligned
│   └── bmad-customize/                  ← ✅ DONE: ported from upstream
│
├── webui/
│   ├── bmad-dashboard.html             ← ✅ DONE: HTML fixed
│   └── bmad-dashboard-store.js         ← ✅ DONE: orphan removed
│
├── prompts/                            ← Phase G: primary target for shared fragment
│   ├── bmad.methodology.shared.md      ← existing shared fragment (Phase D)
│   └── bmad-agent-shared.md            ← Phase G G-P0-1: NEW LOCATION (moved from agents/_shared/)
│
├── tests/                              ← 250+ tests ✅
│   ├── test_extension_80.py            ← routing extension tests
│   ├── test_bmad_status_core.py        ← read_state() variants
│   ├── test_bmad_init_sh.py            ← shell integration tests
│   ├── test_phase_g_include.py         ← Phase G: runtime include resolution test
│   ├── test_phase_g_compliance.py      ← Phase G: process compliance prompt content test
│   └── ... (27+ more test files)
│
├── docs/
│   ├── workflow-builder-failure-analysis.md  ← Phase G source of truth
│   ├── upstream-sync-report-6.6.0.md        ← Phase F source of truth
│   ├── alignment-analysis.md
│   ├── document-lifecycle.md
│   └── adr/                            ← 7 architecture decision records
│       ├── 0002-shared-fragments-include.md  ← Phase G: REVISE (include was never working)
│       └── ...
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
        "artifact": artifact_m.group(1).strip().lower() if artifact_m else "none",
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
| `tests/test_phase_g_include.py` | **Phase G NEW:** runtime include resolution for all 19 agents |
| `tests/test_phase_g_compliance.py` | **Phase G NEW:** process compliance prompt content verification |
| + 20+ more | Dead code, constants, dashboard, routing vars, etc. |

**Coverage targets:**
- `helpers/bmad_status_core.py` — 100% (pure functions)
- `extensions/.../_80_bmad_routing_manifest.py` pure helpers — ≥ 80%
- `api/_bmad_status.py` — integration test per response key
- `skills/bmad-init/scripts/bmad-init.sh` — smoke test via subprocess

**CI gate:**
```bash
python -m pytest tests/ -v --tb=short          # all green (250+ tests)
tidy -e webui/bmad-dashboard.html 2>&1 | grep -c "^Error" | grep -q "^0$"  # zero HTML errors
bash -n skills/bmad-init/scripts/bmad-init.sh  # bash syntax
```

**Test naming convention:**
```python
def test_read_state_phase_with_dash_prefix():   # test_<func>_<scenario>
def test_read_state_no_file_returns_unknown():
def test_init_sh_paths_not_hardcoded():
```

### Test Coverage Gaps (from Failure Analysis)

The existing test suite (250+ tests) covers structural/content validation but has critical gaps:

| Gap | Severity | Would Have Caught |
|---|---|---|
| **Runtime include resolution** | CRITICAL | RC0 — broken `{{ include }}` for 19 agents |
| **Process compliance prompts** | HIGH | RC5 — missing compliance gate in role.md |
| **Subordinate delegation behavior** | HIGH | RC4 — no subordinate-mode awareness |

**Phase G adds:**
- `test_phase_g_include.py` — integration test verifying `{{ include "bmad-agent-shared.md" }}` resolves for all 19 non-master agents via A0's `find_file_in_dirs()`
- `test_phase_g_compliance.py` — content test verifying process compliance gate present in all 20 agent role.md files

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
- **Process compliance:** All BMAD agent prompts MUST enforce step-by-step workflow execution — no shortcuts
- **Include verification:** After any `{{ include }}` directive change, verify resolution on VPS with test script
- **Prompt changes:** Test prompt content with content-based assertions (not just file existence)

### Ask First
- Any change to `02-bmad-state.md` field names or format (breaks existing initialized projects)
- Any change to routing manifest `extras_temporary` key names (`bmad_routing_manifest`, `bmad_paths`, `bmad_not_initialized`) — these are the bmad-master prompt surface
- Adding Python dependencies (must not require `pip install` beyond A0's own venv)
- Removing any `module-help.csv` file before Phase C SKILL.md frontmatter migration is complete for that module
- Changing `bmad-init.sh` output file format or instruction file names (backward-compat risk)
- Any change to the VPS testing instance outside the plugin folder
- Removing the static 19-agent table from bmad-master/role.md before confirming `{{agent_profiles}}` delivers BMAD profiles
- **Adding the `bmad-customize` skill** — upstream-only feature that may need A0 adaptation
- **Moving shared prompt files** — must verify `{{ include }}` resolution after any path change
- **Changing solving.md** — the conflict between A0 defaults and BMAD overrides is sensitive

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
- **Assume `{{ include }}` works** — always verify resolution after path changes
- **Allow "complete task" to override process compliance** in agent prompts

---

## Root Cause Analysis

> **Full report:** `docs/workflow-builder-failure-analysis.md` (559 lines)

The bmad-workflow-builder agent (Wendy) was tasked with creating a Caveman skill. Instead of following the BMAD 11-step workflow, Wendy skipped all steps and wrote a monolithic SKILL.md in a single shot. Investigation revealed this is **NOT a Wendy-specific issue** — all 20 BMAD agents share the same structural vulnerabilities.

### Six Root Causes

| ID | Root Cause | Severity | What |
|---|---|---|---|
| **RC0** | Broken `{{ include }}` resolution | **CRITICAL** — PRIMARY | `{{ include "bmad-agent-shared.md" }}` silently fails for all 19 non-master agents. File is in `agents/_shared/prompts/` which is NOT in A0's search path (`_shared` is not a profile name). `helpers/files.py:364` silently returns literal text on `FileNotFoundError`. All 19 agents missing 85 lines of behavioral instructions. Empirically verified on VPS. |
| **RC1** | Conflicting directives in solving.md | **CRITICAL** | Line 25 (`don't accept failure retry be high-agency`) vs Line 33 (`Follow workflow steps precisely`). LLM task-completion bias resolves toward shortcut. Full override (not `{{ extend }}`) — won't inherit framework updates. |
| **RC2** | Escape hatch in shared fragment | **HIGH** | `Initial Clarification` section in shared fragment allows agents to rationalize skipping steps if they believe requirements are clear. **Moot while RC0 exists** (section never loaded), but becomes active after include fix. |
| **RC3** | Step-file rules not in agent prompts | **HIGH** | Enforcement rules exist only inside skill files (loaded on demand). If agent rationalizes not loading skill, rules never enter context. Circular dependency. |
| **RC4** | No subordinate-mode awareness | **HIGH** | Menu-driven interaction breaks when called via `call_subordinate`. Agents have no alternative execution path for subordinate mode. |
| **RC5** | No process compliance gate | **HIGH** | None of the 20 agents contain a non-overridable process compliance directive. role.md focuses on OUTPUT quality, not PROCESS adherence. |

### Why bmad-master Is Unaffected

bmad-master has a 109-line `specifics.md` that **inlines the shared content directly** — it does NOT use `{{ include }}`. This is why bmad-master works correctly while all 19 specialist agents are broken.

### Failure Probability Assessment

| Scenario | Failure Probability | Rationale |
|---|---|---|
| **Current (broken include, no fixes)** | **95–100%** | Agents missing core behavioral instructions + conflicting directives = almost guaranteed shortcut |
| **After R0 (include fixed only)** | **60–80%** | Shared instructions present but escape hatch + conflict still exist |
| **After R0 + R1–R3 (process compliance)** | **5–15%** | Multiple enforcement layers, conflict removed |
| **After all fixes (R0–R6)** | **<5%** | Defense in depth across all layers |

---

## Recommendations

Ten recommendations (R0–R9), priority-ordered. **All are prompt text changes — no code changes needed.**

| Priority | Fix | Root Cause | Effort | Scope |
|---|---|---|---|---|
| **P0** | R0: Fix include (move to `prompts/`) | RC0 | Low | 1 file move |
| **P0** | R1: Process compliance gate in role.md | RC5 | Low | 20 files |
| **P0** | R2: Rewrite shared fragment | RC2 | Low | 1 file |
| **P0** | R3: Rewrite solving.md (clean full override) | RC1 | Low | 20 files (or 1 shared) |
| **P0** | R7: bmad-master inline → include | RC0+divergence | Low | 1 file |
| **P1** | R4: Subordinate-mode detection | RC4 | Low | 20 files |
| **P1** | R5: Shared solving.md fragment | Maintenance | Medium | 1 new file |
| **P1** | R8: Verify bmad-master response include | Quality | Low | 1 verification |
| **P2** | R6: A0 skill awareness | Quality | Low | 3 files (BMB) |
| **P2** | R9: Update failure analysis report | Documentation | Low | 1 file |

**Total estimated effort:** ~3–4 hours for P0 fixes.

### Gap Analysis (Post-Investigation)

Three additional issues discovered during comprehensive plugin grep:

| # | Issue | Severity | Why |
|---|---|---|---|
| I1 | bmad-master inlines 109 lines of shared content — will diverge from rewritten shared fragment | HIGH | After R0+R2, 19 agents get new process-aware shared content, but master keeps stale inline with escape hatch |
| I2 | bmad-master has same solving.md conflict (high-agency vs follow steps) | HIGH | Master is covered by R3 scope ("all 20") but worth confirming |
| I3 | bmad-master response.md include (`agent.system.response_tool_tips.md`) unverified | MEDIUM | References framework file, should work, but no empirical proof |
| I4 | Failure analysis report outdated — references `{{ include original }}` | LOW | Report should match clean full override decision (R3) |

### R0: Fix the Broken Include (P0 — MUST DO FIRST)

Move `bmad-agent-shared.md` to a directory that IS in the search path:

```
# Current (broken):
agents/_shared/prompts/bmad-agent-shared.md

# Fixed:
prompts/bmad-agent-shared.md
```

The plugin root `prompts/` directory IS in A0's search chain (priority level 7). All `{{ include }}` directives will resolve correctly.

**Steps:**
1. Move `agents/_shared/prompts/bmad-agent-shared.md` → `prompts/bmad-agent-shared.md`
2. Remove empty `agents/_shared/prompts/` directory
3. Verify on VPS with A0 framework Python test script
4. Update ADR 0002 (include was never working)
5. Run existing test suite (250+ tests)

### R1: Add Process Compliance Gate to role.md (P0)

Add to EVERY BMAD agent's `role.md`, BEFORE the persona definition:

```markdown
## MANDATORY PROCESS COMPLIANCE

You are a PROCESS-DRIVEN agent. This means:

1. You MUST load the appropriate BMAD skill before ANY workflow execution
2. You MUST follow the step-file architecture loaded from the skill
3. You MUST execute steps sequentially — NEVER skip or optimize the sequence
4. You MUST read each step file completely before taking action
5. You MUST halt at checkpoints and wait for user input
6. You MUST NOT produce workflow artifacts except through the step-by-step process

Even if you believe you have all requirements, you MUST still follow the step-by-step process.
"Complete task" means complete the PROCESS, not skip to the output.
```

**Apply to:** All 20 BMAD agents.

### R2: Rewrite bmad-agent-shared.md Initial Clarification (P0)

Replace the escape hatch with process-aware clarification:

```markdown
## Initial Clarification

Before executing any BMAD workflow, confirm understanding of:
- What artifact is being created or modified
- Current project phase alignment
- Output format expectations
- Acceptance criteria
- Constraints to honor

Clarification determines WHICH workflow step to START at, not WHETHER to follow the process.
You ALWAYS follow the step-by-step process — clarification only affects where you begin.

NEVER interpret "I have all requirements" as permission to skip the process.
```

**Apply to:** The shared fragment (one change fixes all 19 agents).

### R3: Rewrite solving.md to Remove Conflict (P0)

Replace the conflicting full override with a **clean BMAD-specific solving.md** (no `{{ include original }}`):

```markdown
## Problem solving

You are a PROCESS-DRIVEN BMAD agent. Process compliance overrides efficiency.

0. Load the appropriate BMAD skill FIRST — no exceptions
1. Follow the step-file architecture loaded from the skill
2. Execute steps sequentially — never skip or optimize the sequence
3. Read each step file completely before taking action
4. Halt at checkpoints and wait for user input
5. Produce artifacts only through the step-by-step process
6. Use `text_editor:patch` for large artifacts
7. Update `02-bmad-state.md` after phase transitions

CRITICAL: "Complete task" means complete the PROCESS, not skip to the output.
If you feel tension between completing the task and following the process,
FOLLOW THE PROCESS.
```

**Why clean full override instead of `{{ include original }}`:** BMAD agents need fundamentally different problem-solving behavior (process-driven vs task-driven). The A0 default solving.md contains `"don't accept failure retry be high-agency"` which directly conflicts with BMAD's process requirements. Inheriting and overriding would carry the conflict — a clean override eliminates it entirely.

**Apply to:** All 20 BMAD agents (create shared fragment to avoid 20-file copy — see R5).

### R4: Add Subordinate-Mode Detection (P1)

Add to `communication_additions.md`:

```markdown
## Subordinate Mode Detection

When you receive a direct task instruction (not a menu selection from the user),
you are in SUBORDINATE MODE:

1. Recognize you are being called by a superior agent
2. Load the appropriate BMAD skill IMMEDIATELY
3. Route to the matching workflow based on the task
4. Execute the workflow step-by-step — do NOT skip the process
5. Return results via the `response` tool when complete

Do NOT display the menu in subordinate mode — proceed directly to workflow execution.
```

**Apply to:** All 20 BMAD agents.

### R5: Create Shared solving.md Fragment (P1)

Since all 20 agents share identical solving.md content:

```markdown
{{ include "bmad-agent-shared-solving.md" }}
```

Place `bmad-agent-shared-solving.md` in the same `prompts/` directory as the shared fragment (from R0). This eliminates copy-paste across 20 files.

### R6: Add A0 Framework Skill Awareness (P2)

Add to specifics.md:

```markdown
## A0 Framework Integration

When building workflows that interact with Agent Zero:
- Load `a0-development` skill to understand framework architecture
- Reference A0 tool patterns and conventions
- Use `call_subordinate` to delegate specialist work
- Follow A0 prompt inheritance and override patterns
```

**Apply to:** BMB agents primarily (Wendy, Bond, Morgan).

### R7: Convert bmad-master Inline to Include (P0)

bmad-master's `specifics.md` is 109 lines because it inlines all shared content directly — it does NOT use `{{ include }}`. This was the right call when the include was broken (RC0), but creates a divergence risk after R0+R2.

**Problem:** After R0+R2, 19 agents get new process-aware shared content via the rewritten `bmad-agent-shared.md`, but bmad-master keeps its stale 109-line inline version that still contains the escape hatch. The two copies will silently diverge.

**Fix:**
1. Extract master-specific content from the 109-line `specifics.md`
2. Replace with: persona preamble + `{{ include "bmad-agent-shared.md" }}` + master-specific extras
3. Verify on VPS that include resolves correctly for bmad-master

**Apply to:** `agents/bmad-master/prompts/agent.system.main.specifics.md` (1 file).

### R8: Verify bmad-master Response Include (P1)

bmad-master has `{{ include "agent.system.response_tool_tips.md" }}` in its `response.md`. This references the A0 framework file at `/a0/prompts/agent.system.response_tool_tips.md`. It should work (framework files are in the search path), but this has never been empirically verified.

**Action:** Run verification script on VPS testing instance to confirm the include resolves correctly in bmad-master's context.

**Apply to:** Verification only — no file changes expected.

### R9: Update Failure Analysis Report (P2)

`docs/workflow-builder-failure-analysis.md` still references the old `{{ include original }}` approach in its recommendations. The decision was made to use a clean full override instead (R3). The report should be updated to reflect the actual implementation.

**Action:** Update failure analysis report to reflect clean full override decision.

**Apply to:** `docs/workflow-builder-failure-analysis.md` (1 file).

---

## Migration Phases

### Phase A — Critical Bug Fixes ✅ COMPLETE
**Effort:** ~6–8 hours | **Delivered:** v1.0.8  
7 tasks: hardcoded paths, shared read_state(), mtime fallback, HTML fix, logging, None-guard, dead code.  *See [CHANGELOG § Phase A](CHANGELOG.md).*

### Phase B — Structural Alignment ✅ COMPLETE
**Effort:** ~2–3 days | **Delivered:** v1.0.8  
11 tasks: per_project_config, promptinclude, trigger_patterns, dead code removal, bash hardening, constants consolidation, mtime caching, git setup, shell tests.  *See [CHANGELOG § Phase B](CHANGELOG.md).*

### Phase C — Routing Consolidation ✅ COMPLETE
**Effort:** ~1 week | **Delivered:** v1.0.8  
8 tasks: CSV 13-col migration (all 5 files), trigger_patterns on 57 SKILL.md files, routing verification.  *See [CHANGELOG § Phase C](CHANGELOG.md).*

### Phase D — UX Surface ✅ COMPLETE
**Effort:** ~3–5 days | **Delivered:** v1.0.8  
9 tasks: shared fragment (85 lines), 19 specifics.md updated, dynamic agent table, _recommend() caching, dashboard errors, project-context stub, party mode, plugin audit.  *See [CHANGELOG § Phase D](CHANGELOG.md).*

### Phase F — Upstream v6.6.0 Sync ✅ COMPLETE
**Effort:** ~1–2 days | **Delivered:** v1.2.0  
P0: 3 workflow steps synced (architecture checklist, epic file churn, final validation hook). P1: config migration, bmad-customize skill ported. P2: CHANGELOG, version bump.  *See [CHANGELOG § Phase F](CHANGELOG.md).*

---

### Phase G — Agent Prompt Fixes
**Effort:** ~3–4 hours for P0 fixes | **Risk:** Low (prompt text only) | **Prereq:** Phases A–F complete ✅  
**Reference:** `docs/workflow-builder-failure-analysis.md`  
**ADR:** 0002 (revision required — include was never working)

This phase fixes critical agent prompt defects discovered during failure analysis. All changes are prompt text only — no code changes needed.

#### P0 — Critical Fixes (5 tasks)

| ID | Task | Root Cause | Detail |
|---|---|---|---|
| G-P0-1 | Fix broken `{{ include }}` | RC0 | Move `agents/_shared/prompts/bmad-agent-shared.md` → `prompts/bmad-agent-shared.md`. The plugin root `prompts/` directory IS in A0's search chain. Remove empty `agents/_shared/prompts/` after move. |
| G-P0-2 | Add process compliance gate | RC5 | Add `MANDATORY PROCESS COMPLIANCE` section to all 20 agents' `role.md`, BEFORE persona definition. See R1 for exact text. |
| G-P0-3 | Rewrite shared fragment clarification | RC2 | Replace escape hatch in `bmad-agent-shared.md` `Initial Clarification` section with process-aware clarification. See R2 for exact text. |
| G-P0-4 | Rewrite solving.md (clean full override) | RC1 | Replace conflicting full override in all 20 `solving.md` files with clean BMAD-specific solving.md. No `{{ include original }}` — eliminates conflict entirely. See R3 for exact text. |
| G-P0-5 | Convert bmad-master inline to include | RC0+divergence | After R0 verified, extract master-specific content from 109-line inline specifics.md, replace with `{{ include "bmad-agent-shared.md" }}` + persona extras. See R7. |

**Implementation order:** G-P0-1 FIRST (enables verification of all other changes), then G-P0-2 through G-P0-4 in any order.

**Critical verification for G-P0-1:**
1. After move, verify on VPS: A0 framework Python must find `bmad-agent-shared.md` via `find_file_in_dirs()`
2. Test `{{ include "bmad-agent-shared.md" }}` resolves in all 19 non-master agents
3. Run `python -m pytest tests/ -v` — all 250+ tests green
4. Update ADR 0002 status to "Revised" with corrected claims

#### P1 — High Priority (3 tasks)

| ID | Task | Root Cause | Detail |
|---|---|---|---|
| G-P1-1 | Add subordinate-mode detection | RC4 | Add `Subordinate Mode Detection` section to all 20 agents' `communication_additions.md`. See R4 for exact text. |
| G-P1-2 | Create shared solving.md fragment | Maintenance | Extract common solving.md content to `prompts/bmad-agent-shared-solving.md` and replace 20 `solving.md` files with `{{ include "bmad-agent-shared-solving.md" }}`. Depends on G-P0-4. |
| G-P1-3 | Verify bmad-master response include | Quality | Verify `{{ include "agent.system.response_tool_tips.md" }}` resolves in bmad-master response.md on VPS. See R8. |

#### P2 — Nice to Have (2 tasks)

| ID | Task | Detail |
|---|---|---|
| G-P2-1 | Add A0 framework skill awareness | Add `A0 Framework Integration` section to BMB agent specifics.md (Wendy, Bond, Morgan). See R6 for exact text. |
| G-P2-2 | Update failure analysis report | Update `docs/workflow-builder-failure-analysis.md` to reflect clean full override decision. See R9. |

#### Phase G acceptance criteria:

**P0 (merge gate — no P1/P2 work until these pass):**
- [ ] `bmad-agent-shared.md` moved to `prompts/` directory — `agents/_shared/prompts/` removed
- [ ] Runtime include resolution test passes for all 19 non-master agents on VPS
- [ ] All 20 `role.md` files contain `MANDATORY PROCESS COMPLIANCE` section before persona
- [ ] `bmad-agent-shared.md` Initial Clarification replaced with process-aware version (no escape hatch)
- [ ] All 20 `solving.md` files use clean BMAD-specific full override (no conflicting "high-agency" directive)
- [ ] ADR 0002 revised to reflect actual state (include was never working)
- [ ] `python -m pytest tests/ -v` → all 250+ tests green (no regressions)
- [ ] bmad-master specifics.md converted from 109-line inline to {{ include }} (no divergence)

**P1:**
- [ ] All 20 `communication_additions.md` files contain `Subordinate Mode Detection` section
- [ ] Shared solving.md fragment exists in `prompts/bmad-agent-shared-solving.md`
- [ ] All 20 `solving.md` files reduced to `{{ include "bmad-agent-shared-solving.md" }}`
- [ ] bmad-master response.md include verified resolving on VPS

**P2:**
- [ ] BMB agent specifics.md (Wendy, Bond, Morgan) contain `A0 Framework Integration` section
- [ ] Failure analysis report updated to reflect clean full override

---

## Success Criteria

### Phase G — Agent Prompt Fixes

**P0 (merge gate — no P1/P2 work until these pass):**
- [ ] Broken include fixed — shared fragment resolves for all 19 non-master agents
- [ ] Process compliance gate present in all 20 agent role.md files
- [ ] Shared fragment clarification is process-aware (no escape hatch)
- [ ] solving.md conflict resolved (clean BMAD-specific full override)
- [ ] ADR 0002 revised
- [ ] All 250+ existing tests pass without modification
- [ ] bmad-master specifics.md uses {{ include }} instead of 109-line inline (no divergence from shared fragment)

**P1:**
- [ ] Subordinate-mode detection present in all 20 agents
- [ ] Shared solving.md fragment eliminates 20-file copy
- [ ] bmad-master response.md include verified resolving on VPS

**P2:**
- [ ] BMB agents have A0 framework skill awareness
- [ ] Failure analysis report updated to reflect clean full override decision

**Overall (pre-`main` merge):**
- [ ] All 20 BMAD agents functional end-to-end on VPS testing instance
- [ ] Include resolution empirically verified on VPS for all 19 non-master agents
- [ ] BMAD initializable from workdir, `/a0/usr/projects/`, `/tmp/`, any arbitrary path
- [ ] Failure probability reduced from 95-100% → <15% (P0 only) or <5% (all fixes)

---

## Open Questions

1. ~~**VPS mapping type**~~ ✅ **RESOLVED** — `/home/debian/agent-zero/testing` is Docker volume-mounted to `/a0` (the dev container). Symlink established on VPS host: `testing/usr/plugins/bmad_method → development/usr/projects/a0_bmad_method`. Changes in `/a0/usr/projects/a0_bmad_method` are instantly live on the testing instance. `git push develop` is the record.

2. ~~**`{{agent_profiles}}` covers BMAD profiles?**~~ ✅ **RESOLVED** — `agent.system.tool.call_sub.py` calls `subagents.get_available_agents_dict(project)` which walks all `agents/*/` dirs including from plugins. All 20 BMAD profiles are auto-included.

3. ~~**CSV vs SKILL.md routing**~~ ✅ **RESOLVED** — `module-help.csv` is upstream BMAD-METHOD's canonical routing mechanism. Phase C revised: keep CSV as routing source, add `trigger_patterns` to SKILL.md for A0 discoverability only.

4. ~~**`bmad.methodology.shared.md` exact scope**~~ ✅ **RESOLVED** — Phase D audit identified 7 shared sections; extracted to `agents/_shared/prompts/bmad-agent-shared.md` (85 lines). **Phase G note:** Location was wrong — moved to `prompts/`.

5. ~~**Party Mode requirements**~~ ✅ **RESOLVED** — Phase D delivered solo party mode with 8 ACs. Divergence from upstream documented.

6. ~~**`02-bmad-state.md` backward compat**~~ ✅ **RESOLVED** — Phase C kept existing format; `read_state()` handles all variants.

7. ~~**`resolve_customization.py` in On Complete hook**~~ ✅ **RESOLVED** — Included in plugin, adapted paths to A0 conventions.

8. ~~**`bmad-customize` skill applicability**~~ ✅ **RESOLVED** — Created: ported upstream `bmad-customize` core skill with A0 adaptations.

9. ~~**CSV row coverage post-config-migration**~~ ✅ **RESOLVED** — No CSV rows reference `project_name`. Config migration safe.

10. **ADR 0002 revision** 🔄 **Phase G** — ADR 0002 falsely claims "Confirmed working via live A2A testing." The include silently fails. Must revise status, claims, and consequences. **Action:** Update as part of G-P0-1.

11. **Should `agents/_shared/` directory be removed entirely?** 🔄 **Phase G** — After moving shared fragment to `prompts/`, the `agents/_shared/` directory becomes empty. Decision: remove it ( `_shared` is not a valid A0 profile name, its existence is misleading).
