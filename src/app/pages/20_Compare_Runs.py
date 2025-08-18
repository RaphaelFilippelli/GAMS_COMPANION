
import sys
from pathlib import Path
import pandas as pd
import streamlit as st

# Ensure repo root on sys.path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Prefer duckdb if available
try:
    import duckdb  # type: ignore
except Exception:
    duckdb = None

# Optional fallback GDX reader
def _read_gdx(run_dir: Path):
    try:
        from core.gdx_io_merg import read_gdx_transfer_full  # project-specific
        vals, marg, kinds = read_gdx_transfer_full(str(run_dir / "raw.gdx"))
        return vals or {}, marg or {}, kinds or {}
    except Exception:
        return {}, {}, {}

st.set_page_config(page_title="Compare Runs v1.1", layout="wide")
st.title("🔍 Compare Runs")

runs_root = Path("runs")
run_dirs = sorted([p for p in runs_root.glob("*") if p.is_dir()], key=lambda p: p.name, reverse=True)
run_names = [d.name for d in run_dirs]

# Check for pre-selected runs from batch scenarios page
default_run_a_index = 0
default_run_b_index = 1 if len(run_dirs) > 1 else 0

if "compare_run_a" in st.session_state and st.session_state["compare_run_a"] in run_names:
    default_run_a_index = run_names.index(st.session_state["compare_run_a"]) + 1  # +1 for "(select)" option
if "compare_run_b" in st.session_state and st.session_state["compare_run_b"] in run_names:
    default_run_b_index = run_names.index(st.session_state["compare_run_b"]) + 1  # +1 for "(select)" option

col1, col2 = st.columns(2)
with col1:
    run_a = st.selectbox("Run A", ["(select)"] + run_names, index=default_run_a_index)
with col2:
    run_b = st.selectbox("Run B", ["(select)"] + run_names, index=default_run_b_index)

# Clear session state after using the pre-selected values
if "compare_run_a" in st.session_state:
    del st.session_state["compare_run_a"]
if "compare_run_b" in st.session_state:
    del st.session_state["compare_run_b"]

join_type = st.selectbox("Join type", ["inner", "outer"], index=0)
st.caption("Inner = only matching keys. Outer = keep non-overlapping rows (NaN where missing).")

def _load_values(run_dir: Path) -> dict[str, pd.DataFrame]:
    db = run_dir / "results.duckdb"
    if duckdb and db.exists():
        con = duckdb.connect(str(db))
        df_vals = con.execute("SELECT * FROM symbol_values").fetchdf()
        con.close()
        sym_to_df = {}
        for name, df in df_vals.groupby("symbol"):
            # rebuild per-symbol tidy frames
            cols = [f"key{i}" for i in range(1, 8)] + ["value"]
            cols = [c for c in df.columns if c in cols]
            sym_to_df[name] = df[cols].copy()
        return sym_to_df
    # fallback to GDX
    vals, _, _ = _read_gdx(run_dir)
    return vals

def _norm7(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for i in range(1, 8):
        c = f"key{i}"
        if c not in df.columns:
            df[c] = None
    cols = [f"key{i}" for i in range(1, 8)] + ([c for c in df.columns if c == "value"])
    return df[cols]

if run_a and run_a != "(select)" and run_b and run_b != "(select)":
    vals_a = _load_values(runs_root / run_a)
    vals_b = _load_values(runs_root / run_b)
    syms = sorted(set(vals_a.keys()) & set(vals_b.keys()))
    pick = st.selectbox("Symbol", ["(select)"] + syms, index=0)
    if pick and pick != "(select)":
        df_a = _norm7(vals_a[pick]).rename(columns={"value":"value_A"})
        df_b = _norm7(vals_b[pick]).rename(columns={"value":"value_B"})
        merged = pd.merge(df_a, df_b, on=[f"key{i}" for i in range(1,8)], how=join_type)
        if "value_A" in merged.columns and "value_B" in merged.columns:
            merged["delta"] = merged["value_B"] - merged["value_A"]
            with pd.option_context('mode.use_inf_as_na', True):
                merged["pct_delta"] = merged["delta"] / merged["value_A"]
        st.write(f"Rows: {len(merged):,}")
        st.dataframe(merged, use_container_width=True)

        # CSV export
        st.download_button(
            "Download CSV",
            data=merged.to_csv(index=False).encode("utf-8"),
            file_name=f"compare_{pick}_{run_a}_vs_{run_b}_{join_type}.csv",
            mime="text/csv"
        )

        # XLSX export (always create at least one visible sheet)
        def _safe_write_xlsx(df: pd.DataFrame, out_path: Path):
            if df.empty:
                df = pd.DataFrame({"info": ["No rows for this selection"]})
            with pd.ExcelWriter(out_path, engine="openpyxl") as w:
                df.to_excel(w, sheet_name="diff", index=False)

        xlsx_name = f"compare_{pick}_{run_a}_vs_{run_b}_{join_type}.xlsx"
        xlsx_path = runs_root / xlsx_name
        if st.button("Download XLSX"):
            _safe_write_xlsx(merged, xlsx_path)
            st.success(f"Saved {xlsx_path}")
            st.download_button("Click to download XLSX", data=xlsx_path.read_bytes(), file_name=xlsx_name, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    st.info("Select two runs to compare.")
