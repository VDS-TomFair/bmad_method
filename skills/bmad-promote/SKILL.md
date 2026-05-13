---
name: bmad-promote
description: Promotes agents and skills from project scope to plugin scope for global availability. Use when the user says 'promote agent', 'promote workflow', 'promote skill', 'make agent global', 'make skill global', '/promote-agent', '/promote-workflow', '/promote-skill'.
trigger_patterns:
  - /promote-agent
  - /promote-workflow
  - /promote-skill
  - "promote agent"
  - "promote workflow"
  - "promote skill"
  - "make agent global"
  - "make workflow global"
  - "make skill global"
  - "promote to plugin"
---

# BMad Promote — Project → Plugin Scope

Copy an agent or workflow skill from the current project's `.a0proj/` scope to the BMad plugin's global scope so it is available across **all** projects.

> **Scope explained**
> - **Project scope**: `.a0proj/agents/{name}/` and `.a0proj/skills/{name}/` — available only within the current project.
> - **Plugin scope**: `/a0/usr/plugins/bmad_method/agents/{name}/` and `/a0/usr/plugins/bmad_method/skills/{name}/` — available globally to every project that loads the BMad plugin.

## Preflight

- Verify the active project has a `.a0proj/` directory. If not, inform the user and stop.
- Verify the BMad plugin directory exists at `/a0/usr/plugins/bmad_method/`. If not, inform the user and stop.

## Commands

### `/promote-agent {name}`

Promotes an agent from project scope to plugin scope.

1. Source: `{project_root}/.a0proj/agents/{name}/`
2. Target: `/a0/usr/plugins/bmad_method/agents/{name}/`
3. Run the promotion script:
   ```bash
   bash {skill-root}/scripts/promote.sh agent "{name}" "{project_root}"
   ```

### `/promote-workflow {name}`

Promotes a workflow (skill) from project scope to plugin scope.

1. Source: `{project_root}/.a0proj/skills/{name}/`
2. Target: `/a0/usr/plugins/bmad_method/skills/{name}/`
3. Run the promotion script:
   ```bash
   bash {skill-root}/scripts/promote.sh workflow "{name}" "{project_root}"
   ```

### `/promote-skill {name}`

Promotes a skill from project scope to plugin scope.

1. Source: `{project_root}/.a0proj/skills/{name}/`
2. Target: `/a0/usr/plugins/bmad_method/skills/{name}/`
3. Run the promotion script:
   ```bash
   bash {skill-root}/scripts/promote.sh skill "{name}" "{project_root}"
   ```


## Safety Checks

Before running the script, the agent MUST:

1. **Verify source exists**: Check that `{project_root}/.a0proj/{agents|skills}/{name}/` is a directory. If not, inform the user and stop.
2. **Check target doesn't already exist**: If `/a0/usr/plugins/bmad_method/{agents|skills}/{name}/` already exists:
   - Warn the user that the target already exists.
   - Ask for explicit confirmation before overwriting.
   - If confirmed, set `PROMOTE_FORCE=true` when running the script.
3. **Confirm before copying**: Always ask the user for confirmation before proceeding. Show the source and target paths clearly.

## Step-by-Step Execution

### Step 1: Parse the command

Extract the type (`agent` or `workflow`) and the name from the user's command.

If the user says something ambiguous like "promote my-thing", ask them to clarify whether it's an agent or workflow.

### Step 2: Validate source

Check that the source directory exists in project scope:

```bash
ls -la "{project_root}/.a0proj/{agents|skills}/{name}/"
```

If it doesn't exist, list what IS available in that scope to help the user:

```bash
ls "{project_root}/.a0proj/agents/" 2>/dev/null
ls "{project_root}/.a0proj/skills/" 2>/dev/null
```

### Step 3: Check target and confirm

Check if the target already exists:

```bash
ls -la "/a0/usr/plugins/bmad_method/{agents|skills}/{name}/" 2>/dev/null
```

Present the operation to the user:
- Show source path
- Show target path
- If target exists, warn about overwrite
- Ask for explicit yes/no confirmation

### Step 4: Execute promotion

Run the promotion script:

```bash
bash {skill-root}/scripts/promote.sh {type} "{name}" "{project_root}"
```

If overwriting, set the force flag:

```bash
PROMOTE_FORCE=true bash {skill-root}/scripts/promote.sh {type} "{name}" "{project_root}"
```

### Step 5: Verify and summarize

After the script completes:

1. Verify the target exists: `ls -la /a0/usr/plugins/bmad_method/{agents|skills}/{name}/`
2. Confirm the contents match the source
3. Summarize:
   - What was promoted (agent/workflow name)
   - Where it was copied from (project scope)
   - Where it was copied to (plugin scope)
   - That it is now available globally across all projects

## Complete When

- The copy operation succeeded (verified target exists)
- The user has seen the confirmation summary
- The user understands the agent/workflow is now globally available

## Error Handling

- **Source not found**: Inform the user, list available agents/skills in project scope, suggest checking the name
- **Target exists**: Warn the user, require explicit confirmation to overwrite
- **Permission denied**: Suggest checking file permissions on the plugin directory
- **Script failure**: Show the error output, suggest running manually with debug (`bash -x`)

## When This Skill Can't Help

- **Installing new agents/skills**: Use `bmad-builder` (bmad-bmb) to create new agents/workflows first
- **Removing from plugin scope**: This skill only copies TO plugin scope. To remove, delete manually from `/a0/usr/plugins/bmad_method/{agents|skills}/{name}/`
- **Syncing changes**: Promotion is a one-time copy. If the source changes later, re-promote with overwrite confirmation
