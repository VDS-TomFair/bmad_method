from python.helpers.extension import Extension
from python.helpers import files
from agent import LoopData

BMAD_HELP_CSV = "/a0/skills/bmad-init/_config/bmad-help.csv"
BMAD_STATE_FILE = "/a0/usr/projects/a0_bmad_method/.a0proj/instructions/02-bmad-state.md"
BMAD_MASTER_PROFILE = "bmad-master"

# Phase → relevant modules map
PHASE_MODULES = {
    "ready":          ["core", "bmm", "bmb", "tea", "cis"],
    "1-analysis":     ["core", "bmm"],
    "2-planning":     ["core", "bmm"],
    "3-solutioning":  ["core", "bmm", "tea"],
    "4-implementation": ["core", "bmm", "tea"],
    "bmb":            ["core", "bmb"],
    "cis":            ["core", "cis"],
}


class BmadRoutingManifest(Extension):
    """Injects compact bmad routing manifest into bmad-master context.
    Phase-aware: loads all modules when phase=ready, otherwise loads phase-relevant modules only.
    """

    async def execute(self, loop_data: LoopData = LoopData(), **kwargs):
        if not self.agent or self.agent.config.profile != BMAD_MASTER_PROFILE:
            return

        if not files.exists(BMAD_HELP_CSV):
            return

        try:
            # Read current phase from state file
            active_modules = None
            if files.exists(BMAD_STATE_FILE):
                state = files.read_file(BMAD_STATE_FILE)
                for line in state.splitlines():
                    if line.strip().startswith("- Phase:"):
                        phase = line.split(":", 1)[1].strip().lower()
                        active_modules = PHASE_MODULES.get(phase)
                        break

            # Parse CSV
            csv_content = files.read_file(BMAD_HELP_CSV)
            lines = csv_content.strip().split("\n")
            if len(lines) < 2:
                return

            headers = lines[0].split(",")
            col = {h.strip(): i for i, h in enumerate(headers)}

            routing_rows = []
            for line in lines[1:]:
                parts = line.split(",")
                if len(parts) < 9:
                    continue

                module = parts[col.get("module", 0)].strip()
                row_phase = parts[col.get("phase", 1)].strip()
                name = parts[col.get("name", 2)].strip()
                code = parts[col.get("code", 3)].strip()
                agent_name = parts[col.get("agent-name", 8)].strip()
                agent_display = parts[col.get("agent-display-name", 10)].strip() if len(parts) > 10 else ""

                if not agent_name:
                    continue

                # Filter by active modules if phase-specific
                if active_modules and module not in active_modules:
                    continue

                routing_rows.append(
                    f"`{code}` {name} [{module}/{row_phase}] → {agent_name} ({agent_display})"
                )

            if not routing_rows:
                return

            phase_note = f"(phase={phase}, showing modules: {', '.join(active_modules)})" if active_modules else "(all modules)"
            routing_table = "\n".join(routing_rows)

            manifest_prompt = f"""# BMAD Routing Table {phase_note}
Match user request → read agent-name → map to profile → call_subordinate.
Multiple matches → show list, ask user to pick. Never route from memory.

{routing_table}"""

            loop_data.extras_temporary["bmad_routing_manifest"] = manifest_prompt

        except Exception:
            pass
