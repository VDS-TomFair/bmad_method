# Copy Editing Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Edit and improve marketing copy for consistency, grammar, and brand voice using frameworks and style guides.

## Content Coverage

### Copy Editing Frameworks
- **Grammar and Spelling Check** — Syntax, punctuation, typos
- **Readability Analysis** — Flesch-Kincaid, Gunning Fog scores
- **Consistency Review** — Terminology, formatting, capitalization
- **Fact Verification** — Claims, statistics, references

### Style Guide Adherence
- **Brand Voice Guidelines** — Tone, personality, messaging
- **Formatting Standards** — Headings, lists, emphasis
- **Terminology Compliance** — Product names, jargon, acronyms
- **Legal and Compliance** — Disclaimers, disclosures

### Readability Improvements
- **Sentence Structure** — Length, complexity, clarity
- **Word Choice** — Jargon reduction, active voice
- **Paragraph Flow** — Logical progression, transitions
- **CTA Optimization** — Placement, clarity, urgency

### Brand Voice Consistency
- **Tone Mapping** — Formal/informal, serious/playful
- **Audience Alignment** — ICP, pain points, JTBD
- **Value Proposition Consistency** — Benefits, differentiators
- **Proof Points Integration** — Testimonials, case studies

## Workflow Execution

1. Read BMAD config and product brief for context
2. Apply editing frameworks and checklists
3. Ensure style guide adherence and brand voice
4. Improve grammar, spelling, and readability
5. Assess brand voice consistency

## Final Output

Write results to `{project-root}/_bmad-output/copy-editing-{date}.md` containing:

### Copy Editing Section
- **Edited copy with tracked changes** and comments
- **Style guide compliance report** with violations
- **Readability score improvements** with before/after
- **Brand voice consistency assessment** with examples

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
