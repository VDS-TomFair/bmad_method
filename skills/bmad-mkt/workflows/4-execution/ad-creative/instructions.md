# Ad Creative Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Create compelling ad creative variations using frameworks, copywriting, and platform-specific guidelines.

## Content Coverage

### Ad Creative Frameworks
- **Google Responsive Ads** — Headlines, descriptions, images
- **Facebook Carousel Ads** — Multiple image cards, CTAs
- **LinkedIn Sponsored Content** — Native, single image, video
- **Twitter Promoted Tweets** — Text, image, video formats
- **TikTok In-Feed Ads** — 9:16 video, hashtags, CTAs

### Copywriting Principles
- **Headline Formulas** — Benefit-driven, curiosity, urgency
- **Description Techniques** — Feature-to-benefit, social proof
- **Call-to-Action Patterns** — Direct, value-based, time-sensitive
- **Adaptation Strategies** — Short-form, long-form, mobile-first

### Design Guidelines
- **Visual Hierarchy** — Focal point, contrast, readability
- **Branding Elements** — Logo placement, colors, fonts
- **Image Composition** — Rule of thirds, whitespace, CTAs
- **Platform Optimization** — Aspect ratios, file sizes, formats

### A/B Testing
- **Test Variables** — Headlines, images, CTAs, audiences
- **Hypothesis Framework** — If-then statements, significance
- **Performance Metrics** — CTR, conversion rate, CPA, ROAS
- **Optimization Cycles** — Launch, measure, iterate

## Workflow Execution

1. Read BMAD config and product brief for context
2. Select ad creative frameworks and formats
3. Develop copywriting and design principles
4. Create platform-specific creative templates
5. Define performance metrics and A/B testing

## Final Output

Write results to `{project-root}/_bmad-output/ad-creative-{date}.md` containing:

### Ad Creative Section
- **Ad creative variations** with headlines and descriptions
- **Visual design guidelines and assets** with specs
- **Platform-specific creative templates** with examples
- **Performance metrics and A/B testing recommendations** with tools

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
