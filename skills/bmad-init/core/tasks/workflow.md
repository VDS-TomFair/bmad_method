# Execute Workflow

**Objective:** Execute given workflow by loading its configuration, following instructions, and producing output

**⚠️ LLM EXECUTION RULES (MANDATORY):**
> **Mandate:** Always read COMPLETE files - NEVER use offset/limit when reading any workflow related files
> **Mandate:** Instructions are MANDATORY - either as file path, steps or embedded list in YAML, XML or markdown
> **Mandate:** Execute ALL steps in instructions IN EXACT ORDER
> **Mandate:** Save to template output file after EVERY "template-output" tag
> **Mandate:** NEVER skip a step - YOU are responsible for every steps execution without fail or excuse

## Workflow Rules ⚠️

- **Rule 1:** Steps execute in exact numerical order (1, 2, 3...)
- **Rule 2:** Optional steps: Ask user unless #yolo mode active
- **Rule 3:** Template-output tags: Save content, discuss with the user the section completed, and NEVER proceed until the users indicates
      to proceed (unless YOLO mode has been activated)

---

## Step 1 — Load and Initialize Workflow

  ### Substep 1a — Load Configuration and Resolve Variables

    - **Action:** Read workflow.yaml from provided path
> **Mandate:** Load config_source (REQUIRED for all modules)
    - **Phase 1:** Load external config from config_source path
    - **Phase 2:** Resolve all {config_source}: references with values from config
    - **Phase 3:** Resolve system variables (date:system-generated) and paths ({project-root}, {installed_path})
    - **Phase 4:** Ask user for input of any variables that are still unknown

  ### Substep 1b — Load Required Components

> **Mandate:** Instructions: Read COMPLETE file from path OR embedded list (REQUIRED)

    **Check:** If template path → Read COMPLETE template file

    **Check:** If validation path → Note path for later loading when needed

    **Check:** If template: false → Mark as action-workflow (else template-workflow)
    > **Note:** Data files (csv, json) → Store paths only, load on-demand when instructions reference them

  ### Substep 1c — Initialize Output *(if: template-workflow)*

    - **Action:** Resolve default_output_file path with all variables and {{date}}
    - **Action:** Create output directory if doesn't exist
    - **Action:** If template-workflow → Write template to output file with placeholders
    - **Action:** If action-workflow → Skip file creation

## Step 2 — Process Each Instruction Step in Order

  *For each step in instructions:*

  ### Substep 2a — Handle Step Attributes

    **Check:** If optional="true" and NOT #yolo → Ask user to include

    **Check:** If if="condition" → Evaluate condition

    **Check:** If for-each="item" → Repeat step for each item

    **Check:** If repeat="n" → Repeat step n times

  ### Substep 2b — Execute Step Content

    - **Action:** Process step instructions (markdown or XML tags)
    - **Action:** Replace {{variables}} with values (ask user if unknown)

    **Execute Tags:**
      - `action xml tag → Perform the action`
      - `check if="condition" xml tag → Conditional block wrapping actions (requires closing </check>)`
      - `ask xml tag → Prompt user and WAIT for response`
      - `invoke-workflow xml tag → Execute another workflow with given inputs and the workflow.md runner`
      - `invoke-task xml tag → Execute specified task`
      - `invoke-protocol name="protocol_name" xml tag → Execute reusable protocol from protocols section`
      - `goto step="x" → Jump to specified step`

  ### Substep 2c — Handle template-output Tags

      **If response** = `template-output`:
  > **Mandate:** Generate content for this section
  > **Mandate:** Save to file (Write first time, Edit subsequent)
          - **Action:** Display generated content

          **❓ Ask user:**
          [a] Advanced Elicitation, [c] Continue, [p] Party-Mode, [y] YOLO the rest of this document only. WAIT for response.

              **If response** = `a`:
                  - **Action:** Start the advanced elicitation workflow {project-root}/skills/bmad-init/core/workflows/advanced-elicitation/workflow.md

              **If response** = `c`:
                  - **Action:** Continue to next step

              **If response** = `p`:
                  - **Action:** Start the party-mode workflow {project-root}/skills/bmad-init/core/workflows/party-mode/workflow.md

              **If response** = `y`:
                  - **Action:** Enter #yolo mode for the rest of the workflow

  ### Substep 2d — Step Completion

    **Check:** If no special tags and NOT #yolo:

    **❓ Ask user:**
    Continue to next step? (y/n/edit)

## Step 3 — Completion

  **Check:** Confirm document saved to output path
  - **Action:** Report workflow completion

## Execution Modes

- **`normal`:** Full user interaction and confirmation of EVERY step at EVERY template output - NO EXCEPTIONS except yolo MODE
- **`yolo`:** Skip all confirmations and elicitation, minimize prompts and try to produce all of the workflow automatically by
      simulating the remaining discussions with an simulated expert user

## Supported Tags — Instructions can use these tags

**Structural:**
- `step n="X" goal="..." - Define step with number and goal`
- `optional="true" - Step can be skipped`
- `if="condition" - Conditional execution`
- `for-each="collection" - Iterate over items`
- `repeat="n" - Repeat n times`

**Execution:**
- `action - Required action to perform`
- `action if="condition" - Single conditional action (inline, no closing tag needed)`
- `check if="condition">...</check> - Conditional block wrapping multiple items (closing tag required)`
- `ask - Get user input (ALWAYS wait for response before continuing)`
- `goto - Jump to another step`
- `invoke-workflow - Call another workflow`
- `invoke-task - Call a task`
- `invoke-protocol - Execute a reusable protocol (e.g., discover_inputs)`

- `template-output - Save content checkpoint`
- `critical - Cannot be skipped`
- `example - Show example output`

## Protocols — Reusable workflow protocols that can be invoked via invoke-protocol tag

### Protocol: `discover_inputs`
_Smart file discovery and loading based on input_file_patterns_

**Objective:** Intelligently load project files (whole or sharded) based on workflow's input_file_patterns configuration
> ⚠️ **CRITICAL:** Only execute if workflow.yaml contains input_file_patterns section

---

## Step 1 — Parse Input File Patterns

  - **Action:** Read input_file_patterns from loaded workflow.yaml
  - **Action:** For each pattern group (prd, architecture, epics, etc.), note the load_strategy if present

## Step 2 — Load Files Using Smart Strategies

  *For each pattern in input_file_patterns:*

  ### Substep 2a — Try Sharded Documents First

    **If** *sharded pattern exists*:
        - **Action:** Determine load_strategy from pattern config (defaults to FULL_LOAD if not specified)

  **Strategy: `FULL_LOAD`**
  Load ALL files in sharded directory - used for PRD, Architecture, UX, brownfield docs
        - **Action:** Use glob pattern to find ALL .md files (e.g., "{output_folder}/*architecture*/*.md")
        - **Action:** Load EVERY matching file completely
        - **Action:** Concatenate content in logical order (index.md first if exists, then alphabetical)
        - **Action:** Store in variable: {pattern_name_content}

  **Strategy: `SELECTIVE_LOAD`**
  Load specific shard using template variable - example: used for epics with {{epic_num}}
        - **Action:** Check for template variables in sharded_single pattern (e.g., {{epic_num}})
        - **Action:** If variable undefined, ask user for value OR infer from context
        - **Action:** Resolve template to specific file path
        - **Action:** Load that specific file
        - **Action:** Store in variable: {pattern_name_content}

  **Strategy: `INDEX_GUIDED`**
  Load index.md, analyze structure and description of each doc in the index, then intelligently load relevant docs
  > **Mandate:** DO NOT BE LAZY - use best judgment to load documents that might have relevant information, even if only a 5% chance
        - **Action:** Load index.md from sharded directory
        - **Action:** Parse table of contents, links, section headers
        - **Action:** Analyze workflow's purpose and objective
        - **Action:** Identify which linked/referenced documents are likely relevant

  **Example:**
  ~~~
  If workflow is about authentication and index shows "Auth Overview", "Payment Setup", "Deployment" → Load auth
                  docs, consider deployment docs, skip payment
  ~~~
        - **Action:** Load all identified relevant documents
        - **Action:** Store combined content in variable: {pattern_name_content}
        > **Note:** When in doubt, LOAD IT - context is valuable, being thorough is better than missing critical info
        - **Action:** Mark pattern as RESOLVED, skip to next pattern

  ### Substep 2b — Try Whole Document if No Sharded Found

    **If** *no sharded matches found OR no sharded pattern exists*:
        - **Action:** Attempt glob match on 'whole' pattern (e.g., "{output_folder}/*prd*.md")

        **If** *matches found*:
            - **Action:** Load ALL matching files completely (no offset/limit)
            - **Action:** Store content in variable: {pattern_name_content} (e.g., {prd_content})
            - **Action:** Mark pattern as RESOLVED, skip to next pattern

  ### Substep 2c — Handle Not Found

    **If** *no matches for sharded OR whole*:
        - **Action:** Set {pattern_name_content} to empty string
        - **Action:** Note in session: "No {pattern_name} files found" (not an error, just unavailable, offer use change to provide)

## Step 3 — Report Discovery Results

  - **Action:** List all loaded content variables with file counts

**Example:**
~~~
✓ Loaded {prd_content} from 5 sharded files: prd/index.md, prd/requirements.md, ...
            ✓ Loaded {architecture_content} from 1 file: Architecture.md
            ✓ Loaded {epics_content} from selective load: epics/epic-3.md
            ○ No ux_design files found
~~~
  > **Note:** This gives workflow transparency into what context is available

**⚠️ LLM EXECUTION RULES (MANDATORY):**

**Critical Rules:**

• This is the complete workflow execution engine
      • You MUST Follow instructions exactly as written
      • The workflow execution engine is governed by: {project-root}/skills/bmad-init/core/tasks/workflow.md
      • You MUST have already loaded and processed: {installed_path}/workflow.yaml
      • This workflow uses INTENT-DRIVEN PLANNING - adapt organically to product type and context
      • YOU ARE FACILITATING A CONVERSATION With a user to produce a final document step by step. The whole process is meant to be
      collaborative helping the user flesh out their ideas. Do not rush or optimize and skip any section.
