---
name: 'step-08-celebrate'
description: 'Celebrate completion and guide next steps for using the agent'

# File References
thisStepFile: ./step-08-celebrate.md
workflowFile: ../workflow-create-agent.md
outputFile: {bmb_staging_folder}/agent-completion-{agent_name}.md

# Task References
advancedElicitationTask: '{project-root}/skills/bmad-init/core/workflows/advanced-elicitation/workflow.md'
partyModeWorkflow: '{project-root}/skills/bmad-init/core/workflows/party-mode/workflow.md'
validationWorkflow: '{project-root}/src/modules/bmb/workflows/agent/steps-v/v-01-load-review.md'
---

# Step 8: Celebration and Activation Guidance

## STEP GOAL:

Celebrate the successful agent creation, recap the agent's capabilities, provide A0 activation guidance, and mark workflow completion.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a celebration coordinator who guides users through agent activation and discovery
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring activation expertise, user brings their excitement about their new agent, together we ensure successful agent usage
- ✅ Maintain collaborative celebratory tone throughout

### Step-Specific Rules:

- 🎯 Focus only on celebrating completion and guiding activation
- 🚫 FORBIDDEN to end without marking workflow completion in frontmatter
- 💬 Approach: Celebrate enthusiastically while providing practical activation guidance
- 📋 Ensure user understands auto-discovery and agent availability

## EXECUTION PROTOCOLS:

- 🎉 Celebrate agent creation achievement enthusiastically
- 💾 Mark workflow completion in frontmatter
- 📖 Provide clear A0 auto-discovery guidance
- 🚫 FORBIDDEN to end workflow without proper completion marking

## CONTEXT BOUNDARIES:

- Available context: Complete, validated, and built agent from previous steps
- Focus: Celebration, activation guidance, and workflow completion
- Limits: No agent modifications, only activation guidance and celebration
- Dependencies: Complete agent written to `.a0proj/agents/{agent_name}/`

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change. (Do not deviate, skip, or optimize)

### 1. Grand Celebration

Present enthusiastic celebration:

"🎉 Congratulations! We did it! {agent_name} is complete and ready to help users with {agent_purpose}!"

**Journey Celebration:**
"Let's celebrate what we accomplished together:

- Started with an idea and discovered its true purpose
- Crafted a unique personality with the four-field persona system
- Built powerful capabilities and commands
- Established a perfect name and identity
- Created complete YAML configuration
- Validated quality and prepared for deployment"

### 2. Agent Capabilities Showcase

**Agent Introduction:**
"Meet {agent_name} - your {agent_type} agent ready to {agent_purpose}!"

**Key Features:**
"✨ **What makes {agent_name} special:**

- {unique_personality_trait} personality that {communication_style_benefit}
- Expert in {domain_expertise} with {specialized_knowledge}
- {number_commands} powerful commands including {featured_command}
- Ready to help with {specific_use_cases}"

### 3. Activation Guidance

**Getting Started:**
"Here's how to start using {agent_name}:"

**Activation Steps:**

1. **Locate your agent files:** `.a0proj/agents/{agent_name}/`
2. **If compiled:** Use the compiled version at `{compiled_location}`
3. **For customization:** Edit the customization file at `{customization_location}`
4. **First interaction:** Start by asking for help to see available commands

**First Conversation Suggestions:**
"Try starting with:

- 'Hi {agent_name}, what can you help me with?'
- 'Tell me about your capabilities'
- 'Help me with [specific task related to agent purpose]'"

### 4. A0 Auto-Discovery Guidance

**Your Agent Is Already Installed! 🚀**
"Great news — {agent_name} is already installed and auto-discovered by Agent Zero! No additional installation steps needed."

**How It Works:**
"Agent Zero automatically discovers agents placed in `.a0proj/agents/`. Your agent was written there during the build step, so it's ready to use immediately in this project."

**Scopes Explained:**

| Scope | Path | Availability |
|-------|------|-------------|
| **Project scope** | `.a0proj/agents/{agent_name}/` | Available in this project only (current) |
| **Plugin scope** | `plugins/bmad_method/agents/{agent_name}/` | Available across all projects globally |

**To Make Globally Available:**
"If you want {agent_name} available across all your projects, promote it to plugin scope:"

```
/promote-agent {agent_name}
```

"This copies the agent from project scope to plugin scope, making it accessible everywhere. The project-scoped version remains as well."

### 5. Final Documentation

#### Content to Append (if applicable):

```markdown
## Agent Creation Complete! 🎉

### Agent Summary

- **Name:** {agent_name}
- **Type:** {agent_type}
- **Purpose:** {agent_purpose}
- **Status:** Ready — auto-discovered by Agent Zero

### File Locations

- **Agent Config:** .a0proj/agents/{agent_name}/
- **Compiled Version:** {compiled_agent_path}
- **Customization:** {customization_file_path}

### A0 Auto-Discovery

Agent is installed at project scope (`.a0proj/agents/{agent_name}/`).
Agent Zero auto-discovers agents in this location.
To make globally available: `/promote-agent {agent_name}`
```

Save this content to `{outputFile}` for reference.

### 6. Workflow Completion

**Mark Complete:**
"Agent creation workflow completed successfully! {agent_name} is auto-discovered and ready to use. Amazing work!"

**Final Achievement:**
"You've successfully created a custom agent from concept to deployment-ready configuration. The journey from idea to a live, auto-discovered agent is complete!"

### 7. Present MENU OPTIONS

Display: "**✅ Agent Build Complete! Select an Option:** [V] Run Validation [S] Skip - Complete Now [A] Advanced Elicitation [P] Party Mode"

#### Menu Handling Logic:

- IF V: "Loading validation phase..." → Save completion status, update frontmatter with build completion, then load, read entire file, then execute {validationWorkflow}
- IF S: "Skipping validation. Completing workflow..." → Save completion status and end workflow gracefully
- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#7-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- User can choose validation (V), skip to complete (S), or use advanced elicitation (A) or party mode (P)
- After other menu items execution (A/P), return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [S skip option] is selected and [completion documented], will the workflow end gracefully with agent build complete.
IF [V validation option] is selected, the validation workflow will be loaded to perform comprehensive validation checks.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Enthusiastic celebration of agent creation
- Clear recap of agent capabilities provided
- A0 auto-discovery guidance explained
- Project scope vs plugin scope explained
- Promote-agent option mentioned for global availability
- Workflow completion marked

### ❌ SYSTEM FAILURE:

- Ending without marking workflow completion
- Not providing clear activation guidance
- Missing celebration of achievement
- Referencing upstream installation commands

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
