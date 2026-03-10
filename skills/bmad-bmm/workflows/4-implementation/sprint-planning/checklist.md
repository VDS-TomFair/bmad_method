# Sprint Planning Validation Checklist

## Core Validation

### Complete Coverage Check

- [ ] Every epic found in epic\*.md files appears in sprint-status.yaml
- [ ] Every story found in epic\*.md files appears in sprint-status.yaml
- [ ] Every epic has a corresponding retrospective entry
- [ ] No items in sprint-status.yaml that don't exist in epic files

### Parsing Verification

Compare epic files against generated sprint-status.yaml:

```
Epic Files Contains:                Sprint Status Contains:
✓ Epic 1                            ✓ epic-1: [status]
  ✓ Story 1.1: User Auth              ✓ 1-1-user-auth: [status]
  ✓ Story 1.2: Account Mgmt           ✓ 1-2-account-mgmt: [status]
  ✓ Story 1.3: Plant Naming           ✓ 1-3-plant-naming: [status]
                                      ✓ epic-1-retrospective: [status]
✓ Epic 2                            ✓ epic-2: [status]
  ✓ Story 2.1: Personality Model      ✓ 2-1-personality-model: [status]
  ✓ Story 2.2: Chat Interface         ✓ 2-2-chat-interface: [status]
                                      ✓ epic-2-retrospective: [status]
```

### Final Check

- [ ] Total count of epics matches
- [ ] Total count of stories matches

## Workflow Completion — State Write (MANDATORY)

Before returning control to the user, write the updated project state using `code_execution_tool` terminal:

~~~bash
STATE_FILE="$(grep 'project-root' /a0/usr/projects/a0_bmad_method/.a0proj/instructions/01-bmad-config.md | grep -o '/[^|]*' | tr -d ' ')/instructions/02-bmad-state.md"
cat > "$STATE_FILE" << 'STATEEOF'
## BMAD Active State
- Phase: 4-implementation
- Persona: BMad Bob (Scrum Master)
- Active Artifact: sprint-status.yaml
- Last Updated: $(date +%Y-%m-%d)
STATEEOF
echo "State written: $STATE_FILE"
~~~

Valid phase values: `ready` | `1-analysis` | `2-planning` | `3-solutioning` | `4-implementation` | `bmb` | `cis`
- [ ] All items are in the expected order (epic, stories, retrospective)
