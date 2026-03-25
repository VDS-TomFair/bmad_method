# SEO Technical Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Conduct comprehensive technical SEO audit and optimization to improve crawlability, indexation, and Core Web Vitals.

## Content Coverage

### Technical SEO Audit Categories
- **Crawlability Issues** — Robots.txt, sitemap.xml, crawl errors
- **Indexation Problems** — Noindex, canonicalization, duplicate content
- **Mobile Optimization** — Responsive design, mobile usability errors
- **HTTPS and Security** — SSL certificate, mixed content, HSTS

### Crawlability and Indexation
- **Robots.txt Analysis** — Allow/disallow rules, crawl budget
- **Sitemap Validation** — XML structure, URL inclusion/exclusion
- **Redirect Chain Resolution** — 301/302/404 error handling
- **Pagination and Faceted Navigation** — rel=prev/next, nofollow

### Core Web Vitals Optimization
- **Largest Contentful Paint (LCP)** — Image optimization, lazy loading
- **First Input Delay (FID)** — JavaScript optimization, compression
- **Cumulative Layout Shift (CLS)** — Font loading, reserved space
- **Performance Budgeting** — Page weight limits, resource prioritization

### Structured Data Implementation
- **Schema Markup Types** — Article, FAQ, HowTo, Product, Organization
- **JSON-LD Implementation** — Structured data format best practices
- **Rich Results Validation** — Google Rich Results Test compliance
- **Breadcrumb and Sitelinks** — Search appearance optimization

## Workflow Execution

1. Read BMAD config and product brief for context
2. Conduct technical SEO audit across all categories
3. Identify crawl errors and indexation issues
4. Optimize Core Web Vitals metrics
5. Implement structured data markup

## Final Output

Write results to `{project-root}/_bmad-output/seo-technical-{date}.md` containing:

### SEO Technical Section
- **Technical SEO audit report** with findings and severity
- **Crawl error resolution plan** with prioritized fixes
- **Core Web Vitals improvement recommendations** with impact
- **Structured data implementation guide** with examples

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
