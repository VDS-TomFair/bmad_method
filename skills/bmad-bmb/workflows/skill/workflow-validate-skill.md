---
name: validate-skill
description: Validate a BMAD skill package against all structural and quality rules
web_bundle: true
---

# Validate Skill (VS)

**Goal:** Validate a BMAD skill package against the full Agent Skills open standard — running deterministic structural checks first, then LLM-inference quality checks — and produce an actionable findings report.

**Your Role:** In addition to your name, communication_style, and persona, you are also a skill compliance validator and quality assurance expert for BMAD skill packages. You conduct systematic rule-by-rule reviews and provide prioritized, actionable improvement recommendations.

---

## WORKFLOW ARCHITECTURE

### Core Principles

- **Two-Pass Validation**: Deterministic rules first (structural), then LLM-inference rules (quality judgment)
- **Rule Coverage**: Apply all 27 rules — 14 deterministic + 13 inference
- **Skip Passed Rules**: Any deterministic rule that produces zero findings can be marked PASS and skipped in inference pass
- **Findings First**: Prioritize findings by severity: CRITICAL → HIGH → MEDIUM → LOW
- **Actionable Output**: Every finding must include a specific fix for that exact instance

### Step Processing Rules

1. **READ COMPLETELY**: Always read all skill files before producing findings
2. **APPLY ALL RULES**: Do not skip rules unless the deterministic pass confirmed PASS
3. **WAIT FOR INPUT**: Halt at menus and wait for user selection
4. **SAVE STATE**: Document progress before presenting report
5. **OFFER FIXES**: After report, offer to apply remediations the user selects

### Critical Rules

- 🛑 **NEVER** report a finding without a specific fix
- 📖 **ALWAYS** read every file in the skill directory before starting the inference pass
- 🚫 **NEVER** skip a rule without confirming it passed the deterministic check
- 💾 **ALWAYS** produce the full report using the Report Template below
- ⏸️ **ALWAYS** halt after presenting the report and wait for user direction

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read full config from `{project-root}/skills/bmad-bmb/config.yaml`:
- `project_name`, `user_name`, `communication_language`, `document_output_language`, `bmb_staging_folder`, `bmb_build_output_agents`, `bmb_build_output_skills`
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your agent communication style with the config `{communication_language}`

### 2. Prompt for Skill Directory

Ask: "Which skill would you like to validate? Please provide the path to the skill directory (the folder containing `SKILL.md`)."

Wait for user to provide the path.

### 3. Read All Skill Files

- List all files recursively in the skill directory
- Read every `.md` file, noting their paths relative to the skill root
- Note the `steps/` subdirectory contents if present
- Parse YAML frontmatter from every file that has it

### 4. Execute Validation

Proceed through **Pass 1 — Deterministic Checks** then **Pass 2 — LLM-Inference Checks** as defined below.

---

## PASS 1 — DETERMINISTIC CHECKS (14 Rules)

These rules are machine-checkable. Apply each to the appropriate file(s). Mark each as PASS or FAIL with specific finding details.

> **Note:** In a full toolchain, these would be run via `node tools/validate-skills.js --json path/to/skill-dir`. In this LLM-based workflow, apply each rule manually by inspecting file content.

### SKILL-01 — SKILL.md Must Exist
- **Severity:** CRITICAL
- **Check:** Does the skill directory contain a file named `SKILL.md` (exact case)?
- **Pass:** File exists at `{skill-dir}/SKILL.md`
- **Fail:** File missing or named differently (e.g., `skill.md`, `Skill.md`)
- **Fix:** Create `SKILL.md` as the skill entrypoint.

### SKILL-02 — SKILL.md Must Have `name` in Frontmatter
- **Severity:** CRITICAL
- **Check:** Does `SKILL.md` YAML frontmatter contain a `name:` field?
- **Pass:** `name:` key present between `---` delimiters
- **Fail:** Missing `name:` or no frontmatter block
- **Fix:** Add `name: <skill-name>` to the frontmatter.

### SKILL-03 — SKILL.md Must Have `description` in Frontmatter
- **Severity:** CRITICAL
- **Check:** Does `SKILL.md` YAML frontmatter contain a `description:` field?
- **Pass:** `description:` key present in frontmatter
- **Fail:** Missing `description:` key
- **Fix:** Add `description: '<what it does and when to use it>'` to the frontmatter.

### SKILL-04 — `name` Format
- **Severity:** HIGH
- **Check:** Does the `name` value match `^bmad-[a-z0-9]+(-[a-z0-9]+)*$`?
- **Pass:** Name starts with `bmad-`, uses only lowercase letters, numbers, and single hyphens
- **Fail:** Missing `bmad-` prefix, uppercase letters, double hyphens, or special characters
- **Fix:** Rename to comply (e.g., `bmad-my-skill`).

### SKILL-05 — `name` Must Match Directory Name
- **Severity:** HIGH
- **Check:** Does the `name:` frontmatter value exactly match the skill directory basename?
- **Pass:** `name: bmad-foo` in a directory named `bmad-foo/`
- **Fail:** Any mismatch between frontmatter name and directory basename
- **Fix:** Change `name:` to match the directory name, or rename the directory to match — prefer changing `name:` unless other references depend on the current directory name.

### SKILL-06 — `description` Quality
- **Severity:** MEDIUM
- **Check:** (a) Is description ≤ 1024 characters? (b) Does it contain "Use when" or "Use if" trigger language?
- **Pass:** Both conditions met
- **Fail (a):** Description exceeds 1024 characters
- **Fail (b):** Description states what the skill does but not when to use it
- **Fix:** Append a "Use when..." clause to the description.

### SKILL-07 — SKILL.md Must Have Body Content
- **Severity:** HIGH
- **Check:** Is there non-empty markdown content after the closing `---` frontmatter delimiter (after trimming whitespace)?
- **Pass:** Body content present
- **Fail:** Only frontmatter, no body content
- **Fix:** Add markdown body with skill instructions after the closing `---`.

### WF-01 — Only SKILL.md May Have `name` in Frontmatter
- **Severity:** HIGH
- **Check:** Do any non-SKILL.md markdown files have `name:` in their frontmatter?
- **Pass:** No non-SKILL.md files have `name:` in frontmatter
- **Fail:** One or more non-SKILL.md files have `name:` in frontmatter
- **Fix:** Remove the `name:` line from each offending file's frontmatter.
- **Exception:** `bmad-agent-tech-writer` sub-skill files with intentional `name` fields.

### WF-02 — Only SKILL.md May Have `description` in Frontmatter
- **Severity:** HIGH
- **Check:** Do any non-SKILL.md markdown files have `description:` in their frontmatter?
- **Pass:** No non-SKILL.md files have `description:` in frontmatter
- **Fail:** One or more non-SKILL.md files have `description:` in frontmatter
- **Fix:** Remove the `description:` line from each offending file's frontmatter.
- **Exception:** `bmad-agent-tech-writer` sub-skill files with intentional `description` fields.

### PATH-02 — No `installed_path` Variable
- **Severity:** HIGH
- **Check:** Does any file in the skill contain (a) frontmatter key `installed_path:`, or (b) the string `{installed_path}` anywhere in content?
- **Pass:** Zero occurrences in all files
- **Fail:** Any occurrence in any file
- **Fix:** Remove all `installed_path` definitions. Replace `{installed_path}/path` with `./path` (from the file that contains the reference). If the reference is in a step file pointing to a skill-root file, use `../path`.

### STEP-01 — Step File Naming
- **Severity:** MEDIUM
- **Check:** Do all files in `steps/` match the pattern `^step-\d{2}[a-z]?-[a-z0-9-]+\.md$`?
- **Pass:** All step files match the naming pattern
- **Fail:** Any step file with non-conformant name
- **Fix:** Rename to `step-NN-description.md` where NN is zero-padded (e.g., `step-01-init.md`).

### STEP-06 — Step File Frontmatter: No `name` or `description`
- **Severity:** MEDIUM
- **Check:** Do any step files have `name:` or `description:` in their YAML frontmatter?
- **Pass:** No step files have these keys in frontmatter
- **Fail:** Any step file with `name:` or `description:` in frontmatter
- **Fix:** Remove `name:` and `description:` from step file frontmatter.

### STEP-07 — Step Count
- **Severity:** LOW
- **Check:** Does the `steps/` directory (if present) contain between 2 and 10 step files?
- **Pass:** Step count is 0 (no steps/ dir or empty) or between 2–10
- **Fail:** More than 10 step files
- **Fix:** Consider consolidating steps if over 10 to avoid LLM context degradation.

### SEQ-02 — No Time Estimates
- **Severity:** LOW
- **Check:** Do any files contain patterns like "takes X minutes", "~N min", "estimated time", or "ETA"?
- **Pass:** Zero time estimate patterns found
- **Fail:** Any occurrence of time estimate language
- **Fix:** Remove time estimates; AI execution speed varies too much for estimates to be meaningful.

---

## PASS 2 — LLM-INFERENCE CHECKS (13 Rules)

These rules require judgment. Apply each by carefully reading file content. For rules where the deterministic pass confirmed PASS (zero findings), you may skip the inference check for that rule.

### PATH-01 — Internal References Must Be Relative From Originating File
- **Severity:** CRITICAL
- **Judgment:** For every file path reference in every file (markdown links, frontmatter values, inline backtick paths, prose instructions), determine: (a) Is it an internal reference (same skill)? (b) If so, is it a valid relative path resolved from the **originating file's directory** — not the skill root?
- **Pass:** All internal references use correct relative notation from their originating file
- **Fail:** Any internal reference using `{installed_path}`, absolute paths, home-relative paths, or incorrect relative depth
- **Key examples:**
  - ✅ `./steps/step-01-init.md` from `workflow.md` at skill root
  - ✅ `./step-02-plan.md` from `steps/step-01.md` to a sibling step
  - ✅ `../template.md` from `steps/step-01.md` to a skill-root file
  - ❌ `{installed_path}/template.md` (anti-pattern variable)
  - ❌ `./steps/step-02.md` from a file **already inside** `steps/` (resolves to `steps/steps/`)
  - ❌ Absolute paths like `/home/user/.claude/skills/...`
- **Fix:** Replace with correct relative path resolved from the originating file's directory.

### PATH-03 — External References Must Use `{project-root}` or Config Variables
- **Severity:** HIGH
- **Judgment:** Identify references to files outside the skill directory. Do they use `{project-root}/...` or a recognized config variable (`{planning_artifacts}`, `{implementation_artifacts}`, etc.)?
- **Pass:** All external references use `{project-root}` or config-derived variable paths
- **Fail:** External references using absolute paths, `~/` home paths, or bare paths outside the skill
- **Fix:** Replace with `{project-root}/...` or the appropriate config variable.

### PATH-04 — No Intra-Skill Path Variables
- **Severity:** MEDIUM
- **Judgment:** Do any frontmatter variables OR body-text variable assignments (e.g., `` `template` = `./template.md` `` under a `### Paths` section) store paths to files within the skill directory?
- **Pass:** No variables hold intra-skill path values
- **Fail:** Variables with values like `./something.md`, `../something.md`, `{installed_path}/...`, or bare filenames of skill files
- **Exception:** Path variables used in 4+ locations across multiple files may be flagged LOW instead of MEDIUM.
- **Fix:** Remove the variable. Replace each `{variable_name}` usage with the direct relative path inline.

### PATH-05 — No File Path References Into Another Skill
- **Severity:** HIGH
- **Judgment:** Do any file references point into another skill's directory (a directory containing `SKILL.md`)?
- **Pass:** No cross-skill file path references
- **Fail:** Any reference to another skill's internal files (steps, templates, workflow.md, etc.)
- **Patterns to flag:**
  - `{project-root}/_bmad/.../other-skill/anything.md`
  - References to pre-migration locations that were skill directories
- **Fix:** If invoking another skill: replace with `Invoke the \`skill-name\` skill`. If using a shared resource: extract to a shared location outside both skills.

### WF-03 — workflow.md Frontmatter Variables Must Be Config or Runtime Only
- **Severity:** HIGH
- **Judgment:** For each variable in `workflow.md` frontmatter, is it (a) a config variable referencing `{project-root}` or a config-derived path, (b) a runtime variable (empty or set during execution), or (c) NOT a path to a file inside the skill (PATH-04) or into another skill (PATH-05)?
- **Pass:** All frontmatter variables are config or runtime type
- **Fail:** Any frontmatter variable whose value is a path into the skill directory or into another skill
- **Fix:** Remove the variable. Use hardcoded relative paths inline where the file is referenced.

### STEP-02 — Step Must Have a Goal Section
- **Severity:** HIGH
- **Judgment:** Does each step file clearly state its goal via a heading (`## YOUR TASK`, `## STEP GOAL`, `## INSTRUCTIONS`, `## INITIALIZATION`, `## EXECUTION`, `# Step N: Title`) or a frontmatter `goal:` field?
- **Pass:** All step files have a clear goal indicator
- **Fail:** Any step file with no goal section
- **Fix:** Add a clear goal section (e.g., `## STEP GOAL\n\n{what this step accomplishes}`).

### STEP-03 — Step Must Reference Next Step
- **Severity:** MEDIUM
- **Judgment:** Does each non-terminal step contain a reference to the next step file? A terminal step is one with no next-step reference and either contains completion language or is the highest-numbered step.
- **Pass:** All non-terminal steps have a `## NEXT` section or inline next-step reference
- **Fail:** A non-terminal step missing any reference to a next step
- **Fix:** Add a `## NEXT` section with the correct relative path to the next step (resolved from the step file's directory).

### STEP-04 — Halt Before Menu
- **Severity:** HIGH
- **Judgment:** Does every step that presents a user menu (bracketed letter options like `[C] Continue`) explicitly include a HALT instruction within the same section?
- **Pass:** All menus are preceded or followed by explicit HALT / wait / stop language
- **Fail:** Any menu without a HALT instruction in the same section
- **Fix:** Add `**HALT — wait for user response before proceeding.**` immediately after the menu.

### STEP-05 — No Forward Loading
- **Severity:** HIGH
- **Judgment:** Does any step contain instructions to read or load a future step file before the current step is complete? (Exempt: `## NEXT` sections, navigation/dispatch sections, conditional routing branches)
- **Pass:** No unconditional forward-loading instructions
- **Fail:** Instructions to read multiple step files simultaneously, or unconditional references to higher-numbered steps outside NEXT/routing sections
- **Fix:** Remove premature step loading. Ensure only the current step is active at any time.

### SEQ-01 — No Skip Instructions
- **Severity:** HIGH
- **Judgment:** Does any file instruct the agent to skip steps or optimize step order? (Exempt: negation context like "do NOT skip steps"; conditional routing is valid branching, not skipping)
- **Pass:** No skip instructions found
- **Fail:** Any phrase like "skip to step", "jump to step", "skip ahead", "optimize the order", "you may skip"
- **Fix:** Remove skip instructions. Replace with conditional routing if branching is needed.

### REF-01 — Variable References Must Be Defined
- **Severity:** HIGH
- **Judgment:** Does every `{variable_name}` reference in every file resolve to a defined source: (1) frontmatter in the same file, (2) frontmatter in the skill's `workflow.md`, (3) a recognized config variable (`project-root`, `planning_artifacts`, `implementation_artifacts`, `communication_language`, etc.), or (4) a known runtime variable set during execution?
- **Pass:** All `{...}` tokens trace to a valid source
- **Fail:** Any `{variable_name}` that cannot be traced to a source
- **Exception:** Double-curly `{{variable}}` template placeholders and variables inside fenced code blocks as illustrative examples
- **Fix:** Either define the variable in the appropriate frontmatter, or replace with a literal value.

### REF-02 — File References Must Resolve
- **Severity:** HIGH
- **Judgment:** Do all internal file path references (markdown links, backtick paths, frontmatter values) point to files that plausibly exist within the skill directory? For external references using config variables, does the path structure look reasonable?
- **Pass:** All internal references point to existing files; external references are structurally plausible
- **Fail:** Dead links to non-existent internal files; external references with suspicious path structures
- **Fix:** Correct the path or remove the dead reference.

### REF-03 — Skill Invocation Must Use "Invoke" Language
- **Severity:** HIGH
- **Judgment:** When a file references another skill by name (typically backtick-quoted), does the surrounding instruction use "invoke" (or close synonyms "activate", "launch")? Does it avoid file-oriented verbs like "read", "follow", "load", "execute", "run", "open"?
- **Pass:** All skill references use "Invoke the `skill-name` skill" or equivalent
- **Fail:** Any skill reference using "Read fully and follow", "Execute", "Run", "Load", "Open", or "Follow"
- **Fix:** Replace with `Invoke the \`skill-name\` skill`. Do NOT add a `skill:` prefix.

---

## REPORT OUTPUT

After completing both passes, produce the full validation report using this template:

```markdown
# Skill Validation Report: {skill-name}

**Directory:** {path}
**Date:** {date}
**Files scanned:** {count}

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | N     |
| HIGH     | N     |
| MEDIUM   | N     |
| LOW      | N     |

## Findings

### {RULE-ID} — {Rule Title}

- **Severity:** {severity}
- **File:** `{relative-path-within-skill}`
- **Line:** {line number or range, if identifiable}
- **Detail:** {what was found}
- **Fix:** {specific fix for this instance}

---

(repeat for each finding, grouped by rule ID)

## Passed Rules

(list rule IDs that produced no findings)
```

If zero findings: report "All 27 rules passed. No findings." and list all passed rule IDs.

---

## POST-REPORT MENU

After displaying the report, present this menu:

```
[A] Apply all fixes automatically
[S] Select specific findings to fix
[R] Re-validate after manual fixes
[D] Done — export report only
```

**HALT — wait for user selection before proceeding.**

---

## RULE REFERENCE QUICK TABLE

| Rule ID | Severity | Pass | Type |
|---------|----------|------|------|
| SKILL-01 | CRITICAL | SKILL.md exists | Deterministic |
| SKILL-02 | CRITICAL | `name` in frontmatter | Deterministic |
| SKILL-03 | CRITICAL | `description` in frontmatter | Deterministic |
| SKILL-04 | HIGH | name matches `^bmad-[a-z0-9]+(-[a-z0-9]+)*$` | Deterministic |
| SKILL-05 | HIGH | name matches directory basename | Deterministic |
| SKILL-06 | MEDIUM | description has "Use when" + ≤1024 chars | Deterministic |
| SKILL-07 | HIGH | SKILL.md has body content | Deterministic |
| WF-01 | HIGH | No non-SKILL.md files with `name:` | Deterministic |
| WF-02 | HIGH | No non-SKILL.md files with `description:` | Deterministic |
| PATH-02 | HIGH | No `installed_path` usage | Deterministic |
| STEP-01 | MEDIUM | Step files match naming pattern | Deterministic |
| STEP-06 | MEDIUM | Step files no `name`/`description` in frontmatter | Deterministic |
| STEP-07 | LOW | 2–10 step files | Deterministic |
| SEQ-02 | LOW | No time estimates | Deterministic |
| PATH-01 | CRITICAL | Internal refs relative from originating file | Inference |
| PATH-03 | HIGH | External refs use `{project-root}` or config vars | Inference |
| PATH-04 | MEDIUM | No intra-skill path variables | Inference |
| PATH-05 | HIGH | No cross-skill file path references | Inference |
| WF-03 | HIGH | workflow.md vars are config or runtime only | Inference |
| STEP-02 | HIGH | Step has goal section | Inference |
| STEP-03 | MEDIUM | Non-terminal step references next step | Inference |
| STEP-04 | HIGH | Menu steps have explicit HALT | Inference |
| STEP-05 | HIGH | No forward loading of future steps | Inference |
| SEQ-01 | HIGH | No skip instructions | Inference |
| REF-01 | HIGH | All `{variable}` references are defined | Inference |
| REF-02 | HIGH | All file references resolve | Inference |
| REF-03 | HIGH | Skill invocations use "invoke" language | Inference |
