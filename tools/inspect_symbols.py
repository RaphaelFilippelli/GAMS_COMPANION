from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd

def _from_duck(run_dir: Path) -> pd.DataFrame | None:
    try:
        import duckdb
    except Exception:
        return None
    db = run_dir / "results.duckdb"
    if not db.exists():
        return None
    con = duckdb.connect(str(db))
    try:
        df = con.execute("SELECT DISTINCT symbol FROM symbol_values").fetchdf()
        kinds = None
        try:
            kinds = con.execute("SELECT DISTINCT symbol, kind FROM symbol_values").fetchdf()
        except Exception:
            pass
        return df if kinds is None else kinds
    finally:
        con.close()

def _from_gdx(run_dir: Path) -> pd.DataFrame | None:
    gdx = run_dir / "raw.gdx"
    if not gdx.exists():
        return None
    try:
        from core.gdx_io_merg import read_gdx_transfer_full
    except Exception as e:
        print("Could not import core.gdx_io_merg; falling back to names only via Transfer API.")
        try:
            from gams import transfer as gt
            db = gt.Container(str(gdx))
            rows = []
            for sym in db:
                rows.append({"symbol": sym.name, "dim": getattr(sym, "dimension", None)})
            import pandas as pd
            return pd.DataFrame(rows)
        except Exception as e2:
            print("Transfer fallback failed:", e2)
            return None
    vals, marg, kinds = read_gdx_transfer_full(str(gdx))
    rows = []
    for name, df in (vals or {}).items():
        rows.append({"symbol": name, "dim": sum(c.startswith("key") for c in df.columns), "rows": len(df)})
    return pd.DataFrame(rows)

def main():
    ap = argparse.ArgumentParser(description="List symbols available in a run directory")
    ap.add_argument("run_dir", help="Path to runs/<stamp> folder")
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    if not run_dir.exists():
        raise SystemExit(f"Run dir not found: {run_dir}")

    df = _from_duck(run_dir) or _from_gdx(run_dir)
    if df is None:
        raise SystemExit("Could not read symbol list. Ensure results.duckdb or raw.gdx exists.")
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()