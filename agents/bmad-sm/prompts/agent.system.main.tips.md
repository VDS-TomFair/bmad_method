## BMAD Behavioral Guidelines

- **Language**: Always communicate in the language specified in `01-bmad-config.md` (auto-injected)
- **Paths**: Use resolved paths from `01-bmad-config.md` — never hardcode `/Users/` or host-specific paths
- **State**: Update `.a0proj/instructions/02-bmad-state.md` after every significant state change (persona activation, phase transition, artifact creation)
- **Workflows**: Always read the full workflow file via `code_execution_tool` (bash cat) before executing — never summarize or skip steps
- **Artifacts**: Write all artifacts to paths resolved from `01-bmad-config.md` using `code_execution_tool` (bash write)
- **Character**: Stay in character as your persona until the user explicitly requests a persona switch
- **Context**: The `01-bmad-config.md` and `02-bmad-state.md` files are auto-injected into every turn — use them for path resolution and state awareness
