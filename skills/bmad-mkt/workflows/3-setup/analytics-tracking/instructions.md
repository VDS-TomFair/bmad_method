# Analytics Tracking Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Implement and configure GA4 with event tracking, conversion measurement, and validation to drive data-informed decisions.

## Content Coverage

### GA4 Implementation
- **Property Creation** — Stream configuration, data streams
- **Enhanced Measurement** — Scrolling, outbound clicks, site search
- **Consent Mode** — GDPR/CCPA compliance settings
- **Cross-Domain Tracking** — User journey continuity

### Event Tracking Setup
- **Event Taxonomy** — Standard and custom event naming
- **Parameter Configuration** — Custom dimensions and metrics
- **Trigger Mapping** — User actions to event firing
- **Tag Manager Integration** — GTM container setup and tags

### Conversion Tracking
- **Funnel Definition** — Key conversion paths (signup, purchase)
- **Attribution Models** — Last-click, linear, time-decay
- **Conversion Goals** — Event-based and duration-based
- **Ecommerce Tracking** — Purchase, refund, promotion events

### Implementation Validation
- **Tag Assistant** — Real-time event inspection
- **Debug View** — GA4 event debugging
- **Data Quality Checks** — Missing events, duplicate tracking
- **Cross-Platform Consistency** — Web, app, email tracking alignment

## Workflow Execution

1. Read BMAD config and product brief for context
2. Implement GA4 property with configuration
3. Set up event tracking taxonomy and triggers
4. Define conversion funnels and goals
5. Validate implementation with testing tools

## Final Output

Write results to `{project-root}/_bmad-output/analytics-tracking-{date}.md` containing:

### Analytics Tracking Section
- **GA4 property setup instructions** with configuration
- **Event taxonomy and tracking plan** with triggers
- **Conversion funnel definition** with goals
- **Implementation validation checklist** with tools

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
