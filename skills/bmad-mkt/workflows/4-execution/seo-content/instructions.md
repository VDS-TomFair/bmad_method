# SEO Content Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Perform content quality assessment using frameworks, E-E-A-T optimization, and AI citation readiness evaluation.

## Content Coverage

### Content Quality Frameworks
- **Readability Metrics** — Flesch-Kincaid, SMOG, Coleman-Liau
- **Keyword Analysis** — Primary, secondary, semantic keyword usage
- **Content Depth** — Topic coverage, supporting details, comprehensiveness
- **Structure Assessment** — Headings, lists, paragraphs, flow

### E-E-A-T Optimization
- **Experience** — First-hand knowledge, case studies, examples
- **Expertise** — Credentials, industry knowledge, author bios
- **Authoritativeness** — Backlinks, mentions, domain authority
- **Trustworthiness** — Security, transparency, contact info

### AI Citation Readiness
- **Passage Citability** — Clear answers, direct quotes, structured data
- **Brand Mentions** — Entity linking, brand name placement
- **Query Coverage** — FAQ sections, how-to guides, definitions
- **Citation Signals** — Domain authority, backlink profile

### Content Scoring
- **Quality Scores** — 1-10 scale for readability, keyword, depth
- **E-E-A-T Scores** — 1-10 scale for each dimension
- **AI Readiness** — Pass/fail for citability, mentions, coverage
- **Improvement Areas** — Specific recommendations for each score

## Workflow Execution

1. Read BMAD config and product brief for context
2. Select content quality frameworks and assessment criteria
3. Evaluate E-E-A-T optimization and AI citation readiness
4. Score content quality and identify improvement areas
5. Create readability and structure improvement recommendations

## Final Output

Write results to `{project-root}/_bmad-output/seo-content-{date}.md` containing:

### SEO Content Section
- **Content quality audit** with scoring
- **E-E-A-T optimization recommendations**
- **AI citation readiness assessment**
- **Readability and structure improvements**

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
