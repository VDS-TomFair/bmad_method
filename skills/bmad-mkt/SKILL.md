---
name: "bmad-mkt"
description: "BMAD Marketing Knowledge (BMK) — marketing strategy, SEO, CRO, growth, and content execution. Triggers: marketing strategy, market positioning, content strategy, seo audit, seo plan, conversion optimization, growth engineering, launch strategy, pricing strategy, copywriting, email sequence, paid ads, ad creative, social content, referral program, churn prevention, sales enablement, ab test, a/b test, free tool strategy, gtm planning, mkt module."
version: "1.0.0"
author: "BMAD"
tags: ["bmad", "mkt", "marketing", "seo", "cro", "growth", "content", "ads", "email"]
trigger_patterns:
  - "marketing strategy"
  - "market positioning"
  - "content strategy"
  - "seo audit"
  - "seo plan"
  - "conversion optimization"
  - "growth engineering"
  - "launch strategy"
  - "pricing strategy"
  - "copywriting"
  - "email sequence"
  - "paid ads"
  - "ad creative"
  - "social content"
  - "referral program"
  - "churn prevention"
  - "sales enablement"
  - "ab test"
  - "a/b test"
  - "free tool strategy"
  - "gtm planning"
  - "mkt module"
---

# BMAD Marketing Knowledge (BMK) — Marketing Strategy, SEO, CRO, and Growth

BMK provides end-to-end marketing execution workflows: discovery, strategy, setup, execution, growth, and retention. Use BMK when you need marketing campaigns, SEO optimization, conversion rate improvement, content creation, paid advertising, or growth programs.

All paths use `{project-root}` which resolves to `.a0proj/` as defined in `01-bmad-config.md`. The skill directory alias `{skill-dir}` resolves to `skills/bmad-mkt/`.

When any BMK workflow is triggered, read the full workflow file at the path shown and follow it exactly.

---

## BMK Workflows

### Phase 1 — Discovery

#### Market Positioning
**Triggers:** "market positioning", "competitive positioning", "value proposition", "ICP definition"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/market-positioning-<date>.md`
**Workflow:** `{skill-dir}/workflows/1-discovery/market-positioning/workflow.yaml`

#### Marketing Psychology
**Triggers:** "marketing psychology", "behavioral science", "persuasion", "mental models"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/marketing-psychology-<date>.md`
**Workflow:** `{skill-dir}/workflows/1-discovery/marketing-psychology/workflow.yaml`

#### Pricing Strategy
**Triggers:** "pricing strategy", "pricing model", "pricing tiers", "willingness to pay"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/pricing-strategy-<date>.md`
**Workflow:** `{skill-dir}/workflows/1-discovery/pricing-strategy/workflow.yaml`

### Phase 2 — Strategy

#### Content Strategy
**Triggers:** "content strategy", "content planning", "editorial calendar", "topic clusters"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/content-strategy-<date>.md`
**Workflow:** `{skill-dir}/workflows/2-strategy/content-strategy/workflow.yaml`

#### Launch Strategy
**Triggers:** "launch strategy", "product launch", "go-to-market", "GTM planning"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/launch-strategy-<date>.md`
**Workflow:** `{skill-dir}/workflows/2-strategy/launch-strategy/workflow.yaml`

#### Lead Magnets
**Triggers:** "lead magnets", "lead generation", "gated content", "content upgrade"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/lead-magnets-<date>.md`
**Workflow:** `{skill-dir}/workflows/2-strategy/lead-magnets/workflow.yaml`

#### Marketing Ideas
**Triggers:** "marketing ideas", "growth tactics", "marketing brainstorming"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/marketing-ideas-<date>.md`
**Workflow:** `{skill-dir}/workflows/2-strategy/marketing-ideas/workflow.yaml`

#### SEO Plan
**Triggers:** "seo plan", "SEO strategy", "keyword roadmap", "SEO gaps"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/seo-plan-<date>.md`
**Workflow:** `{skill-dir}/workflows/2-strategy/seo-plan/workflow.yaml`

### Phase 3 — Setup

#### Analytics Tracking
**Triggers:** "analytics tracking", "GA4 setup", "event tracking", "UTM parameters"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/analytics-tracking-<date>.md`
**Workflow:** `{skill-dir}/workflows/3-setup/analytics-tracking/workflow.yaml`

#### Site Architecture
**Triggers:** "site architecture", "page hierarchy", "URL structure", "internal linking"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/site-architecture-<date>.md`
**Workflow:** `{skill-dir}/workflows/3-setup/site-architecture/workflow.yaml`

#### SEO Technical
**Triggers:** "seo technical", "technical SEO", "crawlability", "Core Web Vitals"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/seo-technical-<date>.md`
**Workflow:** `{skill-dir}/workflows/3-setup/seo-technical/workflow.yaml`

#### SEO Sitemap
**Triggers:** "seo sitemap", "XML sitemap", "sitemap generation"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/seo-sitemap-<date>.md`
**Workflow:** `{skill-dir}/workflows/3-setup/seo-sitemap/workflow.yaml`

#### SEO Hreflang
**Triggers:** "seo hreflang", "international SEO", "multi-language", "hreflang tags"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/seo-hreflang-<date>.md`
**Workflow:** `{skill-dir}/workflows/3-setup/seo-hreflang/workflow.yaml`

### Phase 4 — Execution

#### Copywriting
**Triggers:** "copywriting", "page copy", "landing page copy", "homepage copy"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/copywriting-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/copywriting/workflow.yaml`

#### Copy Editing
**Triggers:** "copy editing", "edit copy", "improve copy", "copy review"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/copy-editing-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/copy-editing/workflow.yaml`

#### Email Sequence
**Triggers:** "email sequence", "drip campaign", "nurture sequence", "lifecycle emails"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/email-sequence-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/email-sequence/workflow.yaml`

#### Cold Email
**Triggers:** "cold email", "prospecting email", "B2B outreach", "sales email"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/cold-email-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/cold-email/workflow.yaml`

#### Social Content
**Triggers:** "social content", "LinkedIn post", "Twitter thread", "social media"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/social-content-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/social-content/workflow.yaml`

#### Paid Ads
**Triggers:** "paid ads", "PPC campaign", "Google Ads", "Meta ads"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/paid-ads-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/paid-ads/workflow.yaml`

#### Ad Creative
**Triggers:** "ad creative", "ad copy", "headlines", "creative variations"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/ad-creative-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/ad-creative/workflow.yaml`

#### SEO Audit
**Triggers:** "seo audit", "SEO review", "SEO issues", "SEO diagnosis"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/seo-audit-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/seo-audit/workflow.yaml`

#### AI SEO
**Triggers:** "ai seo", "AI Overviews", "GEO", "LLM optimization"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/ai-seo-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/ai-seo/workflow.yaml`

#### SEO Page
**Triggers:** "seo page", "page analysis", "single page SEO", "on-page SEO"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/seo-page-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/seo-page/workflow.yaml`

#### SEO Content
**Triggers:** "seo content", "E-E-A-T", "content quality", "content audit"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/seo-content-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/seo-content/workflow.yaml`

#### SEO Images
**Triggers:** "seo images", "image optimization", "alt text", "lazy loading"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/seo-images-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/seo-images/workflow.yaml`

#### SEO Schema
**Triggers:** "seo schema", "schema markup", "structured data", "JSON-LD"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/seo-schema-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/seo-schema/workflow.yaml`

#### SEO GEO
**Triggers:** "seo geo", "GEO analysis", "AI visibility", "LLM citability"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/seo-geo-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/seo-geo/workflow.yaml`

#### Programmatic SEO
**Triggers:** "programmatic seo", "pages at scale", "template pages", "dynamic pages"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/programmatic-seo-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/programmatic-seo/workflow.yaml`

#### Signup Flow CRO
**Triggers:** "signup flow", "registration", "free trial", "signup optimization"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/signup-flow-cro-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/signup-flow-cro/workflow.yaml`

#### Form CRO
**Triggers:** "form CRO", "lead form", "contact form", "demo request"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/form-cro-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/form-cro/workflow.yaml`

#### Onboarding CRO
**Triggers:** "onboarding CRO", "user activation", "first-run experience", "time-to-value"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/onboarding-cro-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/onboarding-cro/workflow.yaml`

#### Popup CRO
**Triggers:** "popup CRO", "exit intent", "email popup", "lead capture popup"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/popup-cro-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/popup-cro/workflow.yaml`

#### Paywall Upgrade CRO
**Triggers:** "paywall upgrade", "upgrade screen", "freemium conversion", "upsell"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/paywall-upgrade-cro-<date>.md`
**Workflow:** `{skill-dir}/workflows/4-execution/paywall-upgrade-cro/workflow.yaml`

### Phase 5 — Growth

#### Page CRO
**Triggers:** "page CRO", "conversion rate optimization", "landing page optimization"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/page-cro-<date>.md`
**Workflow:** `{skill-dir}/workflows/5-growth/page-cro/workflow.yaml`

#### A/B Test Setup
**Triggers:** "ab test", "a/b test", "split test", "experiment"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/ab-test-<date>.md`
**Workflow:** `{skill-dir}/workflows/5-growth/ab-test-setup/workflow.yaml`

#### Referral Program
**Triggers:** "referral program", "affiliate", "word of mouth", "refer a friend"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/referral-program-<date>.md`
**Workflow:** `{skill-dir}/workflows/5-growth/referral-program/workflow.yaml`

#### Free Tool Strategy
**Triggers:** "free tool strategy", "marketing tool", "calculator", "generator"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/free-tool-strategy-<date>.md`
**Workflow:** `{skill-dir}/workflows/5-growth/free-tool-strategy/workflow.yaml`

#### RevOps
**Triggers:** "revops", "revenue operations", "lead scoring", "pipeline"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/revops-<date>.md`
**Workflow:** `{skill-dir}/workflows/5-growth/revops/workflow.yaml`

#### Sales Enablement
**Triggers:** "sales enablement", "sales deck", "one-pager", "battle card"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/sales-enablement-<date>.md`
**Workflow:** `{skill-dir}/workflows/5-growth/sales-enablement/workflow.yaml`

#### SEO Competitor Pages
**Triggers:** "seo competitor pages", "alternatives page", "vs page", "comparison page"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/seo-competitor-pages-<date>.md`
**Workflow:** `{skill-dir}/workflows/5-growth/seo-competitor-pages/workflow.yaml`

### Phase 6 — Retention

#### Churn Prevention
**Triggers:** "churn prevention", "churn", "cancellation flow", "retention"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/churn-prevention-<date>.md`
**Workflow:** `{skill-dir}/workflows/6-retention/churn-prevention/workflow.yaml`

### Orchestration

#### GTM Planning
**Triggers:** "gtm planning", "go-to-market", "launch planning", "GTM strategy"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/gtm-planning-<date>.md`
**Workflow:** `{skill-dir}/workflows/orchestration/gtm-planning/workflow.yaml`

#### Growth Audit
**Triggers:** "growth audit", "marketing audit", "performance review"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/growth-audit-<date>.md`
**Workflow:** `{skill-dir}/workflows/orchestration/growth-audit/workflow.yaml`

#### Campaign Sprint
**Triggers:** "campaign sprint", "marketing sprint", "campaign execution"
**Output artifact:** `{project-root}/_bmad-output/planning-artifacts/campaign-sprint-<date>.md`
**Workflow:** `{skill-dir}/workflows/orchestration/campaign-sprint/workflow.yaml`

---


---

## Short Trigger Codes

Use these short codes or fuzzy phrases to activate BMK specialist agents directly:

| Code | Fuzzy Phrase | Agent | Description |
|------|-------------|-------|-------------|
| `MP` | market-positioning | marketing-strategist | Define competitive positioning and ICP |
| `MY` | marketing-psychology | marketing-strategist | Apply behavioral science to marketing |
| `PS` | pricing-strategy | marketing-strategist | Design pricing models and packaging |
| `CS` | content-strategy | content-channels-lead | Plan content and editorial calendar |
| `LS` | launch-strategy | marketing-strategist | Plan product launches |
| `LM` | lead-magnets | content-channels-lead | Design lead generation content |
| `MI` | marketing-ideas | marketing-strategist | Brainstorm growth tactics |
| `SP` | seo-plan | content-channels-lead | Develop SEO strategy and roadmap |
| `AT` | analytics-tracking | content-channels-lead | Set up GA4 and event tracking |
| `SA` | site-architecture | content-channels-lead | Plan site structure and URLs |
| `ST` | seo-technical | content-channels-lead | Audit technical SEO |
| `SM` | seo-sitemap | content-channels-lead | Generate XML sitemaps |
| `SH` | seo-hreflang | content-channels-lead | Implement international SEO |
| `CW` | copywriting | content-channels-lead | Write marketing page copy |
| `CE` | copy-editing | content-channels-lead | Edit existing marketing copy |
| `ES` | email-sequence | content-channels-lead | Create drip and nurture sequences |
| `CL` | cold-email | content-channels-lead | Write B2B outreach emails |
| `SC` | social-content | content-channels-lead | Create social media content |
| `PA` | paid-ads | content-channels-lead | Plan paid advertising campaigns |
| `AC` | ad-creative | content-channels-lead | Generate ad headlines and variations |
| `AU` | seo-audit | content-channels-lead | Run comprehensive SEO audits |
| `AI` | ai-seo | content-channels-lead | Optimize for AI search engines |
| `PG` | seo-page | content-channels-lead | Analyze single-page SEO |
| `CN` | seo-content | content-channels-lead | Audit content quality and E-E-A-T |
| `IM` | seo-images | content-channels-lead | Optimize images for SEO |
| `SS` | seo-schema | content-channels-lead | Generate schema markup |
| `GE` | seo-geo | content-channels-lead | Optimize for AI Overviews |
| `PR` | programmatic-seo | content-channels-lead | Build pages at scale |
| `SF` | signup-flow | content-channels-lead | Optimize signup and trial flows |
| `FC` | form-cro | content-channels-lead | Optimize lead capture forms |
| `OC` | onboarding-cro | content-channels-lead | Improve user activation |
| `PC` | popup-cro | content-channels-lead | Optimize conversion popups |
| `PU` | paywall-upgrade | content-channels-lead | Design upgrade screens |
| `CR` | page-cro | growth-engineer | Optimize conversion pages |
| `AB` | ab-test | growth-engineer | Design A/B and multivariate tests |
| `RP` | referral | growth-engineer | Build referral programs |
| `FT` | free-tool | growth-engineer | Design marketing tools |
| `RV` | revops | growth-engineer | Improve revenue operations |
| `SE` | sales-enablement | growth-engineer | Create sales collateral |
| `CP` | competitor-pages | content-channels-lead | Build SEO competitor pages |
| `CH` | churn | growth-engineer | Prevent user cancellation |
| `GP` | gtm-planning | marketing-strategist | Orchestrate go-to-market |
| `CM` | campaign-sprint | growth-engineer | Execute campaign sprints |

## Execution Instructions

When any BMK workflow is triggered:
1. Identify the workflow from the trigger phrase or short code above.
2. Read the full workflow file at the path shown using `text_editor:read`.
3. Follow the workflow instructions exactly — do not summarize or skip steps.
4. Write output artifacts using `text_editor:write`.
5. Update `{project-root}/instructions/02-bmad-state.md` to reflect the active BMK workflow.

---

## Knowledge Integration

BMK workflows leverage the full BMAD knowledge base for marketing intelligence. All agent responses should include relevant market context, competitive analysis, and data-driven recommendations.
