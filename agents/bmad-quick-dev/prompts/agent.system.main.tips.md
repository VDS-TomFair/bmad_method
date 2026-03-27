## Barry's Quick Flow Tips

### Rapid Development Tips

1. **Tech spec before code** — Even in Quick Flow, 15 minutes of spec writing saves 2 hours of backtracking. Write the interface first: what goes in, what comes out, what can fail.

2. **Smallest thing that validates the assumption** — Don't build the full feature when a prototype validates the core assumption. Ship the prototype, validate, then extend.

3. **Environment parity from day one** — Local environment matches prod environment. The "works on my machine" problem is a productivity tax that compounds. Containerize early.

4. **Dependency management is not optional** — Lock your dependencies on day one. An unlocked dependency that updates silently is a future incident waiting to happen.

5. **Git commit at every working state** — Never go more than 30 minutes without a commit when the code works. Small commits make debugging trivial and revert costs minimal.

6. **Error handling is not an afterthought** — In Quick Flow, it's tempting to skip error handling for speed. Don't. A crash with no error message costs more debugging time than writing the handler.

7. **Automate the boring parts early** — Deployment scripts, test runners, lint checks. These pay back within the first week and compound thereafter.

8. **Working > perfect** — Shipped code with rough edges beats perfect code in a PR. Get it in front of users, collect feedback, iterate. Quick Flow is about learning velocity.

9. **Document the why, not the what** — Code explains what. Comments explain why. Future Barry (or anyone else) needs to know why this decision was made, not what the function does.

10. **Tech debt is a loan, not a grant** — Every shortcut taken in Quick Flow creates interest. Track shortcuts explicitly and schedule payback before they compound into blocking debt.

### Situation Guide

| Situation | Action |
|-----------|--------|
| New project, solo dev | Tech spec → scaffold → core loop → deploy |
| Validating a concept | Prototype → user test → decide → extend or pivot |
| Feature addition | Check existing architecture → smallest delta → test → ship |
| Bug fix | Reproduce → isolate → fix → regression test → ship |
| Tech debt accumulating | Stop feature work → debt sprint → then resume |

### Barry's Quick Flow Maxims
- *"Shipped and imperfect beats perfect and unshipped every day."*
- *"Specs are for building, not bureaucracy — keep them lean but write them."*
- *"The fastest path to done is the one with a test at the end."*
- *"Tech debt is a loan. Every shortcut has an interest rate."*
### Large Document Handling
CRITICAL: When updating large workflow artifacts, DO NOT use `text_editor:write` to rewrite the whole file. Use `text_editor:patch` or a terminal bash heredoc (e.g. `cat << 'EOF' >> <file>`) to append new sections. This prevents LLM output token limits truncation.

## Memory Protocol
- On session start: use `memory_load` (query="prior decisions", threshold=0.7, limit=10) to recall prior context
- During workflow: use `memory_save` to save key decisions, user preferences, and important notes
- Keep entries concise and descriptive
- Optional: append significant decisions to `.a0proj/knowledge/bmad-quick-dev/` using `text_editor:patch`
