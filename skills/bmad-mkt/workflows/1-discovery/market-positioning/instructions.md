# Market Positioning Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Workflow Execution

Execute these steps in order from the `steps/` directory:

1. **step-01-context-gathering.md** — Read BMAD config and product brief
2. **step-02-icp-analysis.md** — Define Ideal Customer Profile with JTBD evidence
3. **step-03-positioning-statement.md** — Craft value proposition with competitive moat
4. **step-04-competitive-mapping.md** — Validate positioning against Porter's Five Forces

## Final Output

Write results to `{project-root}/_bmad-output/marketing-positioning-{date}.md` containing:

- **ICP definition** (≥3 specific attributes with JTBD evidence)
- **Value proposition statement** (one clear sentence)
- **Competitive differentiation** (≥3 specific differentiators with evidence)

## Content Adaptation Compliance

These files comply with BMAD Content Adaptation rules:

- CA-1: No persona instructions like "You are an expert" 
- CA-2: No references to `product-marketing-context.md`
- CA-3: All paths use BMAD aliases ({project-root}, {skill-dir})
- CA-4: Proper BMAD workflow format (instructions.md + steps/)
- CA-5: CLI tools use `node {skill-dir}/tools/clis/<tool>.js` pattern
- CA-6: BMAD frontmatter in workflow.yaml
- CA-7: Source attribution preserved in workflow.yaml
- CA-8: No external API dependencies (web access only)
