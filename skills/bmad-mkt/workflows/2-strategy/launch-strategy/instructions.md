# Launch Strategy Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Plan and execute product launches using pre-launch research, coordinated execution, and post-launch measurement.

## Content Coverage

### Pre-Launch Strategy
- **Audience Research** — ICP definition, job-to-be-done, pain points
- **Messaging Framework** — Value proposition, differentiators, proof points
- **Positioning Alignment** — Competitive mapping, market context
- **Stakeholder Alignment** — Internal buy-in, cross-team coordination

### Launch Execution Plan
- **Timeline Development** — Key milestones, dependencies, deadlines
- **Channel Strategy** — Owned, earned, paid channels with tactics
- **Content Plan** — Launch assets (press release, blog, social posts)
- **Team Roles** — RACI matrix for launch participants

### Post-Launch Measurement
- **KPI Selection** — Leading and lagging indicators of success
- **Success Metrics** — Quantitative targets (signups, traffic, revenue)
- **Feedback Loops** — Qualitative insights (surveys, interviews)
- **Iteration Planning** — What to continue, stop, start

## Workflow Execution

1. Read BMAD config and product brief for context
2. Develop pre-launch strategy (audience, messaging, positioning)
3. Create launch execution plan (timeline, channels, content, roles)
4. Define post-launch measurement framework (KPIs, metrics, feedback)

## Final Output

Write results to `{project-root}/_bmad-output/launch-strategy-{date}.md` containing:

### Launch Strategy Section
- **Launch timeline** with key milestones and dependencies
- **Channel strategy and content plan** for all channels
- **Success metrics and KPI definitions** with targets
- **Team roles and responsibilities** with RACI matrix

## Content Adaptation Compliance

These files comply with BMAD Content Adaptation rules:

- CA-1: No persona instructions like "You are an expert" 
- CA-2: No references to `product-marketing-context.md`
- CA-3: All paths use BMAD aliases ({project-root}, {skill-dir})
- CA-4: Proper Standard tier BMAD format (instructions.md only)
- CA-5: CLI tools use `node {skill-dir}/tools/clis/<tool>.js` pattern
- CA-6: BMAD frontmatter in workflow.yaml
- CA-7: Source attribution preserved in workflow.yaml
- CA-8: No external API dependencies (web access only)
