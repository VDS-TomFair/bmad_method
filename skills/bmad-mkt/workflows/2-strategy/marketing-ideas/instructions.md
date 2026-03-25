# Marketing Ideas Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Generate innovative marketing ideas using frameworks, research, and audience insights to drive growth.

## Content Coverage

### Idea Generation Frameworks
- **SCAMPER** — Substitute, Combine, Adapt, Modify, Put to another use, Eliminate, Reverse
- **Jobs-to-be-Done** — Map ideas to specific customer jobs
- **Blue Ocean Strategy** — Create uncontested market spaces
- **TRIZ** — Systematic innovation principles
- **Mind Mapping** — Visual brainstorming techniques

### Market Research and Intelligence
- **Competitive Analysis** — What are competitors doing?
- **Trend Monitoring** — Industry shifts and emerging patterns
- **Customer Feedback** — Interviews, surveys, support tickets
- **Data Analytics** — Website behavior, conversion paths
- **Social Listening** — Brand mentions, community discussions

### Audience Insights Mapping
- **ICP Definition** — Who are we targeting?
- **Pain Point Analysis** — What problems do they face?
- **Job-to-be-Done Mapping** — What are they trying to accomplish?
- **Content Consumption Patterns** — Where do they get information?
- **Purchase Journey Mapping** — Decision-making process

### Business Alignment
- **Goal Integration** — Revenue, growth, retention objectives
- **Resource Constraints** — Budget, team, timeline limitations
- **Brand Consistency** — Tone, values, messaging alignment
- **Cross-Team Coordination** — Sales, product, support alignment

## Workflow Execution

1. Read BMAD config and product brief for context
2. Apply idea generation frameworks to product/audience
3. Conduct market research and competitive intelligence
4. Map audience insights and pain points
5. Align ideas with business goals and constraints

## Final Output

Write results to `{project-root}/_bmad-output/marketing-ideas-{date}.md` containing:

### Marketing Ideas Section
- **List of marketing ideas** with descriptions
- **Prioritization framework** (impact, effort, alignment)
- **Implementation feasibility assessment** (resources, timeline)
- **Alignment with audience needs and business goals** (JTBD, KPIs)

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
