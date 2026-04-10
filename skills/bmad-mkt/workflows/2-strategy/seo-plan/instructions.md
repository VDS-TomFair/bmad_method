# SEO Plan Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Develop a comprehensive SEO strategy using keyword research, content planning, and technical optimization to improve organic visibility.

## Content Coverage

### Keyword Research and Analysis
- **Primary Keyword Selection** — High-volume, product-aligned terms
- **Secondary Keyword Clustering** — Supporting long-tail and intent-based terms
- **Competitor Keyword Gap Analysis** — Uncovered opportunities
- **Keyword Difficulty and Opportunity Scoring** — Prioritization framework

### Content Gap Analysis
- **Existing Content Inventory** — URLs, topics, performance metrics
- **Topic Cluster Mapping** — Pillar pages with subtopic links
- **Content Silo Structure** — Logical grouping for SEO and user experience
- **Internal Linking Opportunities** — Hub-and-spoke navigation patterns

### SEO Audit Integration
- **Technical Crawl Issues** — Redirects, broken links, indexation
- **On-Page Optimization Needs** — Title tags, meta descriptions, headers
- **Content Quality Benchmarks** — E-E-A-T compliance, readability
- **Performance and Core Web Vitals** — Speed, CLS, mobile-first

### Technical SEO Requirements
- **Indexing Strategy** — robots.txt, sitemap.xml, canonical tags
- **Structured Data Implementation** — Schema markup for rich results
- **International SEO** — hreflang tags for multi-language
- **Security and Accessibility** — HTTPS, alt text, ARIA labels

## Workflow Execution

1. Read BMAD config and product brief for context
2. Conduct keyword research and analysis
3. Perform content gap analysis and cluster mapping
4. Integrate SEO audit findings
5. Define technical SEO requirements

## Final Output

Write results to `{project-root}/_bmad-output/seo-plan-{date}.md` containing:

### SEO Plan Section
- **SEO keyword strategy** with primary and secondary keywords
- **Content plan** with topic clusters and pillar pages
- **Technical SEO requirements** and implementation plan
- **Success metrics and KPI definitions** with targets

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
