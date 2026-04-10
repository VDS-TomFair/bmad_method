# Cold Email Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Create high-conversion cold email campaigns using outreach frameworks, prospect research, and personalization techniques.

## Content Coverage

### Cold Email Frameworks
- **SPICC Framework** — Situation, Problem, Implication, Call-to-action, Curiosity
- **3-Step Formula** — Hook, value proposition, CTA
- **Pain-Agitate-Solution** — Identify problem, amplify pain, offer solution
- **Mutual Friend Approach** — Shared connections, referrals

### Prospect Research
- **ICP Profiling** — Job title, industry, company size
- **Personal Trigger Mapping** — Recent news, social activity, events
- **Account Mapping** — Hierarchy, decision-makers, influencers
- **Tool Integration** — LinkedIn Sales Navigator, Clearbit, Apollo

### Subject Line Techniques
- **Personalization Tokens** — Name, company, location
- **Curiosity Gaps** — Questions, teasers, exclusivity
- **Urgency and Scarcity** — Limited time, expiring offers
- **Benefit-Driven** — Value propositions, outcomes

### Copywriting Best Practices
- **Value Proposition Alignment** — JTBD, benefits
- **Social Proof Integration** — Testimonials, case studies
- **CTA Optimization** — Placement, clarity, urgency
- **Tone Mapping** — Formal/informal, serious/playful

## Workflow Execution

1. Read BMAD config and product brief for context
2. Select cold email framework and outreach strategy
3. Conduct prospect research with ICP profiling
4. Develop subject lines with personalization tokens
5. Write copy with tone mapping and value alignment

## Final Output

Write results to `{project-root}/_bmad-output/cold-email-{date}.md` containing:

### Cold Email Section
- **Cold email templates** with variations (short, long, referral)
- **Prospect research methodology** with tools and triggers
- **Personalization variables and triggers** for each template
- **Follow-up sequence structure** with timing and content

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
