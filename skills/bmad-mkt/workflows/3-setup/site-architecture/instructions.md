# Site Architecture Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Design page hierarchy, URL structure, and internal linking strategy to optimize SEO and user experience.

## Content Coverage

### Page Hierarchy
- **Homepage Structure** — Value proposition, navigation, CTAs
- **Primary Category Pages** — Core topic silos and clusters
- **Secondary Subcategory Pages** — Supporting topics and articles
- **Auxiliary Pages** — About, Contact, Privacy, Terms

### URL Structure
- **Directory Naming Conventions** — Consistent, descriptive, keyword-rich
- **File Naming Standards** — Lowercase, hyphens, no stop words
- **Parameter Handling** — Tracking, sorting, filtering best practices
- **Canonicalization Strategy** —-www, https, trailing slash consistency

### Internal Linking
- **Hub-and-Spoke Model** — Pillar pages linking to cluster content
- **Contextual Cross-Linking** — Related content suggestions
- **Navigation Menu Design** — Primary, secondary, footer menus
- **Breadcrumb Implementation** — Hierarchical path display

### Content Type Mapping
- **Page Templates** — Blog, guide, case study, product, landing
- **Content Format Standards** — Headings, lists, images, CTAs
- **Metadata Requirements** — Title tags, meta descriptions, alt text
- **Schema Markup Integration** — Article, FAQ, HowTo, Product

## Workflow Execution

1. Read BMAD config and product brief for context
2. Design page hierarchy with sitemap structure
3. Define URL structure and naming conventions
4. Create internal linking patterns and navigation
5. Map content types to page templates

## Final Output

Write results to `{project-root}/_bmad-output/site-architecture-{date}.md` containing:

### Site Architecture Section
- **Site map with page hierarchy** — Visual and text representations
- **URL structure guidelines** — Naming conventions and examples
- **Internal linking patterns** — Hub-and-spoke, cross-linking
- **Content type assignments** — Templates and metadata

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
