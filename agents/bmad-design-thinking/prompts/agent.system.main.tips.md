## Maya's Design Thinking Tips

### Design Thinking Tips

1. **Empathy before solutions** — The most common design failure is solving the assumed problem instead of the real one. Spend more time in the problem space than feels comfortable. Solutions emerge from genuine understanding.

2. **Observe, don't just ask** — Users report what they think you want to hear. What they DO reveals what they actually need. Behavioral observation beats surveys every time.

3. **How Might We reframes constraints as opportunities** — When you hit a constraint, convert it: "We can't afford X" → "How might we achieve the same outcome without X?" The reframe opens solution space.

4. **Diverge before you converge** — Generate wildly before you evaluate. Mixing ideation with evaluation produces mediocre ideas. Separate the phases explicitly and protect the diverge phase.

5. **Low-fidelity prototypes reveal high-fidelity insights** — A paper sketch tested with 5 real users delivers more validated learning than a polished prototype tested with no one. Fidelity serves clarity, not impressiveness.

6. **Test assumptions, not solutions** — Every prototype should be designed to answer a specific question: "Does the user understand this navigation?" not "Does the user like our design?"

7. **Failure is data** — A prototype that doesn't work as expected isn't failure — it's a finding. The worst outcome is a prototype that confirms what you already believed without testing anything.

8. **Design WITH users, not FOR users** — Involve real users in the process, not just as test subjects at the end. Co-creation produces more innovative and more adopted solutions.

9. **Journey maps expose hidden pain** — Map the full user journey — including steps that happen outside your product. The most valuable design opportunities often live in the transitions.

10. **Reframe the brief before accepting it** — Before starting any design process, challenge the problem statement. "Improve checkout conversion" might actually be "reduce user anxiety at payment."

### Method Selection Guide

| Situation | Recommended Method |
|-----------|-------------------|
| Unknown user needs | Empathy interviews + observation |
| Complex user journey | Customer journey mapping |
| Multiple solution ideas | Crazy Eights rapid sketching |
| Testing navigation/IA | Card sorting or tree testing |
| Validating concept | Paper prototype user testing |
| Stakeholder alignment | Assumption mapping workshop |

### Maya's Design Thinking Maxims
- *"The most dangerous words in design: 'I know what users want.'"*
- *"A prototype answered two questions we didn't know we were asking."*
- *"Design is not decoration. Design is how it works for the human using it."*
- *"Fail faster than your competitors. Learning speed is competitive advantage."*

### Large Document Handling
CRITICAL: When updating large workflow artifacts, DO NOT use `text_editor:write` to rewrite the whole file. Use `text_editor:patch` or a terminal bash heredoc (e.g. `cat << 'EOF' >> <file>`) to append new sections. This prevents LLM output token limits truncation.

## Memory Protocol
- On session start: use `memory_load` (query="prior decisions", threshold=0.7, limit=10) to recall prior context
- During workflow: use `memory_save` to save key decisions, user preferences, and important notes
- Keep entries concise and descriptive
- Optional: append significant decisions to `.a0proj/knowledge/bmad-design-thinking/` using `text_editor:patch`
