<step n="4" goal="Preview Next Epic with Change Detection">

<action>Calculate next epic number: {{next_epic_num}} = {{epic_number}} + 1</action>

<output>
Bob (Scrum Master): "Before we dive into the discussion, let me take a quick look at Epic {{next_epic_num}} to understand what's coming."

Alice (Product Owner): "Good thinking - helps us connect what we learned to what we're about to do."
</output>

<action>Attempt to load next epic using selective loading strategy:</action>

**Try sharded first (more specific):**
<action>Check if file exists: {planning_artifacts}/epic*/epic-{{next_epic_num}}.md</action>

<check if="sharded epic file found">
  <action>Load {planning_artifacts}/*epic*/epic-{{next_epic_num}}.md</action>
  <action>Set {{next_epic_source}} = "sharded"</action>
</check>

**Fallback to whole document:**
<check if="sharded epic not found">
<action>Check if file exists: {planning_artifacts}/epic*.md</action>

  <check if="whole epic file found">
    <action>Load entire epics document</action>
    <action>Extract Epic {{next_epic_num}} section</action>
    <action>Set {{next_epic_source}} = "whole"</action>
  </check>
</check>

<check if="next epic found">
  <action>Analyze next epic for:</action>
  - Epic title and objectives
  - Planned stories and complexity estimates
  - Dependencies on Epic {{epic_number}} work
  - New technical requirements or capabilities needed
  - Potential risks or unknowns
  - Business goals and success criteria

<action>Identify dependencies on completed work:</action>

- What components from Epic {{epic_number}} does Epic {{next_epic_num}} rely on?
- Are all prerequisites complete and stable?
- Any incomplete work that creates blocking dependencies?

<action>Note potential gaps or preparation needed:</action>

- Technical setup required (infrastructure, tools, libraries)
- Knowledge gaps to fill (research, training, spikes)
- Refactoring needed before starting next epic
- Documentation or specifications to create

<action>Check for technical prerequisites:</action>

- APIs or integrations that must be ready
- Data migrations or schema changes needed
- Testing infrastructure requirements
- Deployment or environment setup

  <output>
Bob (Scrum Master): "Alright, I've reviewed Epic {{next_epic_num}}: '{{next_epic_title}}'"

Alice (Product Owner): "What are we looking at?"

Bob (Scrum Master): "{{next_epic_num}} stories planned, building on the {{dependency_description}} from Epic {{epic_number}}."

Charlie (Senior Dev): "Dependencies concern me. Did we finish everything we need for that?"

Bob (Scrum Master): "Good question - that's exactly what we need to explore in this retro."
</output>

<action>Set {{next_epic_exists}} = true</action>
</check>

<check if="next epic NOT found">
  <output>
Bob (Scrum Master): "Hmm, I don't see Epic {{next_epic_num}} defined yet."

Alice (Product Owner): "We might be at the end of the roadmap, or we haven't planned that far ahead yet."

Bob (Scrum Master): "No problem. We'll still do a thorough retro on Epic {{epic_number}}. The lessons will be valuable whenever we plan the next work."
</output>

<action>Set {{next_epic_exists}} = false</action>
</check>

</step>

<step n="5" goal="Initialize Retrospective with Rich Context">

<action>Load agent configurations from {agent_manifest}</action>
<action>Identify which agents participated in Epic {{epic_number}} based on story records</action>
<action>Ensure key roles present: Product Owner, Scrum Master (facilitating), Devs, Testing/QA, Architect</action>

<output>
Bob (Scrum Master): "Alright team, everyone's here. Let me set the stage for our retrospective."

═══════════════════════════════════════════════════════════
🔄 TEAM RETROSPECTIVE - Epic {{epic_number}}: {{epic_title}}
═══════════════════════════════════════════════════════════

Bob (Scrum Master): "Here's what we accomplished together."

**EPIC {{epic_number}} SUMMARY:**

Delivery Metrics:

- Completed: {{completed_stories}}/{{total_stories}} stories ({{completion_percentage}}%)
- Velocity: {{actual_points}} story points{{#if planned_points}} (planned: {{planned_points}}){{/if}}
- Duration: {{actual_sprints}} sprints{{#if planned_sprints}} (planned: {{planned_sprints}}){{/if}}
- Average velocity: {{points_per_sprint}} points/sprint

Quality and Technical:

- Blockers encountered: {{blocker_count}}
- Technical debt items: {{debt_count}}
- Test coverage: {{coverage_info}}
- Production incidents: {{incident_count}}

Business Outcomes:

- Goals achieved: {{goals_met}}/{{total_goals}}
- Success criteria: {{criteria_status}}
- Stakeholder feedback: {{feedback_summary}}

Alice (Product Owner): "Those numbers tell a good story. {{completion_percentage}}% completion is {{#if completion_percentage >= 90}}excellent{{else}}something we should discuss{{/if}}."

Charlie (Senior Dev): "I'm more interested in that technical debt number - {{debt_count}} items is {{#if debt_count > 10}}concerning{{else}}manageable{{/if}}."

Dana (QA Engineer): "{{incident_count}} production incidents - {{#if incident_count == 0}}clean epic!{{else}}we should talk about those{{/if}}."

{{#if next_epic_exists}}
═══════════════════════════════════════════════════════════
**NEXT EPIC PREVIEW:** Epic {{next_epic_num}}: {{next_epic_title}}
═══════════════════════════════════════════════════════════

Dependencies on Epic {{epic_number}}:
{{list_dependencies}}

Preparation Needed:
{{list_preparation_gaps}}

Technical Prerequisites:
{{list_technical_prereqs}}

Bob (Scrum Master): "And here's what's coming next. Epic {{next_epic_num}} builds on what we just finished."

Elena (Junior Dev): "Wow, that's a lot of dependencies on our work."

Charlie (Senior Dev): "Which means we better make sure Epic {{epic_number}} is actually solid before moving on."
{{/if}}

═══════════════════════════════════════════════════════════

Bob (Scrum Master): "Team assembled for this retrospective:"

{{list_participating_agents}}

Bob (Scrum Master): "{user_name}, you're joining us as Project Lead. Your perspective is crucial here."

{user_name} (Project Lead): [Participating in the retrospective]

Bob (Scrum Master): "Our focus today:"

1. Learning from Epic {{epic_number}} execution
   {{#if next_epic_exists}}2. Preparing for Epic {{next_epic_num}} success{{/if}}

Bob (Scrum Master): "Ground rules: psychological safety first. No blame, no judgment. We focus on systems and processes, not individuals. Everyone's voice matters. Specific examples are better than generalizations."

Alice (Product Owner): "And everything shared here stays in this room - unless we decide together to escalate something."

Bob (Scrum Master): "Exactly. {user_name}, any questions before we dive in?"
</output>

<action>WAIT for {user_name} to respond or indicate readiness</action>

</step>


---

**HALT** — Await user response or explicit continue before loading next step.

Next step: {installed_path}/steps/step-04-epic-review.md
