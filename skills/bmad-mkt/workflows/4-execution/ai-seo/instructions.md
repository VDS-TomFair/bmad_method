# AI SEO Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Optimize content for AI search engines using strategies, citation optimization, and passage-level techniques.

## Content Coverage

### AI SEO Strategies
- **Search Engine Optimization** — Google SGE, Perplexity, Claude, ChatGPT
- **Citation Optimization** — Brand mentions, passage citability, llms.txt
- **Content Structure** — FAQ sections, how-to guides, semantic clustering
- **Technical Implementation** — Schema markup, structured data, indexing

### Content Optimization
- **Passage-Level SEO** — Keyphrase density, entity linking, context
- **E-E-A-T Alignment** — Experience, Expertise, Authoritativeness, Trustworthiness
- **AI Readability** — Concise language, clear structure, direct answers
- **Zero-Click Optimization** — Featured snippets, knowledge panels

### LLM Optimization
- **Crawler Accessibility** — JavaScript rendering, dynamic content
- **Citation Signals** — Domain authority, backlink profile, brand mentions
- **Prompt Engineering** — Query-response patterns, intent matching
- **Performance Monitoring** — Visibility metrics, citation tracking

### AI SEO Metrics
- **Visibility Scores** — AI search rankings, citation frequency
- **Engagement Patterns** — Click-through rates, time-on-page
- **Content Performance** — Query coverage, answer quality
- **Competitive Analysis** — Benchmarking against AI-ready sites

## Workflow Execution

1. Read BMAD config and product brief for context
2. Select AI SEO strategies and optimization techniques
3. Identify content optimization opportunities for AI search
4. Develop citation and passage optimization recommendations
5. Create performance metrics and monitoring approaches

## Final Output

Write results to `{project-root}/_bmad-output/ai-seo-{date}.md` containing:

### AI SEO Section
- **AI SEO strategy framework** with techniques
- **Content optimization guidelines** for AI search
- **Citation and passage optimization recommendations**
- **Performance metrics and monitoring approaches** with tools

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
