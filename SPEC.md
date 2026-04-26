# Spec: BMAD Method Plugin — Full A0 Alignment Migration (v1.1)

**Date:** 2026-04-26  
**Status:** Draft — pending user approval  
**Branch:** `develop` (merge to `main` on `/ship`)  
**Scope:** Phases A–D (full alignment migration)

---

## Objective

Migrate the BMAD Method A0 plugin from its current state (BMAD v5-flavored, partially-aligned, 4 Critical bugs) to a maximally A0-idiomatic implementation that:

- Fixes all 4 Critical and key Important/Suggestion bugs (Phase A)
- Aligns structural conventions with A0 native mechanisms (Phase B)
- Consolidates routing to SKILL.md frontmatter, eliminating `module-help.csv` redundancy (Phase C)
- Improves UX surface: dynamic agent table, shared methodology fragments, dashboard polish (Phase D)

**Target user:** Individual developer using Agent Zero for personal software projects. BMAD is **project-scoped** — each project gets independent BMAD state, initialization, and knowledge. BMAD must work in any A0 project (`.a0proj/` present) or A0 workdir. Not limited to `/a0/usr/projects/`.

**What success looks like:**
- `bmad init` works from any filesystem path (workdir, `/a0/usr/projects/`, `/tmp/`, `/home/user/`)
- Phase tracking is consistent: dashboard and routing always show the same phase
- Cross-project state leakage is eliminated
- Routing manifest extension is ≤ 100 lines (down from 424)
- All 20 BMAD agent personas remain fully functional throughout every phase
- Plugin passes `a0-review-plugin` audit with no Critical findings
- Dashboard renders without malformed HTML

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
├── plugin.yaml                          ← per_project_config: true (Phase B)
├── SPEC.md                              ← this file
├── CHANGELOG.md
├── README.md
├── .gitignore                           ← ✅ DONE: .kilo/ .cursor/ .claude/ .windsurf/ added
│
├── api/
│   └── _bmad_status.py                  ← I2: add None-guard on _spec (Phase A)
│                                           S3: _recommend() accept cached results (Phase B)
│
├── helpers/
│   ├── __init__.py
│   └── bmad_status_core.py              ← C2/I3/N1/N3: shared read_state() (Phase A)
│                                           I6/S6/S8: AGENT_NAMES, PHASE_ACTIONS, PHASE_BUCKET_PREFIXES (Phase B)
│
├── extensions/
│   ├── python/
│   │   └── message_loop_prompts_after/
│   │       └── _80_bmad_routing_manifest.py
│   │           Phase A: C3 fallback gate, I1 logging
│   │           Phase B: mtime caching, dead constant removal
│   │           Phase C: CSV column alignment to upstream format
│   └── webui/
│       └── sidebar-quick-actions-main-start/
│           └── _bmad_dashboard_btn.html
│
├── agents/                              ← 20 bmad-* profiles (idiomatic ✅ — keep structure)
│   ├── bmad-master/
│   │   └── prompts/
│   │       ├── agent.system.main.role.md      ← Phase D: remove static 19-agent table
│   │       ├── agent.system.main.specifics.md ← Phase D: include bmad.methodology.shared.md
│   │       └── ...
│   └── bmad-pm/ ... (19 more — same Phase D treatment for specifics.md)
│
├── skills/
│   ├── bmad-init/
│   │   ├── SKILL.md                    ← Phase B: add /bmad /bmad-init /bmad-help trigger_patterns
│   │   ├── module-help.csv             ← KEEP — upstream BMAD canonical routing
│   │   │                                 Phase C: align to upstream 13-column schema
│   │   └── scripts/
│   │       ├── bmad-init.sh            ← C1: use $A0PROJ paths, set -euo pipefail (Phase A)
│   │       ├── bmad-status.py          ← Phase B: use bmad_status_core constants
│   │       └── bmad_status_core.py     ← DELETED: moved to helpers/ (Phase A)
│   ├── bmad-bmm/
│   │   └── workflows/**/SKILL.md       ← Phase C: add bmad: frontmatter block
│   │   └── workflows/**/SKILL.md       ← Phase C: add trigger_patterns (slash-style, A0 discovery)
│   └── bmad-init/_config/
│       └── manifest.yaml               ← single source of truth for module registry
│
├── webui/
│   ├── bmad-dashboard.html             ← C4: fix malformed HTML (Phase A)
│   └── bmad-dashboard-store.js         ← I8: remove stale error field (Phase B)
│
├── prompts/                            ← NEW: Phase D
│   └── bmad.methodology.shared.md     ← shared fragment included by all 20 main.specifics.md
│
├── tests/
│   ├── test_extension_80.py            ← expand with read_state() variants, ctxid-missing path
│   ├── test_bmad_status_core.py        ← NEW Phase A: unit tests for shared helpers
│   └── test_bmad_init_sh.py            ← NEW Phase B: shell integration tests
│
└── docs/
    ├── SPEC.md (symlink)               ← or just reference from root
    ├── alignment-analysis.md
    └── document-lifecycle.md
```

---

## Code Style

### Python — canonical example (new helpers/bmad_status_core.py style)

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

### SKILL.md frontmatter — Phase C target format

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
| `tests/test_extension_80.py` | Routing extension helpers (expand with `read_state()` variants, ctxid-missing path, mtime caching) |
| `tests/test_bmad_status_core.py` | NEW Phase A: `read_state()`, `_parse_alias_map()`, `AGENT_NAMES`, `PHASE_ACTIONS`, `PHASE_BUCKET_PREFIXES` |
| `tests/test_bmad_status_api.py` | NEW Phase A: `BmadStatus.process()` integration — each response key with fixture project dir |
| `tests/test_bmad_init_sh.py` | NEW Phase B: `bmad-init.sh` on `/tmp/test-*` dirs — idempotency, path correctness, file contents |

**Coverage targets:**
- `helpers/bmad_status_core.py` — 100% (pure functions)
- `extensions/.../_80_bmad_routing_manifest.py` pure helpers — ≥ 80%
- `api/_bmad_status.py` — integration test per response key
- `skills/bmad-init/scripts/bmad-init.sh` — smoke test via subprocess

**CI gate (to add in Phase B):**
```bash
python -m pytest tests/ -v --tb=short          # all green
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

### Ask First
- Any change to `02-bmad-state.md` field names or format (breaks existing initialized projects)
- Any change to routing manifest `extras_temporary` key names (`bmad_routing_manifest`, `bmad_paths`, `bmad_not_initialized`) — these are the bmad-master prompt surface
- Adding Python dependencies (must not require `pip install` beyond A0's own venv)
- Removing any `module-help.csv` file before Phase C SKILL.md frontmatter migration is complete for that module
- Changing `bmad-init.sh` output file format or instruction file names (backward-compat risk)
- Any change to the VPS testing instance outside the plugin folder
- Removing the static 19-agent table from bmad-master/role.md (Phase D) before confirming `{{agent_profiles}}` delivers BMAD profiles

### Never Do
- Modify A0 core files (`/a0/agent.py`, core `/a0/helpers/*.py`, `/a0/prompts/`, core `/a0/extensions/`)
- Commit `.kilo/`, `.cursor/`, `.claude/`, `.windsurf/` AI-tool scratch directories
- Commit credentials, API keys, or SSH key material
- Use bare `except Exception: pass` at a top-level scope — always `log.warning()` at minimum
- Reduce the 20-agent BMAD persona surface (no agent removal or profile deletion)
- Hard-code the string `/a0/usr/projects/` in any new code
- Use `x-html` in Alpine templates (XSS risk)
- Fabricate CHANGELOG entries for changes not in the diff (PR #5 class mistake)

---

## Migration Phases

### Phase A — Critical Bug Fixes
**Effort:** ~6–8 hours | **Risk:** Low | **Gate:** Must pass before any other work

| ID | Task | File | Detail |
|---|---|---|---|
| C1 | Fix hardcoded path | `skills/bmad-init/scripts/bmad-init.sh:40-44` | Replace `$PROJECT_NAME` with `$A0PROJ`-derived vars; add `set -euo pipefail` |
| C2+I3+N1+N3 | Shared `read_state()` | `helpers/bmad_status_core.py` | `_PHASE_RE` + `_ARTIFACT_RE` anchored MULTILINE IGNORECASE; lowercase output; update routing ext + API to use it |
| C3 | Gate mtime fallback | `_80_bmad_routing_manifest.py`, `api/_bmad_status.py`, `scripts/bmad-status.py` | Remove production fallback; gate behind `BMAD_DEV_MODE` env var with `log.warning()` |
| C4 | Fix HTML structure | `webui/bmad-dashboard.html:255-263` | Delete 4 stray `</div>` and 1 stray `</template>`; verify with tidy |
| I1 | Log at outermost except | `_80_bmad_routing_manifest.py:423` | `log.warning(traceback.format_exc())` — do not re-raise |
| I2 | None-guard on `_spec` | `api/_bmad_status.py:11-14` | `if _spec is None: raise ImportError(...)` |
| Tests | Regression tests | `tests/test_bmad_status_core.py` (new) | `read_state()` with 6 format variants (dash/no-dash, extra whitespace, uppercase, narrative match, missing file) |

**Phase A acceptance criteria:**
- [ ] `bash skills/bmad-init/scripts/bmad-init.sh /tmp/test-dir` → `01-bmad-config.md` contains `/tmp/test-dir/.a0proj/`, NOT `/a0/usr/projects/`
- [ ] `tidy -e webui/bmad-dashboard.html` → zero errors
- [ ] `pytest tests/ -v` → all green, all `read_state()` variants pass
- [ ] Routing extension and `BmadStatus.process()` return identical `phase` value for same state file
- [ ] Any exception in `BmadRoutingManifest.execute()` produces a log warning, not silent swallow

---

### Phase B — Structural Alignment
**Effort:** ~2–3 days | **Risk:** Low | **Prereq:** Phase A complete

| Task | File | Detail |
|---|---|---|
| `per_project_config: true` | `plugin.yaml:23` | Enables per-project toggle UI |
| User prefs → promptinclude | `skills/bmad-init/scripts/bmad-init.sh` + new `.promptinclude.md` | Move user name/language/skill level from `01-bmad-config.md` to `bmad-user-prefs.promptinclude.md`; auto-injected by A0 `_16_promptinclude` |
| Slash-style trigger_patterns | `skills/bmad-init/SKILL.md` | Add `/bmad`, `/bmad-init`, `/bmad-help`, `/bmad-status` to trigger_patterns |
| Delete dead constant | `_80_bmad_routing_manifest.py:30-36` | Remove `SKILL_TO_MODULE` (unused) |
| Fix store JS orphan | `webui/bmad-dashboard-store.js:19` | Remove `this.error = ""` or reinstate error UI |
| Bash hardening | `bmad-init.sh:2` | `set -euo pipefail`; rsync fallback; warnings to stderr |
| Consolidate constants | `helpers/bmad_status_core.py` | `AGENT_NAMES`, `PHASE_ACTIONS`, `PHASE_BUCKET_PREFIXES` — single source; update all 3 consumers |
| Remove dead imports | `api/_bmad_status.py:2` | Delete `import re, json` |
| Mtime caching | `_80_bmad_routing_manifest.py` | `_alias_cache` keyed on `(path, mtime_ns)`; `_csv_cache` same; single glob per `execute()` |
| Gitignore | `.gitignore` | Add `.kilo/`, `.cursor/`, `.claude/`, `.windsurf/` |
| Git setup | repo | Create `develop` branch, push to remote; tag current state as `v1.0.8-pre-align` |
| VPS mapping | VPS | Confirm/establish git-based deploy from `develop` branch to `/home/debian/agent-zero/testing/usr/plugins/bmad_method` |
| Tests | `tests/test_bmad_init_sh.py` | Shell integration tests via subprocess |

---

### Phase C — CSV Alignment + A0 Discovery Layer
**Effort:** ~1 week | **Risk:** Medium | **Prereq:** Phase B complete

**Revised goal (upstream discovery):** `module-help.csv` is the **canonical BMAD routing mechanism** — used in upstream BMAD-METHOD too. It is NOT something we invented. Upstream SKILL.md only carries `name` + `description` frontmatter; all routing metadata lives in CSV.

For Agent Zero, the right two-layer model is:
- `module-help.csv` = **BMAD-native routing** (keep; align column names to upstream format)
- `SKILL.md` = **A0-native discovery** (minimal: `name`, `description`, `trigger_patterns` for `skills_tool:search`)
- Routing extension = reads CSV + A0 context → injects manifest into EXTRAS (keep; fix bugs, add caching)

| Task | Detail |
|---|---|
| Align CSV columns to upstream format | Upstream: `module,skill,display-name,menu-code,description,action,args,phase,after,before,required,output-location,outputs`. Our columns differ (e.g. `skill` column uses skill-codes vs agent names). Normalize. |
| Add `trigger_patterns` to all ~40 workflow SKILL.md | Slash-style triggers (`/bmad-dev-story`, `/bmad-create-prd`, etc.) for `skills_tool:search` discoverability. No routing fields — keep SKILL.md minimal. |
| Mtime caching on CSV + alias reads | `_alias_cache` + `_csv_cache` keyed on `(path, mtime_ns)`; single glob per `execute()`. Already listed in Phase B; if not done, do here. |
| Verify all ~40 workflows discoverable | `skills_tool:search` returns correct results on VPS testing instance for key workflow names. |
| Expand tests | CSV column normalization, trigger_patterns presence in SKILL.md, phase-filter correctness |

**Phase C acceptance criteria:**
- [ ] CSV columns match upstream `module-help.csv` schema (all 13 columns present)
- [ ] All ~40 workflow SKILL.md files have `trigger_patterns` with slash-style entries
- [ ] `skills_tool:search "dev story"` returns `bmad-dev-story` on VPS testing instance
- [ ] `skills_tool:search "create prd"` returns correct workflow
- [ ] Routing extension still reads CSV correctly after column normalization
- [ ] Caching: routing manifest built from cache on second call in same turn

---

### Phase D — UX Surface
**Effort:** ~3–5 days | **Risk:** Medium | **Prereq:** Phase C complete

| Task | File | Detail |
|---|---|---|
| Remove static 19-agent table from bmad-master | `agents/bmad-master/prompts/agent.system.main.role.md` | Replace with routing guidance prose; confirm `{{agent_profiles}}` delivers BMAD profiles first (open question #2) |
| Shared methodology fragment | `prompts/bmad.methodology.shared.md` (new) | Extract common Activation Protocol, Thinking Framework, Using BMAD Skills sections; include via `{{ include "bmad.methodology.shared.md" }}` in all 20 `main.specifics.md` |
| Fix `_recommend()` caching | `api/_bmad_status.py:152-178` | Accept pre-computed state/agents/skills/tests instead of recomputing |
| Dashboard error display | `webui/bmad-dashboard.html` + `bmad-dashboard-store.js` | Reinstate or clean up the error template |
| `project-context.md` stub | `skills/bmad-init/scripts/bmad-init.sh` | Write empty stub on init; upstream BMAD v6 alignment |
| Plugin audit | — | Run `a0-review-plugin` skill; fix any Critical/Important findings |

**Phase D acceptance criteria:**
- [ ] `bmad-master` can call all 20 subordinates without a static table (relies on dynamic profile list)
- [ ] `prompts/bmad.methodology.shared.md` included by all 20 `main.specifics.md`
- [ ] Dashboard error states display correctly
- [ ] `a0-review-plugin` passes with no Critical findings

---

### Phase E — Optional Upstream v6 Sync
**Effort:** 2–3 weeks | **Risk:** High | **Decision:** Deferred — user to decide post Phase D

Includes: `module.yaml` per module, `customize.toml` 3-layer model, `_bmad/` non-dot output folder migration, BMGD module addition. Only if user decides to track upstream BMAD-METHOD v6.

---

## Success Criteria (full migration)

**Phase A (merge gate — no Phase B until these pass):**
- [ ] `bmad-init.sh /tmp/test-dir` → config contains `$A0PROJ`-derived paths, NOT `/a0/usr/projects/`
- [ ] `tidy -e webui/bmad-dashboard.html` → zero errors
- [ ] `pytest tests/ -v` → all green
- [ ] Routing extension and dashboard show identical phase value
- [ ] No top-level silent exception swallow in routing extension

**Phase B:**
- [ ] `plugin.yaml` has `per_project_config: true`
- [ ] `bmad-user-prefs.promptinclude.md` exists and is auto-injected
- [ ] All A0 instances of `AGENT_NAMES`/`PHASE_ACTIONS` use the single core module source
- [ ] `.gitignore` blocks AI-tool scratch dirs
- [ ] `develop` branch pushed to remote; VPS deploy pipeline confirmed

**Phase C:**
- [ ] CSV columns aligned to upstream format (all 13 columns)
- [ ] All ~40 workflow SKILL.md files have slash-style `trigger_patterns`
- [ ] `skills_tool:search` returns correct workflows on VPS testing instance
- [ ] Routing extension caching confirmed working

**Phase D:**
- [ ] `bmad-master/role.md` has no static agent table
- [ ] `bmad.methodology.shared.md` included by all 20 agents
- [ ] `a0-review-plugin` clean

**Overall (pre-`main` merge):**
- [ ] All 20 BMAD agents functional end-to-end on VPS testing instance
- [ ] BMAD initializable from workdir, `/a0/usr/projects/`, `/tmp/`, any arbitrary path
- [ ] Tagged as `v1.1.0`; merged to `main`

---

## Open Questions

1. ~~**VPS mapping type**~~ ✅ **RESOLVED** — `/home/debian/agent-zero/testing` is Docker volume-mounted to `/a0` (the dev container). Symlink established on VPS host: `testing/usr/plugins/bmad_method → development/usr/projects/a0_bmad_method`. Changes in `/a0/usr/projects/a0_bmad_method` are instantly live on the testing instance. `git push develop` is the record.

2. ~~**`{{agent_profiles}}` covers BMAD profiles?**~~ ✅ **RESOLVED** — `agent.system.tool.call_sub.py` calls `subagents.get_available_agents_dict(project)` which walks all `agents/*/` dirs including from plugins. All 20 BMAD profiles are auto-included. Phase D static table removal is safe to proceed.

3. ~~**CSV vs SKILL.md routing**~~ ✅ **RESOLVED** — `module-help.csv` is upstream BMAD-METHOD's canonical routing mechanism (confirmed in `bmad-code-org/BMAD-METHOD` source). Upstream SKILL.md carries only `name`+`description`. Phase C revised: keep CSV as routing source, add `trigger_patterns` to SKILL.md for A0 discoverability only.

4. **`bmad.methodology.shared.md` exact scope:** Which sections are truly shared across all 20 agents vs. module-specific? (BMM phase model not relevant to BMB/CIS agents.) Resolve at Phase D start by reading all 20 `main.specifics.md` files.

5. **Party Mode requirements:** `party-mode` workflow exists in `skills/bmad-init/core/workflows/party-mode/`. Any specific acceptance criteria for multi-agent coordination in scope?

6. **`02-bmad-state.md` backward compat:** If we later migrate to YAML frontmatter (cleaner parsing), we need a migration script for existing initialized projects. Defer to Phase C decision.
