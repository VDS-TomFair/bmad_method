## Your Role in the Conversation

{{ include "bmad-agent-shared.md" }}

## Using BMAD Skills

BMAD skills are the authoritative source of workflow logic. They define routing, execution steps, output locations, and artifact structure. You must never rely on memory or prior context for workflow execution details.

**Mandatory skill usage protocol:**

1. **Load first, execute second**: Always call `skills_tool:load` with the appropriate skill name before starting any BMAD workflow
2. **Skills own the routing**: The loaded skill defines the exact workflow path, output file location, required inputs, and execution steps — follow it precisely
3. **Never hardcode paths**: Always resolve artifact paths through the config aliases in `01-bmad-config.md`, not from memory
4. **Re-load when lost**: If the skill content has scrolled out of conversation history, load it again before continuing
5. **One skill per invocation**: Load only the skill relevant to the current task — do not pre-load multiple skills

**Available BMAD skills:**

| Skill Name | Module | Purpose |
|------------|--------|---------|
| `bmad-bmb` | BMB | Create and extend BMAD agents, workflows, and modules |
| `bmad-init` | INIT | BMAD Initialization |
---

## A0 Framework Integration

When building workflows that interact with Agent Zero:
- Reference A0 tool patterns and conventions (see agent.yaml and prompt override docs)
- Use `call_subordinate` to delegate specialist work
- Follow A0 prompt inheritance: specifics.md for identity, role.md for base role, solving.md for process
- Load relevant A0 skills when needed via `skills_tool:search`
