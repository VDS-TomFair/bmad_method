---
name: bmad-sidecar-import
version: 1.0.1
description: "Audit and verify BMAD sidecar memory files. Use when user says: check sidecars, verify sidecar, sidecar status, import sidecar, sidecar import."
trigger_patterns:
  - /sidecar-import
  - /bmad-sidecar-import
  - "check sidecars"
  - "verify sidecar"
  - "sidecar status"
  - "import sidecar"
  - "sidecar import"
---

# BMAD Sidecar Verification

Audit and verify that sidecar memory files are in place for all BMAD agents.

## What This Skill Does

This is a **verification/audit tool** that:

1. Scans the project's `_bmad/_memory/` directory for `*-sidecar/` subdirectories
2. For each sidecar directory, checks which `.md` files exist and have content
3. Reports a summary of found vs. skipped (already existing) files
4. Confirms readiness for agents to load their sidecar content

> **Note:** In the A0 plugin, sidecar directories and seed files are created by `bmad-init`. 
> This script audits the result — it does not copy files from an external source.

## When to Use

- After running `bmad init` to verify all sidecar directories were created
- Checking which agents have memory files populated
- Auditing sidecar readiness before running BMAD workflows
- Troubleshooting missing agent memory files

## Usage

Run the verification script:

```bash
bash skills/bmad-sidecar-import/scripts/import-sidecars.sh /path/to/project
```

Or from within Agent Zero:
```
/load-skill bmad-sidecar-import
```

## Output

The script reports:
- Each sidecar directory found
- Files that exist with content (skipped)
- Files that exist but are empty stubs (counted as found)
- Summary totals

| Count | Meaning |
|-------|---------|
| Files found | Markdown files detected in sidecar directories |
| Files skipped | Files with existing content (> 5 bytes) |

## Notes

- Verification is idempotent — safe to run multiple times
- Existing files with content are never modified
- After verification, agents will automatically load sidecar content on activation
