from __future__ import annotations
import argparse, json
from pathlib import Path
from src.core.scenario import load_yaml, validate_scenario, build_patch_gdx

def main():
    ap = argparse.ArgumentParser(description="Scenario validator and patch.gdx builder")
    ap.add_argument("yaml", help="Path to scenario YAML")
    ap.add_argument("--out", help="Output folder for patch.gdx", default=".")
    args = ap.parse_args()

    data = load_yaml(args.yaml)
    scen = validate_scenario(data)
    print(f"Scenario OK: {scen.id}")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    patch = build_patch_gdx(out, scen)
    print(f"Wrote: {patch}")

if __name__ == "__main__":
    main()
