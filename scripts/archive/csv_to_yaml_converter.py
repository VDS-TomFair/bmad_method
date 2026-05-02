#!/usr/bin/env python3
"""CSV → YAML module.yaml converter — Bundle 1, Slice 1.2.

One-time conversion script that reads all module-help.csv files and produces
corresponding module.yaml files following the A0-adapted schema.

Source: SPEC.md §1.2, §Migration Guide
Upstream reference: .a0proj/upstream/BMAD-METHOD/src/bmm-skills/module.yaml

Usage:
    python scripts/csv_to_yaml_converter.py              # Convert all CSVs
    python scripts/csv_to_yaml_converter.py --dry-run     # Preview without writing
    python scripts/csv_to_yaml_converter.py --verify      # Verify row counts
"""
import csv
import io
import sys
from pathlib import Path

import yaml

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = PLUGIN_ROOT / "skills"

# CSV column order (13 columns from upstream schema)
CSV_COLUMNS = [
    "module", "skill", "display-name", "menu-code", "description",
    "action", "args", "phase", "after", "before",
    "required", "output-location", "outputs",
]

# Module name → human-readable name mapping
MODULE_NAMES = {
    "core": "BMAD Core Utilities",
    "bmm": "BMad Method Agile-AI Driven-Development",
    "tea": "Test Engineering Architecture",
    "cis": "Creative Innovation Suite",
    "bmb": "BMad Builder",
}

# CSV source → YAML target mapping
# The routing extension reads from skills/*/module-help.csv glob
CONVERSION_MAP = {
    "bmad-bmm": {
        "csv": SKILLS_DIR / "bmad-bmm" / "module-help.csv",
        "yaml": SKILLS_DIR / "bmad-bmm" / "module.yaml",
        "code": "bmm",
    },
    "bmad-tea": {
        "csv": SKILLS_DIR / "bmad-tea" / "module-help.csv",
        "yaml": SKILLS_DIR / "bmad-tea" / "module.yaml",
        "code": "tea",
    },
    "bmad-cis": {
        "csv": SKILLS_DIR / "bmad-cis" / "module-help.csv",
        "yaml": SKILLS_DIR / "bmad-cis" / "module.yaml",
        "code": "cis",
    },
    "bmad-bmb": {
        "csv": SKILLS_DIR / "bmad-bmb" / "module-help.csv",
        "yaml": SKILLS_DIR / "bmad-bmb" / "module.yaml",
        "code": "bmb",
    },
    "bmad-init": {
        # Init CSV lives at root, output goes to core/ subdir
        "csv": SKILLS_DIR / "bmad-init" / "module-help.csv",
        "yaml": SKILLS_DIR / "bmad-init" / "core" / "module.yaml",
        "code": "core",
    },
}


def parse_csv(csv_path: Path) -> list[dict]:
    """Parse a module-help.csv file and return list of row dicts."""
    rows = []
    text = csv_path.read_text(encoding="utf-8")
    reader = csv.DictReader(io.StringIO(text))
    for row in reader:
        # Convert 'required' to boolean
        required_raw = row.get("required", "false").strip().lower()
        row["required"] = required_raw in ("true", "yes", "1")
        # Strip whitespace from all string fields
        for key in CSV_COLUMNS:
            if key == "required":
                continue
            if key in row:
                row[key] = row[key].strip()
        rows.append(row)
    return rows


def build_yaml_module(code: str, rows: list[dict]) -> dict:
    """Build the YAML module structure from CSV rows.

    Schema (A0-adapted from upstream module.yaml):
    - code: module code (bmm, tea, cis, bmb, core)
    - name: human-readable module name
    - workflows: list of workflow entries

    Each workflow entry has all 13 CSV columns as fields.
    Source: SPEC §Migration Guide — CSV columns → YAML fields mapping.
    """
    return {
        "code": code,
        "name": MODULE_NAMES.get(code, code),
        "workflows": rows,
    }


def write_yaml(yaml_path: Path, data: dict) -> None:
    """Write YAML module data to file."""
    yaml_path.parent.mkdir(parents=True, exist_ok=True)
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(
            data,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=120,
        )


def convert_module(name: str, info: dict, dry_run: bool = False) -> dict:
    """Convert one CSV module to YAML. Returns stats dict."""
    csv_path = info["csv"]
    yaml_path = info["yaml"]
    code = info["code"]

    if not csv_path.exists():
        return {"name": name, "error": f"CSV not found: {csv_path}"}

    rows = parse_csv(csv_path)
    data = build_yaml_module(code, rows)

    stats = {
        "name": name,
        "csv_path": str(csv_path),
        "yaml_path": str(yaml_path),
        "row_count": len(rows),
        "code": code,
    }

    if dry_run:
        stats["action"] = "DRY RUN - would write"
        # Verify YAML round-trips
        yaml_text = yaml.dump(data, default_flow_style=False,
                              allow_unicode=True, sort_keys=False, width=120)
        reloaded = yaml.safe_load(yaml_text)
        assert reloaded["code"] == code
        assert len(reloaded["workflows"]) == len(rows)
        stats["round_trip"] = "OK"
    else:
        write_yaml(yaml_path, data)
        stats["action"] = "WRITTEN"
        # Verify written file parses
        verified = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        assert verified["code"] == code
        assert len(verified["workflows"]) == len(rows)
        stats["verify"] = "OK"

    return stats


def main():
    dry_run = "--dry-run" in sys.argv
    verify = "--verify" in sys.argv

    print(f"CSV → YAML Converter (dry_run={dry_run}, verify={verify})")
    print(f"Plugin root: {PLUGIN_ROOT}")
    print(f"Skills dir: {SKILLS_DIR}")
    print()

    all_stats = []
    total_rows = 0
    errors = []

    for name, info in CONVERSION_MAP.items():
        stats = convert_module(name, info, dry_run=dry_run)
        all_stats.append(stats)

        if "error" in stats:
            errors.append(stats["error"])
            print(f"  ❌ {name}: {stats['error']}")
        else:
            total_rows += stats["row_count"]
            print(f"  ✅ {name}: {stats['row_count']} rows → {stats['yaml_path']} ({stats.get('action', '?')})")

    print()
    print(f"Total: {total_rows} workflow rows across {len(all_stats)} modules")

    if errors:
        print(f"Errors: {len(errors)}")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    if verify:
        print()
        print("Verification:")
        for stats in all_stats:
            if "error" in stats:
                continue
            yaml_path = Path(stats["yaml_path"])
            data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
            wf_count = len(data["workflows"])
            ok = "✅" if wf_count == stats["row_count"] else "❌"
            print(f"  {ok} {stats['name']}: {wf_count} workflows (expected {stats['row_count']})")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
