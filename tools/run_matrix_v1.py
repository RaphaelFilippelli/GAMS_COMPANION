from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml
import pandas as pd

from core.model_runner_merg import run_gams
from tools.kpis import extract_kpis

def main():
    ap = argparse.ArgumentParser(description="Run a batch of scenarios and extract KPIs")
    ap.add_argument("--model", required=True)
    ap.add_argument("--main", required=True)
    ap.add_argument("--gdx-out", required=True)
    ap.add_argument("--scenarios", required=True, help="Folder with *.yaml or a YAML list file")
    ap.add_argument("--kpis", help="KPI preset YAML (list of {name, symbol, where?, agg?})")
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

    kpis = None
    if args.kpis:
        kpis = yaml.safe_load(Path(args.kpis).read_text(encoding="utf-8"))
        if not isinstance(kpis, list):
            raise SystemExit("--kpis YAML must be a list")

    rows = []
    for sp in scen_paths:
        print(f"Running {sp.name} ...")
        gdx = run_gams(args.model, args.main, args.gdx_out, options={"Lo":2}, keep_temp=args.keep_temp, scenario_yaml=str(sp))
        run_dir = Path(gdx).parent
        row = {"scenario": sp.stem, "run_dir": str(run_dir), "gdx": str(gdx)}
        if kpis:
            df = extract_kpis(run_dir, kpis)
            for _, r in df.iterrows():
                row[r["name"]] = r["value"]
        rows.append(row)

    out_dir = Path("runs")
    out_dir.mkdir(exist_ok=True, parents=True)
    df_all = pd.DataFrame(rows)
    (out_dir / "matrix_summary.json").write_text(json.dumps(rows, indent=2), encoding="utf-8"))
    df_all.to_csv(out_dir / "matrix_summary.csv", index=False)
    print(f"Wrote {out_dir/'matrix_summary.csv'} and matrix_summary.json")

if __name__ == "__main__":
    main()