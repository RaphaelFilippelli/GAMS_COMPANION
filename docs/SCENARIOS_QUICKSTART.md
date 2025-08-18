# Scenarios (v1)

A scenario is a small YAML file describing changes to scalars, parameters, sets, and optional equation includes.
When you supply a scenario, the runner:
1. Copies your model to a temp workspace
2. Builds a `patch.gdx` containing your edits (Transfer API)
3. Copies any `equation` includes into the temp workspace
4. Injects a tiny `autoload_patch.inc` and `$include` in the temp `main.gms`
5. Runs the model

## Minimal example

```yaml
id: BaselineA
description: Raise a scalar and add a set element
edits:
  scalars:
    - name: capA
      value: 3.0
  parameters:
    - name: demand
      updates:
        - key: [A, 2025]
          value: 120.0
  sets:
    - name: Tech
      add: [B2]
      remove: []
  equations:
    includes: []   # or: [eq_patches/new_constraint.inc]
meta:
  author: Rapha
```

## Using it

- **Streamlit (sync run)**: add the path to the scenario YAML to the UI and call `run_gams(..., scenario_yaml=path)`.
- **Programmatic**:
```python
from core.model_runner_merg import run_gams
gdx = run_gams('toy_model', 'main.gms', 'results.gdx', options={'Lo':2}, scenario_yaml='scenarios/BaselineA.yaml')
print(gdx)
```

If the model already has its own patch loader, this approach still works: `$load` lines will load the symbols from `patch.gdx`. The source model folder is never modified.