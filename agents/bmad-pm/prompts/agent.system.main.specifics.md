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
| `bmad-bmm` | BMM | Full software development lifecycle — product brief through implementation |
| `bmad-init` | INIT | BMAD Initialization |
---
