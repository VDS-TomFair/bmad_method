# SEO Competitor Pages Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Create competitor comparison and alternative pages that rank for competitive search terms, provide genuine value to evaluators, and position your product effectively. Covers four page formats with modular content architecture.

## Content Coverage

### Initial Assessment
Before creating competitor pages, gather:
- **Your Product**: Core value proposition, key differentiators, ICP, pricing model, strengths and honest weaknesses
- **Competitive Landscape**: Direct competitors, indirect/adjacent competitors, market positioning, search volume for competitor terms
- **Goals**: SEO traffic capture, sales enablement, conversion from competitor users, brand positioning

### Page Formats

**Format 1: [Competitor] Alternative (Singular)**
- Search intent: User actively looking to switch
- URL pattern: `/alternatives/[competitor]` or `/[competitor]-alternative`
- Target keywords: "[Competitor] alternative", "alternative to [Competitor]"
- Structure: Why switch → Summary positioning → Detailed comparison → Who should switch → Migration path → Social proof → CTA

**Format 2: [Competitor] Alternatives (Plural)**
- Search intent: User researching options, earlier in journey
- URL pattern: `/alternatives/[competitor]-alternatives`
- Target keywords: "[Competitor] alternatives", "best [Competitor] alternatives"
- Structure: Common pain points → Evaluation criteria → List of 4-7 real alternatives → Comparison table → Detailed breakdown → Recommendation by use case → CTA
- Include real alternatives — genuine helpfulness builds trust and ranks better

**Format 3: You vs [Competitor]**
- Search intent: Direct comparison
- URL pattern: `/vs/[competitor]` or `/compare/[you]-vs-[competitor]`
- Target keywords: "[You] vs [Competitor]", "[Competitor] vs [You]"
- Structure: TL;DR summary → At-a-glance table → Detailed comparison by category → Who each is best for → Customer testimonials → Migration support → CTA

**Format 4: [Competitor A] vs [Competitor B]**
- Search intent: User comparing two competitors (not you directly)
- URL pattern: `/compare/[competitor-a]-vs-[competitor-b]`
- Structure: Overview of both → Comparison by category → Who each is best for → The third option (introduce yourself) → Three-way comparison table → CTA
- Captures search traffic for competitor terms, positions you as knowledgeable

### Core Principles
- **Honesty Builds Trust**: Acknowledge competitor strengths, be accurate about limitations, don't misrepresent features
- **Depth Over Surface**: Go beyond feature checklists — explain *why* differences matter, include use cases and scenarios
- **Help Them Decide**: Different tools fit different needs — be clear about who you're best for and who the competitor is best for
- **Modular Content Architecture**: Centralize competitor data, single source of truth per competitor, updates propagate to all pages

### Essential Sections
- **TL;DR Summary**: Quick summary for scanners — key differences in 2-3 sentences
- **Paragraph Comparisons**: For each dimension, explain the differences and when each matters
- **Feature Comparison**: Describe how each handles it, list strengths and limitations, give bottom line recommendation
- **Pricing Comparison**: Tier-by-tier comparison, what's included, hidden costs, total cost calculation for sample team size
- **Who It's For**: Explicit about ideal customer for each option
- **Migration Section**: What transfers, what needs reconfiguration, support offered, quotes from switchers

### SEO Considerations

| Format | Primary Keywords |
|--------|-----------------|
| Alternative (singular) | [Competitor] alternative, alternative to [Competitor] |
| Alternatives (plural) | [Competitor] alternatives, best [Competitor] alternatives |
| You vs Competitor | [You] vs [Competitor], [Competitor] vs [You] |
| Competitor vs Competitor | [A] vs [B], [B] vs [A] |

- Link between related competitor pages
- Link from feature pages to relevant comparisons
- Create hub page linking to all competitor content
- Consider FAQ schema for common questions

### Research Process
For each competitor:
1. **Product research**: Use the product, document features/UX/limitations
2. **Pricing research**: Current pricing, what's included, hidden costs
3. **Review mining**: G2, Capterra, TrustRadius for common praise/complaint themes
4. **Customer feedback**: Talk to customers who switched (both directions)
5. **Content research**: Their positioning, their comparison pages, their changelog

Ongoing updates:
- Quarterly: Verify pricing, check for major feature changes
- When notified: Customer mentions competitor change
- Annually: Full refresh of all competitor data

## Workflow Execution

1. Read BMAD config and product brief for context
2. Gather initial assessment data (product, landscape, goals)
3. Identify top competitors by search volume and strategic importance
4. Create competitor data profiles for each (centralized, modular)
5. Select page format(s) based on keyword opportunity
6. Write page content following format-specific structure
7. Apply SEO optimization (keywords, internal links, schema)
8. Prioritize page set based on search volume and conversion potential

## Final Output

Write results to `{project-root}/_bmad-output/seo-competitor-pages-{date}.md` containing:

### Deliverables
- **Competitor Data File**: Complete competitor profile in structured format for each competitor
- **Page Content**: For each page — URL, meta tags, full page copy organized by section, comparison tables, CTAs
- **Page Set Plan**: Recommended pages to create with priority order based on search volume
- **Internal Linking Map**: How competitor pages connect to each other and to feature pages

## Content Adaptation Compliance

These files comply with BMAD Content Adaptation rules:

- CA-1: No persona instructions like "You are an expert"
- CA-2: No references to `product-marketing-context.md`
- CA-3: All paths use BMAD aliases ({project-root}, {skill-dir})
- CA-4: Proper Standard tier BMAD format (instructions.md only)
- CA-5: CLI tools use `node {skill-dir}/tools/clis/<tool>.js` pattern
