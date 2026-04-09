<step n="4" goal="Generate Sprint Change Proposal">
<action>Compile comprehensive Sprint Change Proposal document with following sections:</action>

<action>Section 1: Issue Summary</action>

- Clear problem statement describing what triggered the change
- Context about when/how the issue was discovered
- Evidence or examples demonstrating the issue

<action>Section 2: Impact Analysis</action>

- Epic Impact: Which epics are affected and how
- Story Impact: Current and future stories requiring changes
- Artifact Conflicts: PRD, Architecture, UI/UX documents needing updates
- Technical Impact: Code, infrastructure, or deployment implications

<action>Section 3: Recommended Approach</action>

- Present chosen path forward from checklist evaluation:
  - Direct Adjustment: Modify/add stories within existing plan
  - Potential Rollback: Revert completed work to simplify resolution
  - MVP Review: Reduce scope or modify goals
- Provide clear rationale for recommendation
- Include effort estimate, risk assessment, and timeline impact

<action>Section 4: Detailed Change Proposals</action>

- Include all refined edit proposals from Step 3
- Group by artifact type (Stories, PRD, Architecture, UI/UX)
- Ensure each change includes before/after and justification

<action>Section 5: Implementation Handoff</action>

- Categorize change scope:
  - Minor: Direct implementation by dev team
  - Moderate: Backlog reorganization needed (PO/SM)
  - Major: Fundamental replan required (PM/Architect)
- Specify handoff recipients and their responsibilities
- Define success criteria for implementation

<action>Present complete Sprint Change Proposal to user</action>
<action>Write Sprint Change Proposal document to {default_output_file}</action>
<ask>Review complete proposal. Continue [c] or Edit [e]?</ask>
</step>

<step n="5" goal="Finalize and Route for Implementation">
<action>Get explicit user approval for complete proposal</action>
<ask>Do you approve this Sprint Change Proposal for implementation? (yes/no/revise)</ask>

<check if="no or revise">
  <action>Gather specific feedback on what needs adjustment</action>
  <action>Return to appropriate step to address concerns</action>
  <goto step="3">If changes needed to edit proposals</goto>
  <goto step="4">If changes needed to overall proposal structure</goto>

</check>

<check if="yes the proposal is approved by the user">
  <action>Finalize Sprint Change Proposal document</action>
  <action>Determine change scope classification:</action>

- **Minor**: Can be implemented directly by development team
- **Moderate**: Requires backlog reorganization and PO/SM coordination
- **Major**: Needs fundamental replan with PM/Architect involvement

<action>Provide appropriate handoff based on scope:</action>

</check>

<check if="Minor scope">
  <action>Route to: Development team for direct implementation</action>
  <action>Deliverables: Finalized edit proposals and implementation tasks</action>
</check>

<check if="Moderate scope">
  <action>Route to: Product Owner / Scrum Master agents</action>
  <action>Deliverables: Sprint Change Proposal + backlog reorganization plan</action>
</check>

<check if="Major scope">
  <action>Route to: Product Manager / Solution Architect</action>
  <action>Deliverables: Complete Sprint Change Proposal + escalation notice</action>

<action>Confirm handoff completion and next steps with user</action>
<action>Document handoff in workflow execution log</action>
</check>

</step>

<step n="6" goal="Workflow Completion">
<action>Summarize workflow execution:</action>
  - Issue addressed: {{change_trigger}}
  - Change scope: {{scope_classification}}
  - Artifacts modified: {{list_of_artifacts}}
  - Routed to: {{handoff_recipients}}

<action>Confirm all deliverables produced:</action>

- Sprint Change Proposal document
- Specific edit proposals with before/after
- Implementation handoff plan

<action>Report workflow completion to user with personalized message: "✅ Correct Course workflow complete, {user_name}!"</action>
<action>Remind user of success criteria and next steps for implementation team</action>
</step>

---

**HALT** — Workflow complete. Await user instruction.
