# RevOps Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Optimize revenue operations using frameworks, lead scoring, and CRM integration.

## Content Coverage

### Operations Frameworks
- **Revenue Lifecycle** — Lead capture, nurturing, conversion, retention
- **Process Optimization** — Workflow automation, data hygiene, governance
- **Technology Stack** — CRM, marketing automation, analytics tools
- **Team Alignment** — Marketing, sales, customer success coordination

### Lead Scoring Models
- **Scoring Criteria** — Firmographic, behavioral, engagement data
- **Model Types** — Rule-based, predictive, hybrid approaches
- **Scoring Thresholds** — MQL, SQL, SAL definitions
- **Validation Methods** — A/B testing, conversion analysis

### CRM Integration
- **Data Flow Architecture** — Lead routing, field mapping, sync frequency
- **Marketing Automation** — Email triggers, behavioral campaigns
- **Analytics Integration** — GA4, Mixpanel, custom reporting
- **Sales Tools** — Lead alerts, activity logging, pipeline views

### Implementation Guide
- **Tool Selection** — CRM platforms, marketing automation, analytics
- **Deployment Steps** — Local testing, staging, production rollout
- **Monitoring Tools** — Real-time dashboards, alerting
- **Performance Metrics** — Conversion rate, pipeline velocity, ROI

## Workflow Execution

1. Read BMAD config and product brief for context
2. Select operations frameworks and scoring models
3. Plan CRM integration and tool selection
4. Create implementation guide and monitoring
5. Define analysis procedures and success criteria

## Final Output

Write results to `{project-root}/_bmad-output/revops-{date}.md` containing:

### RevOps Section
- **RevOps strategy framework** with examples
- **Lead scoring and routing models** with criteria
- **CRM integration and data flow** with steps
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
