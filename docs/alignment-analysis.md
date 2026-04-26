# BMAD ↔ Agent Zero Deep Alignment Analysis

**Date:** 2026-04-26  
**Status:** Read-only analysis — no plugin files modified  
**Sources:** harness architecture doc (rev-5), prompt cartography doc (rev-5), local plugin source, prior code review (25 findings), verification report (20 confirmed)  
**Purpose:** Foundational analysis for next plugin iteration

---

## Section 1 — Agent Zero Harness Mental Model

### 1.1 Per-Turn Lifecycle

Every agent turn executes the same pipeline, encoded in `Agent.monologue()` at `/a0/agent.py:373`:

```
[monologue_start exts]
  → [message_loop_start exts]
  → prepare_prompt()
      → [message_loop_prompts_before exts]   # inject pre-prompt material
      → get_system_prompt()                   # fires all system_prompt exts
          → _10_main_prompt                   # reads agent.system.main.md + includes
          → _11_tools_prompt                  # assembles agent.system.tool.*.md fragments
          → _12_mcp_prompt                    # MCP tools if configured
          → _13_secrets_prompt                # alias declarations
          → _13_skills_prompt                 # skill catalog metadata
          → _14_project_prompt                # active project context
          → _16_promptinclude (plugin)        # *.promptinclude.md files from workdir
          → _20_behaviour_prompt (plugin)     # behaviour.md rules
      → [message_loop_prompts_after exts]    # write extras_temporary / extras_persistent
          → _50_recall_memories               # FAISS recall → extras_temporary[memories]
          → _60_current_datetime              # extras_temporary[current_datetime]
          → _63_recall_relevant_skills        # similarity-ranked skill hints
          → _65_include_loaded_skills         # loaded skill bodies → extras_temporary
          → _66_include_active_skills         # permanently activated → extras_persistent
          → _70_include_agent_info            # profile/LLM → extras_temporary
          → _75_include_workdir_extras        # file tree → extras_temporary
          → _80_bmad_routing_manifest (BMAD) # routing table → extras_temporary
      → assemble: SystemMessage(system_text) + history_langchain + extras envelope
      → extras_temporary.clear()
  → [before_main_llm_call exts]
  → call_chat_model() — streaming JSON
      → closing } detected → stream stops
  → process_tools()
      → validate_tool_request
      → resolve: MCP first, then profile→plugins→core
      → [tool_execute_before exts]  # secret unmask
      → tool.execute()
      → [tool_execute_after exts]
      → hist_add_tool_result()
  → if break_loop → return to superior
  → [message_loop_end exts]
  → next iteration
```

The system prompt is **fully rebuilt every iteration** at `get_system_prompt()` (`agent.py:634`). The LLM sees: a static fragment assembly (role, tools, skills catalog, project) followed by a dynamic `[EXTRAS]` appendix (memories, datetime, loaded skills, workdir tree, plugin-injected context). The system prompt head is cache-friendly (stable across turns); EXTRAS varies.

### 1.2 Extension Points — Complete Hook Map

Every extension is a Python file in `extensions/python/<point>/` (or `plugins/<name>/extensions/python/<point>/`), ordered by numeric filename prefix within each hook.

| Hook | Numeric range | Representative use |
|---|---|---|
| `system_prompt` | _09_–_20_ | Assemble every paragraph of the system prompt |
| `message_loop_prompts_before` | any | Inject pre-history material (rarely used) |
| `message_loop_prompts_after` | _50_–_80_ | Write extras_temporary/persistent keys |
| `message_loop_start` | any | Per-iteration setup |
| `message_loop_end` | any | Post-iteration teardown |
| `monologue_start` | any | Per-monologue setup |
| `monologue_end` | any | Per-monologue cleanup |
| `before_main_llm_call` | any | Last-chance prompt mutation |
| `reasoning_stream` / `response_stream` | any | Stream inspection |
| `tool_execute_before` | _10_ | Secret unmask, pre-validation |
| `tool_execute_after` | any | Result transformation |
| `hist_add_before` | any | History entry pre-processing |
| `hist_add_tool_result` | any | Tool result post-processing |
| `agent_init` | any | Per-context initialization |
| `job_loop` | any | Background scheduler integration |
| `webui_ws_*` | any | WebSocket event hooks |
| `__main___init_a0_end` | any | Framework boot |

**BMAD currently uses only `message_loop_prompts_after` (`_80_`)** — one hook of 16+.

### 1.3 Four-Tier Composition Model

```
Tier 1 — Prompt Fragments (.md files)
  /a0/prompts/                      framework defaults
  /a0/agents/<profile>/prompts/     profile overrides (filename wins)
  /a0/plugins/<p>/prompts/          plugin additions
  /a0/usr/plugins/<p>/agents/<prf>/prompts/   user-plugin profile overrides

Tier 2 — Extensions (.py files in extensions/python/<hook>/)
  Execute in numeric-prefix order within each hook
  Plugin extensions interleave by same numeric key
  May mutate: system_prompt list, loop_data.extras_*, loop_data.history_output

Tier 3 — Tools (Tool subclasses, always-on, advertised in system prompt)
  Discovered at call time: profile/tools/ → plugins/*/tools/ → tools/
  Advertised via agent.system.tool.*.md fragments (assembled by _11_tools_prompt)
  MCP tools resolved FIRST before local tools

Tier 4 — Skills (SKILL.md bundles, lazy-loaded on demand)
  Discovered by rglob("SKILL.md") — nested directories work
  Loaded via skills_tool:load → injects full body into extras_persistent
  Only metadata (name/description/trigger_patterns) visible until loaded
  _63_ injects relevance-ranked skill summaries as hints each turn
```

### 1.4 Override Stack (prompt resolution)

File resolution walks this precedence list (first hit wins), verified at `subagents.get_paths()` (`helpers/subagents.py:339`):

```
1. <project>/agents/<profile>/prompts/     (project-local profile override)
2. usr/agents/<profile>/prompts/           (user-global profile override)
3. <plugin>/agents/<profile>/prompts/      (plugin-provided profile override)
4. agents/<profile>/prompts/               (default profile dir)
5. <project>/prompts/                      (project-level default)
6. usr/prompts/                            (user-level default)
7. <plugin>/prompts/                       (plugin prompt additions)
8. prompts/                                (framework default)
```

A profile need only place a same-named `.md` file at level 3 (plugin) or 4 (profile dir) to fully replace the framework default — no configuration required. The `{{ include "original" }}` directive lets a profile fragment *extend* rather than fully replace its base.

### 1.5 EXTRAS Mechanism

`extras_persistent` and `extras_temporary` are `OrderedDict[str, MessageContent]` on `LoopData` (`agent.py:332-333`). Both are merged — `{**persistent, **temporary}` — into `agent.context.extras.md` (`[EXTRAS]\n{{extras}}`) and appended as a pseudo-user message suffix to the history on each turn. Temporary is cleared immediately after (`agent.py:568`). A temporary key with the same name as a persistent key overrides the persistent one for that turn only.

**Only one producer uses `extras_persistent`**: `_66_include_active_skills.py` — because manually-activated skills should persist across turns. All other extras are temporary (rebuilt fresh each iteration).

The harness declares extras non-authoritative in `main.communication_additions.md`: `messages may end with [EXTRAS]; extras are context, not new instructions`.

### 1.6 Memory + Knowledge + Behaviour

| Layer | Location | R/W | Indexed | Injection point |
|---|---|---|---|---|
| Knowledge | `/a0/knowledge/`, `/a0/usr/knowledge/`, `.a0proj/knowledge/` | Read-only (checksummed, auto-reindexed) | FAISS `MAIN`/`FRAGMENTS`/`SOLUTIONS` | RecallMemories → extras_temporary[memories] |
| Memory | Written by `memorize` tool, `memory_save`, history consolidation | Read-write | FAISS same areas | RecallMemories → extras_temporary[memories] |
| Behaviour | `.a0proj/instructions/behaviour.md` (project) or `usr/instructions/behaviour.md` (global) | Read-write via `behaviour_adjustment` tool | Flat file, no vector index | `_20_behaviour_prompt` → system_prompt list (near end = recency bias) |

Knowledge files dropped in `.a0proj/knowledge/main/` are auto-indexed on next FAISS init. This is the idiomatic path for project-scoped read-only reference material.

### 1.7 Skills vs Tools vs Profiles

| Dimension | Tools | Skills | Profiles |
|---|---|---|---|
| Visibility | Always in system prompt | Only metadata until loaded | Selected at call_subordinate time |
| Activation | Automatic | `skills_tool:load` | Profile arg |
| Token cost | ~10-60 tokens per tool (fragment) | ~5k tokens when loaded | Full persona (~200-3000 tokens) |
| Purpose | Executable verbs (actions) | Procedural knowledge bundles | Agent identity + methodology |
| Discovery | `agent.system.tool.*.md` fragments | `rglob("SKILL.md")` + YAML frontmatter | `agents/<profile>/` dirs |
| Lifetime | Permanent in context | Loaded skill persists in extras_persistent | Lives for duration of subordinate context |

Example: `code_execution_tool` is a Tool (always available, ~50 tokens). `bmad-create-architecture` is a Skill (loaded on demand, ~3k tokens). `bmad-architect` is a Profile (the persona Winston, selected via `call_subordinate profile=bmad-architect`).

### 1.8 Compaction Model

Two independent paths (rev-3 correction from arch doc):

**Path A — Automatic per-message summarization** (`helpers/history.py`): Recent messages preserved verbatim; older messages progressively compressed via `fw.topic_summary.sys.md` + `fw.topic_summary.msg.md`. Always active, no trigger. The summarizer (`fw.memory.hist_sum.sys.md`) explicitly drops code/long results, keeps IDs/URLs/names — tool outputs degrade over long sessions.

**Path B — User-initiated full-chat compaction** (`plugins/_chat_compaction/`): WebUI "compact" button only. Gated by `MIN_COMPACTION_TOKENS = 1000` as a *floor* (prevent trivially-short compaction), not an auto-trigger. No python hooks in `_chat_compaction/extensions/` — purely UI-triggered.

Implication for BMAD: Large routing manifests and workflow skill bodies injected into EXTRAS will eventually be dropped by Path A's summarizer. The routing manifest survives because it's re-injected fresh every turn as `extras_temporary`. Loaded skill bodies survive in `extras_persistent` until explicitly cleared.

---

## Section 2 — BMAD Functional Requirements

Distilled from plugin.yaml, bmad-master role.md, bmad-init/SKILL.md, and module-help.csv. These are *what* must work, not *how*.

### 2.1 Phase Tracking + Transitions
The system must track which of the 4 BMM phases (1-Analysis, 2-Planning, 3-Solutioning, 4-Implementation) plus special states (ready, bmb, cis) the user's project is currently in. Phase must be readable by the routing extension, the dashboard, and the CLI status tool. Phase transitions must be writable by bmad-master after workflow completions. Phase must be durable across sessions.

### 2.2 Phase-Aware Routing
The available set of workflows must change based on current phase. Phase 1 shows analysis workflows; Phase 4 shows implementation workflows. Anytime workflows (document-project, quick-spec, etc.) are always visible. Phase gates must be enforced: Phase N cannot start without Phase N-1 artifacts.

### 2.3 Specialist Agent Personas
20 named specialists, each with: a persona name (Mary, John, Winston, etc.), a module affiliation (BMM/BMB/TEA/CIS), a phase or phase range, and a defined communication style. Each must be addressable via `call_subordinate` with the correct profile.

### 2.4 Workflow Execution
Each workflow is a guided multi-step procedure. Workflows define: required inputs, output artifact names and locations, optional elicitation steps, and acceptance criteria. Workflows must be loadable on demand (not resident in context permanently). Workflow content must be authoritative — agents must not improvise workflow steps from memory.

### 2.5 Artifact Lifecycle
Each phase produces named artifacts (Product Brief, PRD, Architecture, Sprint Plan, Stories) stored at defined filesystem paths. Artifact existence gates phase transitions. Stale artifacts (parent updated after child) should generate warnings.

### 2.6 Project-Scoped State
Each A0 project has independent BMAD state: current phase, active persona, in-progress artifact. State must not leak across projects. State must survive agent context teardown and restart.

### 2.7 Knowledge/Memory Isolation Per Project
BMAD framework knowledge (agent patterns, methodology docs) and project-specific artifacts must be scoped to the active project's FAISS index, not shared across projects.

### 2.8 Status Visibility
Status must be accessible three ways: (a) dashboard UI in the A0 WebUI sidebar, (b) CLI `bmad-status` command, (c) agent self-inspection (routing manifest in EXTRAS). Status covers: current phase, active persona, module health, test results summary.

### 2.9 Help / Discovery
At any time, the user should be able to ask "what can BMAD do for me right now?" and receive a phase-filtered list of available workflows with their trigger phrases. Discovery must work before BMAD is initialized (bootstrap help) and after (phase-contextual help).

### 2.10 Customization
Per-project: user name, communication language, skill level. These affect agent communication style. Optionally: custom artifact paths. These must be readable by all 20 agents without per-agent configuration.

### 2.11 Init Bootstrap
First-time setup: create directory structure, seed framework knowledge into project FAISS, write initial config and state files. Must be idempotent (safe to run twice). Must work for any project path, not just `/a0/usr/projects/`.

### 2.12 Party Mode / Multi-Agent Coordination
For complex workflows, multiple BMAD specialists can be orchestrated in sequence. The ordering and hand-off protocol must be defined. (Currently present in `teams/default-party.csv` files but minimally implemented.)

---

## Section 3 — Current BMAD ↔ A0 Mapping

For each functional requirement, current implementation, idiomaticity score, and evidence.

---

### 3.1 Phase Tracking
**Score: ⚠️ working but not idiomatic**

**Current implementation:** `02-bmad-state.md` markdown file at `.a0proj/instructions/02-bmad-state.md`. Parsed by a line-prefix string match in the routing extension (`_80_bmad_routing_manifest.py:378-380`: `if line.strip().startswith("- Phase:")`) and by an unanchored regex in the status core (`helpers/bmad_status_core.py:27`: `re.search(r"Phase:\s*(.+)", text)`). Two divergent parsers for the same field — verified Critical finding C2 in code review.

**A0's mechanism:** The `lifecycle:` tool manages `.a0proj/run/current/state.md` with YAML frontmatter (`phase:`, `findings.md`, `progress.md`). A0's lifecycle phases are IDEA→SPEC→PLAN→BUILD→VERIFY→REVIEW→SHIP — a 7-stage software development pipeline.

**Why not a drop-in replacement:** A0's lifecycle tool tracks the *plugin/code development* lifecycle for the agent's own work. BMAD's phases track the *user's business methodology project lifecycle*. These are orthogonal axes. A user's project could be in BMAD Phase 2 (Planning) while the BMAD plugin itself is in A0 SHIP phase. Replacing `02-bmad-state.md` with A0's `state.md` would conflate two independent state machines.

**Remaining problem:** The two parsers are a correctness bug (C2, confirmed). The fix is a shared parser helper, not a mechanism replacement.

---

### 3.2 Phase-Aware Routing (Routing Manifest)
**Score: ⚠️ working but not idiomatic — large and fragile**

**Current implementation:** `_80_bmad_routing_manifest.py` — a 424-line extension executing at `message_loop_prompts_after` hook, writing to `extras_temporary["bmad_routing_manifest"]`. The extension:
1. Resolves state file path (`_resolve_state_file` — has C3 cross-project fallback bug)
2. Reads current phase from state file (C2 parser divergence)
3. Reads all `skills/*/module-help.csv` files (5 CSVs) to build routing rows
4. Filters by `PHASE_MODULES` dict mapping phase → module codes
5. Scans artifact filesystem for phase completion detection (AC-01 through AC-06)
6. Builds staleness warnings (mtime comparisons on PRD/Architecture/Sprint Plan)
7. Injects assembled manifest as a ~30-60 line text block into `extras_temporary`

This runs on **every bmad-master message loop**, re-reading and parsing all CSVs each time (I5 — confirmed).

**The CSV architecture:** Each `skills/*/module-help.csv` has 13 columns: `module, skill, display-name, menu-code, description, action, args, phase, after, before, required, output-location, outputs`. These are routing metadata that live in CSVs *separate from* the SKILL.md files they reference.

**A0's native mechanism:** SKILL.md YAML frontmatter (`name`, `description`, `version`, `tags`, `trigger_patterns`) is the canonical metadata surface A0 uses for skill discovery. The `_63_recall_relevant_skills.py` extension runs similarity ranking on this metadata every turn. Nothing in A0 uses a separate CSV registry.

**Idiomaticity gap:** BMAD has invented a parallel metadata registry (module-help.csv) that duplicates information which should live in SKILL.md frontmatter. The routing extension is custom infrastructure replicating A0's skill-discovery pattern with additional phase-aware filtering.

---

### 3.3 Specialist Agent Personas
**Score: ✅ idiomatic**

**Current implementation:** 20 profile directories under `agents/bmad-*/`, each containing `prompts/agent.system.main.role.md`, `main.specifics.md`, `main.communication_additions.md`, `main.solving.md`, `main.tips.md` (confirmed in file tree). Each overrides the relevant prompt fragments to inject the persona (Mary, John, Winston, etc.) and methodology context.

This is exactly the A0 profile override pattern — filename-driven replacement at the plugin level (path precedence level 3: `<plugin>/agents/<profile>/prompts/`). The `call_subordinate` tool selects these by `profile=bmad-architect` etc.

**Minor gap:** Each profile's `main.specifics.md` likely contains duplicated BMAD methodology boilerplate (BMAD Activation Protocol, Initial Clarification, Thinking Framework, Using BMAD Skills sections) that appears identically or near-identically in all 20 agents. Verified in bmad-master role.md (last ~100 lines of output): these sections are methodology-level, not persona-level. This is a DRY violation but not an idiomaticity problem.

---

### 3.4 Workflow Execution
**Score: ✅ idiomatic (nested skills) with ⚠️ routing indirection**

**Current implementation:** Workflows live as nested SKILL.md files (e.g., `skills/bmad-bmm/workflows/4-implementation/dev-story/SKILL.md`). A0's `rglob("SKILL.md")` discovers these automatically. `module-help.csv` column `action` specifies the skill name to load (e.g., `bmad-dev-story`), which then points to the workflow file.

The nested SKILL.md approach for workflows is idiomatic — A0 supports nested skill discovery. The indirection through module-help.csv → action column → skills_tool:load is the non-idiomatic layer; it creates a two-hop lookup where A0's trigger_patterns mechanism could handle the first hop directly.

---

### 3.5 State Injection
**Score: ⚠️ working but suboptimally positioned**

**Current implementation:** `_80_bmad_routing_manifest.py` writes three keys to `extras_temporary`:
- `bmad_routing_manifest` — routing table (30-60 lines, rebuilt every turn from CSV parse)
- `bmad_paths` — resolved config/plugin root paths
- `bmad_not_initialized` — message when no BMAD project found

All three are `extras_temporary`, meaning they disappear from the prompt dict after each turn's `prepare_prompt()` clears them, then are re-injected next turn by the extension re-running. This is functionally correct for data that changes per-phase.

**Position issue:** `message_loop_prompts_after` at `_80_` fires *after* the system prompt is built. EXTRAS appears as an appendix after message history. For context that is fundamentally "part of what bmad-master is configured to know" (routing table), the `system_prompt` hook would place it inside the system prompt proper — semantically more appropriate and earlier in the prompt (slightly better for LLM attention on the routing instructions).

**Compaction note:** Since these are `extras_temporary`, they survive compaction — the extension will re-populate them on the next turn even if old history is compressed. This is correct behavior.

---

### 3.6 Dashboard
**Score: ✅ uses A0 WebUI extension mechanism, ⚠️ correctness issues**

**Current implementation:** `webui/bmad-dashboard.html` + `webui/bmad-dashboard-store.js` are loaded via A0's webui plugin mechanism. `extensions/webui/sidebar-quick-actions-main-start/_bmad_dashboard_btn.html` injects a dashboard button into A0's sidebar. The dashboard calls `api/plugins/bmad_method/_bmad_status` (served by `api/_bmad_status.py` via `helpers/api.ApiHandler`).

Using A0's `extensions/webui/` mechanism for UI injection and `api/` for backend endpoints is idiomatic. The correctness issues (C4 — 4 stray `</div>` + 1 stray `</template>`; I2 — importlib None guard missing; I8 — Alpine store error field undeclared) are bugs, not idiomaticity problems.

**Hardcoded plugin name:** `webui/bmad-dashboard-store.js:23` and `bmad-dashboard.html:6` hardcode `bmad_method` as the API path prefix (S7, confirmed). A0 does not expose a `pluginBaseUrl` runtime variable, so this cannot be cleanly fixed without an A0 core feature request.

---

### 3.7 Slash Commands / Triggers
**Score: ⚠️ working but fragmented — natural language only**

**Current implementation:** Two parallel trigger surfaces:
1. SKILL.md frontmatter `trigger_patterns` lists (e.g., `bmad-init/SKILL.md` has 12 trigger phrases like `"bmad init"`, `"setup bmad"`, `"bmad help"`)
2. `module-help.csv` columns `display-name` + `description` used by the routing manifest for LLM matching
3. bmad-master role.md contains a natural-language routing description

There is no formal slash command registration (no `/bmad` prefix commands). Everything is natural-language trigger-phrase based.

**A0's mechanism:** The `trigger_patterns` field in SKILL.md frontmatter IS A0's native trigger mechanism — `_63_recall_relevant_skills.py` uses these for similarity ranking. No formal `/command` system exists in A0's core (not found in prompt cartography or extensions list). So BMAD's trigger_patterns usage in SKILL.md is idiomatic. The separate module-help.csv triggers are redundant with SKILL.md.

---

### 3.8 Customization
**Score: ⚠️ functional but reinvents A0's persistence mechanisms**

**Current implementation:** `01-bmad-config.md` is a markdown file written by `bmad-init.sh` containing:
- Path alias table (6 aliases mapping `{planning_artifacts}` etc. to absolute paths)
- User settings section (User Name, Communication Language, User Skill Level)

This file is read by `_parse_alias_map()` in the routing extension and referenced by agents. It is injected into agent context as a project instruction file (auto-loaded by A0's project system at `.a0proj/instructions/`).

**A0's mechanism:** `behaviour.md` (edited via `behaviour_adjustment` tool) is the idiomatic channel for persistent behavioural rules. `*.promptinclude.md` files (auto-discovered under workdir by `_16_promptinclude` plugin) are the idiomatic channel for project-specific context. A0's project instruction files (`.a0proj/instructions/`) are also a valid path.

**Gap:** A0 already provides `behaviour_adjustment` as a tool that agents can call to update persistent rules, with a two-step LLM-mediated merge pipeline. BMAD's `01-bmad-config.md` is hand-crafted markdown with no A0-mediated update path. A user who wants to change their communication language must manually edit the file or ask bmad-master to edit it.

---

### 3.9 Memory / Knowledge
**Score: ✅ correctly uses A0's knowledge import mechanism**

**Current implementation:** `bmad-init.sh` runs `cp -rn "$SEED_DIR/." "$A0PROJ/knowledge/main/"` (line 21). This seeds framework knowledge files into `.a0proj/knowledge/main/` — exactly the path A0 auto-indexes into the project FAISS store. The `seed-knowledge/` directory contains per-agent `.md` reference files.

This is idiomatic. The init script correctly uses A0's knowledge-import mechanism. The correctness issues (C1 — path hardcoding, I9 — `cp -rn` portability) are bugs in the script, not architectural misalignment.

**One gap:** `per_project_config: false` in `plugin.yaml` (I10, partially confirmed). This is correct for *runtime* behavior (project resolution already uses `get_context_project_name`), but setting it to `true` would surface per-project enable/disable toggles in A0's plugin manager UI, which is the expected UX for a fundamentally project-scoped plugin.

---

### 3.10 Init Bootstrap
**Score: ⚠️ functional shell script with critical path bug**

**Current implementation:** `skills/bmad-init/SKILL.md` triggers `skills/bmad-init/scripts/bmad-init.sh <PROJECT_PATH>` via `code_execution_tool` terminal runtime. The script creates directory structure, seeds knowledge, writes `01-bmad-config.md` and `02-bmad-state.md`.

**Critical bug C1 (confirmed):** `bmad-init.sh:40-44` writes hardcoded absolute paths:
```bash
| `{project-root}` | `/a0/usr/projects/$PROJECT_NAME/.a0proj/` |
```
The script already computes `A0PROJ="$PROJECT_PATH/.a0proj"` at line 4, but the here-doc uses `$PROJECT_NAME` (just the basename) instead of `$A0PROJ`. This means every alias resolution in `_parse_alias_map()` returns wrong paths for any project not under `/a0/usr/projects/`, silently making the entire artifact detection subsystem a no-op.

**Mechanism question:** The init script is a bash shell script invoked by a skill. A0's Tool subclass pattern could provide a richer init experience (progress feedback, error handling, idempotency checks), but for a one-time bootstrap operation, a bash script via `code_execution_tool` is pragmatically fine and requires no extra Python infrastructure.

---

### 3.11 Help / Discovery
**Score: ⚠️ duplicated surfaces, partially redundant with A0-native**

**Current implementation:** Two surfaces:
1. `bmad-init/SKILL.md` Section 2 contains a complete module reference with trigger phrases — this is the bmad-help skill body
2. `bmad-master/role.md` contains the full 19-agent routing table and available workflows inline

Users can ask bmad-master for help directly (it uses its role.md knowledge) or load the `bmad-init` skill explicitly.

**A0's mechanism:** `_63_recall_relevant_skills.py` injects similarity-ranked skill summaries into EXTRAS every turn, showing the agent what skills are relevant. This is the discovery surface. The agent's knowledge of available skills comes from the SKILL.md `description` and `trigger_patterns` fields.

**Gap:** The bmad-master role.md hard-codes the workflow table as markdown — this is a maintenance liability. When a new workflow is added to `module-help.csv`, the role.md table does not auto-update. The CSV + routing manifest extension provide the live routing table, but the help text in role.md is static.

---

### 3.12 Inter-Agent Context (Subordinate Description)
**Score: ❌ duplicates A0's native profile registry injection**

**Current implementation:** `agents/bmad-master/prompts/agent.system.main.role.md` contains a hardcoded 19-row table:

```
| `bmad-analyst` | Mary (Business Analyst) | BMM Phase 1 | ... |
| `bmad-pm` | John (Product Manager) | BMM Phase 2 | ... |
...
```

This static table tells bmad-master which profiles exist and what they do.

**A0's mechanism:** `agent.system.tool.call_sub.md` (prompt cartography §4.2) has a conditional template block:
```
{{if agent_profiles}}
available profiles:
{{agent_profiles}}
{{endif}}
```
This injects the **live profile registry** into the call_subordinate tool prompt every turn. The `{{agent_profiles}}` variable is populated dynamically from the discovered `agents/*/` directories — meaning all 20 BMAD profiles would be listed automatically.

**Problem:** The static table in role.md is a duplicate of the dynamic `{{agent_profiles}}` injection. If a new BMAD agent is added, the static table in role.md must be manually updated. The A0 mechanism would auto-discover it.

**Why this is ❌:** This directly fights A0's mechanism. The `{{agent_profiles}}` block in the call_sub tool prompt already serves this purpose. bmad-master's role.md table is maintenance-duplicating what the harness provides for free.

---

## Section 4 — Alignment Recommendations

### 4.1 Phase Tracking — Fix the Bug, Preserve the Mechanism

**Goal:** Consistent, reliable phase reading by routing extension, dashboard, and CLI  
**Current approach:** Two divergent parsers: line-prefix (`startswith("- Phase:")`) in routing extension, unanchored regex in `bmad_status_core.py`  
**A0-native alternative:** N/A — A0's lifecycle tool solves a different problem. Phase tracking via markdown file is appropriate for BMAD's use case; the mechanism is fine, the implementation is buggy.

**Migration sketch:**
1. Create single shared parser in `helpers/bmad_status_core.py` (code review C2 fix already specifies it):
```python
_PHASE_RE = re.compile(r"^\s*[-*]?\s*Phase\s*:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
```
2. Replace `_80_bmad_routing_manifest.py:378-380` inline parser with call to `bmad_status_core.read_state(state_path)["phase"]`
3. The state file format (`02-bmad-state.md`) itself is compatible with A0's project instruction injection — `.a0proj/instructions/` files are auto-loaded as project context, so the state is already visible to all BMAD agents without explicit file-reading.

**On the lifecycle tool question:** BMAD's 4-phase methodology model should coexist with A0's 7-phase lifecycle as **parallel orthogonal axes**. A0's lifecycle = the development state of the *plugin itself*. BMAD's phases = the state of the *user's product development project*. They do not map onto each other and should not be collapsed.

**Tradeoffs:** Coexistence means two phase concepts exist. Mitigation: naming discipline (`bmad-phase` vs. `lifecycle-phase` in documentation) prevents confusion.

**Risk:** Low — fix is surgical, no mechanism change  
**Effort:** S (hours)

---

### 4.2 Routing Manifest — Absorb Metadata Into SKILL.md Frontmatter

**Goal:** Phase-aware workflow routing without a separate CSV registry  
**Current approach:** 5 `module-help.csv` files with 13 columns, parsed by `_80_` extension every turn  
**A0-native alternative:** SKILL.md YAML frontmatter with extended fields; thin routing extension that reads frontmatter instead of CSVs

**Migration sketch:**
1. Extend each workflow SKILL.md frontmatter to include the fields currently in module-help.csv:
```yaml
---
name: "bmad-create-prd"
description: "Expert-led facilitation to produce PRD"
version: "1.0.0"
tags: ["bmad", "planning", "prd"]
trigger_patterns:
  - "create prd"
  - "product requirements document"
bmad:
  module: bmm
  agent: pm
  display-name: Create PRD
  menu-code: CP
  phase: 2-planning
  required: true
  output-location: planning_artifacts
  outputs: prd*.md
---
```
2. Replace the `_collect_routing_rows()` CSV reader in `_80_bmad_routing_manifest.py` with a SKILL.md frontmatter scanner using `rglob("SKILL.md")`
3. Parse the `bmad:` frontmatter block to extract routing metadata
4. Filter by `bmad.phase` field against current phase
5. The CSVs become redundant and can be removed over time (or kept as legacy reference)

**Performance improvement:** SKILL.md scanner still runs every turn, but reads fewer/smaller files and avoids the dual-read pattern (I5). With caching keyed on SKILL.md mtimes, it could be a near-zero cost per turn.

**What we lose:** The CSV format is human-editable and easy to read as a table. YAML frontmatter in 40+ SKILL.md files is distributed and harder to scan holistically. Mitigation: keep a generated read-only `module-help.csv` as a build artifact for documentation purposes.

**What we gain:** Single source of truth; no sync step when adding workflows; trigger_patterns in SKILL.md are immediately available to A0's `_63_recall_relevant_skills.py` for similarity-based discovery; the CSVs' `trigger_patterns` column becomes redundant with SKILL.md's native field.

**Risk:** Medium — requires updating 40+ SKILL.md files and rewriting the routing scanner  
**Effort:** M (days) — mostly mechanical YAML additions

---

### 4.3 Routing Extension Position — System Prompt vs. EXTRAS

**Goal:** Routing table visible and reliable in bmad-master context  
**Current approach:** `message_loop_prompts_after` hook → `extras_temporary` → appears in [EXTRAS] appendix after history  
**A0-native alternative:** `system_prompt` hook → appended to `system_prompt` list → appears before history

**Analysis:**  
The `system_prompt` hook runs during `get_system_prompt()`, before `message_loop_prompts_after`. Content injected there becomes part of the assembled system prompt header. This has two implications:
- Position: system prompt content appears *before* conversation history, which may give the routing table more stable attention from the LLM
- Caching: LLM provider prefix caching benefits the system prompt head. The routing manifest changes on phase transition (low frequency), so most turns would benefit from cache hits if placed there

However: the current `extras_temporary` approach works correctly (re-injected every turn, phase-filtered). The position difference is a quality-of-attention argument, not a correctness argument. For a ~50-line routing table used by bmad-master to dispatch, EXTRAS position is sufficient.

**Recommendation:** Keep in `message_loop_prompts_after` for now. If LLM routing accuracy is found to be a problem in practice, migrate to `system_prompt` hook as a targeted improvement.

**Risk:** Low (either position works)  
**Effort:** S (hours)

---

### 4.4 Customization — Adopt behaviour.md + promptinclude.md Pattern

**Goal:** Per-project user preferences (name, language, skill level) available to all BMAD agents  
**Current approach:** `01-bmad-config.md` — hand-crafted markdown, no A0-mediated update mechanism. Only readable by agents that explicitly know to look for it.  
**A0-native alternative:** Project-scoped `behaviour.md` and/or `*.promptinclude.md` files

**Migration sketch:**
1. Keep `01-bmad-config.md` for the **path alias table** (this is BMAD-specific infrastructure that A0 has no equivalent for)
2. Move user preference settings to a `bmad-user-prefs.promptinclude.md` file created by `bmad-init.sh`:
```markdown
## BMAD User Preferences
- User Name: {{user_name}}
- Communication Language: English
- User Skill Level: intermediate
- Respond in the user's communication style preference
```
3. Since `_16_promptinclude` auto-discovers `*.promptinclude.md` files recursively in workdir, this file is auto-injected into *every* agent's system prompt in the project — making preferences available to all 20 BMAD specialists without any agent needing to explicitly load the config file
4. The `behaviour_adjustment` tool can update `behaviour.md` for persistent rules; `bmad-user-prefs.promptinclude.md` can be updated by `text_editor:patch` when user preferences change

**What we lose:** The single-file `01-bmad-config.md` consolidation. The path aliases and user prefs are now in separate files.

**What we gain:** User preferences are injected into all 20 agent contexts automatically via A0's native mechanism. Users can update preferences using `behaviour_adjustment` (A0's native preference update tool). No agent needs special code to read user prefs.

**Risk:** Low — additive change, old file can stay  
**Effort:** S (hours)

---

### 4.5 Slash Commands — Formal Registration

**Goal:** Discoverable entry points (`/bmad`, `/bmad-init`, `/bmad-help`, `/bmad-phase`)  
**Current approach:** Natural-language trigger phrases in SKILL.md frontmatter  
**A0-native alternative:** No formal `/command` registration system exists in A0 core as of current version

**Verification:** Searching prompt cartography (§1, §2, §§9) and extensions list — no `commands` plugin or `/cmd` dispatch mechanism found in A0. The `trigger_patterns` field in SKILL.md frontmatter IS the A0-native equivalent of slash command registration, used by `_63_recall_relevant_skills.py`.

**Recommendation:** Do not pursue formal slash command registration; this would require either (a) an A0 core feature request or (b) a new BMAD plugin that intercepts message routing. The trigger_patterns approach is idiomatic.

**Optional enhancement:** Add more specific trigger patterns that look like slash commands to SKILL.md frontmatter:
```yaml
trigger_patterns:
  - "/bmad"
  - "/bmad-init"
  - "/bmad-help"
```
Users learn to type `/bmad` and A0's skill recall surfaces the correct skill. Zero infrastructure change needed.

**A0 API stability note:** If A0 adds a formal command registration system in a future version, BMAD would need to register then. Low risk given current trajectory.

**Risk:** Low (no change needed)  
**Effort:** S (hours — just add trigger pattern strings)

---

### 4.6 Help / Discovery — Remove Static Tables, Trust SKILL.md

**Goal:** Phase-contextual help that auto-updates when new workflows are added  
**Current approach:** Section 2 of `bmad-init/SKILL.md` has a manually maintained module reference; bmad-master role.md has a static workflow table  
**A0-native alternative:** `_63_recall_relevant_skills.py` already injects similarity-ranked skill summaries. The routing manifest already provides phase-filtered workflow list.

**Migration sketch:**
1. In `bmad-init/SKILL.md` Section 2, replace the hardcoded module table with instructions to read the routing manifest from EXTRAS and format it as a user-facing help response
2. Remove the static workflow table from bmad-master `role.md` — it's already present in `bmad_routing_manifest` EXTRAS and the dynamic `{{agent_profiles}}` template
3. When user asks for help, bmad-master reads its EXTRAS (routing manifest is already there) and formats it

**What we lose:** A human-readable offline reference table in role.md.

**What we gain:** Help is always in sync with installed workflows; no maintenance when adding workflows.

**Risk:** Low  
**Effort:** S (hours)

---

### 4.7 Init Bootstrap — Fix Critical Bug, No Mechanism Change Needed

**Goal:** Correct path alias generation for any project location  
**Current approach:** Shell script via `code_execution_tool`  
**A0-native alternative:** Tool subclass (Tool base class in `tools/`)

**On the Tool question:** The init script runs once per project; a Tool subclass would add Python infrastructure for a one-time operation. The shell script approach is pragmatically fine. The real issue is the C1 path bug.

**Required fix (C1):**
```bash
# Line 40-44: replace $PROJECT_NAME with $A0PROJ already computed at line 4
| `{project-root}` | `$A0PROJ/` |
| `{planning_artifacts}` | `$A0PROJ/_bmad-output/planning-artifacts/` |
| `{implementation_artifacts}` | `$A0PROJ/_bmad-output/implementation-artifacts/` |
| `{product_knowledge}` | `$A0PROJ/knowledge/` |
| `{output_folder}` | `$A0PROJ/_bmad-output/` |
```

**Optional quality improvement:** Convert to a Python script for better error handling, progress reporting, and `notify_user` integration. This would also eliminate the I9 `cp -rn` portability issue by using `shutil.copytree(dirs_exist_ok=True)`.

**Risk:** High if left unfixed (artifact detection silently broken); Low to fix  
**Effort:** S (minutes for the bash fix; hours for Python rewrite)

---

### 4.8 Subordinate Description — Use {{agent_profiles}} Template

**Goal:** bmad-master knows which specialist profiles exist without hardcoded table  
**Current approach:** Static 19-row table in `agents/bmad-master/prompts/agent.system.main.role.md`  
**A0-native alternative:** `{{agent_profiles}}` template variable in `agent.system.tool.call_sub.md` — already injects the live profile registry

**Migration sketch:**
1. Remove the static 19-row table from bmad-master `main.role.md`
2. Keep the persona descriptions (Mary, John, Winston, etc.) and module affiliations — these give bmad-master the routing intelligence to match user requests to the right specialist
3. The `{{agent_profiles}}` block in call_sub tool prompt already shows available profiles; augment bmad-master's specifics with routing hints rather than a full profile registry

**What we keep in role.md:** The per-specialist routing hints ("for PRD work → bmad-pm", "for architecture → bmad-architect"). The static table of profile names+personas+descriptions can move to a condensed format since the full list comes from `{{agent_profiles}}`.

**What we lose:** The rich persona descriptions (Mary/John/Winston etc.) in the routing table. These could move to `main.specifics.md` as routing guidance prose rather than a table.

**A0 API stability note:** `{{agent_profiles}}` is an established template variable in `agent.system.tool.call_sub.md` (verified in prompt cartography §4.2). Stability is high.

**Risk:** Low  
**Effort:** S (hours)

---

### 4.9 Shared Methodology Prompt Fragment

**Goal:** DRY the BMAD methodology boilerplate duplicated across 20 agent prompts  
**Current approach:** Each `agents/bmad-*/prompts/agent.system.main.specifics.md` likely contains near-identical BMAD Activation Protocol, Initial Clarification, Thinking Framework, Using BMAD Skills sections  
**A0-native alternative:** A shared `bmad.methodology.shared.md` prompt fragment included by all 20 agents via the `{{ include "bmad.methodology.shared.md" }}` directive

**Migration sketch:**
1. Extract the shared BMAD methodology sections into `agents/bmad-master/prompts/bmad.methodology.shared.md` (or better: a plugin-level `prompts/bmad.methodology.shared.md` accessible to all profiles)
2. Each agent's `main.specifics.md` becomes: persona identity + `{{ include "bmad.methodology.shared.md" }}` + agent-specific menu/workflow section
3. When methodology changes (e.g., clarification protocol update), change one file instead of 20

**File placement:** Since A0's prompt resolution walks plugin prompts (level 7), placing `bmad.methodology.shared.md` in the plugin's top-level `prompts/` directory makes it accessible to all 20 profile overrides via include directive.

**Risk:** Medium — include directive resolution must be verified for plugin-level `prompts/` directory; the `{{ include "original" }}` override pattern is fragile if the shared file is included from multiple levels  
**Effort:** M (days — requires reading all 20 specifics.md files to extract shared content)

---

### 4.10 Memory Seeding — Already Idiomatic, Fix the Script Bug

**Goal:** BMAD framework knowledge available in project FAISS index  
**Current approach:** `bmad-init.sh` seeds `.a0proj/knowledge/main/` — this IS A0's idiomatic knowledge import path  
**Remaining issues:** C1 path bug (seed happens to correct path because `$A0PROJ` is used here — seed is correct, alias table is wrong), I9 `cp -rn` portability

**No mechanism change needed.** The seed approach is correct. Fix the C1 alias bug and optionally replace `cp -rn` with `rsync` or a Python `shutil.copytree` call.

**Risk:** Low  
**Effort:** S

---

### 4.11 EXTRAS Injection — Temporary vs. Persistent

**Goal:** Routing manifest survives across turns  
**Current approach:** `extras_temporary` — cleared after every prompt build, re-populated next turn  
**Question from spec:** Should it use `extras_persistent` instead?

**Answer: No.** Since `BmadRoutingManifest.execute()` runs every message loop for bmad-master, the manifest is always re-populated. Using `extras_persistent` would mean the *stale* manifest from the previous turn persists if the extension fails silently (I1 bug), whereas `extras_temporary` means a failing extension produces no manifest at all — which is detectable. `extras_temporary` is the correct choice here.

**The I1 bug** (outermost `except: pass` swallows all errors) is the real problem. With proper error logging, a failing extension becomes observable and the choice of temporary vs. persistent is moot.

---

### 4.12 per_project_config Flag

**Goal:** Plugin manager shows per-project enable/disable UX  
**Current approach:** `per_project_config: false` in `plugin.yaml:23`  
**A0-native alternative:** `per_project_config: true` — enables project-scoped settings UI

**Confirmed (I10, partial):** This flag does NOT affect runtime project resolution. The plugin already resolves state per-project via `get_context_project_name(context)`. Setting it to `true` only unlocks the A0 plugin manager UI for per-project enable/disable. Since BMAD is fundamentally project-scoped, this should be `true`.

**Risk:** Low — cosmetic/UX change only  
**Effort:** Trivial (one-line change in plugin.yaml)

---

## Section 5 — Migration Roadmap

Principle: each phase is independently shippable. The plugin must remain fully functional at every checkpoint. Phases are ordered from lowest-risk/highest-impact to highest-risk/optional.

---

### Phase A — Critical Bug Fixes (must ship before any other work)

**Deliverables:**
1. Fix `bmad-init.sh:40-44` C1 — replace `$PROJECT_NAME` with `$A0PROJ` in path alias table (2 minutes)
2. Fix `_80_bmad_routing_manifest.py:423` I1 — add structured logging to outermost exception handler
3. Fix `api/_bmad_status.py:11-14` I2 — add `None` guard on `spec_from_file_location` result
4. Fix `helpers/bmad_status_core.py:27` I3 / C2 — add `re.MULTILINE` and `^` anchor to Phase regex; create shared `read_state()` helper; use it in routing extension
5. Remove C3 mtime cross-project fallback (or gate behind `BMAD_DEV_MODE` env var)
6. Fix `webui/bmad-dashboard.html:255-263` C4 — remove 4 stray `</div>` and 1 stray `</template>`

**Effort:** ~6–8 hours (code review estimate; confirmed)  
**Risk:** Low (all pure bug fixes)  
**Checkpoint:** All existing functionality works correctly; artifact detection subsystem is no longer a silent no-op; routing manifest appears consistently; dashboard renders correctly

---

### Phase B — Structural Alignment (code hygiene + A0 convention adoption)

**Deliverables:**
1. Add `{{ include "/command-style" }}` trigger patterns to key SKILL.md files (`/bmad`, `/bmad-init`, `/bmad-help`) — purely additive
2. Set `per_project_config: true` in `plugin.yaml`
3. Fix unused `SKILL_TO_MODULE` dead code removal (I7)
4. Fix S2 — remove unused `re, json` imports in `_bmad_status.py`
5. Fix I4 — add mtime-based invalidation to `_alias_cache` (or add comment documenting the non-invalidation intent)
6. Fix I6 — consolidate `AGENT_NAMES`/`PHASE_ACTIONS` dicts into `helpers/bmad_status_core.py` (single source for dashboard + CLI)
7. Fix S6/S8 — replace `phase[:2]` bucket prefix matching with explicit prefix dict in all 3 locations
8. Create `bmad-user-prefs.promptinclude.md` in init script output (§4.4) — move User Name/Language/Skill Level from config.md to promptinclude.md

**Effort:** M (days — mostly mechanical)  
**Risk:** Low  
**Checkpoint:** Dashboard and CLI report consistent data; user preferences auto-inject into all 20 agent contexts via promptinclude mechanism

---

### Phase C — SKILL.md Frontmatter Consolidation (eliminate module-help.csv)

**Deliverables:**
1. Define `bmad:` frontmatter schema for workflow SKILL.md files (module, agent, menu-code, phase, required, output-location, outputs)
2. Migrate all ~40 workflow SKILL.md files to include `bmad:` frontmatter block — replacing data currently in module-help.csv
3. Rewrite `_80_bmad_routing_manifest.py` routing scanner to read SKILL.md frontmatter via `rglob("SKILL.md")` + YAML parse instead of CSV read
4. Add SKILL.md mtime-based caching to routing scanner (performance improvement)
5. Mark module-help.csv files as deprecated (keep for one version as fallback)
6. Update `_63_recall_relevant_skills.py` context: trigger_patterns in workflow SKILL.md now serve dual purpose (A0 similarity recall + BMAD routing)

**Effort:** L (weeks — 40+ SKILL.md files to update, routing scanner rewrite, testing)  
**Risk:** Medium — requires careful testing of phase filtering logic  
**Checkpoint:** Phase-filtered routing works identically to CSV-based approach; new workflows auto-appear in routing manifest after SKILL.md addition only

---

### Phase D — UX Surface Refinement

**Deliverables:**
1. Remove static 19-agent table from bmad-master `role.md`; replace with routing guidance prose that references `{{agent_profiles}}` dynamic list
2. Create shared `bmad.methodology.shared.md` fragment; migrate Activation Protocol, Initial Clarification, Thinking Framework, Using BMAD Skills sections from all 20 `main.specifics.md` files
3. Update bmad-help logic to read from live routing manifest in EXTRAS rather than hardcoded module reference in `bmad-init/SKILL.md` Section 2
4. Add progress reporting (`notify_user` calls) to init script for multi-step visibility
5. Dashboard: fix I8 Alpine store error field; add proper error display template

**Effort:** M (days)  
**Risk:** Medium (shared prompt fragment require careful include-chain verification)  
**Checkpoint:** Adding a new workflow requires only: (a) create workflow directory + SKILL.md with bmad: frontmatter, (b) no other changes; it automatically appears in routing, help, and discovery

---

### Phase E — Optional: Upstream BMAD v6 Sync

This phase is optional and depends on user intent regarding upstream compatibility.

**Current state:** BMAD plugin is a v5-flavoured fork with v6 module structure. Key differences from upstream v6:
- Upstream v6 uses `module.yaml` (this plugin uses `module-help.csv`)
- Upstream v6 uses `customize.toml` (this plugin uses `01-bmad-config.md`)
- Upstream v6 has BGMD module vs. this plugin's TEA+CIS split
- Upstream v6 tracks state via artifact existence; this plugin uses explicit `02-bmad-state.md`

**Deliverables (if pursuing):**
1. Adopt `module.yaml` format for module metadata (or align frontmatter schema with v6's conventions)
2. Adopt `customize.toml` equivalent (or map v6 customization to A0's promptinclude pattern)
3. Evaluate upstream v6 workflow content for integration
4. Maintain A0-specific extensions while exposing upstream-compatible surface

**Risk:** High — extensive content migration, risk of divergence from both upstream and A0 conventions  
**Effort:** L (weeks)

---

## Appendix — Findings Cross-Reference

| Finding | Source | Status | Phase |
|---|---|---|---|
| C1 — hardcoded paths in init script | Review 31.txt + Verify 47.txt | Confirmed | Phase A |
| C2 — divergent Phase parsers | Review 31.txt + Verify 47.txt | Confirmed | Phase A |
| C3 — mtime cross-project fallback | Review 31.txt + Verify 47.txt | Confirmed | Phase A |
| C4 — broken HTML in dashboard | Review 31.txt + Verify 47.txt | Confirmed | Phase A |
| I1 — outermost except pass | Review 31.txt + Verify 47.txt | Confirmed | Phase A |
| I2 — importlib None guard | Review 31.txt + Verify 47.txt | Confirmed | Phase A |
| I3 — unanchored Phase regex | Review 31.txt + Verify 47.txt | Confirmed | Phase A |
| I4 — alias cache no mtime | Review 31.txt + Verify 47.txt | Confirmed | Phase B |
| I5 — double CSV read per loop | Review 31.txt + Verify 47.txt | Confirmed | Phase C |
| I6 — duplicated agent name dicts | Review 31.txt + Verify 47.txt | Confirmed | Phase B |
| I7 — SKILL_TO_MODULE dead code | Review 31.txt + Verify 47.txt | Partial (delete) | Phase B |
| I8 — Alpine error field | Review 31.txt + Verify 47.txt | Confirmed | Phase D |
| I9 — bash cp -rn portability | Review 31.txt + Verify 47.txt | Confirmed | Phase B |
| I10 — per_project_config false | Review 31.txt + Verify 47.txt | Partial (UX only) | Phase B |
| S1–S11 (suggestions) | Review 31.txt + Verify 47.txt | Various | Phase B |
| New: static agent table in role.md | This analysis §3.12 | ❌ fights A0 | Phase D |
| New: module-help.csv vs SKILL.md | This analysis §3.2/§4.2 | ⚠️ redundant | Phase C |
| New: user prefs in config vs promptinclude | This analysis §3.8/§4.4 | ⚠️ non-idiomatic | Phase B |
| New: shared methodology fragment | This analysis §4.9 | ⚠️ DRY violation | Phase D |

---

*End of alignment analysis. All claims grounded in local source files and prior verified review. No plugin files modified.*
