
# NEXT STEPS

## 1) Compare Runs v1.1
- Replace your compare page with `src/app/pages/20_Compare_Runs.py` from this shipment.
- New: join type (inner/outer) and **XLSX export** with a guaranteed visible sheet.

## 2) Preflight
- Add `src/app/pages/00_Preflight.py`.
- Checks GAMS API/Transfer availability, gams.exe path, pandas/numpy, temp write, etc.

## 3) Batch (no KPIs) + Export Pack
- Batch (no KPIs yet):
  ```
  python -m tools.run_batch_simple --model toy_model --main main.gms --gdx-out results.gdx --scenarios scenarios
  ```
- Export pack:
  ```
  python -m tools.export_pack runs\<stamp>
  ```

You can skip KPIs now and still use batch + export pack. KPIs and auto-suggest (LLM) can come later.
