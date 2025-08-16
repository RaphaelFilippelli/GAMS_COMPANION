from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.model_runner_merg import run_gams

def main():
    ap = argparse.ArgumentParser(description="Run a batch of scenarios")
    ap.add_argument("--model", required=True, help="Model folder")
    ap.add_argument("--main", required=True, help="Main .gms file (e.g., main.gms)")
    ap.add_argument("--gdx-out", required=True, help="Expected output GDX filename")
    ap.add_argument("--scenarios", required=True, help="Folder containing scenario YAMLs or a YAML list file")
    ap.add_argument("--keep-temp", action="store_true", help="Keep temp workspaces")
    args = ap.parse_args()

    scen_paths = []
    scen_arg = Path(args.scenarios)
    if scen_arg.is_dir():
        scen_paths = sorted([p for p in scen_arg.glob("*.yaml")])
    else:
        data = yaml.safe_load(scen_arg.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            print("List YAML must be a list of file paths", file=sys.stderr); sys.exit(2)
        scen_paths = [Path(p) for p in data]

    runs = []
    for sp in scen_paths:
        print(f"Running {sp.name} ...")
        gdx = run_gams(args.model, args.main, args.gdx_out, options={}, keep_temp=args.keep_temp, scenario_yaml=str(sp))
        runs.append({"scenario": sp.stem, "gdx": str(gdx), "run_dir": str(Path(gdx).parent)})

    out = Path("runs") / "matrix_summary.json"
    out.write_text(json.dumps(runs, indent=2), encoding="utf-8")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
