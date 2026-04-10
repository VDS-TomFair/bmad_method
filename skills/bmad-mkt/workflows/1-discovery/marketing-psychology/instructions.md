# Marketing Psychology Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Apply behavioral science principles to marketing decisions using cognitive biases, persuasion principles, and mental models.

## Content Coverage

### Cognitive Biases
- **Anchoring Effect** — First number seen influences all subsequent judgments
- **Loss Aversion** — Losses feel 2x more painful than equivalent gains
- **Social Proof** — People copy the actions of others in uncertain situations
- **Scarcity Principle** — Perceived scarcity increases value perception

### Cialdini's 6 Persuasion Principles
1. **Reciprocity** — People feel obligated to return favors
2. **Commitment** — People want to be consistent with past actions
3. **Social Proof** — People follow what others do
4. **Authority** — People defer to experts
5. **Liking** — People say yes to people they like
6. **Scarcity** — People want what they can't have

### Mental Models for Buying Decisions
- **Default Bias** — People stick with defaults
- **Decoy Effect** — Adding a third option changes preference between two
- **Framing Effect** — Same information presented differently changes choices

## Workflow Execution

1. Read BMAD config and product brief for context
2. Identify 5+ psychological principles relevant to THIS product
3. For each principle:
   - **Describe** the principle with concrete examples
   - **Apply** it to THIS product's specific use case
   - **Suggest** implementation tactics (headline, CTA, page element)

## Final Output

Write results to `{project-root}/_bmad-output/marketing-psychology-{date}.md` containing:

### Psychology Principles Section
- **5+ contextualized principles** — Each with description, product application, implementation suggestion
- **Evidence-based examples** — Cite real experiments or case studies
- **Implementation tactics** — Specific suggestions for applying each principle

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
