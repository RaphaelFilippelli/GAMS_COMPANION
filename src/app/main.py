from __future__ import annotations
import streamlit as st
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from core.model_runner import run_gams
from core.gdx_io import read_gdx, export_excel

st.set_page_config(page_title="GAMS Companion", layout="wide")

st.title("GAMS Companion — MVP")
st.write("Edit → Run → Excel in a few clicks (starter UI)")

work_dir = st.text_input("Model folder", value=str(Path("toy_model").resolve()))
gms_file = st.text_input("Main .gms file", value="main.gms")
gdx_out = st.text_input("Output GDX", value="results.gdx")
lo = st.number_input("Log option (Lo)", value=2, step=1)

if st.button("Run GAMS"):
    with st.spinner("Running GAMS…"):
        try:
            gdx = run_gams(work_dir, gms_file, gdx_out, options={"Lo": int(lo)})
            st.success(f"Run OK → {gdx}")
            st.session_state["last_gdx"] = str(gdx)
        except Exception as e:
            st.error(f"Run failed: {e}")

if "last_gdx" in st.session_state:
    gdx = st.session_state["last_gdx"]
    if st.button("Export Excel"):
        with st.spinner("Reading GDX and exporting to Excel..."):
            data = read_gdx(gdx)
            xlsx = Path(gdx).with_suffix(".xlsx")
            export_excel(data, xlsx)
            
            # Count symbols with actual data
            total_symbols = len(data)
            symbols_with_data = sum(1 for df in data.values() if len(df) > 0)
            
            if symbols_with_data > 0:
                st.success(f"Excel exported with {symbols_with_data}/{total_symbols} symbols containing data.")
            else:
                st.warning(f"Excel exported, but all {total_symbols} symbols are empty. This may be because the model was compiled but not solved, or the symbols contain no data.")
            
            with open(xlsx, "rb") as f:
                st.download_button("Download Excel", data=f, file_name=xlsx.name)

st.caption("Tip: use the bundled toy model to validate your setup.")
