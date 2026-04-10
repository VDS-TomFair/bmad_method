# Growth Audit Orchestration Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Conduct a full-funnel growth audit that analyzes traffic, conversion, retention, and revenue metrics to identify the highest-leverage optimization opportunities. This is a data-driven diagnostic — not a strategy exercise, not a content planning session. Every recommendation must be backed by a metric and a hypothesis.

## Trigger
- Growth metrics declining or flatlining (traffic, conversion, retention, revenue)
- Quarterly growth review cadence
- New team member onboarding needing baseline understanding
- Pre-investment decision (where to allocate budget/resources)
- Post-launch performance review

## Inputs

### Required
- Access to analytics platform (GA4, Mixpanel, Segment, or similar)
- Date range for analysis (minimum 90 days recommended)
- Funnel stages defined (visit → signup → activate → convert → retain → expand)

### Recommended
- Cohort data segmented by acquisition channel
- Revenue and MRR data by cohort
- Previous audit results (if available) for trend comparison
- Competitor benchmark data

## Agent Responsibilities

| Agent | Role in Audit | Deliverables |
|-------|--------------|-------------|
| **Growth Engineer** (Lead) | Full funnel analysis, metric extraction, hypothesis generation, optimization roadmap | Audit report, funnel analysis, prioritized hypotheses |
| **Content Manager** | Channel content performance review, SEO traffic analysis | Content performance report, SEO gap analysis |
| **Marketing Strategist** | Competitive positioning assessment, market context | Competitive benchmark, strategic recommendations |

## Workflow Execution

### Step 1: Funnel Baseline
1. Extract conversion rates at every funnel stage for the analysis period
2. Map the full funnel: visit → signup → activate → convert → retain → expand
3. Calculate volume and rate at each transition
4. Identify the single biggest drop-off point (highest leverage)

Funnel analysis template:

| Stage | Volume | Conversion from Previous | Industry Benchmark | Gap |
|-------|--------|--------------------------|-------------------|-----|
| Visit | — | — | — | — |
| Signup | — | — | 3-5% | — |
| Activate | — | — | 25-40% | — |
| Convert | — | — | 2-5% | — |
| Retain (D30) | — | — | 40-60% | — |
| Expand | — | — | 10-20% | — |

### Step 2: Channel Performance
1. Break down traffic and conversion by channel (organic, paid, email, social, referral, direct)
2. Calculate ROI per channel (revenue attributed / spend + effort)
3. Identify underperforming channels and overperforming channels
4. Map channel-specific conversion funnels

Channel comparison template:

| Channel | Traffic | Signup CVR | Paid CVR | CPA | LTV | ROI |
|---------|---------|-----------|----------|-----|-----|-----|
| Organic | — | — | — | $0 | — | — |
| Paid Search | — | — | — | $— | — | — |
| Paid Social | — | — | — | $— | — | — |
| Email | — | — | — | $0 | — | — |
| Social | — | — | — | $0 | — | — |
| Referral | — | — | — | $— | — | — |

### Step 3: Cohort Retention Analysis
1. Segment users by acquisition month and channel
2. Track D7, D14, D30, D60, D90 retention for each cohort
3. Identify which cohorts retain best and worst
4. Correlate retention with activation behavior (what do retained users do that churned users don't?)

Cohort analysis questions:
- Which acquisition channel brings the stickiest users?
- Is retention improving or declining over recent cohorts?
- What is the critical drop-off point (day/week where most users leave)?
- Is there a "magic moment" — an action that predicts long-term retention?

### Step 4: Revenue Analysis
1. Calculate MRR/ARR trends over analysis period
2. Break down revenue by plan tier, cohort, and channel
3. Analyze expansion revenue vs. contraction revenue vs. churn
4. Calculate LTV by segment and compare to CAC

Revenue metrics to extract:
- MRR growth rate (month-over-month)
- Net revenue retention (expansion - contraction - churn)
- LTV:CAC ratio by channel
- Average revenue per user (ARPU) trend
- Time to payback CAC by channel

### Step 5: Hypothesis Generation
1. For each identified drop-off or underperformance, generate a hypothesis
2. Format: "We believe [change] will cause [metric impact] because [evidence]"
3. ICE-score each hypothesis:
   - **Impact**: How much will this move the target metric? (1-10)
   - **Confidence**: How strong is the evidence? (1-10)
   - **Ease**: How fast can we ship and measure? (1-10)
4. Rank hypotheses by ICE score

### Step 6: Optimization Roadmap
1. Group top hypotheses by funnel stage
2. Sequence experiments: quick wins first, then highest-impact
3. Estimate resource requirements for each experiment
4. Define success criteria before execution begins

## Expected Outputs

Write results to `{project-root}/_bmad-output/growth-audit-{date}.md` containing:

### Deliverables
- **Funnel Analysis**: Conversion rates at each stage with industry benchmarks and gap analysis
- **Channel Performance**: Traffic, CVR, CPA, LTV, ROI by channel with recommendations
- **Cohort Retention**: D7-D90 retention by acquisition cohort with correlation to activation behavior
- **Revenue Analysis**: MRR trends, LTV:CAC, net revenue retention, expansion vs. churn
- **Hypothesis Backlog**: ICE-scored hypotheses ranked by priority, grouped by funnel stage
- **Optimization Roadmap**: Sequenced experiment plan with resource estimates and success criteria

## Content Adaptation Compliance

These files comply with BMAD Content Adaptation rules:

- CA-1: No persona instructions like "You are an expert"
- CA-2: No references to `product-marketing-context.md`
- CA-3: All paths use BMAD aliases ({project-root}, {skill-dir})
- CA-4: Proper Standard tier BMAD format (instructions.md only)
- CA-5: CLI tools use `node {skill-dir}/tools/clis/<tool>.js` pattern
