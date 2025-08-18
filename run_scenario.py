from core.model_runner_merg import run_gams

gdx = run_gams(
    work_dir="toy_model",
    gms_file="main.gms",
    gdx_out="results.gdx",
    options={"Lo": 2},
    scenario_yaml="scenarios/BaselineA.yaml",  # or leave out to run baseline
)
print("GDX:", gdx)
