# Copywriting Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Create compelling marketing copy for key pages using frameworks, audience insights, and value propositions.

## Content Coverage

### Copywriting Frameworks
- **AIDA Model** — Attention, Interest, Desire, Action
- **PAS Formula** — Problem, Agitation, Solution
- **FAB Method** — Features, Advantages, Benefits
- **4Cs Framework** — Clear, Concise, Compelling, Credible

### Audience Messaging
- **ICP Definition** — Who are we targeting?
- **Pain Point Mapping** — What problems do they face?
- **Job-to-be-Done Alignment** — What are they trying to accomplish?
- **Proof Points** — Evidence of value and results

### Value Proposition
- **Core Messaging** — One-sentence positioning
- **Differentiators** — What sets us apart?
- **Quantified Outcomes** — Measurable results
- **Social Proof** — Testimonials, case studies

### Content Structure
- **Headline Writing** — Magnetic, benefit-driven
- **Subheadline Support** — Context and explanation
- **Body Copy Flow** — Logical progression of ideas
- **Call-to-Action Placement** — Strategic positioning

## Workflow Execution

1. Read BMAD config and product brief for context
2. Apply copywriting frameworks to page types
3. Develop audience messaging and value props
4. Structure content with headlines and CTAs
5. Write final copy for key pages

## Final Output

Write results to `{project-root}/_bmad-output/copywriting-{date}.md` containing:

### Copywriting Section
- **Copy for key pages** (homepage, product, pricing)
- **Value proposition statements** with differentiators
- **Call-to-action recommendations** by page type
- **Tone of voice guidelines** with examples

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
