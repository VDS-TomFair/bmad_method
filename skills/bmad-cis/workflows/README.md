# CIS Workflows

Six interactive workflows facilitating creative, strategic, and visual communication processes through curated technique libraries and structured facilitation.

## Table of Contents

- [Workflow Overview](#workflow-overview)
- [Common Features](#common-features)
- [Usage](#usage)
- [Configuration](#configuration)

## Workflow Overview

### [Brainstorming](../../../skills/bmad-init/core/workflows/brainstorming)

**Purpose:** Interactive ideation using 36 techniques across 7 categories

**Approach:** Master facilitation with "Yes, and..." methodology

**Techniques:** Collaborative, structured, creative, deep, theatrical, wild, introspective

**Selection Modes:** User-selected, AI-recommended, random, or progressive

**Note:** Brainstorming is a shared CORE workflow (used by multiple modules). Owned by `skills/bmad-init/core/workflows/brainstorming/` and routed via `bmad-brainstorming` skill. Carson (bmad-brainstorming-coach) is the CIS agent facilitating this workflow.

### [Design Thinking](./design-thinking)

**Purpose:** Human-centered design through five phases

**Process:** Empathize → Define → Ideate → Prototype → Test

**Focus:** Divergent thinking before convergent action

**Output:** User empathy insights and rapid prototypes

### [Innovation Strategy](./innovation-strategy)

**Purpose:** Identify disruption opportunities and business model innovation

**Frameworks:** Jobs-to-be-Done, Blue Ocean Strategy, Value Chain Analysis

**Focus:** Sustainable competitive advantage over features

**Output:** Strategic innovation roadmap

### [Presentation](./presentation)

**Purpose:** Design compelling presentations and slide decks using visual storytelling frameworks

**Structures:** Problem-Agitate-Solve, Hero's Journey, Pyramid Principle, Framework, Before-After-Bridge, Vision Cast, and 3 more

**Focus:** Audience psychology, visual hierarchy, and narrative-driven design

**Output:** Complete presentation spec with slide-by-slide breakdown, visual design system, speaker notes, and production checklist

### [Problem Solving](./problem-solving)

**Purpose:** Systematic challenge resolution

**Methods:** TRIZ, Theory of Constraints, Systems Thinking, Root Cause Analysis

**Approach:** Detective-style puzzle solving

**Output:** Root cause identification and solution strategies

### [Storytelling](./storytelling)

**Purpose:** Craft compelling narratives

**Frameworks:** Hero's Journey, Three-Act Structure, Story Brand (25 total)

**Customization:** Platform and audience-specific adaptation

**Style:** Whimsical master storyteller facilitation

## Common Features

All workflows share:

- **Interactive Facilitation** - AI guides through questions, not generation
- **Technique Libraries** - CSV databases of proven methods
- **Context Integration** - Optional document input for domain relevance
- **Structured Output** - Comprehensive reports with insights and actions
- **Energy Monitoring** - Adaptive pacing based on engagement

## Usage

### Basic Invocation

```bash
workflow brainstorming
workflow design-thinking
workflow innovation-strategy
workflow presentation
workflow problem-solving
workflow storytelling
```

### With Context

```bash
workflow [workflow-name] --data /path/to/context.md
```

### Via Agent

```bash
agent cis/brainstorming-coach
> *brainstorm
```

## Configuration

Edit `/skills/bmad-cis/config.yaml`:

| Setting                | Purpose                 | Default            |
| ---------------------- | ----------------------- | ------------------ |
| output_folder          | Result storage location | ./creative-outputs |
| user_name              | Session participant     | User               |
| communication_language | Facilitation language   | english            |

## Workflow Structure

Each CIS-owned workflow contains:

```
workflow-name/
├── workflow.yaml      # Configuration
├── instructions.md    # Facilitation guide
├── template.md        # Output document template
└── SKILL.md           # Thin skill wrapper
```

Some workflows additionally contain:
```
├── techniques.csv     # Method library (brainstorming, storytelling)
├── story-types.csv    # Framework library (storytelling)
└── README.md          # Workflow-specific documentation
```

## Agent → Workflow Mapping

| Agent | Menu Code | Workflow | Owned By |
|-------|-----------|----------|----------|
| Carson (brainstorming-coach) | BS | brainstorming/workflow.md | bmad-init/core |
| Maya (design-thinking-coach) | DT | design-thinking/workflow.yaml | bmad-cis |
| Victor (innovation-strategist) | IS | innovation-strategy/workflow.yaml | bmad-cis |
| Caravaggio (presentation) | PR | presentation/workflow.yaml | bmad-cis |
| Dr. Quinn (creative-problem-solver) | PS | problem-solving/workflow.yaml | bmad-cis |
| Sophia (storyteller) | ST | storytelling/workflow.yaml | bmad-cis |

## Best Practices

1. **Prepare context** - Provide background documents for better results
2. **Set clear objectives** - Define goals before starting
3. **Trust the process** - Let facilitation guide discovery
4. **Capture everything** - Document insights as they emerge
5. **Take breaks** - Pause when energy drops

## Integration

CIS workflows integrate with:

- **BMM** - Project brainstorming and ideation
- **BMB** - Creative module design
- **Custom Modules** - Shared creative resource

---

For detailed workflow instructions, see individual workflow directories.
