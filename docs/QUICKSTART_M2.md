# QUICKSTART_M2.md — Scenarios, Compare Runs & Batch

## A) Compare runs (UI)
1. `streamlit run src/app/main.py`
2. Run two scenarios (or just two runs).
3. Go to **Compare Runs** page → pick two runs + a symbol → export CSV.

## B) Scenario basics (CLI)
```powershell
# Validate and build a patch.gdx for a scenario
python -m tools.scenario .\scenarios\BaselineA.yaml --out .\tmp_patch

# Run with scenario via UI
#   - Put the YAML path in sidebar → Scenario YAML path
#   - Click Run GAMS

# Run with scenario via code
python - << 'PY'
from src.core.model_runner_v49 import run_gams
gdx = run_gams('toy_model','main.gms','results.gdx', options={'logoption':2}, scenario_yaml='scenarios/BaselineA.yaml')
print(gdx)
PY
```

## C) Batch runs
```powershell
# Run every *.yaml in scenarios/
python -m tools.run_matrix --model toy_model --main main.gms --gdx-out results.gdx --scenarios scenarios
# See runs/matrix_summary.json
```
