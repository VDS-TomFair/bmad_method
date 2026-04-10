# Pricing Strategy Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Design pricing models and packaging using Van Westendorp analysis, competitive benchmarking, and willingness-to-pay research.

## Content Coverage

### Pricing Model Selection
- **Freemium** — Free tier with paid upgrades
- **Free Trial** — Time-limited full access
- **Paid Only** — No free access
- **Usage-Based** — Pay-per-use model
- **Hybrid** — Combination of above models

### Tier/Packaging Design
- Define tier levels (Starter, Professional, Enterprise)
- Feature allocation per tier
- Pricing anchors and decoy effects
- Value metric selection

### Van Westendorp Price Sensitivity Analysis
- **Too Cheap** — Price where product seems low quality
- **Bargain** — Price where product represents good value
- **Expensive** — Price where product seems high priced
- **Too Expensive** — Price where product is unaffordable

### Competitive Pricing Benchmarking
- Identify 3-5 direct competitors
- Map their pricing tiers and models
- Analyze perceived value vs. price
- Position relative to competition

### Willingness-to-Pay Research
- Customer interviews for job-to-be-done value
- Conjoint analysis for feature valuation
- Max price surveys
- Competitor switching cost analysis

## Workflow Execution

1. Read BMAD config and product brief for context
2. Select pricing model with rationale
3. Design tier structure (if applicable)
4. Conduct Van Westendorp analysis
5. Benchmark competitive pricing
6. Recommend final pricing range

## Final Output

Write results to `{project-root}/_bmad-output/pricing-strategy-{date}.md` containing:

### Pricing Strategy Section
- **Recommended pricing model** with clear rationale
- **Tier structure** (if applicable) with features per tier
- **Pricing range recommendation** from Van Westendorp + benchmarks
- **Competitive positioning** on price (premium, competitive, value)

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
