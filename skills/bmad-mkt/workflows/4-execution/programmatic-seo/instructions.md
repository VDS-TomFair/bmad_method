# Programmatic SEO Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Implement programmatic SEO using frameworks, data-driven generation, and template engines.

## Content Coverage

### Programmatic SEO Frameworks
- **Template Engines** — Jinja2, Handlebars, Liquid, Mustache
- **Data Sources** — CSV, JSON, APIs, databases, spreadsheets
- **Page Generation** — Category pages, location pages, comparison pages
- **SEO Best Practices** — Indexation, canonicalization, structured data

### Data Structures
- **Keyword Mapping** — Primary, secondary, semantic keyword usage
- **Metadata Templates** — Titles, descriptions, headers, alt text
- **Content Modules** — FAQ sections, product specs, location info
- **URL Patterns** — Clean, descriptive, keyword-rich structures

### Template Designs
- **Page Layouts** — Responsive, accessible, conversion-optimized
- **Dynamic Elements** — Personalization, localization, filtering
- **Performance Optimization** — Lazy loading, image compression
- **CMS Integration** — WordPress, Drupal, static site generators

### Implementation Guide
- **Tool Selection** — CLI tools, web frameworks, automation scripts
- **Deployment Steps** — Local testing, staging, production rollout
- **Error Handling** — Missing data, broken links, validation errors
- **Monitoring Tools** — Google Search Console, Ahrefs, SEMrush

## Workflow Execution

1. Read BMAD config and product brief for context
2. Select programmatic SEO frameworks and templates
3. Design data structures and template designs
4. Create implementation guide and deployment steps
5. Define performance metrics and optimization approaches

## Final Output

Write results to `{project-root}/_bmad-output/programmatic-seo-{date}.md` containing:

### Programmatic SEO Section
- **Programmatic SEO strategy framework** with examples
- **Template designs and data structures** with specs
- **Implementation guide and deployment steps**
- **Performance metrics and optimization approaches** with tools

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
