---
title: 'BMAD Agent Counter'
slug: 'bmad-agent-counter'
created: '2026-03-01'
status: 'ready-for-dev'
stepsCompleted: [1, 2, 3, 4]
tech_stack: ['bash', 'python3']
files_to_modify: []
files_to_create:
  - '/a0/usr/local/bin/bmad-agents'
code_patterns: ['POSIX shell script', 'chmod +x', 'ls + grep']
test_patterns: ['manual CLI invocation', 'exit code check']
workflow: 'quick-spec (Barry — Quick Flow, no Phase 1-3 ceremony)'
author: 'Barry (bmad-quick-dev)'
---

# Quick Spec: BMAD Agent Counter

**Author:** Barry 🚀 (Quick Flow Solo Dev)  
**Date:** 2026-03-01  
**Workflow:** Quick Spec — bypasses Phase 1-3 (no PRD, no architecture doc, no epics)  

---

## Overview

### Problem Statement

No quick CLI command exists to count and list installed `bmad-*` agents in `/a0/agents/`. 
Developers and testers must manually `ls | grep bmad-` every time they need to verify the agent inventory.

### Solution

A single executable script (`bmad-agents`) placed on `PATH` that scans `/a0/agents/` for `bmad-*` directories, 
prints a numbered list, and shows the total count. Zero dependencies beyond bash.

### Scope

**In Scope:**
- Count all `bmad-*` directories in `/a0/agents/`
- Print a numbered, sorted list with agent names
- Print total count at the bottom
- Optional `--count` flag to emit count only (machine-parseable)
- Optional `--json` flag for JSON array output

**Out of Scope:**
- Agent health checks (that's a separate tool)
- Checking prompt file presence
- Recursive scanning beyond `/a0/agents/`
- Windows/non-POSIX support

---

## Context for Development

### Codebase Patterns

- Agent dirs follow `bmad-<name>/` pattern directly under `/a0/agents/`
- Current count: **20 agents** (verified by investigation scan)
- No existing agent-listing utility found in `/a0/` or `/usr/local/bin/`
- Python 3.13 available; bash is POSIX-compliant in Kali Linux container
- Scripts in `/usr/local/bin/` are on PATH and world-executable by convention

### Files to Reference

| File | Purpose |
|------|---------|
| `/a0/agents/` | Agent install directory — source of truth |
| `/usr/local/bin/` | Target install location for the CLI script |

### Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Language | Bash | Zero deps, instant execution, fits 'one-liner CLI' requirement |
| Install location | `/usr/local/bin/bmad-agents` | Standard PATH location, no venv needed |
| Flags | `--count`, `--json` | Enables scripted/CI use without text parsing |
| Agent detection | `ls /a0/agents/ \| grep '^bmad-'` | Simple, reliable, matches directory naming convention |

---

## Implementation Plan

### Tasks

- [ ] Task 1: Create the `bmad-agents` bash script
  - File: `/usr/local/bin/bmad-agents`
  - Action: Write script with default list mode, `--count` flag, `--json` flag
  - Notes: Use `find /a0/agents -maxdepth 1 -type d -name 'bmad-*'` for robustness over `ls`

- [ ] Task 2: Make script executable
  - File: `/usr/local/bin/bmad-agents`
  - Action: `chmod +x /usr/local/bin/bmad-agents`

- [ ] Task 3: Smoke-test all three modes
  - Action: Run `bmad-agents`, `bmad-agents --count`, `bmad-agents --json`
  - Notes: Verify exit code 0, count equals 20, JSON is valid array

- [ ] Task 4: Verify PATH accessibility
  - Action: Run `which bmad-agents` — must resolve to `/usr/local/bin/bmad-agents`

### Script Specification

~~~bash
#!/usr/bin/env bash
# bmad-agents — count and list installed BMAD agents
set -euo pipefail

AGENT_DIR="/a0/agents"

collect() {
  find "$AGENT_DIR" -maxdepth 1 -mindepth 1 -type d -name 'bmad-*' \
    | xargs -I{} basename {} \
    | sort
}

case "${1:-}" in
  --count)
    collect | wc -l | tr -d ' '
    ;;
  --json)
    agents=$(collect)
    echo '['
    first=1
    while IFS= read -r agent; do
      [ "$first" -eq 0 ] && echo ','
      printf '  "%s"' "$agent"
      first=0
    done <<< "$agents"
    echo ''
    echo ']'
    ;;
  "")
    agents=$(collect)
    count=$(echo "$agents" | wc -l | tr -d ' ')
    i=1
    while IFS= read -r agent; do
      printf '%3d. %s\n' "$i" "$agent"
      i=$((i+1))
    done <<< "$agents"
    echo "────────────────────────"
    echo "Total: $count BMAD agents"
    ;;
  *)
    echo "Usage: bmad-agents [--count|--json]" >&2
    exit 1
    ;;
esac
~~~

---

## Acceptance Criteria

- [ ] AC 1: Given no flags, when `bmad-agents` is run, then a numbered sorted list of all `bmad-*` agent names is printed, followed by a total count line
- [ ] AC 2: Given `--count` flag, when `bmad-agents --count` is run, then only the integer count is printed (no other output) — suitable for `$(bmad-agents --count)` scripting
- [ ] AC 3: Given `--json` flag, when `bmad-agents --json` is run, then valid JSON array of agent name strings is printed
- [ ] AC 4: Given 20 agents currently installed, when any mode runs, then the count reported equals 20
- [ ] AC 5: Given the script is on PATH, when `which bmad-agents` runs, then it resolves to `/usr/local/bin/bmad-agents`
- [ ] AC 6: Given an unknown flag (e.g. `--help`), when run, then usage message is printed to stderr and exit code is 1
- [ ] AC 7: Given the agent directory is empty, when run, then count reports 0 (no crash)

---

## Additional Context

### Dependencies

- bash (system, no install needed)
- `find`, `sort`, `wc`, `basename` — all standard POSIX utils, present in Kali Linux
- No Python, no npm, no pip

### Testing Strategy

**Manual smoke tests (sufficient for this scope):**

```bash
# Default list mode
bmad-agents
# Expected: numbered list of 20 agents + "Total: 20 BMAD agents"

# Count mode
bmad-agents --count
# Expected: "20" (just the number)

# JSON mode
bmad-agents --json | python3 -m json.tool
# Expected: valid JSON array, 20 elements

# Error mode
bmad-agents --help; echo "exit: $?"
# Expected: usage msg to stderr, exit 1

# PATH check
which bmad-agents
# Expected: /usr/local/bin/bmad-agents
```

### Notes

- **Pre-mortem risk**: `find` vs `ls` — `find -maxdepth 1 -type d` is safer than `ls | grep` as it won't match files named `bmad-*`
- **Future**: Could add `--verbose` to show prompt file count per agent (out of scope here)
- **No state changes**: This is a read-only introspection tool — safe to run anytime
- **Quick Spec confirmation**: Zero Phase 1-3 artifacts created. No PRD. No architecture doc. No epics/stories. Implementation can start immediately.
