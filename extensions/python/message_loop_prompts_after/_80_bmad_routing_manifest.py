"""
BmadRoutingManifest — Dynamically build BMAD routing table from all module-help.csv files.

Reads from skills/*/module-help.csv (single source of truth) instead of a
pre-compiled _config/bmad-help.csv aggregate. This eliminates the two-file
duplication problem — adding a workflow to module-help.csv is all that's needed.

Injects a compact routing table into extras_temporary["bmad_routing_manifest"]
for bmad-master to use on every message loop.
"""

import csv
import io
from pathlib import Path
from helpers.extension import Extension
from helpers import files
from agent import LoopData

# Dynamic path resolution — works regardless of install method (plugin, symlink, dev)
_PLUGIN_ROOT = Path(__file__).resolve().parents[3]
_SKILLS_DIR = _PLUGIN_ROOT / "skills"
_BMAD_CONFIG_DIR = _PLUGIN_ROOT / "skills" / "bmad-init" / "_config"
BMAD_MASTER_PROFILE = "bmad-master"

# Skill directory name → module code used in module-help.csv
SKILL_TO_MODULE = {
    "bmad-init": "core",
    "bmad-bmm": "bmm",
    "bmad-bmb": "bmb",
    "bmad-cis": "cis",
    "bmad-tea": "tea",
}

# Phase → relevant modules map
PHASE_MODULES = {
    "ready":            ["core", "bmm", "bmb", "tea", "cis"],
    "1-analysis":       ["core", "bmm"],
    "2-planning":       ["core", "bmm"],
    "3-solutioning":    ["core", "bmm", "tea"],
    "4-implementation": ["core", "bmm", "tea"],
    "bmb":              ["core", "bmb"],
    "cis":              ["core", "cis"],
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


def _collect_routing_rows(active_modules: list | None) -> list[str]:
    """
    Read all skills/*/module-help.csv files and return routing row strings.
    Filters by active_modules if provided.
    """
    routing_rows = []

    # Discover all module-help.csv files sorted by skill name
    csv_files = sorted(_SKILLS_DIR.glob("*/module-help.csv"))

    for csv_path in csv_files:
        skill_name = csv_path.parent.name

        try:
            content = csv_path.read_text(encoding="utf-8")
            reader = csv.DictReader(io.StringIO(content))

            for row in reader:
                module = row.get("module", "").strip()
                row_phase = row.get("phase", "").strip()
                name = row.get("name", "").strip()
                code = row.get("code", "").strip()
                # module-help.csv uses 'agent'; bmad-help.csv uses 'agent-name'
                agent_name = (
                    row.get("agent-name", "").strip()
                    or row.get("agent", "").strip()
                )
                # display name optional — use agent-display-name or agent-title or agent_name
                agent_display = (
                    row.get("agent-display-name", "").strip()
                    or row.get("agent-title", "").strip()
                    or agent_name
                )

                # Skip rows without agent — these are standalone tools
                # invoked directly by any agent, not routed through bmad-master
                # (matches original design intent from official BMAD)
                if not agent_name:
                    continue

                # Filter by active modules if phase-specific
                if active_modules and module not in active_modules:
                    continue

                routing_rows.append(
                    f"`{code}` {name} [{module}/{row_phase}] → {agent_name} ({agent_display})"
                )

        except Exception:
            continue

    return routing_rows


class BmadRoutingManifest(Extension):
    """
    Injects compact BMAD routing manifest into bmad-master context.

    Phase-aware: loads all modules when phase=ready, otherwise loads
    phase-relevant modules only.

    Reads dynamically from all skills/*/module-help.csv files — no compiled
    aggregate needed. Adding a workflow to module-help.csv is immediately
    reflected in the routing table without any sync step.
    """

    async def execute(self, loop_data: LoopData = LoopData(), **kwargs):
        if not self.agent or self.agent.config.profile != BMAD_MASTER_PROFILE:
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
                state = state_path.read_text(encoding="utf-8")
                for line in state.splitlines():
                    if line.strip().startswith("- Phase:"):
                        phase = line.split(":", 1)[1].strip().lower()
                        active_modules = PHASE_MODULES.get(phase)
                        break

            # Collect routing rows from all module-help.csv files
            routing_rows = _collect_routing_rows(active_modules)

            if not routing_rows:
                return

            phase_note = (
                f"(phase={phase}, showing modules: {', '.join(active_modules)})"
                if active_modules
                else "(all modules)"
            )
            routing_table = "\n".join(routing_rows)

            manifest_prompt = (
                f"# BMAD Routing Table {phase_note}\n"
                f"Match user request → read agent-name → map to profile → call_subordinate.\n"
                f"Multiple matches → show list, ask user to pick. Never route from memory.\n\n"
                f"{routing_table}"
            )

            loop_data.extras_temporary["bmad_routing_manifest"] = manifest_prompt

        except Exception:
            pass
