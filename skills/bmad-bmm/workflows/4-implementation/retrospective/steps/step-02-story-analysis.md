<step n="2" goal="Deep Story Analysis - Extract Lessons from Implementation">

<output>
Bob (Scrum Master): "Before we start the team discussion, let me review all the story records to surface key themes. This'll help us have a richer conversation."

Charlie (Senior Dev): "Good idea - those dev notes always have gold in them."
</output>

<action>For each story in epic {{epic_number}}, read the complete story file from {implementation_artifacts}/{{epic_number}}-{{story_num}}-*.md</action>

<action>Extract and analyze from each story:</action>

**Dev Notes and Struggles:**

- Look for sections like "## Dev Notes", "## Implementation Notes", "## Challenges", "## Development Log"
- Identify where developers struggled or made mistakes
- Note unexpected complexity or gotchas discovered
- Record technical decisions that didn't work out as planned
- Track where estimates were way off (too high or too low)

**Review Feedback Patterns:**

- Look for "## Review", "## Code Review", "## SM Review", "## Scrum Master Review" sections
- Identify recurring feedback themes across stories
- Note which types of issues came up repeatedly
- Track quality concerns or architectural misalignments
- Document praise or exemplary work called out in reviews

**Lessons Learned:**

- Look for "## Lessons Learned", "## Retrospective Notes", "## Takeaways" sections within stories
- Extract explicit lessons documented during development
- Identify "aha moments" or breakthroughs
- Note what would be done differently
- Track successful experiments or approaches

**Technical Debt Incurred:**

- Look for "## Technical Debt", "## TODO", "## Known Issues", "## Future Work" sections
- Document shortcuts taken and why
- Track debt items that affect next epic
- Note severity and priority of debt items

**Testing and Quality Insights:**

- Look for "## Testing", "## QA Notes", "## Test Results" sections
- Note testing challenges or surprises
- Track bug patterns or regression issues
- Document test coverage gaps

<action>Synthesize patterns across all stories:</action>

**Common Struggles:**

- Identify issues that appeared in 2+ stories (e.g., "3 out of 5 stories had API authentication issues")
- Note areas where team consistently struggled
- Track where complexity was underestimated

**Recurring Review Feedback:**

- Identify feedback themes (e.g., "Error handling was flagged in every review")
- Note quality patterns (positive and negative)
- Track areas where team improved over the course of epic

**Breakthrough Moments:**

- Document key discoveries (e.g., "Story 3 discovered the caching pattern we used for rest of epic")
- Note when team velocity improved dramatically
- Track innovative solutions worth repeating

**Velocity Patterns:**

- Calculate average completion time per story
- Note velocity trends (e.g., "First 2 stories took 3x longer than estimated")
- Identify which types of stories went faster/slower

**Team Collaboration Highlights:**

- Note moments of excellent collaboration mentioned in stories
- Track where pair programming or mob programming was effective
- Document effective problem-solving sessions

<action>Store this synthesis - these patterns will drive the retrospective discussion</action>

<output>
Bob (Scrum Master): "Okay, I've reviewed all {{total_stories}} story records. I found some really interesting patterns we should discuss."

Dana (QA Engineer): "I'm curious what you found, Bob. I noticed some things in my testing too."

Bob (Scrum Master): "We'll get to all of it. But first, let me load the previous epic's retro to see if we learned from last time."
</output>

</step>

<step n="3" goal="Load and Integrate Previous Epic Retrospective">

<action>Calculate previous epic number: {{prev_epic_num}} = {{epic_number}} - 1</action>

<check if="{{prev_epic_num}} >= 1">
  <action>Search for previous retrospectives using pattern: {implementation_artifacts}/epic-{{prev_epic_num}}-retro-*.md</action>

  <check if="previous retrospectives found">
    <output>
Bob (Scrum Master): "I found our retrospectives from Epic {{prev_epic_num}}. Let me see what we committed to back then..."
    </output>

    <action>Read the previous retrospectives</action>

    <action>Extract key elements:</action>
    - **Action items committed**: What did the team agree to improve?
    - **Lessons learned**: What insights were captured?
    - **Process improvements**: What changes were agreed upon?
    - **Technical debt flagged**: What debt was documented?
    - **Team agreements**: What commitments were made?
    - **Preparation tasks**: What was needed for this epic?

    <action>Cross-reference with current epic execution:</action>

    **Action Item Follow-Through:**
    - For each action item from Epic {{prev_epic_num}} retro, check if it was completed
    - Look for evidence in current epic's story records
    - Mark each action item: ✅ Completed, ⏳ In Progress, ❌ Not Addressed

    **Lessons Applied:**
    - For each lesson from Epic {{prev_epic_num}}, check if team applied it in Epic {{epic_number}}
    - Look for evidence in dev notes, review feedback, or outcomes
    - Document successes and missed opportunities

    **Process Improvements Effectiveness:**
    - For each process change agreed to in Epic {{prev_epic_num}}, assess if it helped
    - Did the change improve velocity, quality, or team satisfaction?
    - Should we keep, modify, or abandon the change?

    **Technical Debt Status:**
    - For each debt item from Epic {{prev_epic_num}}, check if it was addressed
    - Did unaddressed debt cause problems in Epic {{epic_number}}?
    - Did the debt grow or shrink?

    <action>Prepare "continuity insights" for the retrospective discussion</action>

    <action>Identify wins where previous lessons were applied successfully:</action>
    - Document specific examples of applied learnings
    - Note positive impact on Epic {{epic_number}} outcomes
    - Celebrate team growth and improvement

    <action>Identify missed opportunities where previous lessons were ignored:</action>
    - Document where team repeated previous mistakes
    - Note impact of not applying lessons (without blame)
    - Explore barriers that prevented application

    <output>

Bob (Scrum Master): "Interesting... in Epic {{prev_epic_num}}'s retro, we committed to {{action_count}} action items."

Alice (Product Owner): "How'd we do on those, Bob?"

Bob (Scrum Master): "We completed {{completed_count}}, made progress on {{in_progress_count}}, but didn't address {{not_addressed_count}}."

Charlie (Senior Dev): _looking concerned_ "Which ones didn't we address?"

Bob (Scrum Master): "We'll discuss that in the retro. Some of them might explain challenges we had this epic."

Elena (Junior Dev): "That's... actually pretty insightful."

Bob (Scrum Master): "That's why we track this stuff. Pattern recognition helps us improve."
</output>

  </check>

  <check if="no previous retro found">
    <output>
Bob (Scrum Master): "I don't see a retrospective for Epic {{prev_epic_num}}. Either we skipped it, or this is your first retro."

Alice (Product Owner): "Probably our first one. Good time to start the habit!"
</output>
<action>Set {{first_retrospective}} = true</action>
</check>
</check>

<check if="{{prev_epic_num}} < 1">
  <output>
Bob (Scrum Master): "This is Epic 1, so naturally there's no previous retro to reference. We're starting fresh!"

Charlie (Senior Dev): "First epic, first retro. Let's make it count."
</output>
<action>Set {{first_retrospective}} = true</action>
</check>

</step>
