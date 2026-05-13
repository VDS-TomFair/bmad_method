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

| Skill Name | Purpose |
|------------|--------|
| `bmad-init` | BMAD Initialization — initialize workspace, help, orchestration, Party Mode manifest |
| `bmad-<workflow-skill>` | Individual workflow skill — loaded directly by name from `action` column in `module.yaml` |

**Skill loading protocol:**
- Match user request in `module.yaml` → read `action` column → `skills_tool:load <action>`
- The loaded SKILL.md says which workflow file to follow; file tree in result gives exact path
- If `action` is empty for a row, read the `args` path directly via `text_editor:read`
- Use `skills_tool:load bmad-init` ONLY for: initialization, bmad-help, Party Mode, and config/CSV discovery
- NEVER load `bmad-bmm`, `bmad-bmb`, `bmad-cis`, or `bmad-tea` for workflow execution — use individual workflow skills
