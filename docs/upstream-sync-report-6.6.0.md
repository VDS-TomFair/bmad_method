# Upstream Sync Report: BMAD-METHOD v6.6.0 → A0 Plugin v1.0.8

**Date**: 2026-05-01  
**Upstream**: 88b9a1c → 9debc16 (v6.6.0)  
**Plugin**: v1.0.8  
**Files Changed Upstream**: 37 (3422 insertions, 312 deletions)

---

## Executive Summary

The v6.6.0 upstream release includes 6 categories of changes affecting our plugin. Three workflow step files need content sync, a config migration (project_name from bmm → core) is required, and one new core skill (bmad-customize) is entirely missing from our plugin. The CSV schema was corrected upstream and our CSVs need alignment verification.

---

## 1. Changes Our Plugin Already Covers (Needs Content Sync)

### 1.1 step-02-design-epics.md — Brownfield Epic Scoping (PRIORITY: HIGH)

**Location**: `skills/bmad-bmm/workflows/3-solutioning/create-epics-and-stories/steps/step-02-design-epics.md`

| Aspect | Our Plugin | Upstream v6.6.0 |
|--------|-----------|-----------------|
| EPIC DESIGN PRINCIPLES | 5 principles (ends with #5 Dependency-Free) | 6 principles — added **#6 Implementation Efficiency** |
| Step A name | "Identify User Value Themes" | "Assess Context and Identify Themes" (added brownfield context assessment) |
| Step B | Propose Epic Structure only | Propose Epic Structure **per epic, considering file overlap** |
| Step C | Missing | **NEW: Review for File Overlap** — detects when multiple epics target same core files |
| Wrong Examples | No file-churn examples | **Added: File Churn wrong example** (3 epics touching same model/controller/web) |
| Correct Alternative | Missing | **Added: consolidation example** with rationale |

**Upstream added content** (needs merging into our file with our YAML frontmatter preserved):

~~~markdown
6. **Implementation Efficiency**: Consider consolidating epics that all modify the same core files into fewer epics

**❌ WRONG Epic Examples (File Churn on Same Component):**
- Epic 1: File Upload (modifies model, controller, web form, web API)
- Epic 2: File Status (modifies model, controller, web form, web API)
- Epic 3: File Access permissions (modifies model, controller, web form, web API)
- All three epics touch the same files — consolidate into one epic with ordered stories

**✅ CORRECT Alternative:**
- Epic 1: File Management Enhancement (upload, status, permissions as stories within one epic)
- Rationale: Single component, fully pre-designed, no feedback loop between epics
~~~

Step A changed to:
~~~markdown
**Step A: Assess Context and Identify Themes**

First, assess how much of the solution design is already validated (Architecture, UX, Test Design).
When the outcome is certain and direction changes between epics are unlikely, prefer fewer but larger epics.
Split into multiple epics when there is a genuine risk boundary or when early feedback could change direction
of following epics.

Then, identify user value themes:
- Look for natural groupings in the FRs
- Identify user journeys or workflows
- Consider user types and their goals
~~~

Step B updated:
~~~markdown
**Step B: Propose Epic Structure**

For each proposed epic (considering whether epics share the same core files):
~~~

New Step C:
~~~markdown
**Step C: Review for File Overlap**

Assess whether multiple proposed epics repeatedly target the same core files. If overlap is significant:
- Distinguish meaningful overlap (same component end-to-end) from incidental sharing
- Ask whether to consolidate into one epic with ordered stories
- If confirmed, merge the epic FRs into a single epic, preserving dependency flow
~~~

### 1.2 step-04-final-validation.md — File Churn Validation (PRIORITY: HIGH)

**Location**: `skills/bmad-bmm/workflows/3-solutioning/create-epics-and-stories/steps/step-04-final-validation.md`

| Aspect | Our Plugin | Upstream v6.6.0 |
|--------|-----------|-----------------|
| Epic Structure Validation | 4 bullet checks | Added **File Churn Check** subsection |
| Final menu | No HALT instruction | Added **HALT — wait for user input** |
| On Complete hook | Missing | **Added: resolve_customization.py on_complete hook** |
| Completion action | Invokes bmad-help + state write | Simplified to bmad-help + on_complete hook |

**New content for Epic Structure Validation section 4:**

~~~markdown
- **File Churn Check:** Do multiple epics repeatedly modify the same core files?
  - Assess whether the overlap pattern suggests unnecessary churn or is incidental
  - If overlap is significant: Validate that splitting provides genuine value (risk mitigation, feedback loops, context size limits)
  - If no justification for the split: Recommend consolidation into fewer epics
  - ❌ WRONG: Multiple epics each modify the same core files with no feedback loop between them
  - ✅ RIGHT: Epics target distinct files/components, OR consolidation was explicitly considered and rejected with rationale
~~~

**New HALT instruction:**

~~~markdown
**Present Final Menu:**
**All validations complete!** [C] Complete Workflow

HALT — wait for user input before proceeding.
~~~

**New On Complete hook:**

~~~markdown
## On Complete

Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow.on_complete`

If the resolved `workflow.on_complete` is non-empty, follow it as the final terminal instruction before exiting.
~~~

**Note**: Our version has a "Workflow Completion — State Write" section that upstream doesn't. This is plugin-specific and should be preserved.

### 1.3 step-07-validation.md — Architecture Checklist Fix (PRIORITY: MEDIUM)

**Location**: `skills/bmad-bmm/workflows/3-solutioning/create-architecture/steps/step-07-validation.md`

| Aspect | Our Plugin | Upstream v6.6.0 |
|--------|-----------|-----------------|
| Checklist items | Pre-checked `[x]` | **Unchecked `[ ]`** — must validate to check |
| Overall Status | Hard-coded `READY FOR IMPLEMENTATION` | **Conditional**: based on checklist completion |
| Conditional logic | None | 3-tier: READY / READY WITH MINOR GAPS / NOT READY |
| Section headers | `**✅ Requirements Analysis**` | `**Requirements Analysis**` (no checkmark) |

**Our checklist** (pre-checked, unconditional):
~~~markdown
**✅ Requirements Analysis**
- [x] Project context thoroughly analyzed
- [x] Scale and complexity assessed
...
**Overall Status:** READY FOR IMPLEMENTATION
~~~

**Upstream checklist** (unchecked, conditional):
~~~markdown
Mark each item `[x]` only if validation confirms it; leave `[ ]` if it is missing, partial, or unverified. Any unchecked item must be reflected in the Gap Analysis above and in the Overall Status below.

**Requirements Analysis**
- [ ] Project context thoroughly analyzed
- [ ] Scale and complexity assessed
...

### Architecture Readiness Assessment

**Overall Status:** {{READY FOR IMPLEMENTATION | READY WITH MINOR GAPS | NOT READY}} (choose READY FOR IMPLEMENTATION only when all 16 checklist items are `[x]` and no Critical Gaps remain; choose NOT READY when any Critical Gap is open or any Requirements Analysis or Architectural Decisions item is unchecked; otherwise READY WITH MINOR GAPS)
~~~

**Note**: Our version has a "Step Complete" section at the bottom that upstream doesn't. This is plugin-specific and should be preserved.

---

## 2. Config Migration: project_name (PRIORITY: HIGH)

### Current State
- **Our core config.yaml** (`skills/bmad-init/core/config.yaml`): Does NOT have `project_name`
- **Our bmm config.yaml** (`skills/bmad-bmm/config.yaml`): HAS `project_name: 