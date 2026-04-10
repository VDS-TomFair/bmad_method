# SEO Schema Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Implement schema markup using frameworks, JSON-LD generation, and validation procedures.

## Content Coverage

### Schema Frameworks
- **Schema.org Types** — Organization, Product, Article, FAQPage
- **Rich Results** — Reviews, breadcrumbs, sitelinks, events
- **Technical Implementation** — JSON-LD placement, CMS integration
- **Validation Tools** — Google Rich Results Test, Structured Data Testing Tool

### JSON-LD Generation
- **Organization Schema** — Logo, contact info, social profiles
- **Product Schema** — Name, description, price, availability
- **Article Schema** — Headline, author, publish date, image
- **FAQ Schema** — Question-answer pairs, accordion implementation

### Testing Procedures
- **Validation Checklists** — Required properties, nested objects
- **CMS Integration** — WordPress, Drupal, static site generators
- **Monitoring Tools** — Google Search Console, Ahrefs, SEMrush
- **Error Handling** — Missing properties, incorrect values

### Performance Metrics
- **Rich Result Coverage** — Eligible pages, rendered results
- **Click-Through Rates** — Schema-enhanced SERP performance
- **Indexation Status** — Googlebot crawling, indexing delays
- **Competitive Analysis** — Benchmarking against schema-rich sites

## Workflow Execution

1. Read BMAD config and product brief for context
2. Select schema frameworks and types for implementation
3. Generate JSON-LD code snippets for key schema types
4. Create validation checklists and testing procedures
5. Define performance metrics and monitoring approaches

## Final Output

Write results to `{project-root}/_bmad-output/seo-schema-{date}.md` containing:

### SEO Schema Section
- **Schema markup implementation guide** with examples
- **JSON-LD code snippets** for key types
- **Validation checklist and testing procedures**
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
