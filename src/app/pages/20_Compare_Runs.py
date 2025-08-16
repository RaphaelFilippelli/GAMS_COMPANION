import sys
from pathlib import Path
import pandas as pd
import streamlit as st

# --- Robust import path setup ---
import sys
from pathlib import Path

THIS = Path(__file__).resolve()
REPO_ROOT = THIS.parents[3]   # <repo>/  (pages -> app -> src -> <repo>)
SRC_ROOT  = REPO_ROOT / "src"

for p in (REPO_ROOT, SRC_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

try:
    from src.core.gdx_io_merg import read_gdx_full  # preferred (package import)
except ModuleNotFoundError:
    # fallback if 'src' isn't treated as a package
    from core.gdx_io_merg import read_gdx_full
# --- end path setup ---


st.set_page_config(page_title="Compare Runs", layout="wide")

st.title("🔍 Compare Runs")

runs_root = Path("runs")
run_dirs = sorted([p for p in runs_root.glob("*") if p.is_dir()], key=lambda p: p.name, reverse=True)

col1, col2 = st.columns(2)
with col1:
    run_a = st.selectbox("Run A", ["(select)"] + [d.name for d in run_dirs], index=0)
with col2:
    run_b = st.selectbox("Run B", ["(select)"] + [d.name for d in run_dirs], index=1 if len(run_dirs) > 1 else 0)

def _load_values(run_dir: Path) -> tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]:
    # Prefer DuckDB if present (fast), else fallback to reading raw.gdx
    db = run_dir / "results.duckdb"
    if db.exists():
        con = duckdb.connect(str(db))
        df_vals = con.execute("SELECT * FROM symbol_values").fetchdf()
        sym_to_df = {}
        for name, df in df_vals.groupby("symbol"):
            # rebuild per-symbol tidy frames
            cols = [f"key{i}" for i in range(1, 8)] + ["value"]
            cols = [c for c in df.columns if c in cols]
            sym_to_df[name] = df[cols].copy()
        con.close()
        return sym_to_df, {}
    # fallback: read raw.gdx
    gdx = run_dir / "raw.gdx"
    vals, marg, _ = read_gdx_full(gdx) if gdx.exists() else ({}, {}, {})
    return vals, marg

def _symbol_list(vals_a: dict[str, pd.DataFrame], vals_b: dict[str, pd.DataFrame]) -> list[str]:
    names = sorted(set(vals_a.keys()) & set(vals_b.keys()))
    return names

def _norm7(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for i in range(1, 8):
        col = f"key{i}"
        if col not in df.columns:
            df[col] = None
    cols = [f"key{i}" for i in range(1, 8)] + ([c for c in df.columns if c == "value"])
    return df[cols]

if run_a and run_a != "(select)" and run_b and run_b != "(select)":
    vals_a, _ = _load_values(runs_root / run_a)
    vals_b, _ = _load_values(runs_root / run_b)
    syms = _symbol_list(vals_a, vals_b)
    pick = st.selectbox("Symbol", ["(select)"] + syms, index=0)
    if pick and pick != "(select)":
        df_a = _norm7(vals_a[pick])
        df_b = _norm7(vals_b[pick])
        merged = pd.merge(df_a, df_b, on=[f"key{i}" for i in range(1,8)], how="inner", suffixes=("_A", "_B"))
        if "value_A" in merged.columns and "value_B" in merged.columns:
            merged["delta"] = merged["value_B"] - merged["value_A"]
            with pd.option_context('mode.use_inf_as_na', True):
                merged["pct_delta"] = merged["delta"] / merged["value_A"]
        st.write(f"Rows: {len(merged):,}")
        st.dataframe(merged, use_container_width=True)
        st.download_button(
            "Download CSV",
            data=merged.to_csv(index=False).encode("utf-8"),
            file_name=f"compare_{pick}_{run_a}_vs_{run_b}.csv",
            mime="text/csv"
        )
else:
    st.info("Select two runs to compare.")
