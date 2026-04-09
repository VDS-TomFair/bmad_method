## Step 4 — Web research for latest technical specifics

> ⚠️ **CRITICAL:** 🌐 ENSURE LATEST TECH KNOWLEDGE - Prevent outdated implementations!
**WEB INTELLIGENCE:**
- **Action:** Identify specific
    technical areas that require latest version knowledge:
- **Action:** From architecture analysis, identify specific libraries, APIs, or
    frameworks
- **Action:** For each critical technology, research latest stable version and key changes:
      - Latest API documentation and breaking changes
      - Security vulnerabilities or updates
      - Performance improvements or deprecations
      - Best practices for current version
**EXTERNAL CONTEXT INCLUSION:**
- **Action:** Include in story any critical latest information the developer needs:
      - Specific library versions and why chosen
      - API endpoints with parameters and authentication
      - Recent security patches or considerations
      - Performance optimization techniques
      - Migration considerations if upgrading

## Step 5 — Create comprehensive story file

> ⚠️ **CRITICAL:** 📝 CREATE ULTIMATE STORY FILE - The developer's master implementation guide!
- **Action:** Initialize from template.md:
    {default_output_file}
> **Template Output** → `{default_output_file}`: story_header
> **Template Output** → `{default_output_file}`: story_requirements
> **Template Output** → `{default_output_file}`: developer_context_section
**DEV AGENT GUARDRAILS:**
> **Template Output** → `{default_output_file}`: technical_requirements
> **Template Output** → `{default_output_file}`: architecture_compliance
> **Template Output** → `{default_output_file}`: library_framework_requirements
> **Template Output** → `{default_output_file}`: file_structure_requirements
> **Template Output** → `{default_output_file}`: testing_requirements

**If** previous story learnings available:
  > **Template Output** → `{default_output_file}`: previous_story_intelligence

**If** git analysis completed:
  > **Template Output** → `{default_output_file}`: git_intelligence_summary

**If** web research completed:
  > **Template Output** → `{default_output_file}`: latest_tech_information
> **Template Output** → `{default_output_file}`: project_context_reference
> **Template Output** → `{default_output_file}`: story_completion_status
- **Action:** Set story Status to: "ready-for-dev"
- **Action:** Add completion note: "Ultimate
    context engine analysis completed - comprehensive developer guide created"

---

**HALT** — Await user response or explicit 'continue' before loading next step.

Next step: {installed_path}/steps/step-04-finalize.md
