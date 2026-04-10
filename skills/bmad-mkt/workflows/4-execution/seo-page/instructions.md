# SEO Page Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Perform single-page SEO analysis using frameworks, on-page optimization, and user intent alignment.

## Content Coverage

### SEO Analysis Frameworks
- **Technical SEO** — Crawlability, indexation, mobile, security
- **On-Page Elements** — Titles, meta descriptions, headers, URLs
- **Content Quality** — Keyword usage, readability, E-E-A-T
- **User Intent Mapping** — Informational, navigational, transactional, commercial

### On-Page Elements
- **Title Tags** — Length, keyword placement, brand inclusion
- **Meta Descriptions** — Click-worthy, keyword-rich, character limits
- **Header Tags** — H1 hierarchy, keyword usage, content structure
- **Image Optimization** — Alt text, file names, compression

### Content Quality
- **Keyword Analysis** — Primary, secondary, semantic keyword usage
- **Readability Assessment** — Grade level, sentence length, structure
- **Content Depth** — Topic coverage, supporting details, comprehensiveness
- **E-E-A-T Alignment** — Experience, Expertise, Authoritativeness, Trustworthiness

### User Intent Alignment
- **Search Query Analysis** — Intent classification, SERP features
- **Content Structure** — FAQ, how-to, listicles, guides
- **Internal Linking** — Contextual links, anchor text, siloing
- **Call-to-Actions** — Conversion opportunities, next steps

## Workflow Execution

1. Read BMAD config and product brief for context
2. Select SEO analysis frameworks and checklists
3. Analyze on-page elements and content quality
4. Map user intent and align content structure
5. Create optimization recommendations and rewriting guidance

## Final Output

Write results to `{project-root}/_bmad-output/seo-page-{date}.md` containing:

### SEO Page Section
- **SEO page analysis report** with findings
- **On-page element optimization recommendations**
- **Content quality assessment and rewriting guidance**
- **User intent mapping and content alignment**

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
