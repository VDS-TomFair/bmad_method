# Referral Program Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Create referral programs using frameworks, incentive design, and tracking methodologies.

## Content Coverage

### Program Frameworks
- **Program Types** — Customer, partner, affiliate, employee
- **Reward Structures** — Monetary, credit, gifts, exclusive access
- **Communication Channels** — Email, in-app, social, referral page
- **Compliance Considerations** — FTC guidelines, terms of service

### Incentive Design
- **Value Proposition** — Clear benefits for referrer and referee
- **Tiered Rewards** — Progressive incentives for volume
- **Time-Based Bonuses** — Limited-time promotions
- **Gamification Elements** — Leaderboards, badges, milestones

### Tracking Methodologies
- **Unique Referral Links** — UTM parameters, tracking codes
- **Conversion Attribution** — First-click, last-click, linear
- **Analytics Integration** — GA4, Mixpanel, CRM sync
- **Fraud Prevention** — Duplicate detection, IP filtering

### Implementation Guide
- **Tool Selection** — Referral software, analytics, email
- **Deployment Steps** — Local testing, staging, production rollout
- **Monitoring Tools** — Real-time dashboards, alerting
- **Performance Metrics** — Conversion rate, revenue, retention

## Workflow Execution

1. Read BMAD config and product brief for context
2. Select program frameworks and incentive design
3. Plan tracking methodologies and tool selection
4. Create implementation guide and monitoring
5. Define analysis procedures and success criteria

## Final Output

Write results to `{project-root}/_bmad-output/referral-program-{date}.md` containing:

### Referral Program Section
- **Referral program strategy framework** with examples
- **Incentive structure and reward recommendations**
- **Tracking and measurement plan** with tools
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
