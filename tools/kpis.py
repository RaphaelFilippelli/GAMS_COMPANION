from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd

try:
    import duckdb  # type: ignore
except Exception:
    duckdb = None

def _load_symbol_values(run_dir: Path) -> pd.DataFrame:
    db = run_dir / "results.duckdb"
    if duckdb and db.exists():
        con = duckdb.connect(str(db))
        df = con.execute("SELECT * FROM symbol_values").fetchdf()
        con.close()
        return df
    # Fallback: try raw.gdx via project reader if available
    try:
        from core.gdx_io_merg import read_gdx_transfer_full
        vals, _, _ = read_gdx_transfer_full(str(run_dir / "raw.gdx"))
        frames = []
        for name, df in (vals or {}).items():
            if "value" in df.columns:
                df = df.copy()
                df.insert(0, "symbol", name)
                frames.append(df)
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    except Exception:
        return pd.DataFrame()

def _norm7(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for i in range(1,8):
        c = f"key{i}"
        if c not in df.columns:
            df[c] = None
    cols = ["symbol"] + [f"key{i}" for i in range(1,8)] + ["value"]
    return df[[c for c in cols if c in df.columns]]

def extract_kpis(run_dir: str | Path, requests: List[Dict[str, Any]]) -> pd.DataFrame:
    """Compute KPI rows for a run.
    requests: list of {name, symbol, where: {key1: 'A' or ['A','B'], ...}, agg: 'sum'|'mean'}
    Returns DataFrame with columns: name, value
    """
    run_dir = Path(run_dir)
    df = _load_symbol_values(run_dir)
    if df.empty:
        return pd.DataFrame(columns=["name","value"])
    df = _norm7(df)
    out = []
    for req in requests:
        name = req["name"]; symbol = req["symbol"]
        r = df[df["symbol"] == symbol]
        where = req.get("where") or {}
        for k, v in where.items():
            if k not in r.columns:  # ignore unknown filters
                continue
            if isinstance(v, list):
                r = r[r[k].isin([str(x) for x in v])]
            else:
                r = r[r[k] == str(v)]
        if r.empty:
            val = None
        else:
            agg = (req.get("agg") or "sum").lower()
            if agg == "mean":
                val = r["value"].mean()
            else:
                val = r["value"].sum()
        out.append({"name": name, "value": val})
    return pd.DataFrame(out)