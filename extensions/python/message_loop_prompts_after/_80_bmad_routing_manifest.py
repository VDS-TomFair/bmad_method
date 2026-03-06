from pathlib import Path
from helpers.extension import Extension
from helpers import files
from agent import LoopData

# Dynamic path resolution — works regardless of install method (plugin, symlink, dev)
_PLUGIN_ROOT = Path(__file__).resolve().parents[3]
_BMAD_HELP_CSV = _PLUGIN_ROOT / "skills" / "bmad-init" / "_config" / "bmad-help.csv"
_BMAD_CONFIG_DIR = _PLUGIN_ROOT / "skills" / "bmad-init" / "_config"
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


def _resolve_state_file(agent) -> Path | None:
    """Resolve the BMAD state file from the active project context."""
    try:
        from helpers import projects
        project_name = projects.get_context_project_name(agent.context)
        if project_name:
            folder = Path(projects.get_project_folder(project_name))
            state = folder / ".a0proj" / "instructions" / "02-bmad-state.md"
            if state.exists():
                return state
    except Exception:
        pass

    # Fallback: scan /a0/usr/projects/ for most-recently-modified BMAD state
    try:
        projects_dir = Path("/a0/usr/projects")
        if projects_dir.exists():
            candidates = []
            for proj in projects_dir.iterdir():
                if not proj.is_dir():
                    continue
                state = proj / ".a0proj" / "instructions" / "02-bmad-state.md"
                if state.exists():
                    candidates.append((state.stat().st_mtime, state))
            if candidates:
                candidates.sort(reverse=True)
                return candidates[0][1]
    except Exception:
        pass

    return None


class BmadRoutingManifest(Extension):
    """Injects compact bmad routing manifest into bmad-master context.
    Phase-aware: loads all modules when phase=ready, otherwise loads phase-relevant modules only.
    Also injects resolved BMAD config paths so prompts never need hardcoded paths.
    """

    async def execute(self, loop_data: LoopData = LoopData(), **kwargs):
        if not self.agent or self.agent.config.profile != BMAD_MASTER_PROFILE:
            return

        csv_path = str(_BMAD_HELP_CSV)
        if not files.exists(csv_path):
            return

        try:
            # Inject resolved paths so prompts can reference them
            loop_data.extras_temporary["bmad_paths"] = (
                f"bmad_config_dir: {_BMAD_CONFIG_DIR}\n"
                f"bmad_plugin_root: {_PLUGIN_ROOT}"
            )

            # Read current phase from state file
            phase = "ready"
            active_modules = None
            state_path = _resolve_state_file(self.agent)
            if state_path:
                state = state_path.read_text()
                for line in state.splitlines():
                    if line.strip().startswith("- Phase:"):
                        phase = line.split(":", 1)[1].strip().lower()
                        active_modules = PHASE_MODULES.get(phase)
                        break

            # Parse CSV
            csv_content = files.read_file(csv_path)
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
