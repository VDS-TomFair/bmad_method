# Churn Prevention Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Reduce both voluntary and involuntary churn through cancel flow design, dynamic save offers, proactive retention signals, and dunning strategies. This workflow covers the full retention stack from prediction to recovery.

## Trigger

- Monthly churn rate exceeds target threshold (< 5% B2C, < 2% B2B)
- Customer cancels subscription (voluntary churn)
- Payment fails (involuntary churn)
- Proactive: Health score drops below risk threshold

## Inputs

### Required
- Current churn situation: monthly rate, subscriber count, average MRR per customer, existing cancel flow (or none)
- Billing platform: Stripe, Chargebee, Paddle, Recurly, or Braintree
- Billing intervals: monthly, annual, or both

### Recommended
- Feature usage data per user
- Cancellation reason data from past churns
- Activation metric definition (what retained users do that churned users don't)
- Existing retention tooling (Churnkey, ProsperStack, Raaft)

### Constraints
- B2B vs B2C (affects flow design significantly)
- Self-serve cancellation requirements (FTC Click-to-Cancel compliance)
- Brand tone for offboarding (empathetic, direct, playful)

## Content Coverage

### Cancel Flow Design

The cancel flow follows this sequence:
```
Trigger → Exit Survey → Dynamic Save Offer → Confirmation → Post-Cancel
```

**Exit Survey Design**
- 1 question, single-select with optional free text
- 5-8 reason options maximum
- Reason categories with save offer implications:

| Reason | What It Tells You | Primary Save Offer |
|--------|-------------------|-------------------|
| Too expensive | Price sensitivity | Discount 20-30% for 2-3 months |
| Not using enough | Low engagement | Pause 1-3 months |
| Missing feature | Product gap | Roadmap preview + workaround |
| Switching to competitor | Competitive pressure | Competitive comparison + discount |
| Technical issues | Product quality | Escalate to support + credit |
| Temporary/seasonal | Usage pattern | Pause subscription |
| Business closed | Unavoidable | Skip offer gracefully |

**Dynamic Save Offers**
- Match the offer to the cancel reason — blanket discounts don't work
- Offer types: discount, pause, plan downgrade, feature unlock, personal outreach
- Discount sweet spot: 20-30% for 2-3 months (avoid 50%+ — trains customers to cancel for deals)
- Pause: 1-3 months maximum, 60-80% of pausers eventually return
- Personal outreach for high-value accounts (top 10-20% by MRR)

**UI Principles**
- Keep "continue cancelling" visible (no dark patterns)
- One primary offer + one fallback
- Show specific dollar savings, not abstract percentages
- Mobile-friendly (many cancellations happen on mobile)

### Churn Prediction & Proactive Retention

**Risk Signals**

| Signal | Risk Level | Timeframe Before Cancel |
|--------|-----------|------------------------|
| Login frequency drops 50%+ | High | 2-4 weeks |
| Key feature usage stops | High | 1-3 weeks |
| Support tickets spike then stop | High | 1-2 weeks |
| Data export initiated | Critical | Days |
| NPS score below 6 | Medium | 1-3 months |

**Health Score Model**
```
Health Score = (
  Login frequency score × 0.30 +
  Feature usage score   × 0.25 +
  Support sentiment     × 0.15 +
  Billing health        × 0.15 +
  Engagement score      × 0.15
)
```

| Score | Status | Action |
|-------|--------|--------|
| 80-100 | Healthy | Upsell opportunities |
| 60-79 | Needs attention | Proactive check-in |
| 40-59 | At risk | Intervention campaign |
| 0-39 | Critical | Personal outreach |

### Involuntary Churn: Payment Recovery

**The Dunning Stack**
```
Pre-dunning → Smart retry → Dunning emails → Grace period → Hard cancel
```

**Smart Retry Logic**

| Decline Type | Retry Strategy |
|-------------|----------------|
| Soft decline (insufficient funds) | Retry 3-5 times over 7-10 days |
| Hard decline (card stolen) | Don't retry — ask for new card |
| Authentication required (3D Secure) | Send customer to update payment |

**Retry timing**: 24h → 3 days → 5 days → 7 days → hard cancel

**Dunning Email Sequence**

| Email | Timing | Tone | Content |
|-------|--------|------|---------|
| 1 | Day 0 | Friendly alert | "Payment didn't go through. Update card." |
| 2 | Day 3 | Helpful reminder | "Update payment to keep access." |
| 3 | Day 7 | Urgency | "Account pauses in 3 days." |
| 4 | Day 10 | Final warning | "Last chance to stay active." |

**Dunning best practices**: Direct link to payment update (no login if possible), show what they'll lose, plain text outperforms designed emails

### Metrics & Measurement

| Metric | Formula | Target |
|--------|---------|--------|
| Monthly churn rate | Churned / Start-of-month customers | < 5% B2C, < 2% B2B |
| Cancel flow save rate | Saved / Total cancel sessions | 25-35% |
| Pause reactivation rate | Reactivated / Total paused | 60-80% |
| Dunning recovery rate | Recovered / Failed payments | 50-60% |

**A/B Test Ideas**: Discount % (20% vs 30%), pause duration (1 vs 3 months), survey placement (before vs after offer), copy tone (empathetic vs direct)

### Common Mistakes
- No cancel flow at all (even simple survey + one offer saves 10-15%)
- Hidden cancel button (breeds resentment, FTC compliance risk)
- Same offer for every reason (blanket discount doesn't address "missing feature")
- Discounts too deep (50%+ trains cancel-and-return behavior)
- Ignoring involuntary churn (30-50% of total, easiest to fix)
- No post-cancel reactivation path

## Workflow Execution

1. Read BMAD config and product brief for context
2. Assess current churn situation and billing platform
3. Design cancel flow: exit survey → dynamic save offers → confirmation → post-cancel
4. Build health score model with risk signals and intervention triggers
5. Design dunning stack: pre-dunning, smart retry, email sequence, grace period
6. Define metrics dashboard with targets and cohort analysis segments
7. Plan A/B tests for cancel flow optimization

## Final Output

Write results to `{project-root}/_bmad-output/churn-prevention-{date}.md` containing:

### Deliverables
- **Cancel Flow Design**: Exit survey with reason categories, dynamic save offer mapping, UI patterns, post-cancel flow
- **Health Score Model**: Weighted scoring formula, risk signal thresholds, intervention mapping by score range
- **Dunning Stack**: Smart retry logic by decline type, email sequence with timing and copy direction, recovery benchmarks
- **Metrics Dashboard**: Key churn metrics with targets, cohort analysis segments, A/B test plan
- **Implementation Notes**: Platform-specific guidance (Stripe/Chargebee/Paddle), retention tool recommendations

## Content Adaptation Compliance

These files comply with BMAD Content Adaptation rules:

- CA-1: No persona instructions like "You are an expert"
- CA-2: No references to `product-marketing-context.md`
- CA-3: All paths use BMAD aliases ({project-root}, {skill-dir})
- CA-4: Proper Standard tier BMAD format (instructions.md only)
- CA-5: CLI tools use `node {skill-dir}/tools/clis/<tool>.js` pattern
