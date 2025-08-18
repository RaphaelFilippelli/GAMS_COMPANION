
import sys, os, platform
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Preflight", layout="wide")
st.title("🛫 Preflight Check")

rows = []

def add_row(name, status, detail=""):
    rows.append({"check": name, "status": status, "detail": detail})

# Python & OS
add_row("OS", "ok", platform.platform())
add_row("Python", "ok", f"{sys.version}")

# GAMS API
try:
    from gams import GamsWorkspace  # type: ignore
    ws = GamsWorkspace()
    add_row("GAMS API import", "ok", f"system={ws.system_directory}")
except Exception as e:
    add_row("GAMS API import", "fail", str(e))

# GAMS Transfer API
try:
    from gams import transfer as gt  # type: ignore
    Container = getattr(gt, "Container", None)
    if Container is None:
        raise AttributeError("transfer.Container not found")
    _ = Container()  # sanity-construct a container
    add_row("GAMS Transfer API", "ok", "transfer.Container available")
except Exception as e:
    add_row("GAMS Transfer API", "fail", repr(e))

# Where is the 'gams' module coming from?
try:
    import gams as _g
    add_row("gams module path", "ok", getattr(_g, "__file__", "(unknown)"))
except Exception as e:
    add_row("gams module path", "fail", str(e))


# GAMS_HOME
gh = os.getenv("GAMS_HOME") or "(not set)"
add_row("GAMS_HOME env", "ok" if gh != "(not set)" else "warn", gh)

# gams.exe
gams_home = os.getenv("GAMS_HOME") or "C:\\GAMS\\49.6"
exe_candidates = [Path(gams_home) / "gams.exe", Path(gams_home) / "gams" / "gams.exe"]
exe_found = next((p for p in exe_candidates if p.exists()), None)
add_row("gams.exe", "ok" if exe_found else "warn", str(exe_found or "not found"))

# pandas/numpy
try:
    import pandas as pd, numpy as np  # type: ignore
    add_row("pandas", "ok", pd.__version__)
    add_row("numpy", "ok", np.__version__)
except Exception as e:
    add_row("pandas/numpy import", "fail", str(e))

# Temp write
try:
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as td:
        test = Path(td) / "ok.txt"
        test.write_text("ok", encoding="utf-8")
    add_row("Temp write", "ok", "write/read ok")
except Exception as e:
    add_row("Temp write", "fail", str(e))

st.dataframe(rows, use_container_width=True)
st.caption("If the Control API fails with a 'memoryview/buffer' error, the app will fall back to gams.exe when possible.")
