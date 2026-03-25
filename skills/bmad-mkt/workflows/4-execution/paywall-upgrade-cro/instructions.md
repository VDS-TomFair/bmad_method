# Paywall Upgrade CRO Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Optimize paywalls using frameworks, upgrade path design, and personalization techniques.

## Content Coverage

### Optimization Frameworks
- **Conversion Funnel** — Awareness, interest, decision, action
- **Friction Points** — Pricing, value proposition, CTAs
- **Progressive Profiling** — Minimal initial data, gradual collection
- **A/B Testing** — Hypothesis-driven experimentation

### Upgrade Path Design
- **Visual Design** — Layout, spacing, mobile responsiveness
- **Copywriting** — Benefit-focused, urgency, clear CTAs
- **Trigger Conditions** — Feature gating, usage limits, time delays
- **Frequency Capping** — Avoid annoyance, respect user preferences

### User Experience
- **Page Speed** — Core Web Vitals, loading optimization
- **Accessibility** — WCAG compliance, screen readers
- **Personalization** — Dynamic content, tailored messaging
- **Exit Strategies** — Close buttons, overlay dismissal

### Implementation Guide
- **Tool Selection** — Paywall builders, analytics, A/B testing platforms
- **Deployment Steps** — Local testing, staging, production rollout
- **Monitoring Tools** — Google Analytics, Hotjar, FullStory
- **Performance Metrics** — Conversion rate, engagement, bounce rate

## Workflow Execution

1. Read BMAD config and product brief for context
2. Select optimization frameworks and analyze friction points
3. Design user experience and personalization improvements
4. Create A/B testing hypotheses and implementation guide
5. Define performance metrics and monitoring approaches

## Final Output

Write results to `{project-root}/_bmad-output/paywall-upgrade-cro-{date}.md` containing:

### Paywall Upgrade CRO Section
- **Paywall analysis** with friction points
- **Upgrade path optimization recommendations** with examples
- **A/B testing hypotheses and metrics** with tools
- **Implementation guide and monitoring** with steps

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
