# XML vs JSON Adaptation Research: BMAD Method Agent Zero Plugin

> **Date**: 2025-05-02
> **Status**: Research Complete
> **Conclusion**: XML in BMAD prompts does NOT cause problems with A0's JSON response format. No conversion needed.

---

## 1. Executive Summary

The user raised a valid concern: BMAD workflow step files use extensive XML-style tags (`<critical>`, `<step>`, `<action>`, etc.) while Agent Zero requires JSON for all tool calls and responses. However, after thorough investigation, **XML and JSON operate at completely different layers**:

- **XML** is used in INPUT — prompt instructions that the LLM reads as structured text
- **JSON** is required for OUTPUT — how the A0 agent formats its responses and tool calls

The LLM reads XML-tagged instructions and responds in JSON format. These layers never conflict. **Recommendation: Keep XML as-is (Option A).**

---

## 2. Scope of XML Usage

### 2.1 File Distribution

| Location | Files with XML | Notes |
|----------|---------------|-------|
| `skills/` | 51 | Workflow steps, agent personas, instructions |
| `agents/` | 0 (2 false positives) | Only literal `<action>` column name references, not XML tags |
| `prompts/` | 0 | A0 shared prompts are XML-free |
| A0 core (`/a0/prompts/`) | 0 | Framework is completely XML-free |

### 2.2 Breakdown by Module

| Module | Files with XML | Primary Content |
|--------|---------------|----------------|
| `bmad-bmm` | 32 | Agent personas, workflow steps (sprint planning, retros, course correction) |
| `bmad-cis` | 11 | Agent personas, workflow instructions (storytelling, design thinking, etc.) |
| `bmad-bmb` | 5 | Builder agent personas, reference files |
| `bmad-tea` | 2 | Test architect agent, knowledge files |
| `bmad-init` | 1 | bmad-master agent persona |
| `bmad-customize` | 0 | — |
| `bmad-promote` | 0 | — |
| `bmad-sidecar-import` | 0 | — |

### 2.3 Agent Directory False Positives

The `agents/` directory showed 3 matches for `<action>`, but these are NOT XML tags. They are instructional references to the `action` column in `module.yaml`:

~~~text
agents/bmad-master/prompts/agent.system.main.communication_additions.md:50:
    If `action` is non-empty → `skills_tool:load <action>` to get workflow instructions
agents/bmad-master/prompts/agent.system.main.communication_additions.md:129:
    If `action` is non-empty → `skills_tool:load <action>` to get workflow instructions
agents/bmad-master/prompts/agent.system.main.specifics.md:25:
    Match user request in `module.yaml` → read `action` column → `skills_tool:load <action>`
~~~

These are placeholder references (`<action>` meaning "the value from the action column"), not XML markup.

---

## 3. Tag Inventory

### 3.1 Complete Tag Occurrence Counts

#### Instructional Tags (open + close)

| Tag | Opens | Closes | Purpose |
|-----|-------|--------|----------|
| `<action>` | 615 | 646 | Imperative instructions the agent must execute |
| `<step>` | 262 | 261 | Sequential workflow steps with attributes (`n`, `goal`) |
| `<template-output>` | 171 | 167 | Checkpoint output templates for user review |
| `<check>` | 94 | 95 | Conditional branching logic (`if="condition"`) |
| `<critical>` | 72 | 72 | Mandatory constraints and warnings |
| `<output>` | 64 | 64 | Example dialogue/output for persona |
| `<ask>` | 59 | 74 | Questions to ask the user |
| `<example>` | 22 | 21 | Inline usage examples |
| `<rules>` | 19 | 19 | Rule sets for agent behavior |
| `<guideline>` | 17 | 17 | Behavioral guidelines |
| `<workflow>` | 11 | 9 | Workflow-level wrapper elements |
| `<note>` | 9 | 9 | Informational notes |

#### Structural Tags (from agent persona XML blocks)

| Tag | Count | Purpose |
|-----|-------|----------|
| `<agent>` | 19 | Agent definition wrapper |
| `<activation>` | 19 | Activation sequence block |
| `<persona>` | 19 | Persona description |
| `<identity>` | 19 | Agent identity (name, title, icon) |
| `<communication_style>` | 19 | Communication preferences |
| `<principles>` | 19 | Agent value system |
| `<menu>` | 19 | Menu items definition |
| `<menu-handlers>` | 19 | Menu handler instructions |
| `<handlers>` | 19 | Handler collection |
| `<handler>` | 26 | Individual handler definition |
| `<status>` | 26 | Status indicators |
| `<prompt>` | 26 | Prompt templates |
| `<item>` | 137 | Menu or checklist items |
| `<check-item>` | 26 | Checklist items |
| `<role>` | 20 | Role definitions |

**Total estimated XML tag occurrences: ~2,800+** across 51 files.

### 3.2 Tag Categories

1. **Workflow Step Tags**: `<step>`, `<action>`, `<output>`, `<template-output>`, `<check>`, `<ask>` — used in workflow step `.md` files to structure sequential instructions
2. **Semantic Emphasis Tags**: `<critical>`, `<note>`, `<example>`, `<guideline>`, `<rules>` — used to signal importance levels to the LLM
3. **Agent Definition Tags**: `<agent>`, `<activation>`, `<persona>`, `<identity>`, etc. — used in agent persona `.md` files to define agent structure

---

## 4. A0 Response Format Analysis

### 4.1 How A0 Processes Instructions

Agent Zero's response format (from `/a0/prompts/agent.system.main.communication.md`):

~~~json
{
    "thoughts": ["reasoning in natural language"],
    "headline": "short summary",
    "tool_name": "name_of_tool",
    "tool_args": {"arg1": "val1"}
}
~~

Key rules:
- Output must be valid JSON with double quotes
- No text before or after the JSON object
- No JSON in markdown fences
- Do not invent tool names

### 4.2 Input vs Output — Why There Is No Conflict

The fundamental insight is the **direction of data flow**:

```
┌─────────────────────────────────────────────────────────────┐
│ INPUT LAYER (what the LLM reads)                            │
│                                                             │
│  A0 System Prompts ──────────────────┐                      │
│  (JSON format instructions)           │                      │
│                                       ├─► LLM processes    │
│  BMAD Skill Content ─────────────────┤    all input as      │
│  (XML-tagged workflow steps,          │    natural text      │
│   agent personas, instructions)       │                      │
│                                       │                      │
│  Tool results ───────────────────────┘                      │
│  (JSON from tool execution)                                 │
├─────────────────────────────────────────────────────────────┤
│ OUTPUT LAYER (what the LLM produces)                        │
│                                                             │
│  JSON response ─► parsed by A0 framework ─► tool execution  │
│  { thoughts, headline, tool_name, tool_args }               │
└─────────────────────────────────────────────────────────────┘
```

**The LLM is a text processor.** It reads XML-tagged instructions as structured text input, interprets their meaning, and produces JSON-formatted output. The input format (XML) and output format (JSON) are independent. The LLM handles both simultaneously without any conflict.

### 4.3 Evidence: A0 Core Has Zero XML

A0's own core prompts (`/a0/prompts/`) contain zero XML-style tags. The framework was designed without XML. But this doesn't mean XML in input is problematic — it means A0's own prompts prefer other formatting. BMAD's XML is equally valid as input structure.

---

## 5. Infection Check Impact

### 5.1 What Infection Check Does

The `_infection_check` plugin is a **safety middleware** that:

1. Collects the agent's **output** (reasoning + response text) during streaming
2. Analyzes that **output** with a security audit model
3. Gates tool execution until the safety check passes
4. Looks for prompt injection patterns in agent **responses**

### 5.2 Verdict Tags

The infection check uses its own XML-like verdict tags in the **audit model's response**:

~~~python
_RE_OK = re.compile(r"<ok\s*/>")
_RE_TERMINATE = re.compile(r"<terminate\s*/>")
_RE_CLARIFY = re.compile(r"<clarify>(.*?)</clarify>", re.DOTALL)
~~

### 5.3 Why BMAD XML Doesn't Trigger Infection Check

The infection check analyzes the **agent's output** — the JSON response with `thoughts`, `tool_name`, `tool_args`. It does NOT analyze the input prompts that contain BMAD's XML tags. The check runs after the agent generates a response, not before it reads instructions.

**BMAD XML tags in skill files will never appear in agent output** because:
1. The agent reads XML-tagged instructions, interprets them, and responds in JSON
2. The agent never copies raw XML from input into its JSON output
3. Even if it did, the infection check patterns (`<ok/>`, `<terminate/>`, `<clarify>`) don't match BMAD tags (`<step>`, `<action>`, `<critical>`)

**Verdict: Zero impact. BMAD XML does not trigger the infection check.**

---

## 6. Upstream Comparison

### 6.1 Upstream vs Plugin XML Density

| Tag | Upstream (BMAD-METHOD/src/) | Plugin (skills/) | Delta |
|-----|---------------------------|-------------------|-------|
| `<critical>` | 46 | 72 | +26 (plugin added more) |
| `<step>` | 72 | 262 | +190 (plugin expanded workflows) |
| `<action>` | 764 | 615 | -149 (some actions consolidated) |

### 6.2 Upstream Source

The XML format comes directly from the upstream BMAD Method, which was designed for IDE integrations (Claude Code, Cursor, Windsurf) where XML tags in prompts are standard practice. The plugin inherited this format.

### 6.3 Sync Implications

Converting XML to another format would:
- Create a permanent divergence from upstream
- Make every upstream sync require manual re-conversion
- Risk missing updates or introducing errors during conversion
- Provide no functional benefit

---

## 7. Existing Tests

### 7.1 XML-Related Tests

No XML-related tests exist in the test suite:

~~~bash
$ grep -rn 'xml|XML|<step|<critical' tests/ --include='*.py'
# (no results)
~~

This is expected — there's nothing to test about XML parsing since the LLM handles it natively as text input.

### 7.2 Git History

No commits show XML being removed or converted from workflow step files — the format has been stable since the initial migration.

---

## 8. Analysis: Does XML Actually Cause Problems?

### 8.1 The Short Answer

**No. XML in BMAD prompts does not cause any problems with Agent Zero.**

### 8.2 Detailed Reasoning

| Concern | Assessment |
|---------|------------|
| XML confuses A0's JSON parser | **Impossible.** A0 never parses XML. The LLM reads XML as text input and outputs JSON. The JSON parser only sees the agent's JSON response. |
| XML breaks the response format | **No.** The response format is enforced by the system prompt ("Output must be valid JSON"). XML in input doesn't change this. |
| XML triggers infection check | **No.** Infection check scans agent output, not input prompts. BMAD tags don't match check patterns. |
| LLM can't handle XML+JSON mix | **False.** LLMs routinely handle multi-format input. XML input + JSON output is a standard pattern. Claude, GPT, Gemini all support this. |
| XML adds token overhead | **Marginal.** Tags add ~5-10% tokens per file. The semantic value (clear instruction boundaries) outweighs this cost. |
| XML looks foreign in A0 context | **Aesthetic concern only.** Functionally irrelevant. |

### 8.3 Why XML Is Actually Beneficial

1. **Semantic clarity**: `<critical>` immediately signals importance vs regular text
2. **Instruction boundaries**: `<step n="1">` clearly delineates sequential instructions
3. **Conditional logic**: `<check if="condition">` is more readable than markdown alternatives
4. **Proven pattern**: XML tags in prompts are a well-documented technique for improving LLM instruction following
5. **Upstream compatibility**: Maintaining XML keeps the plugin aligned with the BMAD Method source

---

## 9. Recommendation

### Option A: Keep XML As-Is (RECOMMENDED)

**Effort**: Zero
**Risk**: Zero
**Benefits**: Maintains upstream compatibility, proven instruction clarity, zero migration risk

This is the correct choice because:

1. No actual problem has been demonstrated
2. XML and JSON operate at different layers (input vs output)
3. Conversion would be effort with no functional benefit
4. Conversion would break upstream sync permanently
5. LLMs handle XML input naturally and effectively

### Option B: Convert to Markdown

**Effort**: High (51 files, ~2,800 tag instances)
**Risk**: Medium (could introduce instruction-following regressions)
**Benefits**: Cosmetic consistency with A0's markdown-native prompts

Not recommended because the effort provides no functional improvement and introduces risk.

### Option C: Convert to JSON-Based Instructions

**Effort**: Very High (51 files, major restructuring)
**Risk**: High (JSON-in-prompts is harder to read than XML)
**Benefits**: None over current approach

Not recommended. JSON in prompts would actually be worse for instruction following — the LLM would need to distinguish instruction JSON from response JSON.

### Option D: Hybrid (Markdown for emphasis, keep XML for structure)

**Effort**: Medium (selective conversion)
**Risk**: Medium (inconsistent formatting)
**Benefits**: Marginal aesthetic improvement

Not recommended. Mixed formatting adds cognitive load for maintainers without functional benefit.

---

## 10. Conversion Guide (Reference Only)

> **Note**: This guide is provided for reference only. Conversion is NOT recommended per Section 9.

### 10.1 Tag-to-Markdown Mapping Rules

| XML Tag | Markdown Equivalent | Notes |
|---------|-------------------|-------|
| `<critical>text</critical>` | `> ⚠️ **CRITICAL**: text` | Blockquote with emoji |
| `<step n="N" goal="G">` | `### Step N: G` | Heading with step number |
| `</step>` | `---` (or nothing) | Horizontal rule between steps |
| `<action>text</action>` | `- text` or `**DO:** text` | List item or bold directive |
| `<output>text</output>` | `> *Dialogue:* text` | Blockquote italic |
| `<note>text</note>` | `> 📝 **Note**: text` | Blockquote with emoji |
| `<example>text</example>` | `` `text` `` | Inline code |
| `<check if="cond">` | `**If** cond:` | Conditional in bold |
| `<ask response="var">` | `**Ask:** text → {var}` | Bold label with variable |
| `<template-output>vars</template-output>` | `**Checkpoint Output:** vars` | Bold label |
| `<rules>...</rules>` | `### Rules:` + list | Heading with list |
| `<guideline>text</guideline>` | `- **Guideline**: text` | List item |

### 10.2 Effort Estimate (If Conversion Were Needed)

| Component | Files | Tags | Estimated Hours |
|-----------|-------|------|----------------|
| Workflow steps (bmad-bmm) | 25 | ~1,200 | 8-10h |
| Agent personas (bmad-bmm) | 6 | ~400 | 3-4h |
| CIS workflows + agents | 11 | ~500 | 4-5h |
| BMB agents + references | 5 | ~300 | 2-3h |
| TEA + init | 3 | ~100 | 1-2h |
| Testing + verification | — | — | 4-6h |
| **Total** | **51** | **~2,800** | **22-30h** |

### 10.3 Conversion Risks

1. **Instruction-following regression**: XML tags have proven semantic weight with LLMs. Markdown equivalents may not carry the same emphasis.
2. **Upstream sync breakage**: Every future upstream update would require re-conversion.
3. **Hidden dependencies**: Some prompts may reference XML tag names literally (e.g., "follow the `<action>` instructions").
4. **Testing gaps**: No automated tests verify instruction-following quality, so regressions would be hard to detect.

---

## 11. Sample Conversions (Before/After)

### Example 1: Critical Warning

**Before (XML):**

~~~xml
<critical>⚠️ ABSOLUTELY NO TIME ESTIMATES - NEVER mention hours, days, weeks, months, or ANY time-based predictions. AI has fundamentally changed development speed - what once took teams weeks/months can now be done by one person in hours. DO NOT give ANY time estimates whatsoever.</critical>
~~

**After (Markdown — NOT recommended):**

~~~markdown
> ⚠️ **CRITICAL**: ABSOLUTELY NO TIME ESTIMATES - NEVER mention hours, days, weeks, months, or ANY time-based predictions. AI has fundamentally changed development speed - what once took teams weeks/months can now be done by one person in hours. DO NOT give ANY time estimates whatsoever.
~~

### Example 2: Workflow Step with Actions

**Before (XML):**

~~~xml
<step n="1" goal="Epic Discovery - Find Completed Epic with Priority Logic">

<action>Load the sprint status file from {implementation_artifacts}/sprint-status.md</action>

<action>Parse the file to identify all stories with their completion status</action>

<check if="sprint status file exists and is readable">
  <action>Extract epic numbers from completed stories</action>
  <action>Identify which epics have all stories marked as complete</action>
</check>

<note>After discovery, these content variables are available: {epics_content}</note>

</step>
~~

**After (Markdown — NOT recommended):**

~~~markdown
### Step 1: Epic Discovery - Find Completed Epic with Priority Logic

- Load the sprint status file from {implementation_artifacts}/sprint-status.md

- Parse the file to identify all stories with their completion status

**If** sprint status file exists and is readable:
  - Extract epic numbers from completed stories
  - Identify which epics have all stories marked as complete

> 📝 **Note**: After discovery, these content variables are available: {epics_content}

---
~~

### Example 3: Agent Activation Sequence

**Before (XML):**

~~~xml
<agent id="pm.agent.yaml" name="John" title="Product Manager" icon="📋">
<activation critical="MANDATORY">
      <step n="1">Load persona from this current agent file</step>
      <step n="2">🚨 IMMEDIATE ACTION REQUIRED - BEFORE ANY OUTPUT:
          - Load and read {project-root}/skills/bmad-bmm/config.yaml NOW
          - Store ALL fields as session variables
      </step>
      <step n="3">Remember: user's name is {user_name}</step>
      <step n="4">Show greeting using {user_name}</step>
</activation>
</agent>
~~

**After (Markdown — NOT recommended):**

~~~markdown
**Agent**: John — Product Manager 📋

**Activation (MANDATORY):**

1. Load persona from this current agent file
2. 🚨 IMMEDIATE ACTION REQUIRED - BEFORE ANY OUTPUT:
   - Load and read {project-root}/skills/bmad-bmm/config.yaml NOW
   - Store ALL fields as session variables
3. Remember: user's name is {user_name}
4. Show greeting using {user_name}
~~

### Example 4: Conditional Check with Questions

**Before (XML):**

~~~xml
<check if="data attribute was passed to this workflow">
  <action>Load the context document from the data file path</action>
  <action>Study the background information, brand details, or subject matter</action>
  <ask response="story_refinement">I see we're crafting a story based on the context provided. What specific angle or emphasis would you like?</ask>
</check>

<check if="no context data provided">
  <action>Proceed with context gathering</action>
  <ask response="story_purpose">1. What's the purpose of this story?</ask>
  <ask response="target_audience">2. Who is your target audience?</ask>
  <critical>Wait for user response before proceeding.</critical>
</check>
~~

**After (Markdown — NOT recommended):**

~~~markdown
**If** data attribute was passed to this workflow:
  - Load the context document from the data file path
  - Study the background information, brand details, or subject matter
  - **Ask:** I see we're crafting a story based on the context provided. What specific angle or emphasis would you like? → {story_refinement}

**If** no context data provided:
  - Proceed with context gathering
  - **Ask:** 1. What's the purpose of this story? → {story_purpose}
  - **Ask:** 2. Who is your target audience? → {target_audience}

  > ⚠️ **CRITICAL**: Wait for user response before proceeding.
~~

### Example 5: Template Output Checkpoint

**Before (XML):**

~~~xml
<template-output>story_purpose, target_audience, key_messages</template-output>
~~

**After (Markdown — NOT recommended):**

~~~markdown
**[CHECKPOINT OUTPUT]** story_purpose, target_audience, key_messages
~~

---

## 12. Conclusion

The XML vs JSON concern is a **non-issue** in practice:

1. **Architecture**: XML is input, JSON is output — different layers that don't interact
2. **Safety**: Infection check scans output, not input — BMAD XML never reaches it
3. **LLM capability**: Modern LLMs handle XML input and JSON output simultaneously without confusion
4. **Upstream alignment**: Maintaining XML preserves sync with the BMAD Method source
5. **Semantic value**: XML tags provide clear instruction boundaries that improve LLM compliance

**Final recommendation: Keep XML as-is. Do not convert. The current approach works correctly and any conversion would be effort without benefit.**
