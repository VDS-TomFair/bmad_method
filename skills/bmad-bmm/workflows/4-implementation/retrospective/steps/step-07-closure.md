<step n="10" goal="Retrospective Closure with Celebration and Commitment">

<output>
Bob (Scrum Master): "We've covered a lot of ground today. Let me bring this retrospective to a close."

═══════════════════════════════════════════════════════════
✅ RETROSPECTIVE COMPLETE
═══════════════════════════════════════════════════════════

Bob (Scrum Master): "Epic {{epic_number}}: {{epic_title}} - REVIEWED"

**Key Takeaways:**

1. {{key_lesson_1}}
2. {{key_lesson_2}}
3. {{key_lesson_3}}
   {{#if key_lesson_4}}4. {{key_lesson_4}}{{/if}}

Alice (Product Owner): "That first takeaway is huge - {{impact_of_lesson_1}}."

Charlie (Senior Dev): "And lesson 2 is something we can apply immediately."

Bob (Scrum Master): "Commitments made today:"

- Action Items: {{action_count}}
- Preparation Tasks: {{prep_task_count}}
- Critical Path Items: {{critical_count}}

Dana (QA Engineer): "That's a lot of commitments. We need to actually follow through this time."

Bob (Scrum Master): "Agreed. Which is why we'll review these action items in our next standup."

═══════════════════════════════════════════════════════════
🎯 NEXT STEPS:
═══════════════════════════════════════════════════════════

1. Execute Preparation Sprint (Est: {{prep_days}} days)
2. Complete Critical Path items before Epic {{next_epic_num}}
3. Review action items in next standup
   {{#if epic_update_needed}}4. Hold Epic {{next_epic_num}} planning review session{{else}}4. Begin Epic {{next_epic_num}} planning when preparation complete{{/if}}

Elena (Junior Dev): "{{prep_days}} days of prep work is significant, but necessary."

Alice (Product Owner): "I'll communicate the timeline to stakeholders. They'll understand if we frame it as 'ensuring Epic {{next_epic_num}} success.'"

═══════════════════════════════════════════════════════════

Bob (Scrum Master): "Before we wrap, I want to take a moment to acknowledge the team."

Bob (Scrum Master): "Epic {{epic_number}} delivered {{completed_stories}} stories with {{velocity_description}} velocity. We overcame {{blocker_count}} blockers. We learned a lot. That's real work by real people."

Charlie (Senior Dev): "Hear, hear."

Alice (Product Owner): "I'm proud of what we shipped."

Dana (QA Engineer): "And I'm excited about Epic {{next_epic_num}} - especially now that we're prepared for it."

Bob (Scrum Master): "{user_name}, any final thoughts before we close?"
</output>

<action>WAIT for {user_name} to share final reflections</action>

<output>
Bob (Scrum Master): [Acknowledges what {user_name} shared] "Thank you for that, {user_name}."

Bob (Scrum Master): "Alright team - great work today. We learned a lot from Epic {{epic_number}}. Let's use these insights to make Epic {{next_epic_num}} even better."

Bob (Scrum Master): "See you all when prep work is done. Meeting adjourned!"

═══════════════════════════════════════════════════════════
</output>

<action>Prepare to save retrospective summary document</action>

</step>

<step n="11" goal="Save Retrospective and Update Sprint Status">

<action>Ensure retrospectives folder exists: {implementation_artifacts}</action>
<action>Create folder if it doesn't exist</action>

<action>Generate comprehensive retrospective summary document including:</action>

- Epic summary and metrics
- Team participants
- Successes and strengths identified
- Challenges and growth areas
- Key insights and learnings
- Previous retro follow-through analysis (if applicable)
- Next epic preview and dependencies
- Action items with owners and timelines
- Preparation tasks for next epic
- Critical path items
- Significant discoveries and epic update recommendations (if any)
- Readiness assessment
- Commitments and next steps

<action>Format retrospective document as readable markdown with clear sections</action>
<action>Set filename: {implementation_artifacts}/epic-{{epic_number}}-retro-{date}.md</action>
<action>Save retrospective document</action>

<output>
✅ Retrospective document saved: {implementation_artifacts}/epic-{{epic_number}}-retro-{date}.md
</output>

<action>Update {sprint_status_file} to mark retrospective as completed</action>

<action>Load the FULL file: {sprint_status_file}</action>
<action>Find development_status key "epic-{{epic_number}}-retrospective"</action>
<action>Verify current status (typically "optional" or "pending")</action>
<action>Update development_status["epic-{{epic_number}}-retrospective"] = "done"</action>
<action>Save file, preserving ALL comments and structure including STATUS DEFINITIONS</action>

<check if="update successful">
  <output>
✅ Retrospective marked as completed in {sprint_status_file}

Retrospective key: epic-{{epic_number}}-retrospective
Status: {{previous_status}} → done
</output>
</check>

<check if="retrospective key not found">
  <output>
⚠️ Could not update retrospective status: epic-{{epic_number}}-retrospective not found in {sprint_status_file}

Retrospective document was saved successfully, but {sprint_status_file} may need manual update.
</output>
</check>

</step>

<step n="12" goal="Final Summary and Handoff">

<output>
**✅ Retrospective Complete, {user_name}!**

**Epic Review:**

- Epic {{epic_number}}: {{epic_title}} reviewed
- Retrospective Status: completed
- Retrospective saved: {implementation_artifacts}/epic-{{epic_number}}-retro-{date}.md

**Commitments Made:**

- Action Items: {{action_count}}
- Preparation Tasks: {{prep_task_count}}
- Critical Path Items: {{critical_count}}

**Next Steps:**

1. **Review retrospective summary**: {implementation_artifacts}/epic-{{epic_number}}-retro-{date}.md

2. **Execute preparation sprint** (Est: {{prep_days}} days)
   - Complete {{critical_count}} critical path items
   - Execute {{prep_task_count}} preparation tasks
   - Verify all action items are in progress

3. **Review action items in next standup**
   - Ensure ownership is clear
   - Track progress on commitments
   - Adjust timelines if needed

{{#if epic_update_needed}} 4. **IMPORTANT: Schedule Epic {{next_epic_num}} planning review session**

- Significant discoveries from Epic {{epic_number}} require epic updates
- Review and update affected stories
- Align team on revised approach
- Do NOT start Epic {{next_epic_num}} until review is complete
  {{else}}

4. **Begin Epic {{next_epic_num}} when ready**
   - Start creating stories with SM agent's `create-story`
   - Epic will be marked as `in-progress` automatically when first story is created
   - Ensure all critical path items are done first
     {{/if}}

**Team Performance:**
Epic {{epic_number}} delivered {{completed_stories}} stories with {{velocity_summary}}. The retrospective surfaced {{insight_count}} key insights and {{significant_discovery_count}} significant discoveries. The team is well-positioned for Epic {{next_epic_num}} success.

{{#if significant_discovery_count > 0}}
⚠️ **REMINDER**: Epic update required before starting Epic {{next_epic_num}}
{{/if}}

---

Bob (Scrum Master): "Great session today, {user_name}. The team did excellent work."

Alice (Product Owner): "See you at epic planning!"

Charlie (Senior Dev): "Time to knock out that prep work."

</output>

</step>

</workflow>

<facilitation-guidelines>
<guideline>PARTY MODE REQUIRED: All agent dialogue uses "Name (Role): dialogue" format</guideline>
<guideline>Scrum Master maintains psychological safety throughout - no blame or judgment</guideline>
<guideline>Focus on systems and processes, not individual performance</guideline>
<guideline>Create authentic team dynamics: disagreements, diverse perspectives, emotions</guideline>
<guideline>User ({user_name}) is active participant, not passive observer</guideline>
<guideline>Encourage specific examples over general statements</guideline>
<guideline>Balance celebration of wins with honest assessment of challenges</guideline>
<guideline>Ensure every voice is heard - all agents contribute</guideline>
<guideline>Action items must be specific, achievable, and owned</guideline>
<guideline>Forward-looking mindset - how do we improve for next epic?</guideline>
<guideline>Intent-based facilitation, not scripted phrases</guideline>
<guideline>Deep story analysis provides rich material for discussion</guideline>
<guideline>Previous retro integration creates accountability and continuity</guideline>
<guideline>Significant change detection prevents epic misalignment</guideline>
<guideline>Critical verification prevents starting next epic prematurely</guideline>
<guideline>Document everything - retrospective insights are valuable for future reference</guideline>
<guideline>Two-part structure ensures both reflection AND preparation</guideline>
</facilitation-guidelines>

---

**HALT** -- Workflow complete. Await user instruction.
