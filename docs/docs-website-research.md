# BMAD Method Documentation Website Research

> Compiled from https://docs.bmad-method.org/ on 2026-05-02

---

## 1. Named Agents

**URL:** https://docs.bmad-method.org/explanation/named-agents/

You say "Hey Mary, let's brainstorm," and Mary activates. She greets you by name, in the language you configured, with her distinctive persona. She reminds you that `bmad-help` is always available. Then she skips the menu entirely and drops straight into brainstorming — because your intent was clear.

This page explains what's actually happening and why BMad is designed this way.

### The Three-Legged Stool

BMad's agent model rests on three primitives that compose:

| Primitive | What it provides | Where it lives |
| --- | --- | --- |
| **Skill** | Capability — a discrete thing the assistant can do (brainstorm, draft a PRD, implement a story) | `.claude/skills/{skill-name}/SKILL.md` (or your IDE's equivalent) |
| **Named agent** | Persona continuity — a recognizable identity that wraps a menu of related skills with consistent voice, principles, and visual cues | Skills whose directory starts with `bmad-agent-*` |
| **Customization** | Makes it yours — overrides that reshape an agent's behavior, add MCP integrations, swap templates, layer in org conventions | `_bmad/custom/{skill-name}.toml` (committed team overrides) and `.user.toml` (personal, gitignored) |

Pull any leg away and the experience collapses:

- Skills without agents → capability lists the user has to navigate by name or code
- Agents without skills → personas with nothing to do
- No customization → every user gets the same out-of-box behavior, forcing forks for any org-specific need

### What Named Agents Buy You

BMad ships six named agents, each anchored to a phase of the BMad Method:

| Agent | Phase | Module |
| --- | --- | --- |
| 📊 **Mary**, Business Analyst | Analysis | market research, brainstorming, product briefs, PRFAQs |
| 📚 **Paige**, Technical Writer | Analysis | project documentation, diagrams, doc validation |
| 📋 **John**, Product Manager | Planning | PRD creation, epic/story breakdown, implementation readiness |
| 🎨 **Sally**, UX Designer | Planning | UX design specifications |
| 🏗️ **Winston**, System Architect | Solutioning | technical architecture, alignment checks |
| 💻 **Amelia**, Senior Engineer | Implementation | story execution, quick-dev, code review, sprint planning |

They each have a hardcoded identity (name, title, domain) and a customizable layer (role, principles, communication style, icon, menu). You can rewrite Mary's principles or add menu items; you cannot rename her — that is deliberate. Brand recognition survives customization so "hey Mary" always activates the analyst, regardless of how a team has shaped her behavior.

### The Activation Flow

When you invoke a named agent, eight steps run in order:

1. **Resolve the agent block** — merge the shipped `customize.toml` with team and personal overrides, via a Python resolver using stdlib `tomllib`
2. **Execute prepend steps** — any pre-flight behavior the team configured
3. **Adopt persona** — hardcoded identity plus customized role, communication style, principles
4. **Load persistent facts** — org rules, compliance notes, optionally files loaded via a `file:` prefix (e.g., `file:{project-root}/docs/project-context.md`)
5. **Load config** — user name, communication language, output language, artifact paths
6. **Greet** — personalized, in the configured language, with the agent's emoji prefix so you can see at a glance who's speaking
7. **Execute append steps** — any post-greet setup the team configured
8. **Dispatch or present the menu** — if your opening message maps to a menu item, go directly; otherwise render the menu and wait for input

Step 8 is where intent meets capability. "Hey Mary, let's brainstorm" skips rendering because `bmad-brainstorming` is an obvious match for `BP` on Mary's menu. If you say something ambiguous, she asks once, briefly, not as a confirmation ritual. If nothing fits, she continues the conversation normally.

### Why Not Just a Menu?

Menus force the user to meet the tool halfway. Named agents invert it. You say what you want, to whom, in whatever words feel natural. The agent knows who they are and what they do. The menu is still there as a fallback — show it when you're exploring, skip it when you're not.

### Why Not Just a Blank Prompt?

Blank prompts assume you know the magic words. Named agents add structure without closing off freedom. The persona stays consistent, the capabilities are discoverable, and `bmad-help` is always one command away.

### Customization as a First-Class Citizen

Every agent ships a `customize.toml` with sensible defaults. Teams commit overrides to `_bmad/custom/bmad-agent-{role}.toml`. Individuals can layer personal preferences in `.user.toml` (gitignored). The resolver merges all three at activation time with predictable structural rules.

There is also a second customization surface for *cross-cutting* concerns: the central `_bmad/config.toml` and `_bmad/config.user.toml` (both installer-owned) plus `_bmad/custom/config.toml` (team, committed) and `_bmad/custom/config.user.toml` (personal, gitignored) for overrides. This is where the **agent roster** lives — the lightweight descriptors that roster consumers like `bmad-party-mode`, `bmad-retrospective`, and `bmad-advanced-elicitation` read to know who's available and how to embody them.

### The Bigger Idea

Most AI assistants today are either menus or prompts, and both shift cognitive load onto the user. Named agents plus customizable skills let you talk to a teammate who already knows the work, and let your organization shape that teammate without forking.
---

## 2. Party Mode

**URL:** https://docs.bmad-method.org/explanation/party-mode/

Run `bmad-party-mode` and you've got your whole AI team in one room - PM, Architect, Dev, UX Designer, whoever you need. BMad Master orchestrates, picking relevant agents per message. Agents respond in character, agree, disagree, and build on each other's ideas.

The conversation continues as long as you want. Ask follow-ups, push back on answers, redirect the discussion - it's a real back-and-forth with your agents until you're done.

**Good for:**

- Big decisions with tradeoffs
- Brainstorming sessions
- Post-mortems when things go wrong
- Sprint retrospectives and planning

### Examples

**Calling Out Bad Architecture:**

You: "Okay team, our last sprint was a disaster. The authentication service went down three times. Who screwed this up?"

Architect: "The design was sound - distributed authentication with proper fallbacks. If implementation deviated from the spec..."

Dev: "I followed the architecture doc exactly. The spec didn't account for concurrent session invalidation race conditions."

PM: "Both of you missed the bigger issue - we didn't validate session management requirements in the PRD. This is on me for not catching it."

TEA: "And I should've caught this in integration tests. The test scenarios didn't cover concurrent invalidation."

**Creative Brainstorming:**

UX Designer: "Start with progressive disclosure - reveal features as users need them, not all at once in a tutorial."

Storyteller: "What if onboarding was a story? Each step reveals a character's journey - the user IS the hero."

Game Designer: "Building on that - what if the first 'quest' is actually solving a real user problem? They learn by doing something valuable."

**Technical Decision:**

Architect: "Start monolith. Microservices add complexity you don't need at 1000 users."

PM: "Agree. Time to market matters more than theoretical scalability."

Dev: "Monolith with clear module boundaries. We can extract services later if needed."

Better decisions through diverse perspectives. Welcome to party mode.
---

## 3. Preventing Agent Conflicts

**URL:** https://docs.bmad-method.org/explanation/preventing-agent-conflicts/

When multiple AI agents implement different parts of a system, they can make conflicting technical decisions. Architecture documentation prevents this by establishing shared standards.

### Common Conflict Types

**API Style Conflicts:** Without architecture, Agent A uses REST with `/users/{id}`, Agent B uses GraphQL mutations. Result: Inconsistent API patterns, confused consumers. With architecture: ADR specifies "Use GraphQL for all client-server communication" — all agents follow the same pattern.

**Database Design Conflicts:** Without architecture, Agent A uses snake_case column names, Agent B uses camelCase. Result: Inconsistent schema, confusing queries. With architecture: Standards document specifies naming conventions — all agents follow the same patterns.

**State Management Conflicts:** Without architecture, Agent A uses Redux, Agent B uses React Context. Result: Multiple state management approaches, complexity. With architecture: ADR specifies state management approach — all agents implement consistently.

### How Architecture Prevents Conflicts

1. **Explicit Decisions via ADRs** — Every significant technology choice is documented with Context, Options considered, Decision, Rationale, Consequences
2. **FR/NFR-Specific Guidance** — Architecture maps each functional requirement to technical approach (e.g., FR-001: User Management → GraphQL mutations)
3. **Standards and Conventions** — Explicit documentation of directory structure, naming conventions, code organization, testing patterns

### Architecture as Shared Context

~~~
PRD: "What to build"
     ↓
Architecture: "How to build it"
     ↓
Agent A reads architecture → implements Epic 1
Agent B reads architecture → implements Epic 2
Agent C reads architecture → implements Epic 3
     ↓
Result: Consistent implementation
~~~

### Key ADR Topics

| Topic | Example Decision |
| --- | --- |
| API Style | GraphQL vs REST vs gRPC |
| Database | PostgreSQL vs MongoDB |
| Auth | JWT vs Sessions |
| State Management | Redux vs Context vs Zustand |
| Styling | CSS Modules vs Tailwind vs Styled Components |
| Testing | Jest + Playwright vs Vitest + Cypress |

### Anti-Patterns to Avoid

- **Implicit Decisions** — "We'll figure out the API style as we go" leads to inconsistency
- **Over-Documentation** — Documenting every minor choice causes analysis paralysis
- **Stale Architecture** — Documents written once and never updated cause agents to follow outdated patterns

Document decisions that cross epic boundaries. Focus on conflict-prone areas. Update architecture as you learn. Use `bmad-correct-course` for significant changes.
---

## 4. How to Customize BMad

**URL:** https://docs.bmad-method.org/how-to/customize-bmad/

Tailor agent personas, inject domain context, add capabilities, and configure workflow behavior — all without modifying installed files. Your customizations survive every update.

The `bmad-customize` skill is a guided authoring helper for the **per-skill agent/workflow override surface** described in this doc.

### When to Use This

- You want to change an agent's personality or communication style
- You need to give an agent persistent facts to recall (e.g. "our org is AWS-only")
- You want to add procedural startup steps the agent must run every session
- You want to add custom menu items that trigger your own skills or prompts
- Your team needs shared customizations committed to git, with personal preferences layered on top

### Three-Layer Override Model

~~~
Priority 1 (wins): _bmad/custom/{skill-name}.user.toml  (personal, gitignored)
Priority 2:        _bmad/custom/{skill-name}.toml        (team/org, committed)
Priority 3 (last): skill's own customize.toml                    (defaults)
~~~

### Merge Rules (by shape, not by field name)

The resolver applies four structural rules. Field names are never special-cased — behavior is determined purely by the value's shape:

| Shape | Rule |
| --- | --- |
| Scalar (string, int, bool, float) | Override wins |
| Table | Deep merge (recursively apply these rules) |
| Array of tables where every item shares the **same** identifier field (every item has `code`, or every item has `id`) | Merge by that key — matching keys **replace in place**, new keys **append** |
| Any other array (scalars; tables with no identifier; arrays that mix `code` and `id` across items) | **Append** — base items first, then team items, then user items |

**No removal mechanism.** Overrides cannot delete base items. If you need to suppress a default menu item, override it by `code` with a no-op description or prompt.

### Some agent fields are read-only

`agent.name` and `agent.title` live in `customize.toml` as source-of-truth metadata, but the agent's SKILL.md doesn't read them at runtime — they're hardcoded identity. Putting `name = "Bob"` in an override file has no effect.

### Steps

1. **Find the Skill's Customization Surface** — Look at the skill's `customize.toml` in its installed directory
2. **Create Your Override File** — Create `_bmad/custom/{skill-name}.toml` (team) or `.user.toml` (personal)
3. **Customize What You Need** — Override files are **sparse**. Include only the fields you're changing
4. **Personal vs Team** — Team files are committed to git; personal files are gitignored

### Customization Examples

**Scalars (icon, role, identity, communication_style):**

~~~toml
[agent]
icon = "🏥"
role = "Drives product discovery for a regulated healthcare domain."
communication_style = "Precise, regulatory-aware, asks compliance-shaped questions early."
~~~

**Persistent facts, principles, activation hooks (append arrays):**

~~~toml
[agent]
persistent_facts = [
  "Our org is AWS-only -- do not propose GCP or Azure.",
  "All PRDs require legal sign-off before engineering kickoff.",
  "file:{project-root}/docs/compliance/hipaa-overview.md",
]
principles = [
  "Ship nothing that can't pass an FDA audit.",
]
activation_steps_prepend = [
  "Scan {project-root}/docs/compliance/ and load any HIPAA-related documents as context.",
]
activation_steps_append = [
  "Read {project-root}/_bmad/custom/company-glossary.md if it exists.",
]
~~~

**Menu customization (merge by `code`):**

~~~toml
[[agent.menu]]
code = "CE"
description = "Create Epics using our delivery framework"
skill = "custom-create-epics"

[[agent.menu]]
code = "RC"
description = "Run compliance pre-check"
prompt = "Read compliance-checklist.md and report gaps."
~~~

### Workflow Customization

Workflows share the same override mechanism as agents. Their customizable surface lives under `[workflow]` instead of `[agent]`. Fields: `activation_steps_prepend`, `activation_steps_append`, `persistent_facts`, `on_complete`.

### Central Configuration

Per-skill `customize.toml` covers **deep behavior**. A separate surface covers **cross-cutting state** — install answers and the agent roster.

~~~
_bmad/config.toml               (installer-owned)  team scope
_bmad/config.user.toml          (installer-owned)  user scope
_bmad/custom/config.toml        (human-authored)   team overrides (committed to git)
_bmad/custom/config.user.toml   (human-authored)   personal overrides (gitignored)
~~~

Four-Layer Merge:

~~~
Priority 1 (wins): _bmad/custom/config.user.toml
Priority 2:        _bmad/custom/config.toml
Priority 3:        _bmad/config.user.toml
Priority 4 (base): _bmad/config.toml
~~~

### How Resolution Works

On activation, the agent's SKILL.md runs a shared Python script that does the three-layer merge and returns the resolved block as JSON. The script uses the Python standard library's `tomllib` module (no external dependencies), so plain `python3` is enough. Requires Python 3.11+.

---

## 5. Workflow Map

**URL:** https://docs.bmad-method.org/reference/workflow-map/

The BMad Method (BMM) is a module in the BMad Ecosystem, targeted at following the best practices of context engineering and planning. AI agents work best with clear, structured context. The BMM system builds that context progressively across 4 distinct phases - each phase produces documents that inform the next, so agents always know what to build and why.

If at any time you are unsure what to do, the `bmad-help` skill will help you stay on track or know what to do next.

### Phase 1: Analysis (Optional)

Explore the problem space and validate ideas before committing to planning.

| Workflow | Purpose | Produces |
| --- | --- | --- |
| `bmad-brainstorming` | Brainstorm Project Ideas with guided facilitation | `brainstorming-report.md` |
| `bmad-domain-research`, `bmad-market-research`, `bmad-technical-research` | Validate market, technical, or domain assumptions | Research findings |
| `bmad-product-brief` | Capture strategic vision — best when your concept is clear | `product-brief.md` |
| `bmad-prfaq` | Working Backwards — stress-test and forge your product concept | `prfaq-{project}.md` |

### Phase 2: Planning

Define what to build and for whom.

| Workflow | Purpose | Produces |
| --- | --- | --- |
| `bmad-create-prd` | Define requirements (FRs/NFRs) | `PRD.md` |
| `bmad-create-ux-design` | Design user experience (when UX matters) | `ux-spec.md` |

### Phase 3: Solutioning

Decide how to build it and break work into stories.

| Workflow | Purpose | Produces |
| --- | --- | --- |
| `bmad-create-architecture` | Make technical decisions explicit | `architecture.md` with ADRs |
| `bmad-create-epics-and-stories` | Break requirements into implementable work | Epic files with stories |
| `bmad-check-implementation-readiness` | Gate check before implementation | PASS/CONCERNS/FAIL decision |

### Phase 4: Implementation

Build it, one story at a time.

| Workflow | Purpose | Produces |
| --- | --- | --- |
| `bmad-sprint-planning` | Initialize tracking (once per project to sequence the dev cycle) | `sprint-status.yaml` |
| `bmad-create-story` | Prepare next story for implementation | `story-[slug].md` |
| `bmad-dev-story` | Implement the story | Working code + tests |
| `bmad-code-review` | Validate implementation quality | Approved or changes requested |
| `bmad-correct-course` | Handle significant mid-sprint changes | Updated plan or re-routing |
| `bmad-sprint-status` | Track sprint progress and story status | Sprint status update |
| `bmad-retrospective` | Review after epic completion | Lessons learned |

### Quick Flow (Parallel Track)

Skip phases 1-3 for small, well-understood work.

| Workflow | Purpose | Produces |
| --- | --- | --- |
| `bmad-quick-dev` | Unified quick flow — clarify intent, plan, implement, review, and present | `spec-*.md` + code |

### Context Management

Each document becomes context for the next phase. The PRD tells the architect what constraints matter. The architecture tells the dev agent which patterns to follow. Story files give focused, complete context for implementation. Without this structure, agents make inconsistent decisions.

### Project Context

Create `project-context.md` to ensure AI agents follow your project's rules and preferences. This file works like a constitution for your project — it guides implementation decisions across all workflows. This optional file can be generated at the end of Architecture Creation, or in an existing project it can be generated also to capture what's important to keep aligned with current conventions.

**How to create it:**

- **Manually** — Create `_bmad-output/project-context.md` with your technology stack and implementation rules
- **Generate it** — Run `bmad-generate-project-context` to auto-generate from your architecture or codebase

---

## 6. Skills (Commands)

**URL:** https://docs.bmad-method.org/reference/commands/

Skills | BMAD Method

Skip to content

Skills

Skills are pre-built prompts that load agents, run workflows, or execute tasks inside your IDE. The BMad installer generates them from your installed modules at install time. If you later add, remove, or change modules, re-run the installer to keep skills in sync (see

Troubleshooting

).

Skills vs. Agent Menu Triggers

Section titled “Skills vs. Agent Menu Triggers”

BMad offers two ways to start work, and they serve different purposes.

Mechanism

How you invoke it

What happens

Skill

Type the skill name (e.g.

bmad-help

) in your IDE

Directly loads an agent, runs a workflow, or executes a task

Agent menu trigger

Load an agent first, then type a short code (e.g.

DS

)

The agent interprets the code and starts the matching workflow while staying in character

Agent menu triggers require an active agent session. Use skills when you know which workflow you want. Use triggers when you are already working with an agent and want to switch tasks without leaving the conversation.

How Skills Are Generated

Section titled “How Skills Are Generated”

When you run

npx bmad-method install

, the installer reads the manifests for every selected module and writes one skill per agent, workflow, task, and tool. Each skill is a directory containing a

SKILL.md

file that instructs the AI to load the corresponding source file and follow its instructions.

The installer uses templates for each skill type:

Skill type

What the generated file does

Agent launcher

Loads the agent persona file, activates its menu, and stays in character

Workflow skill

Loads the workflow config and follows its steps

Task skill

Loads a standalone task file and follows its instructions

Tool skill

Loads a standalone tool file and follows its instructions

Re-running the installer

If you add or remove modules, run the installer again. It regenerates all skill files to match your current module selection.

Where Skill Files Live

Section titled “Where Skill Files Live”

The installer writes skill files into an IDE-specific directory inside your project. The exact path depends on which IDE you selected during installation.

IDE / CLI

Skills directory

Claude Code

.claude/skills/

Cursor

.cursor/skills/

Windsurf

.windsurf/skills/

Other IDEs

See the installer output for the target path

Each skill is a directory containing a

SKILL.md

file. For example, a Claude Code installation looks like:

.claude/skills/

├── bmad-help/

│   └── SKILL.md

├── bmad-create-prd/

│   └── SKILL.md

├── bmad-agent-dev/

│   └── SKILL.md

└── ...

The directory name determines the skill name in your IDE. For example, the directory

bmad-agent-dev/

registers the skill

bmad-agent-dev

.

How to Discover Your Skills

Section titled “How to Discover Your Skills”

Type the skill name in your IDE to invoke it. Some platforms require you to enable skills in settings before they appear.

Run

bmad-help

for context-aware guidance on your next step.

Quick discovery

The generated skill directories in your project are the canonical list. Open them in your file explorer to see every skill with its description.

Skill Categories

Section titled “Skill Categories”

Agent Skills

Section titled “Agent Skills”

Agent skills load a specialized AI persona with a defined role, communication style, and menu of workflows. Once loaded, the agent stays in character and responds to menu triggers.

Example skill

Agent

Role

bmad-agent-dev

Amelia (Developer)

Implements stories with strict adherence to specs

bmad-pm

John (Product Manager)

Creates and validates PRDs

bmad-architect

Winston (Architect)

Designs system architecture

See

Agents

for the full list of default agents and their triggers.

Workflow Skills

Section titled “Workflow Skills”

Workflow skills run a structured, multi-step process without loading an agent persona first. They load a workflow configuration and follow its steps.

Example skill

Purpose

bmad-product-brief

Create a product brief — guided discovery when your concept is clear

bmad-prfaq

Working Backwards PRFAQ

challenge to stress-test your product concept

bmad-create-prd

Create a Product Requirements Document

bmad-create-architecture

Design system architecture

bmad-create-epics-and-stories

Create epics and stories

bmad-dev-story

Implement a story

bmad-code-review

Run a code review

bmad-quick-dev

Unified quick flow — clarify intent, plan, implement, review, present

See

Workflow Map

for the complete workflow reference organized by phase.

Task and Tool Skills

Section titled “Task and Tool Skills”

Tasks and tools are standalone operations that do not require an agent or workflow context.

BMad-Help: Your Intelligent Guide

bmad-help

is your primary interface for discovering what to do next. It inspects your project, understands natural language queries, and recommends the next required or optional step based on your installed modules.

Example

bmad-help

bmad-help I have a SaaS idea and know all the features. Where do I start?

bmad-help What are my options for UX design?

Other Core Tasks and Tools

The core module includes 11 built-in tools — reviews, compression, brainstorming, document management, and more. See

Core Tools

for the complete reference.

Naming Convention

Section titled “Naming Convention”

All skills use the

bmad-

prefix followed by a descriptive name (e.g.,

bmad-agent-dev

,

bmad-create-prd

,

bmad-help

). See

Modules

for available modules.

Troubleshooting

Section titled “Troubleshooting”

Skills not appearing after install.

Some platforms require skills to be explicitly enabled in settings. Check your IDE’s documentation or ask your AI assistant how to enable skills. You may also need to restart your IDE or reload the window.

Expected skills are missing.

The installer only generates skills for modules you selected. Run

npx bmad-method install

again and verify your module selection. Check that the skill files exist in the expected directory.

Skills from a removed module still appear.

The installer does not delete old skill files automatically. Remove the stale directories from your IDE’s skills directory, or delete the entire skills directory and re-run the installer for a clean set.

---

## 7. Manage Project Context

**URL:** https://docs.bmad-method.org/how-to/project-context/

Manage Project Context | BMAD Method

Skip to content

Manage Project Context

Use the

project-context.md

file to ensure AI agents follow your project’s technical preferences and implementation rules throughout all workflows. To make sure this is always available, you can also add the line

Important project context and conventions are located in [path to project context]/project-context.md

to your tools context or always rules file (such as

AGENTS.md

)

Prerequisites

BMad Method installed

Understanding of your project’s technology stack and conventions

When to Use This

Section titled “When to Use This”

You have strong technical preferences before starting architecture

You’ve completed architecture and want to capture decisions for implementation

You’re working on an existing codebase with established patterns

You notice agents making inconsistent decisions across stories

Step 1: Choose Your Approach

Section titled “Step 1: Choose Your Approach”

Manual creation

— Best when you know exactly what rules you want to document

Generate after architecture

— Best for capturing decisions made during solutioning

Generate for existing projects

— Best for discovering patterns in existing codebases

Step 2: Create the File

Section titled “Step 2: Create the File”

Option A: Manual Creation

Section titled “Option A: Manual Creation”

Create the file at

_bmad-output/project-context.md

:

Terminal window

mkdir

-p

_bmad-output

touch

_bmad-output/project-context.md

Add your technology stack and implementation rules:

---

project_name

:

'

MyProject

'

user_name

:

'

YourName

'

date

:

'

2026-02-15

'

sections_completed

: [

'

technology_stack

'

,

'

critical_rules

'

]

---

# Project Context for AI Agents

## Technology Stack & Versions

-

Node.js 20.x, TypeScript 5.3, React 18.2

-

State: Zustand

-

Testing: Vitest, Playwright

-

Styling: Tailwind CSS

## Critical Implementation Rules

**

TypeScript:

**

-

Strict mode enabled, no

`any`

types

-

Use

`interface`

for public APIs,

`type`

for unions

**

Code Organization:

**

-

Components in

`/src/components/`

with co-located tests

-

API calls use

`apiClient`

singleton — never fetch directly

**

Testing:

**

-

Unit tests focus on business logic

-

Integration tests use MSW for API mocking

Option B: Generate After Architecture

Section titled “Option B: Generate After Architecture”

Run the workflow in a fresh chat:

Terminal window

bmad-generate-project-context

The workflow scans your architecture document and project files to generate a context file capturing the decisions made.

Option C: Generate for Existing Projects

Section titled “Option C: Generate for Existing Projects”

For existing projects, run:

Terminal window

bmad-generate-project-context

The workflow analyzes your codebase to identify conventions, then generates a context file you can review and refine.

Step 3: Verify Content

Section titled “Step 3: Verify Content”

Review the generated file and ensure it captures:

Correct technology versions

Your actual conventions (not generic best practices)

Rules that prevent common mistakes

Framework-specific patterns

Edit manually to add anything missing or remove inaccuracies.

What You Get

Section titled “What You Get”

A

project-context.md

file that:

Ensures all agents follow the same conventions

Prevents inconsistent decisions across stories

Captures architecture decisions for implementation

Serves as a reference for your project’s patterns and rules

Tips

Section titled “Tips”

Best Practices

Focus on the unobvious

— Document patterns agents might miss (e.g., “Use JSDoc on every public class”), not universal practices like “use meaningful variable names.”

Keep it lean

— This file is loaded by every implementation workflow. Long files waste context. Exclude content that only applies to narrow scope or specific stories.

Update as needed

— Edit manually when patterns change, or re-generate after significant architecture changes.

Works for Quick Flow and full BMad Method projects alike.

Next Steps

Section titled “Next Steps”

Project Context Explanation

— Learn more about how it works

Workflow Map

— See which workflows load project context

---

## 8. Established Projects

**URL:** https://docs.bmad-method.org/how-to/established-projects/

Established Projects | BMAD Method

Skip to content

Established Projects

Use BMad Method effectively when working on existing projects and legacy codebases.

This guide covers the essential workflow for onboarding to existing projects with BMad Method.

Prerequisites

BMad Method installed (

npx bmad-method install

)

An existing codebase you want to work on

Access to an AI-powered IDE (Claude Code or Cursor)

Step 1: Clean Up Completed Planning Artifacts

Section titled “Step 1: Clean Up Completed Planning Artifacts”

If you have completed all PRD epics and stories through the BMad process, clean up those files. Archive them, delete them, or rely on version history if needed. Do not keep these files in:

docs/

_bmad-output/planning-artifacts/

_bmad-output/implementation-artifacts/

Step 2: Create Project Context

Section titled “Step 2: Create Project Context”

Recommended for Existing Projects

Generate

project-context.md

to capture your existing codebase patterns and conventions. This ensures AI agents follow your established practices when implementing changes.

Run the generate project context workflow:

Terminal window

bmad-generate-project-context

This scans your codebase to identify:

Technology stack and versions

Code organization patterns

Naming conventions

Testing approaches

Framework-specific patterns

You can review and refine the generated file, or create it manually at

_bmad-output/project-context.md

if you prefer.

Learn more about project context

Step 3: Maintain Quality Project Documentation

Section titled “Step 3: Maintain Quality Project Documentation”

Your

docs/

folder should contain succinct, well-organized documentation that accurately represents your project:

Intent and business rationale

Business rules

Architecture

Any other relevant project information

For complex projects, consider using the

bmad-document-project

workflow. It offers runtime variants that will scan your entire project and document its actual current state.

Step 3: Get Help

Section titled “Step 3: Get Help”

BMad-Help: Your Starting Point

Section titled “BMad-Help: Your Starting Point”

Run

bmad-help

anytime you’re unsure what to do next.

This intelligent guide:

Inspects your project to see what’s already been done

Shows options based on your installed modules

Understands natural language queries

bmad-help I have an existing Rails app, where should I start?

bmad-help What's the difference between quick-flow and full method?

bmad-help Show me what workflows are available

BMad-Help also

automatically runs at the end of every workflow

, providing clear guidance on exactly what to do next.

Choosing Your Approach

Section titled “Choosing Your Approach”

You have two primary options depending on the scope of changes:

Scope

Recommended Approach

Small updates or additions

Run

bmad-quick-dev

to clarify intent, plan, implement, and review in a single workflow. The full four-phase BMad Method is likely overkill.

Major changes or additions

Start with the BMad Method, applying as much or as little rigor as needed.

During PRD Creation

Section titled “During PRD Creation”

When creating a brief or jumping directly into the PRD, ensure the agent:

Finds and analyzes your existing project documentation

Reads the proper context about your current system

You can guide the agent explicitly, but the goal is to ensure the new feature integrates well with your existing system.

UX Considerations

Section titled “UX Considerations”

UX work is optional. The decision depends not on whether your project has a UX, but on:

Whether you will be working on UX changes

Whether significant new UX designs or patterns are needed

If your changes amount to simple updates to existing screens you are happy with, a full UX process is unnecessary.

Architecture Considerations

Section titled “Architecture Considerations”

When doing architecture, ensure the architect:

Uses the proper documented files

Scans the existing codebase

Pay close attention here to prevent reinventing the wheel or making decisions that misalign with your existing architecture.

More Information

Section titled “More Information”

Quick Fixes

- Bug fixes and ad-hoc changes

Established Projects FAQ

- Common questions about working on established projects

---

## 9. Document Sharding Guide

**URL:** https://docs.bmad-method.org/how-to/shard-large-documents/

Document Sharding Guide | BMAD Method

Skip to content

Document Sharding Guide

Use the

bmad-shard-doc

tool if you need to split large markdown files into smaller, organized files for better context management.

Deprecated

This is no longer recommended, and soon with updated workflows and most major LLMs and tools supporting subprocesses this will be unnecessary.

When to Use This

Section titled “When to Use This”

Only use this if you notice your chosen tool / model combination is failing to load and read all the documents as input when needed.

What is Document Sharding?

Section titled “What is Document Sharding?”

Document sharding splits large markdown files into smaller, organized files based on level 2 headings (

## Heading

).

Architecture

Section titled “Architecture”

Before Sharding:

_bmad-output/planning-artifacts/

└── PRD.md (large 50k token file)

After Sharding:

_bmad-output/planning-artifacts/

└── prd/

├── index.md                    # Table of contents with descriptions

├── overview.md                 # Section 1

├── user-requirements.md        # Section 2

├── technical-requirements.md   # Section 3

└── ...                         # Additional sections

Steps

Section titled “Steps”

1. Run the Shard-Doc Tool

Section titled “1. Run the Shard-Doc Tool”

Terminal window

/bmad-shard-doc

2. Follow the Interactive Process

Section titled “2. Follow the Interactive Process”

Agent: Which document would you like to shard?

User: docs/PRD.md

Agent: Default destination: docs/prd/

Accept default? [y/n]

User: y

Agent: Sharding PRD.md...

✓ Created 12 section files

✓ Generated index.md

✓ Complete!

How Workflow Discovery Works

Section titled “How Workflow Discovery Works”

BMad workflows use a

dual discovery system

:

Try whole document first

- Look for

document-name.md

Check for sharded version

- Look for

document-name/index.md

Priority rule

- Whole document takes precedence if both exist - remove the whole document if you want the sharded to be used instead

Workflow Support

Section titled “Workflow Support”

All BMM workflows support both formats:

Whole documents

Sharded documents

Automatic detection

Transparent to user

---

## 10. How to Get Answers About BMad

**URL:** https://docs.bmad-method.org/how-to/get-answers-about-bmad/

How to Get Answers About BMad | BMAD Method

Skip to content

How to Get Answers About BMad

Use BMad’s built-in help, source docs, or the community to get answers — from quickest to most thorough.

1. Ask BMad-Help

Section titled “1. Ask BMad-Help”

The fastest way to get answers. The

bmad-help

skill is available directly in your AI session and handles over 80% of questions — it inspects your project, sees what you’ve completed, and tells you what to do next.

bmad-help I have a SaaS idea and know all the features. Where do I start?

bmad-help What are my options for UX design?

bmad-help I'm stuck on the PRD workflow

Tip

You can also use

/bmad-help

or

$bmad-help

depending on your platform, but just

bmad-help

should work everywhere.

2. Go Deeper with Source

Section titled “2. Go Deeper with Source”

BMad-Help draws on your installed configuration. For questions about BMad’s internals, history, or architecture — or if you’re researching BMad before installing — point your AI at the source directly.

Clone or open the

BMAD-METHOD repo

and ask your AI about it. Any agent-capable tool (Claude Code, Cursor, Windsurf, etc.) can read the source and answer questions directly.

Example

Q:

“Tell me the fastest way to build something with BMad”

A:

Use Quick Flow: Run

bmad-quick-dev

— it clarifies your intent, plans, implements, reviews, and presents results in a single workflow, skipping the full planning phases.

Tips for better answers:

Be specific

— “What does step 3 of the PRD workflow do?” beats “How does PRD work?”

Verify surprising claims

— LLMs occasionally get things wrong. Check the source file or ask on Discord.

Not using an agent? Use the docs site

Section titled “Not using an agent? Use the docs site”

If your AI can’t read local files (ChatGPT, Claude.ai, etc.), fetch

llms-full.txt

into your session — it’s a single-file snapshot of the BMad documentation.

3. Ask Someone

Section titled “3. Ask Someone”

If neither BMad-Help nor the source answered your question, you now have a much better question to ask.

Channel

Use For

help-requests

forum

Questions

#suggestions-feedback

Ideas and feature requests

Discord:

discord.gg/gk8jAdXWmj

GitHub Issues:

github.com/bmad-code-org/BMAD-METHOD/issues

You!

Stuck

in the queue—

waiting

for who?

The source

is there,

plain to see!

Point

your machine.

Set it free.

It reads.

It speaks.

Ask away—

Why wait

for tomorrow

when you have

today?

—Claude

---

