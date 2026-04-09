## Step 2 — Load and analyze core artifacts

> ⚠️ **CRITICAL:** 🔬 EXHAUSTIVE ARTIFACT ANALYSIS - This is where you prevent future developer fuckups!
> **Invoke Protocol:** `discover_inputs`
> **Note:** Available content: {epics_content}, {prd_content}, {architecture_content}, {ux_content},
    {project_context}
- **Action:** From {epics_content}, extract Epic {{epic_num}} complete context:
**EPIC ANALYSIS:** - Epic
    objectives and business value - ALL stories in this epic for cross-story context - Our specific story's requirements, user story
    statement, acceptance criteria - Technical requirements and constraints - Dependencies on other stories/epics - Source hints pointing to
    original documents
- **Action:** Extract our story ({{epic_num}}-{{story_num}}) details:
**STORY FOUNDATION:** - User story statement
    (As a, I want, so that) - Detailed acceptance criteria (already BDD formatted) - Technical requirements specific to this story -
    Business context and value - Success criteria

**If** story_num > 1:
  - **Action:** Find {{previous_story_num}}: scan {implementation_artifacts} for the story file in epic {{epic_num}} with the highest story number less than {{story_num}}
  - **Action:** Load previous story file: {implementation_artifacts}/{{epic_num}}-{{previous_story_num}}-*.md
  **PREVIOUS STORY INTELLIGENCE:** -
    Dev notes and learnings from previous story - Review feedback and corrections needed - Files that were created/modified and their
    patterns - Testing approaches that worked/didn't work - Problems encountered and solutions found - Code patterns established
  - **Action:** Extract
    all learnings that could impact current story implementation

**If** previous story exists AND git repository detected:
  - **Action:** Get last 5 commit titles to understand recent work patterns
  - **Action:** Analyze 1-5 most recent commits for relevance to current story:
        - Files created/modified
        - Code patterns and conventions used
        - Library dependencies added/changed
        - Architecture decisions implemented
        - Testing approaches used
  - **Action:** Extract actionable insights for current story implementation

## Step 3 — Architecture analysis for developer guardrails

> ⚠️ **CRITICAL:** 🏗️ ARCHITECTURE INTELLIGENCE - Extract everything the developer MUST follow!
**ARCHITECTURE DOCUMENT ANALYSIS:**
- **Action:** Systematically
    analyze architecture content for story-relevant requirements:

**If** architecture file is single file:
  - **Action:** Load complete {architecture_content}

**If** architecture is sharded to folder:
  - **Action:** Load architecture index and scan all architecture files
**CRITICAL ARCHITECTURE EXTRACTION:**
- **Action:** For
    each architecture section, determine if relevant to this story:
- **Technical Stack:** Languages, frameworks, libraries with
    versions - **Code Structure:** Folder organization, naming conventions, file patterns - **API Patterns:** Service structure, endpoint
    patterns, data contracts - **Database Schemas:** Tables, relationships, constraints relevant to story - **Security Requirements:**
    Authentication patterns, authorization rules - **Performance Requirements:** Caching strategies, optimization patterns - **Testing
    Standards:** Testing frameworks, coverage expectations, test patterns - **Deployment Patterns:** Environment configurations, build
    processes - **Integration Patterns:** External service integrations, data flows
- **Action:** Extract any story-specific requirements that the
    developer MUST follow
- **Action:** Identify any architectural decisions that override previous patterns

---

**HALT** — Await user response or explicit 'continue' before loading next step.

Next step: {installed_path}/steps/step-03-research-and-write.md
