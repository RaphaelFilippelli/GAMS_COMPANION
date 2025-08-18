
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml
import sys

# Ensure <repo>/src is on sys.path so 'core.*' imports resolve
THIS = Path(__file__).resolve()
REPO = THIS.parents[1]          # .../<repo>
SRC = REPO / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
    
from core.model_runner_merg import run_gams

def main():
    ap = argparse.ArgumentParser(description="Run a batch of scenarios (no KPIs)")
    ap.add_argument("--model", required=True)
    ap.add_argument("--main", required=True)
    ap.add_argument("--gdx-out", required=True)
    ap.add_argument("--scenarios", required=True, help="Folder with *.yaml or a YAML list file")
    ap.add_argument("--keep-temp", action="store_true")
    args = ap.parse_args()

    scen_paths = []
    scen_arg = Path(args.scenarios)
    if scen_arg.is_dir():
        scen_paths = sorted(scen_arg.glob("*.yaml"))
    else:
        data = yaml.safe_load(scen_arg.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise SystemExit("List YAML must be a list of file paths")
        scen_paths = [Path(p) for p in data]

    rows = []
    for sp in scen_paths:
        print(f"Running {sp.name} ...")
        gdx = run_gams(args.model, args.main, args.gdx_out, options={"Lo":2}, keep_temp=args.keep_temp, scenario_yaml=str(sp))
        rows.append({"scenario": sp.stem, "gdx": str(gdx), "run_dir": str(Path(gdx).parent)})

    out = Path("runs") / "matrix_summary.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
