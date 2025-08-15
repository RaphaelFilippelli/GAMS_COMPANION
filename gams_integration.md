# GAMS Integration Guide

## Run a job (Python)
```python
from core.model_runner import run_gams
gdx_out = run_gams(
    work_dir="C:/path/to/model",
    gms_file="main.gms",
    gdx_out="results.gdx",
    options={"Lo": 2, "gdxcompress": 1}
)
```

## Read/Write GDX
```python
from core.gdx_io import read_gdx, export_excel
data = read_gdx("runs/run_2025.../raw.gdx")
export_excel(data, "results.xlsx", units={"ReducedP":"kg P/yr"})
```

## Patch‑in workflow (concept)
1) Create a **patch.gdx** containing only edited symbols.  
2) In the temp model copy, set:  
   `option gdxincname="patch.gdx"; $gdxin patch.gdx $load` (before declarations).  
3) Solve. Patched symbols override defaults.
