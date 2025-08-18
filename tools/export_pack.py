
from __future__ import annotations
import argparse, json, zipfile
from pathlib import Path
from datetime import datetime

FILES_CANDIDATES = ["raw.gdx", "results.duckdb", "results.xlsx", "run.json", "debug_paths.json"]

def main():
    ap = argparse.ArgumentParser(description="Create an export pack (zip) for a run")
    ap.add_argument("run_dir", help="runs/<stamp> folder")
    ap.add_argument("--out", help="Output zip path", default=None)
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    if not run_dir.exists():
        raise SystemExit(f"Run dir not found: {run_dir}")

    out = Path(args.out) if args.out else (run_dir / f"export_pack_{run_dir.name}.zip")
    manifest = {"created": datetime.utcnow().isoformat() + "Z", "run_dir": str(run_dir), "files": []}

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        # Add standard files
        for name in FILES_CANDIDATES:
            p = run_dir / name
            if p.exists():
                z.write(p, arcname=p.name)
                manifest["files"].append({"name": p.name, "size": p.stat().st_size})
        # Add any .lst files
        for lst in run_dir.glob("*.lst"):
            z.write(lst, arcname=lst.name)
            manifest["files"].append({"name": lst.name, "size": lst.stat().st_size})
        # Manifest
        z.writestr("MANIFEST.json", json.dumps(manifest, indent=2))

    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
