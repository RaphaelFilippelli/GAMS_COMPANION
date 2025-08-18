from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

from tools.inspect_symbols import main as _noop  # just to ensure import path works

TEMPLATE = [
  {"name": "TotalObjective", "symbol": "obj", "agg": "sum"},
  {"name": "Cost_2025", "symbol": "cost", "where": {"key2": "2025"}, "agg": "sum"},
  {"name": "Flow_A_to_B", "symbol": "flow", "where": {"key1": "A", "key2": "B"}, "agg": "sum"}
]

HELP = """
This file lists KPI requests. Each item:
- name: column name in the summary
- symbol: symbol name from your results
- where: optional filters on key1..key7 (string or list of strings)
- agg: sum|mean (default: sum)
Adjust 'symbol' names and filters to your model.
"""

def main():
    ap = argparse.ArgumentParser(description="Create a starter KPIs YAML for a run")
    ap.add_argument("--run-dir", required=True, help="runs/<stamp> folder")
    ap.add_argument("--out", default="docs/kpis_example.yaml", help="Path to write YAML")
    args = ap.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    data = {"_help": HELP.strip(), "kpis": TEMPLATE}
    out.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    print(f"Wrote {out}. Now edit 'symbol' names to match your model.")

if __name__ == "__main__":
    main()