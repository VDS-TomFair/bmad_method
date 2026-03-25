# SEO Hreflang Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Implement hreflang tags for international SEO with proper language/region codes, validation, and cross-domain handling.

## Content Coverage

### Hreflang Implementation
- **Tag Placement** — `<head>` section, HTTP headers, XML sitemap
- **Attribute Syntax** — `hreflang="lang-region"` format
- **Self-Reference Requirement** — Each page must link to itself
- **X-Default Fallback** — Generic landing page for unmatched locales

### Language and Region Codes
- **ISO 639-1 Language Codes** — Two-letter language identifiers
- **ISO 3166-1 Alpha-2 Region Codes** — Two-letter country codes
- **Combined Locale Codes** — `en-US`, `fr-CA`, `de-DE`
- **Code Validation** — Check against official standards

### Cross-Domain and Subdomain Handling
- **Same Domain Implementation** — Subdirectories and subdomains
- **Cross-Domain Setup** — Separate domains per locale
- **Canonical and Hreflang Interaction** — Avoid conflicts
- **Parameter Handling** — UTM, session IDs, tracking

### Error Handling and Common Issues
- **Duplicate Hreflang Tags** — Consolidation strategy
- **Missing Self-References** — Automated detection
- **Incorrect Language Codes** — Validation tools
- **Crawl Budget Impact** — Efficient implementation

## Workflow Execution

1. Read BMAD config and product brief for context
2. Select language and region codes for locales
3. Implement hreflang tags with proper syntax
4. Validate implementation with testing tools
5. Handle cross-domain/subdomain specifics
6. Create error handling and resolution procedures

## Final Output

Write results to `{project-root}/_bmad-output/seo-hreflang-{date}.md` containing:

### SEO Hreflang Section
- **Hreflang implementation guide** with examples
- **Language and region code matrix** by locale
- **Validation checklist and testing procedures** with tools
- **Error handling and common issues resolution** with fixes

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
