<step n="8" goal="Synthesize Action Items with Significant Change Detection">

<output>
Bob (Scrum Master): "Let's capture concrete action items from everything we've discussed."

Bob (Scrum Master): "I want specific, achievable actions with clear owners. Not vague aspirations."
</output>

<action>Synthesize themes from Epic {{epic_number}} review discussion into actionable improvements</action>

<action>Create specific action items with:</action>

- Clear description of the action
- Assigned owner (specific agent or role)
- Timeline or deadline
- Success criteria (how we'll know it's done)
- Category (process, technical, documentation, team, etc.)

<action>Ensure action items are SMART:</action>

- Specific: Clear and unambiguous
- Measurable: Can verify completion
- Achievable: Realistic given constraints
- Relevant: Addresses real issues from retro
- Time-bound: Has clear deadline

<output>
Bob (Scrum Master): "Based on our discussion, here are the action items I'm proposing..."

═══════════════════════════════════════════════════════════
📝 EPIC {{epic_number}} ACTION ITEMS:
═══════════════════════════════════════════════════════════

**Process Improvements:**

1. {{action_item_1}}
   Owner: {{agent_1}}
   Deadline: {{timeline_1}}
   Success criteria: {{criteria_1}}

2. {{action_item_2}}
   Owner: {{agent_2}}
   Deadline: {{timeline_2}}
   Success criteria: {{criteria_2}}

Charlie (Senior Dev): "I can own action item 1, but {{timeline_1}} is tight. Can we push it to {{alternative_timeline}}?"

Bob (Scrum Master): "What do others think? Does that timing still work?"

Alice (Product Owner): "{{alternative_timeline}} works for me, as long as it's done before Epic {{next_epic_num}} starts."

Bob (Scrum Master): "Agreed. Updated to {{alternative_timeline}}."

**Technical Debt:**

1. {{debt_item_1}}
   Owner: {{agent_3}}
   Priority: {{priority_1}}
   Estimated effort: {{effort_1}}

2. {{debt_item_2}}
   Owner: {{agent_4}}
   Priority: {{priority_2}}
   Estimated effort: {{effort_2}}

Dana (QA Engineer): "For debt item 1, can we prioritize that as high? It caused testing issues in three different stories."

Charlie (Senior Dev): "I marked it medium because {{reasoning}}, but I hear your point."

Bob (Scrum Master): "{user_name}, this is a priority call. Testing impact vs. {{reasoning}} - how do you want to prioritize it?"
</output>

<action>WAIT for {user_name} to help resolve priority discussions</action>

<output>
**Documentation:**
1. {{doc_need_1}}
   Owner: {{agent_5}}
   Deadline: {{timeline_3}}

2. {{doc_need_2}}
   Owner: {{agent_6}}
   Deadline: {{timeline_4}}

**Team Agreements:**

- {{agreement_1}}
- {{agreement_2}}
- {{agreement_3}}

Bob (Scrum Master): "These agreements are how we're committing to work differently going forward."

Elena (Junior Dev): "I like agreement 2 - that would've saved me on Story {{difficult_story_num}}."

═══════════════════════════════════════════════════════════
🚀 EPIC {{next_epic_num}} PREPARATION TASKS:
═══════════════════════════════════════════════════════════

**Technical Setup:**
[ ] {{setup_task_1}}
Owner: {{owner_1}}
Estimated: {{est_1}}

[ ] {{setup_task_2}}
Owner: {{owner_2}}
Estimated: {{est_2}}

**Knowledge Development:**
[ ] {{research_task_1}}
Owner: {{owner_3}}
Estimated: {{est_3}}

**Cleanup/Refactoring:**
[ ] {{refactor_task_1}}
Owner: {{owner_4}}
Estimated: {{est_4}}

**Total Estimated Effort:** {{total_hours}} hours ({{total_days}} days)

═══════════════════════════════════════════════════════════
⚠️ CRITICAL PATH:
═══════════════════════════════════════════════════════════

**Blockers to Resolve Before Epic {{next_epic_num}}:**

1. {{critical_item_1}}
   Owner: {{critical_owner_1}}
   Must complete by: {{critical_deadline_1}}

2. {{critical_item_2}}
   Owner: {{critical_owner_2}}
   Must complete by: {{critical_deadline_2}}
   </output>

<action>CRITICAL ANALYSIS - Detect if discoveries require epic updates</action>

<action>Check if any of the following are true based on retrospective discussion:</action>

- Architectural assumptions from planning proven wrong during Epic {{epic_number}}
- Major scope changes or descoping occurred that affects next epic
- Technical approach needs fundamental change for Epic {{next_epic_num}}
- Dependencies discovered that Epic {{next_epic_num}} doesn't account for
- User needs significantly different than originally understood
- Performance/scalability concerns that affect Epic {{next_epic_num}} design
- Security or compliance issues discovered that change approach
- Integration assumptions proven incorrect
- Team capacity or skill gaps more severe than planned
- Technical debt level unsustainable without intervention

<check if="significant discoveries detected">
  <output>

═══════════════════════════════════════════════════════════
🚨 SIGNIFICANT DISCOVERY ALERT 🚨
═══════════════════════════════════════════════════════════

Bob (Scrum Master): "{user_name}, we need to flag something important."

Bob (Scrum Master): "During Epic {{epic_number}}, the team uncovered findings that may require updating the plan for Epic {{next_epic_num}}."

**Significant Changes Identified:**

1. {{significant_change_1}}
   Impact: {{impact_description_1}}

2. {{significant_change_2}}
   Impact: {{impact_description_2}}

{{#if significant_change_3}} 3. {{significant_change_3}}
Impact: {{impact_description_3}}
{{/if}}

Charlie (Senior Dev): "Yeah, when we discovered {{technical_discovery}}, it fundamentally changed our understanding of {{affected_area}}."

Alice (Product Owner): "And from a product perspective, {{product_discovery}} means Epic {{next_epic_num}}'s stories are based on wrong assumptions."

Dana (QA Engineer): "If we start Epic {{next_epic_num}} as-is, we're going to hit walls fast."

**Impact on Epic {{next_epic_num}}:**

The current plan for Epic {{next_epic_num}} assumes:

- {{wrong_assumption_1}}
- {{wrong_assumption_2}}

But Epic {{epic_number}} revealed:

- {{actual_reality_1}}
- {{actual_reality_2}}

This means Epic {{next_epic_num}} likely needs:
{{list_likely_changes_needed}}

**RECOMMENDED ACTIONS:**

1. Review and update Epic {{next_epic_num}} definition based on new learnings
2. Update affected stories in Epic {{next_epic_num}} to reflect reality
3. Consider updating architecture or technical specifications if applicable
4. Hold alignment session with Product Owner before starting Epic {{next_epic_num}}
   {{#if prd_update_needed}}5. Update PRD sections affected by new understanding{{/if}}

Bob (Scrum Master): "**Epic Update Required**: YES - Schedule epic planning review session"

Bob (Scrum Master): "{user_name}, this is significant. We need to address this before committing to Epic {{next_epic_num}}'s current plan. How do you want to handle it?"
</output>

<action>WAIT for {user_name} to decide on how to handle the significant changes</action>

<action>Add epic review session to critical path if user agrees</action>

  <output>
Alice (Product Owner): "I agree with {user_name}'s approach. Better to adjust the plan now than fail mid-epic."

Charlie (Senior Dev): "This is why retrospectives matter. We caught this before it became a disaster."

Bob (Scrum Master): "Adding to critical path: Epic {{next_epic_num}} planning review session before epic kickoff."
</output>
</check>

<check if="no significant discoveries">
  <output>
Bob (Scrum Master): "Good news - nothing from Epic {{epic_number}} fundamentally changes our plan for Epic {{next_epic_num}}. The plan is still sound."

Alice (Product Owner): "We learned a lot, but the direction is right."
</output>
</check>

<output>
Bob (Scrum Master): "Let me show you the complete action plan..."

Bob (Scrum Master): "That's {{total_action_count}} action items, {{prep_task_count}} preparation tasks, and {{critical_count}} critical path items."

Bob (Scrum Master): "Everyone clear on what they own?"
</output>

<action>Give each agent with assignments a moment to acknowledge their ownership</action>

<action>Ensure {user_name} approves the complete action plan</action>

</step>

<step n="9" goal="Critical Readiness Exploration - Interactive Deep Dive">

<output>
Bob (Scrum Master): "Before we close, I want to do a final readiness check."

Bob (Scrum Master): "Epic {{epic_number}} is marked complete in sprint-status, but is it REALLY done?"

Alice (Product Owner): "What do you mean, Bob?"

Bob (Scrum Master): "I mean truly production-ready, stakeholders happy, no loose ends that'll bite us later."

Bob (Scrum Master): "{user_name}, let's walk through this together."
</output>

<action>Explore testing and quality state through natural conversation</action>

<output>
Bob (Scrum Master): "{user_name}, tell me about the testing for Epic {{epic_number}}. What verification has been done?"
</output>

<action>WAIT for {user_name} to describe testing status</action>

<output>
Dana (QA Engineer): [Responds to what {user_name} shared] "I can add to that - {{additional_testing_context}}."

Dana (QA Engineer): "But honestly, {{testing_concern_if_any}}."

Bob (Scrum Master): "{user_name}, are you confident Epic {{epic_number}} is production-ready from a quality perspective?"
</output>

<action>WAIT for {user_name} to assess quality readiness</action>

<check if="{user_name} expresses concerns">
  <output>
Bob (Scrum Master): "Okay, let's capture that. What specific testing is still needed?"

Dana (QA Engineer): "I can handle {{testing_work_needed}}, estimated {{testing_hours}} hours."

Bob (Scrum Master): "Adding to critical path: Complete {{testing_work_needed}} before Epic {{next_epic_num}}."
</output>
<action>Add testing completion to critical path</action>
</check>

<action>Explore deployment and release status</action>

<output>
Bob (Scrum Master): "{user_name}, what's the deployment status for Epic {{epic_number}}? Is it live in production, scheduled for deployment, or still pending?"
</output>

<action>WAIT for {user_name} to provide deployment status</action>

<check if="not yet deployed">
  <output>
Charlie (Senior Dev): "If it's not deployed yet, we need to factor that into Epic {{next_epic_num}} timing."

Bob (Scrum Master): "{user_name}, when is deployment planned? Does that timing work for starting Epic {{next_epic_num}}?"
</output>

<action>WAIT for {user_name} to clarify deployment timeline</action>

<action>Add deployment milestone to critical path with agreed timeline</action>
</check>

<action>Explore stakeholder acceptance</action>

<output>
Bob (Scrum Master): "{user_name}, have stakeholders seen and accepted the Epic {{epic_number}} deliverables?"

Alice (Product Owner): "This is important - I've seen 'done' epics get rejected by stakeholders and force rework."

Bob (Scrum Master): "{user_name}, any feedback from stakeholders still pending?"
</output>

<action>WAIT for {user_name} to describe stakeholder acceptance status</action>

<check if="acceptance incomplete or feedback pending">
  <output>
Alice (Product Owner): "We should get formal acceptance before moving on. Otherwise Epic {{next_epic_num}} might get interrupted by rework."

Bob (Scrum Master): "{user_name}, how do you want to handle stakeholder acceptance? Should we make it a critical path item?"
</output>

<action>WAIT for {user_name} decision</action>

<action>Add stakeholder acceptance to critical path if user agrees</action>
</check>

<action>Explore technical health and stability</action>

<output>
Bob (Scrum Master): "{user_name}, this is a gut-check question: How does the codebase feel after Epic {{epic_number}}?"

Bob (Scrum Master): "Stable and maintainable? Or are there concerns lurking?"

Charlie (Senior Dev): "Be honest, {user_name}. We've all shipped epics that felt... fragile."
</output>

<action>WAIT for {user_name} to assess codebase health</action>

<check if="{user_name} expresses stability concerns">
  <output>
Charlie (Senior Dev): "Okay, let's dig into that. What's causing those concerns?"

Charlie (Senior Dev): [Helps {user_name} articulate technical concerns]

Bob (Scrum Master): "What would it take to address these concerns and feel confident about stability?"

Charlie (Senior Dev): "I'd say we need {{stability_work_needed}}, roughly {{stability_hours}} hours."

Bob (Scrum Master): "{user_name}, is addressing this stability work worth doing before Epic {{next_epic_num}}?"
</output>

<action>WAIT for {user_name} decision</action>

<action>Add stability work to preparation sprint if user agrees</action>
</check>

<action>Explore unresolved blockers</action>

<output>
Bob (Scrum Master): "{user_name}, are there any unresolved blockers or technical issues from Epic {{epic_number}} that we're carrying forward?"

Dana (QA Engineer): "Things that might create problems for Epic {{next_epic_num}} if we don't deal with them?"

Bob (Scrum Master): "Nothing is off limits here. If there's a problem, we need to know."
</output>

<action>WAIT for {user_name} to surface any blockers</action>

<check if="blockers identified">
  <output>
Bob (Scrum Master): "Let's capture those blockers and figure out how they affect Epic {{next_epic_num}}."

Charlie (Senior Dev): "For {{blocker_1}}, if we leave it unresolved, it'll {{impact_description_1}}."

Alice (Product Owner): "That sounds critical. We need to address that before moving forward."

Bob (Scrum Master): "Agreed. Adding to critical path: Resolve {{blocker_1}} before Epic {{next_epic_num}} kickoff."

Bob (Scrum Master): "Who owns that work?"
</output>

<action>Assign blocker resolution to appropriate agent</action>
<action>Add to critical path with priority and deadline</action>
</check>

<action>Synthesize the readiness assessment</action>

<output>
Bob (Scrum Master): "Okay {user_name}, let me synthesize what we just uncovered..."

**EPIC {{epic_number}} READINESS ASSESSMENT:**

Testing & Quality: {{quality_status}}
{{#if quality_concerns}}⚠️ Action needed: {{quality_action_needed}}{{/if}}

Deployment: {{deployment_status}}
{{#if deployment_pending}}⚠️ Scheduled for: {{deployment_date}}{{/if}}

Stakeholder Acceptance: {{acceptance_status}}
{{#if acceptance_incomplete}}⚠️ Action needed: {{acceptance_action_needed}}{{/if}}

Technical Health: {{stability_status}}
{{#if stability_concerns}}⚠️ Action needed: {{stability_action_needed}}{{/if}}

Unresolved Blockers: {{blocker_status}}
{{#if blockers_exist}}⚠️ Must resolve: {{blocker_list}}{{/if}}

Bob (Scrum Master): "{user_name}, does this assessment match your understanding?"
</output>

<action>WAIT for {user_name} to confirm or correct the assessment</action>

<output>
Bob (Scrum Master): "Based on this assessment, Epic {{epic_number}} is {{#if all_clear}}fully complete and we're clear to proceed{{else}}complete from a story perspective, but we have {{critical_work_count}} critical items before Epic {{next_epic_num}}{{/if}}."

Alice (Product Owner): "This level of thoroughness is why retrospectives are valuable."

Charlie (Senior Dev): "Better to catch this now than three stories into the next epic."
</output>

</step>


---

**HALT** -- Await user response or explicit continue before loading next step.

Next step: {installed_path}/steps/step-07-closure.md
