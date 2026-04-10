# Community Marketing Workflow Instructions

## Input Context

Read these BMAD configuration files for context:

1. `{project-root}/instructions/01-bmad-config.md` — Project aliases and settings
2. `{project-root}/instructions/02-bmad-state.md` — Current phase and artifacts
3. `{project-root}/_bmad-output/planning-artifacts/product-brief-*.md` — Product context

## Task Overview

Build and leverage online communities to drive product growth and brand loyalty. Covers community strategy, launch playbooks, ambassador programs, platform selection, and health metrics.

## Trigger

- User wants to create a community strategy
- Need to grow a Discord, Slack, or online community
- Building brand advocates or ambassador programs
- Community-led growth initiatives
- Forum or subreddit management

## Inputs

### Required
- Product or brand identity
- Community platform(s) in play (Discord, Slack, Circle, Reddit, Facebook Groups, forum)
- Community stage (pre-launch, 0-100 members, 100-1k, scaling, or established)
- Primary community goal (retention, activation, word-of-mouth, support deflection, product feedback, revenue)
- Ideal community member profile

### Recommended
- Existing community metrics (if any)
- Brand guidelines and tone of voice
- Prior community engagement results
- Competitive community examples

## Content Coverage

### Community Strategy Principles

**Build around shared identity, not just a product**
- Strongest communities are built around who members *are* or aspire to be
- Members join because of the product but stay because of the people and identity
- Always define: What identity does this community reinforce for its members?

**Value must flow to members first**
- Every touchpoint answers: What does the member get from this?
- Exclusive knowledge, peer connections, recognition, product influence, career opportunities

**The Community Flywheel**
```
Members join → get value → engage → create content/help others
    ↑                                          ↓
    ←←←←← new members discover the community ←←
```
- Design for the flywheel from day one
- Every decision asks: Does this accelerate the loop or slow it down?

### Playbooks by Goal

**Launching a Community from Zero**
1. Recruit 20-50 founding members manually (DM most engaged users, beta testers, fans)
2. Set the culture explicitly — community guidelines that describe the *vibe*, not just rules
3. Seed conversations before launch — 5-10 posts modeling desired behavior
4. Do things that don't scale — reply to every post, welcome every new member by name
5. Define your core loop — what weekly action do you want members to take?

**Growing an Existing Community**
1. Audit where members drop off (joining but not posting? posting once then disappearing?)
2. Create a new member journey (pinned welcome post, #introduce-yourself, DM, clear "start here")
3. Surface member wins publicly (user projects, testimonials, milestones)
4. Run recurring community rituals (weekly threads, monthly AMAs, seasonal challenges)
5. Identify and invest in power users (1% of members generate 90% of value)

**Building a Brand Ambassador / Advocate Program**
1. Identify candidates (people who already recommend you unprompted)
2. Make the ask personal (1:1 outreach, explain why you chose them)
3. Offer meaningful benefits (exclusive access, swag, revenue share, public recognition)
4. Give them tools and content (referral links, shareable assets, talking points, private channel)
5. Measure and iterate (track referral traffic, signups, engagement driven by advocates)

**Community-Led Support (Deflection + Retention)**
1. Create searchable knowledge base from top community questions
2. Recognize members who help others (badges, leaderboards, shoutouts)
3. Close the loop with product (when community feedback drives a change, announce and credit members)
4. Monitor sentiment weekly (look for patterns before they become churn signals)

### Platform Selection Guide

| Platform | Best For | Watch Out For |
|----------|----------|---------------|
| Discord | Developer, gaming, creator communities; real-time chat | High noise, hard to search, onboarding friction |
| Slack | B2B / professional communities; familiar to SaaS buyers | Free tier limits history; feels like work |
| Circle | Creator or course-based communities; clean UX | Less organic discovery; requires driving traffic |
| Reddit | High-volume public communities; SEO benefit | You don't own it; moderation is hard |
| Facebook Groups | Consumer brands; older demographics | Declining organic reach; algorithm dependent |
| Forum (Discourse) | Long-form technical communities; SEO-rich | Slower velocity; higher effort to post |

### Community Health Metrics

Track weekly:
- **DAU/MAU ratio** — Stickiness. Above 20% is healthy
- **New member post rate** — % of new members who post within 7 days of joining
- **Thread reply rate** — % of posts receiving at least one reply
- **Churn/lurker ratio** — Members who joined but haven't posted in 30+ days
- **Content created by non-staff** — % of posts not written by company team

**Warning signs:**
- Most posts are from the company team, not members
- Questions go unanswered for >24 hours
- Same 5 people account for 80%+ of engagement
- New members stop posting after their intro message

## Workflow Execution

1. Read BMAD config and product brief for context
2. Assess community situation (platform, stage, goal, ideal member)
3. Select appropriate playbook (launch, grow, ambassador, support)
4. Apply strategy principles (shared identity, value flow, flywheel design)
5. Design channel architecture and member journey
6. Define health metrics dashboard with targets
7. Create implementation plan with timeline

## Final Output

Write results to `{project-root}/_bmad-output/community-marketing-{date}.md` containing:

### Deliverables
One or more of these based on user needs:
- **Community Strategy Doc**: Platform choice, identity definition, core loop, 90-day launch/growth plan
- **Channel Architecture**: Recommended channels/categories with purpose and posting guidelines
- **New Member Journey**: Welcome sequence with pinned post, DM template, first-week prompts
- **Ambassador Program Brief**: Criteria, benefits, outreach template, tracking plan
- **Health Audit Report**: Current metrics, diagnosis, top 3 priorities to fix

## Content Adaptation Compliance

These files comply with BMAD Content Adaptation rules:

- CA-1: No persona instructions like "You are an expert"
- CA-2: No references to `product-marketing-context.md`
- CA-3: All paths use BMAD aliases ({project-root}, {skill-dir})
- CA-4: Proper Standard tier BMAD format (instructions.md only)
- CA-5: CLI tools use `node {skill-dir}/tools/clis/<tool>.js` pattern
