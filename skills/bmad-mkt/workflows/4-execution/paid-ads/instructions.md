# Paid Ads Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Create effective paid advertising campaigns using platform strategies, audience targeting, and campaign structures.

## Content Coverage

### Platform Strategies
- **Google Ads** — Search, display, video, shopping
- **Meta (Facebook/Instagram)** — Targeting, carousel ads, retargeting
- **LinkedIn** — Sponsored content, message ads, lead gen forms
- **Twitter/X** — Promoted tweets, trends, accounts
- **TikTok** — In-feed ads, branded effects, hashtags

### Audience Targeting
- **Demographics** — Age, gender, income, education
- **Geographics** — Location targeting and exclusion
- **Behavioral** — Purchase behavior, device usage
- **Contextual** — Content relevance, keyword targeting
- **Lookalike Audiences** — Scaling best-performing segments

### Campaign Structure
- **Account Hierarchy** — MCC, accounts, campaigns, ad groups
- **Campaign Types** — Awareness, consideration, conversion
- **Ad Group Organization** — Theme-based grouping
- **Bidding Strategies** — Manual, automated, smart bidding

### Performance Metrics
- **KPI Framework** — ROAS, CPA, CTR, conversion rate
- **Attribution Models** — Last-click, data-driven, time decay
- **Budget Allocation** — Channel weighting, seasonality
- **Optimization Levers** — Keywords, creatives, audiences

## Workflow Execution

1. Read BMAD config and product brief for context
2. Select platform strategies and targeting criteria
3. Develop campaign structure with ad groups
4. Define bidding strategy recommendations
5. Create budget allocation and performance metrics

## Final Output

Write results to `{project-root}/_bmad-output/paid-ads-{date}.md` containing:

### Paid Ads Section
- **Paid ads campaign structure** with ad groups
- **Audience targeting criteria and segments**
- **Bidding strategy recommendations** by platform
- **Budget allocation and performance metrics** with tools

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
