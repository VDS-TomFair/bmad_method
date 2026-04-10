# Sales Enablement Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Enable sales teams using frameworks, content creation, and CRM integration.

## Content Coverage

### Enablement Frameworks
- **Buyer Personas** — ICP mapping, pain points, JTBD
- **Sales Process** — Discovery, demo, objection handling, closing
- **Content Types** — One-pagers, case studies, ROI calculators
- **Success Metrics** — Win rate, deal size, pipeline velocity

### Content Creation
- **Content Strategy** — Needs-based mapping, format variety
- **Writing Frameworks** — Problem-agitation-solution, storytelling
- **Design Principles** — Visual hierarchy, brand consistency
- **Review Process** — Sales feedback, version control

### CRM Integration
- **Data Flow Architecture** — Lead routing, field mapping, sync frequency
- **Sales Tools** — Lead alerts, activity logging, pipeline views
- **Analytics Integration** — GA4, Mixpanel, custom reporting
- **Automation Triggers** — Follow-ups, nurturing, alerts

### Implementation Guide
- **Tool Selection** — CRM platforms, content management, analytics
- **Deployment Steps** — Local testing, staging, production rollout
- **Monitoring Tools** — Real-time dashboards, alerting
- **Performance Metrics** — Content usage, deal acceleration, ROI

## Workflow Execution

1. Read BMAD config and product brief for context
2. Select enablement frameworks and content strategy
3. Plan CRM integration and tool selection
4. Create implementation guide and monitoring
5. Define analysis procedures and success criteria

## Final Output

Write results to `{project-root}/_bmad-output/sales-enablement-{date}.md` containing:

### Sales Enablement Section
- **Sales enablement strategy framework** with examples
- **Content creation and distribution plan** with templates
- **CRM integration and tracking** with steps
- **Success metrics and monitoring** with tools

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
