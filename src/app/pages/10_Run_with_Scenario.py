import sys
from pathlib import Path
import streamlit as st

# Make sure repo root is on path so we can import core.*
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.model_runner_merg import run_gams

st.set_page_config(page_title="Run with Scenario", layout="wide")
st.title("🧪 Run with Scenario (simple page)")

col1, col2 = st.columns(2)
with col1:
    model_dir = st.text_input("Model folder", value=str((ROOT / "toy_model").resolve()))
    main_gms = st.text_input("Main .gms file", value="main.gms")
    gdx_out = st.text_input("Expected GDX output filename", value="results.gdx")

with col2:
    scenario_yaml = st.text_input("Scenario YAML (optional)", help="Path to a scenario YAML to apply before the run.")
    lo = st.selectbox("LogOption (Lo)", [0,1,2,3,4], index=2)
    keep_temp = st.checkbox("Keep temp workspace", value=False)

if st.button("Run now"):
    try:
        gdx = run_gams(model_dir, main_gms, gdx_out, options={"Lo": lo}, keep_temp=keep_temp, scenario_yaml=scenario_yaml or None)
        st.success(f"Run OK → {gdx}")
    except Exception as e:
        st.error(str(e))