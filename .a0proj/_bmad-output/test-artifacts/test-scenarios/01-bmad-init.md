# Test Scenarios: BMAD Initialization (bmad-init)

**Priority:** HIGH  
**Module:** bmad-init skill  
**Risk:** Initialization failure blocks all downstream workflows  

---

## Scenario INIT-01: Fresh Project Initialization

**Objective:** Verify `bmad init` creates the full required workspace structure  
**Risk Level:** CRITICAL  

### Preconditions
- No existing `.a0proj/` directory in target project folder
- bmad-init skill available at `/a0/skills/bmad-init/`

### Steps
1. Trigger bmad-init skill: say "bmad init" or "initialize bmad"
2. Observe: skill loads, presents initialization prompt
3. Provide: project name, description, user name, output folder preferences
4. Confirm execution
5. Verify file system output

### Expected Behavior
- Skill loads `bmad-init` SKILL.md without error
- User prompted for project configuration
- Script executes: `/a0/skills/bmad-init/scripts/bmad-init.sh`
- Following directories created:
  ```
  .a0proj/
  .a0proj/instructions/
  .a0proj/_bmad-output/planning-artifacts/
  .a0proj/_bmad-output/implementation-artifacts/
  .a0proj/_bmad-output/test-artifacts/
  .a0proj/knowledge/main/
  .a0proj/knowledge/fragments/
  .a0proj/knowledge/solutions/
  ```
- `01-bmad-config.md` written with correct path aliases
- `02-bmad-state.md` written with `phase: ready`, `persona: BMad Master`, `active artifact: none`

### Verification Commands
```bash
ls -la /target-project/.a0proj/instructions/
cat /target-project/.a0proj/instructions/01-bmad-config.md
cat /target-project/.a0proj/instructions/02-bmad-state.md
```

### Pass Criteria
- [ ] All directories exist
- [ ] 01-bmad-config.md contains `{project-root}`, `{planning_artifacts}`, `{implementation_artifacts}`, `{output_folder}` alias definitions
- [ ] 02-bmad-state.md contains `phase: ready`
- [ ] 02-bmad-state.md contains `persona: BMad Master`
- [ ] No framework files copied (no skills/, agents/ subdirectories created)

### Fail Signals
- Script exits with error
- Missing directories
- Path aliases contain relative paths instead of absolute paths
- Framework files incorrectly copied into project directory

---

## Scenario INIT-02: Config File Alias Resolution

**Objective:** Verify all path aliases in 01-bmad-config.md resolve to valid absolute paths  
**Risk Level:** HIGH  

### Preconditions
- Initialized project with 01-bmad-config.md present

### Steps
1. Read `01-bmad-config.md`
2. Extract each alias: `{project-root}`, `{planning_artifacts}`, `{implementation_artifacts}`, `{output_folder}`, `{product_knowledge}`
3. For each alias, verify the resolved path is:
   - Absolute (starts with `/`)
   - Directory exists on filesystem
   - Points to correct location within `.a0proj/`

### Expected Behavior
| Alias | Expected Resolved Path |
|-------|----------------------|
| `{project-root}` | `/path/to/project/.a0proj/` |
| `{planning_artifacts}` | `/path/to/project/.a0proj/_bmad-output/planning-artifacts/` |
| `{implementation_artifacts}` | `/path/to/project/.a0proj/_bmad-output/implementation-artifacts/` |
| `{output_folder}` | `/path/to/project/.a0proj/_bmad-output/` |
| `{product_knowledge}` | `/path/to/project/.a0proj/knowledge/` |

### Pass Criteria
- [ ] All 5 aliases present in config file
- [ ] All resolved paths are absolute
- [ ] All resolved paths exist as directories

---

## Scenario INIT-03: Re-initialization on Existing Project

**Objective:** Verify bmad init handles an already-initialized project gracefully  
**Risk Level:** MEDIUM  

### Preconditions
- Project already initialized with existing 01-bmad-config.md and 02-bmad-state.md
- 02-bmad-state.md has `phase: planning` (simulating in-progress project)

### Steps
1. Trigger `bmad init` on already-initialized project
2. Observe agent/skill behavior

### Expected Behavior
- Agent detects existing initialization
- Either: warns user and skips (preferred), or presents update option
- Does NOT overwrite `02-bmad-state.md` with `phase: ready` (would destroy project state)
- Does NOT overwrite existing output artifacts

### Pass Criteria
- [ ] Existing state preserved (no phase reset)
- [ ] Existing artifacts not deleted
- [ ] User informed of existing initialization

---

## Scenario INIT-04: bmad-help Contextual Response

**Objective:** Verify `/bmad-help` responds without loading a skill, with contextual guidance  
**Risk Level:** MEDIUM  

### Steps
1. Say `/bmad-help where do I start?`
2. Say `/bmad-help what phase am I in?`
3. Say `/bmad-help how do I create a PRD?`

### Expected Behavior
- Responds directly — no `skills_tool:load` call observed
- Response is contextually relevant to the question
- References current phase from 02-bmad-state.md
- Guides toward appropriate next workflow

### Pass Criteria
- [ ] No skill load triggered
- [ ] Contextually accurate response
- [ ] Correct phase referenced

---

## Scenario INIT-05: Manifest File Integrity

**Objective:** Verify agent-manifest.csv and workflow-manifest.csv are accurate  
**Risk Level:** MEDIUM  

### Preconditions
- Access to `/a0/skills/bmad-init/_config/agent-manifest.csv`
- Access to `/a0/skills/bmad-init/_config/workflow-manifest.csv`

### Steps
```bash
cat /a0/skills/bmad-init/_config/agent-manifest.csv
cat /a0/skills/bmad-init/_config/workflow-manifest.csv
```

### Expected Behavior
- agent-manifest.csv lists all 19+ BMAD agents with correct profile names
- workflow-manifest.csv lists all major workflows across BMM, BMB, TEA, CIS
- No orphaned entries (agents listed that don't exist)
- No missing entries (agents that exist but aren't listed)

### Pass Criteria
- [ ] 19 agent entries minimum in agent-manifest.csv
- [ ] All BMM workflows represented
- [ ] Profile name matches directory name in `/a0/agents/bmad-*/`
