# SEO Sitemap Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Generate and optimize XML sitemaps with indexation strategy, validation, and search engine submission.

## Content Coverage

### XML Sitemap Generation
- **Sitemap Structure** — XML format, namespace declarations
- **URL Inclusion Rules** — Page types to include/exclude
- **Image and Video Sitemaps** — Media content indexing
- **Multi-Page Sitemaps** — Index files for large sites

### Indexation Strategy
- **Priority Settings** — Priority values (0.0 - 1.0) for page types
- **Change Frequency** — How often content is updated (always, daily, weekly)
- **Last Modified Dates** — Accurate timestamp tracking
- **Canonical URL Handling** — Preferred version selection

### Validation and Submission
- **Sitemap Validator Tools** — XML syntax, Google Search Console
- **Search Engine Submission** — Google, Bing, Yandex portals
- **Robots.txt Integration** — Sitemap directive placement
- **Hreflang and Mobile Sitemaps** — Specialized sitemap types

### Monitoring and Maintenance
- **Automated Generation** — Cron jobs, CI/CD integration
- **Error Detection** — Broken links, missing pages
- **Performance Metrics** — Indexed URLs, crawl stats
- **Update Triggers** — Content changes, new page alerts

## Workflow Execution

1. Read BMAD config and product brief for context
2. Generate XML sitemap structure with inclusion rules
3. Set priority and frequency for page types
4. Validate sitemap with testing tools
5. Submit to search engines and monitor

## Final Output

Write results to `{project-root}/_bmad-output/seo-sitemap-{date}.md` containing:

### SEO Sitemap Section
- **XML sitemap structure and format guidelines** with examples
- **Indexation priority and frequency settings** by page type
- **Validation checklist and submission process** with tools
- **Monitoring and maintenance procedures** with triggers

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
