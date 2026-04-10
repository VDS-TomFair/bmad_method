# Campaign Sprint Orchestration Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Execute a time-boxed, multi-channel campaign sprint — from brief to published assets to performance review — in a structured 1-2 week format. This is the tactical execution layer: defined scope, fixed deadline, measurable outcomes. Not a strategy document — a shipping plan.

## Trigger
- Campaign or promotion with a specific deadline (product launch, seasonal event, feature announcement)
- Need to produce multi-channel content quickly with clear ownership
- Repetitive campaign pattern that benefits from a repeatable sprint structure
- Marketing team has capacity for a focused 1-2 week execution push

## Inputs

### Required
- Campaign objective (awareness, leads, conversion, retention)
- Target audience segment
- Sprint duration (1 or 2 weeks)
- Available channels and budget
- Success metric with target

### Recommended
- Existing content assets that can be repurposed
- Brand guidelines and tone of voice
- Prior campaign results for benchmarking
- Competitive campaign examples for inspiration

## Agent Responsibilities

| Agent | Role in Sprint | Deliverables |
|-------|---------------|-------------|
| **Content Manager** (Lead) | Campaign brief, asset creation, channel execution, launch coordination | Campaign brief, all channel assets, launch checklist |
| **Growth Engineer** | Tracking setup, baseline metrics, performance dashboard | Tracking plan, dashboard template, baseline report |
| **Marketing Strategist** | Positioning validation, messaging framework, strategic review | Messaging brief, positioning check, strategic sign-off |

## Workflow Execution

### Step 1: Campaign Brief (Day 1)
1. Define campaign objective and primary KPI with specific target
2. Identify target audience segment with JTBD framing
3. Select channels based on where audience is reachable
4. Set sprint timeline with daily milestones
5. Assign asset ownership to agents

Campaign brief template:

| Element | Definition |
|---------|------------|
| Campaign name | [Descriptive name] |
| Objective | [Awareness / Leads / Conversion / Retention] |
| Primary KPI | [Metric + target] |
| Audience | [Segment + JTBD] |
| Duration | [1 or 2 weeks] |
| Channels | [Selected channels] |
| Budget | [Allocation per channel] |
| Tone | [Brand voice for this campaign] |

### Step 2: Messaging Framework (Day 1-2)
1. Develop core message (one sentence that drives the campaign)
2. Create channel-specific messaging variants
3. Define CTAs for each channel and audience stage
4. Validate messaging against positioning (Strategist sign-off)

Messaging matrix:

| Channel | Hook Message | Body Copy Direction | Primary CTA |
|---------|-------------|--------------------|----|
| Blog/SEO | — | — | — |
| Email (announce) | — | — | — |
| Email (nurture) | — | — | — |
| Paid ads | — | — | — |
| Social posts | — | — | — |
| Landing page | — | — | — |

### Step 3: Asset Production (Days 2-4)
1. Create assets for each channel in priority order
2. Follow platform-specific best practices for each
3. Include tracking parameters in all links (UTM tags)
4. Write A/B test variants for highest-traffic channels

Asset checklist by channel:

**Blog/SEO**
- [ ] Blog post draft (keyword-optimized)
- [ ] Meta description and social share image
- [ ] Internal links to related content

**Email**
- [ ] Announcement email (subject line + 2 variants)
- [ ] Nurture sequence (3-email drip)
- [ ] Segment-specific personalization

**Paid Ads**
- [ ] Google ad copy (3 headlines, 2 descriptions)
- [ ] Meta ad copy + creative direction
- [ ] LinkedIn ad copy + targeting criteria
- [ ] Budget allocation across ad sets

**Social**
- [ ] LinkedIn post (3 variants for testing)
- [ ] Twitter/X thread
- [ ] Supporting visuals or video scripts

**Landing Page**
- [ ] Headline, subhead, body copy
- [ ] CTA button copy and placement
- [ ] Social proof section
- [ ] Form fields and lead capture setup

### Step 4: Tracking Setup (Days 2-3, parallel with assets)
1. Define tracking events for each channel and conversion point
2. Set up UTM parameters for all campaign links
3. Build performance dashboard template
4. Record baseline metrics before launch

Tracking plan template:

| Event | Platform | Trigger | Property |
|-------|----------|---------|----------|
| Campaign page view | GA4 | Page load | utm_campaign |
| CTA click | GA4/Mixpanel | Button click | utm_content |
| Form submission | GA4/Mixpanel | Form submit | utm_source |
| Email open | Email platform | Open pixel | utm_medium |
| Ad click | Ad platform | Click | utm_content |

### Step 5: Launch Checklist (Day 5)
1. Verify all assets are finalized and approved
2. Confirm tracking is firing correctly (test each event)
3. Schedule email sends and social posts
4. Set ad campaigns to paused/ready state
5. Brief all stakeholders on launch timing

Pre-launch verification:
- [ ] All asset links have UTM parameters
- [ ] Landing page loads correctly on mobile and desktop
- [ ] Email sends are scheduled and tested
- [ ] Ad campaigns are set with correct targeting and budget
- [ ] Dashboard is pulling data from all channels
- [ ] Team is briefed on launch timing and escalation path

### Step 6: Performance Review (Day 7 or 14)
1. Pull performance data from all channels
2. Compare against KPI targets
3. Identify winning and underperforming assets/channels
4. Document learnings for next sprint

Review template:

| Metric | Target | Actual | Gap | Status |
|--------|--------|--------|-----|--------|
| [Primary KPI] | — | — | — | ✅/❌ |
| Impressions | — | — | — | — |
| Clicks | — | — | — | — |
| Conversions | — | — | — | — |
| CPA | — | — | — | — |
| ROAS | — | — | — | — |

### Step 7: Sprint Retrospective
1. What worked well? (repeat in next sprint)
2. What didn't work? (change or eliminate)
3. What surprised us? (new insights to explore)
4. Process improvements for next sprint
5. Asset repurposing opportunities

## Expected Outputs

Write results to `{project-root}/_bmad-output/campaign-sprint-{date}.md` containing:

### Deliverables
- **Campaign Brief**: Objective, audience, channels, timeline, budget, success metrics
- **Messaging Matrix**: Core message with channel-specific variants and CTAs
- **Asset Checklist**: Complete list of assets by channel with production status
- **Tracking Plan**: Events, platforms, triggers, and properties for full measurement
- **Launch Checklist**: Pre-launch verification steps for all channels
- **Performance Dashboard**: Template with KPIs, targets, and actual results
- **Sprint Retrospective**: Learnings, process improvements, repurposing opportunities

## Content Adaptation Compliance

These files comply with BMAD Content Adaptation rules:

- CA-1: No persona instructions like "You are an expert"
- CA-2: No references to `product-marketing-context.md`
- CA-3: All paths use BMAD aliases ({project-root}, {skill-dir})
- CA-4: Proper Standard tier BMAD format (instructions.md only)
- CA-5: CLI tools use `node {skill-dir}/tools/clis/<tool>.js` pattern
