# BMAD-A0 Architecture Alignment
Version: 1.0  
Date: 2026-03-01  
Architect: Winston 🏗️  
Commissioned by: BMad Master 🧙

---

## Executive Summary

The BMAD Method Framework was originally designed for single-LLM platforms (Claude Desktop, Cursor) where all agents are prompt personas sharing one context window. The A0 port has made significant progress: routing is manifest-driven, all 19 specialist profiles are properly wired, and the `call_subordinate` delegation pattern is correctly used for workflow execution.

**However, one critical capability gap remains unaddressed: Party Mode is listed in the BMad Master menu but has zero implementation.** This is not a design misalignment — it is an unimplemented feature with significant user value.

Beyond the critical gap, five medium-to-low severity alignment opportunities exist: agent memory, CIS inline personas, state atomicity, parallel execution, and skill context efficiency.

**Overall Assessment: GOOD alignment with one critical gap (Party Mode), four medium opportunities, and several areas that are already well-designed for A0.**

---

## Current Architecture (As-Is)

### System Topology

~~~
┌─────────────────────────────────────────────────────────────┐
│                    AGENT ZERO RUNTIME                        │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  BMad Master (bmad-master profile)                   │  │
│  │                                                      │  │
│  │  System Prompt Composition:                          │  │
│  │  ├── agent.system.main.role.md                       │  │
│  │  ├── agent.system.main.communication.md              │  │
│  │  ├── agent.system.main.communication_additions.md    │  │
│  │  ├── agent.system.main.tips.md                       │  │
│  │  ├── 01-bmad-config.md [auto-injected]               │  │
│  │  ├── 02-bmad-state.md [auto-injected]                │  │
│  │  └── BMAD Routing Table [_80_bmad_routing_manifest]  │  │
│  │                                                      │  │
│  │  On request: read bmad-help.csv → match → route      │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │ call_subordinate(profile, message)   │
│                       ▼                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Specialist Agent (e.g. bmad-architect)              │  │
│  │                                                      │  │
│  │  Real Agent instance, own history, own profile       │  │
│  │  System prompt loaded from agents/bmad-*/prompts/    │  │
│  │  + 01-bmad-config.md + 02-bmad-state.md              │  │
│  │                                                      │  │
│  │  On activation:                                      │  │
│  │  └── skills_tool:load → SKILL.md (full file)         │  │
│  │      → reads workflow step files sequentially        │  │
│  │      → writes artifact to planning-artifacts/        │  │
│  │      → manually updates 02-bmad-state.md             │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  PARTY MODE: ❌ Listed in menu, zero implementation         │
│  AGENT MEMORY: ❌ No memory_save/load usage                 │
│  PARALLEL EXECUTION: ❌ All workflows sequential            │
└─────────────────────────────────────────────────────────────┘
~~~

### Key A0 Capabilities In Use (Correctly)

| Capability | Implementation | Assessment |
|------------|---------------|------------|
| `call_subordinate` delegation | BMad Master → specialist via profile | ✅ Correct |
| Separate agent contexts | Each specialist is real Agent instance | ✅ Correct |
| Routing manifest extension | `_80_bmad_routing_manifest.py` phase-aware injection | ✅ Well-designed |
| `skills_tool:load` | Specialists load SKILL.md on activation | ✅ Correct |
| `code_execution_tool` | File reads, artifact writes, terminal commands | ✅ Correct |
| State file | `02-bmad-state.md` read by extension, updated after transitions | ✅ Functional |
| Project config | `01-bmad-config.md` path aliases auto-injected | ✅ Correct |
| Agent profiles | 19 specialist profiles, all wired in agent-manifest.csv | ✅ Complete |

### What Is NOT In Use

| Capability | A0 API | Current Status |
|------------|--------|----------------|
| Persistent agent memory | `memory_save/load` | ❌ Not used by any BMAD agent |
| Party Mode real multi-agent | `call_subordinate` × N in sequence | ❌ Menu entry only, no implementation |
| Parallel subordinate calls | Multiple `call_subordinate` | ❌ All sequential |
| A2A communication | `a2a_chat` | ⬜ N/A (same-host use case) |

---

## Target Architecture (To-Be)

### System Topology

~~~
┌─────────────────────────────────────────────────────────────────┐
│                      AGENT ZERO RUNTIME                          │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  BMad Master (Orchestrator)                             │    │
│  │                                                         │    │
│  │  Handles: routing, state, Party Mode orchestration,    │    │
│  │           manifest reads, help, menu display           │    │
│  └──────────────────────┬──────────────────────────────────┘    │
│              ┌──────────┴──────────┐                           │
│    Single workflow     Party Mode                               │
│              │              │                                   │
│              ▼              ▼                                   │
│  ┌─────────────────┐  ┌─────────────────────────────────────┐  │
│  │ Specialist Agent│  │ Party Session Coordinator           │  │
│  │ (real instance) │  │                                     │  │
│  │                 │  │  spawn agent-1 via call_subordinate │  │
│  │ Loads skill,    │  │  spawn agent-2 via call_subordinate │  │
│  │ executes wf,    │  │  spawn agent-N via call_subordinate │  │
│  │ writes artifact │  │  collect responses, present as      │  │
│  │                 │  │  structured discussion              │  │
│  │ memory_save key │  │                                     │  │
│  │ findings at end │  │  Each agent: real isolated context  │  │
│  └─────────────────┘  └─────────────────────────────────────┘  │
│                                                                 │
│  Artifact Layer: filesystem markdown (unchanged, correct)       │
│  State Layer: 02-bmad-state.md + atomic write guard (new)       │
│  Memory Layer: per-specialist memory_save/load (new)            │
└─────────────────────────────────────────────────────────────────┘
~~~

### Target Party Mode Flow

~~~
User: "PM" 
  → BMad Master reads teams/default-party.csv for session
  → Presents topic/question framing to user
  → User provides discussion prompt
  → BMad Master calls each party agent sequentially:
      call_subordinate(profile: bmad-brainstorming-coach, message: "[topic] respond as Carson")
      call_subordinate(profile: bmad-innovation, message: "[topic] respond as Victor")
      ... (inline personas injected directly for path-less agents)
  → Collects all responses
  → Presents formatted discussion: each agent's distinct perspective
  → Offers: "Continue discussion? | New topic? | Dismiss party?"
~~~

---

## Gap Analysis

| # | Area | Current | Target | Gap Severity | Effort |
|---|------|---------|--------|-------------|--------|
| 1 | Party Mode | Menu entry only — no handler | Real `call_subordinate` per agent, sequential collection, formatted discussion | **CRITICAL** | Medium |
| 2 | CIS Inline Personas | 5 agents (Leonardo, Dali, de Bono, Campbell, Jobs) have no A0 profile, no path — referenced in default-party.csv but unroutable | Inline persona injection pattern for path-less agents | **HIGH** | Small |
| 3 | Agent Memory | No `memory_save/load` by any specialist | Key artifact metadata and decisions persisted per specialist | **MEDIUM** | Small-Medium |
| 4 | State Write Atomicity | Manual string writes to 02-bmad-state.md, no guard | Write helper or convention to prevent partial writes | **LOW** | Small |
| 5 | Parallel Phase 4 Execution | All story development sequential | Multiple story subordinates in parallel when stories are independent | **LOW** | Medium |
| 6 | Skill Context Efficiency | Full SKILL.md loaded into context every activation | On-demand workflow file loading after initial step routing | **LOW** | Medium |
| 7 | bmad-sm file tree display | Tree shows empty prompts/ dir | Confirmed NOT a defect — depth limit rendering artifact | **NOTE** | None |

---

## Architectural Decisions

### ADR-001: Party Mode — Real Multi-Agent Implementation

**Status:** Approved — Implement  
**Date:** 2026-03-01

**Context:**  
Party Mode (`PM` command) is listed in the BMad Master menu but has zero implementation. The original BMAD design simulated party mode by having one LLM read agent-manifest.csv and role-play all agents in a single context. A0 provides genuine `call_subordinate` with real agent isolation — this is a fundamentally better capability that should be used.

**Decision:**  
Implement Party Mode as a genuine multi-agent orchestration loop:

1. BMad Master reads the appropriate `teams/default-party.csv` (module-specific or global)
2. User provides discussion topic/question
3. BMad Master iterates the agent list, calling `call_subordinate` for each **profiled agent** (those with A0 profile and path fields populated)
4. For **path-less agents** (Leonardo, Dali, de Bono, Campbell, Jobs — see ADR-002), inject persona inline via prompt, no call_subordinate needed
5. Collect all responses, format as a structured discussion with agent name + icon headers
6. Present to user with continuation options

**Implementation location:**  
`agents/bmad-master/prompts/agent.system.main.communication_additions.md` — add `## PM — Party Mode` section after the `LW` section.

**Party Mode message template to each specialist:**
~~~
You are participating in a BMAD Party Mode discussion session.
Your role: [agent display name] — [agent identity]
Topic: [user topic]
Provide your perspective in character. Be concise (3-5 sentences). 
Do not load skills or execute workflows — this is a discussion, not a task execution.
~~~

**Why this matters:**  
Party Mode is a key differentiator for creative and strategic work — the ability to get genuine multi-perspective analysis (not one LLM pretending to be many) is a compelling capability. Users lose significant value every time they invoke `PM` and nothing happens.

**Alternatives rejected:**  
- Single LLM persona simulation: defeats the purpose of A0's multi-agent capability
- Background parallel calls: A0 `call_subordinate` is sequential by design; parallelism adds coordination complexity without sufficient benefit for conversational sessions

---

### ADR-002: CIS Inline Persona Pattern for Path-Less Agents

**Status:** Approved — Implement  
**Date:** 2026-03-01

**Context:**  
The CIS `default-party.csv` includes 5 agents with **empty `path` fields**:
- Leonardo di ser Piero (Renaissance Polymath)
- Salvador Dali (Surrealist Provocateur)  
- Edward de Bono (Lateral Thinking Pioneer)
- Joseph Campbell (Mythic Storyteller)
- Steve Jobs (Combinatorial Genius)

These are creative personas without dedicated A0 agent directories or profiles. They cannot be routed via `call_subordinate(profile: ...)` because no profile exists. Currently they are silently unroutable.

**Decision:**  
For path-less agents, BMad Master constructs a persona prompt inline and routes to a **default subordinate** (no profile override — uses base Agent Zero) with the persona injected as role context in the message. Example:

~~~
call_subordinate(
  profile: "default",  # or no profile — base agent
  reset: true,
  message: "You are Salvador Dali, Surrealist Provocateur. 
  Identity: [identity from CSV]
  Communication style: [communicationStyle from CSV]
  Principles: [principles from CSV]
  
  Topic: [user topic]
  Respond in character. Be concise (3-5 sentences)."
)
~~~

This gives genuine agent isolation (real subordinate) with inline persona definition.

**Why this matters:**  
The CIS party agents include some of the most creatively distinctive personas (Dali's surrealism, de Bono's lateral thinking). Silently skipping them degrades the party mode experience significantly.

**Implementation:**  
Party Mode handler reads `path` field from CSV. If empty → inline persona pattern. If populated → profile routing pattern (ADR-001).

---

### ADR-003: Specialist Agent Memory Model

**Status:** Recommended — Implement incrementally  
**Date:** 2026-03-01

**Context:**  
A0 provides `memory_save/load` per agent context. No BMAD specialist currently uses this. Each time a specialist is activated via `call_subordinate`, it starts with zero persistent knowledge of prior work. This means:
- Mary (Analyst) re-reads market research files every session
- Winston (Architect) forgets ADRs from previous architecture sessions  
- Murat (Test Architect) has no memory of prior test strategy decisions
- Amelia (Dev) forgets implementation patterns established in previous stories

**Decision:**  
Introduce lightweight specialist memory saves at workflow completion:

| Agent | What to Save | Memory Key Pattern |
|-------|-------------|-------------------|
| Mary (Analyst) | Market research key findings, domain constraints | `analyst:research:[project]` |
| Winston (Architect) | ADRs made, technology decisions, constraints | `architect:decisions:[project]` |
| Murat (Test Architect) | Test strategy summary, risk matrix | `test-arch:strategy:[project]` |
| Amelia (Dev) | Implementation patterns, tech stack choices | `dev:patterns:[project]` |
| John (PM) | PRD key decisions, stakeholder constraints | `pm:decisions:[project]` |

**How to implement:**  
Add memory save as the final step in each specialist's workflow completion prompt:
> "Before finalizing: save key decisions to memory using `memory_save` with text summarizing: artifact produced, key decisions made, constraints identified. Use tag `[agent-name]:[project-name]`."

Add memory load as a step in specialist activation:
> "On activation: call `memory_load` with query `[agent-name]:[project-name]` to retrieve any prior session context."

**Why this matters:**  
Without memory, each specialist session is amnesiac. In a multi-sprint project, Winston needs to remember why certain architectural decisions were made to avoid contradicting them. This is table-stakes for professional-grade specialist behavior.

**Scope:** Implement for core BMM specialists first (Analyst, PM, Architect, Dev, SM). Extend to TEA/CIS specialists in a follow-on sprint.

---

### ADR-004: State Write Atomicity Convention

**Status:** Approved — Low effort, implement alongside ADR-001  
**Date:** 2026-03-01

**Context:**  
The `02-bmad-state.md` file is read by the `_80_bmad_routing_manifest.py` extension on every agent loop iteration. It is updated manually by agents using `code_execution_tool` terminal writes. There is no guard against:
- Partial writes (agent interrupted mid-write)
- Concurrent writes (multiple subordinates updating state simultaneously)
- Invalid state values (misspelled phase names break routing)

**Decision:**  
Define a **State Write Convention** (no new code required):

1. **Always write the full file** — never append partial updates. Write the complete `02-bmad-state.md` content in one `code_execution_tool` call.
2. **Use heredoc pattern** — `cat > /path/02-bmad-state.md << 'EOF'` ensures atomic write at shell level.
3. **Valid phase values** — document the enum: `ready`, `1-analysis`, `2-planning`, `3-solutioning`, `4-implementation`, `bmb`, `cis`. Agents must use only these values.
4. **State write template** — add a canonical template to the state file header comment for agents to copy.

**Why this matters:**  
A corrupted or invalid state file silently breaks phase-aware routing in the extension. The fix costs minutes but prevents subtle bugs that are hard to diagnose.

---

### ADR-005: Parallel Phase 4 Story Execution

**Status:** Deferred — Design only, implement in future sprint  
**Date:** 2026-03-01

**Context:**  
Phase 4 development stories are currently executed sequentially — Bob (SM) creates one story, Amelia (Dev) implements it, repeat. A0 supports multiple simultaneous subordinates (each call_subordinate creates a separate Agent instance). For independent stories, parallel execution could reduce wall-clock time significantly.

**Decision:**  
Defer implementation. Design the target pattern for future reference:

**Target pattern (when implemented):**
~~~
# Bob creates story batch
stories = [story-001, story-002, story-003]  # independent, no deps

# BMad Master or SM spawns parallel dev subordinates
# (requires sequential call_subordinate with reset=true for each)
# then monitors via output files

for story in independent_stories:
    call_subordinate(profile: bmad-dev, reset: true,
                     message: f"Implement {story.path}")
    # A0 does not currently support true async parallel — 
    # sequential calls still give context isolation
~~~

**Constraint identified:** A0's `call_subordinate` is sequential (awaited). True parallelism would require the scheduler subsystem or A2A. This changes the effort estimate from Medium to High.

**Recommendation:** Revisit after core gaps (ADR-001, ADR-002, ADR-003) are implemented. The user value is real but the complexity is non-trivial.

---

### ADR-006: Skill Context Loading Strategy

**Status:** Monitor — No change required now  
**Date:** 2026-03-01

**Context:**  
Specialists load full SKILL.md files via `skills_tool:load` on activation. The bmad-bmm SKILL.md contains 24 workflow trigger entries plus routing instructions. For large skill files, this injects significant token overhead into every specialist's context.

**Decision:**  
Retain current pattern. Rationale:

1. `skills_tool:load` is the correct A0 pattern — it's how skills are designed to work
2. SKILL.md files are reference documents — loading them once per session is correct behavior
3. Context window sizes in current LLMs (100k-200k tokens) make skill files (typically 2-10KB) negligible overhead
4. The alternative (on-demand file loading per workflow step) adds complexity without measurable benefit at current scale

**Revisit trigger:** If SKILL.md files grow beyond 50KB or if specialists exhibit context truncation issues on long workflows, revisit with on-demand loading pattern.

---

## Implementation Roadmap

### Priority 1 — Critical (Do Now)

| # | Task | ADR | Effort | File(s) to Change |
|---|------|-----|--------|-------------------|
| P1-01 | Implement Party Mode handler | ADR-001 | ~2-3h | `agents/bmad-master/prompts/agent.system.main.communication_additions.md` |
| P1-02 | Add inline persona pattern for path-less CIS agents | ADR-002 | ~1h | Same file (part of PM handler) |
| P1-03 | State write atomicity convention | ADR-004 | ~30min | `agents/bmad-master/prompts/agent.system.main.communication_additions.md` + state file template comment |

### Priority 2 — High Value (Next Sprint)

| # | Task | ADR | Effort | File(s) to Change |
|---|------|-----|--------|-------------------|
| P2-01 | Add memory save to workflow completion for core BMM specialists | ADR-003 | ~2h | Each specialist's `communication_additions.md` or `role.md` |
| P2-02 | Add memory load to specialist activation protocol | ADR-003 | ~1h | Same files |
| P2-03 | Document valid phase enum in state file header | ADR-004 | ~15min | `02-bmad-state.md` template |

### Priority 3 — Future Sprint

| # | Task | ADR | Effort | Notes |
|---|------|-----|--------|-------|
| P3-01 | Parallel Phase 4 story execution | ADR-005 | High | Requires scheduler integration or A2A |
| P3-02 | Extend memory model to TEA/CIS specialists | ADR-003 | Medium | After BMM memory proven |

---

## What Stays the Same

These aspects of the current implementation are **correctly aligned** with A0 and should not change:

| Area | Why It's Right |
|------|---------------|
| `call_subordinate` delegation pattern | Creates real Agent instances with genuine isolation — exactly correct |
| `_80_bmad_routing_manifest.py` extension | Phase-aware CSV injection into extras_temporary is the right pattern for dynamic context |
| `skills_tool:load` for workflow execution | Correct A0 skill usage |
| Filesystem-based artifact handoff | Markdown files on shared filesystem is simple, debuggable, and correct for A0 |
| 19-profile agent registry | All specialists have proper A0 profiles with correct prompts |
| Manifest-driven routing (bmad-help.csv) | CSV-as-source-of-truth with mandatory read before routing — correct and maintainable |
| Auto-injected config + state files | Correct use of A0's project instruction injection |
| Sequential workflow execution within specialist | Within a single specialist session, sequential step execution is correct |
| bmad-sm/prompts/ content | Confirmed present — 4 files. File tree display artifact only. |

---

## Appendix: Evidence Base

### A1. call_subordinate Verified Behavior
Source: `/a0/python/tools/call_subordinate.py`
- Creates real `Agent` instance via `initialize_agent()`
- Sets `config.profile` from `profile` kwarg — genuine profile switching
- Calls `subordinate.monologue()` — real autonomous execution
- Calls `subordinate.history.new_topic()` after — history compression for long sessions
- One subordinate slot per superior: `Agent.DATA_NAME_SUBORDINATE` is a single reference. Parallel calls require sequential reset=true cycles, not true concurrency.

### A2. Party Mode Current State
Source: grep of all bmad-master prompts
- `PM` appears 4 times in `communication_additions.md`
- All 4 occurrences are: menu listing, exclusion from routing rules, delegation rule mention, never-implemented handler
- **Zero implementation of what PM actually does**

### A3. CIS Path-Less Agent Inventory
Source: `/a0/skills/bmad-cis/teams/default-party.csv`

| Agent Name | Display Name | Has Path | A0 Profile |
|------------|-------------|----------|------------|
| brainstorming-coach | Carson | ✅ bmad/cis/agents/brainstorming-coach.md | `bmad-brainstorming-coach` |
| creative-problem-solver | Dr. Quinn | ✅ | `bmad-problem-solver` |
| design-thinking-coach | Maya | ✅ | `bmad-design-thinking` |
| innovation-strategist | Victor | ✅ | `bmad-innovation` |
| presentation-master | Spike | ✅ | `bmad-presentation` |
| storyteller | Sophia | ✅ | `bmad-storyteller` |
| renaissance-polymath | Leonardo | ❌ empty | None |
| surrealist-provocateur | Salvador Dali | ❌ empty | None |
| lateral-thinker | Edward de Bono | ❌ empty | None |
| mythic-storyteller | Joseph Campbell | ❌ empty | None |
| combinatorial-genius | Steve Jobs | ❌ empty | None |

### A4. bmad-sm Prompts — Confirmed Not Defect
File tree shows `agents/bmad-sm/prompts/` with no files listed and no `# limit reached` note.
Actual `ls -la /a0/agents/bmad-sm/prompts/` confirms: 4 files present.
- `agent.system.main.communication_additions.md` (1645 bytes)
- `agent.system.main.communication.md` (9455 bytes)
- `agent.system.main.role.md` (5516 bytes)
- `agent.system.main.tips.md` (1642 bytes)

**Root cause:** The file tree scan processes agents alphabetically. `bmad-sm` appears after many agents already at depth limit. The tree renderer stops listing prompts/ contents without the `# limit reached` annotation because the directory itself is rendered at the depth boundary. This is a display artifact in the tree scanner, not a missing file defect.

