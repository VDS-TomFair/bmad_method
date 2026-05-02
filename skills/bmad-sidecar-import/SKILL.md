---
name: bmad-sidecar-import
description: "Import upstream BMAD Method sidecar memory files into A0 plugin. Use when user says: import sidecar, migrate bmad, import bmad memory, sidecar import."
version: 1.0.0
trigger_patterns:
  - /sidecar-import
  - /bmad-sidecar-import
  - "import sidecar"
  - "migrate bmad"
  - "import bmad memory"
  - "sidecar import"
---

# BMAD Sidecar Import

Import upstream BMAD Method sidecar memory files into the A0 plugin's sidecar directory structure.

## When to Use

- Migrating from an IDE-based BMAD Method installation to Agent Zero
- You have existing `_bmad/_memory/*-sidecar/` directories from upstream BMAD
- You want to preserve agent memory, instructions, and accumulated knowledge

## How It Works

1. Scans the project's `_bmad/_memory/` directory for `*-sidecar/` subdirectories
2. For each sidecar directory, reads all `.md` files
3. Files are already in the correct location for A0 agents to discover
4. Reports what was found and confirms readiness

## Usage

Run the import script:

```bash
bash skills/bmad-sidecar-import/scripts/import-sidecars.sh /path/to/project
```

Or from within Agent Zero:
```
/load-skill bmad-sidecar-import
```

## What Gets Imported

| File | Purpose |
|------|---------|
| `memories.md` | Running memory of past decisions and preferences |
| `instructions.md` | Agent-specific behavioral instructions |
| Any other `.md` files | Additional context files |

## Notes

- Import is idempotent — safe to run multiple times
- Existing files are NOT overwritten (no-clobber)
- The import script only copies files that don't already exist in the target
- After import, agents will automatically load sidecar content on next activation
