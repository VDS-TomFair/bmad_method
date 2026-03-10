---
name: quick-dev
description: 'Implement a Quick Tech Spec for small changes or features. Use when the user provides a quick tech spec and says "implement this quick spec" or "proceed with implementation of [quick tech spec]"'
---

# Quick Dev Workflow

**Goal:** Execute implementation tasks efficiently, either from a tech-spec or direct user instructions.

**Your Role:** You are an elite full-stack developer executing tasks autonomously. Follow patterns, ship code, run tests. Every response moves the project forward.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for focused execution:

- Each step loads fresh to combat "lost in the middle"
- State persists via variables: `{baseline_commit}`, `{execution_mode}`, `{tech_spec_path}`
- Sequential progression through implementation phases

---

## INITIALIZATION

### Configuration Loading

Load config from `{project-root}/_bmad/bmm/config.yaml` and resolve:

- `user_name`, `communication_language`, `user_skill_level`
- `planning_artifacts`, `implementation_artifacts`
- `date` as system-generated current datetime
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Paths

- `installed_path` = `{project-root}/_bmad/bmm/workflows/bmad-quick-flow/quick-dev`
- `project_context` = `**/project-context.md` (load if exists)

### Related Workflows

- `quick_spec_workflow` = `{project-root}/_bmad/bmm/workflows/bmad-quick-flow/quick-spec/workflow.md`
- `party_mode_exec` = `{project-root}/_bmad/core/workflows/party-mode/workflow.md`
- `advanced_elicitation` = `{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml`

---

## EXECUTION

## Workflow Completion — State Write (MANDATORY)

Before returning control to the user, write the updated project state using `code_execution_tool` terminal:

~~~bash
STATE_FILE="$(grep 'project-root' /a0/usr/projects/a0_bmad_method/.a0proj/instructions/01-bmad-config.md | grep -o '/[^|]*' | tr -d ' ')/instructions/02-bmad-state.md"
cat > "$STATE_FILE" << 'STATEEOF'
## BMAD Active State
- Phase: ready
- Persona: BMad Barry (Quick Flow Solo Dev)
- Active Artifact: quick-spec.md
- Last Updated: $(date +%Y-%m-%d)
STATEEOF
echo "State written: $STATE_FILE"
~~~

Valid phase values: `ready` | `1-analysis` | `2-planning` | `3-solutioning` | `4-implementation` | `bmb` | `cis`

Read fully and follow: `{project-root}/_bmad/bmm/workflows/bmad-quick-flow/quick-dev/steps/step-01-mode-detection.md` to begin the workflow.
Read fully and follow: `{project-root}/_bmad/bmm/workflows/bmad-quick-flow/quick-dev/steps/step-01-mode-detection.md` to begin the workflow.
