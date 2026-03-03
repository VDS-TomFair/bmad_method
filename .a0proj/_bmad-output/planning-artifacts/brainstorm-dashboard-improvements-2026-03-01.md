# 🧠 Brainstorm: BMAD Status Dashboard Improvements

**Facilitator:** Carson (BMAD Elite Brainstorming Specialist)  
**Participant:** Vanja  
**Date:** 2026-03-01  
**Session Type:** Diverge → Converge — Dashboard Feature Ideation  
**Subject:** BMAD Status Dashboard (PRD v1.1 | Story-001 Implemented)

---

## 🎯 SESSION CONTEXT

What we know is already built or spec'd:
- ✅ Agent Health Check Widget (Story-001 — LIVE)
- ✅ Dark Mode Toggle (FR-07 — in PRD)
- ✅ Architecture defined
- ✅ Comprehensive test strategy in place

Today's mission: Open up the idea space. Find the next 10x improvements — from polish to wild.

---

## 🔥 WARM-UP: WORST IDEAS FIRST

> *(Psychological safety move — get the terrible ideas out fast, lower defenses, signal that this is a safe space)*

The absolute WORST things we could add to the BMAD Status Dashboard:

1. **A mandatory 30-second animated intro every time you open it** — sponsored by a fictional enterprise vendor
2. **Replace all icons with Comic Sans text labels** — maximum readability, minimum taste
3. **Add a random motivational quote that covers the entire screen** before you can see any data
4. **A dashboard that only works when Mercury is not in retrograde** — astrology-aware CI/CD
5. **Make every status update trigger a full-page confetti explosion** — celebrate! Always! Even errors!

> ✅ Warm-up complete. Room is loose. Now let's go find the real gold.

---

## 🔬 ROUND 1: SCAMPER THE EXISTING DASHBOARD

*SCAMPER = Substitute · Combine · Adapt · Modify · Put to other uses · Eliminate · Reverse*

### SUBSTITUTE — What can we swap for something better?

6. **Substitute static health badges → live animated pulse indicators**  
   Agents that are healthy pulse green. Agents degraded pulse amber. Dead agents show flatline.

7. **Substitute text phase labels → visual phase journey map**  
   Instead of "Phase: Planning" show a horizontal journey rail — Analysis → Planning → Solutioning → Implementation — with a glowing dot on the current phase.

8. **Substitute manual refresh → WebSocket real-time push**  
   Dashboard state streams live. No polling. No refresh button. It just *knows*.

### COMBINE — What can we fuse together?

9. **Combine agent health + artifact inventory in one panel**  
   See which agent owns which artifact. If agent is down, the owned artifacts go amber too. Cascading health awareness.

10. **Combine phase state + story progress tracker**  
    In Phase 4 (Implementation), show a mini Kanban: Stories → In Dev → Testing → Done. Linked to the actual story files in `/implementation-artifacts/`.

11. **Combine dark mode toggle + system preference sync**  
    Auto-detect OS dark/light mode. FR-07 already exists — extend it to be *smart*.

### ADAPT — What can we borrow from another context?

12. **Adapt GitHub Actions workflow visualization → BMAD workflow pipeline view**  
    Show the active BMAD workflow as a directed graph. Each node is a step. Completed = green check. Current = spinning. Blocked = red.

13. **Adapt VS Code's minimap → artifact minimap sidebar**  
    Small scrollable thumbnail of all planning + implementation artifacts. Click to open in viewer pane.

14. **Adapt Datadog's service map → BMAD agent dependency map**  
    Visual graph of which agents feed into which. BMad Master orchestrating. Arrows showing data flow.

### MODIFY / MAGNIFY — What can we amplify or tune?

15. **Magnify the "What's happening NOW" signal**  
    Giant, unmistakable hero section: current phase, active agent, active workflow step. Make it impossible to miss.

16. **Modify the test strategy section → live test results feed**  
    If tests are running, stream pass/fail counts in real time. A green number climbing is deeply satisfying.

17. **Modify layout density → user-configurable widget grid**  
    Drag-and-drop widget placement. Resize panels. Save layout to localStorage. Every developer has different priorities.

### PUT TO OTHER USES — What unexpected uses could this serve?

18. **Use dashboard as onboarding surface**  
    First-time users see a guided tour overlaid on the dashboard. "This is your agent roster. This is your current phase." Interactive tooltips.

19. **Use dashboard as a project status report generator**  
    One-click "Export Status Report" → produces a markdown or PDF snapshot of current phase, agent health, artifact inventory, open stories.

20. **Use dashboard as a demo/presentation mode**  
    Clean, full-screen, logo visible, confidential data redacted. Show clients or stakeholders without exposing internal details.

### ELIMINATE — What can we remove to make it faster/cleaner?

21. **Eliminate the need to manually check artifact files**  
    Surface artifact status directly: which artifacts exist, which are drafts, which are approved — right on the dashboard.

22. **Eliminate context switching to check state**  
    Embed a mini state viewer: current `02-bmad-state.md` contents rendered as structured UI, not raw markdown.

### REVERSE — What if we flipped the dashboard's purpose?

23. **Reverse: instead of monitoring the past → predict the future**  
    "Based on current state, next expected step is: Create Architecture (estimated by Winston)." Forward-looking assistant panel.

24. **Reverse: instead of a single user dashboard → multi-user team view**  
    Show which team member is on which agent, who last updated which artifact. Collaboration awareness.

---

## 💥 ROUND 2: DIMENSIONAL EXPLOSION

*Five dimensions. Fast fire. No judgment. YES AND everything.*

### 🎨 UX & VISUAL DESIGN

25. **Keyboard shortcut palette** — press `?` to reveal all shortcuts. Power user delight.
26. **Micro-animations on state transitions** — phase change triggers a subtle slide. Agent goes healthy triggers a gentle pulse. Motion as communication.
27. **Color-blind accessible palette** — not just dark mode. Full WCAG AA compliance. Ship it.
28. **Compact vs. Expanded view toggle** — developers on small screens need compact. Stakeholders on 4K monitors want expanded.
29. **Custom dashboard themes** — beyond dark/light. "BMAD Blue", "Terminal Green", "High Contrast". Let developers *feel at home*.
30. **Breadcrumb trail at top** — Project → Phase → Active Workflow → Current Step. Always know where you are.

### ⚡ NEW FEATURES

31. **Decision Log Viewer** — surface key ADRs and decisions made during the project. Architectural decisions shouldn't live only in files.
32. **Phase Duration Tracker** — how long has the project been in each phase? Timestamps per phase transition. Identify bottlenecks.
33. **Session Replay Timeline** — chronological log of everything that happened: agent activations, workflow executions, artifact saves. Project history at a glance.
34. **"What's Next" Recommendation Widget** — AI-powered: "You're in Phase 3 with architecture done. Recommended: Create Epics & Stories with Bob." Contextual guidance.
35. **Dependency Graph for Stories** — visualize story dependencies. Which stories block which. Clear the path.
36. **Artifact Diff Viewer** — click any artifact to see its current version vs. previous. Track how your PRD evolved.

### 🔌 INTEGRATIONS

37. **Langfuse Trace Viewer embedded panel** — since Langfuse is already a skill, surface trace data directly in dashboard. See LLM call chains without leaving.
38. **GitHub commit correlation** — link implementation stories to actual commits. Story-001 → commit SHA. Close the loop.
39. **Webhook / notification system** — fire a webhook on phase transitions. Connect to Slack, Discord, email. The BMAD dashboard becomes an event source.
40. **Export → Confluence / Notion push** — one-click export of the current project status page to a wiki. Stakeholder communication automated.
41. **Git status panel** — show uncommitted changes in the project directory. Are the new agent files saved? Has the PRD been committed?

### 🛠️ DEVELOPER EXPERIENCE

42. **Debug Mode overlay** — show raw `02-bmad-state.md` JSON, active skill paths, loaded config aliases. X-ray into the framework.
43. **State Transition Simulator** — manually trigger phase transitions in a sandbox mode. Test without touching real state.
44. **Mock Agent Health for offline dev** — develop and test the dashboard when the agent runtime is down. Fake data mode.
45. **CLI companion command** — `bmad status` in terminal renders a compact ASCII version of the dashboard. Terminal-first developers rejoice.
46. **Hot-reload on state file changes** — `inotifywait` on `02-bmad-state.md`. Dashboard updates the instant the file changes. Zero latency feedback.
47. **Performance timing panel** — how long did the last workflow step take? Which agents are slow? Optimization surface.

### 🚀 WILD CARD ROUND

*These are the ideas that made us laugh. Which means at least one of them becomes next quarter's feature.*

48. **AI-Generated Session Narrative** — at end of day, an LLM reads the state and writes: "Today, Vanja and Winston tackled the architecture. Three ADRs were logged. The PRD evolved significantly. Tomorrow: epics." A daily standup, written by the framework itself.

49. **BMAD Health Score / Gamification** — projects score points for: completing phases, hitting Definition-of-Done, running tests. A leaderboard across projects. Absurd? Absolutely. Motivating? Completely.

50. **Multi-Project Dashboard** — switch between active BMAD projects. Compare phases. See which project is ahead. Portfolio view.

51. **Voice Announcements** — optional Web Speech API integration. "Phase transition complete. You are now in Implementation. Good luck, Vanja." Like a mission control voice.

52. **Shareable Dashboard Permalink** — generate a read-only URL that shows current project status. Share with a stakeholder without giving them repo access.

53. **Dashboard Time-Lapse** — record state snapshots over time. Play back the entire project as a time-lapse. Watch your PRD evolve, your architecture emerge, your stories get completed. *This is the project story told visually.*

54. **Emoji Status Indicators** — alongside technical status, show a team-configured emoji. "🚀 Shipping" / "🔥 On fire" / "🤔 Planning". Human signal in a technical tool.

---

## 🎯 CONVERGENCE: TOP 10 PRIORITY IDEAS

*Evaluated on: Impact × Feasibility × Novelty*

| # | Idea | Impact | Feasibility | Novelty | **Score** |
|---|------|--------|-------------|---------|----------|
| 1 | **Live WebSocket real-time push** (idea #8) | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 🔥 HIGH |
| 2 | **Phase Journey Map visual rail** (idea #7) | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 🔥 HIGH |
| 3 | **BMAD Workflow Pipeline View** (idea #12) | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | 🔥 HIGH |
| 4 | **"What's Next" Recommendation Widget** (idea #34) | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | 🔥 HIGH |
| 5 | **One-click Status Report Export** (idea #19) | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 🔥 HIGH |
| 6 | **Debug Mode overlay** (idea #42) | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ✅ SOLID |
| 7 | **Session Replay Timeline** (idea #33) | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ✅ SOLID |
| 8 | **Hot-reload on state file changes** (idea #46) | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ✅ SOLID |
| 9 | **Artifact Diff Viewer** (idea #36) | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ✅ SOLID |
| 10 | **AI-Generated Session Narrative** (idea #48) | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 🌟 WILD CARD |

---

## 🃏 WILD CARD PRESERVE LIST

*Ideas too good to lose — park them for future sprints:*

- Dashboard Time-Lapse (idea #53) — flagship feature for v2
- Multi-Project Portfolio View (idea #50) — enterprise play
- Webhook/notification system (idea #39) — ecosystem integrator
- BMAD Health Score gamification (idea #49) — developer engagement
- Shareable permalink (idea #52) — stakeholder communication

---

## 💡 RECOMMENDED NEXT STORIES (Draft)

Based on this session, Carson recommends the following story candidates for Bob (Scrum Master) to formalize:

1. **Story-002**: Phase Journey Map Widget — visual horizontal rail showing BMAD phases with current phase highlighted
2. **Story-003**: Debug Mode Panel — overlay showing raw state, config aliases, and loaded skill context
3. **Story-004**: Hot-Reload State Watcher — filesystem watch on `02-bmad-state.md` triggering UI refresh
4. **Story-005**: Status Report Export — one-click markdown/PDF snapshot of current project state
5. **Story-006**: "What's Next" Recommendation Panel — context-aware next-step suggestion based on current phase + state

---

## 📊 SESSION STATS

- **Total ideas generated:** 54
- **Techniques used:** Worst Idea First · SCAMPER (7 lenses) · Dimensional Explosion (5 dimensions) · Wild Card Round
- **Convergence method:** Impact × Feasibility × Novelty matrix
- **Top 10 selected:** 5 HIGH priority · 4 SOLID · 1 Wild Card
- **Parking lot (future):** 5 ideas preserved
- **Draft stories surfaced:** 5

---

*Generated by Carson 🧠 — BMAD Elite Brainstorming Specialist*  
*BMAD Creative Intelligence Suite — Problem Solving Workflow*  
*"The idea that made everyone laugh last Tuesday is the patent you file next Tuesday."*
