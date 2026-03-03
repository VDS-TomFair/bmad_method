## BMAD Configuration

**Project:** a0_bmad_method
**Initialized:** 2026-02-28

### Path Conventions
| Alias | Resolved Path |
|---|---|
| `{project-root}` | `/a0/usr/projects/a0_bmad_method/.a0proj/` |
| `{planning_artifacts}` | `/a0/usr/projects/a0_bmad_method/.a0proj/_bmad-output/planning-artifacts/` |
| `{implementation_artifacts}` | `/a0/usr/projects/a0_bmad_method/.a0proj/_bmad-output/implementation-artifacts/` |
| `{product_knowledge}` | `/a0/usr/projects/a0_bmad_method/.a0proj/knowledge/` |
| `{output_folder}` | `/a0/usr/projects/a0_bmad_method/.a0proj/_bmad-output/` |

### User Settings
- **User Name:** Vanja
- **Communication Language:** English
- **User Skill Level:** intermediate

### Project Description
Development of the BMAD Method Framework integration for Agent Zero.

The goal is a fully compatible BMAD implementation that follows Agent Zero architecture and conventions while delivering the full BMAD method. Nothing about the current implementation is assumed to be correct — the number of agents, skills, directory structure, and integration approach are all open to questioning and revision.

Source of truth:
- Official BMAD Method framework files (skills/bmad-*/workflows/)
- Agent Zero codebase and architecture (/a0/)

### Development Context
- This project uses BMAD to develop BMAD (dogfooding)
- Skills, agents, and docs are symlinked from this project into /a0/ for immediate live testing
- Symlinks are a dev convenience only — end users copy agents/ and skills/ directly to /a0/
- All decisions about integration architecture should be validated against A0 conventions
- Workflows are bundled inside their owning skills (skills/bmad-*/workflows/) — no project-level copy
