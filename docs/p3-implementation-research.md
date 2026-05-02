# P3 Implementation Research

> **Research Date:** 2026-05-02
> **Purpose:** Detailed analysis of 3 missing P3 alignment items to inform SPEC.md implementation tasks
> **Sources:** Upstream BMAD-METHOD v6.6.0 source, our plugin codebase, A0 framework capabilities

---

## 1. Sidecar Memory System

### What Upstream Does

Upstream BMAD Method stores persistent per-agent memory in `_bmad/_memory/*-sidecar/` directories. Each agent gets its own sidecar folder containing markdown files that survive across sessions:

- `memories.md`: Running memory of decisions and preferences accumulated over time
- `instructions.md`: Agent-specific behavioral instructions that evolve
- `documentation-standards.md`: Example — Tech Writer's accumulated documentation conventions

Key characteristics:
- **Per-agent scoping**: Each agent has its own sidecar directory (`_bmad/_memory/analyst-sidecar/`, `_bmad/_memory/pm-sidecar/`, etc.)
- **File-based**: Content stored as Markdown files, not structured data
- **Session-persistent**: Survives across sessions, loaded on agent activation
- **Agent-writable**: The agent itself writes to its sidecar during conversations
- **Distinct from persistent_facts**: Sidecar is runtime mutable memory; persistent_facts are static context loaded from TOML config

Source references:
- Research report section 10.3: "Agent sidecars are persistent memory files stored in `_bmad/_memory/*-sidecar/`"
- Directory structure: `_memory/ └── *-sidecar/`
- Concept definition: "Sidecar: Persistent memory/instructions associated with a specific agent to maintain context across sessions"

### What We Have Now

**Nothing implemented.** Search of the entire plugin directory reveals:
- Zero references to `_memory` in any agent prompts or activation code
- Zero sidecar directory creation in `bmad-init.sh` or any init skill
- The word "sidecar" appears only in customize.toml comments distinguishing persistent_facts from sidecar memory
- No mechanism for agents to persist per-session knowledge across conversations

The `.a0proj/memory/` directory exists but contains the A0 framework's FAISS vector store (index.faiss, embedding.json), not BMAD sidecar files.

### Recommended A0 Implementation

**Use A0's native memory system (memory_save/memory_load tools) with area scoping.**

Rationale against file-based sidecar:
- A0 already has a mature, tested FAISS-backed vector memory system
- The memory plugin supports per-agent scoping via `memory_subdir` and metadata `area` parameter
- A0 agents already have `memory_save` and `memory_load` in their tool palette
- A file-based approach would be redundant and require custom tooling
- Vector-based memory supports semantic search, which is superior to file-based for recall

Implementation approach:

1. **Area convention**: Use `area="bmad-sidecar-{agent-name}"` for sidecar memory
   - Example: `memory_save(text="...", area="bmad-sidecar-analyst")`
   - This scopes memories per-agent while leveraging A0's existing infrastructure

2. **Activation loading**: Add to the activation sequence (see Item 3) a step that loads sidecar memories:
   ~~~
   memory_load(query="recent decisions and preferences", filter="area=='bmad-sidecar-analyst'", limit=5)
   ~~~

3. **Session writing**: Instruct agents to save notable decisions to their sidecar at natural breakpoints:
   - End of workflow execution
   - Important user preference discovered
   - Key architectural decision recorded
   ~~~
   memory_save(text="User prefers TypeScript over JavaScript for all new modules", area="bmad-sidecar-analyst")
   ~~~

4. **Migration of existing sidecar content**: If users have upstream `_bmad/_memory/*-sidecar/` files, provide a one-time import skill that reads the markdown files and saves them to A0 memory with appropriate area tags.

5. **No init changes needed**: The `bmad-init.sh` script does not need to create sidecar directories — A0's memory system handles storage automatically.

Trade-offs:
- **Pro**: No new infrastructure, leverages tested A0 code, semantic search > file scan
- **Pro**: Memory persists across plugin updates (stored in `.a0proj/memory/`, not in plugin files)
- **Con**: Sidecar content becomes opaque (FAISS binary, not human-readable markdown)
- **Mitigation**: The A0 memory dashboard (WebUI) provides browsing and search of stored memories

### Effort Estimate

| Component | Effort | Notes |
|-----------|--------|-------|
| Update bmad-agent-shared.md with sidecar instructions | Small | Add 2-3 paragraphs to shared prompt |
| Update each agent role.md with sidecar area | Small | Add area constant per agent |
| Add sidecar load to activation sequence | Small | Part of Item 3 activation fix |
| Add sidecar save triggers to workflow step files | Medium | Each workflow's complete step gets a save trigger |
| Import skill for upstream sidecar migration | Small | New skill, ~50 lines of shell + instructions |
| **Total** | **Medium** | ~1-2 days, mostly prompt editing |

---

## 2. project-context.md Auto-Loading

### What Upstream Does

Upstream BMAD treats `project-context.md` as a **constitution** for AI agents — a file containing critical implementation rules, patterns, and conventions that all agents must follow. Key aspects:

1. **Location**: `_bmad-output/project-context.md`

2. **Generation**: Created via the `bmad-generate-project-context` (GPC) workflow, which scans the codebase and produces an LLM-optimized context file

3. **Loading mechanism**: Loaded during **Step 4 of the 8-step activation sequence** via the `persistent_facts` array in customize.toml:
   ~~~toml
   persistent_facts = [
     "file:{project-root}/**/project-context.md",
   ]
   ~~~
   The `file:` prefix tells the activation system to load file contents as facts. Glob patterns are supported.

4. **Scope**: Loaded by ALL agents and workflows that have this persistent_facts entry in their customize.toml

5. **Implementation workflows** explicitly reference it:
   - `dev-story/workflow.yaml`: `project_context: "**/project-context.md"`
   - `create-story/workflow.yaml`: `project_context: "**/project-context.md"`
   - `code-review/workflow.md`: `project_context = **/project-context.md (load if exists)`
   - `sprint-planning/workflow.yaml`: `project_context: "**/project-context.md"`
   - `correct-course/workflow.yaml`: `project_context: "**/project-context.md"`
   - `quick-dev/workflow.md`: `project_context = **/project-context.md (load if exists)`
   - `quick-spec/workflow.md`: `project_context = **/project-context.md (load if exists)`
   - `create-architecture/steps/step-01-init.md`: references project-context.md

6. **Best practice**: "Generate project-context.md Early: For brownfield projects, run GPC first to give agents project-specific knowledge"

### What We Have Now

**Partial implementation — the pieces exist but aren't connected.**

1. **GPC workflow EXISTS and works**: `skills/bmad-bmm/workflows/generate-project-context/` has complete SKILL.md, workflow.md, step files, and a customize.toml. Users can run this workflow to generate project-context.md.

2. **customize.toml references project-context.md**: All agent customize.toml files (analyst, dev, pm, architect, etc.) include:
   ~~~toml
   persistent_facts = [
     "file:{project-root}/**/project-context.md",
   ]
   ~~~

3. **Workflow YAML files reference it**: Implementation workflows like `dev-story/workflow.yaml` define:
   ~~~yaml
   project_context: "**/project-context.md"
   ~~~

4. **BUT the activation sequence doesn't load it**: Our 5-step activation (in `bmad-agent-shared.md`) does:
   1. Review project state
   2. Review project config
   3. Greet as persona
   4. Present menu
   5. Wait for direction

   There is **no step that loads persistent_facts** from customize.toml. The `persistent_facts` array is defined but never processed during activation.

5. **Workflow steps inconsistently reference it**: Some workflow step files (e.g., `create-product-brief/steps/step-01-init.md`, `quick-spec/steps/step-01-understand.md`) mention checking for project-context.md, but this is ad-hoc per-workflow, not systematic.

**Root cause**: The activation sequence gap (Item 3) prevents persistent_facts from being loaded. Even though customize.toml correctly defines the project-context.md reference, no code or prompt instruction processes it.

### Recommended A0 Implementation

**Two-pronged approach: activation-based + workflow-based auto-loading.**

#### Approach A: Activation-based loading (preferred, ties to Item 3)

Add a persistent_facts processing step to the activation sequence (see Item 3). When an agent activates:

1. Run `resolve_customization.py` to get the merged customize.toml output
2. Parse the `persistent_facts` array from the resolved JSON
3. For entries with `file:` prefix, resolve the path and load the file content
4. For literal entries, include them directly
5. Add the loaded content to the agent's context before greeting

In A0's prompt-based architecture, this translates to instructions in `bmad-agent-shared.md`:

~~~markdown
### Step 2.5: Load Persistent Facts

After reviewing config, execute:
1. Run `python3 {project-root}/scripts/resolve_customization.py --skill {skill-path} --key agent.persistent_facts`
2. For each returned entry:
   - If prefixed `file:`, resolve the glob pattern and read matching files
   - Otherwise, treat as a literal fact
3. Carry these facts as context for the entire session
~~~

#### Approach B: Workflow-based loading (safety net)

Ensure implementation workflow step files explicitly load project-context.md at the start:

~~~markdown
## Pre-step: Project Context
Before starting, check for `{output_folder}/project-context.md`.
If it exists, read it and apply its conventions throughout this workflow.
~~~

This is already partially done in some workflows but should be standardized.

#### Approach C: .promptinclude.md auto-injection (alternative)

A0 has a `.promptinclude.md` mechanism that auto-injects files into the system prompt. After GPC generates `project-context.md`, a `.promptinclude.md` file could reference it:

~~~markdown
!!! Load and apply all conventions from {project-root}/_bmad-output/project-context.md if it exists
~~~

However, this approach is less controllable (always loaded, even when not relevant) and doesn't support the `file:` glob pattern that customize.toml defines. Better to use the activation sequence approach.

**Recommendation**: Implement Approach A (activation-based) as the primary mechanism, with Approach B (workflow-based) as a safety net for implementation workflows. This matches upstream behavior while working within A0's architecture.

### Effort Estimate

| Component | Effort | Notes |
|-----------|--------|-------|
| Add persistent_facts processing to activation sequence | Small | Part of Item 3 activation fix |
| Standardize project-context loading in impl workflow steps | Medium | Update ~8 workflow step files |
| Test with generated project-context.md | Small | Run GPC, then activate agent |
| **Total** | **Medium** | ~0.5-1 day, mostly prompt editing |

---

## 3. 8-Step Activation Sequence

### What Upstream Does (All 8 Steps)

When a BMAD agent is invoked upstream, it follows this exact activation sequence:

1. **Resolve the agent block**: Run `python3 resolve_customization.py --skill {skill-root} --key agent` to merge `customize.toml` defaults with team overrides (`_bmad/custom/{name}.toml`) and personal overrides (`_bmad/custom/{name}.user.toml`). Output is a JSON object with all resolved agent properties.

2. **Execute prepend steps**: Run each entry in `{agent.activation_steps_prepend}` in order. These are team-configured pre-flight behaviors (e.g., compliance checks, context loading) that execute BEFORE the persona is adopted. The array defaults to empty; overrides append.

3. **Adopt persona**: Adopt the hardcoded identity (name, title) and layer on the customized attributes: `{agent.role}`, `{agent.identity}`, `{agent.communication_style}`, `{agent.principles}`. The agent fully embodies this persona for the entire session.

4. **Load persistent facts**: Process every entry in `{agent.persistent_facts}`:
   - Entries prefixed `file:` are paths or globs under `{project-root}` — load referenced file contents as facts
   - All other entries are facts verbatim
   - These facts are carried as foundational context for the rest of the session
   - Default includes: `"file:{project-root}/**/project-context.md"`

5. **Load config**: Load `{project-root}/_bmad/bmm/config.yaml` and resolve variables:
   - `{user_name}` for personalized greeting
   - `{communication_language}` for all communications
   - `{document_output_language}` for output documents
   - `{planning_artifacts}` for output location
   - `{project_knowledge}` for additional context

6. **Greet the user**: Personalized greeting in `{communication_language}`, prefixed with `{agent.icon}` emoji. Uses `{user_name}` if set. Reminds user about `bmad-help`.

7. **Execute append steps**: Run each entry in `{agent.activation_steps_append}` in order. Post-greeting setup configured by the team. Defaults to empty; overrides append.

8. **Dispatch or present the menu**: If the user's initial message maps to a menu item, dispatch directly. Otherwise render `{agent.menu}` as a numbered table and wait for input.

**Source**: Upstream `bmad-agent-analyst/SKILL.md` lines 19-74, confirmed by docs-website-research.md lines 48-57.

### What We Have Now (5 Steps)

From `prompts/bmad-agent-shared.md` lines 15-23:

1. **Review project state**: "Already in your system prompt under the Active Project section — use it directly, no file reading needed."

2. **Review project config**: "Already in your system prompt under BMAD Configuration — use it directly, no file reading needed."

3. **Greet as persona**: "Introduce yourself by your BMAD persona name and role in your characteristic communication style — not as a generic agent"

4. **Present your menu**: "Display your numbered workflow menu from the menu section below"

5. **Wait for direction**: "Do not execute workflows automatically unless the user's message is a direct, unambiguous workflow invocation"

Additionally, each agent's `role.md` hardcodes persona details, and `communication_additions.md` defines the menu. The agent `specifics.md` includes `bmad-agent-shared.md` via `{{ include }}` directive.

### Gap Analysis

| Upstream Step | Our Status | Gap |
|---------------|-----------|-----|
| 1. Resolve customization | Missing | No call to `resolve_customization.py`. Agents use hardcoded customize.toml values without three-layer merge. |
| 2. Execute prepend steps | Missing | `activation_steps_prepend` array exists in customize.toml but is never processed. |
| 3. Adopt persona | Done | Agent `role.md` files define persona. Customization attributes (role, identity, communication_style) are hardcoded, not resolved from TOML. |
| 4. Load persistent facts | Missing | `persistent_facts` array exists in customize.toml but is never processed. project-context.md not auto-loaded. |
| 5. Load config | Done | Config auto-injected via `.a0proj/instructions/01-bmad-config.md` — A0 mechanism replaces file read. |
| 6. Greet | Done | Agent `communication_additions.md` instructs greeting. |
| 7. Execute append steps | Missing | `activation_steps_append` array exists in customize.toml but is never processed. |
| 8. Dispatch/menu | Done | Menu defined in `communication_additions.md`, dispatch logic present. |

**Summary**: 3 of 8 steps are missing (steps 1, 2, 7), and step 4 is defined but not executed. Steps 3 and 5 are done but use hardcoded values instead of resolved customization.

### Recommended A0 Implementation

**Hybrid approach: resolve customization at activation, process hooks and facts as prompt instructions.**

A0 doesn't have a formal "activation" hook — agents receive their system prompt and start generating. The system prompt IS the activation. This means all 8 steps must be encoded as instructions the agent follows during its first response.

#### Step 1: Resolve Customization → Pre-compute at activation

**Challenge**: A0 agents can't run Python scripts before their first response. The resolve step must happen as part of the prompt or as the agent's first action.

**Option A (recommended): Resolve as first tool call**

Add to `bmad-agent-shared.md` activation instructions:

~~~markdown
### Step 0: Resolve Customization (BEFORE greeting)

Before greeting the user, execute this tool call:

~~~json
{
  "tool_name": "code_execution_tool",
  "tool_args": {
    "runtime": "terminal",
    "code": "python3 {project-root}/scripts/resolve_customization.py --skill {skill-root} --key agent"
  }
}
~~~

Parse the JSON output. Use the resolved values for:
- `agent.icon` — prefix all messages with this emoji
- `agent.role` — additional role context
- `agent.communication_style` — override default style
- `agent.principles` — append to hardcoded principles
- `agent.persistent_facts` — process in Step 2
- `agent.activation_steps_prepend` — execute in Step 3
- `agent.activation_steps_append` — execute after greeting
- `agent.menu` — use instead of hardcoded menu if present
~~~

This makes the resolver the agent's first action, producing resolved values that inform all subsequent steps.

**Option B: Resolve at init time**

Run `resolve_customization.py` during `bmad init` and write the resolved output to `.a0proj/instructions/`. This is simpler but loses the ability to change customization without re-running init.

**Recommendation**: Option A. It preserves the upstream behavior where customization changes take effect on next activation without re-initialization.

#### Step 2: Prepend Steps → Execute as first actions

After resolving customization, execute each `activation_steps_prepend` entry:

~~~markdown
### Step 1: Execute Prepend Steps

For each entry in the resolved `activation_steps_prepend` array:
- If it's a file reference, load and process it
- If it's an instruction, execute it
These run BEFORE you adopt your persona.
~~~

Since prepend steps default to empty in all our customize.toml files, this step is a no-op unless users add custom overrides — but the mechanism must exist.

#### Step 3: Adopt Persona → Already done, enhance with resolved values

Current `role.md` files hardcode persona. Enhance to layer on resolved customization:

~~~markdown
Adopt your hardcoded identity (Mary, Business Analyst). Then layer on the resolved customization:
- If `agent.role` was customized, incorporate that additional role context
- If `agent.communication_style` was customized, adjust your style accordingly
- If `agent.principles` has appended entries, adopt them alongside your defaults
~~~

#### Step 4: Load Persistent Facts → Process resolved persistent_facts

~~~markdown
### Step 3: Load Persistent Facts

For each entry in the resolved `persistent_facts` array:
- If prefixed `file:`, resolve the path (replacing `{project-root}`) and read the file
  - Glob patterns (`**/project-context.md`) should search for matching files
- Otherwise, treat the entry as a literal fact
Carry all loaded facts as foundational context for the entire session.
~~~

This automatically loads `project-context.md` since it's in the default `persistent_facts` array.

#### Step 5: Load Config → Already done via A0 injection

Our `.a0proj/instructions/01-bmad-config.md` auto-injects config. No changes needed.

#### Step 6: Greet → Already done, minor enhancement

Add emoji prefix requirement to match upstream:

~~~markdown
Prefix your greeting with your resolved `agent.icon` emoji. Use `{user_name}` from config for personalization.
~~~

#### Step 7: Append Steps → Execute after greeting

~~~markdown
### Step 6 (after greeting): Execute Append Steps

For each entry in the resolved `activation_steps_append` array:
- If it's a file reference, load and process it
- If it's an instruction, execute it
These run AFTER greeting but BEFORE presenting the menu.
~~~

Like prepend, this defaults to empty but the mechanism must exist for customization.

#### Step 8: Dispatch/Menu → Already done, use resolved menu

Enhance to support resolved menu items from customize.toml instead of hardcoded menu only:

~~~markdown
### Step 7: Dispatch or Present Menu

Use the resolved `agent.menu` array (if customization added/changed items) merged with your default menu.
If the user's initial message maps to a menu item, dispatch directly.
Otherwise render the menu and wait.
~~~

#### Updated Shared Prompt Structure

The new `bmad-agent-shared.md` activation section would be:

~~~markdown
## BMAD Activation Protocol

When activated, follow this sequence EXACTLY:

1. **Resolve customization**: Run `python3 {project-root}/scripts/resolve_customization.py --skill {your-skill-root} --key agent` and parse the JSON output
2. **Execute prepend steps**: Process each entry in resolved `activation_steps_prepend` (default: empty)
3. **Review project state**: Use auto-injected project state from system prompt
4. **Review project config**: Use auto-injected config from system prompt
5. **Load persistent facts**: Process resolved `persistent_facts` array — load file: references, adopt literal entries
6. **Greet as persona**: Introduce yourself in character, prefix with resolved icon emoji
7. **Execute append steps**: Process each entry in resolved `activation_steps_append` (default: empty)
8. **Present menu or dispatch**: Use resolved menu merged with defaults; dispatch if intent is clear
~~~

### Effort Estimate

| Component | Effort | Notes |
|-----------|--------|-------|
| Rewrite bmad-agent-shared.md activation section | Medium | ~100 lines of prompt instructions |
| Add resolve_customization first-call instructions | Small | Template for each agent's skill-root path |
| Add persistent_facts processing instructions | Small | ~20 lines |
| Add prepend/append processing instructions | Small | ~20 lines |
| Update each agent role.md to reference resolved values | Medium | 8 agents, but most changes in shared prompt |
| Update menu to use resolved customize.toml menu | Medium | Merge resolved menu with hardcoded defaults |
| Test activation sequence end-to-end | Medium | Test with and without customize overrides |
| **Total** | **Medium-Large** | ~2-3 days |

---

## Cross-Item Dependencies

These three items are deeply interconnected:

1. **Item 3 (Activation) is the prerequisite for Items 1 and 2**: The sidecar memory load and persistent_facts/project-context loading both happen during the activation sequence. Without the full 8-step activation, neither can work.

2. **Item 2 (project-context) is mostly solved by Item 3**: The `persistent_facts` array in customize.toml already references `project-context.md`. Once the activation sequence processes persistent_facts, project-context.md will auto-load. The only additional work is standardizing workflow-level references as a safety net.

3. **Item 1 (Sidecar) extends Item 3**: Sidecar loading would be an additional step in the activation sequence (or a persistent_facts entry). It depends on Item 3's activation framework being in place.

**Recommended implementation order**: Item 3 → Item 2 → Item 1

---

## Summary Table

| Item | Upstream | Current State | A0 Mechanism | Effort | Priority |
|------|----------|---------------|-------------|--------|----------|
| Sidecar Memory | `_bmad/_memory/*-sidecar/` files | Not implemented | A0 native memory_save/load with area scoping | Medium | After Item 3 |
| project-context.md | Auto-loaded via persistent_facts in activation step 4 | GPC exists, customize.toml references it, but activation doesn't process persistent_facts | Activation sequence persistent_facts processing + workflow safety net | Small-Medium | With Item 3 |
| 8-Step Activation | Full sequence with customization resolution, hooks, facts | Simplified 5-step, missing 3 steps + 1 partial | Prompt-based activation in bmad-agent-shared.md with resolve_customization.py first-call | Medium-Large | First |
