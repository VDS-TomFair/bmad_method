# SEO Audit Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Conduct comprehensive SEO audits using frameworks, technical issue identification, and content optimization opportunities.

## Content Coverage

### SEO Audit Frameworks
- **Technical SEO** — Crawlability, indexation, mobile, security
- **On-Page SEO** — Titles, meta descriptions, headers, content
- **Off-Page SEO** — Backlinks, domain authority, citations
- **Content SEO** — Keyword usage, readability, E-E-A-T

### Technical Issues
- **Crawl Errors** — 4xx, 5xx, redirect chains, orphaned pages
- **Indexation Issues** — Noindex, canonicalization, duplicate content
- **Core Web Vitals** — LCP, FID, CLS optimization opportunities
- **Structured Data** — Schema markup implementation gaps

### Content Quality
- **Keyword Analysis** — Primary, secondary, semantic keyword usage
- **Readability Assessment** — Grade level, sentence length, structure
- **Content Gaps** — Missing topics, thin content, cannibalization
- **User Intent Alignment** — Matching search queries to content

### Competitor Analysis
- **SERP Comparison** — Ranking positions, features, gaps
- **Backlink Profile** — Linking domains, anchor text, quality
- **Content Benchmarking** — Topic depth, format variety, freshness
- **Opportunity Mapping** — Untapped keywords, low-hanging fruit

## Workflow Execution

1. Read BMAD config and product brief for context
2. Select SEO audit frameworks and checklists
3. Identify technical SEO issues and content gaps
4. Perform competitor analysis and gap identification
5. Create prioritized recommendations and fixes

## Final Output

Write results to `{project-root}/_bmad-output/seo-audit-{date}.md` containing:

### SEO Audit Section
- **SEO audit report** with findings and severity
- **Technical SEO issues** with prioritized fixes
- **Content quality assessment** and recommendations
- **Competitor analysis and gap identification**

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
