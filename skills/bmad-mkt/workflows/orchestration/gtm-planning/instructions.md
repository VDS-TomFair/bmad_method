# Go-To-Market Planning Orchestration Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context
4. `{project-root}/_bmad-output/planning-artifacts/architecture-*.md` — Technical architecture (if exists)

## Task Overview

Orchestrate a complete go-to-market plan that coordinates positioning, content, growth, and sales into a unified launch strategy. This is the strategic coordination layer — it defines *what* needs to happen, *who* owns it, and *when* it ships.

## Trigger
- New product or feature launch planned
- Market entry into new segment or geography
- Pivot requiring repositioning of existing product
- Annual/quarterly GTM strategy refresh

## Inputs

### Required
- Product or feature being launched
- Target ICP and market segment
- Positioning statement or JTBD evidence
- Available channels (owned, earned, paid)
- Team composition and available agents

### Recommended
- Competitive landscape analysis
- Pricing model and packaging
- Budget allocation per channel
- Timeline constraints (hard launch date vs. flexible)
- Prior launch results and learnings

## Agent Responsibilities

| Agent | Role in GTM | Deliverables |
|-------|-------------|-------------|
| **Marketing Strategist** (Lead) | GTM strategy, positioning, channel selection, timeline, cross-agent coordination | GTM plan document, launch timeline, RACI matrix |
| **Content Manager** | Content creation, channel execution, asset production | Content plan, channel assets, launch copy |
| **Growth Engineer** | Analytics instrumentation, conversion tracking, experiment design | Tracking plan, baseline metrics, test hypotheses |
| **PM** (if available) | Cross-team alignment, resource allocation, stakeholder communication | Stakeholder brief, resource plan |
| **Architect** (if available) | Technical readiness, infrastructure for launch scale | Technical readiness checklist |

## Workflow Execution

### Step 1: Strategic Foundation
1. Read product brief and architecture docs for context
2. Define launch objectives (primary KPIs with targets)
3. Map positioning to target segments using JTBD framework
4. Identify competitive moats to emphasize in launch messaging

### Step 2: Channel Strategy & Timeline
1. Select launch channels based on where ICP is reachable
2. Design launch sequence: tease → announce → sustain → expand
3. Assign channel ownership to agents (who creates what for which channel)
4. Build launch timeline with milestones and dependencies

Channel selection matrix:

| Channel | Best For | Lead Agent |
|---------|----------|------------|
| Blog/SEO | Organic discovery, long-term traffic | Content Manager |
| Email | Existing audience activation | Content Manager |
| Paid Ads | Rapid awareness, targeting precision | Content Manager (creative) + Growth Engineer (tracking) |
| Social | Virality, community engagement | Content Manager |
| Product Hunt / Launch platforms | Tech audience, early adopters | Marketing Strategist |
| PR / Media | Credibility, broad reach | Marketing Strategist |
| Partner channels | Distribution leverage | Marketing Strategist |

### Step 3: Cross-Agent Coordination
1. Build RACI matrix for every launch deliverable
2. Identify dependencies between agents (content needs positioning brief, growth needs tracking plan)
3. Set up feedback loops: weekly standups, launch readiness reviews
4. Define escalation paths for blockers

### Step 4: Budget & Resource Allocation
1. Allocate budget across channels based on expected ROI
2. Identify resource constraints (content capacity, design bandwidth, engineering support)
3. Prioritize channels by impact × effort
4. Define contingency budget for top-performing channels post-launch

### Step 5: Measurement Framework
1. Define leading indicators (pre-launch: signups, waitlist, engagement)
2. Define lagging indicators (post-launch: conversion, revenue, retention)
3. Assign measurement ownership to Growth Engineer
4. Set review cadence: daily first week, weekly first month, monthly ongoing

### Step 6: Risk & Contingency
1. Identify top 3 launch risks and mitigation strategies
2. Define rollback criteria (when to pause or pivot)
3. Prepare contingency messaging for common issues
4. Plan for both best-case and worst-case scenarios

## Expected Outputs

Write results to `{project-root}/_bmad-output/gtm-plan-{date}.md` containing:

### Deliverables
- **GTM Strategy**: Positioning, ICP, channel selection, competitive advantages
- **Launch Timeline**: Week-by-week plan with milestones, dependencies, and deadlines
- **RACI Matrix**: Every deliverable assigned to responsible, accountable, consulted, informed agents
- **Budget Allocation**: Channel-by-channel spend with ROI expectations
- **Measurement Framework**: KPIs with targets, measurement tools, review cadence
- **Risk Assessment**: Top risks with mitigation strategies and rollback criteria

## Content Adaptation Compliance

These files comply with BMAD Content Adaptation rules:

- CA-1: No persona instructions like "You are an expert"
- CA-2: No references to `product-marketing-context.md`
- CA-3: All paths use BMAD aliases ({project-root}, {skill-dir})
- CA-4: Proper Standard tier BMAD format (instructions.md only)
- CA-5: CLI tools use `node {skill-dir}/tools/clis/<tool>.js` pattern
