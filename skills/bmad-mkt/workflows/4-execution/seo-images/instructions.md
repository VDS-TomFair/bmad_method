# SEO Images Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Perform image optimization using frameworks, alt text best practices, and format selection techniques.

## Content Coverage

### Image Optimization Frameworks
- **Technical SEO** — File size, dimensions, loading speed
- **Accessibility Standards** — WCAG compliance, screen readers
- **Performance Metrics** — LCP, CLS, Core Web Vitals
- **SEO Best Practices** — Indexation, structured data, sitemaps

### Alt Text Best Practices
- **Descriptive Language** — Accurate, concise, context-aware
- **Keyword Integration** — Natural inclusion, relevance
- **Avoid Redundancy** — No "image of," "picture of"
- **Brand Consistency** — Tone, terminology, messaging

### File Naming Conventions
- **Descriptive Names** — Product, feature, benefit focused
- **Keyword Usage** — Primary keywords when relevant
- **Hyphen Separation** — Lowercase, hyphens between words
- **Avoid Generic Names** — img001, photo, screenshot

### Format Selection
- **JPEG** — Photographs, complex images, smaller files
- **PNG** — Transparency, graphics, sharp lines
- **WebP** — Modern compression, smaller file sizes
- **SVG** — Icons, logos, scalable graphics

## Workflow Execution

1. Read BMAD config and product brief for context
2. Select image optimization frameworks and checklists
3. Develop alt text guidelines and file naming conventions
4. Recommend format selection and compression techniques
5. Create performance metrics and monitoring approaches

## Final Output

Write results to `{project-root}/_bmad-output/seo-images-{date}.md` containing:

### SEO Images Section
- **Image optimization audit** with findings
- **Alt text guidelines and template** with examples
- **Format selection recommendations** by use case
- **Performance metrics and monitoring** with tools

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
