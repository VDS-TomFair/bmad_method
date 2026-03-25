# A/B Test Setup Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Set up A/B tests using frameworks, hypothesis formation, and statistical planning.

## Content Coverage

### Testing Frameworks
- **Hypothesis Framework** — If-then statements, significance levels
- **Statistical Planning** — Sample size, confidence intervals
- **Test Types** — Multivariate, sequential, factorial designs
- **Best Practices** — Randomization, control groups, duration

### Hypothesis Formation
- **Problem Statement** — Current performance, user pain points
- **Proposed Solution** — Change description, expected impact
- **Success Metrics** — Primary KPI, secondary metrics
- **Risk Assessment** — Potential negative impacts, mitigation

### Tool Selection
- **A/B Testing Platforms** — Optimizely, VWO, Google Optimize
- **Analytics Integration** — GA4, Mixpanel, Segment
- **Visualization Tools** — Charts, dashboards, reporting
- **Statistical Calculators** — Significance, sample size tools

### Implementation Guide
- **Deployment Steps** — Local testing, staging, production rollout
- **Quality Assurance** — Validation checks, error handling
- **Monitoring Tools** — Real-time dashboards, alerting
- **Performance Metrics** — Conversion rate, engagement, revenue

## Workflow Execution

1. Read BMAD config and product brief for context
2. Select testing frameworks and form hypothesis
3. Plan statistical approach and tool selection
4. Create implementation guide and monitoring
5. Define analysis procedures and success criteria

## Final Output

Write results to `{project-root}/_bmad-output/ab-test-setup-{date}.md` containing:

### A/B Test Setup Section
- **A/B test hypothesis framework** with examples
- **Statistical significance and sample size calculations**
- **Tool implementation guide** with steps
- **Monitoring and analysis procedures** with tools

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
